from collections.abc import Iterable, Iterator
from copy import copy
from typing import Protocol, Self, TypeVar, runtime_checkable

import attrs

from .utils import ItemT, NumericT, interpret_as_range

_FLOAT_PRECISION = 9

ItemT_co = TypeVar("ItemT_co", covariant=True)


@runtime_checkable
class CompasArgCollection(Protocol[ItemT_co]):
    @classmethod
    def from_iterable(cls, iterable: Iterable) -> Self: ...

    def __iter__(self) -> Iterator[ItemT_co]: ...


@attrs.define(frozen=True)
class CompasVector(Iterable[ItemT]):
    """Represent COMPAS Vector-type argument inputs."""

    values: list[ItemT]

    @classmethod
    def from_iterable(cls, iterable: Iterable[ItemT]) -> "CompasVector":
        return CompasVector(list(iterable))

    def __iter__(self) -> Iterator[ItemT]:
        yield from iter(self.values)


@attrs.define(frozen=True)
class CompasSet(Iterable[ItemT]):
    """Represent COMPAS Set-type argument inputs."""

    values: tuple[ItemT, ...]

    @classmethod
    def from_iterable(cls, iterable: Iterable[ItemT]) -> "CompasSet":
        return CompasSet(tuple(iterable))

    def __iter__(self) -> Iterator[ItemT]:
        yield from iter(self.values)


@attrs.define(frozen=True)
class CompasRange(Iterable[NumericT]):
    """Represent COMPAS Range-type argument inputs."""

    start: NumericT
    count: int
    increment: NumericT

    @classmethod
    def from_slice(cls, sl: slice):
        return CompasRange(
            start=sl.start,
            count=int((sl.stop - sl.start) // sl.step),
            increment=sl.step,
        )

    @classmethod
    def from_iterable(cls, iterable: Iterable[NumericT]):
        """Validate and extract range properties from an iterable to create a CompasRange.

        Uses an algorithm to try to deduce what range-defining values might have produced the
        provided iterable - robust to skipped or dropped values after the first pair, and to
        non-ordered iterables.

        Args:
            iterable (Iterable[NumericT]):
        """
        start, count, increment = interpret_as_range(iterable)
        return CompasRange(start=start, count=count, increment=round(increment, _FLOAT_PRECISION))

    def __iter__(self) -> Iterator[NumericT]:
        value, remaining = copy(self.start), self.count
        while remaining != 0:
            yield value
            value = value + self.increment
            remaining -= 1
