"""Analyze robustness across the bounded four-state parent-hopping homotopy."""

from __future__ import annotations

import csv
import math
from pathlib import Path

from ksdft2effmass.campaigns.model_adequacy.band_equivalence_locality.periodic1d import (
    SmoothFourStateConvergenceDefinition,
    SmoothFourStateConvergenceExperiment,
    SmoothFourStateConvergenceThresholds,
    SmoothFourStateVerifier,
)

ANALYSIS = Path(__file__).resolve().parent
PARENT_HOPPING_SCALES = (0.0, 0.25, 0.5, 0.75, 1.0)
MOMENTUM_MESHES = (32, 64, 128, 256)
AMPLITUDE_INTERVALS = 32
DRAFT_TOLERANCE = 1.01e-8
VERIFICATION_TOLERANCE = 1.0e-10


def _number(value: float) -> str:
    return format(value, ".17g")


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError("rows must not be empty")
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=tuple(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _amplitudes() -> tuple[float, ...]:
    return tuple(
        float(index * math.pi / (4 * AMPLITUDE_INTERVALS))
        for index in range(AMPLITUDE_INTERVALS + 1)
    )


def main() -> int:
    """Write finite-mesh family surfaces and momentum-control summaries."""
    thresholds = SmoothFourStateConvergenceThresholds(
        maximum_parent_diagnostic_change=DRAFT_TOLERANCE,
        maximum_correlation_change=DRAFT_TOLERANCE,
        maximum_threshold_change=DRAFT_TOLERANCE,
        maximum_hopping_weight_change=DRAFT_TOLERANCE,
        maximum_hopping_block_power_change=DRAFT_TOLERANCE,
        maximum_angle_change=DRAFT_TOLERANCE,
        maximum_band_defect=DRAFT_TOLERANCE,
        maximum_reconstruction_defect=DRAFT_TOLERANCE,
        maximum_parseval_defect=DRAFT_TOLERANCE,
    )
    experiment = SmoothFourStateConvergenceExperiment()
    verifier = SmoothFourStateVerifier()
    surface_rows: list[dict[str, str]] = []
    summary_rows: list[dict[str, str]] = []
    for parent_scale in PARENT_HOPPING_SCALES:
        convergence = experiment.execute(
            SmoothFourStateConvergenceDefinition(
                reciprocal_mesh_sizes=MOMENTUM_MESHES,
                amplitudes=_amplitudes(),
                minimum_external_gap=1.0,
                minimum_transport_singular_value=0.99,
                frame_absolute_tolerance=1.0e-10,
                harmonic_absolute_degeneracy_tolerance=1.0e-14,
                harmonic_relative_degeneracy_tolerance=1.0e-13,
                verification_absolute_tolerance=VERIFICATION_TOLERANCE,
                parent_hopping_scale=parent_scale,
                thresholds=thresholds,
                required_stable_refinements=2,
            )
        )
        final = convergence.mesh_results[-1]
        verification = verifier.execute(final)
        for point in final.points:
            root_scale = math.sqrt(point.splitting_scale)
            surface_rows.append(
                {
                    "parent_hopping_scale": _number(parent_scale),
                    "amplitude": _number(point.amplitude),
                    "maximum_correlation": _number(point.discrete_maximum_correlation),
                    "splitting_scale": _number(point.splitting_scale),
                    "minimum_operator_threshold_over_sqrt_kappa": _number(
                        point.minimum_operator_threshold / root_scale
                    ),
                    "joint_threshold_over_sqrt_kappa": _number(
                        point.exact_spectrum_joint_operator_threshold / root_scale
                    ),
                    "reference_nonzero_hopping_weight": _number(
                        point.reference_nonzero_hopping_weight
                    ),
                    "comparison_nonzero_hopping_weight": _number(
                        point.comparison_nonzero_hopping_weight
                    ),
                    "excess_nonzero_hopping_weight": _number(
                        point.comparison_nonzero_hopping_weight
                        - point.reference_nonzero_hopping_weight
                    ),
                    "normalized_squared_operator_residual": _number(
                        (point.minimum_operator_threshold / root_scale) ** 2
                    ),
                    "normalized_excess_nonzero_hopping_weight": _number(
                        (
                            point.comparison_nonzero_hopping_weight
                            - point.reference_nonzero_hopping_weight
                        )
                        / point.splitting_scale
                    ),
                    "flat_identity_departure": _number(
                        (
                            point.comparison_nonzero_hopping_weight
                            - point.reference_nonzero_hopping_weight
                        )
                        / point.splitting_scale
                        - (point.minimum_operator_threshold / root_scale) ** 2
                    ),
                    "maximum_band_defect": _number(point.maximum_band_defect),
                }
            )
        final_refinement = convergence.refinements[-1]
        endpoint = final.points[-1]
        summary_rows.append(
            {
                "parent_hopping_scale": _number(parent_scale),
                "momentum_disposition": convergence.disposition.value,
                "minimum_sampled_external_gap": _number(final.minimum_external_gap),
                "minimum_sampled_transport_singular_value": _number(
                    final.minimum_transport_singular_value
                ),
                "maximum_final_parent_invariant_change": _number(
                    final_refinement.maximum_parent_diagnostic_change
                ),
                "maximum_final_outcome_change": _number(
                    max(
                        final_refinement.maximum_correlation_change,
                        final_refinement.maximum_threshold_change,
                        final_refinement.maximum_hopping_weight_change,
                        final_refinement.maximum_hopping_block_power_change,
                    )
                ),
                "verification_defect": _number(verification.maximum_absolute_defect),
                "endpoint_minimum_threshold_over_sqrt_kappa": _number(
                    endpoint.minimum_operator_threshold
                    / math.sqrt(endpoint.splitting_scale)
                ),
                "endpoint_excess_nonzero_hopping_weight": _number(
                    endpoint.comparison_nonzero_hopping_weight
                    - endpoint.reference_nonzero_hopping_weight
                ),
            }
        )
    _write_csv(ANALYSIS / "parent-family-continuum.csv", surface_rows)
    _write_csv(ANALYSIS / "parent-family-summary.csv", summary_rows)
    print(f"parent_scales={len(PARENT_HOPPING_SCALES)}")
    print(f"amplitudes={AMPLITUDE_INTERVALS + 1}")
    print(
        "momentum_dispositions="
        + ",".join(row["momentum_disposition"] for row in summary_rows)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
