"""Cohesive immutable facade for retained periodic-1D Wannier90 integration.

The facade owns encoded documents and explicitly supplied native groups while separate
request-scoped Actions perform correlation and bounded verification. It discovers no
files, invokes no calculator, and assigns no scientific acceptance meaning.
"""

from dataclasses import dataclass

from .encoded_documents import Periodic1DWannier90EncodedDocuments
from .integration_correlation import (
    Periodic1DWannier90IntegrationCorrelationRequest,
    Periodic1DWannier90IntegrationCorrelationResult,
    Periodic1DWannier90IntegrationCorrelator,
)
from .integration_verification import (
    Periodic1DWannier90IntegrationVerificationRequest,
    Periodic1DWannier90IntegrationVerificationResult,
    Periodic1DWannier90IntegrationVerifier,
)
from .native_artifacts import Periodic1DWannier90NativeArtifactGroup


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90Integration:
    """Encapsulate immutable integration state behind cohesive Actions.

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
    claim. ``verify`` repeats and preserves that result-first correlation before it
    requires complete native artifact groups and applies explicit bounded Wilson-loop
    verification controls. Neither operation executes
    Wannier90 or discovers files from ambient paths.
    """

    encoded_documents: Periodic1DWannier90EncodedDocuments
    artifact_groups: tuple[Periodic1DWannier90NativeArtifactGroup, ...] = ()

    def __post_init__(self) -> None:
        """Validate exact document ownership and artifact-group inventory."""
        self._check_args_encoded_documents()
        self._check_args_artifact_groups()

    def _check_args_encoded_documents(self) -> None:
        """Require the exact encoded-document aggregate.

        Raises
        ------
        TypeError
            If another semantic record is supplied.
        """
        if type(self.encoded_documents) is not Periodic1DWannier90EncodedDocuments:
            raise TypeError(
                "encoded_documents must be Periodic1DWannier90EncodedDocuments"
            )

    def _check_args_artifact_groups(self) -> None:
        """Require an immutable typed inventory with unique explicit group IDs.

        Raises
        ------
        TypeError
            If the inventory is not an exact tuple of native artifact groups.
        ValueError
            If explicit group identifiers are repeated.
        """
        if type(self.artifact_groups) is not tuple or any(
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
            Authenticated campaign/result correlation, native artifacts, and bounded
            numerical findings.

        Raises
        ------
        TypeError
            If a control or nested retained/native value has the wrong exact
            representation.
        ValueError
            If controls are invalid, campaign or native identities disagree, native
            artifacts are unavailable or incomplete, or represented structures are
            incompatible.
        UnicodeDecodeError
            If retained JSON is not valid UTF-8 after the applicable result-first
            authentication boundary.
        OverflowError
            If a required retained or native numeric value cannot be represented in
            the documented binary64/complex128 representation.
        numpy.linalg.LinAlgError
            If a dense singular-value or eigenvalue decomposition does not converge.
        MemoryError
            If strict decoding, native parsing, or dense verification cannot allocate
            required storage.
        RecursionError
            If retained JSON exceeds parser recursion limits.
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
