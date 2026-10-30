"""Run the direct higher-rank periodic-1D development calculation."""

from __future__ import annotations

import json
from pathlib import Path

from ksdft2effmass.analysis.matrix_field.diagnostics import ScalarRefinementAnalyzer
from ksdft2effmass.periodic1d.higher_rank_alignment import (
    Periodic1DHigherRankAlignmentAnalyzer,
    Periodic1DHigherRankAlignmentCalculationControls,
    Periodic1DHigherRankAlignmentCalculationRequest,
    Periodic1DHigherRankAlignmentCalculationResult,
    Periodic1DHigherRankAlignmentConfiguration,
)
from ksdft2effmass.periodic1d.higher_rank_alignment.gauge_alignment.definition import (
    GaugeAlignmentWireMapping,
)
from projectkoios.optimization.alignment.numpy.batched_procrustes import (
    NumpyBatchedComplexUnitaryProcrustesSolver,
)
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesRankCutoffRule,
)
from projectkoios.physkit.solidstate.electronic import (
    ClosedLoopPolarFrameTransporter,
    ClosedLoopPolarFrameTransportPrincipalPhaseBranch,
    EndpointSewingAction,
    FrameRotationAction,
)
from projectkoios.physkit.solidstate.tb import (
    FinitePeriodicMatrixFourierTensorEvaluator,
    FinitePeriodicMatrixFourierTransformer,
)

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


def _configuration() -> Periodic1DHigherRankAlignmentConfiguration:
    """Return the complete frozen version-one configuration."""
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


def _request(
    configuration: Periodic1DHigherRankAlignmentConfiguration,
    retained_rank: int,
    circuit_depth: int,
) -> Periodic1DHigherRankAlignmentCalculationRequest:
    """Return one complete immutable calculation request."""
    return Periodic1DHigherRankAlignmentCalculationRequest(
        configuration=configuration,
        controls=Periodic1DHigherRankAlignmentCalculationControls.frozen(),
        retained_rank=retained_rank,
        circuit_depth=circuit_depth,
        ambient_basis_identifier="analytic-parent-ordered-retained-exterior-basis",
        retained_frame_identifier="analytic-retained-coordinate-frame",
        endpoint_sewing_identifier="analytic-periodic-identity-sewing",
        represented_basis_identifier="aligned-retained-orbital-basis",
        energy_reference_identifier="analytic-dimensionless-zero",
    )


def _calculate(
    request: Periodic1DHigherRankAlignmentCalculationRequest,
) -> Periodic1DHigherRankAlignmentCalculationResult:
    """Execute one direct case with explicit reviewed collaborators."""
    return Periodic1DHigherRankAlignmentAnalyzer(
        request=request,
        procrustes_solver=NumpyBatchedComplexUnitaryProcrustesSolver(),
        transporter=ClosedLoopPolarFrameTransporter(),
        fourier_transformer=FinitePeriodicMatrixFourierTransformer(),
        fourier_evaluator=FinitePeriodicMatrixFourierTensorEvaluator(),
        scalar_refinement_analyzer=ScalarRefinementAnalyzer(),
    ).execute()


def _case_summary(
    result: Periodic1DHigherRankAlignmentCalculationResult,
) -> dict[str, JsonValue]:
    """Return a bounded development summary without claiming retained evidence."""
    final_gauge_alignments: list[JsonValue] = []
    for alignment in result.meshes[-1].gauge_alignment_results:
        summary: dict[str, JsonValue] = {
            "gauge_alignment": GaugeAlignmentWireMapping.to_wire(
                alignment.status.gauge_alignment
            ),
            "alignment_status": alignment.status.status.value,
            "downstream_applicability": (
                None
                if alignment.status.global_unitary_downstream_applicability is None
                else alignment.status.global_unitary_downstream_applicability.value
            ),
            "support_count": len(alignment.supports),
        }
        if len(alignment.supports) > 2:
            support_two = alignment.supports[2]
            summary["support_two_normalized_tail_l2"] = (
                support_two.normalized_omitted_frobenius_l2_norm
            )
            summary["support_two_normalized_total_operator_error"] = (
                support_two.total.errors.normalized_matrix_frobenius_maximum
            )
            summary["support_two_normalized_total_spectrum_error"] = (
                support_two.total.errors.normalized_ordered_spectrum_maximum
            )
        final_gauge_alignments.append(summary)
    return {
        "case_identity": result.request.case_identity,
        "retained_rank": result.request.retained_rank,
        "circuit_depth": result.request.circuit_depth,
        "construction_mesh_count": len(result.meshes),
        "block_refinement_record_count": len(result.block_refinements),
        "scalar_refinement_record_count": len(result.scalar_refinements),
        "final_mesh_gauge_alignments": final_gauge_alignments,
    }


def _summary() -> dict[str, JsonValue]:
    """Calculate every frozen case and return a development-only shape summary."""
    configuration = _configuration()
    cases: list[JsonValue] = []
    for retained_rank in configuration.retained_ranks:
        for circuit_depth in configuration.circuit_depths:
            cases.append(
                _case_summary(
                    _calculate(
                        _request(configuration, retained_rank, circuit_depth)
                    )
                )
            )
    return {
        "artifact_role": "replaceable-direct-development-summary",
        "scientific_evidence": False,
        "family_identity": configuration.family_identity,
        "version_identity": configuration.version_identity,
        "case_count": len(cases),
        "cases": cases,
    }


def main() -> int:
    """Write one replaceable local summary outside the retained runs tree."""
    output = Path(__file__).resolve().parent / "results"
    output.mkdir(parents=True, exist_ok=True)
    destination = output / "direct-development-summary.json"
    payload = _summary()
    destination.write_text(
        json.dumps(payload, allow_nan=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        "lifecycle=replaceable-direct-development "
        f"case_count={payload['case_count']} output={destination}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
