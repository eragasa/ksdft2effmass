"""Integration tests for the complete higher-rank calculation producer."""

import json

import numpy as np
import pytest
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
from projectkoios.physkit.solidstate.tb import (
    FinitePeriodicMatrixFourierTensorEvaluator,
    FinitePeriodicMatrixFourierTransformer,
)

from ksdft2effmass.periodic1d.higher_rank_alignment import (
    Periodic1DHigherRankAlignmentAnalyzer,
    Periodic1DHigherRankAlignmentBackendExceptionCode,
    Periodic1DHigherRankAlignmentCalculationRequest,
    Periodic1DHigherRankAlignmentCalculationResult,
    Periodic1DHigherRankAlignmentChannel,
    Periodic1DHigherRankAlignmentStatus,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]


class TestPeriodic1DHigherRankAlignmentAnalyzer:
    """Establish owner composition, closed inventories, and request-bound bytes."""

    def test__analyzer__produces_complete_mesh_channel_support_inventories(
        self,
        higher_rank_calculation_result: Periodic1DHigherRankAlignmentCalculationResult,
    ) -> None:
        result = higher_rank_calculation_result

        assert result.global_selection.status.status is (
            Periodic1DHigherRankAlignmentStatus.QUALIFIED
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
        assert result.global_selection.maximum_objective_identity_defect < 1.0e-12
        assert len(result.meshes) == 3
        assert result.construction_evaluation_disjoint is True
        assert result.evaluation_noninfluence_confirmed is True
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
            assert tuple(channel.status.channel for channel in mesh.channels) == (
                Periodic1DHigherRankAlignmentChannel.IDENTITY,
                Periodic1DHigherRankAlignmentChannel.GLOBAL_UNITARY,
                Periodic1DHigherRankAlignmentChannel.POINTWISE_UNITARY,
                Periodic1DHigherRankAlignmentChannel.KNOWN_INVERSE_ORACLE,
            )
            for channel in mesh.channels:
                assert channel.status.status is (
                    Periodic1DHigherRankAlignmentStatus.QUALIFIED
                )
                assert tuple(item.maximum_range for item in channel.supports) == (
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
                    channel.coefficient_translations,
                    np.arange(-128, 129, dtype=np.int64),
                )
                assert (
                    channel.fourier_representative_count == mesh.construction_mesh_size
                )
                assert channel.fourier_representative_inventory_ordered_unique is True
                assert channel.fourier_inversion_closed is True
                assert channel.fourier_index_bijection_pass is True
                assert (
                    channel.no_nyquist_disposition
                    == "inapplicable-odd-centered-no-nyquist"
                )
                assert channel.frame_recovery is not None
                assert channel.represented_operator_recovery is not None
                if channel.status.channel in (
                    Periodic1DHigherRankAlignmentChannel.POINTWISE_UNITARY,
                    Periodic1DHigherRankAlignmentChannel.KNOWN_INVERSE_ORACLE,
                ):
                    assert channel.known_frame_recovery_pass is True
                    assert channel.known_operator_recovery_pass is True
                else:
                    assert channel.known_frame_recovery_pass is None
                    assert channel.known_operator_recovery_pass is None
                assert channel.reconstruction is not None
                assert channel.reconstruction_pass is True
                assert channel.interpolation is not None
                assert channel.final_interpolation_operator_pass is True
                assert channel.final_interpolation_spectrum_pass is True
                assert channel.parseval_pass is True
                assert channel.ordinary_hermiticity_pass is True
                assert channel.twisted_cyclic_hermiticity_pass is True
                assert channel.all_tail_monotonicity_checks_pass is True
                assert all(item.construction_parseval_pass for item in channel.supports)
                assert all(item.error_decomposition_pass for item in channel.supports)
                assert all(
                    item.truncation.all_perturbation_bounds_pass
                    and item.total.all_perturbation_bounds_pass
                    for item in channel.supports
                )
            assert mesh.channels[0].frame_recovery is not None
            assert mesh.channels[0].frame_recovery.normalized_frobenius_maximum > 0.0
            for recovered in mesh.channels[2:]:
                assert recovered.frame_recovery is not None
                assert recovered.frame_recovery.normalized_frobenius_maximum < 1.0e-12

    def test__analyzer__retains_separate_interpolation_truncation_and_total_errors(
        self,
        higher_rank_calculation_result: Periodic1DHigherRankAlignmentCalculationResult,
    ) -> None:
        final_mesh = higher_rank_calculation_result.meshes[-1]
        identity = final_mesh.channels[0]
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
        higher_rank_calculation_request: (
            Periodic1DHigherRankAlignmentCalculationRequest
        ),
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
        result = Periodic1DHigherRankAlignmentAnalyzer(
            request=higher_rank_calculation_request,
            procrustes_solver=NumpyBatchedComplexUnitaryProcrustesSolver(),
            transporter=ClosedLoopPolarFrameTransporter(),
            fourier_transformer=FinitePeriodicMatrixFourierTransformer(),
            fourier_evaluator=FinitePeriodicMatrixFourierTensorEvaluator(),
        ).execute()

        assert result.global_selection.status.status is (
            Periodic1DHigherRankAlignmentStatus.NUMERICALLY_UNRESOLVED
        )
        assert result.global_selection.status.backend_exception_code is (
            Periodic1DHigherRankAlignmentBackendExceptionCode.NONCONVERGENCE
        )
        assert result.global_selection.cross_singular_values.shape == (0, 3)
        assert result.global_selection.backend_identifier is None
        for mesh in result.meshes:
            assert mesh.pointwise_selection.status.status is (
                Periodic1DHigherRankAlignmentStatus.NUMERICALLY_UNRESOLVED
            )
            assert mesh.channels[1].reconstruction is None
            assert mesh.channels[2].reconstruction is None
        assert (
            Periodic1DHigherRankAlignmentCalculationResult.from_json(
                result.to_json()
            ).to_json()
            == result.to_json()
        )

    def test__analyzer__retains_bounded_transport_backend_failures(
        self,
        higher_rank_calculation_request: (
            Periodic1DHigherRankAlignmentCalculationRequest
        ),
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
        result = Periodic1DHigherRankAlignmentAnalyzer(
            request=higher_rank_calculation_request,
            procrustes_solver=NumpyBatchedComplexUnitaryProcrustesSolver(),
            transporter=ClosedLoopPolarFrameTransporter(),
            fourier_transformer=FinitePeriodicMatrixFourierTransformer(),
            fourier_evaluator=FinitePeriodicMatrixFourierTensorEvaluator(),
        ).execute()

        assert result.block_refinements == ()
        for mesh in result.meshes:
            assert mesh.transport is None
            assert mesh.transport_backend_failure is not None
            assert all(
                channel.status.status
                is Periodic1DHigherRankAlignmentStatus.NUMERICALLY_UNRESOLVED
                for channel in mesh.channels
            )
            assert all(channel.reconstruction is None for channel in mesh.channels)
        assert (
            Periodic1DHigherRankAlignmentCalculationResult.from_json(
                result.to_json()
            ).to_json()
            == result.to_json()
        )

    def test__calculation_result__round_trips_exact_bytes_and_rejects_request_tampering(
        self,
        higher_rank_calculation_result: Periodic1DHigherRankAlignmentCalculationResult,
    ) -> None:
        wire = higher_rank_calculation_result.to_json()
        reconstructed = Periodic1DHigherRankAlignmentCalculationResult.from_json(wire)

        assert reconstructed.to_json() == wire
        decoded = json.loads(wire)
        decoded["request"]["retained_rank"] = 4
        tampered = (json.dumps(decoded, indent=2, sort_keys=True) + "\n").encode()
        with pytest.raises(ValueError, match="global selection"):
            Periodic1DHigherRankAlignmentCalculationResult.from_json(tampered)

        gate_tampering = json.loads(wire)
        gate_tampering["meshes"]["items"][0]["channels"]["items"][0][
            "parseval_pass"
        ] = False
        tampered_gate = (
            json.dumps(gate_tampering, indent=2, sort_keys=True) + "\n"
        ).encode()
        with pytest.raises(ValueError, match="gate disposition"):
            Periodic1DHigherRankAlignmentCalculationResult.from_json(tampered_gate)
