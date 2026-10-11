"""Offline draft-provider interface; no configured live adapter or SDK import."""

from .fake import FakeFailure, FakeProvider
from .port import (
    CandidateDraft, ContractProvider, GenerationError, GenerationErrorCode,
    GenerationProvenance, GenerationRequest, ProviderValidationError,
)

__all__ = [
    "CandidateDraft", "ContractProvider", "FakeFailure", "FakeProvider",
    "GenerationError", "GenerationErrorCode", "GenerationProvenance",
    "GenerationRequest", "ProviderValidationError",
]
