"""Untrusted lifecycle modeling only; no identity, receipt or approval authority."""

from dataclasses import dataclass, replace
from datetime import datetime, timezone
from enum import Enum
import re
from typing import cast

from ._validation import DomainValidationError, require_type, typed_tuple
from .contracts import ContractBody, canonical_bytes, contract_digest, parse_contract
from .identifiers import _Identifier


class ContractStatus(Enum):
    DRAFT = "DRAFT"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    SUPERSEDED = "SUPERSEDED"
    DEPRECATED = "DEPRECATED"


class ModelTransitionError(DomainValidationError):
    """Invalid/stale/replayed model event; not a trusted audit event."""

    def __init__(self, code: str) -> None:
        super().__init__("untrusted lifecycle transition rejected: " + code)
        self.code = code


class ApprovalRequiredError(DomainValidationError):
    """No authenticated review mechanism is available in this domain model."""


_EDGES = frozenset({
    (ContractStatus.DRAFT, ContractStatus.NEEDS_REVIEW),
    (ContractStatus.NEEDS_REVIEW, ContractStatus.APPROVED),
    (ContractStatus.NEEDS_REVIEW, ContractStatus.REJECTED),
    (ContractStatus.APPROVED, ContractStatus.SUPERSEDED),
    (ContractStatus.APPROVED, ContractStatus.DEPRECATED),
})


def _digest(value: object) -> None:
    if type(value) is not str or re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise DomainValidationError("expected lowercase candidate content digest")


def _edge(source: object, target: object) -> None:
    require_type(source, ContractStatus, "source status")
    require_type(target, ContractStatus, "target status")
    if (source, target) not in _EDGES:
        raise ModelTransitionError("INVALID_TRANSITION")


@dataclass(frozen=True, slots=True)
class UntrustedApprovalSnapshot:
    """Claimed review metadata and exact content, never an authenticated receipt."""

    body: ContractBody
    content_digest: str
    claimed_author_ref: str
    claimed_reviewer_ref: str
    claimed_review_ref: str
    claimed_reviewed_at: datetime

    def __post_init__(self) -> None:
        require_type(self.body, ContractBody, "snapshot body")
        _digest(self.content_digest)
        if self.content_digest != contract_digest(self.body):
            raise DomainValidationError("snapshot content and digest disagree")
        for value in (self.claimed_author_ref, self.claimed_reviewer_ref, self.claimed_review_ref):
            _Identifier.from_value(value)
        # A UTC timestamp is a claim; no trusted clock/freshness proof is inferred.
        require_type(self.claimed_reviewed_at, datetime, "claimed review time")
        if self.claimed_reviewed_at.tzinfo is not timezone.utc:
            raise DomainValidationError("claimed review time must use explicit UTC")

    @property
    def is_authoritative(self) -> bool:
        return False

    @property
    def canonical_body(self) -> bytes:
        return canonical_bytes(self.body)

    def to_mapping(self) -> dict[str, object]:
        """Detached diagnostic export, not a public receipt schema or import path."""
        return {"kind": "UNTRUSTED_APPROVAL_MODEL", "status": "APPROVED",
                "body": self.body.to_mapping(), "content_digest": self.content_digest,
                "claimed_author_ref": self.claimed_author_ref,
                "claimed_reviewer_ref": self.claimed_reviewer_ref,
                "claimed_review_ref": self.claimed_review_ref,
                "claimed_reviewed_at": self.claimed_reviewed_at.isoformat()}


@dataclass(frozen=True, slots=True)
class ModeledTransition:
    """Local immutable history data; event names have no nonce/identity authority."""

    event_id: str
    from_status: ContractStatus
    to_status: ContractStatus
    expected_revision: int
    content_digest: str

    def __post_init__(self) -> None:
        _Identifier.from_value(self.event_id)
        _edge(self.from_status, self.to_status)
        if type(self.expected_revision) is not int or not 0 <= self.expected_revision <= 2:
            raise DomainValidationError("invalid modeled revision")
        _digest(self.content_digest)


@dataclass(frozen=True, slots=True)
class UntrustedContractState:
    """A consistency-checked model; even APPROVED cannot satisfy execution approval."""

    body: ContractBody
    claimed_author_ref: str
    status: ContractStatus = ContractStatus.DRAFT
    revision: int = 0
    history: tuple[ModeledTransition, ...] = ()
    snapshot: UntrustedApprovalSnapshot | None = None

    def __post_init__(self) -> None:
        require_type(self.body, ContractBody, "modeled body")
        _Identifier.from_value(self.claimed_author_ref)
        require_type(self.status, ContractStatus, "modeled status")
        typed_tuple(self.history, ModeledTransition, "modeled history", maximum=3)
        if type(self.revision) is not int or self.revision != len(self.history):
            raise DomainValidationError("modeled revision and history disagree")
        digest = self.content_digest
        state = ContractStatus.DRAFT
        seen = set()
        approval_event = None
        for index, event in enumerate(self.history):
            if (event.event_id in seen or event.expected_revision != index
                    or event.content_digest != digest or event.from_status != state):
                raise DomainValidationError("inconsistent or replayed modeled history")
            seen.add(event.event_id)
            state = event.to_status
            if state == ContractStatus.APPROVED:
                approval_event = event.event_id
        if state != self.status:
            raise DomainValidationError("status cannot bypass modeled history")
        if approval_event is None:
            if self.snapshot is not None:
                raise DomainValidationError("snapshot without modeled approval event")
        else:
            require_type(self.snapshot, UntrustedApprovalSnapshot, "claimed snapshot")
            snapshot = cast(UntrustedApprovalSnapshot, self.snapshot)
            if (snapshot.body != self.body or snapshot.content_digest != digest
                    or snapshot.claimed_author_ref != self.claimed_author_ref
                    or snapshot.claimed_review_ref != approval_event):
                raise DomainValidationError("claimed snapshot and modeled event disagree")

    @property
    def content_digest(self) -> str:
        return contract_digest(self.body)

    @property
    def is_authoritative(self) -> bool:
        return False


def import_candidate(source: object, *, claimed_author_ref: str) -> UntrustedContractState:
    """Closed body import always starts DRAFT; privileged extras are rejected."""
    return UntrustedContractState(parse_contract(source), claimed_author_ref)


def transition_model(record: UntrustedContractState, target: ContractStatus, *, event_id: str,
                     expected_revision: int, expected_digest: str,
                     claimed_snapshot: UntrustedApprovalSnapshot | None = None) -> UntrustedContractState:
    """Pure transition over untrusted data; no human action or authorization occurs."""
    require_type(record, UntrustedContractState, "modeled record")
    require_type(target, ContractStatus, "target status")
    _Identifier.from_value(event_id)
    if any(event.event_id == event_id for event in record.history):
        raise ModelTransitionError("REPLAY")
    if type(expected_revision) is not int or expected_revision != record.revision:
        raise ModelTransitionError("STALE_REVISION")
    if type(expected_digest) is not str or expected_digest != record.content_digest:
        raise ModelTransitionError("STALE_CONTENT")
    _edge(record.status, target)
    chosen_snapshot: UntrustedApprovalSnapshot | None
    if target == ContractStatus.APPROVED:
        if (type(claimed_snapshot) is not UntrustedApprovalSnapshot
                or claimed_snapshot.body != record.body
                or claimed_snapshot.claimed_author_ref != record.claimed_author_ref
                or claimed_snapshot.claimed_review_ref != event_id):
            raise ModelTransitionError("SNAPSHOT_MISMATCH")
        chosen_snapshot = claimed_snapshot
    else:
        if claimed_snapshot is not None:
            raise ModelTransitionError("UNEXPECTED_SNAPSHOT")
        chosen_snapshot = record.snapshot
    event = ModeledTransition(event_id, record.status, target, record.revision, record.content_digest)
    return replace(record, status=target, revision=record.revision + 1,
                   history=record.history + (event,), snapshot=chosen_snapshot)


def new_draft_version(record: UntrustedContractState, body: ContractBody) -> UntrustedContractState:
    """Same logical policy, next version; retain old model/snapshot by immutability."""
    require_type(record, UntrustedContractState, "modeled record")
    require_type(body, ContractBody, "new body")
    if (body.contract_id != record.body.contract_id or body.project_ref != record.body.project_ref
            or body.version != record.body.version + 1):
        raise DomainValidationError("edit requires same policy/project and next contract version")
    return UntrustedContractState(body, record.claimed_author_ref)


def require_authenticated_approval(value: object) -> None:
    """Fail closed for every input; M2 must supply a separately trusted service."""
    raise ApprovalRequiredError("authenticated approval is unavailable; domain state is untrusted")
