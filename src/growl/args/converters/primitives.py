from enum import Enum

from .base import TypedArgConverter, arg_converter


class BoolArgFormat(Enum):
    ONE_ZERO = ("1", "0")
    TRUE_FALSE = ("TRUE", "FALSE")
    YES_NO = ("YES", "NO")
    ON_OFF = ("ON", "OFF")


@arg_converter
class BoolArgConverter(TypedArgConverter[bool]):
    _TRUES, _FALSES = zip(*(arg_format.value for arg_format in BoolArgFormat))

    def to_arg(self, value: bool, arg_format: BoolArgFormat = BoolArgFormat.TRUE_FALSE, **_) -> str:
        true_str, false_str = arg_format.value
        return true_str if value else false_str

    def from_arg(self, arg: str, **_) -> bool:
        if arg in self._TRUES:
            return True
        elif arg in self._FALSES:
            return False
        else:
            raise ValueError(f"Invalid boolean representation: '{arg}'")


@arg_converter
class StrArgConverter(TypedArgConverter[str]):
    def to_arg(self, value: str, **_) -> str:
        return value

    def from_arg(self, arg: str, **_) -> str:
        return arg


@arg_converter
class IntArgConverter(TypedArgConverter[int]):
    def to_arg(self, value: int, **_) -> str:
        return str(value)

    def from_arg(self, arg: str, **_) -> int:
        return int(arg)


@arg_converter
class FloatArgConverter(TypedArgConverter[float]):
    def to_arg(self, value: float, precision: int | None = None, **_) -> str:
        if precision:
            return format(value, f".{precision}f")
        return str(value)

    def from_arg(self, arg: str, **_) -> float:
        return float(arg)
