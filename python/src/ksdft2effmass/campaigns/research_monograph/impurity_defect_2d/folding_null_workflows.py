"""Separate folding/null calculation and independent-verification Workflows."""

from __future__ import annotations

from dataclasses import dataclass

from .folding_null import (
    FoldingNullCalculator,
    FoldingNullResult,
    FoldingNullStudyDefinition,
)
from .folding_null_serialization import FoldingNullResultJsonSerializer
from .folding_null_verification import (
    FoldingNullIndependentVerifier,
    FoldingNullVerificationResult,
)


@dataclass(frozen=True, slots=True)
class FoldingNullCalculationWorkflowResult:
    """Retain one typed folding/null calculation and canonical result bytes."""

    result: FoldingNullResult
    serialized_result: bytes

    def __post_init__(self) -> None:
        """Require canonical bytes to reconstruct the exact calculation result."""
        if type(self.result) is not FoldingNullResult:
            raise TypeError("result must be FoldingNullResult")
        if type(self.serialized_result) is not bytes:
            raise TypeError("serialized_result must be bytes")
        serializer = FoldingNullResultJsonSerializer()
        if serializer.deserialize(self.serialized_result) != self.result:
            raise ValueError("serialized_result must reconstruct the exact result")
        if serializer.serialize(self.result) != self.serialized_result:
            raise ValueError("serialized_result must use canonical bytes")


class FoldingNullCalculationWorkflow:
    """Compose authored folding/null calculation and canonical serialization."""

    __slots__ = ()

    def execute(
        self, definition: FoldingNullStudyDefinition
    ) -> FoldingNullCalculationWorkflowResult:
        """Return one synthetic result without invoking independent verification."""
        if type(definition) is not FoldingNullStudyDefinition:
            raise TypeError("definition must be FoldingNullStudyDefinition")
        result = FoldingNullCalculator().execute(definition)
        serialized = FoldingNullResultJsonSerializer().serialize(result)
        return FoldingNullCalculationWorkflowResult(result, serialized)


@dataclass(frozen=True, slots=True)
class FoldingNullVerificationWorkflowResult:
    """Retain authenticated source bytes and their independent verification."""

    serialized_result: bytes
    verification: FoldingNullVerificationResult

    def __post_init__(self) -> None:
        """Require the source bytes to reconstruct the verified typed result."""
        if type(self.serialized_result) is not bytes:
            raise TypeError("serialized_result must be bytes")
        if type(self.verification) is not FoldingNullVerificationResult:
            raise TypeError("verification must be FoldingNullVerificationResult")
        reconstructed = FoldingNullResultJsonSerializer().deserialize(
            self.serialized_result
        )
        if reconstructed != self.verification.source:
            raise ValueError("verification must own the serialized source result")


class FoldingNullIndependentVerificationWorkflow:
    """Deserialize and independently reconstruct one retained folding/null result."""

    __slots__ = ()

    def execute(
        self,
        serialized_result: bytes,
        *,
        verification_relative_tolerance: float,
        verification_absolute_tolerance: float,
    ) -> FoldingNullVerificationWorkflowResult:
        """Return verification without importing or invoking the calculation route."""
        if type(serialized_result) is not bytes:
            raise TypeError("serialized_result must be bytes")
        result = FoldingNullResultJsonSerializer().deserialize(serialized_result)
        verification = FoldingNullIndependentVerifier().execute(
            result,
            relative_tolerance=verification_relative_tolerance,
            absolute_tolerance=verification_absolute_tolerance,
        )
        return FoldingNullVerificationWorkflowResult(serialized_result, verification)
