"""Tests for higher-rank alignment status and owner-transport records."""

import json
from dataclasses import replace

import numpy as np
import pytest
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh
from projectkoios.optimization.alignment.closed_loop_polar_transport import (
    ClosedLoopPolarFrameTransportBackendFailure,
    ClosedLoopPolarFrameTransportBackendFailureReason,
    ClosedLoopPolarFrameTransportBackendOperation,
    ClosedLoopPolarFrameTransportLinkStatus,
    ClosedLoopPolarFrameTransportStatus,
)
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesRankCutoffRule,
    ComplexUnitaryProcrustesTolerance,
)
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopFrameTransportOutcome,
    ClosedLoopPolarFrameTransporter,
    ClosedLoopPolarFrameTransportPrincipalPhaseBranch,
    EndpointSewingAction,
    FinitePeriodicMeshFrameInventory,
    FrameRotationAction,
    OrderedReducedPointFrameInventory,
)
from projectkoios.physkit.units import ComplexMatrixQuantity, Unitless

from ksdft2effmass.periodic1d.rankN.band_alignment.composite import (
    Periodic1DRankNAlignmentBackendExceptionCode,
    Periodic1DRankNAlignmentConfiguration,
    Periodic1DRankNAlignmentStatus,
    Periodic1DRankNAlignmentStatusResult,
    Periodic1DRankNAlignmentTransportBackendFailureResult,
    Periodic1DRankNAlignmentTransportOwnerResult,
    Periodic1DRankNAlignmentTransportRequest,
    Periodic1DRankNBlockRefinementResult,
    Periodic1DRankNGaugeAlignment,
    Periodic1DRankNGlobalUnitaryDownstreamApplicability,
)

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]


def _configuration() -> Periodic1DRankNAlignmentConfiguration:
    return Periodic1DRankNAlignmentConfiguration(
        family_identity=Periodic1DRankNAlignmentConfiguration.FAMILY_IDENTITY,
        version_identity=Periodic1DRankNAlignmentConfiguration.VERSION_IDENTITY,
        retained_ranks=(3, 4, 8, 16),
        circuit_depths=(1, 2, 4, 8),
        construction_mesh_sizes=(513, 1025, 2049),
        final_construction_mesh_size=2049,
        global_unitary_selection_mesh_size=2049,
        evaluation_mesh_size=8191,
        evaluation_shift_numerator=1,
        evaluation_shift_denominator=2,
        gauge_alignments=(
            Periodic1DRankNGaugeAlignment.IDENTITY,
            Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY,
            Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY,
            Periodic1DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE,
        ),
        frame_rotation_action=FrameRotationAction.RIGHT,
        endpoint_sewing_action=EndpointSewingAction.LEFT_AMBIENT,
        principal_phase_branch=(
            ClosedLoopPolarFrameTransportPrincipalPhaseBranch.negative_pi_open
        ),
        rank_cutoff_rule=ComplexUnitaryProcrustesRankCutoffRule.MAXIMUM,
        rank_absolute_tolerance=1.0e-12,
        rank_relative_tolerance=1.0e-10,
        backend_validation_absolute_tolerance=1.0e-12,
        backend_validation_relative_tolerance=1.0e-10,
        endpoint_and_primitive_closure_tolerance=1.0e-11,
        maximum_closure_phase_tolerance=1.0e-10,
    )


def _transport_request(
    *,
    retained_rank: int = 3,
    circuit_depth: int = 1,
    construction_mesh_size: int = 513,
    ambient_basis_identifier: str = "ordered-six-state-ambient-basis",
    retained_frame_identifier: str | None = None,
    endpoint_sewing_identifier: str = "periodic-reciprocal-endpoint-sewing",
) -> Periodic1DRankNAlignmentTransportRequest:
    selected_frame_identifier = (
        f"r{retained_rank:02d}-L{circuit_depth:02d}-retained-frame"
        if retained_frame_identifier is None
        else retained_frame_identifier
    )
    return Periodic1DRankNAlignmentTransportRequest(
        configuration=_configuration(),
        retained_rank=retained_rank,
        circuit_depth=circuit_depth,
        construction_mesh_size=construction_mesh_size,
        ambient_basis_identifier=ambient_basis_identifier,
        retained_frame_identifier=selected_frame_identifier,
        endpoint_sewing_identifier=endpoint_sewing_identifier,
    )


def _owner_tolerance() -> ComplexUnitaryProcrustesTolerance:
    return ComplexUnitaryProcrustesTolerance(
        rank_absolute=1.0e-12,
        rank_relative=1.0e-10,
        validation_absolute=1.0e-12,
        validation_relative=1.0e-10,
        rank_cutoff_rule=ComplexUnitaryProcrustesRankCutoffRule.MAXIMUM,
    )


def _owner_outcome(
    *,
    rank_deficient: bool,
    mesh_offset: float = 0.0,
    ambient_basis_identifier: str = "ordered-six-state-ambient-basis",
    retained_frame_identifier: str = "r03-L01-retained-frame",
    endpoint_sewing_identifier: str = "periodic-reciprocal-endpoint-sewing",
) -> ClosedLoopFrameTransportOutcome:
    mesh = CenteredUniformMesh(1, 513, (mesh_offset,))
    frames = np.zeros((mesh.point_count, 6, 3), dtype=np.complex128)
    frames[:, :3, :] = np.eye(3, dtype=np.complex128)
    if rank_deficient:
        frames[1:, :, :] = 0.0
        frames[1:, 3:, :] = np.eye(3, dtype=np.complex128)
    inventory = FinitePeriodicMeshFrameInventory.from_arrays(
        mesh=mesh,
        frames=frames,
        endpoint_sewing_map=np.eye(6, dtype=np.complex128),
        ambient_basis_identifier=ambient_basis_identifier,
        retained_frame_identifier=retained_frame_identifier,
        endpoint_sewing_identifier=endpoint_sewing_identifier,
        principal_phase_branch=(
            ClosedLoopPolarFrameTransportPrincipalPhaseBranch.negative_pi_open
        ),
        tolerance=_owner_tolerance(),
    )
    return ClosedLoopPolarFrameTransporter().transport(inventory)


class TestPeriodic1DRankNAlignmentTransportOwnerResult:
    """Establish exact dispositions and typed adaptation of PhysKit outcomes."""

    def test__transport_request__round_trips_exact_configuration_and_identities(
        self,
    ) -> None:
        request = _transport_request()

        reconstructed = Periodic1DRankNAlignmentTransportRequest.from_json(
            request.to_json()
        )

        assert reconstructed == request
        assert reconstructed.case_identity == "r03-L01"
        assert reconstructed.ambient_dimension == 6
        assert reconstructed.to_json() == request.to_json()

    def test__transport_request__rejects_boolean_rank_and_empty_identity(self) -> None:
        request = _transport_request()

        with pytest.raises(TypeError, match="built-in integer"):
            replace(request, retained_rank=True)
        with pytest.raises(ValueError, match="must be nonempty"):
            replace(request, endpoint_sewing_identifier="")

    def test__array_backed_records__do_not_generate_numpy_equality(self) -> None:
        coarse = np.asarray([1.0, 2.0], dtype=np.float64)
        zeros = np.zeros(2, dtype=np.float64)
        tolerances = 1.0e-10 + 1.0e-6 * coarse
        result = Periodic1DRankNBlockRefinementResult(
            gauge_alignment=Periodic1DRankNGaugeAlignment.IDENTITY,
            coarse_mesh_size=513,
            fine_mesh_size=1025,
            translations=np.asarray([0, 1], dtype=np.int64),
            coarse_normalized_block_norms=coarse,
            fine_normalized_block_norms=coarse,
            absolute_changes=zeros,
            relative_changes=zeros,
            applied_tolerances=tolerances,
            signed_margins=tolerances,
            all_pass=True,
        )

        reconstructed = Periodic1DRankNBlockRefinementResult.from_json(result.to_json())

        assert reconstructed is not result
        assert (reconstructed == result) is False
        assert reconstructed.to_json() == result.to_json()

    def test__status_result__round_trips_qualified_global_unitary(self) -> None:
        result = Periodic1DRankNAlignmentStatusResult(
            case_identity="r03-L01",
            retained_rank=3,
            circuit_depth=1,
            construction_mesh_size=513,
            gauge_alignment=Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY,
            status=Periodic1DRankNAlignmentStatus.QUALIFIED,
            global_unitary_downstream_applicability=(
                Periodic1DRankNGlobalUnitaryDownstreamApplicability.APPLICABLE
            ),
            backend_exception_code=None,
        )

        reconstructed = Periodic1DRankNAlignmentStatusResult.from_json(result.to_json())

        assert reconstructed == result
        assert reconstructed.to_json() == result.to_json()

        old_key = json.loads(result.to_json())
        old_key["channel"] = old_key.pop("gauge_alignment")
        old_key_wire = (json.dumps(old_key, indent=2, sort_keys=True) + "\n").encode()
        with pytest.raises(ValueError, match="status fields do not match"):
            Periodic1DRankNAlignmentStatusResult.from_json(old_key_wire)

    def test__status_result__retains_failure_code_without_exception_text(self) -> None:
        result = Periodic1DRankNAlignmentStatusResult(
            case_identity="r04-L02",
            retained_rank=4,
            circuit_depth=2,
            construction_mesh_size=1025,
            gauge_alignment=Periodic1DRankNGaugeAlignment.POINTWISE_UNITARY,
            status=Periodic1DRankNAlignmentStatus.NUMERICALLY_UNRESOLVED,
            global_unitary_downstream_applicability=None,
            backend_exception_code=(
                Periodic1DRankNAlignmentBackendExceptionCode.NONCONVERGENCE
            ),
        )

        wire = result.to_json()

        assert Periodic1DRankNAlignmentStatusResult.from_json(wire) == result
        assert b"backend-nonconvergence" in wire
        assert b"exception_text" not in wire

    def test__status_result__rejects_gauge_alignment_and_applicability_mismatch(
        self,
    ) -> None:
        valid = Periodic1DRankNAlignmentStatusResult(
            case_identity="r03-L01",
            retained_rank=3,
            circuit_depth=1,
            construction_mesh_size=513,
            gauge_alignment=Periodic1DRankNGaugeAlignment.GLOBAL_UNITARY,
            status=Periodic1DRankNAlignmentStatus.AGGREGATE_RANK_DEFICIENT,
            global_unitary_downstream_applicability=(
                Periodic1DRankNGlobalUnitaryDownstreamApplicability.INAPPLICABLE_AGGREGATE_RANK_DEFICIENT
            ),
            backend_exception_code=None,
        )

        with pytest.raises(ValueError, match="disagree"):
            replace(
                valid,
                global_unitary_downstream_applicability=(
                    Periodic1DRankNGlobalUnitaryDownstreamApplicability.APPLICABLE
                ),
            )
        with pytest.raises(ValueError, match="not admissible"):
            replace(
                valid,
                gauge_alignment=Periodic1DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE,
            )
        with pytest.raises(ValueError, match="not in the frozen inventory"):
            replace(valid, construction_mesh_size=512)

    def test__transport_failure_result__preserves_typed_owner_failure(self) -> None:
        failure = ClosedLoopPolarFrameTransportBackendFailure(
            ClosedLoopPolarFrameTransportBackendOperation.CLOSURE_SCHUR,
            ClosedLoopPolarFrameTransportBackendFailureReason.NONCONVERGENCE,
            512,
        )

        result_type = Periodic1DRankNAlignmentTransportBackendFailureResult
        result = result_type.from_owner_failure(
            case_identity="r03-L01",
            retained_rank=3,
            circuit_depth=1,
            construction_mesh_size=513,
            failure=failure,
        )
        wire = result.to_json()

        assert result.operation is (
            ClosedLoopPolarFrameTransportBackendOperation.CLOSURE_SCHUR
        )
        assert result.reason is (
            ClosedLoopPolarFrameTransportBackendFailureReason.NONCONVERGENCE
        )
        assert result.backend_exception_code is (
            Periodic1DRankNAlignmentBackendExceptionCode.NONCONVERGENCE
        )
        assert (
            Periodic1DRankNAlignmentTransportBackendFailureResult.from_json(wire)
            == result
        )
        assert b"backend failed" not in wire

        with pytest.raises(ValueError, match="outside the selected closed route"):
            replace(result, link_index=513)
        with pytest.raises(ValueError, match="must identify the closure link"):
            replace(result, link_index=0)
        with pytest.raises(ValueError, match="exception code disagree"):
            replace(
                result,
                backend_exception_code=(
                    Periodic1DRankNAlignmentBackendExceptionCode.ARITHMETIC_NONFINITE
                ),
            )

    def test__transport_owner_result__consumes_and_round_trips_qualified_outcome(
        self,
    ) -> None:
        outcome = _owner_outcome(rank_deficient=False)

        result = Periodic1DRankNAlignmentTransportOwnerResult.from_owner_outcome(
            request=_transport_request(),
            outcome=outcome,
        )
        reconstructed = Periodic1DRankNAlignmentTransportOwnerResult.from_json(
            result.to_json()
        )

        assert result.request == _transport_request()
        assert reconstructed.request == result.request
        assert result.status is ClosedLoopPolarFrameTransportStatus.QUALIFIED
        assert len(result.link_results) == 513
        assert result.deficient_link_indices == ()
        assert result.unattempted_link_indices == ()
        assert result.ordered_closure_endpoint_mismatch_phases == (0.0, 0.0, 0.0)
        assert result.primitive_last_to_sewn_first_right_unitary is not None
        assert result.sewn_first_to_primitive_last_right_unitary is not None
        assert result.distributed_closure_correction_right_unitary_step is not None
        assert reconstructed.primitive_last_to_sewn_first_right_unitary is not None
        assert reconstructed.sewn_first_to_primitive_last_right_unitary is not None
        assert (
            reconstructed.distributed_closure_correction_right_unitary_step is not None
        )
        np.testing.assert_allclose(
            result.sewn_first_to_primitive_last_right_unitary.magnitude,
            result.primitive_last_to_sewn_first_right_unitary.magnitude.conjugate().T,
            atol=0.0,
        )
        np.testing.assert_allclose(
            np.linalg.matrix_power(
                result.distributed_closure_correction_right_unitary_step.magnitude,
                513,
            ),
            result.primitive_last_to_sewn_first_right_unitary.magnitude,
            atol=1.0e-14,
        )
        np.testing.assert_array_equal(
            reconstructed.primitive_last_to_sewn_first_right_unitary.magnitude,
            result.primitive_last_to_sewn_first_right_unitary.magnitude,
        )
        np.testing.assert_array_equal(
            reconstructed.sewn_first_to_primitive_last_right_unitary.magnitude,
            result.sewn_first_to_primitive_last_right_unitary.magnitude,
        )
        np.testing.assert_array_equal(
            reconstructed.distributed_closure_correction_right_unitary_step.magnitude,
            result.distributed_closure_correction_right_unitary_step.magnitude,
        )
        assert reconstructed.to_json() == result.to_json()
        with pytest.raises(ValueError, match="read-only"):
            result.primitive_last_to_sewn_first_right_unitary.magnitude[0, 0] = 0.0

    def test__transport_owner_result__preserves_deficient_progression(self) -> None:
        outcome = _owner_outcome(rank_deficient=True)

        result = Periodic1DRankNAlignmentTransportOwnerResult.from_owner_outcome(
            request=_transport_request(),
            outcome=outcome,
        )

        assert result.status is ClosedLoopPolarFrameTransportStatus.RANK_DEFICIENT
        assert result.deficient_link_indices == (0,)
        assert result.unattempted_link_indices == tuple(range(1, 513))
        assert result.link_results[0].status is (
            ClosedLoopPolarFrameTransportLinkStatus.RANK_DEFICIENT
        )
        assert all(
            link.status is ClosedLoopPolarFrameTransportLinkStatus.UNATTEMPTED
            for link in result.link_results[1:]
        )
        assert result.ordered_closure_endpoint_mismatch_phases is None
        assert result.primitive_last_to_sewn_first_right_unitary is None
        assert result.sewn_first_to_primitive_last_right_unitary is None
        assert result.distributed_closure_correction_right_unitary_step is None
        assert result.schur_backend_identifier is None
        reconstructed = Periodic1DRankNAlignmentTransportOwnerResult.from_json(
            result.to_json()
        )
        assert reconstructed.to_json() == result.to_json()

    def test__transport_owner_result__rejects_missing_qualified_action(self) -> None:
        result = Periodic1DRankNAlignmentTransportOwnerResult.from_owner_outcome(
            request=_transport_request(),
            outcome=_owner_outcome(rank_deficient=False),
        )

        with pytest.raises(ValueError, match="all three closure right unitaries"):
            replace(result, sewn_first_to_primitive_last_right_unitary=None)

    def test__transport_owner_result__rejects_inconsistent_closure_directions(
        self,
    ) -> None:
        result = Periodic1DRankNAlignmentTransportOwnerResult.from_owner_outcome(
            request=_transport_request(),
            outcome=_owner_outcome(rank_deficient=False),
        )
        inconsistent_reverse = ComplexMatrixQuantity(
            1.0j * np.eye(3, dtype=np.complex128),
            Unitless(),
        )

        with pytest.raises(ValueError, match="must be the adjoint"):
            replace(
                result,
                sewn_first_to_primitive_last_right_unitary=inconsistent_reverse,
            )

    def test__transport_owner_result__rejects_inconsistent_distributed_root(
        self,
    ) -> None:
        result = Periodic1DRankNAlignmentTransportOwnerResult.from_owner_outcome(
            request=_transport_request(),
            outcome=_owner_outcome(rank_deficient=False),
        )
        inconsistent_step = ComplexMatrixQuantity(
            1.0j * np.eye(3, dtype=np.complex128),
            Unitless(),
        )

        with pytest.raises(ValueError, match="must close"):
            replace(
                result,
                distributed_closure_correction_right_unitary_step=inconsistent_step,
            )

    def test__transport_owner_result__rejects_mismatched_bound_request(self) -> None:
        result = Periodic1DRankNAlignmentTransportOwnerResult.from_owner_outcome(
            request=_transport_request(),
            outcome=_owner_outcome(rank_deficient=False),
        )

        with pytest.raises(ValueError, match="case and mesh disagree"):
            replace(result, request=_transport_request(circuit_depth=2))

    def test__transport_owner_result__rejects_nonmesh_route_source(self) -> None:
        frames = np.zeros((513, 6, 3), dtype=np.complex128)
        frames[:, :3, :] = np.eye(3, dtype=np.complex128)
        source = OrderedReducedPointFrameInventory.from_arrays(
            reduced_points=tuple((float(index) / 513.0,) for index in range(513)),
            frames=frames,
            endpoint_sewing_map=np.eye(6, dtype=np.complex128),
            ambient_basis_identifier="ordered-six-state-ambient-basis",
            retained_frame_identifier="r03-L01-retained-frame",
            endpoint_sewing_identifier="periodic-reciprocal-endpoint-sewing",
            principal_phase_branch=(
                ClosedLoopPolarFrameTransportPrincipalPhaseBranch.negative_pi_open
            ),
            tolerance=_owner_tolerance(),
        )
        outcome = ClosedLoopPolarFrameTransporter().transport(source)

        with pytest.raises(TypeError, match="FinitePeriodicMeshFrameInventory"):
            Periodic1DRankNAlignmentTransportOwnerResult.from_owner_outcome(
                request=_transport_request(),
                outcome=outcome,
            )

    def test__transport_owner_result__rejects_shifted_source_mesh(self) -> None:
        with pytest.raises(ValueError, match="unshifted centered mesh"):
            Periodic1DRankNAlignmentTransportOwnerResult.from_owner_outcome(
                request=_transport_request(),
                outcome=_owner_outcome(rank_deficient=False, mesh_offset=0.25),
            )

    def test__transport_owner_result__rejects_wrong_source_identity(self) -> None:
        with pytest.raises(ValueError, match="identities disagree"):
            Periodic1DRankNAlignmentTransportOwnerResult.from_owner_outcome(
                request=_transport_request(),
                outcome=_owner_outcome(
                    rank_deficient=False,
                    ambient_basis_identifier="wrong-ambient-basis",
                ),
            )

    def test__transport_owner_result__rejects_wrong_source_mesh_size(self) -> None:
        with pytest.raises(ValueError, match="mesh size disagrees"):
            Periodic1DRankNAlignmentTransportOwnerResult.from_owner_outcome(
                request=_transport_request(construction_mesh_size=1025),
                outcome=_owner_outcome(rank_deficient=False),
            )

    def test__transport_owner_result__rejects_mismatched_case_rank(self) -> None:
        outcome = _owner_outcome(rank_deficient=False)

        with pytest.raises(ValueError, match="rank disagrees"):
            Periodic1DRankNAlignmentTransportOwnerResult.from_owner_outcome(
                request=_transport_request(retained_rank=4),
                outcome=outcome,
            )
