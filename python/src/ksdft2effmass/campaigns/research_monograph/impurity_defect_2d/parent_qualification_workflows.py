"""Separate calculation and verification Workflows for parent qualification."""

from __future__ import annotations

from dataclasses import dataclass

from .parent_qualification import (
    ParentQualificationResult,
)
from .parent_qualification_calculation import ParentQualificationCalculator
from .parent_qualification_serialization import (
    ParentQualificationRequestJsonSerializer,
    ParentQualificationResultJsonSerializer,
)
from .parent_qualification_verification import (
    ParentQualificationIndependentVerifier,
    ParentQualificationVerificationResult,
)


@dataclass(frozen=True, slots=True)
class ParentQualificationCalculationWorkflowResult:
    """Retain exact request bytes, calculated result, and canonical result bytes."""

    serialized_request: bytes
    result: ParentQualificationResult
    serialized_result: bytes

    def __post_init__(self) -> None:
        """Require both wire records to reconstruct the exact typed values."""
        if type(self.serialized_request) is not bytes:
            raise TypeError("serialized_request must be bytes")
        if type(self.result) is not ParentQualificationResult:
            raise TypeError("result must be ParentQualificationResult")
        if type(self.serialized_result) is not bytes:
            raise TypeError("serialized_result must be bytes")
        request = ParentQualificationRequestJsonSerializer().deserialize(
            self.serialized_request
        )
        if request != self.result.definition:
            raise ValueError(
                "serialized_request must reconstruct the result definition"
            )
        serializer = ParentQualificationResultJsonSerializer()
        if serializer.deserialize(self.serialized_result) != self.result:
            raise ValueError("serialized_result must reconstruct the exact result")
        if serializer.serialize(self.result) != self.serialized_result:
            raise ValueError("serialized_result must use canonical bytes")


class ParentQualificationCalculationWorkflow:
    """Deserialize, qualify, and canonically serialize one parent request."""

    __slots__ = ()

    def execute(
        self, serialized_request: bytes
    ) -> ParentQualificationCalculationWorkflowResult:
        """Return local parent qualification without invoking verification."""
        if type(serialized_request) is not bytes:
            raise TypeError("serialized_request must be bytes")
        definition = ParentQualificationRequestJsonSerializer().deserialize(
            serialized_request
        )
        result = ParentQualificationCalculator().execute(definition)
        serialized = ParentQualificationResultJsonSerializer().serialize(result)
        return ParentQualificationCalculationWorkflowResult(
            serialized_request, result, serialized
        )


@dataclass(frozen=True, slots=True)
class ParentQualificationVerificationWorkflowResult:
    """Retain authenticated result bytes and independent reconstruction."""

    serialized_result: bytes
    verification: ParentQualificationVerificationResult

    def __post_init__(self) -> None:
        """Require source bytes to reconstruct the independently verified result."""
        if type(self.serialized_result) is not bytes:
            raise TypeError("serialized_result must be bytes")
        if type(self.verification) is not ParentQualificationVerificationResult:
            raise TypeError(
                "verification must be ParentQualificationVerificationResult"
            )
        source = ParentQualificationResultJsonSerializer().deserialize(
            self.serialized_result
        )
        if source != self.verification.source:
            raise ValueError("verification must own the serialized source result")


class ParentQualificationIndependentVerificationWorkflow:
    """Deserialize and independently reconstruct one parent qualification result."""

    __slots__ = ()

    def execute(
        self,
        serialized_result: bytes,
        *,
        verification_absolute_tolerance: float,
    ) -> ParentQualificationVerificationWorkflowResult:
        """Return independent verification without invoking the calculation route."""
        if type(serialized_result) is not bytes:
            raise TypeError("serialized_result must be bytes")
        source = ParentQualificationResultJsonSerializer().deserialize(
            serialized_result
        )
        verification = ParentQualificationIndependentVerifier().execute(
            source,
            absolute_tolerance=verification_absolute_tolerance,
        )
        return ParentQualificationVerificationWorkflowResult(
            serialized_result, verification
        )
