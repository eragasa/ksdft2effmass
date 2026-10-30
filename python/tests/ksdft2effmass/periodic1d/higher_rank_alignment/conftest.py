"""Shared fixtures for higher-rank calculation-producer tests."""

import pytest
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesRankCutoffRule,
)
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
    ClosedLoopPolarFrameTransportPrincipalPhaseBranch,
    EndpointSewingAction,
    FrameRotationAction,
)

from ksdft2effmass.analysis.matrix_field.diagnostics import ScalarRefinementAnalyzer
from ksdft2effmass.periodic1d.higher_rank_alignment import (
    Periodic1DHigherRankAlignmentAnalyzer,
    Periodic1DHigherRankAlignmentCalculationControls,
    Periodic1DHigherRankAlignmentCalculationRequest,
    Periodic1DHigherRankAlignmentCalculationResult,
    Periodic1DHigherRankAlignmentConfiguration,
)


@pytest.fixture
def higher_rank_configuration() -> Periodic1DHigherRankAlignmentConfiguration:
    """Return the exact version-one higher-rank configuration."""
    configuration_type = Periodic1DHigherRankAlignmentConfiguration
    return configuration_type(
        family_identity=configuration_type.FAMILY_IDENTITY,
        version_identity=configuration_type.VERSION_IDENTITY,
        retained_ranks=configuration_type.RETAINED_RANKS,
        circuit_depths=configuration_type.CIRCUIT_DEPTHS,
        construction_mesh_sizes=configuration_type.CONSTRUCTION_MESH_SIZES,
        final_construction_mesh_size=configuration_type.FINAL_CONSTRUCTION_MESH_SIZE,
        global_unitary_selection_mesh_size=(
            configuration_type.GLOBAL_UNITARY_SELECTION_MESH_SIZE
        ),
        evaluation_mesh_size=configuration_type.EVALUATION_MESH_SIZE,
        evaluation_shift_numerator=configuration_type.EVALUATION_SHIFT_NUMERATOR,
        evaluation_shift_denominator=configuration_type.EVALUATION_SHIFT_DENOMINATOR,
        gauge_alignments=configuration_type.GAUGE_ALIGNMENTS,
        frame_rotation_action=FrameRotationAction.RIGHT,
        endpoint_sewing_action=EndpointSewingAction.LEFT_AMBIENT,
        principal_phase_branch=(
            ClosedLoopPolarFrameTransportPrincipalPhaseBranch.negative_pi_open
        ),
        rank_cutoff_rule=ComplexUnitaryProcrustesRankCutoffRule.MAXIMUM,
        rank_absolute_tolerance=configuration_type.RANK_ABSOLUTE_TOLERANCE,
        rank_relative_tolerance=configuration_type.RANK_RELATIVE_TOLERANCE,
        backend_validation_absolute_tolerance=(
            configuration_type.BACKEND_VALIDATION_ABSOLUTE_TOLERANCE
        ),
        backend_validation_relative_tolerance=(
            configuration_type.BACKEND_VALIDATION_RELATIVE_TOLERANCE
        ),
        endpoint_and_primitive_closure_tolerance=(
            configuration_type.ENDPOINT_AND_PRIMITIVE_CLOSURE_TOLERANCE
        ),
        maximum_closure_phase_tolerance=(
            configuration_type.MAXIMUM_CLOSURE_PHASE_TOLERANCE
        ),
    )


@pytest.fixture
def higher_rank_calculation_request(
    higher_rank_configuration: Periodic1DHigherRankAlignmentConfiguration,
) -> Periodic1DHigherRankAlignmentCalculationRequest:
    """Return the smallest-rank, shallowest-depth complete calculation request."""
    return Periodic1DHigherRankAlignmentCalculationRequest(
        configuration=higher_rank_configuration,
        controls=Periodic1DHigherRankAlignmentCalculationControls.frozen(),
        retained_rank=3,
        circuit_depth=1,
        ambient_basis_identifier="analytic-parent-ordered-retained-exterior-basis",
        retained_frame_identifier="analytic-retained-coordinate-frame",
        endpoint_sewing_identifier="analytic-periodic-identity-sewing",
        represented_basis_identifier="aligned-retained-orbital-basis",
        energy_reference_identifier="analytic-dimensionless-zero",
    )


@pytest.fixture(scope="session")
def higher_rank_calculation_result() -> Periodic1DHigherRankAlignmentCalculationResult:
    """Execute one complete smallest case once for integration assertions."""
    configuration_type = Periodic1DHigherRankAlignmentConfiguration
    configuration = configuration_type(
        family_identity=configuration_type.FAMILY_IDENTITY,
        version_identity=configuration_type.VERSION_IDENTITY,
        retained_ranks=configuration_type.RETAINED_RANKS,
        circuit_depths=configuration_type.CIRCUIT_DEPTHS,
        construction_mesh_sizes=configuration_type.CONSTRUCTION_MESH_SIZES,
        final_construction_mesh_size=configuration_type.FINAL_CONSTRUCTION_MESH_SIZE,
        global_unitary_selection_mesh_size=(
            configuration_type.GLOBAL_UNITARY_SELECTION_MESH_SIZE
        ),
        evaluation_mesh_size=configuration_type.EVALUATION_MESH_SIZE,
        evaluation_shift_numerator=configuration_type.EVALUATION_SHIFT_NUMERATOR,
        evaluation_shift_denominator=configuration_type.EVALUATION_SHIFT_DENOMINATOR,
        gauge_alignments=configuration_type.GAUGE_ALIGNMENTS,
        frame_rotation_action=FrameRotationAction.RIGHT,
        endpoint_sewing_action=EndpointSewingAction.LEFT_AMBIENT,
        principal_phase_branch=(
            ClosedLoopPolarFrameTransportPrincipalPhaseBranch.negative_pi_open
        ),
        rank_cutoff_rule=ComplexUnitaryProcrustesRankCutoffRule.MAXIMUM,
        rank_absolute_tolerance=configuration_type.RANK_ABSOLUTE_TOLERANCE,
        rank_relative_tolerance=configuration_type.RANK_RELATIVE_TOLERANCE,
        backend_validation_absolute_tolerance=(
            configuration_type.BACKEND_VALIDATION_ABSOLUTE_TOLERANCE
        ),
        backend_validation_relative_tolerance=(
            configuration_type.BACKEND_VALIDATION_RELATIVE_TOLERANCE
        ),
        endpoint_and_primitive_closure_tolerance=(
            configuration_type.ENDPOINT_AND_PRIMITIVE_CLOSURE_TOLERANCE
        ),
        maximum_closure_phase_tolerance=(
            configuration_type.MAXIMUM_CLOSURE_PHASE_TOLERANCE
        ),
    )
    request = Periodic1DHigherRankAlignmentCalculationRequest(
        configuration=configuration,
        controls=Periodic1DHigherRankAlignmentCalculationControls.frozen(),
        retained_rank=3,
        circuit_depth=1,
        ambient_basis_identifier="analytic-parent-ordered-retained-exterior-basis",
        retained_frame_identifier="analytic-retained-coordinate-frame",
        endpoint_sewing_identifier="analytic-periodic-identity-sewing",
        represented_basis_identifier="aligned-retained-orbital-basis",
        energy_reference_identifier="analytic-dimensionless-zero",
    )
    return Periodic1DHigherRankAlignmentAnalyzer(
        request=request,
        procrustes_solver=NumpyBatchedComplexUnitaryProcrustesSolver(),
        transporter=ClosedLoopPolarFrameTransporter(),
        scalar_refinement_analyzer=ScalarRefinementAnalyzer(),
    ).execute()
