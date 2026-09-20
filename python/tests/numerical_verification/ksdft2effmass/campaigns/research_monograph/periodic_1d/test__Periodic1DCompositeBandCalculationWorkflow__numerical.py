r"""Numerical verification of ``Periodic1DCompositeBandCalculationWorkflow``.

Evidence profile: claim_bearing

Bounded artifact scope: execution-local Appendix G finite plane-wave parent matrices,
transported rank-two frames, projectors, Wilson spectra, complete block Fourier
coefficients, finite-range errors, and direct least-squares route comparisons.

Facet and represented meaning

The calculation Workflow's represented finite channels are compared with the direct
NumPy reconstruction owned by ``Periodic1DCompositeBandCalculationVerifier``.

Intrinsic and cross-object scope

The oracle independently assembles matrices, SVD transport, gauge attacks, direct
Fourier sums, eigenspectra, truncations, interpolation, and least squares without
importing production construction or analysis algorithms.

VVUQ and scientific exclusions

A pass establishes numerical verification of the finite represented calculation. It
does not establish basis convergence, material validity, polarization, topology,
scientific validation, uncertainty quantification, or human acceptance.
"""

from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DCompositeBandCalculationGroupResult,
    Periodic1DCompositeBandCalculationRequest,
    Periodic1DCompositeBandCalculationResult,
    Periodic1DCompositeBandCalculationVerificationRequest,
    Periodic1DCompositeBandCalculationVerifier,
    Periodic1DCompositeBandCalculationWorkflow,
    Periodic1DCompositeCampaignDefinition,
    Periodic1DCompositeCampaignJsonSerializer,
)
from ksdft2effmass.operators import ComplexMatrixQuantity, ScalarQuantity, Unitless
from ksdft2effmass.solid_state import (
    BandFrameAlignmentResult1D,
    BandProjectorPathResult1D,
    ReciprocalBandFramePath1D,
    WilsonLoopPhaseSetComparisonResult1D,
    WilsonLoopSpectrum1D,
)

pytestmark = pytest.mark.numerical_verification
SUT = Periodic1DCompositeBandCalculationWorkflow


class TestPeriodic1DCompositeBandCalculationWorkflow:
    """Own independent numerical reconstruction of calculated composite channels."""

    @staticmethod
    def repo_root() -> Path:
        """This helper owns no identifier; it locates the maintained input."""

        return Path(__file__).resolve().parents[7]

    @classmethod
    def definition(cls) -> Periodic1DCompositeCampaignDefinition:
        """This helper owns no identifier; it decodes the maintained input."""

        path = (
            cls.repo_root()
            / "calculations"
            / "research-monograph"
            / "periodic-1d"
            / "composite-input.json"
        )
        return Periodic1DCompositeCampaignJsonSerializer().deserialize(
            path.read_bytes()
        )

    @classmethod
    def request(cls) -> Periodic1DCompositeBandCalculationRequest:
        """This helper owns no identifier; it supplies explicit finite tolerances."""

        return Periodic1DCompositeBandCalculationRequest(
            cls.definition(),
            ScalarQuantity(1.0e-12, Unitless()),
            ScalarQuantity(1.0e-10, Unitless()),
            ScalarQuantity(0.0, Unitless()),
            ScalarQuantity(1.0e-12, Unitless()),
            ScalarQuantity(1.0e-10, Unitless()),
            ScalarQuantity(1.0e-10, Unitless()),
            1.0e-10,
        )

    @staticmethod
    def rank_gauge_path(
        path: ReciprocalBandFramePath1D, phase: float
    ) -> ReciprocalBandFramePath1D:
        """Return a valid path with a constant nontrivial internal gauge."""

        rotation = np.eye(path.rank, dtype=np.complex128)
        rotation[0, 0] = np.exp(1j * phase)
        rotation[1, 1] = np.exp(-1j * phase)
        return ReciprocalBandFramePath1D(
            path.mesh,
            tuple(
                ComplexMatrixQuantity(frame.magnitude @ rotation, Unitless())
                for frame in path.frames
            ),
            path.sewing_map,
            path.orthonormality_absolute_tolerance,
        )

    @staticmethod
    def ambient_rotation_path(
        path: ReciprocalBandFramePath1D, angle: float
    ) -> ReciprocalBandFramePath1D:
        """Return a valid path with a changed represented subspace."""

        rotation = np.eye(path.ambient_dimension, dtype=np.complex128)
        cosine = np.cos(angle)
        sine = np.sin(angle)
        center = path.ambient_dimension // 2
        rotation[center, center] = cosine
        rotation[center, -1] = -sine
        rotation[-1, center] = sine
        rotation[-1, -1] = cosine
        return ReciprocalBandFramePath1D(
            path.mesh,
            tuple(
                ComplexMatrixQuantity(rotation @ frame.magnitude, Unitless())
                for frame in path.frames
            ),
            path.sewing_map,
            path.orthonormality_absolute_tolerance,
        )

    @staticmethod
    def projector_path(
        path: ReciprocalBandFramePath1D,
    ) -> BandProjectorPathResult1D:
        """Construct exact frame projectors with elementary array operations."""

        return BandProjectorPathResult1D(
            path,
            tuple(
                ComplexMatrixQuantity(
                    frame.magnitude @ frame.magnitude.conj().T,
                    Unitless(),
                )
                for frame in path.frames
            ),
        )

    @staticmethod
    def alignment_with_reference(
        alignment: BandFrameAlignmentResult1D,
        reference: ReciprocalBandFramePath1D,
    ) -> BandFrameAlignmentResult1D:
        """Replace only the independent reference and its derived scalar defects."""

        frame_defect = float(
            max(
                np.linalg.norm(aligned.magnitude - reference_frame.magnitude)
                for aligned, reference_frame in zip(
                    alignment.aligned.frames,
                    reference.frames,
                    strict=True,
                )
            )
        )
        projector_defect = float(
            max(
                np.linalg.norm(
                    reference_frame.magnitude @ reference_frame.magnitude.conj().T
                    - candidate_frame.magnitude @ candidate_frame.magnitude.conj().T
                )
                for reference_frame, candidate_frame in zip(
                    reference.frames,
                    alignment.candidate.frames,
                    strict=True,
                )
            )
        )
        return BandFrameAlignmentResult1D(
            reference=reference,
            candidate=alignment.candidate,
            aligned=alignment.aligned,
            rotations=alignment.rotations,
            frame_maximum_frobenius_defect=frame_defect,
            projector_maximum_frobenius_defect=projector_defect,
        )

    @staticmethod
    def alignment_with_candidate_bundle(
        reference: ReciprocalBandFramePath1D,
        candidate: ReciprocalBandFramePath1D,
    ) -> BandFrameAlignmentResult1D:
        """Replace the correlated candidate/aligned/rotation bundle directly."""

        rotations = tuple(
            ComplexMatrixQuantity(
                np.eye(candidate.rank, dtype=np.complex128), Unitless()
            )
            for _ in candidate.frames
        )
        frame_defect = float(
            max(
                np.linalg.norm(candidate_frame.magnitude - reference_frame.magnitude)
                for candidate_frame, reference_frame in zip(
                    candidate.frames,
                    reference.frames,
                    strict=True,
                )
            )
        )
        projector_defect = float(
            max(
                np.linalg.norm(
                    reference_frame.magnitude @ reference_frame.magnitude.conj().T
                    - candidate_frame.magnitude @ candidate_frame.magnitude.conj().T
                )
                for reference_frame, candidate_frame in zip(
                    reference.frames,
                    candidate.frames,
                    strict=True,
                )
            )
        )
        return BandFrameAlignmentResult1D(
            reference=reference,
            candidate=candidate,
            aligned=candidate,
            rotations=rotations,
            frame_maximum_frobenius_defect=frame_defect,
            projector_maximum_frobenius_defect=projector_defect,
        )

    @staticmethod
    def shifted_wilson_comparison(
        comparison: WilsonLoopPhaseSetComparisonResult1D,
        phase_shift: float,
    ) -> WilsonLoopPhaseSetComparisonResult1D:
        """Construct one valid shifted comparison by direct circular arithmetic."""

        candidate = WilsonLoopSpectrum1D(
            tuple(phase + phase_shift for phase in comparison.candidate.eigenphases)
        )
        residuals = tuple(
            float((candidate_phase - reference_phase + np.pi) % (2.0 * np.pi) - np.pi)
            for reference_phase, candidate_phase in zip(
                comparison.reference.eigenphases,
                candidate.eigenphases,
                strict=True,
            )
        )
        maximum = max(abs(residual) for residual in residuals)
        return WilsonLoopPhaseSetComparisonResult1D(
            reference=comparison.reference,
            candidate=candidate,
            matched_candidate_indices=tuple(range(comparison.reference.rank)),
            signed_phase_residuals=residuals,
            maximum_absolute_phase_defect=maximum,
            phase_l2_defect=float(np.linalg.norm(residuals)),
            absolute_tolerance=maximum,
            passes=True,
        )

    @staticmethod
    def replace_first_group(
        calculation: Periodic1DCompositeBandCalculationResult,
        group: Periodic1DCompositeBandCalculationGroupResult,
    ) -> Periodic1DCompositeBandCalculationResult:
        """Return the calculation with one valid adversarial group replacement."""

        return replace(calculation, groups=(group, calculation.groups[1]))

    @staticmethod
    def assert_frame_provenance_rejected(
        calculation: Periodic1DCompositeBandCalculationResult,
    ) -> None:
        """Require the independent verifier to reject altered retained provenance."""

        verification = Periodic1DCompositeBandCalculationVerifier().execute(
            Periodic1DCompositeBandCalculationVerificationRequest(
                calculation,
                ScalarQuantity(1.0e-11, Unitless()),
            )
        )
        assert not verification.passes
        assert not verification.groups[0].passes
        assert (
            verification.groups[
                0
            ].retained_frame_provenance_maximum_absolute_defect.magnitude
            > 1.0e-11
        )

    def test_method__execute__agrees_with_independent_direct_reconstruction(
        self,
    ) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-ONE-D-COMPOSITE-002

        Requirement: Every calculated parent, gauge, Wilson, complete hopping,
        truncation, withheld, and direct-fit channel agrees with an independently
        implemented finite-dimensional route.

        Method: Execute the public Workflow, then pass its complete typed result to
        the direct-NumPy verifier under an explicit unitless tolerance.

        Oracle: The independent verifier's explicit plane-wave matrices, SVD transport,
        deterministic gauge attacks, direct Fourier sums, Hermitian eigenspectra,
        truncation/interpolation, and unconstrained complex least-squares route.

        Acceptance: Every parent and per-group defect is at most ``1e-11`` in the
        Appendix G dimensionless convention and both group dispositions pass.

        Interpretation: A pass establishes numerical verification of the documented
        finite composite calculation and its separate diagnostic channels.

        Limitations: This finite reconstruction does not establish basis convergence,
        material validity, polarization, topology, scientific validation, uncertainty
        quantification, or human acceptance.
        """

        calculated = SUT().execute(self.request())
        verification = Periodic1DCompositeBandCalculationVerifier().execute(
            Periodic1DCompositeBandCalculationVerificationRequest(
                calculated,
                ScalarQuantity(1.0e-11, Unitless()),
            )
        )

        assert verification.passes
        assert (
            verification.parent_representation_maximum_absolute_defect.magnitude == 0.0
        )
        assert verification.parent_operator_maximum_absolute_defect.magnitude == 0.0
        assert verification.parent_eigenframe_maximum_frobenius_defect.magnitude == 0.0
        assert verification.training_eigenvalue_maximum_absolute_defect.magnitude == 0.0
        assert verification.withheld_eigenvalue_maximum_absolute_defect.magnitude == 0.0
        low_pair, higher_pair = verification.groups
        assert low_pair.group_id == "low_pair"
        assert higher_pair.group_id == "higher_pair"
        assert low_pair.passes
        assert higher_pair.passes
        assert low_pair.source_projector_maximum_frobenius_defect.magnitude < 5.0e-12
        assert higher_pair.source_projector_maximum_frobenius_defect.magnitude < 5.0e-12
        assert (
            low_pair.retained_frame_provenance_maximum_absolute_defect.magnitude
            < 5.0e-12
        )
        assert (
            higher_pair.retained_frame_provenance_maximum_absolute_defect.magnitude
            < 5.0e-12
        )
        assert low_pair.smooth_hopping_maximum_absolute_defect.magnitude < 5.0e-12
        assert higher_pair.smooth_hopping_maximum_absolute_defect.magnitude < 5.0e-12
        assert low_pair.range_diagnostic_maximum_absolute_defect.magnitude < 1.0e-11
        assert higher_pair.range_diagnostic_maximum_absolute_defect.magnitude < 1.0e-11
        assert low_pair.direct_route_maximum_absolute_defect.magnitude < 5.0e-12
        assert higher_pair.direct_route_maximum_absolute_defect.magnitude < 5.0e-12

    def test_method__execute__rejects_each_altered_frame_provenance_channel(
        self,
    ) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-ONE-D-COMPOSITE-003

        Requirement: Every independently variable source, transported, controlled,
        aligned, and rough frame path participates in the verification disposition;
        alignment reference and candidate bundles are independently covered.

        Method: Replace each path in turn with a valid but independently altered
        record while leaving reported downstream outcomes unchanged. Mutate the
        alignment reference separately from its correlated candidate/aligned/rotation
        bundle. Construct projectors and alignment records directly from typed
        DataObjects and elementary arrays, without production ActionObjects.

        Oracle: The verifier independently reconstructs direct eigenspaces,
        deterministic gauge attacks, polar transport, pointwise alignment, projectors,
        and rough-gauge paths.

        Acceptance: Altering any independently variable path, the alignment reference,
        or the correlated candidate bundle makes the affected group and complete
        calculation fail through the retained-provenance defect.

        Interpretation: A pass verifies fail-closed coverage of frame paths. Projector
        values cannot vary independently of their source because the public ResultObject
        rejects that state under ``SV-SOLID-STATE-PERIODIC-ONE-D-025``.

        Limitations: The adversarial records are synthetic valid DataObjects, not
        calculated physical evidence. Intrinsically correlated fields are tested by
        their owning DataObject rather than bypassing immutability here.
        """

        calculated = SUT().execute(self.request())
        group = calculated.groups[0]
        altered_source = self.rank_gauge_path(group.source_frames, 0.23)
        source_group = replace(
            group,
            source_frames=altered_source,
            smooth_transport=replace(group.smooth_transport, source=altered_source),
            source_projectors=self.projector_path(altered_source),
        )
        self.assert_frame_provenance_rejected(
            self.replace_first_group(calculated, source_group)
        )

        altered_controlled_source = self.rank_gauge_path(
            group.controlled_source_frames, 0.29
        )
        controlled_source_group = replace(
            group,
            controlled_source_frames=altered_controlled_source,
            controlled_transport=replace(
                group.controlled_transport, source=altered_controlled_source
            ),
            controlled_source_projectors=self.projector_path(altered_controlled_source),
        )
        self.assert_frame_provenance_rejected(
            self.replace_first_group(calculated, controlled_source_group)
        )

        altered_smooth = self.rank_gauge_path(group.smooth_transport.transported, 0.31)
        smooth_group = replace(
            group,
            smooth_transport=replace(
                group.smooth_transport, transported=altered_smooth
            ),
        )
        self.assert_frame_provenance_rejected(
            self.replace_first_group(calculated, smooth_group)
        )

        altered_controlled = self.rank_gauge_path(
            group.controlled_transport.transported, 0.37
        )
        controlled_group = replace(
            group,
            controlled_transport=replace(
                group.controlled_transport, transported=altered_controlled
            ),
        )
        self.assert_frame_provenance_rejected(
            self.replace_first_group(calculated, controlled_group)
        )

        altered_reference = self.ambient_rotation_path(
            group.controlled_alignment.reference, 0.17
        )
        reference_alignment_group = replace(
            group,
            controlled_alignment=self.alignment_with_reference(
                group.controlled_alignment,
                altered_reference,
            ),
        )
        self.assert_frame_provenance_rejected(
            self.replace_first_group(calculated, reference_alignment_group)
        )

        altered_candidate = self.ambient_rotation_path(
            group.controlled_alignment.candidate, 0.19
        )
        candidate_alignment_group = replace(
            group,
            controlled_alignment=self.alignment_with_candidate_bundle(
                group.controlled_alignment.reference,
                altered_candidate,
            ),
        )
        self.assert_frame_provenance_rejected(
            self.replace_first_group(calculated, candidate_alignment_group)
        )

        altered_rough = self.rank_gauge_path(group.rough_frames, 0.41)
        rough_group = replace(group, rough_frames=altered_rough)
        self.assert_frame_provenance_rejected(
            self.replace_first_group(calculated, rough_group)
        )

    def test_method__execute__rejects_altered_transport_and_wilson_diagnostics(
        self,
    ) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-ONE-D-COMPOSITE-004

        Requirement: Smooth and controlled transport diagnostics plus retained Wilson
        comparison data participate independently in the verification disposition.

        Method: Alter each minimum singular value, threshold, and closure-phase record
        separately, then replace the Wilson candidate and derived residuals by direct
        circular arithmetic. Leave all frame paths and downstream outcomes unchanged.

        Oracle: The verifier directly reconstructs transport singular values, request
        thresholds, closure phases, and both Wilson phase multisets.

        Acceptance: Every diagnostic-only or Wilson-only alteration fails the affected
        group and complete calculation through the retained-provenance defect.

        Interpretation: A pass verifies fail-closed diagnostic and Wilson coverage.

        Limitations: These synthetic DataObjects establish verifier sensitivity only,
        not a physical interpretation of Wilson phases.
        """

        calculated = SUT().execute(self.request())
        group = calculated.groups[0]
        smooth = group.smooth_transport
        controlled = group.controlled_transport

        smooth_minimum_group = replace(
            group,
            smooth_transport=replace(
                smooth,
                minimum_overlap_singular_value=(
                    smooth.minimum_overlap_singular_value / 2.0
                ),
            ),
        )
        self.assert_frame_provenance_rejected(
            self.replace_first_group(calculated, smooth_minimum_group)
        )

        smooth_threshold_group = replace(
            group,
            smooth_transport=replace(
                smooth,
                overlap_singular_value_threshold=(
                    smooth.minimum_overlap_singular_value / 4.0
                ),
            ),
        )
        self.assert_frame_provenance_rejected(
            self.replace_first_group(calculated, smooth_threshold_group)
        )

        smooth_phase_group = replace(
            group,
            smooth_transport=replace(
                smooth,
                closure_eigenphases=tuple(
                    phase + 0.07 for phase in smooth.closure_eigenphases
                ),
            ),
        )
        self.assert_frame_provenance_rejected(
            self.replace_first_group(calculated, smooth_phase_group)
        )

        controlled_minimum_group = replace(
            group,
            controlled_transport=replace(
                controlled,
                minimum_overlap_singular_value=(
                    controlled.minimum_overlap_singular_value / 2.0
                ),
            ),
        )
        self.assert_frame_provenance_rejected(
            self.replace_first_group(calculated, controlled_minimum_group)
        )

        controlled_threshold_group = replace(
            group,
            controlled_transport=replace(
                controlled,
                overlap_singular_value_threshold=(
                    controlled.minimum_overlap_singular_value / 4.0
                ),
            ),
        )
        self.assert_frame_provenance_rejected(
            self.replace_first_group(calculated, controlled_threshold_group)
        )

        controlled_phase_group = replace(
            group,
            controlled_transport=replace(
                controlled,
                closure_eigenphases=tuple(
                    phase - 0.09 for phase in controlled.closure_eigenphases
                ),
            ),
        )
        self.assert_frame_provenance_rejected(
            self.replace_first_group(calculated, controlled_phase_group)
        )

        wilson_group = replace(
            group,
            wilson_comparison=self.shifted_wilson_comparison(
                group.wilson_comparison, 0.05
            ),
        )
        self.assert_frame_provenance_rejected(
            self.replace_first_group(calculated, wilson_group)
        )
