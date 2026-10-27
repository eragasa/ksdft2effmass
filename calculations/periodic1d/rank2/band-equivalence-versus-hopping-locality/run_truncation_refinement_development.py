"""Evaluate dense-cutoff decision stability across momentum refinements."""

from __future__ import annotations

import csv
import math
from pathlib import Path

from workflow.nonflat import SmoothFourStateDefinition
from workflow.truncation import (
    SmoothFourStateTruncationDefinition,
    SmoothFourStateTruncationExperiment,
    SmoothFourStateTruncationPointResult,
    SmoothFourStateTruncationRangeDecision,
    SmoothFourStateTruncationVerifier,
)

RESULTS = Path(__file__).resolve().parent / "simulations" / "development" / "results"
PARENT_HOPPING_SCALES = (0.0, 0.25, 0.5, 0.75, 1.0)
MOMENTUM_MESHES = (128, 256, 512)
AMPLITUDE_INTERVALS = 32
MAXIMUM_RANGE = 16
DECISION_TOLERANCE = 1.0e-8


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


def _range_value(
    point: SmoothFourStateTruncationPointResult,
    maximum_range: int,
    channel: str,
) -> float:
    item = point.ranges[maximum_range]
    if item.maximum_range != maximum_range:
        raise AssertionError("dense range results must be indexed by maximum range")
    if channel == "reference_band":
        return item.reference_maximum_band_error
    if channel == "comparison_band":
        return item.comparison_maximum_total_band_error
    if channel == "reference_hamiltonian":
        return item.reference_maximum_truncation_hamiltonian_error
    if channel == "comparison_hamiltonian":
        return item.comparison_maximum_total_hamiltonian_error
    raise ValueError("unknown range-decision channel")


def _decision_fields(
    point: SmoothFourStateTruncationPointResult,
    decision: SmoothFourStateTruncationRangeDecision,
) -> dict[str, str]:
    output: dict[str, str] = {}
    selections = (
        ("reference_band", decision.reference_band_first_passing_range),
        ("comparison_band", decision.comparison_band_first_passing_range),
        (
            "reference_hamiltonian",
            decision.reference_hamiltonian_first_passing_range,
        ),
        (
            "comparison_hamiltonian",
            decision.comparison_hamiltonian_first_passing_range,
        ),
    )
    for channel, maximum_range in selections:
        if maximum_range is None:
            raise ValueError(f"{channel} does not pass within the dense cutoff cap")
        passing_error = _range_value(point, maximum_range, channel)
        if passing_error > DECISION_TOLERANCE:
            raise AssertionError("selected range does not pass its declared tolerance")
        output[f"{channel}_first_passing_range"] = str(maximum_range)
        output[f"{channel}_passing_error"] = _number(passing_error)
        if maximum_range == 0:
            output[f"{channel}_preceding_error"] = "not-applicable"
        else:
            preceding_error = _range_value(point, maximum_range - 1, channel)
            if preceding_error <= DECISION_TOLERANCE:
                raise AssertionError("range before first passing range also passes")
            output[f"{channel}_preceding_error"] = _number(preceding_error)
    return output


def main() -> None:
    """Write independently verified, threshold-adjacent refinement decisions."""
    experiment = SmoothFourStateTruncationExperiment()
    verifier = SmoothFourStateTruncationVerifier()
    rows: list[dict[str, str]] = []
    for parent_scale in PARENT_HOPPING_SCALES:
        for mesh_size in MOMENTUM_MESHES:
            print(
                f"parent_hopping_scale={parent_scale:g}, N={mesh_size}: start",
                flush=True,
            )
            definition = SmoothFourStateTruncationDefinition.every_integer_through(
                model=SmoothFourStateDefinition(
                    reciprocal_mesh_size=mesh_size,
                    amplitudes=_amplitudes(),
                    minimum_external_gap=1.0,
                    minimum_transport_singular_value=0.99,
                    frame_absolute_tolerance=1.0e-10,
                    harmonic_absolute_degeneracy_tolerance=1.0e-14,
                    harmonic_relative_degeneracy_tolerance=1.0e-13,
                    verification_absolute_tolerance=1.0e-10,
                    parent_hopping_scale=parent_scale,
                ),
                maximum_range=MAXIMUM_RANGE,
                evaluation_mesh_size=4 * mesh_size + 1,
            )
            result = experiment.execute(definition)
            verification = verifier.execute(result, (DECISION_TOLERANCE,))
            if not verification.passes:
                raise ValueError("independent truncation reconstruction failed")
            if not verification.inventory_is_dense:
                raise AssertionError("refinement study requires a dense inventory")
            if len(verification.decisions) != len(result.points):
                raise AssertionError("one range decision is required per amplitude")
            for point, decision in zip(
                result.points, verification.decisions, strict=True
            ):
                row = {
                    "parent_hopping_scale": _number(parent_scale),
                    "amplitude": _number(point.amplitude),
                    "construction_mesh_size": str(mesh_size),
                    "evaluation_mesh_size": str(definition.evaluation_mesh_size),
                    "decision_tolerance": _number(DECISION_TOLERANCE),
                    "verification_discrepancy": _number(
                        verification.maximum_absolute_discrepancy
                    ),
                }
                row.update(_decision_fields(point, decision))
                rows.append(row)
            print(
                f"parent_hopping_scale={parent_scale:g}, N={mesh_size}: complete",
                flush=True,
            )

    _write_csv(RESULTS / "truncation-refinement.csv", rows)
    keys = (
        "reference_band_first_passing_range",
        "comparison_band_first_passing_range",
        "reference_hamiltonian_first_passing_range",
        "comparison_hamiltonian_first_passing_range",
    )
    final_pair_changes = 0
    by_identity = {
        (
            row["parent_hopping_scale"],
            row["amplitude"],
            row["construction_mesh_size"],
        ): row
        for row in rows
    }
    for parent_scale in PARENT_HOPPING_SCALES:
        for amplitude in _amplitudes():
            coarse = by_identity[
                (_number(parent_scale), _number(amplitude), str(MOMENTUM_MESHES[-2]))
            ]
            fine = by_identity[
                (_number(parent_scale), _number(amplitude), str(MOMENTUM_MESHES[-1]))
            ]
            final_pair_changes += sum(coarse[key] != fine[key] for key in keys)
    print(f"rows={len(rows)}")
    print(f"final_pair_decision_changes={final_pair_changes}")


if __name__ == "__main__":
    main()
