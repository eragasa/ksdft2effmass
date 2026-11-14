#!/usr/bin/env python3
"""Calculate one authored synthetic defect-2D folding/null-control execution."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from projectkoios.physkit.units import Unitless

from ksdft2effmass.campaigns.research_monograph.impurity_defect_2d import (
    FoldingNullAlignmentAttack,
    FoldingNullCalculationWorkflow,
    FoldingNullCase,
    FoldingNullStudyDefinition,
    FoldingNullTolerances,
)
from ksdft2effmass.solidstate import (
    BoundaryTwistLift,
    FiniteLatticeShape,
    LatticeDimension,
    LatticeDisplacement,
    ScalarHoppingModel,
    ScalarHoppingTerm,
)

EXECUTION_ID = "folding-null-controls-v1"
CALCULATION_FAMILY = "periodic2d-rank-defect"
type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


def definition() -> FoldingNullStudyDefinition:
    """Return the adopted authored folding and null-alignment definition."""
    terms = tuple(
        ScalarHoppingTerm(
            LatticeDisplacement(LatticeDimension.TWO, displacement),
            real,
            0.0,
        )
        for displacement, real in (
            ((-1, 0), -0.10),
            ((0, -1), -0.08),
            ((0, 0), 0.20),
            ((0, 1), -0.08),
            ((1, 0), -0.10),
        )
    )
    parent = ScalarHoppingModel(
        identifier="authored-folding-null-parent",
        dimension=LatticeDimension.TWO,
        terms=terms,
        energy_unit=Unitless(),
        energy_reference="authored-folding-null-zero",
        basis_identifier="scalar-cell-basis",
    )
    cases = tuple(
        FoldingNullCase(
            identifier=f"shape-{extent}.twist-{twist_index}",
            shape=FiniteLatticeShape(LatticeDimension.TWO, (extent, extent)),
            twist=BoundaryTwistLift(LatticeDimension.TWO, twist),
        )
        for extent in (6, 8)
        for twist_index, twist in enumerate(
            ((0.0, 0.0), (0.37, -0.23), (0.5, 0.0), (0.0, 0.5))
        )
    )
    return FoldingNullStudyDefinition(
        identifier="periodic2d-rank-defect.folding-null-controls.v1",
        parent=parent,
        cases=cases,
        null_attack=FoldingNullAlignmentAttack(
            translation_cells=(1, 1),
            site_phase_steps_radians=(0.137, -0.191),
            energy_reference_shift=0.137,
        ),
        tolerances=FoldingNullTolerances(1.0e-11, 1.0e-11),
    )


def canonical_json(payload: dict[str, JsonValue]) -> bytes:
    """Encode one calculation-owned record deterministically."""
    return (
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode("utf-8")


def execute(output_root: Path) -> None:
    """Write one no-overwrite authored folding/null-control calculation package."""
    output_root = output_root.resolve()
    temporary_root = output_root.with_name(f".{output_root.name}.incomplete")
    if output_root.exists() or temporary_root.exists():
        raise FileExistsError(
            "refusing to overwrite an authored folding/null-control execution"
        )
    calculation = FoldingNullCalculationWorkflow().execute(definition())
    result = calculation.result
    result_bytes = calculation.serialized_result
    script_bytes = Path(__file__).resolve().read_bytes()
    execution_bytes = canonical_json(
        {
            "schema_version": 1,
            "record_type": "periodic2d_rank_defect_folding_null_execution",
            "calculation_family": CALCULATION_FAMILY,
            "execution_id": EXECUTION_ID,
            "outcome": "completed",
            "evidence_status": "calculated_synthetic_result_unsealed",
            "external_execution": False,
            "accepted_parent_read": False,
            "definition_location": "embedded_in_results/result.json",
            "result_path": "results/result.json",
            "result_sha256": hashlib.sha256(result_bytes).hexdigest(),
            "calculation_script_sha256": hashlib.sha256(script_bytes).hexdigest(),
            "case_count": len(result.cases),
            "criterion_status": "pass" if result.passes else "fail",
            "failed_criteria": list(result.failed_criteria),
            "claim_boundary": (
                "Authored dimensionless scalar synthetic folding and known-map null "
                "extraction only. No accepted parent, material model, external "
                "calculator, convergence conclusion, uncertainty quantification, or "
                "protected execution is included."
            ),
        }
    )
    (temporary_root / "results").mkdir(parents=True)
    (temporary_root / "results" / "result.json").write_bytes(result_bytes)
    (temporary_root / "execution.json").write_bytes(execution_bytes)
    (temporary_root / "UNSEALED.md").write_text(
        "# Authored Folding and Null-Alignment Controls execution\n\n"
        "CALCULATED SYNTHETIC RESULT — UNSEALED. This is software and bounded "
        "numerical-verification evidence only.\n",
        encoding="utf-8",
    )
    temporary_root.rename(output_root)


def main() -> None:
    """Parse the explicit output location and calculate the authored package."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, required=True)
    arguments = parser.parse_args()
    execute(arguments.output_root)


if __name__ == "__main__":
    main()
