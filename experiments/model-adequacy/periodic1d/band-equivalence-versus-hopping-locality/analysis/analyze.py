"""Generate exploratory analysis of the smooth flat-parent continuum.

This local deterministic analysis creates no retained run or evidence-package identity.
It evaluates the implemented analytic family and writes reviewable CSV summaries.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
from scipy.special import j0  # type: ignore[import-untyped]

from band_equivalence_hopping_locality import (
    SmoothBlochContinuumConvergenceDefinition,
    SmoothBlochContinuumConvergenceExperiment,
    SmoothBlochContinuumConvergenceThresholds,
    SmoothBlochContinuumConvergenceVerifier,
)

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = Path(__file__).resolve().parent
ANALYTIC_CURVE = ROOT / "smooth-threshold-continuum.csv"
MOMENTUM_MESHES = (32, 64, 128, 256, 512)
AMPLITUDE_INTERVALS = (8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096)
SELECTED_AMPLITUDES = (0.0, math.pi / 8.0, math.pi / 4.0)
TAIL_RANGES = (0, 1, 2, 3, 4, 6, 8)
MAXIMUM_PLOTTED_ABSOLUTE_DISPLACEMENT = 12
DRAFT_ABSOLUTE_TOLERANCE = 1.0e-10
DRAFT_RELATIVE_TOLERANCE = 1.0e-8
UNIT_SCALE_DRAFT_TOLERANCE = DRAFT_ABSOLUTE_TOLERANCE + DRAFT_RELATIVE_TOLERANCE
VERIFICATION_ABSOLUTE_TOLERANCE = 1.0e-11


def _write_csv(
    path: Path, fieldnames: tuple[str, ...], rows: list[dict[str, str]]
) -> None:
    """Write deterministic CSV with Unix newlines."""
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _number(value: float) -> str:
    """Return a round-trip binary64 spelling."""
    return format(value, ".17g")


def _analytic_thresholds(amplitudes: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return the two normalized Bessel threshold laws using SciPy's ``J_0``."""
    correlation = j0(2.0 * amplitudes)
    operator = np.sqrt(np.maximum(0.0, 1.0 - correlation * correlation))
    joint = np.sqrt(np.maximum(0.0, 2.0 * (1.0 - correlation)))
    return operator, joint


def _amplitude_rows() -> list[dict[str, str]]:
    """Measure midpoint interpolation error on nested amplitude grids."""
    rows: list[dict[str, str]] = []
    for intervals in AMPLITUDE_INTERVALS:
        nodes = (
            np.arange(intervals + 1, dtype=np.float64)
            * math.pi
            / (4.0 * float(intervals))
        )
        midpoints = 0.5 * (nodes[:-1] + nodes[1:])
        operator_nodes, joint_nodes = _analytic_thresholds(nodes)
        operator_midpoints, joint_midpoints = _analytic_thresholds(midpoints)
        operator_interpolated = 0.5 * (operator_nodes[:-1] + operator_nodes[1:])
        joint_interpolated = 0.5 * (joint_nodes[:-1] + joint_nodes[1:])
        operator_defect = float(
            np.max(np.abs(operator_interpolated - operator_midpoints))
        )
        joint_defect = float(np.max(np.abs(joint_interpolated - joint_midpoints)))
        rows.append(
            {
                "amplitude_intervals": str(intervals),
                "amplitude_nodes": str(intervals + 1),
                "maximum_operator_threshold_midpoint_interpolation_defect": _number(
                    operator_defect
                ),
                "maximum_joint_threshold_midpoint_interpolation_defect": _number(
                    joint_defect
                ),
                "passes_unit_scale_draft_tolerance": str(
                    max(operator_defect, joint_defect) <= UNIT_SCALE_DRAFT_TOLERANCE
                ).lower(),
            }
        )
    return rows


def main() -> int:
    """Execute the exploratory analysis and write deterministic summaries."""
    analytic = np.genfromtxt(ANALYTIC_CURVE, delimiter=",", names=True)
    amplitudes_csv = np.asarray(analytic["a"], dtype=np.float64)
    operator_csv = np.asarray(
        analytic["operator_threshold_over_sqrt_kappa"], dtype=np.float64
    )
    joint_csv = np.asarray(
        analytic["joint_threshold_over_sqrt_kappa"], dtype=np.float64
    )
    if amplitudes_csv.size != 181:
        raise ValueError("analytic curve must contain exactly 181 samples")
    if not np.all(np.diff(amplitudes_csv) > 0.0):
        raise ValueError("analytic amplitudes must be strictly increasing")
    if not np.all(np.diff(operator_csv) > 0.0) or not np.all(np.diff(joint_csv) > 0.0):
        raise ValueError("both analytic threshold curves must be strictly increasing")

    amplitudes = tuple(float(index * math.pi / (4 * 64)) for index in range(65))
    thresholds = SmoothBlochContinuumConvergenceThresholds(
        maximum_correlation_change=UNIT_SCALE_DRAFT_TOLERANCE,
        maximum_threshold_change=UNIT_SCALE_DRAFT_TOLERANCE,
        maximum_hopping_weight_change=UNIT_SCALE_DRAFT_TOLERANCE,
        maximum_hopping_block_power_change=UNIT_SCALE_DRAFT_TOLERANCE,
        maximum_angle_change=UNIT_SCALE_DRAFT_TOLERANCE,
        maximum_fine_quadrature_defect=UNIT_SCALE_DRAFT_TOLERANCE,
        maximum_band_defect=UNIT_SCALE_DRAFT_TOLERANCE,
        maximum_identity_defect=UNIT_SCALE_DRAFT_TOLERANCE,
        maximum_parseval_defect=UNIT_SCALE_DRAFT_TOLERANCE,
    )
    definition = SmoothBlochContinuumConvergenceDefinition(
        reciprocal_mesh_sizes=MOMENTUM_MESHES,
        amplitudes=amplitudes,
        harmonic_absolute_degeneracy_tolerance=1.0e-14,
        harmonic_relative_degeneracy_tolerance=1.0e-13,
        verification_absolute_tolerance=VERIFICATION_ABSOLUTE_TOLERANCE,
        thresholds=thresholds,
        required_stable_refinements=2,
    )
    result = SmoothBlochContinuumConvergenceExperiment().execute(definition)
    verification = SmoothBlochContinuumConvergenceVerifier().execute(result)
    if not verification.passes:
        raise ValueError("independent reconstruction failed")

    momentum_rows = [
        {
            "coarse_mesh_size": str(item.coarse_mesh_size),
            "fine_mesh_size": str(item.fine_mesh_size),
            "maximum_correlation_change": _number(item.maximum_correlation_change),
            "maximum_threshold_change": _number(item.maximum_threshold_change),
            "maximum_hopping_weight_change": _number(
                item.maximum_hopping_weight_change
            ),
            "maximum_hopping_block_power_change": _number(
                item.maximum_hopping_block_power_change
            ),
            "maximum_angle_change": _number(item.maximum_angle_change),
            "maximum_fine_quadrature_defect": _number(
                item.maximum_fine_quadrature_defect
            ),
            "maximum_band_defect": _number(item.maximum_band_defect),
            "maximum_identity_defect": _number(item.maximum_identity_defect),
            "maximum_parseval_defect": _number(item.maximum_parseval_defect),
            "within_draft_tolerances": str(item.within_tolerances).lower(),
        }
        for item in result.refinements
    ]
    _write_csv(
        ANALYSIS / "momentum-refinement.csv",
        tuple(momentum_rows[0]),
        momentum_rows,
    )

    amplitude_rows = _amplitude_rows()
    _write_csv(
        ANALYSIS / "amplitude-resolution.csv",
        tuple(amplitude_rows[0]),
        amplitude_rows,
    )

    final_result = result.mesh_results[-1]
    tail_rows: list[dict[str, str]] = []
    for selected in SELECTED_AMPLITUDES:
        point = min(
            final_result.points, key=lambda value: abs(value.amplitude - selected)
        )
        if abs(point.amplitude - selected) > 1.0e-15:
            raise ValueError(
                "selected amplitude is absent from the nested amplitude grid"
            )
        for maximum_range in TAIL_RANGES:
            tail = math.fsum(
                item.normalized_squared_frobenius_norm
                for item in point.hopping_blocks
                if abs(item.displacement) > maximum_range
            )
            tail_rows.append(
                {
                    "amplitude": _number(point.amplitude),
                    "maximum_range": str(maximum_range),
                    "normalized_tail_weight": _number(tail),
                    "finite_mesh_maximum_correlation": _number(
                        point.discrete_maximum_correlation
                    ),
                    "minimum_operator_threshold": _number(
                        point.minimum_operator_threshold
                    ),
                    "exact_spectrum_joint_operator_threshold": _number(
                        point.exact_spectrum_joint_operator_threshold
                    ),
                    "nonzero_hopping_weight": _number(point.nonzero_hopping_weight),
                }
            )
    _write_csv(
        ANALYSIS / "selected-hopping-tails.csv",
        tuple(tail_rows[0]),
        tail_rows,
    )

    hopping_power_rows: list[dict[str, str]] = []
    for point in final_result.points:
        for absolute_displacement in range(MAXIMUM_PLOTTED_ABSOLUTE_DISPLACEMENT + 1):
            power = math.fsum(
                item.normalized_squared_frobenius_norm
                for item in point.hopping_blocks
                if abs(item.displacement) == absolute_displacement
            )
            hopping_power_rows.append(
                {
                    "amplitude": _number(point.amplitude),
                    "absolute_displacement": str(absolute_displacement),
                    "normalized_hopping_weight": _number(power),
                }
            )
    _write_csv(
        ANALYSIS / "hopping-power-map.csv",
        tuple(hopping_power_rows[0]),
        hopping_power_rows,
    )

    print(f"disposition={result.disposition.value}")
    print(f"verification_passes={verification.passes}")
    maximum_verification_defect = max(
        item.maximum_absolute_defect for item in verification.mesh_verifications
    )
    print(f"maximum_mesh_verification_defect={maximum_verification_defect:.17g}")
    print(f"analytic_rows={amplitudes_csv.size}")
    print(f"operator_endpoint={operator_csv[-1]:.17g}")
    print(f"joint_endpoint={joint_csv[-1]:.17g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
