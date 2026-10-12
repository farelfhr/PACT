"""Logical fixture/policy identifiers, distinct from PACT wire resource IDs."""

from dataclasses import dataclass
import re
from typing import Self

from ._validation import DomainValidationError

_IDENTIFIER = re.compile(r"[A-Za-z][A-Za-z0-9._-]{0,95}", re.ASCII)


@dataclass(frozen=True, slots=True)
class _Identifier:
    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str or _IDENTIFIER.fullmatch(self.value) is None:
            raise DomainValidationError("identifier: expected 1..96 ASCII identifier characters")

    @classmethod
    def from_value(cls, value: object) -> Self:
        if type(value) is not str:
            raise DomainValidationError("identifier: expected an exact string")
        return cls(value)


@dataclass(frozen=True, slots=True)
class ActorId(_Identifier):
    pass


@dataclass(frozen=True, slots=True)
class TenantId(_Identifier):
    pass


@dataclass(frozen=True, slots=True)
class ResourceId(_Identifier):
    pass


@dataclass(frozen=True, slots=True)
class RoleId(_Identifier):
    pass


@dataclass(frozen=True, slots=True)
class ResourceTypeId(_Identifier):
    pass


@dataclass(frozen=True, slots=True)
class RuleId(_Identifier):
    pass
