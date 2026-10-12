"""Typed rule structure only; no matching, approval or HTTP assertions."""

from dataclasses import dataclass
from builtins import object as BuiltinObject

from ._validation import DomainValidationError, array, closed, enum_value, require_type, typed_tuple
from .enums import Action, AssertionProfile, Binding, Decision, Relation
from .identifiers import ResourceTypeId, RoleId, RuleId


@dataclass(frozen=True, slots=True)
class ActorSelector:
    role: RoleId

    def __post_init__(self) -> None:
        require_type(self.role, RoleId, "actor.role")

    @classmethod
    def from_mapping(cls, value: object) -> "ActorSelector":
        data = closed(value, {"role"}, "actor selector")
        return cls(RoleId.from_value(data["role"]))


@dataclass(frozen=True, slots=True)
class ResourceSelector:
    type: ResourceTypeId

    def __post_init__(self) -> None:
        require_type(self.type, ResourceTypeId, "resource.type")

    @classmethod
    def from_mapping(cls, value: object) -> "ResourceSelector":
        data = closed(value, {"type"}, "resource selector")
        return cls(ResourceTypeId.from_value(data["type"]))


@dataclass(frozen=True, slots=True)
class Predicate:
    relation: Relation
    subject: Binding
    object: Binding

    def __post_init__(self) -> None:
        require_type(self.relation, Relation, "predicate.relation")
        require_type(self.subject, Binding, "predicate.subject")
        require_type(self.object, Binding, "predicate.object")
        signatures = {
            Relation.OWNS: (Binding.ACTOR, Binding.RESOURCE),
            Relation.MEMBER_OF: (Binding.ACTOR, Binding.RESOURCE_TENANT),
            Relation.SHARED_WITH: (Binding.RESOURCE, Binding.ACTOR),
            Relation.SAME_TENANT: (Binding.ACTOR_TENANT, Binding.RESOURCE_TENANT),
            Relation.DIFFERENT_TENANT: (Binding.ACTOR_TENANT, Binding.RESOURCE_TENANT),
        }
        if (self.subject, self.object) != signatures[self.relation]:
            raise DomainValidationError("predicate: invalid relation binding")

    @classmethod
    def from_mapping(cls, value: BuiltinObject) -> "Predicate":
        data = closed(value, {"relation", "subject", "object"}, "predicate")
        return cls(enum_value(Relation, data["relation"], "relation"),
                   enum_value(Binding, data["subject"], "subject"),
                   enum_value(Binding, data["object"], "object"))


@dataclass(frozen=True, slots=True)
class Rule:
    rule_id: RuleId
    actor: ActorSelector
    resource: ResourceSelector
    action: Action
    when: tuple[Predicate, ...]
    expect: Decision
    assertion_profile: AssertionProfile

    def __post_init__(self) -> None:
        for value, kind, label in (
            (self.rule_id, RuleId, "rule_id"), (self.actor, ActorSelector, "actor"),
            (self.resource, ResourceSelector, "resource"), (self.action, Action, "action"),
            (self.expect, Decision, "expect"),
            (self.assertion_profile, AssertionProfile, "assertion_profile"),
        ):
            require_type(value, kind, label)
        typed_tuple(self.when, Predicate, "when", minimum=1, maximum=8, unique=False)
        allows = self.assertion_profile == AssertionProfile.OBJECT_READ_ALLOW
        if allows != (self.expect == Decision.ALLOW):
            raise DomainValidationError("rule: decision and assertion profile disagree")

    @classmethod
    def from_mapping(cls, value: object) -> "Rule":
        data = closed(value, {"rule_id", "actor", "resource", "action", "when",
                              "expect", "assertion_profile"}, "rule")
        return cls(RuleId.from_value(data["rule_id"]), ActorSelector.from_mapping(data["actor"]),
                   ResourceSelector.from_mapping(data["resource"]),
                   enum_value(Action, data["action"], "action"),
                   array(data["when"], Predicate.from_mapping, "when", minimum=1, maximum=8),
                   enum_value(Decision, data["expect"], "expect"),
                   enum_value(AssertionProfile, data["assertion_profile"], "assertion_profile"))
