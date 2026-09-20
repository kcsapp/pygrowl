import abc
from typing import Literal, TypeVar, get_args, get_origin, get_type_hints

T = TypeVar("T")


def satisfies_type(target: TypeVar | type, test: type) -> bool:
    if isinstance(target, type):
        return target is test
    if target.__constraints__:
        return test in target.__constraints__
    if target.__bound__ is not None:
        return isinstance(test, type) and issubclass(test, target.__bound__)
    return True


class TypedArgConverter[T](metaclass=abc.ABCMeta):
    def __init__(self, *converters: "TypedArgConverter"):
        self._converters = converters

    @abc.abstractmethod
    def to_arg(self, value: T, **config) -> str: ...

    @abc.abstractmethod
    def from_arg(self, arg: str, **config) -> T: ...


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class ArgConverter(metaclass=Singleton):
    _cls_registry: dict[type, type[TypedArgConverter]] = {}
    _inst_registry: dict[type, TypedArgConverter | None] = {}

    def __call__(self, converter_cls: type[TypedArgConverter]) -> type[TypedArgConverter]:
        key: type = get_type_hints(converter_cls.to_arg)["value"]
        if key not in self._cls_registry:
            self._cls_registry[key] = converter_cls

        return self._cls_registry[key]

    def get(self, key: type[T]) -> TypedArgConverter[T] | None:
        if key not in self._inst_registry:
            key_origin, key_args = get_origin(key) or key, get_args(key)
            if key_origin is None and key in self._cls_registry:
                self._inst_registry[key] = self._cls_registry[key]()
            else:
                if key_origin is Literal:
                    key_origin, key_args = type(key_args[0]), []
                for key_cls, converter_cls in self._cls_registry.items():
                    converter_origin = get_origin(key_cls) or key_cls
                    if key_origin != converter_origin:
                        continue

                    cls_args = get_args(key_cls)
                    if len(cls_args) != len(key_args):
                        continue

                    if any(
                        not satisfies_type(cls_arg, key_arg)
                        for cls_arg, key_arg in zip(cls_args, key_args)
                    ):
                        continue

                    subconverters = []
                    for key_arg in key_args:
                        subconverter = self.get(key_arg)
                        if subconverter is None:
                            break

                        subconverters.append(subconverter)
                    else:
                        self._inst_registry[key] = converter_cls(*subconverters)
                        break
                else:
                    self._inst_registry[key] = None

        return self._inst_registry[key]

    def __getitem__(self, key: type[T]) -> TypedArgConverter[T]:
        converter = self.get(key)
        if converter is None:
            raise KeyError(repr(key))
        return converter

    def __contains__(self, key: type[T]) -> bool:
        return self.get(key) is not None


arg_converter = ArgConverter()
