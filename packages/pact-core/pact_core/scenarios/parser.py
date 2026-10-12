"""Bounded JSON parser and declaration checks, never an interpreter or executor."""

import json
from typing import cast

from ..domain import (ActorId, AssertionProfile, Decision, DomainValidationError,
                      ResourceId, RuleId, contract_digest)
from ..domain._validation import array, closed, enum_value
from .models import (ContractReference, DecisionAssertion, HttpMethod, HttpRequestStep,
                     ResourceAssertion, ResourceAssertionKind, ResourcePath, Scenario,
                     ScenarioDeclarations, ScenarioValidationError, SetupStep, TeardownStep)

MAX_BYTES = 65536
MAX_DEPTH = 16


def _pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ScenarioValidationError("duplicate JSON key", "DUPLICATE_KEY")
        result[key] = value
    return result


def _integer(token: str) -> int:
    if len(token) > 11:
        raise ScenarioValidationError("integer token exceeds bound")
    return int(token)


def _unsupported(token: str) -> None:
    raise ScenarioValidationError("unsupported numeric token")


def _decode(value: object) -> object:
    if type(value) not in (str, bytes):
        raise ScenarioValidationError("scenario input must be JSON text or UTF-8 bytes")
    try:
        raw = value.encode("utf-8") if type(value) is str else cast(bytes, value)
        if len(raw) > MAX_BYTES:
            raise ScenarioValidationError("scenario exceeds byte bound", "INPUT_SIZE")
        text = raw.decode("utf-8")
    except UnicodeError:
        raise ScenarioValidationError("invalid UTF-8 scenario") from None
    # Scan nesting before the JSON decoder can exhaust Python's recursive stack.
    depth, quoted, escaped = 0, False, False
    for char in text:
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char in "[{":
            depth += 1
            if depth > MAX_DEPTH:
                raise ScenarioValidationError("scenario exceeds nesting bound", "INPUT_DEPTH")
        elif char in "]}":
            depth -= 1
    try:
        data = json.loads(text, object_pairs_hook=_pairs, parse_int=_integer,
                          parse_float=_unsupported, parse_constant=_unsupported)
    except ScenarioValidationError:
        raise
    except (ValueError, RecursionError):
        raise ScenarioValidationError("invalid JSON scenario") from None
    pending = [data]
    while pending:
        node = pending.pop()
        if type(node) is dict:
            if len(node) > 64 or any(type(key) is not str or not key.isascii() or len(key) > 96 for key in node):
                raise ScenarioValidationError("invalid bounded JSON object")
            pending.extend(node.values())
        elif type(node) is list:
            if len(node) > 64:
                raise ScenarioValidationError("invalid bounded JSON array")
            pending.extend(node)
        elif type(node) is str:
            if not node.isascii() or len(node) > 96:
                raise ScenarioValidationError("invalid bounded ASCII string")
        elif type(node) is not int:
            raise ScenarioValidationError("unsupported JSON scalar")
    return data


def _assertion(value: object) -> DecisionAssertion | ResourceAssertion:
    if type(value) is not dict:
        raise ScenarioValidationError("invalid assertion object")
    if value.get("kind") == "decision":
        data = closed(value, {"kind", "expected", "profile"}, "decision assertion")
        return DecisionAssertion(enum_value(Decision, data["expected"], "expected"),
                                 enum_value(AssertionProfile, data["profile"], "profile"))
    data = closed(value, {"kind", "resource_ref"}, "resource assertion")
    return ResourceAssertion(enum_value(ResourceAssertionKind, data["kind"], "assertion kind"),
                             ResourceId.from_value(data["resource_ref"]))


def _step(value: object) -> SetupStep | HttpRequestStep | TeardownStep:
    if type(value) is not dict:
        raise ScenarioValidationError("invalid step object")
    operation = value.get("operation")
    if operation == "fixture.setup":
        data = closed(value, {"id", "operation", "actors", "resources"}, "setup")
        return SetupStep(cast(str, data["id"]), array(data["actors"], ActorId.from_value, "actors", minimum=1),
                         array(data["resources"], ResourceId.from_value, "resources", minimum=1))
    if operation == "fixture.teardown":
        return TeardownStep(cast(str, closed(value, {"id", "operation"}, "teardown")["id"]))
    if operation != "http.request":
        raise ScenarioValidationError("unsupported scenario operation", "UNKNOWN_OPERATION")
    data = closed(value, {"id", "operation", "as_actor", "method", "route",
                          "expected_rule", "assertions"}, "request")
    route = closed(data["route"], {"route_ref", "resource_ref"}, "resource path")
    return HttpRequestStep(cast(str, data["id"]), ActorId.from_value(data["as_actor"]),
                           enum_value(HttpMethod, data["method"], "method"),
                           ResourcePath(cast(str, route["route_ref"]), ResourceId.from_value(route["resource_ref"])),
                           RuleId.from_value(data["expected_rule"]),
                           array(data["assertions"], _assertion, "assertions", minimum=2, maximum=3))


def _bind(scenario: Scenario, declarations: ScenarioDeclarations) -> None:
    body, ref = declarations.contract, scenario.contract_ref
    if (scenario.fixture_adapter != declarations.fixture_adapter
            or (ref.contract_id, ref.project_ref, ref.version, ref.digest) !=
            (body.contract_id, body.project_ref, body.version, contract_digest(body))):
        raise ScenarioValidationError("scenario/candidate declaration mismatch", "DECLARATION_MISMATCH")
    actors = {actor.id: actor for actor in declarations.fixtures.actors}
    resources = {resource.id: resource for resource in declarations.fixtures.resources}
    routes = {route.route_ref: route for route in declarations.routes}
    rules = {rule.rule_id: rule for rule in body.rules}
    # Scenario.__post_init__ already checked these exact step/assertion types.
    setup = cast(SetupStep, scenario.steps[0])
    if not set(setup.actors) <= actors.keys() or not set(setup.resources) <= resources.keys():
        raise ScenarioValidationError("undeclared setup reference", "UNDECLARED_REFERENCE")
    for request in cast(tuple[HttpRequestStep, ...], scenario.steps[1:-1]):
        if (request.as_actor not in setup.actors or request.route.resource_ref not in setup.resources
                or request.route.route_ref not in routes or request.expected_rule not in rules):
            raise ScenarioValidationError("undeclared request reference", "UNDECLARED_REFERENCE")
        actor, resource = actors[request.as_actor], resources[request.route.resource_ref]
        rule, route = rules[request.expected_rule], routes[request.route.route_ref]
        decision = cast(DecisionAssertion, request.assertions[0])
        if (resource.type != route.resource_type or resource.type != rule.resource.type
                or rule.actor.role not in actor.roles or decision.expected != rule.expect
                or decision.profile != rule.assertion_profile):
            raise ScenarioValidationError("request/rule/profile binding mismatch", "DECLARATION_MISMATCH")
    # Predicate matching, real authentication and approval remain separate future gates.


def parse_scenario(value: str | bytes, declarations: ScenarioDeclarations) -> Scenario:
    """Return non-authoritative typed data; declarations cannot authorize a run."""
    if type(declarations) is not ScenarioDeclarations:
        raise ScenarioValidationError("scenario requires explicit typed declarations")
    try:
        data = closed(_decode(value), {"schema_version", "scenario_id", "contract_ref",
                                     "fixture_adapter", "steps"}, "scenario")
        ref = closed(data["contract_ref"], {"contract_id", "project_ref", "version", "digest"}, "contract ref")
        scenario = Scenario(cast(str, data["schema_version"]), cast(str, data["scenario_id"]),
                            ContractReference(cast(str, ref["contract_id"]), cast(str, ref["project_ref"]), cast(int, ref["version"]), cast(str, ref["digest"])),
                            cast(str, data["fixture_adapter"]), array(data["steps"], _step, "steps", minimum=3, maximum=32))
        _bind(scenario, declarations)
        return scenario
    except ScenarioValidationError:
        raise
    except DomainValidationError:
        raise ScenarioValidationError("invalid typed scenario structure") from None
