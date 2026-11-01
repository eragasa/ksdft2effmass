"""Integration tests for the complete higher-rank calculation producer."""

import json
import math
from dataclasses import replace

import numpy as np
import pytest
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayConstructor
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesDefinition,
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.physkit.solidstate.electronic import (
    ClosedLoopPolarFrameTransportBackendFailure,
    ClosedLoopPolarFrameTransportBackendFailureReason,
    ClosedLoopPolarFrameTransportBackendOperation,
    ClosedLoopPolarFrameTransporter,
    FinitePeriodicMeshFrameInventory,
)

from ksdft2effmass.analysis.matrix_field.diagnostics import ScalarRefinementAnalyzer
from ksdft2effmass.gauge_alignment import (
    GaugeAlignmentActionConvention,
    GaugeAlignmentGroupFamily,
    GaugeAlignmentInnerProductConvention,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.composite import (
    Periodic1DRankNAlignmentAnalyzer,
    Periodic1DRankNAlignmentBackendExceptionCode,
    Periodic1DRankNAlignmentCalculationRequest,
    Periodic1DRankNAlignmentCalculationResult,
    Periodic1DRankNAlignmentStatus,
    Periodic1DRankNGaugeAlignment,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.composite.refinement import (
    Periodic1DRankNRefinementAnalysisRequest,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.model import (
    Periodic1DRankNAnalyticCaseConstructor,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment import (
    NyquistModeDispositionEnum,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment import (
    interpolation as gauge_interpolation,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.fields import (  # noqa: E501
    Periodic1DRankNGaugeAlignedFields,
    Periodic1DRankNGaugeAlignmentConstructionRequest,
    Periodic1DRankNGaugeAlignmentConstructor,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.fourier import (  # noqa: E501
    Periodic1DRankNFourierAnalysisRequest,
    Periodic1DRankNFourierAnalyzer,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.request import (  # noqa: E501
    Periodic1DRankNGaugeAlignmentAnalysisRequest,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPeriodic1DRankNAlignmentAnalyzer:
    """Establish owner composition, closed inventories, and request-bound bytes."""

    def test__analyzer__produces_complete_mesh_gauge_alignment_support_inventories(
        self,
        higher_rank_calculation_result: Periodic1DRankNAlignmentCalculationResult,
    ) -> None:
        result = higher_rank_calculation_result

        assert result.global_selection.status.status is (
            Periodic1DRankNAlignmentStatus.QUALIFIED
        )
        assert result.global_selection.selection_mesh_size == 2049
        assert result.global_selection.cross_singular_values.shape == (1, 3)
        assert result.global_selection.rank_margins.shape == (1,)
        assert result.global_selection.minimum_rank_margin == pytest.approx(
            result.global_selection.rank_margins[0]
        )
        assert len(result.global_selection.spectral_condition_numbers) == 1
        assert result.global_selection.spectral_condition_numbers[0] is not None
        assert result.global_selection.spectral_condition_numbers[0] >= 1.0
        assert result.global_selection.maximum_objective_identity_defect is not None
        assert result.global_selection.maximum_objective_identity_defect < 1.0e-12
        assert len(result.meshes) == 3
        provenance = result.evaluation_independence
        assert provenance.construction_evaluation_disjoint is True
        assert provenance.evaluation_mesh_excluded_from_selection is True
        assert provenance.global_selection_mesh_size == 2049
        assert provenance.pointwise_selection_mesh_sizes == (513, 1025, 2049)
        assert len(result.block_refinements) == 8
        assert all(item.all_pass for item in result.block_refinements)
        assert len(result.scalar_refinements) == 1360
        assert all(item.passes for item in result.scalar_refinements)
        for mesh in result.meshes:
            assert mesh.transport is not None
            assert mesh.transport_backend_failure is None
            assert mesh.model_diagnostics.exact_analytic_isolation_gap == 2.1
            assert mesh.model_diagnostics.sampled_isolation_gaps.shape == (3,)
            assert np.all(mesh.model_diagnostics.sampled_isolation_gaps >= 2.1)
            assert mesh.model_diagnostics.exact_analytic_attack_angle_maximum < 0.4025
            assert mesh.model_diagnostics.sampled_attack_angle_maxima.shape == (3,)
            assert np.all(
                mesh.model_diagnostics.sampled_attack_angle_maxima
                <= mesh.model_diagnostics.exact_analytic_attack_angle_maximum
            )
            assert mesh.model_diagnostics.gauge_unitarity_defect < 1.0e-12
            assert mesh.model_diagnostics.attacked_projector_equality_defect < 1.0e-12
            assert (
                mesh.pointwise_selection.maximum_objective_identity_defect is not None
            )
            assert mesh.pointwise_selection.maximum_objective_identity_defect < 1.0e-12
            assert mesh.pointwise_selection.rank_margins.shape == (
                mesh.construction_mesh_size,
            )
            assert mesh.pointwise_selection.deficient_point_indices == ()
            assert mesh.pointwise_selection.deficient_point_count == 0
            assert all(
                condition is not None
                for condition in mesh.pointwise_selection.spectral_condition_numbers
            )
            assert mesh.endpoint_closure_defect == pytest.approx(0.0, abs=1.0e-14)
            assert mesh.primitive_closure_defect == pytest.approx(0.0, abs=1.0e-14)
            assert tuple(
                gauge_alignment.status.gauge_alignment
                for gauge_alignment in mesh.gauge_alignment_results
            ) == (
                Periodic1DRankNGaugeAlignment.IDENTITY,
                Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY,
                Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY,
                Periodic1DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE,
            )
            for gauge_alignment in mesh.gauge_alignment_results:
                assert gauge_alignment.status.status is (
                    Periodic1DRankNAlignmentStatus.QUALIFIED
                )
                assert tuple(
                    item.maximum_range for item in gauge_alignment.supports
                ) == (
                    0,
                    1,
                    2,
                    4,
                    8,
                    16,
                    32,
                    64,
                    128,
                )
                np.testing.assert_array_equal(
                    gauge_alignment.coefficient_translations,
                    np.arange(-128, 129, dtype=np.int64),
                )
                assert (
                    gauge_alignment.fourier_representative_count
                    == mesh.construction_mesh_size
                )
                assert (
                    gauge_alignment.fourier_representative_inventory_ordered_unique
                    is True
                )
                assert gauge_alignment.fourier_inversion_closed is True
                assert gauge_alignment.fourier_index_bijection_pass is True
                assert gauge_alignment.nyquist_mode_disposition is (
                    NyquistModeDispositionEnum.ABSENT_ON_ODD_MESH
                )
                assert gauge_alignment.frame_recovery is not None
                assert gauge_alignment.represented_operator_recovery is not None
                if gauge_alignment.status.gauge_alignment in (
                    Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY,
                    Periodic1DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE,
                ):
                    assert gauge_alignment.known_frame_recovery_pass is True
                    assert gauge_alignment.known_operator_recovery_pass is True
                else:
                    assert gauge_alignment.known_frame_recovery_pass is None
                    assert gauge_alignment.known_operator_recovery_pass is None
                assert gauge_alignment.reconstruction is not None
                assert gauge_alignment.reconstruction_pass is True
                assert gauge_alignment.interpolation is not None
                assert gauge_alignment.final_interpolation_operator_pass is True
                assert gauge_alignment.final_interpolation_spectrum_pass is True
                assert gauge_alignment.parseval_pass is True
                assert gauge_alignment.ordinary_hermiticity_pass is True
                assert gauge_alignment.twisted_cyclic_hermiticity_pass is True
                assert gauge_alignment.all_tail_monotonicity_checks_pass is True
                alignment_wire = gauge_alignment.to_json()
                hopping_tails = gauge_alignment.hopping_locality_tails
                assert tuple(item.maximum_range for item in hopping_tails) == tuple(
                    item.maximum_range for item in gauge_alignment.supports
                )
                assert gauge_alignment.to_json() == alignment_wire
                for tail, item in zip(
                    hopping_tails,
                    gauge_alignment.supports,
                    strict=True,
                ):
                    assert tail.omitted_squared_frobenius_weight == (
                        item.omitted_squared_frobenius_weight
                    )
                    assert tail.normalized_omitted_block_l1_norm == (
                        item.normalized_omitted_block_l1_norm
                    )
                    assert all(
                        abs(value) > tail.maximum_range
                        for value in tail.omitted_translations
                    )
                    wire = item.to_json()
                    assert tuple(
                        displacement.components
                        for displacement in item.support_policy.displacements
                    ) == tuple(
                        (translation,) for translation in item.retained_translations
                    )
                    assert item.to_json() == wire
                assert all(
                    item.construction_parseval_pass for item in gauge_alignment.supports
                )
                assert all(
                    item.error_decomposition_pass for item in gauge_alignment.supports
                )
                assert all(
                    item.truncation.all_perturbation_bounds_pass
                    and item.total.all_perturbation_bounds_pass
                    for item in gauge_alignment.supports
                )
            assert mesh.gauge_alignment_results[0].frame_recovery is not None
            assert (
                mesh.gauge_alignment_results[
                    0
                ].frame_recovery.normalized_frobenius_maximum
                > 0.0
            )
            for recovered in mesh.gauge_alignment_results[2:]:
                assert recovered.frame_recovery is not None
                assert recovered.frame_recovery.normalized_frobenius_maximum < 1.0e-12

    def test__result_arrays__are_immutable_and_refinement_is_correlated(
        self,
        higher_rank_calculation_result: Periodic1DRankNAlignmentCalculationResult,
    ) -> None:
        block = higher_rank_calculation_result.block_refinements[0]

        with pytest.raises(ValueError):
            block.absolute_changes.setflags(write=True)
        with pytest.raises(TypeError, match="exact dtype int64"):
            replace(block, translations=block.translations.astype(np.float64))
        decoded = dict(block.to_dict())
        decoded["translations"] = block.translations.astype(np.float64)
        with pytest.raises(TypeError, match="exact dtype int64"):
            type(block).from_dict(decoded)
        with pytest.raises(ValueError, match="arithmetic is inconsistent"):
            replace(block, absolute_changes=np.full(block.absolute_changes.shape, -1.0))
        with pytest.raises(ValueError, match="disjointness provenance"):
            replace(
                higher_rank_calculation_result.evaluation_independence,
                construction_evaluation_disjoint=False,
            )

    def test__gauge_alignment_request__rejects_mismatched_model_and_mesh_coordinates(
        self,
        higher_rank_calculation_request: (Periodic1DRankNAlignmentCalculationRequest),
        higher_rank_calculation_result: Periodic1DRankNAlignmentCalculationResult,
    ) -> None:
        mesh = CenteredUniformMesh(1, 513, (0.0,))
        status = (
            higher_rank_calculation_result.meshes[0].gauge_alignment_results[0].status
        )
        samples = NumpyImmutableArrayConstructor(
            np.zeros((513, 3, 3), dtype=np.complex128),
            "samples",
            np.dtype(np.complex128),
        ).execute()
        frames = NumpyImmutableArrayConstructor(
            np.zeros((513, 6, 3), dtype=np.complex128),
            "frames",
            np.dtype(np.complex128),
        ).execute()
        matching_model = Periodic1DRankNAnalyticCaseConstructor(
            retained_rank=3,
            circuit_depth=1,
        ).execute()
        mismatched_model = Periodic1DRankNAnalyticCaseConstructor(
            retained_rank=3,
            circuit_depth=2,
        ).execute()
        coordinates = NumpyImmutableArrayConstructor(
            -0.5 + np.arange(513, dtype=np.float64) / 513,
            "coordinates",
            np.dtype(np.float64),
        ).execute()

        aligned_fields = Periodic1DRankNGaugeAlignedFields(
            case_identity=higher_rank_calculation_request.case_identity,
            gauge_alignment=status.gauge_alignment,
            coordinates=coordinates,
            represented_operators=samples,
            frames=frames,
        )
        with pytest.raises(ValueError, match="model rank and depth"):
            Periodic1DRankNGaugeAlignmentAnalysisRequest(
                calculation_request=higher_rank_calculation_request,
                model=mismatched_model,
                mesh=mesh,
                status=status,
                aligned_fields=aligned_fields,
                global_selection=higher_rank_calculation_result.global_selection,
            )
        mismatched_coordinates = NumpyImmutableArrayConstructor(
            np.zeros(513, dtype=np.float64),
            "coordinates",
            np.dtype(np.float64),
        ).execute()
        with pytest.raises(ValueError, match="declared construction mesh"):
            Periodic1DRankNGaugeAlignmentAnalysisRequest(
                calculation_request=higher_rank_calculation_request,
                model=matching_model,
                mesh=mesh,
                status=status,
                aligned_fields=Periodic1DRankNGaugeAlignedFields(
                    case_identity=higher_rank_calculation_request.case_identity,
                    gauge_alignment=status.gauge_alignment,
                    coordinates=mismatched_coordinates,
                    represented_operators=samples,
                    frames=frames,
                ),
                global_selection=higher_rank_calculation_result.global_selection,
            )
        with pytest.raises(ValueError, match="represented operators"):
            Periodic1DRankNGaugeAlignmentAnalysisRequest(
                calculation_request=higher_rank_calculation_request,
                model=matching_model,
                mesh=mesh,
                status=status,
                aligned_fields=aligned_fields,
                global_selection=higher_rank_calculation_result.global_selection,
            )

    def test__typed_stages__retain_immutable_arrays_and_exact_request_correlation(
        self,
        higher_rank_calculation_request: (Periodic1DRankNAlignmentCalculationRequest),
        higher_rank_calculation_result: Periodic1DRankNAlignmentCalculationResult,
    ) -> None:
        mesh = CenteredUniformMesh(1, 513, (0.0,))
        coordinates = NumpyImmutableArrayConstructor(
            -0.5 + np.arange(mesh.size, dtype=np.float64) / mesh.size,
            "coordinates",
            np.dtype(np.float64),
        ).execute()
        model = Periodic1DRankNAnalyticCaseConstructor(
            retained_rank=3,
            circuit_depth=1,
        ).execute()
        status = (
            higher_rank_calculation_result.meshes[0].gauge_alignment_results[0].status
        )
        fields = Periodic1DRankNGaugeAlignmentConstructor(
            Periodic1DRankNGaugeAlignmentConstructionRequest(
                calculation_request=higher_rank_calculation_request,
                model=model,
                gauge_alignment=status.gauge_alignment,
                coordinates=coordinates,
                global_selection=higher_rank_calculation_result.global_selection,
            )
        ).execute()
        analysis_request = Periodic1DRankNGaugeAlignmentAnalysisRequest(
            calculation_request=higher_rank_calculation_request,
            model=model,
            mesh=mesh,
            status=status,
            aligned_fields=fields,
            global_selection=higher_rank_calculation_result.global_selection,
        )
        fourier = Periodic1DRankNFourierAnalyzer(
            request=Periodic1DRankNFourierAnalysisRequest(analysis_request),
        ).execute()

        assert analysis_request.retained_rank == model.retained_rank
        assert analysis_request.gauge_group == "U(3)"
        assert analysis_request.alignment_sample_count == mesh.size
        assert (
            analysis_request.gauge_group_identity.family
            is GaugeAlignmentGroupFamily.UNITARY
        )
        assert (
            analysis_request.gauge_group_identity.represented_dimension
            == analysis_request.model.retained_rank
        )
        assert (
            analysis_request.action_convention
            is GaugeAlignmentActionConvention.RIGHT
        )
        assert (
            analysis_request.inner_product_convention
            is GaugeAlignmentInnerProductConvention.EUCLIDEAN
        )
        assert fourier.analysis_request is analysis_request
        assert not fourier.coefficient_translations.flags.writeable
        assert not fourier.block_raw_frobenius_norms.flags.writeable
        assert not fourier.block_normalized_frobenius_norms.flags.writeable
        with pytest.raises(ValueError, match="derive from the bound request"):
            gauge_interpolation.Periodic1DRankNInterpolationAnalysisRequest(
                analysis_request=replace(analysis_request),
                fourier_analysis=fourier,
            )

        interpolation = gauge_interpolation.Periodic1DRankNInterpolationAnalyzer(
            request=gauge_interpolation.Periodic1DRankNInterpolationAnalysisRequest(
                analysis_request=analysis_request,
                fourier_analysis=fourier,
            ),
        ).execute()

        assert interpolation.analysis_request is analysis_request
        assert not interpolation.evaluation_coordinates.flags.writeable
        assert not interpolation.full_evaluation.flags.writeable
        assert not interpolation.direct_evaluation.flags.writeable

    def test__result_admission__rejects_mismatched_model_and_gauge_alignment_evidence(
        self,
        higher_rank_calculation_result: Periodic1DRankNAlignmentCalculationResult,
    ) -> None:
        first_mesh = higher_rank_calculation_result.meshes[0]
        diagnostics = first_mesh.model_diagnostics
        q = (math.sqrt(41.0) - 3.0) / 8.0
        harmonic_maximum = math.sqrt(1.0 - q**2) * (0.75 + 0.5 * q)
        rank_four_angle = 0.35 * (1.0 + 0.15 * 2.0 / 3.0) * harmonic_maximum
        mismatched_diagnostics = replace(
            diagnostics,
            case_identity="r04-L01",
            retained_rank=4,
            exact_analytic_attack_angle_maximum=rank_four_angle,
        )
        mismatched_mesh = replace(
            first_mesh,
            model_diagnostics=mismatched_diagnostics,
        )
        with pytest.raises(ValueError, match="model diagnostics"):
            replace(
                higher_rank_calculation_result,
                meshes=(mismatched_mesh, *higher_rank_calculation_result.meshes[1:]),
            )

        first_channel = first_mesh.gauge_alignment_results[0]
        with pytest.raises(ValueError, match="block norm inventories"):
            replace(
                first_channel,
                block_normalized_frobenius_norms=-np.ones_like(
                    first_channel.block_normalized_frobenius_norms
                ),
            )

        first_refinement = higher_rank_calculation_result.block_refinements[0]
        translations = np.asarray(first_refinement.translations).copy()
        translations[0] += 1
        mismatched_refinement = replace(
            first_refinement,
            translations=translations,
        )
        with pytest.raises(ValueError, match="source alignments"):
            replace(
                higher_rank_calculation_result,
                block_refinements=(
                    mismatched_refinement,
                    *higher_rank_calculation_result.block_refinements[1:],
                ),
            )

        scalar_index, source_scalar = next(
            (index, item)
            for index, item in enumerate(
                higher_rank_calculation_result.scalar_refinements
            )
            if item.coarse_value != 0.0 or item.fine_value != 0.0
        )
        mismatched_scalar = replace(
            source_scalar,
            coarse_value=0.0,
            fine_value=0.0,
            absolute_change=0.0,
            relative_change=0.0,
            applied_tolerance=1.0e-10,
            signed_margin=1.0e-10,
            passes=True,
        )
        scalar_refinements = list(higher_rank_calculation_result.scalar_refinements)
        scalar_refinements[scalar_index] = mismatched_scalar
        with pytest.raises(ValueError, match="source alignments"):
            replace(
                higher_rank_calculation_result,
                scalar_refinements=tuple(scalar_refinements),
            )

    def test__refinement_request__rejects_mismatched_case_status(
        self,
        higher_rank_calculation_request: (Periodic1DRankNAlignmentCalculationRequest),
        higher_rank_calculation_result: Periodic1DRankNAlignmentCalculationResult,
    ) -> None:
        first_mesh = higher_rank_calculation_result.meshes[0]
        first_channel = first_mesh.gauge_alignment_results[0]
        mismatched_status = replace(
            first_channel.status,
            case_identity="r03-L02",
            circuit_depth=2,
        )
        mismatched_channel = replace(first_channel, status=mismatched_status)
        mismatched_mesh = replace(
            first_mesh,
            gauge_alignment_results=(mismatched_channel,)
            + first_mesh.gauge_alignment_results[1:],
        )

        with pytest.raises(ValueError, match="statuses must match"):
            Periodic1DRankNRefinementAnalysisRequest(
                calculation_request=higher_rank_calculation_request,
                meshes=(mismatched_mesh,) + higher_rank_calculation_result.meshes[1:],
            )

    def test__analyzer__retains_separate_interpolation_truncation_and_total_errors(
        self,
        higher_rank_calculation_result: Periodic1DRankNAlignmentCalculationResult,
    ) -> None:
        final_mesh = higher_rank_calculation_result.meshes[-1]
        identity = final_mesh.gauge_alignment_results[0]
        assert identity.retained_rank == identity.status.retained_rank
        assert identity.gauge_group == f"U({identity.status.retained_rank})"
        assert (
            identity.alignment_sample_count
            == identity.status.construction_mesh_size
        )
        assert identity.interpolation is not None
        smallest_support = identity.supports[0]

        assert (
            identity.interpolation.errors.normalized_matrix_frobenius_maximum < 1.0e-12
        )
        assert (
            smallest_support.truncation.errors.normalized_matrix_frobenius_maximum > 0.0
        )
        assert smallest_support.total.errors.normalized_matrix_frobenius_maximum > 0.0
        assert smallest_support.normalized_error_decomposition_defect < 2.0e-11
        assert smallest_support.construction_parseval_relative_defect < 2.0e-11

    def test__analyzer__retains_bounded_procrustes_backend_failures(
        self,
        higher_rank_calculation_request: (Periodic1DRankNAlignmentCalculationRequest),
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        def fail_svd(
            solver: NumpyBatchedComplexUnitaryProcrustesSolver,
            definition: NumpyBatchedComplexUnitaryProcrustesDefinition,
        ) -> None:
            del solver, definition
            raise np.linalg.LinAlgError("synthetic backend failure")

        monkeypatch.setattr(
            NumpyBatchedComplexUnitaryProcrustesSolver,
            "solve",
            fail_svd,
        )
        result = Periodic1DRankNAlignmentAnalyzer(
            request=higher_rank_calculation_request,
            procrustes_solver=NumpyBatchedComplexUnitaryProcrustesSolver(),
            transporter=ClosedLoopPolarFrameTransporter(),
            scalar_refinement_analyzer=ScalarRefinementAnalyzer(),
        ).execute()

        assert result.global_selection.status.status is (
            Periodic1DRankNAlignmentStatus.NUMERICALLY_UNRESOLVED
        )
        assert result.global_selection.status.backend_exception_code is (
            Periodic1DRankNAlignmentBackendExceptionCode.NONCONVERGENCE
        )
        assert result.global_selection.cross_singular_values.shape == (0, 3)
        assert result.global_selection.backend_identifier is None
        for mesh in result.meshes:
            assert mesh.pointwise_selection.status.status is (
                Periodic1DRankNAlignmentStatus.NUMERICALLY_UNRESOLVED
            )
            assert mesh.gauge_alignment_results[1].reconstruction is None
            assert mesh.gauge_alignment_results[2].reconstruction is None
        assert (
            Periodic1DRankNAlignmentCalculationResult.from_json(
                result.to_json()
            ).to_json()
            == result.to_json()
        )

    def test__analyzer__retains_bounded_transport_backend_failures(
        self,
        higher_rank_calculation_request: (Periodic1DRankNAlignmentCalculationRequest),
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        def fail_transport(
            transporter: ClosedLoopPolarFrameTransporter,
            source: FinitePeriodicMeshFrameInventory,
        ) -> None:
            del transporter, source
            raise ClosedLoopPolarFrameTransportBackendFailure(
                operation=(
                    ClosedLoopPolarFrameTransportBackendOperation.PROCRUSTES_SVD
                ),
                reason=ClosedLoopPolarFrameTransportBackendFailureReason.NONCONVERGENCE,
                link_index=0,
            )

        monkeypatch.setattr(
            ClosedLoopPolarFrameTransporter,
            "transport",
            fail_transport,
        )
        result = Periodic1DRankNAlignmentAnalyzer(
            request=higher_rank_calculation_request,
            procrustes_solver=NumpyBatchedComplexUnitaryProcrustesSolver(),
            transporter=ClosedLoopPolarFrameTransporter(),
            scalar_refinement_analyzer=ScalarRefinementAnalyzer(),
        ).execute()

        assert result.block_refinements == ()
        for mesh in result.meshes:
            assert mesh.transport is None
            assert mesh.transport_backend_failure is not None
            assert all(
                gauge_alignment.status.status
                is Periodic1DRankNAlignmentStatus.NUMERICALLY_UNRESOLVED
                for gauge_alignment in mesh.gauge_alignment_results
            )
            assert all(
                gauge_alignment.reconstruction is None
                for gauge_alignment in mesh.gauge_alignment_results
            )
        assert (
            Periodic1DRankNAlignmentCalculationResult.from_json(
                result.to_json()
            ).to_json()
            == result.to_json()
        )
        first_failure = result.meshes[0].transport_backend_failure
        assert first_failure is not None
        mismatched_failure = replace(
            first_failure,
            case_identity="r03-L02",
            circuit_depth=2,
        )
        mismatched_mesh = replace(
            result.meshes[0],
            transport_backend_failure=mismatched_failure,
        )
        with pytest.raises(ValueError, match="backend failure"):
            replace(result, meshes=(mismatched_mesh, *result.meshes[1:]))

    def test__calculation_result__round_trips_exact_bytes_and_rejects_request_tampering(
        self,
        higher_rank_calculation_result: Periodic1DRankNAlignmentCalculationResult,
    ) -> None:
        wire = higher_rank_calculation_result.to_json()
        reconstructed = Periodic1DRankNAlignmentCalculationResult.from_json(wire)

        assert reconstructed.to_json() == wire
        assert b'"nyquist_mode_disposition": "absent-on-odd-mesh"' in wire
        decoded = json.loads(wire)
        first_alignment = decoded["meshes"]["items"][0]["gauge_alignment_results"][
            "items"
        ][0]
        assert first_alignment["nyquist_mode_disposition"] == "absent-on-odd-mesh"
        assert "no_nyquist_disposition" not in first_alignment

        old_nyquist = json.loads(wire)
        old_nyquist["meshes"]["items"][0]["gauge_alignment_results"]["items"][0][
            "nyquist_mode_disposition"
        ] = "inapplicable-odd-centered-no-nyquist"
        old_nyquist_wire = (
            json.dumps(old_nyquist, indent=2, sort_keys=True) + "\n"
        ).encode()
        with pytest.raises(ValueError, match="unsupported NyquistModeDispositionEnum"):
            Periodic1DRankNAlignmentCalculationResult.from_json(old_nyquist_wire)

        decoded["request"]["retained_rank"] = 4
        tampered = (json.dumps(decoded, indent=2, sort_keys=True) + "\n").encode()
        with pytest.raises(ValueError, match="global selection"):
            Periodic1DRankNAlignmentCalculationResult.from_json(tampered)

        gate_tampering = json.loads(wire)
        gate_tampering["meshes"]["items"][0]["gauge_alignment_results"]["items"][0][
            "parseval_pass"
        ] = False
        tampered_gate = (
            json.dumps(gate_tampering, indent=2, sort_keys=True) + "\n"
        ).encode()
        with pytest.raises(ValueError, match="gate disposition"):
            Periodic1DRankNAlignmentCalculationResult.from_json(tampered_gate)
