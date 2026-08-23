import re
from typing import Literal, TypeVar

from ..options import CompasRange, CompasSet, CompasVector
from .base import TypedArgConverter, arg_converter

T = TypeVar("T")
NumericT = TypeVar("NumericT", int, float)


@arg_converter
class VectorArgConverter(TypedArgConverter[CompasVector[T]]):
    """Transform to and from COMPAS Vector arguments.

    This converter operates on Vector arguments intended to provide a single vector of values to a
    simulation as space-separated lists on the command line. It uses a primitive-type arg converter
    for the individual items, as a represented by the type arg T.

    Command line to python example:

    "class1 class2 class3" becomes ["class1", "class2", "class3"]

    Python to command line example:

    ["class1", "class2", "class3"] becomes "class1 class2 class3"
    """

    _VEC_PAT = re.compile(r"(\[)?(?P<content>[^\]]+)(\])?")

    def to_arg(self, value: CompasVector[T], shorthand: bool = False, **config) -> str:
        conv = self._converters[0].to_arg

        arg_values = []
        for v in value:
            arg_values.append(conv(v, **config) or "")
            shorthand |= not arg_values[-1]

        if shorthand:
            return "[" + ",".join(arg_values) + "]"
        return " ".join(arg_values)

    def from_arg(self, arg: str, **config) -> CompasVector[T]:
        m = self._VEC_PAT.match(arg)
        if not m:
            raise ValueError(f"Invalid vector specifier: '{arg}'")

        conv = self._converters[0].from_arg
        return CompasVector.from_iterable(
            conv(item, **config) for item in re.split(r"\s*,\s*|\s+", m.group("content"))
        )


@arg_converter
class SetArgConverter(TypedArgConverter[CompasSet[T]]):
    """Transform to and from COMPAS Set arguments.

    This converter operates on Set arguments specified as a collection of values intended to trigger
    simulations at multiple points in its parameter space. When constructing command lines from
    python inputs, it uses a single standard set identifier, which defaults to "s". Note that the
    COMPAS argument Set is distinct from a python `set`, in that it is ordered and can contain
    duplicates; thus we represent it internally as a tuple.

    Command line to python examples:

    "s[A,B,C]"   becomes ["A", "B", "C"]
    "set[A,B,C]" becomes ["A", "B", "C"]

    Python to command line examples:

    ["A", "B", "C"] becomes "s[A,B,C]"
    ["A", "B", "C"] becomes "set[A,B,C]"
    """

    _SET_PAT = re.compile(r"(?i:s|set)\[(?P<content>[^\]]+)\]")

    def to_arg(self, value: CompasSet[T], identifier: Literal["s", "set"] = "s", **config) -> str:
        conv = self._converters[0].to_arg
        return f"{identifier}[" + ",".join(conv(v, **config) for v in value if v is not None) + "]"

    def from_arg(self, arg: str, **config) -> CompasSet[T]:
        m = self._SET_PAT.match(arg)
        if not m:
            raise ValueError(f"Invalid set specifier: '{arg}'")

        conv = self._converters[0].from_arg
        return CompasSet.from_iterable(
            conv(v.strip(), **config) for v in m.group("content").split(",")
        )


@arg_converter
class RangeArgConverter(TypedArgConverter[CompasRange[NumericT]]):
    """Transform to and from COMPAS Range arguments.

    This converter operates on Range arguments specified as a triple with numeric-typed start and
    increment values (which can be ints or floats) and an integer count. It represents these as
    a custom type, CompasRange. When constructing command lines from python inputs, it uses a
    single standard range identifier, which defaults to "r". Also note that CompasRange can be
    constructed from an explicit iterable; an example of this is included below.

    Command line to python examples:

    "[0.0001,5,0.0013]" becomes CompasRange(start=0.0001, count=5, increment=0.0013)
    "r[1,19,2]"         becomes CompasRange(start=1, count=19, increment=2)
    "range[2,3,0.1]"    becomes CompasRange(start=2.0, count=3, increment=0.1)

    Python to command line examples:

    CompasRange(start=0.0001, count=5, increment=0.0013) becomes r[0.0001,5,0.0013]
    CompasRange(start=1, count=19, increment=2)          becomes r[1,19,2]
    CompasRange.from_iterable([2.0, 2.1, 2.2])           becomes range[2,3,0.1]
    """

    _RANGE_PAT = re.compile(
        r"(?i:r|range)?\[\s*(?P<start>[0-9]+(\.[0-9]+)?)\s*,\s*(?P<count>[0-9]+)\s*,\s*(?P<increment>[0-9]*(\.[0-9]+)?)\s*\]"
    )

    def to_arg(
        self, value: CompasRange[NumericT], identifier: Literal["r", "range", ""] = "r", **config
    ) -> str:
        conv = self._converters[0].to_arg
        return f"{identifier}[{conv(value.start, **config)},{value.count},{conv(value.increment, **config)}]"

    def from_arg(self, arg: str, **config) -> CompasRange[NumericT]:
        m = self._RANGE_PAT.match(arg)
        if not m:
            raise ValueError(f"Invalid range specifier: '{arg}'")

        conv = self._converters[0].from_arg
        return CompasRange(
            start=conv(m.group("start"), **config),
            count=int(m.group("count")),
            increment=conv(m.group("increment"), **config),
        )
