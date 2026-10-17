"""Deterministic wire serialization for locality development records.

This module is deliberately separate from the calculator: JSON field names, schema
identities, canonical byte encoding, and filesystem output are wire mechanics rather
than scientific transformations. Serializers consume immutable definitions and results
without selecting thresholds, recomputing diagnostics, or changing evidence status.
"""

from __future__ import annotations

import json
from pathlib import Path

from .definitions import BandEquivalenceLocalityFamily, BandEquivalenceLocalityRequest
from .records import (
    BandEquivalenceLocalityResult,
    BandEquivalenceLocalityVerificationResult,
    ErrorChannels,
)
from .refinement_records import BandEquivalenceLocalityRefinementResult

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]


def band_equivalence_locality_schema_id(
    family: BandEquivalenceLocalityFamily, document: str
) -> str:
    """Return the family-bound development schema identity."""
    if type(family) is not BandEquivalenceLocalityFamily:
        raise TypeError("family must be BandEquivalenceLocalityFamily")
    if type(document) is not str or document not in {
        "input",
        "result",
        "verification",
    }:
        raise ValueError("document must be input, result, or verification")
    return f"{family.value}.calculation.{document}.v1"


def refinement_schema_id(family: BandEquivalenceLocalityFamily) -> str:
    """Return the family-bound refinement-assessment schema identity."""
    if type(family) is not BandEquivalenceLocalityFamily:
        raise TypeError("family must be BandEquivalenceLocalityFamily")
    return f"{family.value}.calculation.refinement-assessment.v1"


def canonical_json_bytes(document: dict[str, JsonValue]) -> bytes:
    """Return deterministic UTF-8 JSON bytes for hashing and storage."""
    return (
        json.dumps(document, allow_nan=False, separators=(",", ":"), sort_keys=True)
        + "\n"
    ).encode()


def _errors_document(value: ErrorChannels) -> dict[str, JsonValue]:
    return {
        "maximum_band": value.maximum_band,
        "maximum_hamiltonian": value.maximum_hamiltonian,
        "rms_band": value.rms_band,
        "rms_hamiltonian": value.rms_hamiltonian,
    }


def band_equivalence_locality_request_document(
    value: BandEquivalenceLocalityRequest,
) -> dict[str, JsonValue]:
    """Serialize a development definition without accepting unspecified values."""
    return {
        "amplitude_resolution_intervals": list(value.amplitude_resolution_intervals),
        "amplitudes": list(value.amplitudes),
        "band_tolerances": list(value.band_tolerances),
        "cases": [
            {
                "basis_offsets": [list(offset) for offset in case.basis_offsets],
                "dimension": case.dimension,
                "direct_lattice_primitive_basis_rows": [
                    [float(value) for value in row]
                    for row in case.direct_metric.primitive_basis
                ],
                "direct_lattice_primitive_vector_axis": "columns",
                "gauge_normalization": case.gauge_normalization.value,
                "name": case.name,
                "parent_kind": case.parent_kind.value,
                "shell_metric_scale": case.shell_metric_scale,
                "positive_bonds": [list(bond) for bond in case.positive_bonds],
            }
            for case in value.cases
        ],
        "construction_size": value.construction_size,
        "evaluation_shift": value.evaluation_shift,
        "evaluation_size": value.evaluation_size,
        "family": value.family.value,
        "parent_scales": list(value.parent_scales),
        "schema": band_equivalence_locality_schema_id(value.family, "input"),
        "shell_cap": value.shell_cap,
        "status": "bounded-development-smoke-input",
        "transport_rank_absolute": value.transport_rank_absolute,
        "transport_rank_relative": value.transport_rank_relative,
    }


def band_equivalence_locality_result_document(
    value: BandEquivalenceLocalityResult,
) -> dict[str, JsonValue]:
    """Serialize compact development diagnostics without assigning evidence status."""
    cases: list[JsonValue] = []
    for case in value.cases:
        points: list[JsonValue] = []
        for point in case.points:
            shells: list[JsonValue] = [
                {
                    "comparison_omitted_power": shell.comparison_omitted_power,
                    "comparison_shell_power": shell.comparison_shell_power,
                    "comparison_total": _errors_document(shell.comparison_total),
                    "comparison_total_omitted_power": (
                        shell.comparison_total_omitted_power
                    ),
                    "comparison_truncation": _errors_document(
                        shell.comparison_truncation
                    ),
                    "comparison_truncation_parseval_defect": (
                        shell.comparison_truncation_parseval_defect
                    ),
                    "reference_omitted_power": shell.reference_omitted_power,
                    "reference_shell_power": shell.reference_shell_power,
                    "reference_total": _errors_document(shell.reference_total),
                    "reference_total_omitted_power": (
                        shell.reference_total_omitted_power
                    ),
                    "reference_truncation": _errors_document(
                        shell.reference_truncation
                    ),
                    "reference_truncation_parseval_defect": (
                        shell.reference_truncation_parseval_defect
                    ),
                    "retained_blocks": shell.retained_blocks,
                    "shell_index": shell.shell_index,
                }
                for shell in point.shell_diagnostics
            ]
            decisions: list[JsonValue] = [
                {
                    "comparison_band_passing_error": (
                        decision.comparison_band_passing_error
                    ),
                    "comparison_band_preceding_error": (
                        decision.comparison_band_preceding_error
                    ),
                    "comparison_band_shell": decision.comparison_band_shell,
                    "comparison_hamiltonian_passing_error": (
                        decision.comparison_hamiltonian_passing_error
                    ),
                    "comparison_hamiltonian_preceding_error": (
                        decision.comparison_hamiltonian_preceding_error
                    ),
                    "comparison_hamiltonian_shell": (
                        decision.comparison_hamiltonian_shell
                    ),
                    "reference_band_passing_error": (
                        decision.reference_band_passing_error
                    ),
                    "reference_band_preceding_error": (
                        decision.reference_band_preceding_error
                    ),
                    "reference_band_shell": decision.reference_band_shell,
                    "reference_hamiltonian_passing_error": (
                        decision.reference_hamiltonian_passing_error
                    ),
                    "reference_hamiltonian_preceding_error": (
                        decision.reference_hamiltonian_preceding_error
                    ),
                    "reference_hamiltonian_shell": (
                        decision.reference_hamiltonian_shell
                    ),
                    "tolerance": decision.tolerance,
                }
                for decision in point.first_passing
            ]
            points.append(
                {
                    "alignment_applicable": point.alignment_applicable,
                    "alignment_inapplicable_reason": (
                        point.alignment_inapplicable_reason
                    ),
                    "amplitude": point.amplitude,
                    "analytic_correlation_remainder_bound": (
                        point.analytic_correlation_remainder_bound
                    ),
                    "analytic_flat_correlation": point.analytic_flat_correlation,
                    "basis_distance_maximum": point.basis_distance_maximum,
                    "basis_distance_minimum": point.basis_distance_minimum,
                    "comparison_fourier_reconstruction_defect": (
                        point.comparison_fourier_reconstruction_defect
                    ),
                    "comparison_interpolation": _errors_document(
                        point.comparison_interpolation
                    ),
                    "comparison_nononsite_power": point.comparison_nononsite_power,
                    "comparison_nyquist_power": point.comparison_nyquist_power,
                    "comparison_onsite_power": point.comparison_onsite_power,
                    "comparison_ordinary_hermiticity_defect": (
                        point.comparison_ordinary_hermiticity_defect
                    ),
                    "comparison_parseval_defect": point.comparison_parseval_defect,
                    "comparison_total_power": point.comparison_total_power,
                    "comparison_twisted_nyquist_defect": (
                        point.comparison_twisted_nyquist_defect
                    ),
                    "continuous_external_gap_lower_bound": (
                        point.continuous_external_gap_lower_bound
                    ),
                    "correlation_quadrature_defect": (
                        point.correlation_quadrature_defect
                    ),
                    "exact_spectrum_joint_operator_threshold": (
                        point.exact_spectrum_joint_operator_threshold
                    ),
                    "exact_spectrum_joint_threshold_over_sqrt_splitting": (
                        point.exact_spectrum_joint_threshold_over_sqrt_splitting
                    ),
                    "excess_nonzero_hopping_weight": (
                        point.excess_nonzero_hopping_weight
                    ),
                    "finite_mesh_maximum_correlation": (
                        point.finite_mesh_maximum_correlation
                    ),
                    "first_passing": decisions,
                    "flat_identity_departure": point.flat_identity_departure,
                    "flat_residual_tail_identity_defect": (
                        point.flat_residual_tail_identity_defect
                    ),
                    "maximum_absolute_closure_holonomy_phases": (
                        None
                        if point.maximum_absolute_closure_holonomy_phases is None
                        else list(point.maximum_absolute_closure_holonomy_phases)
                    ),
                    "maximum_closure_holonomy_unitarity_defect": (
                        point.maximum_closure_holonomy_unitarity_defect
                    ),
                    "maximum_covariant_defect": point.maximum_covariant_defect,
                    "maximum_direct_band_defect": point.maximum_direct_band_defect,
                    "maximum_eigensystem_reconstruction_defect": (
                        point.maximum_eigensystem_reconstruction_defect
                    ),
                    "maximum_frame_orthonormality_defect": (
                        point.maximum_frame_orthonormality_defect
                    ),
                    "maximum_parent_fourier_reconstruction_defect": (
                        point.maximum_parent_fourier_reconstruction_defect
                    ),
                    "maximum_parent_hermiticity_defect": (
                        point.maximum_parent_hermiticity_defect
                    ),
                    "maximum_parent_retained_reconstruction_defect": (
                        point.maximum_parent_retained_reconstruction_defect
                    ),
                    "maximum_periodic_frame_closure_defect": (
                        point.maximum_periodic_frame_closure_defect
                    ),
                    "maximum_plaquette_holonomy_phase": (
                        point.maximum_plaquette_holonomy_phase
                    ),
                    "maximum_projector_reconstruction_defect": (
                        point.maximum_projector_reconstruction_defect
                    ),
                    "maximum_transport_procrustes_residual": (
                        point.maximum_transport_procrustes_residual
                    ),
                    "maximum_transport_squared_residual_roundoff_cutoff": (
                        point.maximum_transport_squared_residual_roundoff_cutoff
                    ),
                    "maximum_transport_rank_cutoff": (
                        point.maximum_transport_rank_cutoff
                    ),
                    "maximum_transport_unitarity_defect": (
                        point.maximum_transport_unitarity_defect
                    ),
                    "minimum_operator_threshold": point.minimum_operator_threshold,
                    "minimum_operator_threshold_over_sqrt_splitting": (
                        point.minimum_operator_threshold_over_sqrt_splitting
                    ),
                    "minimum_sampled_external_gap": (
                        point.minimum_sampled_external_gap
                    ),
                    "minimum_sampled_transport_singular_value": (
                        point.minimum_sampled_transport_singular_value
                    ),
                    "minimum_seed_overlap": point.minimum_seed_overlap,
                    "parent_scale": point.parent_scale,
                    "reference_fourier_reconstruction_defect": (
                        point.reference_fourier_reconstruction_defect
                    ),
                    "reference_interpolation": _errors_document(
                        point.reference_interpolation
                    ),
                    "normalized_excess_nonzero_hopping_weight": (
                        point.normalized_excess_nonzero_hopping_weight
                    ),
                    "normalized_squared_operator_residual": (
                        point.normalized_squared_operator_residual
                    ),
                    "reference_nononsite_power": point.reference_nononsite_power,
                    "reference_nyquist_power": point.reference_nyquist_power,
                    "reference_onsite_power": point.reference_onsite_power,
                    "reference_ordinary_hermiticity_defect": (
                        point.reference_ordinary_hermiticity_defect
                    ),
                    "reference_parseval_defect": point.reference_parseval_defect,
                    "reference_total_power": point.reference_total_power,
                    "reference_twisted_nyquist_defect": (
                        point.reference_twisted_nyquist_defect
                    ),
                    "restricted_global_rotation_angle": (
                        point.restricted_global_rotation_angle
                    ),
                    "restricted_global_rotation_degenerate": (
                        point.restricted_global_rotation_degenerate
                    ),
                    "restricted_global_rotation_residual": (
                        point.restricted_global_rotation_residual
                    ),
                    "shell_diagnostics": shells,
                    "splitting_scale": point.splitting_scale,
                    "transport_closure_and_plaquette_applicable": (
                        point.transport_closure_and_plaquette_applicable
                    ),
                    "transport_closure_and_plaquette_inapplicable_reason": (
                        point.transport_closure_and_plaquette_inapplicable_reason
                    ),
                    "transport_rank_deficient_link_count": (
                        point.transport_rank_deficient_link_count
                    ),
                }
            )
        cases.append(
            {
                "amplitude_midpoint": {
                    "amplitude_nodes": case.amplitude_midpoint.amplitude_nodes,
                    "applicable": case.amplitude_midpoint.applicable,
                    "endpoint_minimum_threshold_over_sqrt_splitting": (
                        case.amplitude_midpoint.endpoint_minimum_threshold_over_sqrt_splitting
                    ),
                    "inapplicable_reason": (
                        case.amplitude_midpoint.inapplicable_reason
                    ),
                    "maximum_correlation_midpoint_defect": (
                        case.amplitude_midpoint.maximum_correlation_midpoint_defect
                    ),
                    "maximum_hopping_block_power_midpoint_defect": (
                        case.amplitude_midpoint.maximum_hopping_block_power_midpoint_defect
                    ),
                    "maximum_joint_threshold_midpoint_defect": (
                        case.amplitude_midpoint.maximum_joint_threshold_midpoint_defect
                    ),
                    "maximum_nonzero_hopping_weight_midpoint_defect": (
                        case.amplitude_midpoint.maximum_nonzero_hopping_weight_midpoint_defect
                    ),
                    "maximum_operator_threshold_midpoint_defect": (
                        case.amplitude_midpoint.maximum_operator_threshold_midpoint_defect
                    ),
                },
                "construction_evaluation_minimum_separation": (
                    case.construction_evaluation_minimum_separation
                ),
                "flat_amplitude_resolution": [
                    {
                        "amplitude_intervals": item.amplitude_intervals,
                        "amplitude_nodes": item.amplitude_nodes,
                        "maximum_joint_threshold_midpoint_interpolation_defect": (
                            item.maximum_joint_threshold_midpoint_interpolation_defect
                        ),
                        "maximum_operator_threshold_midpoint_interpolation_defect": (
                            item.maximum_operator_threshold_midpoint_interpolation_defect
                        ),
                        "passes_unit_scale_draft_tolerance": (
                            item.passes_unit_scale_draft_tolerance
                        ),
                        "tolerance_inapplicable_reason": (
                            item.tolerance_inapplicable_reason
                        ),
                    }
                    for item in case.flat_amplitude_resolution
                ],
                "metric_covariance_defect": case.metric_covariance_defect,
                "name": case.name,
                "points": points,
            }
        )
    return {
        "analysis_request_sha256": value.analysis_request_sha256,
        "cases": cases,
        "construction_size": value.construction_size,
        "evaluation_size": value.evaluation_size,
        "family": value.family.value,
        "schema": band_equivalence_locality_schema_id(value.family, "result"),
        "status": value.status,
    }


def band_equivalence_locality_refinement_document(
    value: BandEquivalenceLocalityRefinementResult,
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
                "transport_closure_and_plaquette_applicability_stable": (
                    item.transport_closure_and_plaquette_applicability_stable
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
                "maximum_shared_projector_defect": (
                    item.maximum_shared_projector_defect
                ),
                "maximum_threshold_change": item.maximum_threshold_change,
                "shared_mesh_inapplicable_reason": (
                    item.shared_mesh_inapplicable_reason
                ),
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


def band_equivalence_locality_verification_document(
    value: BandEquivalenceLocalityVerificationResult,
) -> dict[str, JsonValue]:
    """Serialize independent development verification diagnostics."""
    return {
        "family": value.family.value,
        "input_sha256": value.input_sha256,
        "maximum_independent_band_defect": value.maximum_independent_band_defect,
        "maximum_independent_parent_defect": value.maximum_independent_parent_defect,
        "maximum_stored_identity_defect": value.maximum_stored_identity_defect,
        "passes": value.passes,
        "result_sha256": value.result_sha256,
        "schema": band_equivalence_locality_schema_id(value.family, "verification"),
        "status": "development-verification-not-scientific-validation",
    }


def write_band_equivalence_locality_documents(
    directory: Path,
    definition: BandEquivalenceLocalityRequest,
    result: BandEquivalenceLocalityResult,
    verification: BandEquivalenceLocalityVerificationResult,
) -> tuple[Path, Path, Path]:
    """Write replaceable development JSON documents to an experiment directory."""
    if not isinstance(directory, Path):
        raise TypeError("directory must be pathlib.Path")
    directory.mkdir(parents=True, exist_ok=True)
    documents = (
        (
            directory / "development-input.json",
            band_equivalence_locality_request_document(definition),
        ),
        (
            directory / "development-result.json",
            band_equivalence_locality_result_document(result),
        ),
        (
            directory / "development-verification.json",
            band_equivalence_locality_verification_document(verification),
        ),
    )
    for path, document in documents:
        path.write_bytes(canonical_json_bytes(document))
    return documents[0][0], documents[1][0], documents[2][0]


def write_band_equivalence_locality_refinement(
    directory: Path,
    result: BandEquivalenceLocalityRefinementResult,
) -> tuple[Path, Path]:
    """Write one refinement result and its strict family-bound schema."""
    if not isinstance(directory, Path):
        raise TypeError("directory must be pathlib.Path")
    from .schemas import band_equivalence_locality_refinement_schema

    directory.mkdir(parents=True, exist_ok=True)
    document_path = directory / "development-refinement-assessment.json"
    schema_path = directory / "development-refinement-assessment.schema.json"
    document_path.write_bytes(
        canonical_json_bytes(band_equivalence_locality_refinement_document(result))
    )
    schema_path.write_bytes(
        canonical_json_bytes(band_equivalence_locality_refinement_schema(result.family))
    )
    return document_path, schema_path


__all__ = [
    "JsonValue",
    "canonical_json_bytes",
    "band_equivalence_locality_refinement_document",
    "band_equivalence_locality_request_document",
    "band_equivalence_locality_result_document",
    "band_equivalence_locality_schema_id",
    "band_equivalence_locality_verification_document",
    "refinement_schema_id",
    "write_band_equivalence_locality_documents",
    "write_band_equivalence_locality_refinement",
]
