"""Generate exploratory analysis of the smooth non-flat four-state realization."""

from __future__ import annotations

import csv
import math
from pathlib import Path

from development_study import (
    adaptive_amplitude,
    amplitude_refinement_levels,
    analysis_verification_defect,
    momentum_refinement,
    qualified_parent,
)

RESULTS = Path(__file__).resolve().parent / "simulations" / "development" / "results"
MOMENTUM_MESHES = (32, 64, 128, 256, 512)
MOMENTUM_AMPLITUDE_INTERVALS = 64
AMPLITUDE_RESOLUTION_MESH = 128
AMPLITUDE_INTERVALS = (8, 16, 32, 64)
TAIL_RANGES = (0, 1, 2, 3, 4, 6, 8)
POWER_MAP_MAXIMUM_RANGE = 12
DRAFT_TOLERANCE = 1.01e-8


def _number(value: float) -> str:
    return format(value, ".17g")


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError("rows must not be empty")
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=tuple(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _amplitudes(intervals: int) -> tuple[float, ...]:
    return tuple(
        float(index * math.pi / (4 * intervals)) for index in range(intervals + 1)
    )


def main() -> None:
    """Execute the pre-version non-flat analysis and write deterministic tables."""
    amplitudes = _amplitudes(MOMENTUM_AMPLITUDE_INTERVALS)
    convergence = momentum_refinement(
        reciprocal_mesh_sizes=MOMENTUM_MESHES,
        amplitudes=amplitudes,
        parent_hopping_scale=1.0,
        draft_tolerance=DRAFT_TOLERANCE,
    )
    verification_defects = {
        result.request.reciprocal_mesh_size: analysis_verification_defect(result)
        for result in convergence.mesh_analyses
    }
    refinement_rows = [
        {
            "coarse_mesh_size": str(item.coarse_mesh_size),
            "fine_mesh_size": str(item.fine_mesh_size),
            "maximum_parent_diagnostic_change": _number(
                item.maximum_parent_diagnostic_change
            ),
            "maximum_shared_parent_eigenvalue_defect": _number(
                item.maximum_shared_parent_eigenvalue_defect
            ),
            "maximum_shared_projector_defect": _number(
                item.maximum_shared_parent_projector_defect
            ),
            "maximum_correlation_change": _number(item.maximum_correlation_change),
            "maximum_threshold_change": _number(item.maximum_threshold_change),
            "maximum_hopping_weight_change": _number(
                item.maximum_hopping_weight_change
            ),
            "maximum_hopping_block_power_change": _number(
                item.maximum_hopping_power_change
            ),
            "maximum_angle_change": _number(item.maximum_angle_change),
            "maximum_band_defect": _number(item.maximum_band_defect),
            "maximum_reconstruction_defect": _number(
                item.maximum_reconstruction_defect
            ),
            "maximum_parseval_defect": _number(item.maximum_parseval_defect),
            "fine_mesh_verification_defect": _number(
                verification_defects[item.fine_mesh_size]
            ),
            "within_draft_tolerances": str(item.within_tolerances).lower(),
        }
        for item in convergence.refinements
    ]
    _write_csv(RESULTS / "nonflat-momentum-refinement.csv", refinement_rows)

    amplitude_refinement = adaptive_amplitude(
        reciprocal_mesh_size=AMPLITUDE_RESOLUTION_MESH,
        initial_amplitudes=_amplitudes(min(AMPLITUDE_INTERVALS)),
        parent_hopping_scale=1.0,
        draft_tolerance=DRAFT_TOLERANCE,
        maximum_refinement_levels=len(AMPLITUDE_INTERVALS),
        maximum_evaluated_amplitudes=2 * max(AMPLITUDE_INTERVALS) + 1,
    )
    resolution_rows = [
        {
            "amplitude_intervals": str(len(level.interpolation_nodes) - 1),
            "maximum_correlation_midpoint_defect": _number(
                level.maximum_correlation_defect
            ),
            "maximum_operator_threshold_midpoint_defect": _number(
                level.maximum_operator_threshold_defect
            ),
            "maximum_joint_threshold_midpoint_defect": _number(
                level.maximum_joint_threshold_defect
            ),
            "maximum_nonzero_hopping_weight_midpoint_defect": _number(
                level.maximum_hopping_weight_defect
            ),
            "maximum_hopping_block_power_midpoint_defect": _number(
                level.maximum_hopping_power_defect
            ),
            "passes_draft_tolerance": str(level.within_tolerances).lower(),
        }
        for level in amplitude_refinement_levels(amplitude_refinement)
    ]
    _write_csv(RESULTS / "nonflat-amplitude-resolution.csv", resolution_rows)

    final = convergence.mesh_analyses[-1]
    qualification = qualified_parent(final)
    continuum_rows = [
        {
            "amplitude": _number(point.amplitude),
            "maximum_band_defect": _number(point.maximum_band_defect),
            "maximum_correlation": _number(point.discrete_maximum_correlation),
            "minimum_operator_threshold": _number(point.minimum_operator_threshold),
            "exact_spectrum_joint_operator_threshold": _number(
                point.exact_spectrum_joint_operator_threshold
            ),
            "reference_nonzero_hopping_weight": _number(
                point.reference_nonzero_hopping_weight
            ),
            "comparison_nonzero_hopping_weight": _number(
                point.comparison_nonzero_hopping_weight
            ),
        }
        for point in final.points
    ]
    _write_csv(RESULTS / "nonflat-continuum.csv", continuum_rows)

    power_map_rows: list[dict[str, str]] = []
    for point in final.points:
        for absolute_displacement in range(POWER_MAP_MAXIMUM_RANGE + 1):
            matching = tuple(
                block
                for block in point.hopping_powers
                if abs(block.displacement) == absolute_displacement
            )
            power_map_rows.append(
                {
                    "amplitude": _number(point.amplitude),
                    "absolute_displacement": str(absolute_displacement),
                    "reference_normalized_hopping_weight": _number(
                        math.fsum(
                            block.reference_normalized_squared_frobenius_norm
                            for block in matching
                        )
                    ),
                    "comparison_normalized_hopping_weight": _number(
                        math.fsum(
                            block.comparison_normalized_squared_frobenius_norm
                            for block in matching
                        )
                    ),
                }
            )
    _write_csv(RESULTS / "nonflat-hopping-power-map.csv", power_map_rows)

    selected_amplitudes = (0.0, math.pi / 8.0, math.pi / 4.0)
    tail_rows: list[dict[str, str]] = []
    for selected in selected_amplitudes:
        point = min(final.points, key=lambda item: abs(item.amplitude - selected))
        for maximum_range in TAIL_RANGES:
            reference_tail = math.fsum(
                block.reference_normalized_squared_frobenius_norm
                for block in point.hopping_powers
                if abs(block.displacement) > maximum_range
            )
            comparison_tail = math.fsum(
                block.comparison_normalized_squared_frobenius_norm
                for block in point.hopping_powers
                if abs(block.displacement) > maximum_range
            )
            tail_rows.append(
                {
                    "amplitude": _number(point.amplitude),
                    "maximum_range": str(maximum_range),
                    "reference_normalized_tail_weight": _number(reference_tail),
                    "comparison_normalized_tail_weight": _number(comparison_tail),
                    "maximum_correlation": _number(point.discrete_maximum_correlation),
                    "minimum_operator_threshold": _number(
                        point.minimum_operator_threshold
                    ),
                    "exact_spectrum_joint_operator_threshold": _number(
                        point.exact_spectrum_joint_operator_threshold
                    ),
                }
            )
    _write_csv(RESULTS / "nonflat-selected-hopping-tails.csv", tail_rows)

    print(f"momentum_disposition={type(convergence).__name__}")
    print(f"minimum_sampled_external_gap={qualification.minimum_external_gap:.17g}")
    print(
        "minimum_sampled_transport_singular_value="
        f"{qualification.minimum_transport_singular_value:.17g}"
    )
    print(f"maximum_verification_defect={max(verification_defects.values()):.17g}")


if __name__ == "__main__":
    main()
