"""Strict family-bound schemas for bounded development documents."""

from __future__ import annotations

from pathlib import Path

from .definitions import TRANSPORT_RANK_DEFICIENT_REASON, BandEquivalenceLocalityFamily
from .serialization import (
    JsonValue,
    band_equivalence_locality_schema_id,
    canonical_json_bytes,
    refinement_schema_id,
)


def _number(*, minimum: float | None = None) -> dict[str, JsonValue]:
    schema: dict[str, JsonValue] = {"type": "number"}
    if minimum is not None:
        schema["minimum"] = minimum
    return schema


def _nullable_number(*, minimum: float | None = None) -> dict[str, JsonValue]:
    schema: dict[str, JsonValue] = {"type": ["number", "null"]}
    if minimum is not None:
        schema["minimum"] = minimum
    return schema


def _nullable_integer() -> dict[str, JsonValue]:
    return {"type": ["integer", "null"]}


def _strict_object(
    properties: dict[str, JsonValue], required: tuple[str, ...]
) -> dict[str, JsonValue]:
    return {
        "additionalProperties": False,
        "properties": properties,
        "required": list(required),
        "type": "object",
    }


def _fixed_number_vector(length: int) -> dict[str, JsonValue]:
    return {
        "items": {"type": "number"},
        "maxItems": length,
        "minItems": length,
        "type": "array",
    }


def _fixed_integer_vector(length: int) -> dict[str, JsonValue]:
    return {
        "items": {"type": "integer"},
        "maxItems": length,
        "minItems": length,
        "type": "array",
    }


def band_equivalence_locality_request_schema(
    family: BandEquivalenceLocalityFamily,
) -> dict[str, JsonValue]:
    """Return the strict input schema for one experiment family."""
    if type(family) is not BandEquivalenceLocalityFamily:
        raise TypeError("family must be BandEquivalenceLocalityFamily")
    vector: dict[str, JsonValue] = {
        "items": {"type": "number"},
        "type": "array",
    }
    integer_vector: dict[str, JsonValue] = {
        "items": {"type": "integer"},
        "type": "array",
    }
    case = _strict_object(
        {
            "basis_offsets": {"items": vector, "type": "array"},
            "dimension": {"enum": [2, 3], "type": "integer"},
            "direct_lattice_primitive_basis_rows": {
                "items": vector,
                "type": "array",
            },
            "direct_lattice_primitive_vector_axis": {"const": "columns"},
            "gauge_normalization": {
                "enum": ["axis-maximum", "bond-rms"],
                "type": "string",
            },
            "name": {"minLength": 1, "type": "string"},
            "parent_kind": {
                "enum": [
                    "bipartite-inspired",
                    "directed-axis",
                    "hermitian-bravais",
                ],
                "type": "string",
            },
            "positive_bonds": {
                "items": integer_vector,
                "minItems": 1,
                "type": "array",
            },
            "shell_metric_scale": {"exclusiveMinimum": 0.0, "type": "number"},
        },
        (
            "basis_offsets",
            "dimension",
            "direct_lattice_primitive_basis_rows",
            "direct_lattice_primitive_vector_axis",
            "gauge_normalization",
            "name",
            "parent_kind",
            "positive_bonds",
            "shell_metric_scale",
        ),
    )
    case["allOf"] = [
        {
            "if": {
                "properties": {"dimension": {"const": dimension}},
                "required": ["dimension"],
            },
            "then": {
                "properties": {
                    "basis_offsets": {
                        "items": _fixed_number_vector(dimension),
                        "type": "array",
                    },
                    "direct_lattice_primitive_basis_rows": {
                        "items": _fixed_number_vector(dimension),
                        "maxItems": dimension,
                        "minItems": dimension,
                        "type": "array",
                    },
                    "positive_bonds": {
                        "items": _fixed_integer_vector(dimension),
                        "minItems": 1,
                        "type": "array",
                    },
                }
            },
        }
        for dimension in (2, 3)
    ]
    schema_id = band_equivalence_locality_schema_id(family, "input")
    return {
        "$id": schema_id,
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        **_strict_object(
            {
                "amplitude_resolution_intervals": {
                    "items": {"minimum": 1, "type": "integer"},
                    "minItems": 1,
                    "type": "array",
                    "uniqueItems": True,
                },
                "amplitudes": {
                    "items": _number(minimum=0.0),
                    "minItems": 1,
                    "type": "array",
                    "uniqueItems": True,
                },
                "band_tolerances": {
                    "items": {"exclusiveMinimum": 0.0, "type": "number"},
                    "minItems": 1,
                    "type": "array",
                    "uniqueItems": True,
                },
                "cases": {"items": case, "minItems": 1, "type": "array"},
                "construction_size": {"minimum": 4, "type": "integer"},
                "evaluation_shift": {
                    "exclusiveMaximum": 1.0,
                    "exclusiveMinimum": 0.0,
                    "type": "number",
                },
                "evaluation_size": {"minimum": 3, "type": "integer"},
                "family": {"const": family.value},
                "parent_scales": {
                    "items": {"maximum": 1.0, "minimum": 0.0, "type": "number"},
                    "minItems": 1,
                    "type": "array",
                    "uniqueItems": True,
                },
                "schema": {"const": schema_id},
                "shell_cap": {"minimum": 0, "type": "integer"},
                "status": {"const": "bounded-development-smoke-input"},
                "transport_rank_absolute": {
                    "exclusiveMinimum": 0.0,
                    "type": "number",
                },
                "transport_rank_relative": {
                    "exclusiveMinimum": 0.0,
                    "type": "number",
                },
            },
            (
                "amplitude_resolution_intervals",
                "amplitudes",
                "band_tolerances",
                "cases",
                "construction_size",
                "evaluation_shift",
                "evaluation_size",
                "family",
                "parent_scales",
                "schema",
                "shell_cap",
                "status",
                "transport_rank_absolute",
                "transport_rank_relative",
            ),
        ),
    }


def _error_channels_schema() -> dict[str, JsonValue]:
    fields = (
        "maximum_band",
        "maximum_hamiltonian",
        "rms_band",
        "rms_hamiltonian",
    )
    return _strict_object({name: _number(minimum=0.0) for name in fields}, fields)


def band_equivalence_locality_result_schema(
    family: BandEquivalenceLocalityFamily,
) -> dict[str, JsonValue]:
    """Return the strict result schema for one experiment family."""
    if type(family) is not BandEquivalenceLocalityFamily:
        raise TypeError("family must be BandEquivalenceLocalityFamily")
    errors = _error_channels_schema()
    decision_fields = (
        "comparison_band_passing_error",
        "comparison_band_preceding_error",
        "comparison_band_shell",
        "comparison_hamiltonian_passing_error",
        "comparison_hamiltonian_preceding_error",
        "comparison_hamiltonian_shell",
        "reference_band_passing_error",
        "reference_band_preceding_error",
        "reference_band_shell",
        "reference_hamiltonian_passing_error",
        "reference_hamiltonian_preceding_error",
        "reference_hamiltonian_shell",
        "tolerance",
    )
    decision = _strict_object(
        {
            "comparison_band_passing_error": _nullable_number(minimum=0.0),
            "comparison_band_preceding_error": _nullable_number(minimum=0.0),
            "comparison_band_shell": _nullable_integer(),
            "comparison_hamiltonian_passing_error": _nullable_number(minimum=0.0),
            "comparison_hamiltonian_preceding_error": _nullable_number(minimum=0.0),
            "comparison_hamiltonian_shell": _nullable_integer(),
            "reference_band_passing_error": _nullable_number(minimum=0.0),
            "reference_band_preceding_error": _nullable_number(minimum=0.0),
            "reference_band_shell": _nullable_integer(),
            "reference_hamiltonian_passing_error": _nullable_number(minimum=0.0),
            "reference_hamiltonian_preceding_error": _nullable_number(minimum=0.0),
            "reference_hamiltonian_shell": _nullable_integer(),
            "tolerance": {"exclusiveMinimum": 0.0, "type": "number"},
        },
        decision_fields,
    )
    shell_fields = (
        "comparison_omitted_power",
        "comparison_shell_power",
        "comparison_total",
        "comparison_total_omitted_power",
        "comparison_truncation",
        "comparison_truncation_parseval_defect",
        "reference_omitted_power",
        "reference_shell_power",
        "reference_total",
        "reference_total_omitted_power",
        "reference_truncation",
        "reference_truncation_parseval_defect",
        "retained_blocks",
        "shell_index",
    )
    shell = _strict_object(
        {
            "comparison_omitted_power": _number(minimum=0.0),
            "comparison_shell_power": _number(minimum=0.0),
            "comparison_total": errors,
            "comparison_total_omitted_power": _number(minimum=0.0),
            "comparison_truncation": errors,
            "comparison_truncation_parseval_defect": _number(minimum=0.0),
            "reference_omitted_power": _number(minimum=0.0),
            "reference_shell_power": _number(minimum=0.0),
            "reference_total": errors,
            "reference_total_omitted_power": _number(minimum=0.0),
            "reference_truncation": errors,
            "reference_truncation_parseval_defect": _number(minimum=0.0),
            "retained_blocks": {"minimum": 1, "type": "integer"},
            "shell_index": {"minimum": 0, "type": "integer"},
        },
        shell_fields,
    )
    nonnegative_fields = (
        "comparison_fourier_reconstruction_defect",
        "comparison_nononsite_power",
        "comparison_nyquist_power",
        "comparison_onsite_power",
        "comparison_ordinary_hermiticity_defect",
        "comparison_parseval_defect",
        "comparison_total_power",
        "comparison_twisted_nyquist_defect",
        "continuous_external_gap_lower_bound",
        "exact_spectrum_joint_operator_threshold",
        "maximum_covariant_defect",
        "maximum_direct_band_defect",
        "maximum_eigensystem_reconstruction_defect",
        "maximum_frame_orthonormality_defect",
        "maximum_parent_fourier_reconstruction_defect",
        "maximum_parent_hermiticity_defect",
        "maximum_parent_retained_reconstruction_defect",
        "maximum_periodic_frame_closure_defect",
        "maximum_projector_reconstruction_defect",
        "maximum_transport_procrustes_residual",
        "maximum_transport_squared_residual_roundoff_cutoff",
        "maximum_transport_rank_cutoff",
        "maximum_transport_unitarity_defect",
        "minimum_operator_threshold",
        "minimum_sampled_external_gap",
        "minimum_sampled_transport_singular_value",
        "minimum_seed_overlap",
        "reference_fourier_reconstruction_defect",
        "reference_nononsite_power",
        "reference_nyquist_power",
        "reference_onsite_power",
        "reference_ordinary_hermiticity_defect",
        "reference_parseval_defect",
        "reference_total_power",
        "reference_twisted_nyquist_defect",
        "restricted_global_rotation_residual",
        "splitting_scale",
    )
    point_properties: dict[str, JsonValue] = {
        name: _number(minimum=0.0) for name in nonnegative_fields
    }
    point_properties.update(
        {
            "alignment_applicable": {"type": "boolean"},
            "alignment_inapplicable_reason": {"type": ["string", "null"]},
            "amplitude": _number(minimum=0.0),
            "analytic_correlation_remainder_bound": _nullable_number(),
            "analytic_flat_correlation": _nullable_number(),
            "basis_distance_maximum": _nullable_number(),
            "basis_distance_minimum": _nullable_number(),
            "comparison_interpolation": errors,
            "correlation_quadrature_defect": _nullable_number(),
            "exact_spectrum_joint_threshold_over_sqrt_splitting": (
                _nullable_number(minimum=0.0)
            ),
            "excess_nonzero_hopping_weight": _number(),
            "finite_mesh_maximum_correlation": _nullable_number(),
            "flat_identity_departure": _nullable_number(),
            "flat_residual_tail_identity_defect": _nullable_number(),
            "first_passing": {"items": decision, "minItems": 1, "type": "array"},
            "maximum_absolute_closure_holonomy_phases": {
                "anyOf": [
                    {
                        "items": _number(minimum=0.0),
                        "maxItems": 2,
                        "minItems": 2,
                        "type": "array",
                    },
                    {"type": "null"},
                ]
            },
            "maximum_closure_holonomy_unitarity_defect": _nullable_number(minimum=0.0),
            "maximum_plaquette_holonomy_phase": _nullable_number(minimum=0.0),
            "minimum_operator_threshold_over_sqrt_splitting": (
                _nullable_number(minimum=0.0)
            ),
            "normalized_excess_nonzero_hopping_weight": _nullable_number(),
            "normalized_squared_operator_residual": _nullable_number(minimum=0.0),
            "parent_scale": {"maximum": 1.0, "minimum": 0.0, "type": "number"},
            "reference_interpolation": errors,
            "restricted_global_rotation_angle": _nullable_number(),
            "restricted_global_rotation_degenerate": {"type": "boolean"},
            "shell_diagnostics": {"items": shell, "minItems": 1, "type": "array"},
            "transport_closure_and_plaquette_applicable": {"type": "boolean"},
            "transport_closure_and_plaquette_inapplicable_reason": {
                "type": ["string", "null"]
            },
            "transport_rank_deficient_link_count": {
                "minimum": 0,
                "type": "integer",
            },
        }
    )
    point_fields = tuple(sorted(point_properties))
    point = _strict_object(point_properties, point_fields)
    point["allOf"] = [
        {
            "if": {
                "properties": {
                    "transport_closure_and_plaquette_applicable": {"const": True}
                },
                "required": ["transport_closure_and_plaquette_applicable"],
            },
            "then": {
                "properties": {
                    "maximum_absolute_closure_holonomy_phases": {"type": "array"},
                    "maximum_closure_holonomy_unitarity_defect": {"type": "number"},
                    "maximum_plaquette_holonomy_phase": {"type": "number"},
                    "transport_closure_and_plaquette_inapplicable_reason": {
                        "const": None
                    },
                    "transport_rank_deficient_link_count": {"const": 0},
                }
            },
        },
        {
            "if": {
                "properties": {
                    "transport_closure_and_plaquette_applicable": {"const": False}
                },
                "required": ["transport_closure_and_plaquette_applicable"],
            },
            "then": {
                "properties": {
                    "maximum_absolute_closure_holonomy_phases": {"const": None},
                    "maximum_closure_holonomy_unitarity_defect": {"const": None},
                    "maximum_plaquette_holonomy_phase": {"const": None},
                    "transport_closure_and_plaquette_inapplicable_reason": {
                        "const": TRANSPORT_RANK_DEFICIENT_REASON
                    },
                    "transport_rank_deficient_link_count": {
                        "minimum": 1,
                        "type": "integer",
                    },
                }
            },
        },
    ]
    amplitude_midpoint_fields = (
        "amplitude_nodes",
        "applicable",
        "endpoint_minimum_threshold_over_sqrt_splitting",
        "inapplicable_reason",
        "maximum_correlation_midpoint_defect",
        "maximum_hopping_block_power_midpoint_defect",
        "maximum_joint_threshold_midpoint_defect",
        "maximum_nonzero_hopping_weight_midpoint_defect",
        "maximum_operator_threshold_midpoint_defect",
    )
    amplitude_midpoint = _strict_object(
        {
            "amplitude_nodes": {"minimum": 1, "type": "integer"},
            "applicable": {"type": "boolean"},
            "endpoint_minimum_threshold_over_sqrt_splitting": _nullable_number(
                minimum=0.0
            ),
            "inapplicable_reason": {"type": ["string", "null"]},
            "maximum_correlation_midpoint_defect": _nullable_number(minimum=0.0),
            "maximum_hopping_block_power_midpoint_defect": _nullable_number(
                minimum=0.0
            ),
            "maximum_joint_threshold_midpoint_defect": _nullable_number(minimum=0.0),
            "maximum_nonzero_hopping_weight_midpoint_defect": _nullable_number(
                minimum=0.0
            ),
            "maximum_operator_threshold_midpoint_defect": _nullable_number(minimum=0.0),
        },
        amplitude_midpoint_fields,
    )
    amplitude_resolution_fields = (
        "amplitude_intervals",
        "amplitude_nodes",
        "maximum_joint_threshold_midpoint_interpolation_defect",
        "maximum_operator_threshold_midpoint_interpolation_defect",
        "passes_unit_scale_draft_tolerance",
        "tolerance_inapplicable_reason",
    )
    amplitude_resolution = _strict_object(
        {
            "amplitude_intervals": {"minimum": 1, "type": "integer"},
            "amplitude_nodes": {"minimum": 2, "type": "integer"},
            "maximum_joint_threshold_midpoint_interpolation_defect": _number(
                minimum=0.0
            ),
            "maximum_operator_threshold_midpoint_interpolation_defect": _number(
                minimum=0.0
            ),
            "passes_unit_scale_draft_tolerance": {"type": ["boolean", "null"]},
            "tolerance_inapplicable_reason": {
                "minLength": 1,
                "type": "string",
            },
        },
        amplitude_resolution_fields,
    )
    case_fields = (
        "amplitude_midpoint",
        "construction_evaluation_minimum_separation",
        "flat_amplitude_resolution",
        "metric_covariance_defect",
        "name",
        "points",
    )
    case = _strict_object(
        {
            "amplitude_midpoint": amplitude_midpoint,
            "construction_evaluation_minimum_separation": {
                "exclusiveMinimum": 0.0,
                "type": "number",
            },
            "flat_amplitude_resolution": {
                "items": amplitude_resolution,
                "minItems": 1,
                "type": "array",
            },
            "metric_covariance_defect": _number(minimum=0.0),
            "name": {"minLength": 1, "type": "string"},
            "points": {"items": point, "minItems": 1, "type": "array"},
        },
        case_fields,
    )
    schema_id = band_equivalence_locality_schema_id(family, "result")
    return {
        "$id": schema_id,
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        **_strict_object(
            {
                "analysis_request_sha256": {
                    "pattern": "^[0-9a-f]{64}$",
                    "type": "string",
                },
                "cases": {"items": case, "minItems": 1, "type": "array"},
                "construction_size": {"minimum": 4, "type": "integer"},
                "evaluation_size": {"minimum": 3, "type": "integer"},
                "family": {"const": family.value},
                "schema": {"const": schema_id},
                "status": {"const": "development-smoke-not-retained-evidence"},
            },
            (
                "analysis_request_sha256",
                "cases",
                "construction_size",
                "evaluation_size",
                "family",
                "schema",
                "status",
            ),
        ),
    }


def band_equivalence_locality_verification_schema(
    family: BandEquivalenceLocalityFamily,
) -> dict[str, JsonValue]:
    """Return the strict verification schema for one experiment family."""
    if type(family) is not BandEquivalenceLocalityFamily:
        raise TypeError("family must be BandEquivalenceLocalityFamily")
    schema_id = band_equivalence_locality_schema_id(family, "verification")
    return {
        "$id": schema_id,
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        **_strict_object(
            {
                "family": {"const": family.value},
                "input_sha256": {
                    "pattern": "^[0-9a-f]{64}$",
                    "type": "string",
                },
                "maximum_independent_band_defect": _number(minimum=0.0),
                "maximum_independent_parent_defect": _number(minimum=0.0),
                "maximum_stored_identity_defect": _number(minimum=0.0),
                "passes": {"type": "boolean"},
                "result_sha256": {
                    "pattern": "^[0-9a-f]{64}$",
                    "type": "string",
                },
                "schema": {"const": schema_id},
                "status": {
                    "const": "development-verification-not-scientific-validation"
                },
            },
            (
                "family",
                "input_sha256",
                "maximum_independent_band_defect",
                "maximum_independent_parent_defect",
                "maximum_stored_identity_defect",
                "passes",
                "result_sha256",
                "schema",
                "status",
            ),
        ),
    }


def band_equivalence_locality_refinement_schema(
    family: BandEquivalenceLocalityFamily,
) -> dict[str, JsonValue]:
    """Return a strict schema for one family refinement result."""
    if type(family) is not BandEquivalenceLocalityFamily:
        raise TypeError("family must be BandEquivalenceLocalityFamily")
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
        "transport_closure_and_plaquette_applicability_stable": {"type": "boolean"},
        **nonnegative,
        "maximum_final_outcome_change": {"type": ["integer", "null"]},
        "maximum_shared_parent_eigenvalue_defect": {"type": ["number", "null"]},
        "maximum_shared_projector_defect": {"type": ["number", "null"]},
        "shared_mesh_inapplicable_reason": {"minLength": 1, "type": "string"},
        "shared_mesh_quantities_applicable": {"type": "boolean"},
        "tolerance_disposition_reason": {"minLength": 1, "type": "string"},
        "within_draft_tolerances": {"type": ["boolean", "null"]},
    }
    pair = _strict_object(properties, tuple(sorted(properties)))
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
    return {
        "$id": refinement_schema_id(family),
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        **_strict_object(root_properties, tuple(sorted(root_properties))),
    }


def write_band_equivalence_locality_schemas(
    directory: Path, family: BandEquivalenceLocalityFamily
) -> tuple[Path, Path, Path]:
    """Write strict family-specific schemas to one experiment-owned directory."""
    if not isinstance(directory, Path):
        raise TypeError("directory must be pathlib.Path")
    if type(family) is not BandEquivalenceLocalityFamily:
        raise TypeError("family must be BandEquivalenceLocalityFamily")
    directory.mkdir(parents=True, exist_ok=True)
    documents = (
        (
            directory / "development-input.schema.json",
            band_equivalence_locality_request_schema(family),
        ),
        (
            directory / "development-result.schema.json",
            band_equivalence_locality_result_schema(family),
        ),
        (
            directory / "development-verification.schema.json",
            band_equivalence_locality_verification_schema(family),
        ),
    )
    for path, document in documents:
        path.write_bytes(canonical_json_bytes(document))
    return documents[0][0], documents[1][0], documents[2][0]


__all__ = [
    "band_equivalence_locality_refinement_schema",
    "band_equivalence_locality_request_schema",
    "band_equivalence_locality_result_schema",
    "band_equivalence_locality_verification_schema",
    "write_band_equivalence_locality_schemas",
]
