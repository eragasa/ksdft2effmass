#!/usr/bin/env python3
"""Create the execution-free periodic-2D finite-domain defect plan."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from ksdft2effmass.campaigns.research_monograph.impurity_defect_2d import (
    FiniteDomainEffectsCampaignPlanningWorkflow,
    FiniteDomainEffectsCaseInventoryJsonSerializer,
    FiniteDomainEffectsStudyDefinition,
)
from ksdft2effmass.solidstate import (
    BoundaryTwistMesh,
    FiniteLatticeShape,
    LatticeDimension,
)

EXECUTION_ID = "finite-domain-defect-planning-v1"
CALCULATION_FAMILY = "periodic2d-rank-defect"
type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)


def definition() -> FiniteDomainEffectsStudyDefinition:
    """Return the adopted execution-free finite-domain definition."""
    area_shapes = tuple(
        FiniteLatticeShape(LatticeDimension.TWO, (extent, extent))
        for extent in (6, 8, 10, 12, 16)
    )
    shape_shapes = tuple(
        FiniteLatticeShape(LatticeDimension.TWO, extents)
        for extents in ((8, 18), (9, 16), (12, 12), (16, 9), (18, 8))
    )
    return FiniteDomainEffectsStudyDefinition(
        identifier="research-monograph.impurity-defect-2d.finite-domain-effects.v1",
        area_shapes=area_shapes,
        shape_shapes=shape_shapes,
        orientation_shape_pairs=(
            (shape_shapes[0], shape_shapes[4]),
            (shape_shapes[1], shape_shapes[3]),
        ),
        defect_identifiers=(
            "directional_nearest_neighbor",
            "finite_range_diagonal_nonlocal",
        ),
        twist_mesh=BoundaryTwistMesh(LatticeDimension.TWO, (9, 9)),
        isotropic_parent_identifier="isotropic_lambda_0p5_0p5_0",
        orientation_source_parent_identifier="anisotropic_lambda_0p3_0p7_0",
        orientation_swapped_parent_identifier="anisotropic_lambda_0p7_0p3_0",
    )


def canonical_json(payload: dict[str, JsonValue]) -> bytes:
    """Encode one calculation-owned record deterministically."""
    return (
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode("utf-8")


def execute(output_root: Path) -> None:
    """Write one no-overwrite execution-free planning package."""
    output_root = output_root.resolve()
    temporary_root = output_root.with_name(f".{output_root.name}.incomplete")
    if output_root.exists() or temporary_root.exists():
        raise FileExistsError("refusing to overwrite a finite-domain planning package")

    study_definition = definition()
    plan = FiniteDomainEffectsCampaignPlanningWorkflow().execute(study_definition)
    serializer = FiniteDomainEffectsCaseInventoryJsonSerializer()
    definition_bytes = canonical_json(
        {
            "schema_version": 1,
            "record_type": "finite_domain_effects_study_definition",
            "execution_authorized_by_this_record": False,
            "definition": serializer.definition_payload(study_definition),
        }
    )
    plan_bytes = plan.serialized_plan
    script_bytes = Path(__file__).resolve().read_bytes()
    execution_bytes = canonical_json(
        {
            "schema_version": 1,
            "record_type": "finite_domain_effects_planning_execution",
            "calculation_family": CALCULATION_FAMILY,
            "execution_id": EXECUTION_ID,
            "outcome": "completed_execution_free_planning",
            "execution_status": "not_executed",
            "input_path": "inputs/definition.json",
            "input_sha256": hashlib.sha256(definition_bytes).hexdigest(),
            "result_path": "results/case-inventory.json",
            "result_sha256": hashlib.sha256(plan_bytes).hexdigest(),
            "planning_script_sha256": hashlib.sha256(script_bytes).hexdigest(),
            "isotropic_case_count": len(plan.inventory.isotropic_cases),
            "orientation_case_count": len(plan.inventory.orientation_cases),
            "proposed_operator_evaluation_count": (
                plan.inventory.operator_evaluation_count
            ),
            "claim_boundary": (
                "Execution-free deterministic case planning only. No operator was "
                "constructed, no accepted parent was read, and no calculation, "
                "convergence, material validation, uncertainty quantification, or "
                "protected external execution is authorized or reported."
            ),
        }
    )

    (temporary_root / "inputs").mkdir(parents=True)
    (temporary_root / "results").mkdir()
    (temporary_root / "inputs" / "definition.json").write_bytes(definition_bytes)
    (temporary_root / "results" / "case-inventory.json").write_bytes(plan_bytes)
    (temporary_root / "execution.json").write_bytes(execution_bytes)
    (temporary_root / "UNEXECUTED.md").write_text(
        "# Execution-free finite-domain defect plan\n\n"
        "This package records proposed cases only. No operator evaluation or protected "
        "calculation has been executed.\n",
        encoding="utf-8",
    )
    temporary_root.rename(output_root)


def main() -> None:
    """Parse the explicit output location and create the planning package."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, required=True)
    arguments = parser.parse_args()
    execute(arguments.output_root)


if __name__ == "__main__":
    main()
