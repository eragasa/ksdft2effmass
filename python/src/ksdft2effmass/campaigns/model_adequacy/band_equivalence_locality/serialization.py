"""Deterministic wire serialization for locality development records.

This module is deliberately separate from the calculator: JSON field names, schema
identities, canonical byte encoding, and filesystem output are wire mechanics rather
than scientific transformations. Serializers consume immutable definitions and results
without selecting thresholds, recomputing diagnostics, or changing evidence status.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.definitions import (  # noqa: E501
    BandEquivalenceLocalityFamily,
    BandEquivalenceLocalityRequest,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.records import (
    BandEquivalenceLocalityDiagnostics,
    BandEquivalenceLocalityVerificationDiagnostics,
    ErrorChannels,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.refinement_records import (  # noqa: E501
    BandEquivalenceLocalityRefinementAssessment,
)


class _ErrorChannelsWire(TypedDict):
    maximum_band: float
    maximum_hamiltonian: float
    rms_band: float
    rms_hamiltonian: float


class _ShellWire(TypedDict):
    comparison_omitted_power: float
    comparison_shell_power: float
    comparison_total: _ErrorChannelsWire
    comparison_total_omitted_power: float
    comparison_truncation: _ErrorChannelsWire
    comparison_truncation_parseval_defect: float
    reference_omitted_power: float
    reference_shell_power: float
    reference_total: _ErrorChannelsWire
    reference_total_omitted_power: float
    reference_truncation: _ErrorChannelsWire
    reference_truncation_parseval_defect: float
    retained_blocks: int
    shell_index: int


class _FirstPassingWire(TypedDict):
    comparison_band_passing_error: float | None
    comparison_band_preceding_error: float | None
    comparison_band_shell: int | None
    comparison_hamiltonian_passing_error: float | None
    comparison_hamiltonian_preceding_error: float | None
    comparison_hamiltonian_shell: int | None
    reference_band_passing_error: float | None
    reference_band_preceding_error: float | None
    reference_band_shell: int | None
    reference_hamiltonian_passing_error: float | None
    reference_hamiltonian_preceding_error: float | None
    reference_hamiltonian_shell: int | None
    tolerance: float


class _PointWire(TypedDict):
    alignment_applicable: bool
    alignment_inapplicable_reason: str | None
    amplitude: float
    analytic_correlation_remainder_bound: float | None
    analytic_flat_correlation: float | None
    basis_distance_maximum: float | None
    basis_distance_minimum: float | None
    comparison_fourier_reconstruction_defect: float
    comparison_interpolation: _ErrorChannelsWire
    comparison_nononsite_power: float
    comparison_nyquist_power: float
    comparison_onsite_power: float
    comparison_ordinary_hermiticity_defect: float
    comparison_parseval_defect: float
    comparison_total_power: float
    comparison_twisted_nyquist_defect: float
    continuous_external_gap_lower_bound: float
    correlation_quadrature_defect: float | None
    exact_spectrum_joint_operator_threshold: float
    exact_spectrum_joint_threshold_over_sqrt_splitting: float | None
    excess_nonzero_hopping_weight: float
    finite_mesh_maximum_correlation: float | None
    first_passing: list[_FirstPassingWire]
    flat_identity_departure: float | None
    flat_residual_tail_identity_defect: float | None
    maximum_absolute_closure_holonomy_phases: list[float] | None
    maximum_closure_holonomy_unitarity_defect: float | None
    maximum_covariant_defect: float
    maximum_direct_band_defect: float
    maximum_eigensystem_reconstruction_defect: float
    maximum_frame_orthonormality_defect: float
    maximum_parent_fourier_reconstruction_defect: float
    maximum_parent_hermiticity_defect: float
    maximum_parent_retained_reconstruction_defect: float
    maximum_periodic_frame_closure_defect: float
    maximum_plaquette_holonomy_phase: float | None
    maximum_projector_reconstruction_defect: float
    maximum_transport_procrustes_residual: float
    maximum_transport_rank_cutoff: float
    maximum_transport_squared_residual_roundoff_cutoff: float
    maximum_transport_unitarity_defect: float
    minimum_operator_threshold: float
    minimum_operator_threshold_over_sqrt_splitting: float | None
    minimum_sampled_external_gap: float
    minimum_sampled_transport_singular_value: float
    minimum_seed_overlap: float
    normalized_excess_nonzero_hopping_weight: float | None
    normalized_squared_operator_residual: float | None
    parent_scale: float
    reference_fourier_reconstruction_defect: float
    reference_interpolation: _ErrorChannelsWire
    reference_nononsite_power: float
    reference_nyquist_power: float
    reference_onsite_power: float
    reference_ordinary_hermiticity_defect: float
    reference_parseval_defect: float
    reference_total_power: float
    reference_twisted_nyquist_defect: float
    restricted_global_rotation_angle: float | None
    restricted_global_rotation_degenerate: bool
    restricted_global_rotation_residual: float
    shell_diagnostics: list[_ShellWire]
    splitting_scale: float
    transport_closure_and_plaquette_applicable: bool
    transport_closure_and_plaquette_inapplicable_reason: str | None
    transport_rank_deficient_link_count: int


class _AmplitudeMidpointWire(TypedDict):
    amplitude_nodes: int
    applicable: bool
    endpoint_minimum_threshold_over_sqrt_splitting: float | None
    inapplicable_reason: str | None
    maximum_correlation_midpoint_defect: float | None
    maximum_hopping_block_power_midpoint_defect: float | None
    maximum_joint_threshold_midpoint_defect: float | None
    maximum_nonzero_hopping_weight_midpoint_defect: float | None
    maximum_operator_threshold_midpoint_defect: float | None


class _FlatAmplitudeResolutionWire(TypedDict):
    amplitude_intervals: int
    amplitude_nodes: int
    maximum_joint_threshold_midpoint_interpolation_defect: float
    maximum_operator_threshold_midpoint_interpolation_defect: float
    passes_unit_scale_draft_tolerance: bool | None
    tolerance_inapplicable_reason: str


class _ResultCaseWire(TypedDict):
    amplitude_midpoint: _AmplitudeMidpointWire
    construction_evaluation_minimum_separation: float
    flat_amplitude_resolution: list[_FlatAmplitudeResolutionWire]
    metric_covariance_defect: float
    name: str
    points: list[_PointWire]


class _RequestCaseWire(TypedDict):
    basis_offsets: list[list[float]]
    dimension: int
    direct_lattice_primitive_basis_rows: list[list[float]]
    direct_lattice_primitive_vector_axis: str
    gauge_normalization: str
    name: str
    parent_kind: str
    positive_bonds: list[list[int]]
    shell_metric_scale: float


class _RequestWire(TypedDict):
    amplitude_resolution_intervals: list[int]
    amplitudes: list[float]
    band_tolerances: list[float]
    cases: list[_RequestCaseWire]
    construction_size: int
    evaluation_shift: float
    evaluation_size: int
    family: str
    parent_scales: list[float]
    schema: str
    shell_cap: int
    status: str
    transport_rank_absolute: float
    transport_rank_relative: float


class _ResultWire(TypedDict):
    analysis_request_sha256: str
    cases: list[_ResultCaseWire]
    construction_size: int
    evaluation_size: int
    family: str
    schema: str
    status: str


class _VerificationWire(TypedDict):
    family: str
    input_sha256: str
    maximum_independent_band_defect: float
    maximum_independent_parent_defect: float
    maximum_stored_identity_defect: float
    passes: bool
    result_sha256: str
    schema: str
    status: str


class _RefinementPairWire(TypedDict):
    coarse_construction_size: int
    fine_construction_size: int
    first_passing_dispositions_stable: bool
    maximum_angle_change: float
    maximum_band_defect: float
    maximum_correlation_change: float
    maximum_final_outcome_change: int | None
    maximum_final_parent_invariant_change: float
    maximum_hopping_block_power_change: float
    maximum_hopping_weight_change: float
    maximum_parent_diagnostic_change: float
    maximum_parseval_defect: float
    maximum_reconstruction_defect: float
    maximum_shared_parent_eigenvalue_defect: float | None
    maximum_shared_projector_defect: float | None
    maximum_threshold_change: float
    shared_mesh_inapplicable_reason: str
    shared_mesh_quantities_applicable: bool
    tolerance_disposition_reason: str
    transport_closure_and_plaquette_applicability_stable: bool
    within_draft_tolerances: bool | None


class _RefinementWire(TypedDict):
    family: str
    momentum_disposition: str
    momentum_disposition_reason: str
    paper1_literal_range_endpoints_applicable: bool
    paper1_literal_range_endpoints_inapplicable_reason: str
    passes_draft_tolerance: bool | None
    passes_unit_scale_draft_tolerance: bool | None
    refinements: list[_RefinementPairWire]
    required_stable_refinements: int
    schema: str
    source_result_sha256: list[str]
    status: str
    tolerance_inapplicable_reason: str


type _WireDocument = _RequestWire | _ResultWire | _VerificationWire | _RefinementWire


@dataclass(frozen=True, slots=True)
class CanonicalJsonDocument:
    """Immutable canonical JSON bytes owned by the wire boundary."""

    _content: bytes

    def __post_init__(self) -> None:
        if type(self._content) is not bytes:
            raise TypeError("canonical JSON content must be built-in bytes")
        try:
            decoded = self._content.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError("canonical JSON content must be UTF-8") from error
        try:
            document = json.loads(decoded)
        except json.JSONDecodeError as error:
            raise ValueError("canonical JSON content must be valid JSON") from error
        if type(document) is not dict:
            raise ValueError("canonical JSON document must be an object")
        try:
            expected = (
                json.dumps(
                    document,
                    allow_nan=False,
                    separators=(",", ":"),
                    sort_keys=True,
                )
                + "\n"
            ).encode("utf-8")
        except (TypeError, ValueError) as error:
            raise ValueError(
                "canonical JSON content contains invalid values"
            ) from error
        if self._content != expected:
            raise ValueError("canonical JSON content must use canonical encoding")

    @classmethod
    def _from_wire(cls, document: _WireDocument) -> CanonicalJsonDocument:
        content = (
            json.dumps(document, allow_nan=False, separators=(",", ":"), sort_keys=True)
            + "\n"
        ).encode()
        return cls(content)

    def canonical_bytes(self) -> bytes:
        """Return the immutable canonical UTF-8 bytes."""

        return self._content

    def content_sha256(self) -> str:
        """Return the wire-level SHA-256 identity of these canonical bytes."""

        return hashlib.sha256(self._content).hexdigest()

    def write_to(self, path: Path) -> None:
        """Write the complete canonical document to ``path``."""

        if not isinstance(path, Path):
            raise TypeError("path must be pathlib.Path")
        path.write_bytes(self._content)


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


def _errors_wire(value: ErrorChannels) -> _ErrorChannelsWire:
    return {
        "maximum_band": value.maximum_band,
        "maximum_hamiltonian": value.maximum_hamiltonian,
        "rms_band": value.rms_band,
        "rms_hamiltonian": value.rms_hamiltonian,
    }


def _request_wire(value: BandEquivalenceLocalityRequest) -> _RequestWire:
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


def _result_wire(
    value: BandEquivalenceLocalityDiagnostics,
    analysis_request_sha256: str,
) -> _ResultWire:
    """Build the explicit result wire record without assigning evidence status."""
    cases: list[_ResultCaseWire] = []
    for case in value.cases:
        points: list[_PointWire] = []
        for point in case.points:
            shells: list[_ShellWire] = [
                {
                    "comparison_omitted_power": shell.comparison_omitted_power,
                    "comparison_shell_power": shell.comparison_shell_power,
                    "comparison_total": _errors_wire(shell.comparison_total),
                    "comparison_total_omitted_power": (
                        shell.comparison_total_omitted_power
                    ),
                    "comparison_truncation": _errors_wire(shell.comparison_truncation),
                    "comparison_truncation_parseval_defect": (
                        shell.comparison_truncation_parseval_defect
                    ),
                    "reference_omitted_power": shell.reference_omitted_power,
                    "reference_shell_power": shell.reference_shell_power,
                    "reference_total": _errors_wire(shell.reference_total),
                    "reference_total_omitted_power": (
                        shell.reference_total_omitted_power
                    ),
                    "reference_truncation": _errors_wire(shell.reference_truncation),
                    "reference_truncation_parseval_defect": (
                        shell.reference_truncation_parseval_defect
                    ),
                    "retained_blocks": shell.retained_blocks,
                    "shell_index": shell.shell_index,
                }
                for shell in point.shell_diagnostics
            ]
            decisions: list[_FirstPassingWire] = [
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
                    "comparison_interpolation": _errors_wire(
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
                    "reference_interpolation": _errors_wire(
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
        "analysis_request_sha256": analysis_request_sha256,
        "cases": cases,
        "construction_size": value.construction_size,
        "evaluation_size": value.evaluation_size,
        "family": value.family.value,
        "schema": band_equivalence_locality_schema_id(value.family, "result"),
        "status": value.status,
    }


def _refinement_wire(
    value: BandEquivalenceLocalityRefinementAssessment,
    source_result_sha256: tuple[str, ...],
) -> _RefinementWire:
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
        "source_result_sha256": list(source_result_sha256),
        "status": "replaceable-development-refinement-not-scientific-evidence",
        "tolerance_inapplicable_reason": value.tolerance_inapplicable_reason,
    }


def _verification_wire(
    value: BandEquivalenceLocalityVerificationDiagnostics,
    input_sha256: str,
    result_sha256: str,
) -> _VerificationWire:
    """Serialize independent development verification diagnostics."""
    return {
        "family": value.family.value,
        "input_sha256": input_sha256,
        "maximum_independent_band_defect": value.maximum_independent_band_defect,
        "maximum_independent_parent_defect": value.maximum_independent_parent_defect,
        "maximum_stored_identity_defect": value.maximum_stored_identity_defect,
        "passes": value.passes,
        "result_sha256": result_sha256,
        "schema": band_equivalence_locality_schema_id(value.family, "verification"),
        "status": "development-verification-not-scientific-validation",
    }


class BandEquivalenceLocalityRequestSerializer:
    """Encode one analysis request as a canonical JSON document."""

    __slots__ = ()

    def execute(self, value: BandEquivalenceLocalityRequest) -> CanonicalJsonDocument:
        if type(value) is not BandEquivalenceLocalityRequest:
            raise TypeError("value must be BandEquivalenceLocalityRequest")
        return CanonicalJsonDocument._from_wire(_request_wire(value))


class BandEquivalenceLocalityResultSerializer:
    """Encode diagnostics bound to their complete canonical analysis request."""

    __slots__ = ()

    def execute(
        self,
        value: BandEquivalenceLocalityDiagnostics,
        analysis_request: CanonicalJsonDocument,
    ) -> CanonicalJsonDocument:
        if type(value) is not BandEquivalenceLocalityDiagnostics:
            raise TypeError("value must be BandEquivalenceLocalityDiagnostics")
        if type(analysis_request) is not CanonicalJsonDocument:
            raise TypeError("analysis_request must be CanonicalJsonDocument")
        return CanonicalJsonDocument._from_wire(
            _result_wire(value, analysis_request.content_sha256())
        )


class BandEquivalenceLocalityVerificationSerializer:
    """Encode verification bound to its complete canonical input documents."""

    __slots__ = ()

    def execute(
        self,
        value: BandEquivalenceLocalityVerificationDiagnostics,
        input_document: CanonicalJsonDocument,
        result_document: CanonicalJsonDocument,
    ) -> CanonicalJsonDocument:
        if type(value) is not BandEquivalenceLocalityVerificationDiagnostics:
            raise TypeError(
                "value must be BandEquivalenceLocalityVerificationDiagnostics"
            )
        if type(input_document) is not CanonicalJsonDocument:
            raise TypeError("input_document must be CanonicalJsonDocument")
        if type(result_document) is not CanonicalJsonDocument:
            raise TypeError("result_document must be CanonicalJsonDocument")
        return CanonicalJsonDocument._from_wire(
            _verification_wire(
                value,
                input_document.content_sha256(),
                result_document.content_sha256(),
            )
        )


class BandEquivalenceLocalityRefinementSerializer:
    """Encode a refinement bound to its ordered canonical source results."""

    __slots__ = ()

    def execute(
        self,
        value: BandEquivalenceLocalityRefinementAssessment,
        source_results: tuple[CanonicalJsonDocument, ...],
    ) -> CanonicalJsonDocument:
        if type(value) is not BandEquivalenceLocalityRefinementAssessment:
            raise TypeError("value must be BandEquivalenceLocalityRefinementAssessment")
        if type(source_results) is not tuple or len(source_results) < 3:
            raise ValueError("source_results must contain at least three documents")
        if any(
            type(document) is not CanonicalJsonDocument for document in source_results
        ):
            raise TypeError("source_results must contain CanonicalJsonDocument values")
        return CanonicalJsonDocument._from_wire(
            _refinement_wire(
                value,
                tuple(document.content_sha256() for document in source_results),
            )
        )


__all__ = [
    "BandEquivalenceLocalityRefinementSerializer",
    "BandEquivalenceLocalityRequestSerializer",
    "BandEquivalenceLocalityResultSerializer",
    "BandEquivalenceLocalityVerificationSerializer",
    "CanonicalJsonDocument",
]
