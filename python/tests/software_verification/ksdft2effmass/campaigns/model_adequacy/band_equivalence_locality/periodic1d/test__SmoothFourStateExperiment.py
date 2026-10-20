"""Software verification for the exploratory smooth non-flat realization."""

from __future__ import annotations

import math
from dataclasses import replace

import numpy as np
import pytest

from ksdft2effmass.campaigns.model_adequacy.band_equivalence_locality.periodic1d import (  # noqa: E501
    SmoothFourStateAdaptiveAmplitudeDefinition,
    SmoothFourStateAdaptiveAmplitudeExperiment,
    SmoothFourStateAmplitudeThresholds,
    SmoothFourStateConvergenceDefinition,
    SmoothFourStateConvergenceDisposition,
    SmoothFourStateConvergenceExperiment,
    SmoothFourStateConvergenceThresholds,
    SmoothFourStateDefinition,
    SmoothFourStateExperiment,
    SmoothFourStateParentFamilyDefinition,
    SmoothFourStateParentFamilyExperiment,
    SmoothFourStateParentFamilyVerifier,
    SmoothFourStateVerifier,
)

pytestmark = pytest.mark.software_verification


class TestSmoothFourStateExperiment:
    """Establish the bounded non-flat model, convergence, and verifier behavior."""

    @staticmethod
    def _definition(mesh_size: int = 32) -> SmoothFourStateDefinition:
        return SmoothFourStateDefinition(
            reciprocal_mesh_size=mesh_size,
            amplitudes=(0.0, math.pi / 8.0, math.pi / 4.0),
            minimum_external_gap=1.0,
            minimum_transport_singular_value=0.99,
            frame_absolute_tolerance=1.0e-11,
            harmonic_absolute_degeneracy_tolerance=1.0e-14,
            harmonic_relative_degeneracy_tolerance=1.0e-13,
            verification_absolute_tolerance=1.0e-10,
            parent_hopping_scale=1.0,
        )

    @staticmethod
    def _thresholds(parent_change: float) -> SmoothFourStateConvergenceThresholds:
        return SmoothFourStateConvergenceThresholds(
            maximum_parent_diagnostic_change=parent_change,
            maximum_correlation_change=1.01e-8,
            maximum_threshold_change=1.01e-8,
            maximum_hopping_weight_change=1.01e-8,
            maximum_hopping_block_power_change=1.01e-8,
            maximum_angle_change=1.01e-8,
            maximum_band_defect=1.01e-8,
            maximum_reconstruction_defect=1.01e-8,
            maximum_parseval_defect=1.01e-8,
        )

    @classmethod
    def _convergence_definition(
        cls, parent_change: float
    ) -> SmoothFourStateConvergenceDefinition:
        return SmoothFourStateConvergenceDefinition(
            reciprocal_mesh_sizes=(32, 64),
            amplitudes=(0.0, math.pi / 8.0, math.pi / 4.0),
            minimum_external_gap=1.0,
            minimum_transport_singular_value=0.99,
            frame_absolute_tolerance=1.0e-11,
            harmonic_absolute_degeneracy_tolerance=1.0e-14,
            harmonic_relative_degeneracy_tolerance=1.0e-13,
            verification_absolute_tolerance=1.0e-10,
            parent_hopping_scale=1.0,
            thresholds=cls._thresholds(parent_change),
            required_stable_refinements=1,
        )

    def test_transport__rejects_rank_deficiency_before_unitary_completion(self) -> None:
        accepted = np.asarray([[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]], dtype=np.complex128)
        rank_deficient = np.asarray(
            [[1.0, 0.0], [0.0, 0.0], [0.0, 1.0]], dtype=np.complex128
        )

        with pytest.raises(ValueError, match="numerically rank deficient"):
            SmoothFourStateExperiment._align_neighbor(
                accepted, rank_deficient, 0.99, 1.0e-12
            )
        at_cutoff = np.asarray(
            [
                [1.0, 0.0],
                [0.0, 0.99],
                [0.0, math.sqrt(1.0 - 0.99**2)],
            ],
            dtype=np.complex128,
        )
        with pytest.raises(ValueError, match="fails before unitary completion"):
            SmoothFourStateExperiment._align_neighbor(
                accepted, at_cutoff, 0.99, 1.0e-12
            )

        raw_frames = np.asarray([accepted, rank_deficient], dtype=np.complex128)
        with pytest.raises(ValueError, match="fails before unitary completion"):
            SmoothFourStateVerifier._frame(raw_frames, self._definition())

    def test_execute__separates_equal_bands_from_nonflat_hopping_locality(self) -> None:
        result = SmoothFourStateExperiment().execute(self._definition())

        assert result.minimum_external_gap > 1.05
        assert result.minimum_transport_singular_value > 0.999
        assert result.maximum_frame_orthonormality_defect < 1.0e-14
        assert result.periodic_closure_defect < 1.0e-14
        zero, intermediate, maximum = result.points
        assert zero.maximum_band_defect == 0.0
        assert zero.discrete_maximum_correlation == 1.0
        assert zero.minimum_operator_threshold == 0.0
        assert maximum.maximum_band_defect < 1.0e-14
        assert (
            maximum.minimum_operator_threshold > intermediate.minimum_operator_threshold
        )
        assert (
            maximum.comparison_nonzero_hopping_weight
            > intermediate.comparison_nonzero_hopping_weight
            > zero.comparison_nonzero_hopping_weight
        )
        assert maximum.reference_nonzero_hopping_weight == pytest.approx(
            zero.reference_nonzero_hopping_weight, abs=1.0e-15
        )
        assert maximum.minimum_loss_reconstruction_defect < 1.0e-14
        assert maximum.reference_parseval_defect < 1.0e-14
        assert maximum.comparison_parseval_defect < 1.0e-14

    def test_verifier__independently_reconstructs_and_detects_tampering(self) -> None:
        result = SmoothFourStateExperiment().execute(self._definition())
        verification = SmoothFourStateVerifier().execute(result)
        assert verification.passes
        assert verification.maximum_absolute_defect < 1.0e-14

        point = result.points[-1]
        tampered_point = replace(
            point,
            comparison_nonzero_hopping_weight=(
                point.comparison_nonzero_hopping_weight + 1.0e-6
            ),
        )
        tampered = replace(result, points=(*result.points[:-1], tampered_point))
        tampered_verification = SmoothFourStateVerifier().execute(tampered)
        assert not tampered_verification.passes
        assert tampered_verification.maximum_absolute_defect == pytest.approx(1.0e-6)

        tampered_maximum = replace(
            point.harmonic_maximum,
            applied_degeneracy_cutoff=(
                point.harmonic_maximum.applied_degeneracy_cutoff + 1.0e-6
            ),
        )
        tampered_harmonic = replace(
            result,
            points=(
                *result.points[:-1],
                replace(point, harmonic_maximum=tampered_maximum),
            ),
        )
        assert not SmoothFourStateVerifier().execute(tampered_harmonic).passes

    def test_convergence__uses_invariants_not_neighbor_overlap_as_a_metric(
        self,
    ) -> None:
        converged = SmoothFourStateConvergenceExperiment().execute(
            self._convergence_definition(1.01e-8)
        )
        assert converged.disposition is SmoothFourStateConvergenceDisposition.CONVERGED
        assert converged.refinements[0].within_tolerances
        coarse, fine = converged.mesh_results
        assert (
            abs(
                fine.minimum_transport_singular_value
                - coarse.minimum_transport_singular_value
            )
            > 1.01e-8
        )
        assert converged.refinements[0].maximum_shared_projector_defect < 1.0e-14

        unresolved = SmoothFourStateConvergenceExperiment().execute(
            self._convergence_definition(1.0e-11)
        )
        assert (
            unresolved.disposition is SmoothFourStateConvergenceDisposition.UNRESOLVED
        )
        assert not unresolved.refinements[0].within_tolerances

    def test_parent_family__separates_parent_dispersion_from_rotation_amplitude(
        self,
    ) -> None:
        template = replace(self._definition(), amplitudes=(0.0, math.pi / 4.0))
        family = SmoothFourStateParentFamilyExperiment().execute(
            SmoothFourStateParentFamilyDefinition(
                template_definition=template,
                parent_hopping_scales=(0.0, 0.5, 1.0),
            )
        )

        onsite, intermediate, full = family.members
        assert onsite.minimum_external_gap > 1.0
        assert full.minimum_external_gap > 1.0
        assert onsite.points[0].reference_nonzero_hopping_weight < 1.0e-28
        assert (
            full.points[0].reference_nonzero_hopping_weight
            > intermediate.points[0].reference_nonzero_hopping_weight
            > onsite.points[0].reference_nonzero_hopping_weight
        )
        assert (
            onsite.points[-1].comparison_nonzero_hopping_weight
            > onsite.points[0].reference_nonzero_hopping_weight
        )
        onsite_endpoint = onsite.points[-1]
        onsite_residual = 1.0 - onsite_endpoint.discrete_maximum_correlation**2
        onsite_excess = (
            onsite_endpoint.comparison_nonzero_hopping_weight
            - onsite_endpoint.reference_nonzero_hopping_weight
        ) / onsite_endpoint.splitting_scale
        assert onsite_excess == pytest.approx(onsite_residual, abs=1.0e-14)
        full_endpoint = full.points[-1]
        full_departure = (
            full_endpoint.comparison_nonzero_hopping_weight
            - full_endpoint.reference_nonzero_hopping_weight
        ) / full_endpoint.splitting_scale - (
            1.0 - full_endpoint.discrete_maximum_correlation**2
        )
        assert full_departure < -0.05
        assert SmoothFourStateVerifier().execute(intermediate).passes
        assert SmoothFourStateParentFamilyVerifier().execute(family).passes

    def test_adaptive_amplitudes__converges_or_remains_unresolved_at_the_cap(
        self,
    ) -> None:
        initial = replace(self._definition(), amplitudes=(0.0, math.pi / 4.0))

        def thresholds(value: float) -> SmoothFourStateAmplitudeThresholds:
            return SmoothFourStateAmplitudeThresholds(
                maximum_correlation_midpoint_defect=value,
                maximum_operator_threshold_midpoint_defect=value,
                maximum_joint_threshold_midpoint_defect=value,
                maximum_hopping_weight_midpoint_defect=value,
                maximum_hopping_block_power_midpoint_defect=value,
            )

        converged = SmoothFourStateAdaptiveAmplitudeExperiment().execute(
            SmoothFourStateAdaptiveAmplitudeDefinition(
                initial_definition=initial,
                thresholds=thresholds(1.0),
                maximum_refinement_levels=1,
                maximum_evaluated_amplitudes=5,
            )
        )
        assert converged.disposition is SmoothFourStateConvergenceDisposition.CONVERGED
        assert converged.levels[0].evaluated_amplitudes == (
            0.0,
            math.pi / 8.0,
            math.pi / 4.0,
        )
        assert converged.validations[0].evaluated_amplitudes == (
            math.pi / 16.0,
            3.0 * math.pi / 16.0,
        )
        assert converged.validations[0].within_tolerances
        assert len(converged.all_evaluated_amplitudes) == 5

        validation_limited = SmoothFourStateAdaptiveAmplitudeExperiment().execute(
            SmoothFourStateAdaptiveAmplitudeDefinition(
                initial_definition=initial,
                thresholds=SmoothFourStateAmplitudeThresholds(
                    maximum_correlation_midpoint_defect=1.0,
                    maximum_operator_threshold_midpoint_defect=1.0,
                    maximum_joint_threshold_midpoint_defect=1.0,
                    maximum_hopping_weight_midpoint_defect=0.0215,
                    maximum_hopping_block_power_midpoint_defect=0.0215,
                ),
                maximum_refinement_levels=1,
                maximum_evaluated_amplitudes=5,
            )
        )
        assert validation_limited.levels[0].within_tolerances
        assert not validation_limited.validations[0].within_tolerances
        assert (
            validation_limited.disposition
            is SmoothFourStateConvergenceDisposition.UNRESOLVED
        )

        observed = converged.levels[0]
        half_margin = 0.5 * initial.verification_absolute_tolerance
        margin_limited = SmoothFourStateAdaptiveAmplitudeExperiment().execute(
            SmoothFourStateAdaptiveAmplitudeDefinition(
                initial_definition=initial,
                thresholds=SmoothFourStateAmplitudeThresholds(
                    maximum_correlation_midpoint_defect=(
                        observed.maximum_correlation_midpoint_defect + half_margin
                    ),
                    maximum_operator_threshold_midpoint_defect=(
                        observed.maximum_operator_threshold_midpoint_defect
                        + half_margin
                    ),
                    maximum_joint_threshold_midpoint_defect=(
                        observed.maximum_joint_threshold_midpoint_defect + half_margin
                    ),
                    maximum_hopping_weight_midpoint_defect=(
                        observed.maximum_hopping_weight_midpoint_defect + half_margin
                    ),
                    maximum_hopping_block_power_midpoint_defect=(
                        observed.maximum_hopping_block_power_midpoint_defect
                        + half_margin
                    ),
                ),
                maximum_refinement_levels=1,
                maximum_evaluated_amplitudes=3,
            )
        )
        assert (
            margin_limited.disposition
            is SmoothFourStateConvergenceDisposition.UNRESOLVED
        )

        unresolved = SmoothFourStateAdaptiveAmplitudeExperiment().execute(
            SmoothFourStateAdaptiveAmplitudeDefinition(
                initial_definition=initial,
                thresholds=thresholds(1.0e-12),
                maximum_refinement_levels=1,
                maximum_evaluated_amplitudes=3,
            )
        )
        assert (
            unresolved.disposition is SmoothFourStateConvergenceDisposition.UNRESOLVED
        )
        assert unresolved.levels[0].failing_interval_count == 1
        assert not unresolved.levels[0].within_tolerances

    def test_execute__fails_closed_on_unmet_gap_and_invalid_public_scalars(
        self,
    ) -> None:
        with pytest.raises(ValueError, match="external gap"):
            SmoothFourStateExperiment().execute(
                replace(self._definition(), minimum_external_gap=1.1)
            )
        with pytest.raises(TypeError, match=r"amplitudes\[1\]"):
            replace(self._definition(), amplitudes=(0.0, True))
