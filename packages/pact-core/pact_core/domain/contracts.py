"""Bounded candidate bodies; normalization and content hashes never grant approval."""

from dataclasses import dataclass
import hashlib
from itertools import combinations
import json
from typing import cast

from ._validation import DomainValidationError, array, closed, enum_value, typed_tuple
from .enums import Action, Relation
from .identifiers import _Identifier, ResourceTypeId, RoleId
from .rules import Rule

MAX_BYTES = 65536
MAX_DEPTH = 16
MAX_VERSION = 2147483647
FIELDS = frozenset({"schema_version", "canonicalization", "contract_id", "project_ref",
                    "version", "source_refs", "roles", "resource_types", "actions",
                    "combining", "on_unmatched", "rules"})


class ContractValidationError(DomainValidationError):
    """Invalid candidate input; errors contain no submitted payload."""

    def __init__(self, message: str, code: str = "INVALID_STRUCTURE") -> None:
        super().__init__(message)
        self.code = code


class AmbiguousContractError(ContractValidationError):
    """Impossible or potentially conflicting policy requires human clarification."""

    review_state = "NEEDS_REVIEW"


def _identifier(value: object) -> str:
    return _Identifier.from_value(value).value


def _plain_tree(value: object) -> None:
    # Iterative traversal rejects cycles by depth before serialization/recursion.
    pending = [(value, 0)]
    visited = 0
    while pending:
        visited += 1
        if visited > MAX_BYTES:
            raise ContractValidationError("candidate exceeds traversal budget", "INPUT_SIZE")
        item, parent_depth = pending.pop()
        if type(item) in (dict, list):
            item = cast(dict[str, object] | list[object], item)
            depth = parent_depth + 1
            if depth > MAX_DEPTH:
                raise ContractValidationError("candidate exceeds container depth", "INPUT_DEPTH")
            if len(item) > 64:
                raise ContractValidationError("candidate collection exceeds bound")
            if type(item) is dict:
                for key, child in item.items():
                    if type(key) is not str or len(key) > MAX_BYTES or not key.isascii():
                        raise ContractValidationError("candidate keys must be ASCII strings")
                    pending.append((child, depth))
            else:
                pending.extend((child, depth) for child in item)
        elif type(item) is str:
            if len(item) > MAX_BYTES:
                raise ContractValidationError("candidate string exceeds byte limit", "INPUT_SIZE")
            if not item.isascii():
                raise ContractValidationError("candidate strings must be ASCII")
        elif type(item) is not int:
            raise ContractValidationError("candidate contains unsupported scalar")


def _encoded(mapping: dict[str, object]) -> bytes:
    return json.dumps(mapping, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("utf-8")


def _rule_mapping(rule: Rule) -> dict[str, object]:
    return {"rule_id": rule.rule_id.value, "actor": {"role": rule.actor.role.value},
            "resource": {"type": rule.resource.type.value}, "action": rule.action.value,
            "when": [{"relation": p.relation.value, "subject": p.subject.value,
                      "object": p.object.value} for p in rule.when],
            "expect": rule.expect.value, "assertion_profile": rule.assertion_profile.value}


@dataclass(frozen=True, slots=True)
class ContractBody:
    """Immutable non-authoritative policy content, separate from review records."""

    schema_version: str
    canonicalization: str
    contract_id: str
    project_ref: str
    version: int
    source_refs: tuple[str, ...]
    roles: tuple[RoleId, ...]
    resource_types: tuple[ResourceTypeId, ...]
    actions: tuple[Action, ...]
    combining: str
    on_unmatched: str
    rules: tuple[Rule, ...]

    def __post_init__(self) -> None:
        try:
            for actual, expected in ((self.schema_version, "1.0"),
                                     (self.canonicalization, "pact-json-1"),
                                     (self.combining, "reject_conflicts"),
                                     (self.on_unmatched, "NEEDS_REVIEW")):
                if type(actual) is not str or actual != expected:
                    raise ContractValidationError("unsupported contract convention")
            _identifier(self.contract_id)
            _identifier(self.project_ref)
            if type(self.version) is not int or not 1 <= self.version <= MAX_VERSION:
                raise ContractValidationError("invalid contract version")
            typed_tuple(self.source_refs, str, "source_refs", minimum=1, maximum=32, unique=False)
            for ref in self.source_refs:
                _identifier(ref)
            typed_tuple(self.roles, RoleId, "roles", minimum=1)
            typed_tuple(self.resource_types, ResourceTypeId, "resource_types", minimum=1)
            typed_tuple(self.actions, Action, "actions", minimum=1, maximum=1)
            typed_tuple(self.rules, Rule, "rules", minimum=1, unique=False)
            if len({rule.rule_id for rule in self.rules}) != len(self.rules):
                raise ContractValidationError("duplicate rule identifier")
            for rule in self.rules:
                if (rule.actor.role not in self.roles or rule.resource.type not in self.resource_types
                        or rule.action not in self.actions):
                    raise ContractValidationError("rule references undeclared selector or action")
            if len(_encoded(self.to_mapping())) > MAX_BYTES:
                raise ContractValidationError("candidate exceeds byte limit", "INPUT_SIZE")
        except ContractValidationError:
            raise
        except DomainValidationError:
            raise ContractValidationError("invalid typed contract structure") from None

    @classmethod
    def from_mapping(cls, value: object) -> "ContractBody":
        """Structural validation only; overlaps are checked by normalization."""
        try:
            _plain_tree(value)
            data = closed(value, set(FIELDS), "contract body")
            # Casts describe constructor inputs; __post_init__ still validates
            # exact runtime types and conventions without coercion.
            return cls(cast(str, data["schema_version"]), cast(str, data["canonicalization"]),
                       cast(str, data["contract_id"]), cast(str, data["project_ref"]), cast(int, data["version"]),
                       array(data["source_refs"], _identifier, "source_refs", minimum=1, maximum=32),
                       array(data["roles"], RoleId.from_value, "roles", minimum=1),
                       array(data["resource_types"], ResourceTypeId.from_value, "resource_types", minimum=1),
                       array(data["actions"], lambda v: enum_value(Action, v, "action"),
                             "actions", minimum=1, maximum=1),
                       cast(str, data["combining"]), cast(str, data["on_unmatched"]),
                       array(data["rules"], Rule.from_mapping, "rules", minimum=1))
        except ContractValidationError:
            raise
        except DomainValidationError:
            raise ContractValidationError("invalid contract structure") from None

    def to_mapping(self) -> dict[str, object]:
        """Return detached exact content; arrays retain submitted order."""
        return {"schema_version": self.schema_version, "canonicalization": self.canonicalization,
                "contract_id": self.contract_id, "project_ref": self.project_ref,
                "version": self.version, "source_refs": list(self.source_refs),
                "roles": [role.value for role in self.roles],
                "resource_types": [kind.value for kind in self.resource_types],
                "actions": [action.value for action in self.actions],
                "combining": self.combining, "on_unmatched": self.on_unmatched,
                "rules": [_rule_mapping(rule) for rule in self.rules]}


def _check_depth(text: str) -> None:
    depth = 0
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char in "[{":
            depth += 1
            if depth > MAX_DEPTH:
                raise ContractValidationError("candidate exceeds container depth", "INPUT_DEPTH")
        elif char in "]}":
            depth -= 1
            if depth < 0:
                raise ContractValidationError("malformed JSON")


def _pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ContractValidationError("duplicate JSON key", "DUPLICATE_KEY")
        result[key] = value
    return result


def _integer(token: str) -> int:
    if len(token.lstrip("-")) > 10:
        raise ContractValidationError("integer token exceeds supported range")
    return int(token)


def _unsupported_number(token: str) -> None:
    raise ContractValidationError("floating or non-finite number forbidden")


def parse_contract(source: object, *, format: str = "json") -> ContractBody:
    """Decode strict JSON, also the accepted JSON-compatible YAML subset."""
    if type(format) is not str or format not in ("json", "yaml"):
        raise ContractValidationError("unsupported input format")
    if type(source) not in (str, bytes):
        raise ContractValidationError("expected JSON text or UTF-8 bytes")
    try:
        raw = source.encode("utf-8") if type(source) is str else cast(bytes, source)
        if len(raw) > MAX_BYTES:
            raise ContractValidationError("candidate exceeds byte limit", "INPUT_SIZE")
        text = raw.decode("utf-8")
        _check_depth(text)
        data = json.loads(text, object_pairs_hook=_pairs, parse_int=_integer,
                          parse_float=_unsupported_number, parse_constant=_unsupported_number)
    except (UnicodeError, json.JSONDecodeError, RecursionError):
        raise ContractValidationError("malformed JSON or UTF-8 encoding") from None
    return ContractBody.from_mapping(data)


def normalize_contract(value: object) -> ContractBody:
    """Reject possible conflicts without inventing role/fixture exclusivity facts."""
    body = value if type(value) is ContractBody else parse_contract(value)
    relations = [frozenset(p.relation for p in rule.when) for rule in body.rules]
    complements = {Relation.SAME_TENANT, Relation.DIFFERENT_TENANT}
    if any(complements <= predicates for predicates in relations):
        raise AmbiguousContractError("unsatisfiable tenant conjunction", "UNSATISFIABLE_RULE")
    for i, j in combinations(range(len(body.rules)), 2):
        left, right = body.rules[i], body.rules[j]
        if left.resource.type != right.resource.type or left.action != right.action:
            continue
        if (left.expect, left.assertion_profile) == (right.expect, right.assertion_profile):
            continue
        # Roles coexist; owns/member_of/shared_with do not imply tenant equality.
        if not complements <= relations[i] | relations[j]:
            raise AmbiguousContractError("possible decision or profile conflict", "POSSIBLE_CONFLICT")
    return body


def canonical_bytes(value: object) -> bytes:
    """pact-json-1: sorted ASCII keys, compact UTF-8, ordered arrays, no newline."""
    return _encoded(normalize_contract(value).to_mapping())


def contract_digest(value: object) -> str:
    """Lowercase SHA-256 of canonical content, never an approval receipt."""
    return hashlib.sha256(canonical_bytes(value)).hexdigest()
