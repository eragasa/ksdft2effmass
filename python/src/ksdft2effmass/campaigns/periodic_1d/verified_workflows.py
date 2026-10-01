r"""Integrated native-artifact and Wilson verification Workflow for Appendix G.

The Workflow is the supported orchestration boundary for retained Wannier90 Wilson
evidence.  It first authenticates every caller-supplied artifact against the retained
name, byte-count, and SHA-256 inventory; parses the supported native scientific text
formats; correlates parsed centers and dimensions; and only then performs independent
Wilson-loop reconstruction.  Authentication, parsing, correlation, and numerical
verification remain distinct ResultObjects in the returned composition.

No path, run root, or executable is discovered.  No electronic-structure or Wannier90
calculation is started.  A passing result is bounded verification of the represented
synthetic records, not scientific acceptance.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .native_artifact_workflows import (
    Periodic1DWannier90NativeArtifactWorkflow,
    Periodic1DWannier90NativeArtifactWorkflowRequest,
    Periodic1DWannier90NativeArtifactWorkflowResult,
)
from .verification import (
    Periodic1DWannier90WilsonVerificationRequest,
    Periodic1DWannier90WilsonVerificationResult,
    Periodic1DWannier90WilsonVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90VerifiedNativeWorkflowRequest:
    """Declare native correlation inputs and independent Wilson verification controls.

    Parameters
    ----------
    native_artifact_request
        Retained result bytes, result kind, and complete caller-supplied artifact
        groups.
    phase_absolute_tolerance
        Maximum accepted circular Wilson phase-set defect in dimensionless radians.
    loop_unitarity_absolute_tolerance
        Maximum accepted Frobenius defect of either reconstructed Wilson loop from
        identity unitarity.
    minimum_active_overlap_singular_value
        Minimum accepted singular value among selected active reciprocal-neighbor
        overlaps.

    Notes
    -----
    The nested native request owns bytes and artifact identities.  This request adds
    only numerical-verification controls; it cannot authorize execution or modify the
    meaning of the retained result.

    See Also
    --------
    Periodic1DWannier90NativeArtifactWorkflowRequest
        Lower-level native authentication and parsing request.
    Periodic1DWannier90WilsonVerificationRequest
        Verification request constructed internally after native correlation.
    """

    native_artifact_request: Periodic1DWannier90NativeArtifactWorkflowRequest
    phase_absolute_tolerance: float
    loop_unitarity_absolute_tolerance: float
    minimum_active_overlap_singular_value: float

    def __post_init__(self) -> None:
        """Validate exact request ownership and finite nonnegative controls.

        Raises
        ------
        TypeError
            If ``native_artifact_request`` has the wrong exact semantic type.
        ValueError
            If any numerical control is not a finite nonnegative built-in ``float``.
        """
        if (
            type(self.native_artifact_request)
            is not Periodic1DWannier90NativeArtifactWorkflowRequest
        ):
            raise TypeError(
                "native_artifact_request must be the native Workflow request"
            )
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
class Periodic1DWannier90VerifiedNativeWorkflowResult:
    """Retain correlated native artifacts and independent Wilson verification.

    Parameters
    ----------
    native_artifact_result
        Complete authenticated artifact identities and parsed native records.
    wilson_verification
        Independent raw-overlap and native-gauge Wilson verification for the same
        ordered group inventory.

    Notes
    -----
    Both ResultObjects are preserved so a caller can distinguish authentication or
    parsing evidence from numerical Wilson evidence.  ``passes`` delegates only to the
    Wilson-verification disposition because incompatible native inputs are rejected
    before this ResultObject can be constructed.
    """

    native_artifact_result: Periodic1DWannier90NativeArtifactWorkflowResult
    wilson_verification: Periodic1DWannier90WilsonVerificationResult

    def __post_init__(self) -> None:
        """Validate ResultObject types and ordered group correlation.

        Raises
        ------
        TypeError
            If either value has the wrong exact ResultObject type.
        ValueError
            If native and Wilson-verification group identifiers differ or are reordered.
        """
        if (
            type(self.native_artifact_result)
            is not Periodic1DWannier90NativeArtifactWorkflowResult
        ):
            raise TypeError(
                "native_artifact_result uses the wrong Workflow ResultObject"
            )
        if (
            type(self.wilson_verification)
            is not Periodic1DWannier90WilsonVerificationResult
        ):
            raise TypeError("wilson_verification uses the wrong ResultObject")
        native_ids = tuple(
            group.group_id for group in self.native_artifact_result.groups
        )
        verification_ids = tuple(
            group.group_id for group in self.wilson_verification.groups
        )
        if verification_ids != native_ids:
            raise ValueError(
                "native and Wilson verification group inventories disagree"
            )

    @property
    def passes(self) -> bool:
        """Return the independent Wilson verification disposition.

        Returns
        -------
        bool
            ``True`` exactly when every Wilson verification group passes its explicit
            phase, unitarity, and overlap-conditioning controls.
        """
        return self.wilson_verification.passes


class Periodic1DWannier90VerifiedNativeWorkflow:
    """Compose native authentication, parsing, correlation, and Wilson verification.

    Processing order is fixed:

    1. deserialize the retained result and its expected artifact inventory;
    2. authenticate all caller-supplied native bytes;
    3. parse the seven supported scientific text artifacts;
    4. correlate native dimensions, centers, and retained band-group rank; and
    5. independently reconstruct and compare raw and native-gauge Wilson loops.

    A numerical failure is retained as ``passes=False``.  Structural incompatibility,
    missing artifacts, identity disagreement, or an incomplete reciprocal loop raises
    an exception because no meaningful verification result can then be formed.

    Notes
    -----
    The Workflow consumes only explicit immutable bytes.  It performs no filesystem
    discovery, Wannier90 execution, historical extractor execution, scientific
    validation, or uncertainty quantification.  The physical background is discussed
    in [WVFKS1993]_ and [WVFM2012]_; the Workflow itself makes only the bounded software
    and numerical claims documented above.

    References
    ----------
    .. [WVFKS1993] R. D. King-Smith and D. Vanderbilt, "Theory of polarization of
       crystalline solids," *Physical Review B* **47**, 1651--1654 (1993).
       https://doi.org/10.1103/PhysRevB.47.1651
    .. [WVFM2012] N. Marzari, A. A. Mostofi, J. R. Yates, I. Souza, and D. Vanderbilt,
       "Maximally localized Wannier functions: Theory and applications,"
       *Reviews of Modern Physics* **84**, 1419--1475 (2012).
       https://doi.org/10.1103/RevModPhys.84.1419

    See Also
    --------
    Periodic1DWannier90NativeArtifactWorkflow
        Lower-level artifact authentication, parsing, and retained correlation.
    Periodic1DWannier90WilsonVerifier
        Independent numerical verifier composed by this Workflow.
    """

    __slots__ = ()

    native_artifact_workflow = Periodic1DWannier90NativeArtifactWorkflow()
    wilson_verifier = Periodic1DWannier90WilsonVerifier()

    def execute(
        self, request: Periodic1DWannier90VerifiedNativeWorkflowRequest
    ) -> Periodic1DWannier90VerifiedNativeWorkflowResult:
        """Authenticate and parse native bytes, then independently verify Wilson loops.

        Parameters
        ----------
        request
            Native artifact request and explicit numerical-verification controls.

        Returns
        -------
        Periodic1DWannier90VerifiedNativeWorkflowResult
            Correlated native artifacts and a pass-or-fail independent Wilson result.

        Raises
        ------
        TypeError
            If ``request`` has the wrong exact semantic type.
        ValueError
            If native identities, inventories, parsed dimensions, centers, or active
            reciprocal-loop structure are incompatible.
        """
        if type(request) is not Periodic1DWannier90VerifiedNativeWorkflowRequest:
            raise TypeError(
                "request must be Periodic1DWannier90VerifiedNativeWorkflowRequest"
            )
        native_result = self.native_artifact_workflow.execute(
            request.native_artifact_request
        )
        verification = self.wilson_verifier.execute(
            Periodic1DWannier90WilsonVerificationRequest(
                native_result,
                request.phase_absolute_tolerance,
                request.loop_unitarity_absolute_tolerance,
                request.minimum_active_overlap_singular_value,
            )
        )
        return Periodic1DWannier90VerifiedNativeWorkflowResult(
            native_result, verification
        )
