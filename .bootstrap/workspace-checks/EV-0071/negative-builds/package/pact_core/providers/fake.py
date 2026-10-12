"""Scripted offline provider: fixed bytes or simulated failure, never inference."""

from dataclasses import dataclass, field
from enum import Enum

from ..domain import AmbiguousContractError, DomainValidationError, normalize_contract
from .port import (
    CandidateDraft, GenerationError, GenerationErrorCode, GenerationProvenance,
    GenerationRequest, ProviderValidationError,
)


class FakeFailure(Enum):
    TRANSPORT = "TRANSPORT"
    TIMEOUT = "TIMEOUT"


@dataclass(frozen=True, slots=True)
class FakeProvider:
    response: str | bytes | None = field(default=None, repr=False)
    failure: FakeFailure | None = None

    def __post_init__(self) -> None:
        if (self.response is None) == (self.failure is None):
            raise ProviderValidationError("choose one scripted response or failure")
        if self.response is not None and type(self.response) not in (str, bytes):
            raise ProviderValidationError("expected scripted JSON text or bytes")
        if self.failure is not None and type(self.failure) is not FakeFailure:
            raise ProviderValidationError("expected typed simulated failure")

    def generate_structured_contract(self, request: GenerationRequest) -> CandidateDraft | GenerationError:
        if type(request) is not GenerationRequest:
            return GenerationError(GenerationErrorCode.INVALID_REQUEST)
        if self.failure is not None:
            code = (GenerationErrorCode.TIMEOUT if self.failure == FakeFailure.TIMEOUT
                    else GenerationErrorCode.TRANSPORT_FAILURE)
            return GenerationError(code)
        # Convert only expected decoder/domain errors. No raw completion or
        # exception is retained; unexpected programmer errors are not successes.
        try:
            body = normalize_contract(self.response)
        except AmbiguousContractError:
            return GenerationError(GenerationErrorCode.NEEDS_REVIEW)
        except DomainValidationError:
            return GenerationError(GenerationErrorCode.INVALID_OUTPUT)
        if body.project_ref != request.project_ref:
            return GenerationError(GenerationErrorCode.PROJECT_MISMATCH)
        return CandidateDraft(body, GenerationProvenance("fake", "offline-fixture", "m2-01-1", True))
