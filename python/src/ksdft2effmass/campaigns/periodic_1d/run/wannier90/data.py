"""Encapsulating DataObject for one Wannier90 campaign integration."""

from dataclasses import dataclass

from ...encoded_documents import Periodic1DWannier90EncodedDocuments
from ...native_artifact_workflows import Periodic1DWannier90NativeArtifactGroup
from .correlate import (
    Periodic1DWannier90IntegrationCorrelationRequest,
    Periodic1DWannier90IntegrationCorrelationResult,
    Periodic1DWannier90IntegrationCorrelator,
)
from .verify import (
    Periodic1DWannier90IntegrationVerificationRequest,
    Periodic1DWannier90IntegrationVerificationResult,
    Periodic1DWannier90IntegrationVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90Integration:
    """Encapsulate immutable integration state behind cohesive Actionizers.

    Parameters
    ----------
    encoded_documents
        Exact composite controls, Wannier90 result bytes, and result variant identity.
    artifact_groups
        Explicit native artifact inventories ordered by band group. An empty tuple
        remains valid for document correlation; native verification requires groups.

    Notes
    -----
    ``correlate`` checks encoded input/result identities without making a numerical
    claim. ``verify`` additionally requires complete native artifact groups and applies
    explicit bounded Wilson-loop verification controls. Neither operation executes
    Wannier90 or discovers files from ambient paths.
    """

    encoded_documents: Periodic1DWannier90EncodedDocuments
    artifact_groups: tuple[Periodic1DWannier90NativeArtifactGroup, ...] = ()

    def __post_init__(self) -> None:
        """Require exact documents and unique typed native artifact groups."""
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

    def correlate(self) -> Periodic1DWannier90IntegrationCorrelationResult:
        """Correlate retained composite controls and Wannier90 result bytes.

        Returns
        -------
        Periodic1DWannier90IntegrationCorrelationResult
            Typed records and exact payload identities without a numerical claim.
        """
        return Periodic1DWannier90IntegrationCorrelator().execute(
            Periodic1DWannier90IntegrationCorrelationRequest(self.encoded_documents)
        )

    def verify(
        self,
        *,
        phase_absolute_tolerance: float,
        loop_unitarity_absolute_tolerance: float,
        minimum_active_overlap_singular_value: float,
    ) -> Periodic1DWannier90IntegrationVerificationResult:
        """Authenticate explicit native bytes and verify Wilson-loop evidence.

        Parameters
        ----------
        phase_absolute_tolerance
            Maximum circular Wilson phase-set defect in dimensionless radians.
        loop_unitarity_absolute_tolerance
            Maximum Frobenius unitarity defect for reconstructed Wilson loops.
        minimum_active_overlap_singular_value
            Minimum accepted dimensionless active-overlap singular value.

        Returns
        -------
        Periodic1DWannier90IntegrationVerificationResult
            Authenticated native artifacts and bounded numerical findings.

        Raises
        ------
        ValueError
            If controls are invalid, native artifacts are unavailable or incomplete,
            identities disagree, or represented structures are incompatible.
        """
        return Periodic1DWannier90IntegrationVerifier().execute(
            Periodic1DWannier90IntegrationVerificationRequest(
                self.encoded_documents,
                self.artifact_groups,
                phase_absolute_tolerance,
                loop_unitarity_absolute_tolerance,
                minimum_active_overlap_singular_value,
            )
        )
