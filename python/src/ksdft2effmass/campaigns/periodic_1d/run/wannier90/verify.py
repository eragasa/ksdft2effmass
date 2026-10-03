"""Native-artifact and Wilson verification for a Wannier90 integration."""

from dataclasses import dataclass

import numpy as np

from ...encoded_documents import Periodic1DWannier90EncodedDocuments
from ...native_artifact_workflows import (
    Periodic1DWannier90NativeArtifactGroup,
    Periodic1DWannier90NativeArtifactWorkflowRequest,
)
from ...verification import (
    Periodic1DWannier90WilsonGroupVerificationResult,
    Periodic1DWannier90WilsonVerificationRequest,
    Periodic1DWannier90WilsonVerificationResult,
    Periodic1DWannier90WilsonVerifier,
)
from ...verified_workflows import (
    Periodic1DWannier90VerifiedNativeWorkflow,
    Periodic1DWannier90VerifiedNativeWorkflowRequest,
    Periodic1DWannier90VerifiedNativeWorkflowResult,
)


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90IntegrationVerificationRequest:
    """Request native correlation and Wilson verification with explicit controls."""

    encoded_documents: Periodic1DWannier90EncodedDocuments
    artifact_groups: tuple[Periodic1DWannier90NativeArtifactGroup, ...]
    phase_absolute_tolerance: float
    loop_unitarity_absolute_tolerance: float
    minimum_active_overlap_singular_value: float

    def __post_init__(self) -> None:
        """Require exact state and finite nonnegative dimensionless controls."""
        if type(self.encoded_documents) is not Periodic1DWannier90EncodedDocuments:
            raise TypeError(
                "encoded_documents must be Periodic1DWannier90EncodedDocuments"
            )
        if not isinstance(self.artifact_groups, tuple) or any(
            type(group) is not Periodic1DWannier90NativeArtifactGroup
            for group in self.artifact_groups
        ):
            raise TypeError("artifact_groups must be a typed tuple")
        group_ids = tuple(group.group_id for group in self.artifact_groups)
        if len(set(group_ids)) != len(group_ids):
            raise ValueError("native artifact group identifiers must be unique")
        for name, value in (
            ("phase_absolute_tolerance", self.phase_absolute_tolerance),
            (
                "loop_unitarity_absolute_tolerance",
                self.loop_unitarity_absolute_tolerance,
            ),
            (
                "minimum_active_overlap_singular_value",
                self.minimum_active_overlap_singular_value,
            ),
        ):
            if type(value) is not float or not np.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be a finite nonnegative built-in float")


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90IntegrationVerificationResult:
    """Retain authenticated native artifacts and bounded Wilson verification."""

    native_verification: Periodic1DWannier90VerifiedNativeWorkflowResult

    def __post_init__(self) -> None:
        """Require the exact integrated verification AbstractResultObject type."""
        if (
            type(self.native_verification)
            is not Periodic1DWannier90VerifiedNativeWorkflowResult
        ):
            raise TypeError(
                "native_verification uses the wrong AbstractResultObject type"
            )

    @property
    def passes(self) -> bool:
        """Return the bounded native/Wilson verification disposition."""
        return self.native_verification.passes


class Periodic1DWannier90IntegrationVerifier:
    """Authenticate native bytes and independently verify Wilson-loop evidence."""

    __slots__ = ()

    workflow = Periodic1DWannier90VerifiedNativeWorkflow()

    def execute(
        self, request: Periodic1DWannier90IntegrationVerificationRequest
    ) -> Periodic1DWannier90IntegrationVerificationResult:
        """Return bounded verification over explicit retained and native bytes.

        Parameters
        ----------
        request
            Integration state and explicit dimensionless verification controls.

        Returns
        -------
        Periodic1DWannier90IntegrationVerificationResult
            Authenticated native records and independent Wilson-loop findings.

        Raises
        ------
        TypeError
            If ``request`` or nested integration state has the wrong exact type.
        ValueError
            If artifacts are unavailable, identities disagree, parsing fails, or the
            retained/native structures cannot support the requested verification.
        """
        if type(request) is not Periodic1DWannier90IntegrationVerificationRequest:
            raise TypeError(
                "request must be Periodic1DWannier90IntegrationVerificationRequest"
            )
        encoded_documents = request.encoded_documents
        native_request = Periodic1DWannier90NativeArtifactWorkflowRequest(
            encoded_documents.result_payload,
            encoded_documents.result_kind,
            request.artifact_groups,
        )
        result = self.workflow.execute(
            Periodic1DWannier90VerifiedNativeWorkflowRequest(
                native_request,
                request.phase_absolute_tolerance,
                request.loop_unitarity_absolute_tolerance,
                request.minimum_active_overlap_singular_value,
            )
        )
        return Periodic1DWannier90IntegrationVerificationResult(result)


__all__ = [
    "Periodic1DWannier90IntegrationVerificationRequest",
    "Periodic1DWannier90IntegrationVerificationResult",
    "Periodic1DWannier90IntegrationVerifier",
    "Periodic1DWannier90VerifiedNativeWorkflow",
    "Periodic1DWannier90VerifiedNativeWorkflowRequest",
    "Periodic1DWannier90VerifiedNativeWorkflowResult",
    "Periodic1DWannier90WilsonGroupVerificationResult",
    "Periodic1DWannier90WilsonVerificationRequest",
    "Periodic1DWannier90WilsonVerificationResult",
    "Periodic1DWannier90WilsonVerifier",
]
