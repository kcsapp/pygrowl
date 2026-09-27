from collections import defaultdict
from collections.abc import Iterable, Mapping
from pathlib import Path
from types import UnionType
from typing import (
    Any,
    Literal,
    Self,
    TypeVar,
    Union,
    get_args,
    get_origin,
)

import attrs
from attrs.converters import pipe

from .converters import arg_converter
from .options import CompasArgCollection

_UNION_TYPES = {Union, UnionType}


def _attr_type_list(field: attrs.Attribute) -> list[type]:
    field_type = field.type
    result = (
        []
        if field_type is None
        else [fta for fta in get_args(field_type) if fta is not type(None)]
        if get_origin(field_type) in _UNION_TYPES or field_type in _UNION_TYPES
        else [field_type]
    )
    return result


def _arg_to_flag(arg_name: str) -> str:
    return "--" + arg_name.replace("_", "-")


def _flag_to_arg(flag: str) -> str:
    return flag.strip("-").replace("-", "_")


def _str_allowed(type_objs: Any) -> bool:
    for type_obj in type_objs:
        if (
            type_obj is str
            or get_origin(type_obj) is Literal
            and type(next(iter(get_args(type_obj)), None)) is str
        ):
            return True

    return False


def validate_input_type(cls: type, attribute: attrs.Attribute, value: Any):
    """Validates that passed values have a valid type at runtime."""
    del cls
    if value is None:
        return

    value_type = type(value)
    for attr_type in _attr_type_list(attribute):
        if value_type is attr_type or value_type is get_origin(attr_type):
            return

        if get_origin(attr_type) is Literal and value in get_args(attr_type):
            return

    raise ValueError(
        f"{attribute.name} does not support type {value_type} (allowed: {attribute.type})"
    )


T = TypeVar("T")


def convert_input_iterables[T](
    value: T | Iterable[T] | None, field: attrs.Attribute
) -> T | CompasArgCollection[T] | None:
    """Converts passed iterables to one of the COMPAS argument collections: Vector, Set, or Range.

    This method attempts a conversion for each COMPAS argument collection kind provided on the field
    and returns the first conversion that succeeds.
    """
    if value is None:
        return value

    type_list = _attr_type_list(field)
    str_allowed = _str_allowed(type_list)
    for allowed_type in type_list:
        if isinstance(value, CompasArgCollection) or not isinstance(value, Iterable):
            return value

        if str_allowed and isinstance(value, (str, bytes)):
            return value  # type: ignore

        if hasattr(allowed_type, "from_iterable"):
            try:
                return allowed_type.from_iterable(value)
            except ValueError:
                pass


def field_value_to_arg(value: Any, field: attrs.Attribute) -> str | None:
    """Generate a command line representation for a given field value.

    This method matches a field's value to the type annotation it represents and use that type's
    converter to generate the appropriate command-line representation."""
    if value is None:
        return None

    type_list = _attr_type_list(field)
    for attr_type in type_list:
        instance_type = get_origin(attr_type) or attr_type
        if instance_type is Literal and value in get_args(attr_type):
            return arg_converter[type(value)].to_arg(value)

        if isinstance(value, (str, bytes)) and instance_type not in (str, bytes):
            continue

        if isinstance(value, instance_type):
            return arg_converter[attr_type].to_arg(value)

    raise TypeError(f"Value type '{type(value)}' is not valid for field {field}")


def field_value_from_arg(arg: str, field: attrs.Attribute) -> Any:
    """Generate python configuration-class representation for a given command line argument.

    This method matches a field's value to the type annotation it represents and use that type's
    converter to generate the appropriate python value."""
    for attr_type in _attr_type_list(field):
        converter = arg_converter.get(attr_type)
        if converter:
            try:
                value = converter.from_arg(arg)
                return value
            except ValueError:
                pass

    raise TypeError(f"Argument '{arg}' cannot be parsed by converters for field {field}")


def transform_growl_args(_, fields: list[attrs.Attribute]):
    """Add missing 'flag' definitions using the default representation."""
    new_fields = []
    for f in fields:
        attr_type = f.type
        if not attr_type:
            raise ValueError("Attribute type must be defined")

        new_field = f

        # Try to convert iterables into CompasArgCollections; incorporate runtime type checking
        cac_converter = attrs.Converter(convert_input_iterables, takes_field=True)
        new_field = new_field.evolve(
            converter=pipe(cac_converter, f.converter) if f.converter else cac_converter,
            validator=[f.validator, validate_input_type] if f.validator else validate_input_type,
        )

        if "flag" not in f.metadata:
            new_field = new_field.evolve(metadata={**f.metadata, "flag": _arg_to_flag(f.name)})

        new_fields.append(new_field)

    return new_fields


### ------------------------------------------------------------- ###
### Definitions used to construct GrowlArgs configuration classes ###
### ------------------------------------------------------------- ###

_MISSING = "__MISSING__"


class GrowlArgs(attrs.AttrsInstance):
    @classmethod
    def from_argv(cls, argv: list[str]) -> tuple[Self, list[str]]:
        """Convert an argv list representing a growl-args class into a class instance.

        This function extracts arguments and associated values into a dict of mappings from
        field name to value for all arguments matching a field in the supplied `cls`.
        It leaves arguments not mapped to a COMPAS argument untouched for downstream parsing,
        returning them in the second tuple output.
        """
        if not (attrs.has(cls) and attrs.fields(cls)):
            raise TypeError(
                f"Expected an attrs class with at least one field attribute; got '{cls}'"
            )
        if next(iter(argv), None) == getattr(cls, "command", _MISSING):
            argv = argv[1:]

        option_fields = {f.name: f for f in attrs.fields(cls)}

        kwargs = defaultdict(list)
        remaining_args: list[str] = []
        curr_arg = None
        for arg in argv:
            if arg.startswith("-"):
                arg_name = _flag_to_arg(arg)
                if arg_name not in option_fields:
                    remaining_args.append(arg)
                    curr_arg = None
                else:
                    curr_arg = kwargs[option_fields[arg_name]]
            elif curr_arg is not None:
                curr_arg.append(arg)
            else:
                remaining_args.append(arg)

        input_kwargs = {k: " ".join(v) for k, v in kwargs.items()}
        inst = cls(**{k.name: field_value_from_arg(v, k) for k, v in input_kwargs.items()})
        return inst, remaining_args

    def to_argv(self, remove_defaults: bool = False) -> list[str]:
        """Convert a growl options class to command-line arguments."""
        argv: list[str] = []
        growl_command = getattr(type(self), "command", _MISSING)
        if growl_command != _MISSING:
            argv.append(growl_command)

        for field in attrs.fields(self):
            flag = field.metadata.get("flag")
            if not flag:
                raise ValueError(f"Argument flag not defined for '{field.name}': {field.metadata=}")

            value = getattr(self, field.name)
            if remove_defaults and value == field.default:
                continue

            arg_value = field_value_to_arg(value, field)
            if arg_value is not None:
                argv.extend((flag, arg_value))

        return argv

    def localize(self, path: str, arg_names: Iterable[str], as_default: bool = False) -> Self:
        """Ensure the arguments specified are prefixed by the provided path."""
        changes = {}
        root_path = Path(path)
        for name in arg_names:
            value = getattr(self, name, None)
            if value:
                if not value.startswith(path):
                    changes[name] = str(root_path / value)
            elif as_default:
                changes[name] = str(root_path)

        return attrs.evolve(self, **changes) if changes else self

    def evolve(self, **changes: Any) -> Self:
        return attrs.evolve(self, **changes) if changes else self


################################################################################
### Exported functions                                                       ###
###  * growl_field: define attrs.field attributes with growl-args details    ###
###  * growl_args: freeze attrs on a class and add from- and to-argv methods ###
################################################################################


def GrowlField(
    *,
    description: str | None = None,
    flag: str | None = None,
    arg_options: Mapping[str, Any] | None = None,
    **kwargs,
) -> Any:
    """Construct an attrs.field with growl argument converter options."""
    metadata = dict(kwargs.pop("metadata", None) or {})
    if description:
        metadata["description"] = description
    if flag:
        metadata["flag"] = flag
    if arg_options:
        metadata["arg_options"] = arg_options
    return attrs.field(metadata=metadata, **kwargs)


def growl_transform(cls: type[GrowlArgs]) -> type[GrowlArgs]:
    """Transform the decorated class into a frozen-attrs class with from- and to-argv methods."""
    return attrs.frozen(field_transformer=transform_growl_args)(cls)
