"""Native-artifact and Wilson verification Action for the integration facade.

The Action first performs result-first composite-input authentication, then adapts the
same explicit result wire, immutable native state, and caller-supplied numerical
controls to the verified native Workflow. Campaign correlation, native authentication,
parsing, numerical verification, and aggregate disposition remain represented by
distinct Results.
"""

from dataclasses import dataclass

import numpy as np

from .correlation import (
    Periodic1DWannier90CampaignWorkflow,
    Periodic1DWannier90CampaignWorkflowRequest,
    Periodic1DWannier90CampaignWorkflowResult,
)
from .encoded_documents import Periodic1DWannier90EncodedDocuments
from .native_artifacts import (
    Periodic1DWannier90NativeArtifactGroup,
    Periodic1DWannier90NativeArtifactWorkflowRequest,
)
from .verified_workflow import (
    Periodic1DWannier90VerifiedNativeWorkflow,
    Periodic1DWannier90VerifiedNativeWorkflowRequest,
    Periodic1DWannier90VerifiedNativeWorkflowResult,
)


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90IntegrationVerificationRequest:
    """Request native correlation and Wilson verification with explicit controls.

    Parameters
    ----------
    encoded_documents
        Exact retained input/result wires and explicit result kind.
    artifact_groups
        Complete caller-supplied native groups; no files are discovered.
    phase_absolute_tolerance
        Maximum circular phase defect in dimensionless radians.
    loop_unitarity_absolute_tolerance
        Maximum Frobenius defect from loop unitarity.
    minimum_active_overlap_singular_value
        Lower conditioning threshold for every selected overlap.

    Raises
    ------
    TypeError
        If records, containers, or controls have wrong exact representations.
    ValueError
        If group identities repeat or a control is nonfinite or negative.
    """

    encoded_documents: Periodic1DWannier90EncodedDocuments
    artifact_groups: tuple[Periodic1DWannier90NativeArtifactGroup, ...]
    phase_absolute_tolerance: float
    loop_unitarity_absolute_tolerance: float
    minimum_active_overlap_singular_value: float

    def __post_init__(self) -> None:
        """Validate exact integration state, inventory, and numerical controls."""
        self._check_args_encoded_documents()
        self._check_args_artifact_groups()
        self._check_args_numerical_controls()

    def _check_args_encoded_documents(self) -> None:
        """Require the exact encoded-document aggregate."""
        if type(self.encoded_documents) is not Periodic1DWannier90EncodedDocuments:
            raise TypeError(
                "encoded_documents must be Periodic1DWannier90EncodedDocuments"
            )

    def _check_args_artifact_groups(self) -> None:
        """Require an exact typed tuple with unique explicit group identifiers."""
        if type(self.artifact_groups) is not tuple or any(
            type(group) is not Periodic1DWannier90NativeArtifactGroup
            for group in self.artifact_groups
        ):
            raise TypeError("artifact_groups must be a typed tuple")
        group_ids = tuple(group.group_id for group in self.artifact_groups)
        if len(set(group_ids)) != len(group_ids):
            raise ValueError("native artifact group identifiers must be unique")

    def _check_args_numerical_controls(self) -> None:
        """Require finite nonnegative built-in-float verification bounds."""
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
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90IntegrationVerificationResult:
    """Retain campaign correlation, native authentication, and Wilson verification.

    Parameters
    ----------
    campaign_correlation
        Result-first authenticated composite-input/result correlation.
    native_verification
        Complete verified-native Workflow result over the same result bytes.

    Raises
    ------
    TypeError
        If either nested Result has the wrong exact semantic type.
    ValueError
        If the campaign correlation and native verification do not retain the same
        exact result bytes and explicit result kind.

    Notes
    -----
    The Result keeps campaign-wire authentication distinct from native-byte and
    numerical evidence. It does not convert bounded software verification into
    scientific validation, UQ, or acceptance.
    """

    campaign_correlation: Periodic1DWannier90CampaignWorkflowResult
    native_verification: Periodic1DWannier90VerifiedNativeWorkflowResult

    def __post_init__(self) -> None:
        """Require exact nested Result types and identical retained result wires."""
        self._check_args_result_types()
        self._check_args_result_correlation()

    def _check_args_result_types(self) -> None:
        """Require exact campaign and native verification Result types."""
        if (
            type(self.campaign_correlation)
            is not Periodic1DWannier90CampaignWorkflowResult
        ):
            raise TypeError(
                "campaign_correlation uses the wrong AbstractResultObject type"
            )
        if (
            type(self.native_verification)
            is not Periodic1DWannier90VerifiedNativeWorkflowResult
        ):
            raise TypeError(
                "native_verification uses the wrong AbstractResultObject type"
            )

    def _check_args_result_correlation(self) -> None:
        """Require both routes to consume identical bytes under one explicit kind."""
        correlated_source = self.campaign_correlation.campaign_result.source_document
        native_artifacts = self.native_verification.native_artifact_result
        native_source = native_artifacts.campaign_result.source_document
        if (
            correlated_source.kind is not native_source.kind
            or correlated_source.source_document != native_source.source_document
        ):
            raise ValueError(
                "campaign and native verification result wires do not agree"
            )

    @property
    def passes(self) -> bool:
        """Return the bounded native/Wilson verification disposition.

        Returns
        -------
        bool
            ``True`` exactly when every retained verification group satisfies its
            explicit phase, loop-unitarity, and overlap-conditioning controls.
        """
        return self.native_verification.passes


class Periodic1DWannier90IntegrationVerifier:
    """Authenticate campaign/native bytes and verify Wilson-loop evidence.

    The request-scoped Action authenticates the opaque composite input against the
    result declaration before building native and verified Workflow requests from the
    same result wire and immutable integration state. It neither caches mutable
    collaborators nor discovers files or invokes external executables.
    """

    __slots__ = ()

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
        UnicodeDecodeError
            If retained JSON is not valid UTF-8 after the applicable result-first
            authentication boundary.
        OverflowError
            If a required retained or native value is not representable in the
            documented binary64/complex128 representation.
        numpy.linalg.LinAlgError
            If a dense singular-value or eigenvalue decomposition does not converge.
        MemoryError
            If strict decoding or dense numerical reconstruction cannot allocate its
            required storage.
        RecursionError
            If retained JSON exceeds parser recursion limits.
        """
        if type(request) is not Periodic1DWannier90IntegrationVerificationRequest:
            raise TypeError(
                "request must be Periodic1DWannier90IntegrationVerificationRequest"
            )
        encoded_documents = request.encoded_documents
        # Authenticate the still-opaque composite input against the strictly decoded
        # result before any native scientific text is parsed or numerically consumed.
        campaign_correlation = Periodic1DWannier90CampaignWorkflow().execute(
            Periodic1DWannier90CampaignWorkflowRequest(
                encoded_documents.composite_input_payload,
                encoded_documents.result_payload,
                encoded_documents.result_kind,
            )
        )
        native_request = Periodic1DWannier90NativeArtifactWorkflowRequest(
            encoded_documents.result_payload,
            encoded_documents.result_kind,
            request.artifact_groups,
        )
        result = Periodic1DWannier90VerifiedNativeWorkflow().execute(
            Periodic1DWannier90VerifiedNativeWorkflowRequest(
                native_request,
                request.phase_absolute_tolerance,
                request.loop_unitarity_absolute_tolerance,
                request.minimum_active_overlap_singular_value,
            )
        )
        return Periodic1DWannier90IntegrationVerificationResult(
            campaign_correlation, result
        )


__all__ = [
    "Periodic1DWannier90IntegrationVerificationRequest",
    "Periodic1DWannier90IntegrationVerificationResult",
    "Periodic1DWannier90IntegrationVerifier",
]
