"""ADR-0001 vocabulary and AGENTS §4.3 observed-verdict names."""

from enum import Enum


class Action(Enum):
    READ = "read"


class Decision(Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"


class Relation(Enum):
    OWNS = "owns"
    MEMBER_OF = "member_of"
    SHARED_WITH = "shared_with"
    SAME_TENANT = "same_tenant"
    DIFFERENT_TENANT = "different_tenant"


class Binding(Enum):
    ACTOR = "actor"
    RESOURCE = "resource"
    ACTOR_TENANT = "actor.tenant"
    RESOURCE_TENANT = "resource.tenant"


class AssertionProfile(Enum):
    OBJECT_READ_ALLOW = "object-read-allow-v1"
    OBJECT_READ_DENY_403_404 = "object-read-deny-403-404-v1"
    OBJECT_READ_DENY_401_403_404 = "object-read-deny-401-403-404-v1"


class ScenarioVerdict(Enum):
    PASS = "PASS"
    VIOLATION = "VIOLATION"
    INCONCLUSIVE = "INCONCLUSIVE"
    ERROR = "ERROR"
    SKIPPED = "SKIPPED"
    CANCELED = "CANCELED"
