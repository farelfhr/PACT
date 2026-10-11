"""Immutable fixture facts and reference checks; data does not confer trust."""

from dataclasses import dataclass

from ._validation import DomainValidationError, array, closed, require_type, typed_tuple
from .identifiers import ActorId, ResourceId, ResourceTypeId, RoleId, TenantId
from .rules import Rule


@dataclass(frozen=True, slots=True)
class Tenant:
    id: TenantId

    def __post_init__(self) -> None:
        require_type(self.id, TenantId, "tenant.id")

    @classmethod
    def from_mapping(cls, value: object) -> "Tenant":
        return cls(TenantId.from_value(closed(value, {"id"}, "tenant")["id"]))


@dataclass(frozen=True, slots=True)
class Actor:
    id: ActorId
    tenant: TenantId
    roles: tuple[RoleId, ...]
    memberships: tuple[TenantId, ...]

    def __post_init__(self) -> None:
        require_type(self.id, ActorId, "actor.id")
        require_type(self.tenant, TenantId, "actor.tenant")
        typed_tuple(self.roles, RoleId, "actor.roles", minimum=1)
        typed_tuple(self.memberships, TenantId, "actor.memberships")

    @classmethod
    def from_mapping(cls, value: object) -> "Actor":
        data = closed(value, {"id", "tenant", "roles", "memberships"}, "actor")
        return cls(ActorId.from_value(data["id"]), TenantId.from_value(data["tenant"]),
                   array(data["roles"], RoleId.from_value, "roles", minimum=1),
                   array(data["memberships"], TenantId.from_value, "memberships"))


@dataclass(frozen=True, slots=True)
class Resource:
    id: ResourceId
    tenant: TenantId
    type: ResourceTypeId
    owner: ActorId
    shared_with: tuple[ActorId, ...]

    def __post_init__(self) -> None:
        require_type(self.id, ResourceId, "resource.id")
        require_type(self.tenant, TenantId, "resource.tenant")
        require_type(self.type, ResourceTypeId, "resource.type")
        require_type(self.owner, ActorId, "resource.owner")
        typed_tuple(self.shared_with, ActorId, "resource.shared_with")

    @classmethod
    def from_mapping(cls, value: object) -> "Resource":
        data = closed(value, {"id", "tenant", "type", "owner", "shared_with"}, "resource")
        return cls(ResourceId.from_value(data["id"]), TenantId.from_value(data["tenant"]),
                   ResourceTypeId.from_value(data["type"]), ActorId.from_value(data["owner"]),
                   array(data["shared_with"], ActorId.from_value, "shared_with"))


@dataclass(frozen=True, slots=True)
class DomainCatalog:
    """Structural reference completeness, not an approved fixture or session."""

    roles: tuple[RoleId, ...]
    resource_types: tuple[ResourceTypeId, ...]
    tenants: tuple[Tenant, ...]
    actors: tuple[Actor, ...]
    resources: tuple[Resource, ...]

    def __post_init__(self) -> None:
        for value, kind, label in (
            (self.roles, RoleId, "roles"), (self.resource_types, ResourceTypeId, "resource_types"),
            (self.tenants, Tenant, "tenants"), (self.actors, Actor, "actors"),
            (self.resources, Resource, "resources"),
        ):
            typed_tuple(value, kind, label, minimum=1)
        for values in (self.tenants, self.actors, self.resources):
            if len({entity.id for entity in values}) != len(values):
                raise DomainValidationError("catalog: duplicate entity IDs")
        tenant_ids = {entity.id for entity in self.tenants}
        actor_ids = {entity.id for entity in self.actors}
        for actor in self.actors:
            if (actor.tenant not in tenant_ids or not set(actor.memberships) <= tenant_ids
                    or not set(actor.roles) <= set(self.roles)):
                raise DomainValidationError("catalog: undeclared actor tenant, membership or role")
        for resource in self.resources:
            if (resource.tenant not in tenant_ids or resource.type not in self.resource_types
                    or resource.owner not in actor_ids or not set(resource.shared_with) <= actor_ids):
                raise DomainValidationError("catalog: undeclared resource tenant, type, owner or share")

    def validate_rule(self, rule: Rule) -> None:
        require_type(rule, Rule, "catalog.rule")
        if rule.actor.role not in self.roles or rule.resource.type not in self.resource_types:
            raise DomainValidationError("rule: undeclared role or resource type")

    @classmethod
    def from_mapping(cls, value: object) -> "DomainCatalog":
        data = closed(value, {"roles", "resource_types", "tenants", "actors", "resources"}, "catalog")
        return cls(array(data["roles"], RoleId.from_value, "roles", minimum=1),
                   array(data["resource_types"], ResourceTypeId.from_value, "resource_types", minimum=1),
                   array(data["tenants"], Tenant.from_mapping, "tenants", minimum=1),
                   array(data["actors"], Actor.from_mapping, "actors", minimum=1),
                   array(data["resources"], Resource.from_mapping, "resources", minimum=1))
