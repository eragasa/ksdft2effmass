"""Software verification for bounded dimensional methodology replications."""

import math
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest
from jsonschema import ValidationError  # type: ignore[import-untyped]
from numpy.typing import NDArray
from projectkoios.physkit.periodic.lattice import (
    DirectLattice2D,
    DirectLattice3D,
    DirectLatticeMetric,
)
from scipy.special import j0  # type: ignore[import-untyped]

from ksdft2effmass.analysis.model_adequacy import band_equivalence_locality
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality import (
    calculation,
    definitions,
    records,
)
from ksdft2effmass.application import band_equivalence_locality as application_api
from ksdft2effmass.application.band_equivalence_locality import (
    BandEquivalenceLocalityRefinementAssessor,
    BandEquivalenceLocalityRefinementRequest,
    BandEquivalenceLocalityResultConstructor,
    BandEquivalenceLocalityResultVerifier,
    BandEquivalenceLocalityVerificationRequest,
)
from ksdft2effmass.campaigns.model_adequacy.band_equivalence_locality import (
    schemas,
    serialization,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


class TestBandEquivalenceLocalityApplicationArtifacts:
    """Establish independent family controls and complete smoke diagnostics."""

    def test_public_analysis__calculates_and_verifies_one_request(self) -> None:
        definition = definitions.BandEquivalenceLocalityRequest(
            family=definitions.BandEquivalenceLocalityFamily.SQUARE,
            cases=(self._square_directed(),),
            construction_size=4,
            evaluation_size=5,
            evaluation_shift=1.0 / 3.0,
            parent_scales=(1.0,),
            amplitudes=(math.pi / 8.0,),
            band_tolerances=(1.0e-3,),
            shell_cap=2,
        )
        result = BandEquivalenceLocalityResultConstructor().execute(definition)
        verification = BandEquivalenceLocalityResultVerifier().execute(
            BandEquivalenceLocalityVerificationRequest(
                analysis_request=definition,
                result=result,
            )
        )

        assert verification.diagnostics.passes

    def test_request_serializer__two_and_three_dimensions__round_trips(self) -> None:
        serializer = serialization.BandEquivalenceLocalityRequestSerializer()
        for family, case in (
            (
                definitions.BandEquivalenceLocalityFamily.SQUARE,
                self._square_directed(),
            ),
            (
                definitions.BandEquivalenceLocalityFamily.GRAPHENE_INSPIRED,
                self._graphene(),
            ),
            (
                definitions.BandEquivalenceLocalityFamily.SIMPLE_CUBIC,
                self._simple_cubic_directed(),
            ),
            (
                definitions.BandEquivalenceLocalityFamily.SILICON_INSPIRED,
                self._silicon(),
            ),
        ):
            request = definitions.BandEquivalenceLocalityRequest(
                family=family,
                cases=(case,),
                construction_size=4,
                evaluation_size=5,
                evaluation_shift=1.0 / 3.0,
                parent_scales=(1.0,),
                amplitudes=(math.pi / 8.0,),
                band_tolerances=(1.0e-3,),
                shell_cap=2,
            )
            document = serializer.execute(request)

            reconstructed = serializer.reconstruct(document)

            assert serializer.execute(reconstructed).canonical_bytes() == (
                document.canonical_bytes()
            )

    def test_verification_request__mismatched_analysis_controls__fail_closed(
        self,
    ) -> None:
        request = definitions.BandEquivalenceLocalityRequest(
            family=definitions.BandEquivalenceLocalityFamily.SQUARE,
            cases=(self._square_directed(),),
            construction_size=4,
            evaluation_size=5,
            evaluation_shift=1.0 / 3.0,
            parent_scales=(1.0,),
            amplitudes=(math.pi / 8.0,),
            band_tolerances=(1.0e-3,),
            shell_cap=2,
        )
        result = BandEquivalenceLocalityResultConstructor().execute(request)
        changed_geometry = replace(
            request.cases[0],
            direct_metric=DirectLatticeMetric(
                DirectLattice2D(
                    a1=np.array((2.0, 0.0), dtype=np.float64),
                    a2=np.array((0.0, 1.0), dtype=np.float64),
                )
            ),
        )
        mismatched_requests = (
            replace(request, amplitudes=(0.0,)),
            replace(request, evaluation_shift=0.25),
            replace(request, cases=(changed_geometry,)),
        )

        for mismatched_request in mismatched_requests:
            with pytest.raises(ValueError, match="does not belong"):
                BandEquivalenceLocalityVerificationRequest(
                    analysis_request=mismatched_request,
                    result=result,
                )

        stored_case = result.diagnostics.cases[0]
        stored_point = stored_case.points[0]
        with pytest.raises(ValueError, match="diagnostics do not belong"):
            replace(
                result,
                diagnostics=replace(
                    result.diagnostics,
                    cases=(
                        replace(
                            stored_case,
                            points=(replace(stored_point, amplitude=0.0),),
                        ),
                    ),
                ),
            )

    def test_result__mixed_request_and_diagnostics__fail_closed(self) -> None:
        request = definitions.BandEquivalenceLocalityRequest(
            family=definitions.BandEquivalenceLocalityFamily.SQUARE,
            cases=(self._square_directed(),),
            construction_size=4,
            evaluation_size=5,
            evaluation_shift=1.0 / 3.0,
            parent_scales=(1.0,),
            amplitudes=(math.pi / 8.0,),
            band_tolerances=(1.0e-3,),
            shell_cap=2,
        )
        result = BandEquivalenceLocalityResultConstructor().execute(request)
        changed_request = replace(request, evaluation_shift=0.25)
        changed_request_document = (
            serialization.BandEquivalenceLocalityRequestSerializer().execute(
                changed_request
            )
        )
        forged_document = (
            serialization.BandEquivalenceLocalityResultSerializer().execute(
                result.diagnostics,
                changed_request_document,
            )
        )

        with pytest.raises(ValueError, match="diagnostics do not belong"):
            application_api.BandEquivalenceLocalityResult(
                analysis_request=changed_request,
                diagnostics=result.diagnostics,
                request_document=changed_request_document,
                document=forged_document,
            )

    def test_verification_result__mixed_source_documents__fail_closed(self) -> None:
        request = definitions.BandEquivalenceLocalityRequest(
            family=definitions.BandEquivalenceLocalityFamily.SQUARE,
            cases=(self._square_directed(),),
            construction_size=4,
            evaluation_size=5,
            evaluation_shift=1.0 / 3.0,
            parent_scales=(1.0,),
            amplitudes=(math.pi / 8.0,),
            band_tolerances=(1.0e-3,),
            shell_cap=2,
        )
        result = BandEquivalenceLocalityResultConstructor().execute(request)
        verification_request = BandEquivalenceLocalityVerificationRequest(
            request, result
        )
        verification = BandEquivalenceLocalityResultVerifier().execute(
            verification_request
        )
        other_request = replace(request, evaluation_shift=0.25)
        other_result = BandEquivalenceLocalityResultConstructor().execute(other_request)
        forged_document = (
            serialization.BandEquivalenceLocalityVerificationSerializer().execute(
                verification.diagnostics,
                other_result.request_document,
                other_result.document,
            )
        )

        with pytest.raises(ValueError, match="does not belong"):
            application_api.BandEquivalenceLocalityVerificationResult(
                verification_request=verification_request,
                diagnostics=verification.diagnostics,
                input_document=other_result.request_document,
                result_document=other_result.document,
                document=forged_document,
            )

    def test_canonical_document__rejects_noncanonical_or_non_json_bytes(self) -> None:
        canonical = serialization.CanonicalJsonDocument(b'{"a":1,"b":2}\n')
        assert canonical.canonical_bytes() == b'{"a":1,"b":2}\n'

        invalid_documents = (
            b'{"b":2,"a":1}\n',
            b'{"a":1}\n\n',
            b'{"a":NaN}\n',
            b"[]\n",
            b"not-json\n",
            b"\xff\n",
        )
        for content in invalid_documents:
            with pytest.raises(ValueError, match="canonical JSON"):
                serialization.CanonicalJsonDocument(content)

    def test_public_api__contains_only_analysis_contracts(self) -> None:
        assert tuple(band_equivalence_locality.__all__) == (
            "BandEquivalenceLocalityCase",
            "BandEquivalenceLocalityDiagnostics",
            "BandEquivalenceLocalityFamily",
            "BandEquivalenceLocalityRefinementAssessment",
            "BandEquivalenceLocalityRequest",
            "BandEquivalenceLocalityVerificationDiagnostics",
            "GaugeNormalization",
            "ParentKind",
        )
        assert "BandEquivalenceLocalityResultConstructor" in application_api.__all__
        assert "BandEquivalenceLocalityResultVerifier" in application_api.__all__
        assert "BandEquivalenceLocalityRefinementAssessor" in application_api.__all__
        assert not hasattr(band_equivalence_locality, "canonical_json_bytes")
        assert not hasattr(band_equivalence_locality, "ConstrainedBesselTailDiagnostic")

    def test_module_ownership__separates_domain_action_records_and_wire_format(
        self,
    ) -> None:
        assert definitions.BandEquivalenceLocalityRequest.__module__.endswith(
            ".definitions"
        )
        assert calculation.BandEquivalenceLocalityCalculator.__module__.endswith(
            ".calculation"
        )
        assert records.BandEquivalenceLocalityDiagnostics.__module__.endswith(
            ".records"
        )
        assert (
            serialization.BandEquivalenceLocalityResultSerializer.__module__
            == "ksdft2effmass.campaigns.model_adequacy.band_equivalence_locality."
            "serialization"
        )
        assert (
            application_api.BandEquivalenceLocalityResultConstructor.__module__
            == "ksdft2effmass.application.band_equivalence_locality"
        )
        assert serialization.CanonicalJsonDocument.__module__.endswith(".serialization")
        assert schemas.BandEquivalenceLocalitySchema.__module__.endswith(".schemas")
        assert not hasattr(schemas, "band_equivalence_locality_refinement_schema")

    def test_schema__is_an_immutable_packaged_document_not_a_mapping(
        self, tmp_path: Path
    ) -> None:
        for family in definitions.BandEquivalenceLocalityFamily:
            for kind in schemas.BandEquivalenceLocalitySchemaKind:
                schema = schemas.BandEquivalenceLocalitySchema(family, kind)
                canonical = schema.canonical_bytes()

                assert canonical.startswith(b'{"$id":')
                assert canonical.endswith(b"\n")
                assert f'"$id":"{schema.identity}"'.encode() in canonical
                output = schema.write_to(tmp_path / family.name / kind.name)
                assert output.read_bytes() == canonical

    def test_square__monkhorst_pack_chain__reconstructs_and_verifies(self) -> None:
        definition = definitions.BandEquivalenceLocalityRequest(
            family=definitions.BandEquivalenceLocalityFamily.SQUARE,
            cases=(self._square_directed(),),
            construction_size=6,
            evaluation_size=7,
            evaluation_shift=1.0 / 3.0,
            parent_scales=(0.0, 1.0),
            amplitudes=(0.0, math.pi / 16.0, math.pi / 8.0),
            band_tolerances=(1.0e-3,),
            shell_cap=5,
        )

        result = BandEquivalenceLocalityResultConstructor().execute(definition)
        verification = BandEquivalenceLocalityResultVerifier().execute(
            BandEquivalenceLocalityVerificationRequest(definition, result)
        )

        assert result.diagnostics.status == "development-smoke-not-retained-evidence"
        assert verification.diagnostics.passes
        assert len(result.diagnostics.cases) == 1
        case = result.diagnostics.cases[0]
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
        assert all(
            point.transport_closure_and_plaquette_applicable for point in case.points
        )
        closure_defects = tuple(
            point.maximum_closure_holonomy_unitarity_defect for point in case.points
        )
        assert all(value is not None for value in closure_defects)
        assert max(value for value in closure_defects if value is not None) < 1.0e-12
        closure_phases = tuple(
            point.maximum_absolute_closure_holonomy_phases for point in case.points
        )
        assert all(value is not None for value in closure_phases)
        assert all(len(value) == 2 for value in closure_phases if value is not None)
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
        definition = definitions.BandEquivalenceLocalityRequest(
            family=definitions.BandEquivalenceLocalityFamily.SQUARE,
            cases=(self._square_directed(),),
            construction_size=16,
            evaluation_size=17,
            evaluation_shift=1.0 / 3.0,
            parent_scales=(0.0,),
            amplitudes=(amplitude,),
            band_tolerances=(1.0e-3,),
            shell_cap=5,
        )

        point = (
            BandEquivalenceLocalityResultConstructor()
            .execute(definition)
            .diagnostics.cases[0]
            .points[0]
        )
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

    def test_all_families__frame_isometry_and_periodicity__match_direct_reference(
        self,
    ) -> None:
        cases = (
            (
                definitions.BandEquivalenceLocalityFamily.SQUARE,
                self._square_directed(),
            ),
            (
                definitions.BandEquivalenceLocalityFamily.SIMPLE_CUBIC,
                self._simple_cubic_directed(),
            ),
            (
                definitions.BandEquivalenceLocalityFamily.GRAPHENE_INSPIRED,
                self._graphene(),
            ),
            (
                definitions.BandEquivalenceLocalityFamily.SILICON_INSPIRED,
                self._silicon(),
            ),
        )
        identity = np.eye(2, dtype=np.complex128)
        seed = np.eye(4, 2, dtype=np.complex128)

        for family, case in cases:
            definition = definitions.BandEquivalenceLocalityRequest(
                family=family,
                cases=(case,),
                construction_size=4,
                evaluation_size=5,
                evaluation_shift=1.0 / 3.0,
                parent_scales=(1.0,),
                amplitudes=(0.0,),
                band_tolerances=(1.0e-3,),
                shell_cap=2,
            )
            point = (
                BandEquivalenceLocalityResultConstructor()
                .execute(definition)
                .diagnostics.cases[0]
                .points[0]
            )
            coordinates = calculation._coordinates(  # noqa: SLF001
                definition.construction_size, definition.dimension, 0.5
            )

            def independent_frame(
                coordinate_grid: NDArray[np.float64],
                case_definition: definitions.BandEquivalenceLocalityCase = case,
            ) -> NDArray[np.complex128]:
                parent = calculation._parent_field(  # noqa: SLF001
                    case_definition, coordinate_grid, 1.0
                )
                eigenvectors = np.linalg.eigh(parent).eigenvectors[..., :, :2]
                projector = eigenvectors @ np.swapaxes(eigenvectors.conjugate(), -1, -2)
                projected_seed = projector @ seed
                gram = np.swapaxes(projected_seed.conjugate(), -1, -2) @ projected_seed
                values, vectors = np.linalg.eigh(gram)
                inverse_root = (
                    vectors * (1.0 / np.sqrt(values))[..., None, :]
                ) @ np.swapaxes(vectors.conjugate(), -1, -2)
                return projected_seed @ inverse_root

            frame = independent_frame(coordinates)
            expected_orthonormality = float(
                np.max(
                    np.linalg.norm(
                        np.swapaxes(frame.conjugate(), -1, -2) @ frame
                        - np.broadcast_to(identity, frame.shape[:-2] + (2, 2)),
                        axis=(-2, -1),
                    )
                )
            )
            expected_periodicity = 0.0
            for axis in range(definition.dimension):
                shifted = coordinates.copy()
                shifted[..., axis] += 1.0
                shifted_frame = independent_frame(shifted)
                shifted_defect = float(
                    np.max(np.linalg.norm(shifted_frame - frame, axis=(-2, -1)))
                )
                expected_periodicity = max(expected_periodicity, shifted_defect)

            assert point.maximum_frame_orthonormality_defect == pytest.approx(
                expected_orthonormality, abs=2.0e-15
            )
            assert point.maximum_periodic_frame_closure_defect == pytest.approx(
                expected_periodicity, abs=2.0e-15
            )

    def test_all_families__flat_alignment_correlation__matches_zero_mode(
        self,
    ) -> None:
        cases = (
            (
                definitions.BandEquivalenceLocalityFamily.SQUARE,
                self._square_directed(),
                12,
            ),
            (
                definitions.BandEquivalenceLocalityFamily.SIMPLE_CUBIC,
                self._simple_cubic_directed(),
                8,
            ),
            (
                definitions.BandEquivalenceLocalityFamily.GRAPHENE_INSPIRED,
                replace(
                    self._graphene(),
                    name="triangular-bravais-control",
                    parent_kind=definitions.ParentKind.HERMITIAN_BRAVAIS,
                    basis_offsets=(),
                ),
                12,
            ),
            (
                definitions.BandEquivalenceLocalityFamily.SILICON_INSPIRED,
                replace(
                    self._silicon(),
                    name="fcc-bravais-control",
                    parent_kind=definitions.ParentKind.HERMITIAN_BRAVAIS,
                    basis_offsets=(),
                ),
                8,
            ),
        )
        amplitude = math.pi / 16.0

        for family, case, construction_size in cases:
            definition = definitions.BandEquivalenceLocalityRequest(
                family=family,
                cases=(case,),
                construction_size=construction_size,
                evaluation_size=construction_size + 1,
                evaluation_shift=1.0 / 3.0,
                parent_scales=(0.0,),
                amplitudes=(amplitude,),
                band_tolerances=(1.0e-3,),
                shell_cap=2,
            )
            point = (
                BandEquivalenceLocalityResultConstructor()
                .execute(definition)
                .diagnostics.cases[0]
                .points[0]
            )

            assert point.analytic_flat_correlation is not None
            assert point.analytic_correlation_remainder_bound is not None
            assert point.correlation_quadrature_defect is not None
            assert point.finite_mesh_maximum_correlation == pytest.approx(
                point.analytic_flat_correlation,
                abs=point.analytic_correlation_remainder_bound + 5.0e-12,
            )
            if family is definitions.BandEquivalenceLocalityFamily.SQUARE:
                assert point.analytic_flat_correlation == pytest.approx(
                    float(j0(amplitude)) ** 2,
                    abs=2.0e-15,
                )
            elif family is definitions.BandEquivalenceLocalityFamily.SIMPLE_CUBIC:
                assert point.analytic_flat_correlation == pytest.approx(
                    float(j0(2.0 * amplitude / 3.0)) ** 3,
                    abs=2.0e-15,
                )

    def test_graphene_and_silicon__repeat_full_chain_with_basis_diagnostics(
        self,
    ) -> None:
        families = (
            definitions.BandEquivalenceLocalityRequest(
                family=definitions.BandEquivalenceLocalityFamily.GRAPHENE_INSPIRED,
                cases=(self._graphene(),),
                construction_size=4,
                evaluation_size=5,
                evaluation_shift=1.0 / 3.0,
                parent_scales=(1.0,),
                amplitudes=(math.pi / (8.0 * math.sqrt(6.0)),),
                band_tolerances=(1.0e-2,),
                shell_cap=2,
            ),
            definitions.BandEquivalenceLocalityRequest(
                family=definitions.BandEquivalenceLocalityFamily.SILICON_INSPIRED,
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
            result = BandEquivalenceLocalityResultConstructor().execute(definition)
            verification = BandEquivalenceLocalityResultVerifier().execute(
                BandEquivalenceLocalityVerificationRequest(definition, result)
            )
            point = result.diagnostics.cases[0].points[0]

            assert verification.diagnostics.passes
            assert point.continuous_external_gap_lower_bound == pytest.approx(1.84)
            assert point.minimum_sampled_external_gap >= 1.84
            assert point.basis_distance_minimum is not None
            assert point.basis_distance_maximum is not None
            assert point.maximum_direct_band_defect < 1.0e-12
            assert point.maximum_covariant_defect == 0.0

    def test_three_level_refinement__reports_changes_and_unresolved_tolerances(
        self,
    ) -> None:
        base = definitions.BandEquivalenceLocalityRequest(
            family=definitions.BandEquivalenceLocalityFamily.SQUARE,
            cases=(self._square_directed(),),
            construction_size=4,
            evaluation_size=9,
            evaluation_shift=1.0 / 3.0,
            parent_scales=(0.0, 1.0),
            amplitudes=(0.0, math.pi / 16.0, math.pi / 8.0),
            band_tolerances=(1.0e-3,),
            shell_cap=2,
        )
        refinement_definitions = (
            base,
            replace(base, construction_size=8, evaluation_size=17),
            replace(base, construction_size=16, evaluation_size=33),
        )
        results = tuple(
            BandEquivalenceLocalityResultConstructor().execute(item)
            for item in refinement_definitions
        )
        refinement_result = BandEquivalenceLocalityRefinementAssessor().execute(
            BandEquivalenceLocalityRefinementRequest(results=results)
        )
        serializer = serialization.BandEquivalenceLocalityRefinementSerializer()
        expected_document = serializer.execute(
            refinement_result.assessment,
            tuple(result.document for result in results),
        )

        assert refinement_result.document == expected_document
        schemas.BandEquivalenceLocalitySchema(
            definitions.BandEquivalenceLocalityFamily.SQUARE,
            schemas.BandEquivalenceLocalitySchemaKind.REFINEMENT_RESULT,
        ).validate(refinement_result.document.canonical_bytes())
        assessment = refinement_result.assessment
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
        assert all(
            item.maximum_shared_projector_defect is None
            for item in assessment.refinements
        )
        for pair, coarse, fine in zip(
            assessment.refinements,
            results[:-1],
            results[1:],
            strict=True,
        ):
            point_pairs = tuple(
                zip(
                    coarse.diagnostics.cases[0].points,
                    fine.diagnostics.cases[0].points,
                    strict=True,
                )
            )
            expected_correlation_change = max(
                abs(
                    left.finite_mesh_maximum_correlation
                    - right.finite_mesh_maximum_correlation
                )
                for left, right in point_pairs
                if left.finite_mesh_maximum_correlation is not None
                and right.finite_mesh_maximum_correlation is not None
            )
            expected_angle_change = max(
                abs(
                    (
                        left.restricted_global_rotation_angle
                        - right.restricted_global_rotation_angle
                        + 0.5 * math.pi
                    )
                    % math.pi
                    - 0.5 * math.pi
                )
                for left, right in point_pairs
                if left.restricted_global_rotation_angle is not None
                and right.restricted_global_rotation_angle is not None
            )
            expected_threshold_change = max(
                max(
                    abs(
                        left.minimum_operator_threshold
                        - right.minimum_operator_threshold
                    ),
                    abs(
                        left.exact_spectrum_joint_operator_threshold
                        - right.exact_spectrum_joint_operator_threshold
                    ),
                )
                for left, right in point_pairs
            )
            expected_hopping_weight_change = max(
                max(
                    abs(
                        left.reference_nononsite_power - right.reference_nononsite_power
                    ),
                    abs(
                        left.comparison_nononsite_power
                        - right.comparison_nononsite_power
                    ),
                )
                for left, right in point_pairs
            )
            block_power_changes: list[float] = []
            for left, right in point_pairs:
                right_shells = {
                    shell.shell_index: shell for shell in right.shell_diagnostics
                }
                for left_shell_diagnostic in left.shell_diagnostics:
                    right_shell_diagnostic = right_shells.get(
                        left_shell_diagnostic.shell_index
                    )
                    if right_shell_diagnostic is not None:
                        block_power_changes.extend(
                            (
                                abs(
                                    left_shell_diagnostic.reference_shell_power
                                    - right_shell_diagnostic.reference_shell_power
                                ),
                                abs(
                                    left_shell_diagnostic.comparison_shell_power
                                    - right_shell_diagnostic.comparison_shell_power
                                ),
                            )
                        )
            expected_invariant_change = max(
                max(
                    abs(
                        left.minimum_sampled_external_gap
                        - right.minimum_sampled_external_gap
                    ),
                    abs(
                        left.continuous_external_gap_lower_bound
                        - right.continuous_external_gap_lower_bound
                    ),
                    abs(left.minimum_seed_overlap - right.minimum_seed_overlap),
                )
                for left, right in point_pairs
            )
            parent_changes: list[float] = []
            for left, right in point_pairs:
                parent_changes.extend(
                    abs(left_value - right_value)
                    for left_value, right_value in zip(
                        (
                            left.minimum_sampled_external_gap,
                            left.continuous_external_gap_lower_bound,
                            left.minimum_seed_overlap,
                            left.maximum_parent_hermiticity_defect,
                            left.maximum_eigensystem_reconstruction_defect,
                            left.maximum_frame_orthonormality_defect,
                            left.maximum_projector_reconstruction_defect,
                            left.maximum_parent_retained_reconstruction_defect,
                            left.maximum_parent_fourier_reconstruction_defect,
                            left.maximum_periodic_frame_closure_defect,
                            left.minimum_sampled_transport_singular_value,
                            left.maximum_transport_procrustes_residual,
                            left.maximum_transport_squared_residual_roundoff_cutoff,
                            left.maximum_transport_unitarity_defect,
                            left.maximum_transport_rank_cutoff,
                            float(left.transport_rank_deficient_link_count),
                        ),
                        (
                            right.minimum_sampled_external_gap,
                            right.continuous_external_gap_lower_bound,
                            right.minimum_seed_overlap,
                            right.maximum_parent_hermiticity_defect,
                            right.maximum_eigensystem_reconstruction_defect,
                            right.maximum_frame_orthonormality_defect,
                            right.maximum_projector_reconstruction_defect,
                            right.maximum_parent_retained_reconstruction_defect,
                            right.maximum_parent_fourier_reconstruction_defect,
                            right.maximum_periodic_frame_closure_defect,
                            right.minimum_sampled_transport_singular_value,
                            right.maximum_transport_procrustes_residual,
                            right.maximum_transport_squared_residual_roundoff_cutoff,
                            right.maximum_transport_unitarity_defect,
                            right.maximum_transport_rank_cutoff,
                            float(right.transport_rank_deficient_link_count),
                        ),
                        strict=True,
                    )
                )
                if (
                    left.maximum_absolute_closure_holonomy_phases is not None
                    and right.maximum_absolute_closure_holonomy_phases is not None
                    and left.maximum_closure_holonomy_unitarity_defect is not None
                    and right.maximum_closure_holonomy_unitarity_defect is not None
                    and left.maximum_plaquette_holonomy_phase is not None
                    and right.maximum_plaquette_holonomy_phase is not None
                ):
                    parent_changes.extend(
                        abs(left_phase - right_phase)
                        for left_phase, right_phase in zip(
                            left.maximum_absolute_closure_holonomy_phases,
                            right.maximum_absolute_closure_holonomy_phases,
                            strict=True,
                        )
                    )
                    parent_changes.extend(
                        (
                            abs(
                                left.maximum_closure_holonomy_unitarity_defect
                                - right.maximum_closure_holonomy_unitarity_defect
                            ),
                            abs(
                                left.maximum_plaquette_holonomy_phase
                                - right.maximum_plaquette_holonomy_phase
                            ),
                        )
                    )
            decision_changes = []
            for left, right in point_pairs:
                for left_decision, right_decision in zip(
                    left.first_passing, right.first_passing, strict=True
                ):
                    for left_shell, right_shell in (
                        (
                            left_decision.reference_band_shell,
                            right_decision.reference_band_shell,
                        ),
                        (
                            left_decision.comparison_band_shell,
                            right_decision.comparison_band_shell,
                        ),
                        (
                            left_decision.reference_hamiltonian_shell,
                            right_decision.reference_hamiltonian_shell,
                        ),
                        (
                            left_decision.comparison_hamiltonian_shell,
                            right_decision.comparison_hamiltonian_shell,
                        ),
                    ):
                        if left_shell is not None and right_shell is not None:
                            decision_changes.append(abs(left_shell - right_shell))
            assert pair.maximum_correlation_change == expected_correlation_change
            assert pair.maximum_angle_change == expected_angle_change
            assert pair.maximum_threshold_change == expected_threshold_change
            assert pair.maximum_hopping_weight_change == expected_hopping_weight_change
            assert pair.maximum_hopping_block_power_change == max(block_power_changes)
            assert (
                pair.maximum_final_parent_invariant_change == expected_invariant_change
            )
            assert pair.maximum_parent_diagnostic_change == max(parent_changes)
            assert pair.maximum_final_outcome_change == (
                max(decision_changes) if decision_changes else None
            )

        finest_case = results[-1].diagnostics.cases[0]
        correlation_midpoint_defects = []
        joint_midpoint_defects = []
        hopping_midpoint_defects = []
        block_power_midpoint_defects = []
        for parent_scale in base.parent_scales:
            left, midpoint, right = tuple(
                point
                for point in finest_case.points
                if point.parent_scale == parent_scale
            )
            assert left.finite_mesh_maximum_correlation is not None
            assert midpoint.finite_mesh_maximum_correlation is not None
            assert right.finite_mesh_maximum_correlation is not None
            correlation_midpoint_defects.append(
                abs(
                    midpoint.finite_mesh_maximum_correlation
                    - 0.5
                    * (
                        left.finite_mesh_maximum_correlation
                        + right.finite_mesh_maximum_correlation
                    )
                )
            )
            joint_midpoint_defects.append(
                abs(
                    midpoint.exact_spectrum_joint_operator_threshold
                    - 0.5
                    * (
                        left.exact_spectrum_joint_operator_threshold
                        + right.exact_spectrum_joint_operator_threshold
                    )
                )
            )
            hopping_midpoint_defects.append(
                abs(
                    midpoint.comparison_nononsite_power
                    - 0.5
                    * (
                        left.comparison_nononsite_power
                        + right.comparison_nononsite_power
                    )
                )
            )
            for (
                left_shell_diagnostic,
                midpoint_shell_diagnostic,
                right_shell_diagnostic,
            ) in zip(
                left.shell_diagnostics,
                midpoint.shell_diagnostics,
                right.shell_diagnostics,
                strict=True,
            ):
                block_power_midpoint_defects.append(
                    abs(
                        midpoint_shell_diagnostic.comparison_shell_power
                        - 0.5
                        * (
                            left_shell_diagnostic.comparison_shell_power
                            + right_shell_diagnostic.comparison_shell_power
                        )
                    )
                )
        midpoint_diagnostic = finest_case.amplitude_midpoint
        observed_correlation_midpoint_defect = (
            midpoint_diagnostic.maximum_correlation_midpoint_defect
        )
        observed_joint_midpoint_defect = (
            midpoint_diagnostic.maximum_joint_threshold_midpoint_defect
        )
        observed_hopping_midpoint_defect = (
            midpoint_diagnostic.maximum_nonzero_hopping_weight_midpoint_defect
        )
        observed_block_midpoint_defect = (
            midpoint_diagnostic.maximum_hopping_block_power_midpoint_defect
        )
        assert observed_correlation_midpoint_defect == max(correlation_midpoint_defects)
        assert observed_joint_midpoint_defect == max(joint_midpoint_defects)
        assert observed_hopping_midpoint_defect == max(hopping_midpoint_defects)
        assert observed_block_midpoint_defect == max(block_power_midpoint_defects)

        for resolution in finest_case.flat_amplitude_resolution:
            nodes = np.linspace(
                0.0,
                base.amplitudes[-1],
                resolution.amplitude_nodes,
                dtype=np.float64,
            )
            midpoints = 0.5 * (nodes[:-1] + nodes[1:])
            node_correlations = j0(nodes) ** 2
            midpoint_correlations = j0(midpoints) ** 2
            node_joint = np.sqrt(2.0 * (1.0 - node_correlations))
            midpoint_joint = np.sqrt(2.0 * (1.0 - midpoint_correlations))
            expected_interpolation_defect = float(
                np.max(
                    np.abs(0.5 * (node_joint[:-1] + node_joint[1:]) - midpoint_joint)
                )
            )
            assert (
                resolution.maximum_joint_threshold_midpoint_interpolation_defect
                == pytest.approx(expected_interpolation_defect, abs=2.0e-15)
            )

        other_result = BandEquivalenceLocalityResultConstructor().execute(
            replace(base, evaluation_shift=0.25)
        )
        mixed_sources = (
            other_result.document,
            *(result.document for result in results[1:]),
        )
        forged_document = serializer.execute(assessment, mixed_sources)
        with pytest.raises(ValueError, match="do not belong"):
            application_api.BandEquivalenceLocalityRefinementResult(
                refinement_request=BandEquivalenceLocalityRefinementRequest(results),
                assessment=assessment,
                source_result_documents=mixed_sources,
                document=forged_document,
            )

    def test_documents__strict_family_schemas_and_hash_binding__reject_tampering(
        self,
    ) -> None:
        definition = definitions.BandEquivalenceLocalityRequest(
            family=definitions.BandEquivalenceLocalityFamily.SQUARE,
            cases=(self._square_directed(),),
            construction_size=4,
            evaluation_size=5,
            evaluation_shift=1.0 / 3.0,
            parent_scales=(1.0,),
            amplitudes=(math.pi / 8.0,),
            band_tolerances=(1.0e-3,),
            shell_cap=2,
        )
        result = BandEquivalenceLocalityResultConstructor().execute(definition)
        verification = BandEquivalenceLocalityResultVerifier().execute(
            BandEquivalenceLocalityVerificationRequest(definition, result)
        )
        result_serializer = serialization.BandEquivalenceLocalityResultSerializer()
        verification_serializer = (
            serialization.BandEquivalenceLocalityVerificationSerializer()
        )
        input_document = result.request_document
        result_document = result.document
        verification_document = verification.document
        assert result_document == result_serializer.execute(
            result.diagnostics,
            input_document,
        )
        assert verification_document == verification_serializer.execute(
            verification.diagnostics,
            input_document,
            result_document,
        )

        schemas.BandEquivalenceLocalitySchema(
            definition.family,
            schemas.BandEquivalenceLocalitySchemaKind.ANALYSIS_REQUEST,
        ).validate(input_document.canonical_bytes())
        schemas.BandEquivalenceLocalitySchema(
            definition.family,
            schemas.BandEquivalenceLocalitySchemaKind.ANALYSIS_RESULT,
        ).validate(result_document.canonical_bytes())
        schemas.BandEquivalenceLocalitySchema(
            definition.family,
            schemas.BandEquivalenceLocalitySchemaKind.VERIFICATION_RESULT,
        ).validate(verification_document.canonical_bytes())

        input_bytes = input_document.canonical_bytes()
        assert (
            b'"direct_lattice_primitive_basis_rows":[[1.0,0.0],[0.0,1.0]]'
            in input_bytes
        )
        assert b'"direct_lattice_primitive_vector_axis":"columns"' in input_bytes
        malformed_basis = input_bytes.replace(
            b"[[1.0,0.0],[0.0,1.0]]",
            b"[[1.0,0.0],[0.0,1.0],[0.0,0.0]]",
        )
        with pytest.raises(ValidationError):
            schemas.BandEquivalenceLocalitySchema(
                definition.family,
                schemas.BandEquivalenceLocalitySchemaKind.ANALYSIS_REQUEST,
            ).validate(malformed_basis)
        result_bytes = result_document.canonical_bytes()
        tampered_result = result_bytes[:-2] + b',"unexpected":"rejected"}\n'
        with pytest.raises(ValidationError):
            schemas.BandEquivalenceLocalitySchema(
                definition.family,
                schemas.BandEquivalenceLocalitySchemaKind.ANALYSIS_RESULT,
            ).validate(tampered_result)

    def test_definition__invalid_mesh_and_family_controls__fail_closed(self) -> None:
        with pytest.raises(ValueError, match="even"):
            definitions.BandEquivalenceLocalityRequest(
                family=definitions.BandEquivalenceLocalityFamily.SQUARE,
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
            definitions.BandEquivalenceLocalityRequest(
                family=definitions.BandEquivalenceLocalityFamily.SQUARE,
                cases=(self._square_directed(), self._silicon()),
                construction_size=4,
                evaluation_size=5,
                evaluation_shift=1.0 / 3.0,
                parent_scales=(1.0,),
                amplitudes=(0.0,),
                band_tolerances=(1.0e-3,),
                shell_cap=2,
            )

    def test_case__malformed_domain_vectors__fail_closed(self) -> None:
        case = self._square_directed()
        with pytest.raises(TypeError, match="positive_bonds"):
            replace(case, positive_bonds=((True, 0), (0, 1)))
        with pytest.raises(TypeError, match="basis_offsets"):
            replace(case, basis_offsets=((0, 0),))
        with pytest.raises(ValueError, match="dimension"):
            replace(
                case,
                direct_metric=DirectLatticeMetric(
                    DirectLattice3D(
                        a1=np.array((1.0, 0.0, 0.0), dtype=np.float64),
                        a2=np.array((0.0, 1.0, 0.0), dtype=np.float64),
                        a3=np.array((0.0, 0.0, 1.0), dtype=np.float64),
                    )
                ),
            )

    @staticmethod
    def _square_directed() -> definitions.BandEquivalenceLocalityCase:
        return definitions.BandEquivalenceLocalityCase(
            name="square-directed-parent",
            dimension=2,
            parent_kind=definitions.ParentKind.DIRECTED_AXIS,
            gauge_normalization=definitions.GaugeNormalization.AXIS_MAXIMUM,
            positive_bonds=((1, 0), (0, 1)),
            direct_metric=DirectLatticeMetric(
                DirectLattice2D(
                    a1=np.array((1.0, 0.0), dtype=np.float64),
                    a2=np.array((0.0, 1.0), dtype=np.float64),
                )
            ),
            shell_metric_scale=1.0,
        )

    @staticmethod
    def _simple_cubic_directed() -> definitions.BandEquivalenceLocalityCase:
        return definitions.BandEquivalenceLocalityCase(
            name="simple-cubic-directed-parent",
            dimension=3,
            parent_kind=definitions.ParentKind.DIRECTED_AXIS,
            gauge_normalization=definitions.GaugeNormalization.AXIS_MAXIMUM,
            positive_bonds=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            direct_metric=DirectLatticeMetric(
                DirectLattice3D(
                    a1=np.array((1.0, 0.0, 0.0), dtype=np.float64),
                    a2=np.array((0.0, 1.0, 0.0), dtype=np.float64),
                    a3=np.array((0.0, 0.0, 1.0), dtype=np.float64),
                )
            ),
            shell_metric_scale=1.0,
        )

    @staticmethod
    def _graphene() -> definitions.BandEquivalenceLocalityCase:
        return definitions.BandEquivalenceLocalityCase(
            name="graphene-inspired-honeycomb",
            dimension=2,
            parent_kind=definitions.ParentKind.BIPARTITE_INSPIRED,
            gauge_normalization=definitions.GaugeNormalization.BOND_RMS,
            positive_bonds=((1, 0), (0, 1), (1, -1)),
            direct_metric=DirectLatticeMetric(
                DirectLattice2D(
                    a1=np.array((1.0, 0.0), dtype=np.float64),
                    a2=np.array((0.5, math.sqrt(3.0) / 2.0), dtype=np.float64),
                )
            ),
            shell_metric_scale=1.0,
            basis_offsets=((0.0, 0.0), (1.0 / 3.0, 1.0 / 3.0)),
        )

    @staticmethod
    def _silicon() -> definitions.BandEquivalenceLocalityCase:
        return definitions.BandEquivalenceLocalityCase(
            name="silicon-inspired-diamond",
            dimension=3,
            parent_kind=definitions.ParentKind.BIPARTITE_INSPIRED,
            gauge_normalization=definitions.GaugeNormalization.BOND_RMS,
            positive_bonds=(
                (1, 0, 0),
                (0, 1, 0),
                (0, 0, 1),
                (-1, 1, 0),
                (-1, 0, 1),
                (0, -1, 1),
            ),
            direct_metric=DirectLatticeMetric(
                DirectLattice3D(
                    a1=np.array((0.0, 0.5, 0.5), dtype=np.float64),
                    a2=np.array((0.5, 0.0, 0.5), dtype=np.float64),
                    a3=np.array((0.5, 0.5, 0.0), dtype=np.float64),
                )
            ),
            shell_metric_scale=2.0,
            basis_offsets=(
                (0.0, 0.0, 0.0),
                (1.0 / 4.0, 1.0 / 4.0, 1.0 / 4.0),
            ),
        )
