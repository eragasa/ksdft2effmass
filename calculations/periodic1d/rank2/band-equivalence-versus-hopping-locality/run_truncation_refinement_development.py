"""Evaluate dense-cutoff decision stability across momentum refinements."""

from __future__ import annotations

import csv
import math
from pathlib import Path

from development_study import (
    completed_truncation,
    truncation_analysis,
    truncation_verification_defect,
)
from ksdft2effmass.periodic1d import (
    Periodic1DEmbeddedSubspaceRank2TruncationToleranceSelector,
)
from ksdft2effmass.real_space_support_truncation import (
    MinimumToleranceSatisfyingSupport,
    RealSpaceSupportTruncationToleranceSelection,
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


def _selection_fields(
    selection: RealSpaceSupportTruncationToleranceSelection,
) -> dict[str, str]:
    output: dict[str, str] = {}
    # Prefixes below are immutable historical CSV labels only.
    outcomes = (
        (
            "reference_band",
            selection.reference_model.ordered_eigenvalue_maximum_absolute_error,
        ),
        (
            "comparison_band",
            selection.comparison_model.ordered_eigenvalue_maximum_absolute_error,
        ),
        (
            "reference_hamiltonian",
            selection.reference_model.matrix_frobenius_maximum_error,
        ),
        (
            "comparison_hamiltonian",
            selection.comparison_model.matrix_frobenius_maximum_error,
        ),
    )
    for channel, outcome in outcomes:
        if type(outcome) is not MinimumToleranceSatisfyingSupport:
            raise ValueError(f"{channel} does not pass within the dense cutoff cap")
        output[f"{channel}_first_passing_range"] = str(outcome.comparison_index)
        output[f"{channel}_passing_error"] = _number(outcome.satisfying_error)
        output[f"{channel}_preceding_error"] = (
            "not-applicable"
            if outcome.preceding_error is None
            else _number(outcome.preceding_error)
        )
    return output


def main() -> None:
    """Write independently verified support-tolerance refinement decisions."""
    rows: list[dict[str, str]] = []
    for parent_scale in PARENT_HOPPING_SCALES:
        for mesh_size in MOMENTUM_MESHES:
            print(
                f"parent_hopping_scale={parent_scale:g}, N={mesh_size}: start",
                flush=True,
            )
            evaluation_mesh_size = 4 * mesh_size + 1
            result = completed_truncation(
                truncation_analysis(
                    construction_mesh_size=mesh_size,
                    evaluation_mesh_size=evaluation_mesh_size,
                    amplitudes=_amplitudes(),
                    parent_hopping_scale=parent_scale,
                    maximum_range=MAXIMUM_RANGE,
                )
            )
            verification_discrepancy = truncation_verification_defect(result)
            for point in result.points:
                selection = Periodic1DEmbeddedSubspaceRank2TruncationToleranceSelector(
                    point=point,
                    tolerance=DECISION_TOLERANCE,
                ).execute()
                row = {
                    "parent_hopping_scale": _number(parent_scale),
                    "amplitude": _number(point.amplitude),
                    "construction_mesh_size": str(mesh_size),
                    "evaluation_mesh_size": str(evaluation_mesh_size),
                    "decision_tolerance": _number(DECISION_TOLERANCE),
                    "verification_discrepancy": _number(verification_discrepancy),
                }
                row.update(_selection_fields(selection))
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
