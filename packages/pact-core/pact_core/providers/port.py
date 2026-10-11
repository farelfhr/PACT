"""FR-AI-001/002: internal draft-only port, independent of provider SDKs."""

from dataclasses import dataclass, field
from enum import Enum
import re
from typing import Protocol

from ..domain import ContractBody, ContractStatus, normalize_contract


class ProviderValidationError(ValueError):
    """Fixed diagnostics; no request/completion material in errors."""


def _label(value: object) -> None:
    # Logical identifiers match M1-02; these are not public wire IDs or grants.
    if type(value) is not str or re.fullmatch(r"[A-Za-z][A-Za-z0-9._-]{0,95}", value, re.ASCII) is None:
        raise ProviderValidationError("expected bounded logical identifier")


@dataclass(frozen=True, slots=True)
class GenerationRequest:
    project_ref: str
    requirement: str = field(repr=False)

    def __post_init__(self) -> None:
        _label(self.project_ref)
        if type(self.requirement) is not str or not self.requirement.strip() or len(self.requirement) > 8192:
            raise ProviderValidationError("expected nonempty bounded requirement")
        try:
            encoded = self.requirement.encode("utf-8")
        except UnicodeError:
            raise ProviderValidationError("expected UTF-8 requirement") from None
        if len(encoded) > 8192:
            raise ProviderValidationError("requirement exceeds UTF-8 byte limit")


@dataclass(frozen=True, slots=True)
class GenerationProvenance:
    adapter_ref: str
    model_ref: str
    prompt_version: str
    is_synthetic: bool

    def __post_init__(self) -> None:
        for value in (self.adapter_ref, self.model_ref, self.prompt_version):
            _label(value)
        if type(self.is_synthetic) is not bool:
            raise ProviderValidationError("expected explicit synthetic-provenance flag")
        # Descriptive adapter claims are never identity, usage or consent proof.


@dataclass(frozen=True, slots=True)
class CandidateDraft:
    body: ContractBody = field(repr=False)
    provenance: GenerationProvenance

    def __post_init__(self) -> None:
        if type(self.body) is not ContractBody or type(self.provenance) is not GenerationProvenance:
            raise ProviderValidationError("expected typed candidate and provenance")
        normalize_contract(self.body)

    @property
    def status(self) -> ContractStatus:
        return ContractStatus.DRAFT

    @property
    def is_authoritative(self) -> bool:
        return False


class GenerationErrorCode(Enum):
    INVALID_REQUEST = "INVALID_REQUEST"
    INVALID_OUTPUT = "INVALID_OUTPUT"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    PROJECT_MISMATCH = "PROJECT_MISMATCH"
    TRANSPORT_FAILURE = "TRANSPORT_FAILURE"
    TIMEOUT = "TIMEOUT"


@dataclass(frozen=True, slots=True)
class GenerationError:
    code: GenerationErrorCode

    def __post_init__(self) -> None:
        if type(self.code) is not GenerationErrorCode:
            raise ProviderValidationError("expected typed generation error")

    @property
    def message(self) -> str:
        return {
            GenerationErrorCode.INVALID_REQUEST: "generation request rejected",
            GenerationErrorCode.INVALID_OUTPUT: "candidate output rejected",
            GenerationErrorCode.NEEDS_REVIEW: "candidate semantics require human review",
            GenerationErrorCode.PROJECT_MISMATCH: "candidate project differs from request",
            GenerationErrorCode.TRANSPORT_FAILURE: "provider transport unavailable",
            GenerationErrorCode.TIMEOUT: "provider timeout",
        }[self.code]

    @property
    def review_state(self) -> ContractStatus | None:
        return ContractStatus.NEEDS_REVIEW if self.code == GenerationErrorCode.NEEDS_REVIEW else None

    @property
    def is_authoritative(self) -> bool:
        return False


class ContractProvider(Protocol):
    """One draft-or-error operation; no approval, execution, fallback or egress grant.

    Implementations must normalize output and bind it to request.project_ref.
    Future live adapters require their own consent, acquisition and conformance
    work; implementing this Protocol supplies no network permission.
    """

    def generate_structured_contract(self, request: GenerationRequest) -> CandidateDraft | GenerationError:
        ...
