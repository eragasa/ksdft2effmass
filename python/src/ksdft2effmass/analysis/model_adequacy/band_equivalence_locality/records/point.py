"""Point-resolved band-equivalence locality result values."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from ..definitions import TRANSPORT_RANK_DEFICIENT_REASON
from ..results import BandEquivalenceLocalityPointAnalysis
from .channels import ErrorChannels
from .shell import FirstPassingDecision, ShellDiagnostic


@dataclass(frozen=True, slots=True)
class PointDiagnostic(BaseTypedRecord):
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
            raise TypeError("invalid field: transport_rank_deficient_link_count")
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
            raise TypeError("invalid field: transport_closure_and_plaquette_applicable")
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

    @classmethod
    def from_analysis(cls, analysis: BandEquivalenceLocalityPointAnalysis) -> Self:
        """Project one plain scientific point into a retained record."""
        if type(analysis) is not BandEquivalenceLocalityPointAnalysis:
            raise TypeError("analysis must be BandEquivalenceLocalityPointAnalysis")
        return cls(
            parent_scale=analysis.parent_scale,
            amplitude=analysis.amplitude,
            minimum_sampled_external_gap=analysis.minimum_sampled_external_gap,
            continuous_external_gap_lower_bound=analysis.continuous_external_gap_lower_bound,
            minimum_seed_overlap=analysis.minimum_seed_overlap,
            maximum_parent_hermiticity_defect=analysis.maximum_parent_hermiticity_defect,
            maximum_eigensystem_reconstruction_defect=analysis.maximum_eigensystem_reconstruction_defect,
            maximum_frame_orthonormality_defect=analysis.maximum_frame_orthonormality_defect,
            maximum_projector_reconstruction_defect=analysis.maximum_projector_reconstruction_defect,
            maximum_parent_retained_reconstruction_defect=analysis.maximum_parent_retained_reconstruction_defect,
            maximum_parent_fourier_reconstruction_defect=analysis.maximum_parent_fourier_reconstruction_defect,
            maximum_periodic_frame_closure_defect=analysis.maximum_periodic_frame_closure_defect,
            minimum_sampled_transport_singular_value=analysis.minimum_sampled_transport_singular_value,
            maximum_transport_procrustes_residual=analysis.maximum_transport_procrustes_residual,
            maximum_transport_squared_residual_roundoff_cutoff=analysis.maximum_transport_squared_residual_roundoff_cutoff,
            maximum_transport_unitarity_defect=analysis.maximum_transport_unitarity_defect,
            maximum_transport_rank_cutoff=analysis.maximum_transport_rank_cutoff,
            transport_rank_deficient_link_count=analysis.transport_rank_deficient_link_count,
            transport_closure_and_plaquette_applicable=analysis.transport_closure_and_plaquette_applicable,
            transport_closure_and_plaquette_inapplicable_reason=analysis.transport_closure_and_plaquette_inapplicable_reason,
            maximum_absolute_closure_holonomy_phases=analysis.maximum_absolute_closure_holonomy_phases,
            maximum_closure_holonomy_unitarity_defect=analysis.maximum_closure_holonomy_unitarity_defect,
            maximum_plaquette_holonomy_phase=analysis.maximum_plaquette_holonomy_phase,
            maximum_direct_band_defect=analysis.maximum_direct_band_defect,
            maximum_covariant_defect=analysis.maximum_covariant_defect,
            alignment_applicable=analysis.alignment_applicable,
            alignment_inapplicable_reason=analysis.alignment_inapplicable_reason,
            restricted_global_rotation_angle=analysis.restricted_global_rotation_angle,
            restricted_global_rotation_degenerate=analysis.restricted_global_rotation_degenerate,
            splitting_scale=analysis.splitting_scale,
            finite_mesh_maximum_correlation=analysis.finite_mesh_maximum_correlation,
            analytic_flat_correlation=analysis.analytic_flat_correlation,
            analytic_correlation_remainder_bound=analysis.analytic_correlation_remainder_bound,
            correlation_quadrature_defect=analysis.correlation_quadrature_defect,
            minimum_operator_threshold=analysis.minimum_operator_threshold,
            exact_spectrum_joint_operator_threshold=analysis.exact_spectrum_joint_operator_threshold,
            minimum_operator_threshold_over_sqrt_splitting=analysis.minimum_operator_threshold_over_sqrt_splitting,
            exact_spectrum_joint_threshold_over_sqrt_splitting=analysis.exact_spectrum_joint_threshold_over_sqrt_splitting,
            normalized_squared_operator_residual=analysis.normalized_squared_operator_residual,
            restricted_global_rotation_residual=analysis.restricted_global_rotation_residual,
            reference_fourier_reconstruction_defect=analysis.reference_fourier_reconstruction_defect,
            comparison_fourier_reconstruction_defect=analysis.comparison_fourier_reconstruction_defect,
            reference_parseval_defect=analysis.reference_parseval_defect,
            comparison_parseval_defect=analysis.comparison_parseval_defect,
            reference_twisted_nyquist_defect=analysis.reference_twisted_nyquist_defect,
            comparison_twisted_nyquist_defect=analysis.comparison_twisted_nyquist_defect,
            reference_ordinary_hermiticity_defect=analysis.reference_ordinary_hermiticity_defect,
            comparison_ordinary_hermiticity_defect=analysis.comparison_ordinary_hermiticity_defect,
            reference_interpolation=ErrorChannels.from_analysis(
                analysis.reference_interpolation
            ),
            comparison_interpolation=ErrorChannels.from_analysis(
                analysis.comparison_interpolation
            ),
            reference_total_power=analysis.reference_total_power,
            comparison_total_power=analysis.comparison_total_power,
            reference_onsite_power=analysis.reference_onsite_power,
            comparison_onsite_power=analysis.comparison_onsite_power,
            reference_nononsite_power=analysis.reference_nononsite_power,
            comparison_nononsite_power=analysis.comparison_nononsite_power,
            excess_nonzero_hopping_weight=analysis.excess_nonzero_hopping_weight,
            normalized_excess_nonzero_hopping_weight=analysis.normalized_excess_nonzero_hopping_weight,
            flat_identity_departure=analysis.flat_identity_departure,
            reference_nyquist_power=analysis.reference_nyquist_power,
            comparison_nyquist_power=analysis.comparison_nyquist_power,
            flat_residual_tail_identity_defect=analysis.flat_residual_tail_identity_defect,
            basis_distance_minimum=analysis.basis_distance_minimum,
            basis_distance_maximum=analysis.basis_distance_maximum,
            shell_diagnostics=tuple(
                ShellDiagnostic.from_analysis(value)
                for value in analysis.shell_diagnostics
            ),
            first_passing=tuple(
                FirstPassingDecision.from_analysis(value)
                for value in analysis.first_passing
            ),
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "parent_scale": self.parent_scale,
            "amplitude": self.amplitude,
            "minimum_sampled_external_gap": self.minimum_sampled_external_gap,
            "continuous_external_gap_lower_bound": (
                self.continuous_external_gap_lower_bound
            ),
            "minimum_seed_overlap": self.minimum_seed_overlap,
            "maximum_parent_hermiticity_defect": self.maximum_parent_hermiticity_defect,
            "maximum_eigensystem_reconstruction_defect": (
                self.maximum_eigensystem_reconstruction_defect
            ),
            "maximum_frame_orthonormality_defect": (
                self.maximum_frame_orthonormality_defect
            ),
            "maximum_projector_reconstruction_defect": (
                self.maximum_projector_reconstruction_defect
            ),
            "maximum_parent_retained_reconstruction_defect": (
                self.maximum_parent_retained_reconstruction_defect
            ),
            "maximum_parent_fourier_reconstruction_defect": (
                self.maximum_parent_fourier_reconstruction_defect
            ),
            "maximum_periodic_frame_closure_defect": (
                self.maximum_periodic_frame_closure_defect
            ),
            "minimum_sampled_transport_singular_value": (
                self.minimum_sampled_transport_singular_value
            ),
            "maximum_transport_procrustes_residual": (
                self.maximum_transport_procrustes_residual
            ),
            "maximum_transport_squared_residual_roundoff_cutoff": (
                self.maximum_transport_squared_residual_roundoff_cutoff
            ),
            "maximum_transport_unitarity_defect": (
                self.maximum_transport_unitarity_defect
            ),
            "maximum_transport_rank_cutoff": self.maximum_transport_rank_cutoff,
            "transport_rank_deficient_link_count": (
                self.transport_rank_deficient_link_count
            ),
            "transport_closure_and_plaquette_applicable": (
                self.transport_closure_and_plaquette_applicable
            ),
            "transport_closure_and_plaquette_inapplicable_reason": (
                self.transport_closure_and_plaquette_inapplicable_reason
            ),
            "maximum_absolute_closure_holonomy_phases": (
                self.maximum_absolute_closure_holonomy_phases
            ),
            "maximum_closure_holonomy_unitarity_defect": (
                self.maximum_closure_holonomy_unitarity_defect
            ),
            "maximum_plaquette_holonomy_phase": self.maximum_plaquette_holonomy_phase,
            "maximum_direct_band_defect": self.maximum_direct_band_defect,
            "maximum_covariant_defect": self.maximum_covariant_defect,
            "alignment_applicable": self.alignment_applicable,
            "alignment_inapplicable_reason": self.alignment_inapplicable_reason,
            "restricted_global_rotation_angle": self.restricted_global_rotation_angle,
            "restricted_global_rotation_degenerate": (
                self.restricted_global_rotation_degenerate
            ),
            "splitting_scale": self.splitting_scale,
            "finite_mesh_maximum_correlation": self.finite_mesh_maximum_correlation,
            "analytic_flat_correlation": self.analytic_flat_correlation,
            "analytic_correlation_remainder_bound": (
                self.analytic_correlation_remainder_bound
            ),
            "correlation_quadrature_defect": self.correlation_quadrature_defect,
            "minimum_operator_threshold": self.minimum_operator_threshold,
            "exact_spectrum_joint_operator_threshold": (
                self.exact_spectrum_joint_operator_threshold
            ),
            "minimum_operator_threshold_over_sqrt_splitting": (
                self.minimum_operator_threshold_over_sqrt_splitting
            ),
            "exact_spectrum_joint_threshold_over_sqrt_splitting": (
                self.exact_spectrum_joint_threshold_over_sqrt_splitting
            ),
            "normalized_squared_operator_residual": (
                self.normalized_squared_operator_residual
            ),
            "restricted_global_rotation_residual": (
                self.restricted_global_rotation_residual
            ),
            "reference_fourier_reconstruction_defect": (
                self.reference_fourier_reconstruction_defect
            ),
            "comparison_fourier_reconstruction_defect": (
                self.comparison_fourier_reconstruction_defect
            ),
            "reference_parseval_defect": self.reference_parseval_defect,
            "comparison_parseval_defect": self.comparison_parseval_defect,
            "reference_twisted_nyquist_defect": self.reference_twisted_nyquist_defect,
            "comparison_twisted_nyquist_defect": self.comparison_twisted_nyquist_defect,
            "reference_ordinary_hermiticity_defect": (
                self.reference_ordinary_hermiticity_defect
            ),
            "comparison_ordinary_hermiticity_defect": (
                self.comparison_ordinary_hermiticity_defect
            ),
            "reference_interpolation": self.reference_interpolation,
            "comparison_interpolation": self.comparison_interpolation,
            "reference_total_power": self.reference_total_power,
            "comparison_total_power": self.comparison_total_power,
            "reference_onsite_power": self.reference_onsite_power,
            "comparison_onsite_power": self.comparison_onsite_power,
            "reference_nononsite_power": self.reference_nononsite_power,
            "comparison_nononsite_power": self.comparison_nononsite_power,
            "excess_nonzero_hopping_weight": self.excess_nonzero_hopping_weight,
            "normalized_excess_nonzero_hopping_weight": (
                self.normalized_excess_nonzero_hopping_weight
            ),
            "flat_identity_departure": self.flat_identity_departure,
            "reference_nyquist_power": self.reference_nyquist_power,
            "comparison_nyquist_power": self.comparison_nyquist_power,
            "flat_residual_tail_identity_defect": (
                self.flat_residual_tail_identity_defect
            ),
            "basis_distance_minimum": self.basis_distance_minimum,
            "basis_distance_maximum": self.basis_distance_maximum,
            "shell_diagnostics": self.shell_diagnostics,
            "first_passing": self.first_passing,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "parent_scale",
            "amplitude",
            "minimum_sampled_external_gap",
            "continuous_external_gap_lower_bound",
            "minimum_seed_overlap",
            "maximum_parent_hermiticity_defect",
            "maximum_eigensystem_reconstruction_defect",
            "maximum_frame_orthonormality_defect",
            "maximum_projector_reconstruction_defect",
            "maximum_parent_retained_reconstruction_defect",
            "maximum_parent_fourier_reconstruction_defect",
            "maximum_periodic_frame_closure_defect",
            "minimum_sampled_transport_singular_value",
            "maximum_transport_procrustes_residual",
            "maximum_transport_squared_residual_roundoff_cutoff",
            "maximum_transport_unitarity_defect",
            "maximum_transport_rank_cutoff",
            "transport_rank_deficient_link_count",
            "transport_closure_and_plaquette_applicable",
            "transport_closure_and_plaquette_inapplicable_reason",
            "maximum_absolute_closure_holonomy_phases",
            "maximum_closure_holonomy_unitarity_defect",
            "maximum_plaquette_holonomy_phase",
            "maximum_direct_band_defect",
            "maximum_covariant_defect",
            "alignment_applicable",
            "alignment_inapplicable_reason",
            "restricted_global_rotation_angle",
            "restricted_global_rotation_degenerate",
            "splitting_scale",
            "finite_mesh_maximum_correlation",
            "analytic_flat_correlation",
            "analytic_correlation_remainder_bound",
            "correlation_quadrature_defect",
            "minimum_operator_threshold",
            "exact_spectrum_joint_operator_threshold",
            "minimum_operator_threshold_over_sqrt_splitting",
            "exact_spectrum_joint_threshold_over_sqrt_splitting",
            "normalized_squared_operator_residual",
            "restricted_global_rotation_residual",
            "reference_fourier_reconstruction_defect",
            "comparison_fourier_reconstruction_defect",
            "reference_parseval_defect",
            "comparison_parseval_defect",
            "reference_twisted_nyquist_defect",
            "comparison_twisted_nyquist_defect",
            "reference_ordinary_hermiticity_defect",
            "comparison_ordinary_hermiticity_defect",
            "reference_interpolation",
            "comparison_interpolation",
            "reference_total_power",
            "comparison_total_power",
            "reference_onsite_power",
            "comparison_onsite_power",
            "reference_nononsite_power",
            "comparison_nononsite_power",
            "excess_nonzero_hopping_weight",
            "normalized_excess_nonzero_hopping_weight",
            "flat_identity_departure",
            "reference_nyquist_power",
            "comparison_nyquist_power",
            "flat_residual_tail_identity_defect",
            "basis_distance_minimum",
            "basis_distance_maximum",
            "shell_diagnostics",
            "first_passing",
        }
        if set(values) != required:
            raise ValueError("PointDiagnostic fields do not match")
        parent_scale = values["parent_scale"]
        amplitude = values["amplitude"]
        minimum_sampled_external_gap = values["minimum_sampled_external_gap"]
        continuous_external_gap_lower_bound = values[
            "continuous_external_gap_lower_bound"
        ]
        minimum_seed_overlap = values["minimum_seed_overlap"]
        maximum_parent_hermiticity_defect = values["maximum_parent_hermiticity_defect"]
        maximum_eigensystem_reconstruction_defect = values[
            "maximum_eigensystem_reconstruction_defect"
        ]
        maximum_frame_orthonormality_defect = values[
            "maximum_frame_orthonormality_defect"
        ]
        maximum_projector_reconstruction_defect = values[
            "maximum_projector_reconstruction_defect"
        ]
        maximum_parent_retained_reconstruction_defect = values[
            "maximum_parent_retained_reconstruction_defect"
        ]
        maximum_parent_fourier_reconstruction_defect = values[
            "maximum_parent_fourier_reconstruction_defect"
        ]
        maximum_periodic_frame_closure_defect = values[
            "maximum_periodic_frame_closure_defect"
        ]
        minimum_sampled_transport_singular_value = values[
            "minimum_sampled_transport_singular_value"
        ]
        maximum_transport_procrustes_residual = values[
            "maximum_transport_procrustes_residual"
        ]
        maximum_transport_squared_residual_roundoff_cutoff = values[
            "maximum_transport_squared_residual_roundoff_cutoff"
        ]
        maximum_transport_unitarity_defect = values[
            "maximum_transport_unitarity_defect"
        ]
        maximum_transport_rank_cutoff = values["maximum_transport_rank_cutoff"]
        maximum_direct_band_defect = values["maximum_direct_band_defect"]
        maximum_covariant_defect = values["maximum_covariant_defect"]
        splitting_scale = values["splitting_scale"]
        minimum_operator_threshold = values["minimum_operator_threshold"]
        exact_spectrum_joint_operator_threshold = values[
            "exact_spectrum_joint_operator_threshold"
        ]
        restricted_global_rotation_residual = values[
            "restricted_global_rotation_residual"
        ]
        reference_fourier_reconstruction_defect = values[
            "reference_fourier_reconstruction_defect"
        ]
        comparison_fourier_reconstruction_defect = values[
            "comparison_fourier_reconstruction_defect"
        ]
        reference_parseval_defect = values["reference_parseval_defect"]
        comparison_parseval_defect = values["comparison_parseval_defect"]
        reference_twisted_nyquist_defect = values["reference_twisted_nyquist_defect"]
        comparison_twisted_nyquist_defect = values["comparison_twisted_nyquist_defect"]
        reference_ordinary_hermiticity_defect = values[
            "reference_ordinary_hermiticity_defect"
        ]
        comparison_ordinary_hermiticity_defect = values[
            "comparison_ordinary_hermiticity_defect"
        ]
        reference_total_power = values["reference_total_power"]
        comparison_total_power = values["comparison_total_power"]
        reference_onsite_power = values["reference_onsite_power"]
        comparison_onsite_power = values["comparison_onsite_power"]
        reference_nononsite_power = values["reference_nononsite_power"]
        comparison_nononsite_power = values["comparison_nononsite_power"]
        excess_nonzero_hopping_weight = values["excess_nonzero_hopping_weight"]
        reference_nyquist_power = values["reference_nyquist_power"]
        comparison_nyquist_power = values["comparison_nyquist_power"]
        transport_rank_deficient_link_count = values[
            "transport_rank_deficient_link_count"
        ]
        transport_closure_and_plaquette_applicable = values[
            "transport_closure_and_plaquette_applicable"
        ]
        alignment_applicable = values["alignment_applicable"]
        restricted_global_rotation_degenerate = values[
            "restricted_global_rotation_degenerate"
        ]
        transport_closure_and_plaquette_inapplicable_reason = values[
            "transport_closure_and_plaquette_inapplicable_reason"
        ]
        alignment_inapplicable_reason = values["alignment_inapplicable_reason"]
        maximum_absolute_closure_holonomy_phases = values[
            "maximum_absolute_closure_holonomy_phases"
        ]
        maximum_closure_holonomy_unitarity_defect = values[
            "maximum_closure_holonomy_unitarity_defect"
        ]
        maximum_plaquette_holonomy_phase = values["maximum_plaquette_holonomy_phase"]
        restricted_global_rotation_angle = values["restricted_global_rotation_angle"]
        finite_mesh_maximum_correlation = values["finite_mesh_maximum_correlation"]
        analytic_flat_correlation = values["analytic_flat_correlation"]
        analytic_correlation_remainder_bound = values[
            "analytic_correlation_remainder_bound"
        ]
        correlation_quadrature_defect = values["correlation_quadrature_defect"]
        minimum_operator_threshold_over_sqrt_splitting = values[
            "minimum_operator_threshold_over_sqrt_splitting"
        ]
        exact_spectrum_joint_threshold_over_sqrt_splitting = values[
            "exact_spectrum_joint_threshold_over_sqrt_splitting"
        ]
        normalized_squared_operator_residual = values[
            "normalized_squared_operator_residual"
        ]
        normalized_excess_nonzero_hopping_weight = values[
            "normalized_excess_nonzero_hopping_weight"
        ]
        flat_identity_departure = values["flat_identity_departure"]
        flat_residual_tail_identity_defect = values[
            "flat_residual_tail_identity_defect"
        ]
        basis_distance_minimum = values["basis_distance_minimum"]
        basis_distance_maximum = values["basis_distance_maximum"]
        reference_interpolation_value = values["reference_interpolation"]
        comparison_interpolation_value = values["comparison_interpolation"]
        shell_diagnostics_values = values["shell_diagnostics"]
        first_passing_values = values["first_passing"]
        if (
            type(parent_scale) is not float
            or type(amplitude) is not float
            or type(minimum_sampled_external_gap) is not float
            or type(continuous_external_gap_lower_bound) is not float
            or type(minimum_seed_overlap) is not float
            or type(maximum_parent_hermiticity_defect) is not float
            or type(maximum_eigensystem_reconstruction_defect) is not float
            or type(maximum_frame_orthonormality_defect) is not float
            or type(maximum_projector_reconstruction_defect) is not float
            or type(maximum_parent_retained_reconstruction_defect) is not float
            or type(maximum_parent_fourier_reconstruction_defect) is not float
            or type(maximum_periodic_frame_closure_defect) is not float
            or type(minimum_sampled_transport_singular_value) is not float
            or type(maximum_transport_procrustes_residual) is not float
            or type(maximum_transport_squared_residual_roundoff_cutoff) is not float
            or type(maximum_transport_unitarity_defect) is not float
            or type(maximum_transport_rank_cutoff) is not float
            or type(maximum_direct_band_defect) is not float
            or type(maximum_covariant_defect) is not float
            or type(splitting_scale) is not float
            or type(minimum_operator_threshold) is not float
            or type(exact_spectrum_joint_operator_threshold) is not float
            or type(restricted_global_rotation_residual) is not float
            or type(reference_fourier_reconstruction_defect) is not float
            or type(comparison_fourier_reconstruction_defect) is not float
            or type(reference_parseval_defect) is not float
            or type(comparison_parseval_defect) is not float
            or type(reference_twisted_nyquist_defect) is not float
            or type(comparison_twisted_nyquist_defect) is not float
            or type(reference_ordinary_hermiticity_defect) is not float
            or type(comparison_ordinary_hermiticity_defect) is not float
            or type(reference_total_power) is not float
            or type(comparison_total_power) is not float
            or type(reference_onsite_power) is not float
            or type(comparison_onsite_power) is not float
            or type(reference_nononsite_power) is not float
            or type(comparison_nononsite_power) is not float
            or type(excess_nonzero_hopping_weight) is not float
            or type(reference_nyquist_power) is not float
            or type(comparison_nyquist_power) is not float
        ):
            raise TypeError("float fields must use exact built-in types")
        if type(transport_rank_deficient_link_count) is not int:
            raise TypeError("integer fields must use exact built-in types")
        if (
            type(transport_closure_and_plaquette_applicable) is not bool
            or type(alignment_applicable) is not bool
            or type(restricted_global_rotation_degenerate) is not bool
        ):
            raise TypeError("Boolean fields must use exact built-in types")
        if (
            (
                maximum_closure_holonomy_unitarity_defect is not None
                and type(maximum_closure_holonomy_unitarity_defect) is not float
            )
            or (
                maximum_plaquette_holonomy_phase is not None
                and type(maximum_plaquette_holonomy_phase) is not float
            )
            or (
                restricted_global_rotation_angle is not None
                and type(restricted_global_rotation_angle) is not float
            )
            or (
                finite_mesh_maximum_correlation is not None
                and type(finite_mesh_maximum_correlation) is not float
            )
            or (
                analytic_flat_correlation is not None
                and type(analytic_flat_correlation) is not float
            )
            or (
                analytic_correlation_remainder_bound is not None
                and type(analytic_correlation_remainder_bound) is not float
            )
            or (
                correlation_quadrature_defect is not None
                and type(correlation_quadrature_defect) is not float
            )
            or (
                minimum_operator_threshold_over_sqrt_splitting is not None
                and type(minimum_operator_threshold_over_sqrt_splitting) is not float
            )
            or (
                exact_spectrum_joint_threshold_over_sqrt_splitting is not None
                and type(exact_spectrum_joint_threshold_over_sqrt_splitting)
                is not float
            )
            or (
                normalized_squared_operator_residual is not None
                and type(normalized_squared_operator_residual) is not float
            )
            or (
                normalized_excess_nonzero_hopping_weight is not None
                and type(normalized_excess_nonzero_hopping_weight) is not float
            )
            or (
                flat_identity_departure is not None
                and type(flat_identity_departure) is not float
            )
            or (
                flat_residual_tail_identity_defect is not None
                and type(flat_residual_tail_identity_defect) is not float
            )
            or (
                basis_distance_minimum is not None
                and type(basis_distance_minimum) is not float
            )
            or (
                basis_distance_maximum is not None
                and type(basis_distance_maximum) is not float
            )
        ):
            raise TypeError("optional float fields have invalid types")
        if (
            transport_closure_and_plaquette_inapplicable_reason is not None
            and type(transport_closure_and_plaquette_inapplicable_reason) is not str
        ) or (
            alignment_inapplicable_reason is not None
            and type(alignment_inapplicable_reason) is not str
        ):
            raise TypeError("optional string fields have invalid types")
        if maximum_absolute_closure_holonomy_phases is not None and (
            not isinstance(maximum_absolute_closure_holonomy_phases, tuple)
            or len(maximum_absolute_closure_holonomy_phases) != 2
            or any(
                type(item) is not float
                for item in maximum_absolute_closure_holonomy_phases
            )
        ):
            raise TypeError("holonomy phases must decode to a float pair")
        if not isinstance(reference_interpolation_value, Mapping):
            raise TypeError("reference_interpolation must decode to a mapping")
        if not isinstance(comparison_interpolation_value, Mapping):
            raise TypeError("comparison_interpolation must decode to a mapping")
        if not isinstance(shell_diagnostics_values, tuple) or any(
            not isinstance(item, Mapping) for item in shell_diagnostics_values
        ):
            raise TypeError("shell_diagnostics must decode to a tuple of mappings")
        if not isinstance(first_passing_values, tuple) or any(
            not isinstance(item, Mapping) for item in first_passing_values
        ):
            raise TypeError("first_passing must decode to a tuple of mappings")
        return cls(
            parent_scale=parent_scale,
            amplitude=amplitude,
            minimum_sampled_external_gap=minimum_sampled_external_gap,
            continuous_external_gap_lower_bound=continuous_external_gap_lower_bound,
            minimum_seed_overlap=minimum_seed_overlap,
            maximum_parent_hermiticity_defect=maximum_parent_hermiticity_defect,
            maximum_eigensystem_reconstruction_defect=maximum_eigensystem_reconstruction_defect,
            maximum_frame_orthonormality_defect=maximum_frame_orthonormality_defect,
            maximum_projector_reconstruction_defect=maximum_projector_reconstruction_defect,
            maximum_parent_retained_reconstruction_defect=maximum_parent_retained_reconstruction_defect,
            maximum_parent_fourier_reconstruction_defect=maximum_parent_fourier_reconstruction_defect,
            maximum_periodic_frame_closure_defect=maximum_periodic_frame_closure_defect,
            minimum_sampled_transport_singular_value=minimum_sampled_transport_singular_value,
            maximum_transport_procrustes_residual=maximum_transport_procrustes_residual,
            maximum_transport_squared_residual_roundoff_cutoff=maximum_transport_squared_residual_roundoff_cutoff,
            maximum_transport_unitarity_defect=maximum_transport_unitarity_defect,
            maximum_transport_rank_cutoff=maximum_transport_rank_cutoff,
            transport_rank_deficient_link_count=transport_rank_deficient_link_count,
            transport_closure_and_plaquette_applicable=transport_closure_and_plaquette_applicable,
            transport_closure_and_plaquette_inapplicable_reason=transport_closure_and_plaquette_inapplicable_reason,
            maximum_absolute_closure_holonomy_phases=maximum_absolute_closure_holonomy_phases,
            maximum_closure_holonomy_unitarity_defect=maximum_closure_holonomy_unitarity_defect,
            maximum_plaquette_holonomy_phase=maximum_plaquette_holonomy_phase,
            maximum_direct_band_defect=maximum_direct_band_defect,
            maximum_covariant_defect=maximum_covariant_defect,
            alignment_applicable=alignment_applicable,
            alignment_inapplicable_reason=alignment_inapplicable_reason,
            restricted_global_rotation_angle=restricted_global_rotation_angle,
            restricted_global_rotation_degenerate=restricted_global_rotation_degenerate,
            splitting_scale=splitting_scale,
            finite_mesh_maximum_correlation=finite_mesh_maximum_correlation,
            analytic_flat_correlation=analytic_flat_correlation,
            analytic_correlation_remainder_bound=analytic_correlation_remainder_bound,
            correlation_quadrature_defect=correlation_quadrature_defect,
            minimum_operator_threshold=minimum_operator_threshold,
            exact_spectrum_joint_operator_threshold=exact_spectrum_joint_operator_threshold,
            minimum_operator_threshold_over_sqrt_splitting=minimum_operator_threshold_over_sqrt_splitting,
            exact_spectrum_joint_threshold_over_sqrt_splitting=exact_spectrum_joint_threshold_over_sqrt_splitting,
            normalized_squared_operator_residual=normalized_squared_operator_residual,
            restricted_global_rotation_residual=restricted_global_rotation_residual,
            reference_fourier_reconstruction_defect=reference_fourier_reconstruction_defect,
            comparison_fourier_reconstruction_defect=comparison_fourier_reconstruction_defect,
            reference_parseval_defect=reference_parseval_defect,
            comparison_parseval_defect=comparison_parseval_defect,
            reference_twisted_nyquist_defect=reference_twisted_nyquist_defect,
            comparison_twisted_nyquist_defect=comparison_twisted_nyquist_defect,
            reference_ordinary_hermiticity_defect=reference_ordinary_hermiticity_defect,
            comparison_ordinary_hermiticity_defect=comparison_ordinary_hermiticity_defect,
            reference_interpolation=ErrorChannels.from_dict(
                reference_interpolation_value
            ),
            comparison_interpolation=ErrorChannels.from_dict(
                comparison_interpolation_value
            ),
            reference_total_power=reference_total_power,
            comparison_total_power=comparison_total_power,
            reference_onsite_power=reference_onsite_power,
            comparison_onsite_power=comparison_onsite_power,
            reference_nononsite_power=reference_nononsite_power,
            comparison_nononsite_power=comparison_nononsite_power,
            excess_nonzero_hopping_weight=excess_nonzero_hopping_weight,
            normalized_excess_nonzero_hopping_weight=normalized_excess_nonzero_hopping_weight,
            flat_identity_departure=flat_identity_departure,
            reference_nyquist_power=reference_nyquist_power,
            comparison_nyquist_power=comparison_nyquist_power,
            flat_residual_tail_identity_defect=flat_residual_tail_identity_defect,
            basis_distance_minimum=basis_distance_minimum,
            basis_distance_maximum=basis_distance_maximum,
            shell_diagnostics=tuple(
                ShellDiagnostic.from_dict(item) for item in shell_diagnostics_values
            ),
            first_passing=tuple(
                FirstPassingDecision.from_dict(item) for item in first_passing_values
            ),
        )
