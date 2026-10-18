"""Analyze finite-range band consequences across the sampled parent family."""

from __future__ import annotations

import csv
import math
from pathlib import Path

from band_equivalence_hopping_locality import (
    SmoothFourStateDefinition,
    SmoothFourStateTruncationDefinition,
    SmoothFourStateTruncationExperiment,
)

ANALYSIS = Path(__file__).resolve().parent
PARENT_HOPPING_SCALES = (0.0, 0.25, 0.5, 0.75, 1.0)
MOMENTUM_MESH_SIZE = 256
EVALUATION_MESH_SIZE = 4 * MOMENTUM_MESH_SIZE + 1
AMPLITUDE_INTERVALS = 32
MAXIMUM_RANGES = (0, 1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64)


def _number(value: float) -> str:
    return format(value, ".17g")


def _amplitudes() -> tuple[float, ...]:
    return tuple(
        float(index * math.pi / (4 * AMPLITUDE_INTERVALS))
        for index in range(AMPLITUDE_INTERVALS + 1)
    )


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError("rows must not be empty")
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=tuple(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    """Write pointwise interpolation, truncation, and total band-error channels."""
    rows: list[dict[str, str]] = []
    summary_rows: list[dict[str, str]] = []
    experiment = SmoothFourStateTruncationExperiment()
    for parent_scale in PARENT_HOPPING_SCALES:
        print(f"parent_hopping_scale={parent_scale:g}: start", flush=True)
        result = experiment.execute(
            SmoothFourStateTruncationDefinition(
                model=SmoothFourStateDefinition(
                    reciprocal_mesh_size=MOMENTUM_MESH_SIZE,
                    amplitudes=_amplitudes(),
                    minimum_external_gap=1.0,
                    minimum_transport_singular_value=0.99,
                    frame_absolute_tolerance=1.0e-10,
                    harmonic_absolute_degeneracy_tolerance=1.0e-14,
                    harmonic_relative_degeneracy_tolerance=1.0e-13,
                    verification_absolute_tolerance=1.0e-10,
                    parent_hopping_scale=parent_scale,
                ),
                maximum_ranges=MAXIMUM_RANGES,
                evaluation_mesh_size=EVALUATION_MESH_SIZE,
            )
        )
        for point in result.points:
            for range_result in point.ranges:
                rows.append(
                    {
                        "parent_hopping_scale": _number(parent_scale),
                        "amplitude": _number(point.amplitude),
                        "maximum_range": str(range_result.maximum_range),
                        "reference_nyquist_power": _number(
                            point.reference_nyquist_power
                        ),
                        "comparison_nyquist_power": _number(
                            point.comparison_nyquist_power
                        ),
                        "maximum_direct_band_defect": _number(
                            point.maximum_direct_band_defect
                        ),
                        "comparison_maximum_interpolation_band_error": _number(
                            point.comparison_maximum_interpolation_band_error
                        ),
                        "comparison_rms_interpolation_band_error": _number(
                            point.comparison_rms_interpolation_band_error
                        ),
                        "reference_ordinary_omitted_power": _number(
                            range_result.reference_ordinary_omitted_power
                        ),
                        "comparison_ordinary_omitted_power": _number(
                            range_result.comparison_ordinary_omitted_power
                        ),
                        "reference_total_omitted_power": _number(
                            range_result.reference_total_omitted_power
                        ),
                        "comparison_total_omitted_power": _number(
                            range_result.comparison_total_omitted_power
                        ),
                        "reference_maximum_band_error": _number(
                            range_result.reference_maximum_band_error
                        ),
                        "reference_rms_band_error": _number(
                            range_result.reference_rms_band_error
                        ),
                        "comparison_maximum_truncation_band_error": _number(
                            range_result.comparison_maximum_truncation_band_error
                        ),
                        "comparison_rms_truncation_band_error": _number(
                            range_result.comparison_rms_truncation_band_error
                        ),
                        "comparison_maximum_total_band_error": _number(
                            range_result.comparison_maximum_total_band_error
                        ),
                        "comparison_rms_total_band_error": _number(
                            range_result.comparison_rms_total_band_error
                        ),
                    }
                )
        print(f"parent_hopping_scale={parent_scale:g}: complete", flush=True)
        endpoint = result.points[-1]
        summary_rows.append(
            {
                "parent_hopping_scale": _number(parent_scale),
                "construction_mesh_size": str(MOMENTUM_MESH_SIZE),
                "evaluation_mesh_size": str(EVALUATION_MESH_SIZE),
                "minimum_mesh_separation": _number(
                    result.minimum_construction_evaluation_separation
                ),
                "maximum_direct_band_defect": _number(
                    max(point.maximum_direct_band_defect for point in result.points)
                ),
                "maximum_interpolation_band_error": _number(
                    max(
                        point.comparison_maximum_interpolation_band_error
                        for point in result.points
                    )
                ),
                "endpoint_range_0_total_band_error": _number(
                    endpoint.ranges[0].comparison_maximum_total_band_error
                ),
                "endpoint_range_8_total_band_error": _number(
                    endpoint.ranges[
                        MAXIMUM_RANGES.index(8)
                    ].comparison_maximum_total_band_error
                ),
                "endpoint_range_64_total_band_error": _number(
                    endpoint.ranges[-1].comparison_maximum_total_band_error
                ),
            }
        )
    _write_csv(ANALYSIS / "truncation-consequences.csv", rows)
    _write_csv(ANALYSIS / "truncation-summary.csv", summary_rows)
    maximum_interpolation = max(
        float(row["maximum_interpolation_band_error"]) for row in summary_rows
    )
    maximum_range_64 = max(
        float(row["endpoint_range_64_total_band_error"]) for row in summary_rows
    )
    print(f"rows={len(rows)}")
    print(f"maximum_interpolation_band_error={maximum_interpolation:.17g}")
    print(f"maximum_endpoint_range_64_total_band_error={maximum_range_64:.17g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
