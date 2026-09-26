from collections.abc import Iterable
from typing import TypeVar

ItemT = TypeVar("ItemT")
NumericT_co = TypeVar("NumericT_co", int, float, covariant=True)


def interpret_as_range[NumericT: (int, float)](
    iterable: Iterable[NumericT],
) -> tuple[NumericT, int, NumericT]:
    """Deduce a range which most closely resembles this iterable.

    This uses an algorithm which attempts to interpret any iterable collection of numeric values
    as a range with some regular increment. It is forgiving of missing values in the range and
    arbitrary numerical order, but expects the two smallest values to be separated by the minimum
    increment.

    Args:
        iterable (Iterable[NumericT]): The iterable to interpret as a range

    Returns:
        tuple[NumericT, int, NumericT]: the starting value, number of values, and increment
            defining the deduced range

    Raises:
        StopIteration: if the iterable has less than 2 entries
        ValueError: If the two smallest values are not separated by the minimum interval
    """

    it = iter(iterable)
    first, second = next(it), next(it)
    rng_min, rng_max = min(first, second), max(first, second)
    min_interval = second - first if second > first else first - second
    min_increment = min_interval
    for item in it:
        if item < rng_min:
            interval = rng_min - item

            # min_interval = |past_item - rng_min|, so if rng_min becomes curr_item, we update
            # it to |past_item - curr_item| = |past_item - rng_min| + |curr_item - rng_min|,
            # increacing the past interval by the gap between its minimum and the new minimum
            min_interval = min_interval + interval
            min_interval = min(min_interval, interval)

            rng_min = item
        else:
            interval = item - rng_min
            rng_max = max(rng_max, item)

        if min_increment % interval == 0:
            min_increment = interval
        else:
            (min_inc, max_inc) = (
                (min_increment, interval) if min_increment < interval else (interval, min_increment)
            )
            # set increment to the GCD of increment and inc_test
            # this guarantees that all values in the range are divisible by `increment`
            while min_inc != 0:
                max_inc, min_inc = min_inc, max_inc % min_inc

            min_increment = max_inc

    if min_increment < min_interval:
        raise ValueError(
            "Input iterable is inconsistent; the smallest increment these values can be drawn "
            f"from, {min_increment}, is smaller than the minimum interval found, {min_interval}"
        )

    count = int((rng_max - rng_min + min_increment) // min_increment)

    return rng_min, count, min_increment
