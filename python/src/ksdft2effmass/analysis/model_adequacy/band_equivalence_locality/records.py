"""Immutable results produced by locality development calculations."""

from __future__ import annotations

import math
from dataclasses import dataclass

from .definitions import TRANSPORT_RANK_DEFICIENT_REASON, BandEquivalenceLocalityFamily


@dataclass(frozen=True, slots=True)
class ErrorChannels:
    """Retain normalized reconstructed-matrix and sorted-band errors."""

    maximum_hamiltonian: float
    rms_hamiltonian: float
    maximum_band: float
    rms_band: float


@dataclass(frozen=True, slots=True)
class ShellDiagnostic:
    """Retain all diagnostics at one complete metric-shell cutoff."""

    shell_index: int
    retained_blocks: int
    reference_truncation: ErrorChannels
    comparison_truncation: ErrorChannels
    reference_total: ErrorChannels
    comparison_total: ErrorChannels
    reference_shell_power: float
    comparison_shell_power: float
    reference_omitted_power: float
    comparison_omitted_power: float
    reference_total_omitted_power: float
    comparison_total_omitted_power: float
    reference_truncation_parseval_defect: float
    comparison_truncation_parseval_defect: float


@dataclass(frozen=True, slots=True)
class FirstPassingDecision:
    """Name one first-passing complete shell or an unresolved sampled decision."""

    tolerance: float
    reference_band_shell: int | None
    comparison_band_shell: int | None
    reference_hamiltonian_shell: int | None
    comparison_hamiltonian_shell: int | None
    reference_band_passing_error: float | None
    reference_band_preceding_error: float | None
    comparison_band_passing_error: float | None
    comparison_band_preceding_error: float | None
    reference_hamiltonian_passing_error: float | None
    reference_hamiltonian_preceding_error: float | None
    comparison_hamiltonian_passing_error: float | None
    comparison_hamiltonian_preceding_error: float | None


@dataclass(frozen=True, slots=True)
class PointDiagnostic:
    """Retain one independently calculated parent-scale/amplitude point."""

    parent_scale: float
    amplitude: float
    minimum_sampled_external_gap: float
    continuous_external_gap_lower_bound: float
    minimum_seed_overlap: float
    maximum_parent_hermiticity_defect: float
    maximum_eigensystem_reconstruction_defect: float
    maximum_frame_orthonormality_defect: float
    maximum_projector_reconstruction_defect: float
    maximum_parent_retained_reconstruction_defect: float
    maximum_parent_fourier_reconstruction_defect: float
    maximum_periodic_frame_closure_defect: float
    minimum_sampled_transport_singular_value: float
    maximum_transport_procrustes_residual: float
    maximum_transport_squared_residual_roundoff_cutoff: float
    maximum_transport_unitarity_defect: float
    maximum_transport_rank_cutoff: float
    transport_rank_deficient_link_count: int
    transport_closure_and_plaquette_applicable: bool
    transport_closure_and_plaquette_inapplicable_reason: str | None
    maximum_absolute_closure_holonomy_phases: tuple[float, float] | None
    maximum_closure_holonomy_unitarity_defect: float | None
    maximum_plaquette_holonomy_phase: float | None
    maximum_direct_band_defect: float
    maximum_covariant_defect: float
    alignment_applicable: bool
    alignment_inapplicable_reason: str | None
    restricted_global_rotation_angle: float | None
    restricted_global_rotation_degenerate: bool
    splitting_scale: float
    finite_mesh_maximum_correlation: float | None
    analytic_flat_correlation: float | None
    analytic_correlation_remainder_bound: float | None
    correlation_quadrature_defect: float | None
    minimum_operator_threshold: float
    exact_spectrum_joint_operator_threshold: float
    minimum_operator_threshold_over_sqrt_splitting: float | None
    exact_spectrum_joint_threshold_over_sqrt_splitting: float | None
    normalized_squared_operator_residual: float | None
    restricted_global_rotation_residual: float
    reference_fourier_reconstruction_defect: float
    comparison_fourier_reconstruction_defect: float
    reference_parseval_defect: float
    comparison_parseval_defect: float
    reference_twisted_nyquist_defect: float
    comparison_twisted_nyquist_defect: float
    reference_ordinary_hermiticity_defect: float
    comparison_ordinary_hermiticity_defect: float
    reference_interpolation: ErrorChannels
    comparison_interpolation: ErrorChannels
    reference_total_power: float
    comparison_total_power: float
    reference_onsite_power: float
    comparison_onsite_power: float
    reference_nononsite_power: float
    comparison_nononsite_power: float
    excess_nonzero_hopping_weight: float
    normalized_excess_nonzero_hopping_weight: float | None
    flat_identity_departure: float | None
    reference_nyquist_power: float
    comparison_nyquist_power: float
    flat_residual_tail_identity_defect: float | None
    basis_distance_minimum: float | None
    basis_distance_maximum: float | None
    shell_diagnostics: tuple[ShellDiagnostic, ...]
    first_passing: tuple[FirstPassingDecision, ...]

    def __post_init__(self) -> None:
        """Reject inconsistent transport applicability and resolution evidence."""
        count = self.transport_rank_deficient_link_count
        if type(count) is not int:
            raise TypeError(
                "transport_rank_deficient_link_count must be a built-in int"
            )
        if count < 0:
            raise ValueError("transport_rank_deficient_link_count must be nonnegative")
        cutoff = self.maximum_transport_squared_residual_roundoff_cutoff
        if type(cutoff) is not float:
            raise TypeError(
                "maximum_transport_squared_residual_roundoff_cutoff must be a "
                "built-in float"
            )
        if not math.isfinite(cutoff) or cutoff < 0.0:
            raise ValueError(
                "maximum_transport_squared_residual_roundoff_cutoff must be finite "
                "and nonnegative"
            )
        applicable = self.transport_closure_and_plaquette_applicable
        if type(applicable) is not bool:
            raise TypeError(
                "transport_closure_and_plaquette_applicable must be a built-in bool"
            )
        if applicable != (count == 0):
            raise ValueError(
                "transport applicability must equal zero rank-deficient links"
            )
        topology_values = (
            self.maximum_absolute_closure_holonomy_phases,
            self.maximum_closure_holonomy_unitarity_defect,
            self.maximum_plaquette_holonomy_phase,
        )
        if applicable:
            if self.transport_closure_and_plaquette_inapplicable_reason is not None:
                raise ValueError("applicable transport must not have a reason")
            if any(value is None for value in topology_values):
                raise ValueError("applicable transport requires topology diagnostics")
        else:
            if (
                self.transport_closure_and_plaquette_inapplicable_reason
                != TRANSPORT_RANK_DEFICIENT_REASON
            ):
                raise ValueError("inapplicable transport requires the stable reason")
            if any(value is not None for value in topology_values):
                raise ValueError(
                    "inapplicable transport prohibits topology diagnostics"
                )


@dataclass(frozen=True, slots=True)
class FlatAmplitudeResolutionDiagnostic:
    """Retain analytic flat-parent midpoint interpolation defects."""

    amplitude_intervals: int
    amplitude_nodes: int
    maximum_operator_threshold_midpoint_interpolation_defect: float
    maximum_joint_threshold_midpoint_interpolation_defect: float
    passes_unit_scale_draft_tolerance: bool | None
    tolerance_inapplicable_reason: str


@dataclass(frozen=True, slots=True)
class AmplitudeMidpointDiagnostic:
    """Retain direct midpoint-versus-linear-interpolation defects."""

    amplitude_nodes: int
    applicable: bool
    inapplicable_reason: str | None
    endpoint_minimum_threshold_over_sqrt_splitting: float | None
    maximum_correlation_midpoint_defect: float | None
    maximum_operator_threshold_midpoint_defect: float | None
    maximum_joint_threshold_midpoint_defect: float | None
    maximum_nonzero_hopping_weight_midpoint_defect: float | None
    maximum_hopping_block_power_midpoint_defect: float | None


@dataclass(frozen=True, slots=True)
class CaseDiagnostic:
    """Retain all points for one independently interpreted geometry and parent."""

    name: str
    metric_covariance_defect: float
    construction_evaluation_minimum_separation: float
    amplitude_midpoint: AmplitudeMidpointDiagnostic
    flat_amplitude_resolution: tuple[FlatAmplitudeResolutionDiagnostic, ...]
    points: tuple[PointDiagnostic, ...]


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityDiagnostics:
    """Retain calculated diagnostics without artifact provenance or evidence claims."""

    family: BandEquivalenceLocalityFamily
    status: str
    construction_size: int
    evaluation_size: int
    cases: tuple[CaseDiagnostic, ...]


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityVerificationDiagnostics:
    """Retain independent numerical checks without artifact provenance."""

    family: BandEquivalenceLocalityFamily
    passes: bool
    maximum_stored_identity_defect: float
    maximum_independent_parent_defect: float
    maximum_independent_band_defect: float


__all__ = [
    "AmplitudeMidpointDiagnostic",
    "CaseDiagnostic",
    "BandEquivalenceLocalityDiagnostics",
    "BandEquivalenceLocalityVerificationDiagnostics",
    "ErrorChannels",
    "FirstPassingDecision",
    "FlatAmplitudeResolutionDiagnostic",
    "PointDiagnostic",
    "ShellDiagnostic",
]
