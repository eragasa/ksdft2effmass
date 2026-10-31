"""Plain immutable scientific values for point analysis."""

from __future__ import annotations

import math
from dataclasses import dataclass

from ksdft2effmass.representation_equivalence import RepresentationEquivalence

from ..definitions import TRANSPORT_RANK_DEFICIENT_REASON
from .channels import BandEquivalenceLocalityErrorChannels
from .shell import (
    BandEquivalenceLocalityFirstPassingDecision,
    BandEquivalenceLocalityShellAnalysis,
)


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityRepresentationEquivalenceAnalysis(
    RepresentationEquivalence
):
    """Retain gauge-equivalence and restricted-alignment diagnostics."""

    spatial_dimension: int
    retained_rank: int
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

    def __post_init__(self) -> None:
        if type(self.spatial_dimension) is not int:
            raise TypeError("spatial_dimension must be a built-in int")
        if self.spatial_dimension not in (2, 3):
            raise ValueError("spatial_dimension must be two or three")
        if type(self.retained_rank) is not int:
            raise TypeError("retained_rank must be a built-in int")
        if self.retained_rank != 2:
            raise ValueError("retained_rank must be two")
        required_nonnegative = (
            ("maximum_direct_band_defect", self.maximum_direct_band_defect),
            ("maximum_covariant_defect", self.maximum_covariant_defect),
            ("splitting_scale", self.splitting_scale),
            ("minimum_operator_threshold", self.minimum_operator_threshold),
            (
                "exact_spectrum_joint_operator_threshold",
                self.exact_spectrum_joint_operator_threshold,
            ),
        )
        for name, required_value in required_nonnegative:
            if type(required_value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(required_value) or required_value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if type(self.alignment_applicable) is not bool:
            raise TypeError("alignment_applicable must be a built-in bool")
        if (
            self.alignment_inapplicable_reason is not None
            and type(self.alignment_inapplicable_reason) is not str
        ):
            raise TypeError("alignment_inapplicable_reason must be a string or None")
        if type(self.restricted_global_rotation_degenerate) is not bool:
            raise TypeError(
                "restricted_global_rotation_degenerate must be a built-in bool"
            )
        optional_finite = (
            (
                "restricted_global_rotation_angle",
                self.restricted_global_rotation_angle,
            ),
            (
                "finite_mesh_maximum_correlation",
                self.finite_mesh_maximum_correlation,
            ),
            ("analytic_flat_correlation", self.analytic_flat_correlation),
        )
        for name, optional_value in optional_finite:
            if optional_value is not None:
                if type(optional_value) is not float:
                    raise TypeError(f"{name} must be a built-in float or None")
                if not math.isfinite(optional_value):
                    raise ValueError(f"{name} must be finite or None")
                if "correlation" in name and not -1.0 <= optional_value <= 1.0:
                    raise ValueError(f"{name} must lie in [-1, 1] or be None")
        optional_nonnegative = (
            (
                "analytic_correlation_remainder_bound",
                self.analytic_correlation_remainder_bound,
            ),
            ("correlation_quadrature_defect", self.correlation_quadrature_defect),
            (
                "minimum_operator_threshold_over_sqrt_splitting",
                self.minimum_operator_threshold_over_sqrt_splitting,
            ),
            (
                "exact_spectrum_joint_threshold_over_sqrt_splitting",
                self.exact_spectrum_joint_threshold_over_sqrt_splitting,
            ),
            (
                "normalized_squared_operator_residual",
                self.normalized_squared_operator_residual,
            ),
        )
        for name, optional_nonnegative_value in optional_nonnegative:
            if optional_nonnegative_value is not None:
                if type(optional_nonnegative_value) is not float:
                    raise TypeError(f"{name} must be a built-in float or None")
                if (
                    not math.isfinite(optional_nonnegative_value)
                    or optional_nonnegative_value < 0.0
                ):
                    raise ValueError(f"{name} must be finite and nonnegative or None")
        normalized_values = (
            self.minimum_operator_threshold_over_sqrt_splitting,
            self.exact_spectrum_joint_threshold_over_sqrt_splitting,
            self.normalized_squared_operator_residual,
        )
        if self.alignment_applicable:
            if self.alignment_inapplicable_reason is not None:
                raise ValueError("applicable alignment cannot have a reason")
            if (
                self.restricted_global_rotation_angle is None
                or self.finite_mesh_maximum_correlation is None
                or any(value is None for value in normalized_values)
            ):
                raise ValueError(
                    "applicable alignment requires rotation, correlation, and "
                    "normalized diagnostics"
                )
        else:
            if not self.alignment_inapplicable_reason:
                raise ValueError("inapplicable alignment requires a reason")
            if (
                self.restricted_global_rotation_angle is not None
                or self.finite_mesh_maximum_correlation is not None
                or any(value is not None for value in normalized_values)
            ):
                raise ValueError(
                    "inapplicable alignment prohibits rotation, correlation, and "
                    "normalized diagnostics"
                )
            if not self.restricted_global_rotation_degenerate:
                raise ValueError("inapplicable alignment must be degenerate")
        analytic_values = (
            self.analytic_flat_correlation,
            self.analytic_correlation_remainder_bound,
            self.correlation_quadrature_defect,
        )
        if any(value is None for value in analytic_values) and any(
            value is not None for value in analytic_values
        ):
            raise ValueError("analytic correlation diagnostics must be all-or-none")


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityPointAnalysis:
    """Represent one independently calculated parent-scale/amplitude point."""

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
    representation_equivalence: BandEquivalenceLocalityRepresentationEquivalenceAnalysis
    reference_fourier_reconstruction_defect: float
    comparison_fourier_reconstruction_defect: float
    reference_parseval_defect: float
    comparison_parseval_defect: float
    reference_twisted_nyquist_defect: float
    comparison_twisted_nyquist_defect: float
    reference_ordinary_hermiticity_defect: float
    comparison_ordinary_hermiticity_defect: float
    reference_interpolation: BandEquivalenceLocalityErrorChannels
    comparison_interpolation: BandEquivalenceLocalityErrorChannels
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
    shell_diagnostics: tuple[BandEquivalenceLocalityShellAnalysis, ...]
    first_passing: tuple[BandEquivalenceLocalityFirstPassingDecision, ...]

    def __post_init__(self) -> None:
        """Reject inconsistent transport applicability and resolution evidence."""
        if (
            type(self.representation_equivalence)
            is not BandEquivalenceLocalityRepresentationEquivalenceAnalysis
        ):
            raise TypeError(
                "representation_equivalence has the wrong scientific result type"
            )
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

    @property
    def maximum_direct_band_defect(self) -> float:
        """Project the historical direct-band-defect field."""
        return self.representation_equivalence.maximum_direct_band_defect

    @property
    def maximum_covariant_defect(self) -> float:
        """Project the historical covariance-defect field."""
        return self.representation_equivalence.maximum_covariant_defect

    @property
    def alignment_applicable(self) -> bool:
        """Project the historical alignment-applicability field."""
        return self.representation_equivalence.alignment_applicable

    @property
    def alignment_inapplicable_reason(self) -> str | None:
        """Project the historical alignment-inapplicability reason."""
        return self.representation_equivalence.alignment_inapplicable_reason

    @property
    def restricted_global_rotation_angle(self) -> float | None:
        """Project the historical restricted-rotation angle."""
        return self.representation_equivalence.restricted_global_rotation_angle

    @property
    def restricted_global_rotation_degenerate(self) -> bool:
        """Project the historical restricted-rotation degeneracy."""
        return self.representation_equivalence.restricted_global_rotation_degenerate

    @property
    def splitting_scale(self) -> float:
        """Project the historical splitting-scale field."""
        return self.representation_equivalence.splitting_scale

    @property
    def finite_mesh_maximum_correlation(self) -> float | None:
        """Project the historical finite-mesh correlation."""
        return self.representation_equivalence.finite_mesh_maximum_correlation

    @property
    def analytic_flat_correlation(self) -> float | None:
        """Project the historical analytic flat-parent correlation."""
        return self.representation_equivalence.analytic_flat_correlation

    @property
    def analytic_correlation_remainder_bound(self) -> float | None:
        """Project the historical analytic remainder bound."""
        return self.representation_equivalence.analytic_correlation_remainder_bound

    @property
    def correlation_quadrature_defect(self) -> float | None:
        """Project the historical correlation quadrature defect."""
        return self.representation_equivalence.correlation_quadrature_defect

    @property
    def minimum_operator_threshold(self) -> float:
        """Project the historical minimum operator threshold."""
        return self.representation_equivalence.minimum_operator_threshold

    @property
    def exact_spectrum_joint_operator_threshold(self) -> float:
        """Project the historical exact-spectrum joint threshold."""
        return self.representation_equivalence.exact_spectrum_joint_operator_threshold

    @property
    def minimum_operator_threshold_over_sqrt_splitting(self) -> float | None:
        """Project the historical normalized operator threshold."""
        result = self.representation_equivalence
        return result.minimum_operator_threshold_over_sqrt_splitting

    @property
    def exact_spectrum_joint_threshold_over_sqrt_splitting(self) -> float | None:
        """Project the historical normalized exact-spectrum threshold."""
        result = self.representation_equivalence
        return result.exact_spectrum_joint_threshold_over_sqrt_splitting

    @property
    def normalized_squared_operator_residual(self) -> float | None:
        """Project the historical normalized squared operator residual."""
        return self.representation_equivalence.normalized_squared_operator_residual

    @property
    def restricted_global_rotation_residual(self) -> float:
        """Project the historical restricted-rotation residual alias."""
        return self.representation_equivalence.minimum_operator_threshold
