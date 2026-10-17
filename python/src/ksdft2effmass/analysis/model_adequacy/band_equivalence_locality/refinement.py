"""Three-level refinement diagnostics for dimensional development replications."""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from .definitions import DevelopmentFamily
from .records import DevelopmentResult, PointDiagnostic
from .serialization import JsonValue, canonical_json_bytes


@dataclass(frozen=True, slots=True)
class DevelopmentRefinementPair:
    """Retain changes across one adjacent mesh-doubling pair."""

    coarse_construction_size: int
    fine_construction_size: int
    maximum_parent_diagnostic_change: float
    maximum_final_parent_invariant_change: float
    maximum_correlation_change: float
    maximum_threshold_change: float
    maximum_hopping_weight_change: float
    maximum_hopping_block_power_change: float
    maximum_angle_change: float
    maximum_band_defect: float
    maximum_reconstruction_defect: float
    maximum_parseval_defect: float
    maximum_final_outcome_change: int | None
    first_passing_dispositions_stable: bool
    shared_mesh_quantities_applicable: bool
    shared_mesh_inapplicable_reason: str
    maximum_shared_parent_eigenvalue_defect: float | None
    maximum_shared_projector_defect: float | None
    within_draft_tolerances: bool | None
    tolerance_disposition_reason: str


@dataclass(frozen=True, slots=True)
class DevelopmentRefinementAssessment:
    """Retain a conservative three-level family refinement assessment."""

    family: DevelopmentFamily
    source_result_sha256: tuple[str, ...]
    refinements: tuple[DevelopmentRefinementPair, ...]
    required_stable_refinements: int
    momentum_disposition: str
    momentum_disposition_reason: str
    passes_draft_tolerance: bool | None
    passes_unit_scale_draft_tolerance: bool | None
    tolerance_inapplicable_reason: str
    paper1_literal_range_endpoints_applicable: bool
    paper1_literal_range_endpoints_inapplicable_reason: str


def _maximum_change(coarse: tuple[float, ...], fine: tuple[float, ...]) -> float:
    if len(coarse) != len(fine):
        raise ValueError("refinement diagnostic inventories differ")
    return max(
        (abs(left - right) for left, right in zip(coarse, fine, strict=True)),
        default=0.0,
    )


def _periodic_angle_change(left: float, right: float) -> float:
    return abs((left - right + 0.5 * math.pi) % math.pi - 0.5 * math.pi)


def _parent_diagnostics(point: PointDiagnostic) -> tuple[float, ...]:
    return (
        point.minimum_sampled_external_gap,
        point.continuous_external_gap_lower_bound,
        point.minimum_seed_overlap,
        point.maximum_parent_hermiticity_defect,
        point.maximum_eigensystem_reconstruction_defect,
        point.maximum_frame_orthonormality_defect,
        point.maximum_projector_reconstruction_defect,
        point.maximum_parent_retained_reconstruction_defect,
        point.maximum_parent_fourier_reconstruction_defect,
        point.maximum_periodic_frame_closure_defect,
        point.minimum_sampled_transport_singular_value,
        point.maximum_transport_procrustes_residual,
        point.maximum_transport_unitarity_defect,
        point.maximum_closure_holonomy_unitarity_defect,
        point.maximum_plaquette_holonomy_phase,
    )


def _invariant_diagnostics(point: PointDiagnostic) -> tuple[float, ...]:
    return (
        point.minimum_sampled_external_gap,
        point.continuous_external_gap_lower_bound,
        point.minimum_seed_overlap,
    )


def _reconstruction_diagnostics(point: PointDiagnostic) -> tuple[float, ...]:
    return (
        point.maximum_eigensystem_reconstruction_defect,
        point.maximum_projector_reconstruction_defect,
        point.maximum_parent_retained_reconstruction_defect,
        point.maximum_parent_fourier_reconstruction_defect,
        point.reference_fourier_reconstruction_defect,
        point.comparison_fourier_reconstruction_defect,
    )


def _point_pair_changes(
    coarse: PointDiagnostic, fine: PointDiagnostic
) -> dict[str, float]:
    if (coarse.parent_scale, coarse.amplitude) != (fine.parent_scale, fine.amplitude):
        raise ValueError("refinement point identities differ")
    correlations = 0.0
    if (
        coarse.finite_mesh_maximum_correlation is not None
        and fine.finite_mesh_maximum_correlation is not None
    ):
        correlations = abs(
            coarse.finite_mesh_maximum_correlation
            - fine.finite_mesh_maximum_correlation
        )
    angles = 0.0
    if (
        coarse.restricted_global_rotation_angle is not None
        and fine.restricted_global_rotation_angle is not None
    ):
        angles = _periodic_angle_change(
            coarse.restricted_global_rotation_angle,
            fine.restricted_global_rotation_angle,
        )
    coarse_shells = {shell.shell_index: shell for shell in coarse.shell_diagnostics}
    fine_shells = {shell.shell_index: shell for shell in fine.shell_diagnostics}
    common_shells = sorted(coarse_shells.keys() & fine_shells.keys())
    block_change = max(
        (
            max(
                abs(
                    coarse_shells[index].reference_shell_power
                    - fine_shells[index].reference_shell_power
                ),
                abs(
                    coarse_shells[index].comparison_shell_power
                    - fine_shells[index].comparison_shell_power
                ),
            )
            for index in common_shells
        ),
        default=0.0,
    )
    return {
        "parent": _maximum_change(
            _parent_diagnostics(coarse), _parent_diagnostics(fine)
        ),
        "invariant": _maximum_change(
            _invariant_diagnostics(coarse), _invariant_diagnostics(fine)
        ),
        "correlation": correlations,
        "threshold": max(
            abs(coarse.minimum_operator_threshold - fine.minimum_operator_threshold),
            abs(
                coarse.exact_spectrum_joint_operator_threshold
                - fine.exact_spectrum_joint_operator_threshold
            ),
        ),
        "hopping": max(
            abs(coarse.reference_nononsite_power - fine.reference_nononsite_power),
            abs(coarse.comparison_nononsite_power - fine.comparison_nononsite_power),
        ),
        "block": block_change,
        "angle": angles,
        "band": abs(
            coarse.maximum_direct_band_defect - fine.maximum_direct_band_defect
        ),
        "reconstruction": _maximum_change(
            _reconstruction_diagnostics(coarse), _reconstruction_diagnostics(fine)
        ),
        "parseval": max(
            abs(coarse.reference_parseval_defect - fine.reference_parseval_defect),
            abs(coarse.comparison_parseval_defect - fine.comparison_parseval_defect),
        ),
    }


def _decision_changes(
    coarse: PointDiagnostic, fine: PointDiagnostic
) -> tuple[bool, int | None]:
    if len(coarse.first_passing) != len(fine.first_passing):
        raise ValueError("refinement decision inventories differ")
    stable = True
    changes: list[int] = []
    for left, right in zip(coarse.first_passing, fine.first_passing, strict=True):
        if left.tolerance != right.tolerance:
            raise ValueError("refinement tolerances differ")
        for coarse_shell, fine_shell in (
            (left.reference_band_shell, right.reference_band_shell),
            (left.comparison_band_shell, right.comparison_band_shell),
            (left.reference_hamiltonian_shell, right.reference_hamiltonian_shell),
            (left.comparison_hamiltonian_shell, right.comparison_hamiltonian_shell),
        ):
            stable = stable and coarse_shell == fine_shell
            if coarse_shell is not None and fine_shell is not None:
                changes.append(abs(coarse_shell - fine_shell))
    return stable, max(changes) if changes else None


class DevelopmentRefinementAnalyzer:
    """Compare three mesh levels without inventing convergence tolerances."""

    __slots__ = ()

    def execute(
        self,
        results: tuple[DevelopmentResult, ...],
        source_result_sha256: tuple[str, ...],
    ) -> DevelopmentRefinementAssessment:
        if type(results) is not tuple or len(results) < 3:
            raise ValueError("results must contain at least three mesh levels")
        if type(source_result_sha256) is not tuple or len(source_result_sha256) != len(
            results
        ):
            raise ValueError("one source result hash is required per mesh level")
        family = results[0].family
        if any(result.family is not family for result in results):
            raise ValueError("all refinement results must belong to one family")
        sizes = tuple(result.construction_size for result in results)
        if any(
            fine != 2 * coarse
            for coarse, fine in zip(sizes[:-1], sizes[1:], strict=True)
        ):
            raise ValueError("construction sizes must form a doubling ladder")
        pairs: list[DevelopmentRefinementPair] = []
        for coarse_result, fine_result in zip(results[:-1], results[1:], strict=True):
            changes: list[dict[str, float]] = []
            decision_stability: list[bool] = []
            decision_changes: list[int] = []
            for coarse_case, fine_case in zip(
                coarse_result.cases, fine_result.cases, strict=True
            ):
                if coarse_case.name != fine_case.name:
                    raise ValueError("refinement case identities differ")
                for coarse_point, fine_point in zip(
                    coarse_case.points, fine_case.points, strict=True
                ):
                    changes.append(_point_pair_changes(coarse_point, fine_point))
                    stable, maximum_change = _decision_changes(coarse_point, fine_point)
                    decision_stability.append(stable)
                    if maximum_change is not None:
                        decision_changes.append(maximum_change)
            maxima = {
                name: max((change[name] for change in changes), default=0.0)
                for name in (
                    "parent",
                    "invariant",
                    "correlation",
                    "threshold",
                    "hopping",
                    "block",
                    "angle",
                    "band",
                    "reconstruction",
                    "parseval",
                )
            }
            pairs.append(
                DevelopmentRefinementPair(
                    coarse_construction_size=coarse_result.construction_size,
                    fine_construction_size=fine_result.construction_size,
                    maximum_parent_diagnostic_change=maxima["parent"],
                    maximum_final_parent_invariant_change=maxima["invariant"],
                    maximum_correlation_change=maxima["correlation"],
                    maximum_threshold_change=maxima["threshold"],
                    maximum_hopping_weight_change=maxima["hopping"],
                    maximum_hopping_block_power_change=maxima["block"],
                    maximum_angle_change=maxima["angle"],
                    maximum_band_defect=maxima["band"],
                    maximum_reconstruction_defect=maxima["reconstruction"],
                    maximum_parseval_defect=maxima["parseval"],
                    maximum_final_outcome_change=(
                        max(decision_changes) if decision_changes else None
                    ),
                    first_passing_dispositions_stable=all(decision_stability),
                    shared_mesh_quantities_applicable=False,
                    shared_mesh_inapplicable_reason=(
                        "half-step Monkhorst--Pack doubling meshes have no "
                        "shared nodes; "
                        "shared-node eigenvalue and projector defects are inapplicable"
                    ),
                    maximum_shared_parent_eigenvalue_defect=None,
                    maximum_shared_projector_defect=None,
                    within_draft_tolerances=None,
                    tolerance_disposition_reason=(
                        "channel-specific refinement tolerances were not prospectively "
                        "frozen for these replaceable development actions"
                    ),
                )
            )
        return DevelopmentRefinementAssessment(
            family=family,
            source_result_sha256=source_result_sha256,
            refinements=tuple(pairs),
            required_stable_refinements=2,
            momentum_disposition="unresolved",
            momentum_disposition_reason=(
                "three levels are available, but catalog-wide channel tolerances were "
                "not prospectively frozen"
            ),
            passes_draft_tolerance=None,
            passes_unit_scale_draft_tolerance=None,
            tolerance_inapplicable_reason=(
                "Paper 2 family-owned alignment and refinement tolerances were not "
                "prospectively frozen; Paper 1 tolerances are not transferred"
            ),
            paper1_literal_range_endpoints_applicable=False,
            paper1_literal_range_endpoints_inapplicable_reason=(
                "Paper 1 ranges 0, 8, and 16 are one-dimensional absolute-displacement "
                "cutoffs; Paper 2 uses geometry-owned complete physical-metric shells"
            ),
        )


def refinement_schema_id(family: DevelopmentFamily) -> str:
    """Return the family-bound refinement-assessment schema identity."""
    if type(family) is not DevelopmentFamily:
        raise TypeError("family must be DevelopmentFamily")
    return f"{family.value}.development.refinement-assessment.v0"


def development_refinement_document(
    value: DevelopmentRefinementAssessment,
) -> dict[str, JsonValue]:
    """Serialize one conservative refinement assessment."""
    return {
        "family": value.family.value,
        "momentum_disposition": value.momentum_disposition,
        "momentum_disposition_reason": value.momentum_disposition_reason,
        "paper1_literal_range_endpoints_applicable": (
            value.paper1_literal_range_endpoints_applicable
        ),
        "paper1_literal_range_endpoints_inapplicable_reason": (
            value.paper1_literal_range_endpoints_inapplicable_reason
        ),
        "passes_draft_tolerance": value.passes_draft_tolerance,
        "passes_unit_scale_draft_tolerance": (value.passes_unit_scale_draft_tolerance),
        "refinements": [
            {
                "coarse_construction_size": item.coarse_construction_size,
                "fine_construction_size": item.fine_construction_size,
                "first_passing_dispositions_stable": (
                    item.first_passing_dispositions_stable
                ),
                "maximum_angle_change": item.maximum_angle_change,
                "maximum_band_defect": item.maximum_band_defect,
                "maximum_correlation_change": item.maximum_correlation_change,
                "maximum_final_outcome_change": item.maximum_final_outcome_change,
                "maximum_final_parent_invariant_change": (
                    item.maximum_final_parent_invariant_change
                ),
                "maximum_hopping_block_power_change": (
                    item.maximum_hopping_block_power_change
                ),
                "maximum_hopping_weight_change": item.maximum_hopping_weight_change,
                "maximum_parent_diagnostic_change": (
                    item.maximum_parent_diagnostic_change
                ),
                "maximum_parseval_defect": item.maximum_parseval_defect,
                "maximum_reconstruction_defect": item.maximum_reconstruction_defect,
                "maximum_shared_parent_eigenvalue_defect": (
                    item.maximum_shared_parent_eigenvalue_defect
                ),
                "maximum_shared_projector_defect": item.maximum_shared_projector_defect,
                "maximum_threshold_change": item.maximum_threshold_change,
                "shared_mesh_inapplicable_reason": item.shared_mesh_inapplicable_reason,
                "shared_mesh_quantities_applicable": (
                    item.shared_mesh_quantities_applicable
                ),
                "tolerance_disposition_reason": item.tolerance_disposition_reason,
                "within_draft_tolerances": item.within_draft_tolerances,
            }
            for item in value.refinements
        ],
        "required_stable_refinements": value.required_stable_refinements,
        "schema": refinement_schema_id(value.family),
        "source_result_sha256": list(value.source_result_sha256),
        "status": "replaceable-development-refinement-not-scientific-evidence",
        "tolerance_inapplicable_reason": value.tolerance_inapplicable_reason,
    }


def development_refinement_schema(family: DevelopmentFamily) -> dict[str, JsonValue]:
    """Return a strict schema for one family refinement assessment."""
    if type(family) is not DevelopmentFamily:
        raise TypeError("family must be DevelopmentFamily")
    nonnegative: dict[str, JsonValue] = {
        name: {"minimum": 0.0, "type": "number"}
        for name in (
            "maximum_angle_change",
            "maximum_band_defect",
            "maximum_correlation_change",
            "maximum_final_parent_invariant_change",
            "maximum_hopping_block_power_change",
            "maximum_hopping_weight_change",
            "maximum_parent_diagnostic_change",
            "maximum_parseval_defect",
            "maximum_reconstruction_defect",
            "maximum_threshold_change",
        )
    }
    properties: dict[str, JsonValue] = {
        "coarse_construction_size": {"minimum": 4, "type": "integer"},
        "fine_construction_size": {"minimum": 8, "type": "integer"},
        "first_passing_dispositions_stable": {"type": "boolean"},
        **nonnegative,
        "maximum_final_outcome_change": {"type": ["integer", "null"]},
        "maximum_shared_parent_eigenvalue_defect": {"type": ["number", "null"]},
        "maximum_shared_projector_defect": {"type": ["number", "null"]},
        "shared_mesh_inapplicable_reason": {"minLength": 1, "type": "string"},
        "shared_mesh_quantities_applicable": {"type": "boolean"},
        "tolerance_disposition_reason": {"minLength": 1, "type": "string"},
        "within_draft_tolerances": {"type": ["boolean", "null"]},
    }
    pair_required: list[JsonValue] = []
    pair_required.extend(sorted(properties))
    pair: dict[str, JsonValue] = {
        "additionalProperties": False,
        "properties": properties,
        "required": pair_required,
        "type": "object",
    }
    root_properties: dict[str, JsonValue] = {
        "family": {"const": family.value},
        "momentum_disposition": {"const": "unresolved"},
        "momentum_disposition_reason": {"minLength": 1, "type": "string"},
        "paper1_literal_range_endpoints_applicable": {"const": False},
        "paper1_literal_range_endpoints_inapplicable_reason": {
            "minLength": 1,
            "type": "string",
        },
        "passes_draft_tolerance": {"type": ["boolean", "null"]},
        "passes_unit_scale_draft_tolerance": {"type": ["boolean", "null"]},
        "refinements": {"items": pair, "minItems": 2, "type": "array"},
        "required_stable_refinements": {"const": 2},
        "schema": {"const": refinement_schema_id(family)},
        "source_result_sha256": {
            "items": {"pattern": "^[0-9a-f]{64}$", "type": "string"},
            "minItems": 3,
            "type": "array",
        },
        "status": {
            "const": "replaceable-development-refinement-not-scientific-evidence"
        },
        "tolerance_inapplicable_reason": {"minLength": 1, "type": "string"},
    }
    root_required: list[JsonValue] = []
    root_required.extend(sorted(root_properties))
    return {
        "$id": refinement_schema_id(family),
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "additionalProperties": False,
        "properties": root_properties,
        "required": root_required,
        "type": "object",
    }


def write_development_refinement_assessment(
    directory: Path, assessment: DevelopmentRefinementAssessment
) -> tuple[Path, Path]:
    """Write one assessment and its strict family-bound schema."""
    if not isinstance(directory, Path):
        raise TypeError("directory must be pathlib.Path")
    directory.mkdir(parents=True, exist_ok=True)
    document_path = directory / "development-refinement-assessment.json"
    schema_path = directory / "development-refinement-assessment.schema.json"
    document_path.write_bytes(
        canonical_json_bytes(development_refinement_document(assessment))
    )
    schema_path.write_bytes(
        canonical_json_bytes(development_refinement_schema(assessment.family))
    )
    return document_path, schema_path


__all__ = [
    "DevelopmentRefinementAnalyzer",
    "DevelopmentRefinementAssessment",
    "DevelopmentRefinementPair",
    "development_refinement_document",
    "development_refinement_schema",
    "write_development_refinement_assessment",
]
