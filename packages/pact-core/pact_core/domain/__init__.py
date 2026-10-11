"""Validated domain data; importing or constructing it authorizes nothing."""

from ._validation import DomainValidationError
from .approval_model import (ApprovalRequiredError, ContractStatus, ModelTransitionError,
                             UntrustedApprovalSnapshot, UntrustedContractState,
                             import_candidate, new_draft_version, require_authenticated_approval,
                             transition_model)
from .contracts import (AmbiguousContractError, ContractBody, ContractValidationError,
                        canonical_bytes, contract_digest, normalize_contract, parse_contract)
from .entities import Actor, DomainCatalog, Resource, Tenant
from .enums import Action, AssertionProfile, Binding, Decision, Relation, ScenarioVerdict
from .identifiers import ActorId, ResourceId, ResourceTypeId, RoleId, RuleId, TenantId
from .rules import ActorSelector, Predicate, ResourceSelector, Rule

__all__ = [
    "Action", "Actor", "ActorId", "ActorSelector", "AssertionProfile", "Binding",
    "Decision", "DomainCatalog", "DomainValidationError", "Predicate", "Relation",
    "Resource", "ResourceId", "ResourceSelector", "ResourceTypeId", "RoleId", "Rule",
    "RuleId", "ScenarioVerdict", "Tenant", "TenantId",
    "AmbiguousContractError", "ContractBody", "ContractValidationError",
    "canonical_bytes", "contract_digest", "normalize_contract", "parse_contract",
    "ApprovalRequiredError", "ContractStatus", "ModelTransitionError",
    "UntrustedApprovalSnapshot", "UntrustedContractState", "import_candidate",
    "new_draft_version", "require_authenticated_approval", "transition_model",
]
