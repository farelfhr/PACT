"""Closed plain-data boundaries for immutable domain objects."""

from collections.abc import Callable
from enum import Enum
from typing import TypeVar, cast

T = TypeVar("T")
E = TypeVar("E", bound=Enum)


class DomainValidationError(ValueError):
    """Invalid structure or reference; never a verification verdict."""


def closed(value: object, fields: set[str], label: str) -> dict[str, object]:
    if (type(value) is not dict or any(type(key) is not str for key in value)
            or set(value) != fields):
        raise DomainValidationError(f"{label}: missing or unexpected fields")
    return cast(dict[str, object], value)


def enum_value(kind: type[E], value: object, label: str) -> E:
    if type(value) is not str:
        raise DomainValidationError(f"{label}: expected an exact enum string")
    try:
        return kind(value)
    except ValueError:
        raise DomainValidationError(f"{label}: unsupported enum value") from None


def require_type(value: object, kind: type[T], label: str) -> None:
    if type(value) is not kind:
        raise DomainValidationError(f"{label}: wrong domain type")


def typed_tuple(value: object, kind: type[T], label: str, *, minimum: int = 0,
                maximum: int = 64, unique: bool = True) -> None:
    if type(value) is not tuple or not minimum <= len(value) <= maximum:
        raise DomainValidationError(f"{label}: expected bounded immutable tuple")
    for item in value:
        require_type(item, kind, label)
    if unique and len(set(value)) != len(value):
        raise DomainValidationError(f"{label}: duplicate values")


def array(value: object, parser: Callable[[object], T], label: str, *,
          minimum: int = 0, maximum: int = 64) -> tuple[T, ...]:
    if type(value) is not list or not minimum <= len(value) <= maximum:
        raise DomainValidationError(f"{label}: expected bounded array")
    return tuple(parser(item) for item in value)
