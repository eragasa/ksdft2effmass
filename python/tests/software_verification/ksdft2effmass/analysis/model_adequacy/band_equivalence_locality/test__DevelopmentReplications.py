"""Software verification for bounded dimensional methodology replications."""

import hashlib
import math
from dataclasses import replace

import pytest
from jsonschema import (  # type: ignore[import-untyped]
    Draft202012Validator,
    ValidationError,
)
from scipy.special import j0  # type: ignore[import-untyped]

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality import (
    DevelopmentCalculator,
    DevelopmentCase,
    DevelopmentDefinition,
    DevelopmentFamily,
    DevelopmentRefinementAnalyzer,
    DevelopmentResult,
    DevelopmentVerifier,
    GaugeNormalization,
    ParentKind,
    canonical_json_bytes,
    development_definition_document,
    development_input_schema,
    development_refinement_document,
    development_refinement_schema,
    development_result_document,
    development_result_schema,
    development_verification_document,
    development_verification_schema,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestDevelopmentReplications:
    """Establish independent family controls and complete smoke diagnostics."""

    def test_module_ownership__separates_domain_action_records_and_wire_format(
        self,
    ) -> None:
        assert DevelopmentDefinition.__module__.endswith(".definitions")
        assert DevelopmentCalculator.__module__.endswith(".development")
        assert DevelopmentResult.__module__.endswith(".records")
        assert development_result_document.__module__.endswith(".serialization")

    def test_square__monkhorst_pack_chain__reconstructs_and_verifies(self) -> None:
        definition = DevelopmentDefinition(
            family=DevelopmentFamily.SQUARE,
            cases=(self._square_directed(),),
            construction_size=6,
            evaluation_size=7,
            evaluation_shift=1.0 / 3.0,
            parent_scales=(0.0, 1.0),
            amplitudes=(0.0, math.pi / 16.0, math.pi / 8.0),
            band_tolerances=(1.0e-3,),
            shell_cap=5,
        )

        result = DevelopmentCalculator().execute(definition)
        verification = DevelopmentVerifier().execute(definition, result)

        assert result.status == "development-smoke-not-retained-evidence"
        assert verification.passes
        assert len(result.cases) == 1
        case = result.cases[0]
        assert case.construction_evaluation_minimum_separation > 0.0
        assert case.metric_covariance_defect == 0.0
        assert len(case.points) == 6
        assert case.amplitude_midpoint.applicable
        assert case.amplitude_midpoint.amplitude_nodes == 3
        assert (
            case.amplitude_midpoint.endpoint_minimum_threshold_over_sqrt_splitting
            is not None
        )
        assert (
            case.amplitude_midpoint.maximum_operator_threshold_midpoint_defect
            is not None
        )
        assert (
            case.amplitude_midpoint.maximum_hopping_block_power_midpoint_defect
            is not None
        )
        assert len(case.flat_amplitude_resolution) == 10
        assert case.flat_amplitude_resolution[-1].amplitude_nodes == 4097
        assert all(
            item.passes_unit_scale_draft_tolerance is None
            for item in case.flat_amplitude_resolution
        )
        assert (
            case.flat_amplitude_resolution[
                -1
            ].maximum_operator_threshold_midpoint_interpolation_defect
            < case.flat_amplitude_resolution[
                0
            ].maximum_operator_threshold_midpoint_interpolation_defect
        )
        assert (
            max(point.reference_fourier_reconstruction_defect for point in case.points)
            < 1.0e-12
        )
        assert (
            max(point.comparison_fourier_reconstruction_defect for point in case.points)
            < 1.0e-12
        )
        assert (
            min(point.minimum_sampled_transport_singular_value for point in case.points)
            > 0.99
        )
        assert (
            max(point.maximum_transport_unitarity_defect for point in case.points)
            < 1.0e-12
        )
        assert (
            max(
                point.maximum_closure_holonomy_unitarity_defect for point in case.points
            )
            < 1.0e-12
        )
        assert all(
            len(point.maximum_absolute_closure_holonomy_phases) == 2
            for point in case.points
        )
        for point in case.points:
            if point.amplitude == 0.0 and point.alignment_applicable:
                assert point.finite_mesh_maximum_correlation == 1.0
                assert point.minimum_operator_threshold == 0.0
                assert point.exact_spectrum_joint_operator_threshold == 0.0
        for point in case.points:
            for shell in point.shell_diagnostics:
                assert shell.reference_total_omitted_power == pytest.approx(
                    shell.reference_omitted_power + point.reference_nyquist_power
                )
                assert shell.comparison_total_omitted_power == pytest.approx(
                    shell.comparison_omitted_power + point.comparison_nyquist_power
                )
            for decision in point.first_passing:
                for shell_index, passing, preceding in (
                    (
                        decision.reference_band_shell,
                        decision.reference_band_passing_error,
                        decision.reference_band_preceding_error,
                    ),
                    (
                        decision.comparison_band_shell,
                        decision.comparison_band_passing_error,
                        decision.comparison_band_preceding_error,
                    ),
                    (
                        decision.reference_hamiltonian_shell,
                        decision.reference_hamiltonian_passing_error,
                        decision.reference_hamiltonian_preceding_error,
                    ),
                    (
                        decision.comparison_hamiltonian_shell,
                        decision.comparison_hamiltonian_passing_error,
                        decision.comparison_hamiltonian_preceding_error,
                    ),
                ):
                    if shell_index is None:
                        assert passing is None
                        assert preceding is None
                    else:
                        assert passing is not None
                        assert passing <= decision.tolerance
                        if preceding is not None:
                            assert preceding > decision.tolerance

    def test_square_flat_parent__alignment_channels__repeat_paper1_thresholds(
        self,
    ) -> None:
        amplitude = math.pi / 8.0
        definition = DevelopmentDefinition(
            family=DevelopmentFamily.SQUARE,
            cases=(self._square_directed(),),
            construction_size=16,
            evaluation_size=17,
            evaluation_shift=1.0 / 3.0,
            parent_scales=(0.0,),
            amplitudes=(amplitude,),
            band_tolerances=(1.0e-3,),
            shell_cap=5,
        )

        point = DevelopmentCalculator().execute(definition).cases[0].points[0]
        correlation = float(j0(amplitude)) ** 2

        assert point.finite_mesh_maximum_correlation == pytest.approx(
            correlation, abs=2.0e-15
        )
        assert point.minimum_operator_threshold == pytest.approx(
            math.sqrt(point.splitting_scale * (1.0 - correlation**2)),
            abs=2.0e-15,
        )
        assert point.exact_spectrum_joint_operator_threshold == pytest.approx(
            math.sqrt(2.0 * point.splitting_scale * (1.0 - correlation)),
            abs=2.0e-15,
        )
        assert point.restricted_global_rotation_residual == (
            point.minimum_operator_threshold
        )
        assert point.analytic_flat_correlation == pytest.approx(correlation)
        assert point.correlation_quadrature_defect is not None
        assert point.correlation_quadrature_defect < 2.0e-15
        assert point.reference_nononsite_power < 2.0e-30
        assert point.flat_residual_tail_identity_defect is not None
        assert point.flat_residual_tail_identity_defect < 2.0e-15
        assert point.minimum_operator_threshold_over_sqrt_splitting == pytest.approx(
            math.sqrt(1.0 - correlation**2)
        )
        assert point.exact_spectrum_joint_threshold_over_sqrt_splitting == (
            pytest.approx(math.sqrt(2.0 * (1.0 - correlation)))
        )
        assert point.normalized_squared_operator_residual == pytest.approx(
            1.0 - correlation**2
        )
        assert point.normalized_excess_nonzero_hopping_weight == pytest.approx(
            1.0 - correlation**2
        )
        assert point.flat_identity_departure == pytest.approx(0.0, abs=2.0e-15)

    def test_graphene_and_silicon__repeat_full_chain_with_basis_diagnostics(
        self,
    ) -> None:
        families = (
            DevelopmentDefinition(
                family=DevelopmentFamily.GRAPHENE_INSPIRED,
                cases=(self._graphene(),),
                construction_size=4,
                evaluation_size=5,
                evaluation_shift=1.0 / 3.0,
                parent_scales=(1.0,),
                amplitudes=(math.pi / (8.0 * math.sqrt(6.0)),),
                band_tolerances=(1.0e-2,),
                shell_cap=2,
            ),
            DevelopmentDefinition(
                family=DevelopmentFamily.SILICON_INSPIRED,
                cases=(self._silicon(),),
                construction_size=4,
                evaluation_size=5,
                evaluation_shift=1.0 / 3.0,
                parent_scales=(1.0,),
                amplitudes=(math.pi / (8.0 * math.sqrt(12.0)),),
                band_tolerances=(1.0e-2,),
                shell_cap=2,
            ),
        )

        for definition in families:
            result = DevelopmentCalculator().execute(definition)
            verification = DevelopmentVerifier().execute(definition, result)
            point = result.cases[0].points[0]

            assert verification.passes
            assert point.continuous_external_gap_lower_bound == pytest.approx(1.84)
            assert point.minimum_sampled_external_gap >= 1.84
            assert point.basis_distance_minimum is not None
            assert point.basis_distance_maximum is not None
            assert point.maximum_direct_band_defect < 1.0e-12
            assert point.maximum_covariant_defect == 0.0

    def test_three_level_refinement__reports_changes_and_unresolved_tolerances(
        self,
    ) -> None:
        base = DevelopmentDefinition(
            family=DevelopmentFamily.SQUARE,
            cases=(self._square_directed(),),
            construction_size=4,
            evaluation_size=9,
            evaluation_shift=1.0 / 3.0,
            parent_scales=(0.0, 1.0),
            amplitudes=(0.0, math.pi / 16.0, math.pi / 8.0),
            band_tolerances=(1.0e-3,),
            shell_cap=2,
        )
        definitions = (
            base,
            replace(base, construction_size=8, evaluation_size=17),
            replace(base, construction_size=16, evaluation_size=33),
        )
        results = tuple(DevelopmentCalculator().execute(item) for item in definitions)
        assessment = DevelopmentRefinementAnalyzer().execute(
            results, ("0" * 64, "1" * 64, "2" * 64)
        )
        document = development_refinement_document(assessment)

        Draft202012Validator(
            development_refinement_schema(DevelopmentFamily.SQUARE)
        ).validate(document)
        assert len(assessment.refinements) == 2
        assert assessment.momentum_disposition == "unresolved"
        assert assessment.passes_draft_tolerance is None
        assert assessment.passes_unit_scale_draft_tolerance is None
        assert not assessment.paper1_literal_range_endpoints_applicable
        assert all(
            item.within_draft_tolerances is None for item in assessment.refinements
        )
        assert all(
            not item.shared_mesh_quantities_applicable
            for item in assessment.refinements
        )
        assert all(
            item.maximum_shared_parent_eigenvalue_defect is None
            for item in assessment.refinements
        )

    def test_documents__strict_family_schemas_and_hash_binding__reject_tampering(
        self,
    ) -> None:
        definition = DevelopmentDefinition(
            family=DevelopmentFamily.SQUARE,
            cases=(self._square_directed(),),
            construction_size=4,
            evaluation_size=5,
            evaluation_shift=1.0 / 3.0,
            parent_scales=(1.0,),
            amplitudes=(math.pi / 8.0,),
            band_tolerances=(1.0e-3,),
            shell_cap=2,
        )
        result = DevelopmentCalculator().execute(definition)
        verification = DevelopmentVerifier().execute(definition, result)
        input_document = development_definition_document(definition)
        result_document = development_result_document(result)
        verification_document = development_verification_document(verification)

        Draft202012Validator(development_input_schema(definition.family)).validate(
            input_document
        )
        Draft202012Validator(development_result_schema(definition.family)).validate(
            result_document
        )
        Draft202012Validator(
            development_verification_schema(definition.family)
        ).validate(verification_document)
        assert hashlib.sha256(canonical_json_bytes(input_document)).hexdigest() == (
            verification.input_sha256
        )
        assert hashlib.sha256(canonical_json_bytes(result_document)).hexdigest() == (
            verification.result_sha256
        )

        tampered_input = dict(input_document)
        tampered_input["shell_cap"] = 3
        assert hashlib.sha256(canonical_json_bytes(tampered_input)).hexdigest() != (
            verification.input_sha256
        )
        tampered = dict(result_document)
        tampered["unexpected"] = "rejected"
        with pytest.raises(ValidationError):
            Draft202012Validator(development_result_schema(definition.family)).validate(
                tampered
            )
        assert hashlib.sha256(canonical_json_bytes(tampered)).hexdigest() != (
            verification.result_sha256
        )

    def test_definition__invalid_mesh_and_family_controls__fail_closed(self) -> None:
        with pytest.raises(ValueError, match="even"):
            DevelopmentDefinition(
                family=DevelopmentFamily.SQUARE,
                cases=(self._square_directed(),),
                construction_size=5,
                evaluation_size=7,
                evaluation_shift=1.0 / 3.0,
                parent_scales=(1.0,),
                amplitudes=(0.0,),
                band_tolerances=(1.0e-3,),
                shell_cap=2,
            )

        with pytest.raises(ValueError, match="one dimension"):
            DevelopmentDefinition(
                family=DevelopmentFamily.SQUARE,
                cases=(self._square_directed(), self._silicon()),
                construction_size=4,
                evaluation_size=5,
                evaluation_shift=1.0 / 3.0,
                parent_scales=(1.0,),
                amplitudes=(0.0,),
                band_tolerances=(1.0e-3,),
                shell_cap=2,
            )

    @staticmethod
    def _square_directed() -> DevelopmentCase:
        return DevelopmentCase(
            name="square-directed-parent",
            dimension=2,
            parent_kind=ParentKind.DIRECTED_AXIS,
            gauge_normalization=GaugeNormalization.AXIS_MAXIMUM,
            positive_bonds=((1, 0), (0, 1)),
            metric=((1.0, 0.0), (0.0, 1.0)),
            shell_metric_scale=1.0,
        )

    @staticmethod
    def _graphene() -> DevelopmentCase:
        return DevelopmentCase(
            name="graphene-inspired-honeycomb",
            dimension=2,
            parent_kind=ParentKind.BIPARTITE_INSPIRED,
            gauge_normalization=GaugeNormalization.BOND_RMS,
            positive_bonds=((1, 0), (0, 1), (1, -1)),
            metric=((1.0, 0.5), (0.5, 1.0)),
            shell_metric_scale=1.0,
            basis_offsets=((0.0, 0.0), (1.0 / 3.0, 1.0 / 3.0)),
        )

    @staticmethod
    def _silicon() -> DevelopmentCase:
        return DevelopmentCase(
            name="silicon-inspired-diamond",
            dimension=3,
            parent_kind=ParentKind.BIPARTITE_INSPIRED,
            gauge_normalization=GaugeNormalization.BOND_RMS,
            positive_bonds=(
                (1, 0, 0),
                (0, 1, 0),
                (0, 0, 1),
                (-1, 1, 0),
                (-1, 0, 1),
                (0, -1, 1),
            ),
            metric=(
                (0.5, 0.25, 0.25),
                (0.25, 0.5, 0.25),
                (0.25, 0.25, 0.5),
            ),
            shell_metric_scale=2.0,
            basis_offsets=(
                (0.0, 0.0, 0.0),
                (1.0 / 4.0, 1.0 / 4.0, 1.0 / 4.0),
            ),
        )
