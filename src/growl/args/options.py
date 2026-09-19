from copy import copy
from typing import Iterable, Iterator, Protocol, Self, runtime_checkable

import attrs

from .utils import ItemT_co, NumericT_co, interpret_as_range

_FLOAT_PRECISION = 9


@runtime_checkable
class CompasArgCollection(Protocol[ItemT_co]):
    @classmethod
    def from_iterable(cls, iterable: Iterable) -> Self: ...

    def __iter__(self) -> Iterator: ...


@attrs.define(frozen=True)
class CompasVector(Iterable[ItemT_co]):
    """Represent COMPAS Vector-type argument inputs."""

    values: list[ItemT_co]

    @classmethod
    def from_iterable(cls, iterable: Iterable[ItemT_co]) -> "CompasVector":
        return CompasVector(list(iterable))

    def __iter__(self) -> Iterator[ItemT_co]:
        yield from iter(self.values)


@attrs.define(frozen=True)
class CompasSet(Iterable[ItemT_co]):
    """Represent COMPAS Set-type argument inputs."""

    values: tuple[ItemT_co, ...]

    @classmethod
    def from_iterable(cls, iterable: Iterable[ItemT_co]) -> "CompasSet":
        return CompasSet(tuple(iterable))

    def __iter__(self) -> Iterator[ItemT_co]:
        yield from iter(self.values)


@attrs.define(frozen=True)
class CompasRange(Iterable[NumericT_co]):
    """Represent COMPAS Range-type argument inputs."""

    start: NumericT_co
    count: int
    increment: NumericT_co

    @classmethod
    def from_slice(cls, sl: slice):
        return CompasRange(
            start=sl.start,
            count=int((sl.stop - sl.start) // sl.step),
            increment=sl.step,
        )

    @classmethod
    def from_iterable(cls, iterable: Iterable[NumericT_co]):
        """Validate and extract range properties from an iterable to create a CompasRange.

        Uses an algorithm to try to deduce what range-defining values might have produced the
        provided iterable - robust to skipped or dropped values after the first pair, and to
        non-ordered iterables.

        Args:
            iterable (Iterable[NumericT_co]):
        """
        start, count, increment = interpret_as_range(iterable)
        return CompasRange(start=start, count=count, increment=round(increment, _FLOAT_PRECISION))

    def __iter__(self) -> Iterator[NumericT_co]:
        value, remaining = copy(self.start), self.count
        while remaining != 0:
            yield value
            value = value + self.increment
            remaining -= 1
