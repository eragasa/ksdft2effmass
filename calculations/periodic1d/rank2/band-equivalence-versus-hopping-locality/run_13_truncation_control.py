#!/usr/bin/env python3
"""Analyze finite-range band consequences across the sampled parent family."""

from __future__ import annotations

import csv
import math
from pathlib import Path

from rank2_control_analysis import (
    completed_truncation,
    truncation_analysis,
    truncation_verification_defect,
)

RESULTS = Path(__file__).resolve().parent / "simulations" / "development" / "results"
PARENT_HOPPING_SCALES = (0.0, 0.25, 0.5, 0.75, 1.0)
MOMENTUM_MESH_SIZE = 256
EVALUATION_MESH_SIZE = 4 * MOMENTUM_MESH_SIZE + 1
AMPLITUDE_INTERVALS = 32
MAXIMUM_RANGE = 16
MAXIMUM_RANGES = tuple(range(MAXIMUM_RANGE + 1))


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


def main() -> None:
    """Write pointwise Hamiltonian and band-error channels."""
    rows: list[dict[str, str]] = []
    summary_rows: list[dict[str, str]] = []
    maximum_verification_discrepancy = 0.0
    for parent_scale in PARENT_HOPPING_SCALES:
        print(f"parent_hopping_scale={parent_scale:g}: start", flush=True)
        result = completed_truncation(
            truncation_analysis(
                construction_mesh_size=MOMENTUM_MESH_SIZE,
                evaluation_mesh_size=EVALUATION_MESH_SIZE,
                amplitudes=_amplitudes(),
                parent_hopping_scale=parent_scale,
                maximum_range=MAXIMUM_RANGE,
            )
        )
        maximum_verification_discrepancy = max(
            maximum_verification_discrepancy,
            truncation_verification_defect(result),
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
                            point.direct_spectral_maximum_defect
                        ),
                        "comparison_maximum_interpolation_hamiltonian_error": _number(
                            point.comparison_interpolation_hamiltonian_maximum_error
                        ),
                        "comparison_rms_interpolation_hamiltonian_error": _number(
                            point.comparison_interpolation_hamiltonian_rms_error
                        ),
                        "comparison_maximum_interpolation_band_error": _number(
                            point.comparison_interpolation_spectral_maximum_error
                        ),
                        "comparison_rms_interpolation_band_error": _number(
                            point.comparison_interpolation_spectral_rms_error
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
                        "reference_maximum_truncation_hamiltonian_error": _number(
                            range_result.reference_truncation_hamiltonian_maximum_error
                        ),
                        "reference_rms_truncation_hamiltonian_error": _number(
                            range_result.reference_truncation_hamiltonian_rms_error
                        ),
                        "reference_maximum_band_error": _number(
                            range_result.reference_truncation_spectral_maximum_error
                        ),
                        "reference_rms_band_error": _number(
                            range_result.reference_truncation_spectral_rms_error
                        ),
                        "comparison_maximum_truncation_hamiltonian_error": _number(
                            range_result.comparison_truncation_hamiltonian_maximum_error
                        ),
                        "comparison_rms_truncation_hamiltonian_error": _number(
                            range_result.comparison_truncation_hamiltonian_rms_error
                        ),
                        "comparison_maximum_truncation_band_error": _number(
                            range_result.comparison_truncation_spectral_maximum_error
                        ),
                        "comparison_rms_truncation_band_error": _number(
                            range_result.comparison_truncation_spectral_rms_error
                        ),
                        "comparison_maximum_total_hamiltonian_error": _number(
                            range_result.comparison_total_hamiltonian_maximum_error
                        ),
                        "comparison_rms_total_hamiltonian_error": _number(
                            range_result.comparison_total_hamiltonian_rms_error
                        ),
                        "comparison_maximum_total_band_error": _number(
                            range_result.comparison_total_spectral_maximum_error
                        ),
                        "comparison_rms_total_band_error": _number(
                            range_result.comparison_total_spectral_rms_error
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
                    max(point.direct_spectral_maximum_defect for point in result.points)
                ),
                "maximum_interpolation_hamiltonian_error": _number(
                    max(
                        point.comparison_interpolation_hamiltonian_maximum_error
                        for point in result.points
                    )
                ),
                "maximum_interpolation_band_error": _number(
                    max(
                        point.comparison_interpolation_spectral_maximum_error
                        for point in result.points
                    )
                ),
                "endpoint_range_0_total_hamiltonian_error": _number(
                    endpoint.ranges[0].comparison_total_hamiltonian_maximum_error
                ),
                "endpoint_range_0_total_band_error": _number(
                    endpoint.ranges[0].comparison_total_spectral_maximum_error
                ),
                "endpoint_range_8_total_hamiltonian_error": _number(
                    endpoint.ranges[
                        MAXIMUM_RANGES.index(8)
                    ].comparison_total_hamiltonian_maximum_error
                ),
                "endpoint_range_8_total_band_error": _number(
                    endpoint.ranges[
                        MAXIMUM_RANGES.index(8)
                    ].comparison_total_spectral_maximum_error
                ),
                "endpoint_range_16_total_hamiltonian_error": _number(
                    endpoint.ranges[-1].comparison_total_hamiltonian_maximum_error
                ),
                "endpoint_range_16_total_band_error": _number(
                    endpoint.ranges[-1].comparison_total_spectral_maximum_error
                ),
            }
        )
    _write_csv(RESULTS / "truncation-consequences.csv", rows)
    _write_csv(RESULTS / "truncation-summary.csv", summary_rows)
    maximum_interpolation = max(
        float(row["maximum_interpolation_band_error"]) for row in summary_rows
    )
    maximum_range_16 = max(
        float(row["endpoint_range_16_total_band_error"]) for row in summary_rows
    )
    print(f"rows={len(rows)}")
    print(f"maximum_interpolation_band_error={maximum_interpolation:.17g}")
    print(f"maximum_endpoint_range_16_total_band_error={maximum_range_16:.17g}")
    print(
        "maximum_independent_verification_discrepancy="
        f"{maximum_verification_discrepancy:.17g}"
    )


if __name__ == "__main__":
    main()
