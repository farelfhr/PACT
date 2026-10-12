"""Provisional immutable scenario data; no execution or approval authority."""

from dataclasses import dataclass
from enum import Enum
import re
from typing import cast

from ..domain import (ActorId, AssertionProfile, ContractBody, Decision, DomainCatalog,
                      DomainValidationError, ResourceId, ResourceTypeId, RuleId,
                      normalize_contract)

MAX_STEPS = 32
_NAME = re.compile(r"[A-Za-z][A-Za-z0-9._-]{0,95}", re.ASCII)
_SEGMENT = re.compile(r"[A-Za-z][A-Za-z0-9_-]{0,31}", re.ASCII)
_DIGEST = re.compile(r"[a-f0-9]{64}", re.ASCII)


class ScenarioValidationError(DomainValidationError):
    """Rejected data; messages omit submitted values, never assign a verdict."""

    def __init__(self, message: str, code: str = "INVALID_STRUCTURE") -> None:
        super().__init__(message)
        self.code = code


def _typed(value: object, kind: type) -> None:
    if type(value) is not kind:
        raise ScenarioValidationError("invalid scenario field type")


def _name(value: object) -> None:
    if type(value) is not str or _NAME.fullmatch(value) is None:
        raise ScenarioValidationError("invalid scenario identifier")


def _items(value: object, kind: type, maximum: int = 64) -> None:
    if type(value) is not tuple or not 1 <= len(value) <= maximum:
        raise ScenarioValidationError("invalid bounded scenario collection")
    for item in value:
        _typed(item, kind)
    if len(set(value)) != len(value):
        raise ScenarioValidationError("duplicate scenario references")


class HttpMethod(Enum):
    GET = "GET"


class ResourceAssertionKind(Enum):
    INTENDED_RESOURCE = "intended_resource"
    NO_DISCLOSURE = "no_protected_resource_disclosure"
    NO_STATE_CHANGE = "no_protected_state_change"


@dataclass(frozen=True, slots=True)
class DeclaredRoute:
    """Catalog data only: literal path segments followed by one ResourceId node."""

    route_ref: str
    segments: tuple[str, ...]
    resource_type: ResourceTypeId

    def __post_init__(self) -> None:
        _name(self.route_ref)
        _typed(self.resource_type, ResourceTypeId)
        if type(self.segments) is not tuple or not 1 <= len(self.segments) <= 8:
            raise ScenarioValidationError("invalid declared path length")
        for segment in self.segments:
            if type(segment) is not str or _SEGMENT.fullmatch(segment) is None:
                raise ScenarioValidationError("invalid literal declared path segment")


@dataclass(frozen=True, slots=True)
class ScenarioDeclarations:
    """Caller-supplied mock-compatible bindings, NOT an approved fixture/contract."""

    fixture_adapter: str
    contract: ContractBody
    fixtures: DomainCatalog
    routes: tuple[DeclaredRoute, ...]

    def __post_init__(self) -> None:
        _name(self.fixture_adapter)
        _typed(self.contract, ContractBody)
        _typed(self.fixtures, DomainCatalog)
        _items(self.routes, DeclaredRoute)
        if len({route.route_ref for route in self.routes}) != len(self.routes):
            raise ScenarioValidationError("duplicate declared route identifiers")
        if any(route.resource_type not in self.fixtures.resource_types for route in self.routes):
            raise ScenarioValidationError("undeclared route resource type")
        try:
            normalize_contract(self.contract)
            for rule in self.contract.rules:
                self.fixtures.validate_rule(rule)
        except DomainValidationError:
            raise ScenarioValidationError("invalid declared candidate policy or fixture bindings") from None

    @property
    def is_authoritative(self) -> bool:
        return False


@dataclass(frozen=True, slots=True)
class ContractReference:
    contract_id: str
    project_ref: str
    version: int
    digest: str

    def __post_init__(self) -> None:
        _name(self.contract_id)
        _name(self.project_ref)
        if type(self.version) is not int or not 1 <= self.version <= 2147483647:
            raise ScenarioValidationError("invalid referenced contract version")
        if type(self.digest) is not str or _DIGEST.fullmatch(self.digest) is None:
            raise ScenarioValidationError("invalid referenced contract digest")

    def to_mapping(self) -> dict[str, object]:
        return {"contract_id": self.contract_id, "project_ref": self.project_ref,
                "version": self.version, "digest": self.digest}


@dataclass(frozen=True, slots=True)
class ResourcePath:
    route_ref: str
    resource_ref: ResourceId

    def __post_init__(self) -> None:
        _name(self.route_ref)
        _typed(self.resource_ref, ResourceId)

    def to_mapping(self) -> dict[str, str]:
        return {"route_ref": self.route_ref, "resource_ref": self.resource_ref.value}


@dataclass(frozen=True, slots=True)
class DecisionAssertion:
    expected: Decision
    profile: AssertionProfile

    def __post_init__(self) -> None:
        _typed(self.expected, Decision)
        _typed(self.profile, AssertionProfile)
        if (self.profile == AssertionProfile.OBJECT_READ_ALLOW) != (self.expected == Decision.ALLOW):
            raise ScenarioValidationError("assertion decision/profile mismatch")

    def to_mapping(self) -> dict[str, str]:
        return {"kind": "decision", "expected": self.expected.value, "profile": self.profile.value}


@dataclass(frozen=True, slots=True)
class ResourceAssertion:
    kind: ResourceAssertionKind
    resource_ref: ResourceId

    def __post_init__(self) -> None:
        _typed(self.kind, ResourceAssertionKind)
        _typed(self.resource_ref, ResourceId)

    def to_mapping(self) -> dict[str, str]:
        return {"kind": self.kind.value, "resource_ref": self.resource_ref.value}


@dataclass(frozen=True, slots=True)
class SetupStep:
    id: str
    actors: tuple[ActorId, ...]
    resources: tuple[ResourceId, ...]

    def __post_init__(self) -> None:
        _name(self.id)
        _items(self.actors, ActorId)
        _items(self.resources, ResourceId)

    def to_mapping(self) -> dict[str, object]:
        return {"id": self.id, "operation": "fixture.setup",
                "actors": [item.value for item in self.actors],
                "resources": [item.value for item in self.resources]}


@dataclass(frozen=True, slots=True)
class HttpRequestStep:
    id: str
    as_actor: ActorId
    method: HttpMethod
    route: ResourcePath
    expected_rule: RuleId
    assertions: tuple[DecisionAssertion | ResourceAssertion, ...]

    def __post_init__(self) -> None:
        _name(self.id)
        _typed(self.as_actor, ActorId)
        _typed(self.method, HttpMethod)
        _typed(self.route, ResourcePath)
        _typed(self.expected_rule, RuleId)
        if type(self.assertions) is not tuple or not 2 <= len(self.assertions) <= 3:
            raise ScenarioValidationError("invalid bounded request assertions")
        _typed(self.assertions[0], DecisionAssertion)
        resources = cast(tuple[ResourceAssertion, ...], self.assertions[1:])
        for assertion in resources:
            _typed(assertion, ResourceAssertion)
            if assertion.resource_ref != self.route.resource_ref:
                raise ScenarioValidationError("assertion/resource binding mismatch")
        decision = cast(DecisionAssertion, self.assertions[0])
        required = ((ResourceAssertionKind.INTENDED_RESOURCE,) if decision.expected == Decision.ALLOW
                    else (ResourceAssertionKind.NO_DISCLOSURE, ResourceAssertionKind.NO_STATE_CHANGE))
        if tuple(assertion.kind for assertion in resources) != required:
            raise ScenarioValidationError("missing or conflicting required profile assertions")

    def to_mapping(self) -> dict[str, object]:
        return {"id": self.id, "operation": "http.request", "as_actor": self.as_actor.value,
                "method": self.method.value, "route": self.route.to_mapping(),
                "expected_rule": self.expected_rule.value,
                "assertions": [assertion.to_mapping() for assertion in self.assertions]}


@dataclass(frozen=True, slots=True)
class TeardownStep:
    id: str

    def __post_init__(self) -> None:
        _name(self.id)

    def to_mapping(self) -> dict[str, str]:
        return {"id": self.id, "operation": "fixture.teardown"}


@dataclass(frozen=True, slots=True)
class Scenario:
    schema_version: str
    scenario_id: str
    contract_ref: ContractReference
    fixture_adapter: str
    steps: tuple[SetupStep | HttpRequestStep | TeardownStep, ...]

    def __post_init__(self) -> None:
        if type(self.schema_version) is not str or self.schema_version != "1.0":
            raise ScenarioValidationError("unsupported provisional scenario version", "UNSUPPORTED_SCHEMA")
        _name(self.scenario_id)
        _name(self.fixture_adapter)
        _typed(self.contract_ref, ContractReference)
        if type(self.steps) is not tuple or not 3 <= len(self.steps) <= MAX_STEPS:
            raise ScenarioValidationError("invalid bounded scenario steps")
        _typed(self.steps[0], SetupStep)
        _typed(self.steps[-1], TeardownStep)
        for request in self.steps[1:-1]:
            _typed(request, HttpRequestStep)
        if len({step.id for step in self.steps}) != len(self.steps):
            raise ScenarioValidationError("duplicate scenario step identifiers")

    @property
    def is_authoritative(self) -> bool:
        return False

    def to_mapping(self) -> dict[str, object]:
        return {"schema_version": self.schema_version, "scenario_id": self.scenario_id,
                "contract_ref": self.contract_ref.to_mapping(), "fixture_adapter": self.fixture_adapter,
                "steps": [step.to_mapping() for step in self.steps]}
