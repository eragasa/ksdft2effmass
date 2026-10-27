"""Definitions for the exploratory smooth non-flat four-state realization."""

from __future__ import annotations

import math
from dataclasses import dataclass

from .._validation import _finite_float

SMOOTH_FOUR_STATE_METHOD_ID = "nonflat-four-state-smooth-sinusoidal-gauge.v1"
SMOOTH_FOUR_STATE_PARENT_ID = "specified-finite-range-four-state-parent.v1"
SMOOTH_FOUR_STATE_INPUT_SCHEMA_ID = (
    "ksdft2effmass.campaign.model-adequacy.periodic1d."
    "band-equivalence-versus-hopping-locality.nonflat.input.v0"
)
SMOOTH_FOUR_STATE_RESULT_SCHEMA_ID = (
    "ksdft2effmass.campaign.model-adequacy.periodic1d."
    "band-equivalence-versus-hopping-locality.nonflat.result.v0"
)
SMOOTH_FOUR_STATE_VERIFICATION_SCHEMA_ID = (
    "ksdft2effmass.campaign.model-adequacy.periodic1d."
    "band-equivalence-versus-hopping-locality.nonflat.verification.v0"
)


@dataclass(frozen=True, slots=True)
class SmoothFourStateDefinition:
    """Define one exploratory non-flat four-state calculation.

    All energy-valued parent matrices are normalized by the positive scale ``E_ref``.
    Caller-supplied thresholds are numerical controls, not physical error bars. Numeric
    controls are finite built-in binary64 floats; booleans, strings, nonfinite values,
    and values that cannot already be represented as floats are rejected rather than
    coerced or saturated. Gap and neighbor-transport bounds apply to the declared
    construction samples; they are not continuous-Brillouin-zone certificates.
    """

    reciprocal_mesh_size: int
    amplitudes: tuple[float, ...]
    minimum_external_gap: float
    minimum_transport_singular_value: float
    frame_absolute_tolerance: float
    harmonic_absolute_degeneracy_tolerance: float
    harmonic_relative_degeneracy_tolerance: float
    verification_absolute_tolerance: float
    parent_hopping_scale: float

    def __post_init__(self) -> None:
        """Reject incomplete meshes and unreviewable numerical controls."""
        if type(self.reciprocal_mesh_size) is not int:
            raise TypeError("reciprocal_mesh_size must be a built-in int")
        if self.reciprocal_mesh_size < 8:
            raise ValueError("reciprocal_mesh_size must be at least eight")
        if self.reciprocal_mesh_size % 2 != 0:
            raise ValueError("reciprocal_mesh_size must be even")
        if type(self.amplitudes) is not tuple or len(self.amplitudes) < 2:
            raise TypeError("amplitudes must contain at least two built-in floats")
        for index, amplitude in enumerate(self.amplitudes):
            _finite_float(f"amplitudes[{index}]", amplitude)
            if amplitude < 0.0 or amplitude > math.pi / 4.0:
                raise ValueError("amplitudes must lie in [0, pi/4]")
        if self.amplitudes[0] != 0.0:
            raise ValueError("amplitudes must begin at zero")
        if tuple(sorted(set(self.amplitudes))) != self.amplitudes:
            raise ValueError("amplitudes must be unique and strictly increasing")
        for name, value in (
            ("minimum_external_gap", self.minimum_external_gap),
            (
                "minimum_transport_singular_value",
                self.minimum_transport_singular_value,
            ),
            ("frame_absolute_tolerance", self.frame_absolute_tolerance),
            (
                "harmonic_absolute_degeneracy_tolerance",
                self.harmonic_absolute_degeneracy_tolerance,
            ),
            (
                "harmonic_relative_degeneracy_tolerance",
                self.harmonic_relative_degeneracy_tolerance,
            ),
            ("verification_absolute_tolerance", self.verification_absolute_tolerance),
            ("parent_hopping_scale", self.parent_hopping_scale),
        ):
            _finite_float(name, value)
            if value < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        if not 0.0 <= self.parent_hopping_scale <= 1.0:
            raise ValueError("parent_hopping_scale must lie in [0, 1]")
        if self.minimum_external_gap == 0.0:
            raise ValueError("minimum_external_gap must be positive")
        if not 0.0 < self.minimum_transport_singular_value <= 1.0:
            raise ValueError("minimum_transport_singular_value must lie in (0, 1]")
        if self.frame_absolute_tolerance == 0.0:
            raise ValueError("frame_absolute_tolerance must be positive")
        if (
            self.harmonic_absolute_degeneracy_tolerance == 0.0
            and self.harmonic_relative_degeneracy_tolerance == 0.0
        ):
            raise ValueError(
                "at least one harmonic degeneracy tolerance must be positive"
            )
        if self.verification_absolute_tolerance == 0.0:
            raise ValueError("verification_absolute_tolerance must be positive")


@dataclass(frozen=True, slots=True)
class SmoothFourStateConvergenceThresholds:
    """Declare finite built-in-float, unit-free momentum-refinement thresholds."""

    maximum_parent_diagnostic_change: float
    maximum_correlation_change: float
    maximum_threshold_change: float
    maximum_hopping_weight_change: float
    maximum_hopping_block_power_change: float
    maximum_angle_change: float
    maximum_band_defect: float
    maximum_reconstruction_defect: float
    maximum_parseval_defect: float

    def __post_init__(self) -> None:
        """Require strictly positive finite thresholds."""
        for name, value in (
            ("maximum_parent_diagnostic_change", self.maximum_parent_diagnostic_change),
            ("maximum_correlation_change", self.maximum_correlation_change),
            ("maximum_threshold_change", self.maximum_threshold_change),
            ("maximum_hopping_weight_change", self.maximum_hopping_weight_change),
            (
                "maximum_hopping_block_power_change",
                self.maximum_hopping_block_power_change,
            ),
            ("maximum_angle_change", self.maximum_angle_change),
            ("maximum_band_defect", self.maximum_band_defect),
            ("maximum_reconstruction_defect", self.maximum_reconstruction_defect),
            ("maximum_parseval_defect", self.maximum_parseval_defect),
        ):
            _finite_float(name, value)
            if value <= 0.0:
                raise ValueError(f"{name} must be positive")


@dataclass(frozen=True, slots=True)
class SmoothFourStateConvergenceDefinition:
    """Define a nested momentum study at one fixed amplitude inventory."""

    reciprocal_mesh_sizes: tuple[int, ...]
    amplitudes: tuple[float, ...]
    minimum_external_gap: float
    minimum_transport_singular_value: float
    frame_absolute_tolerance: float
    harmonic_absolute_degeneracy_tolerance: float
    harmonic_relative_degeneracy_tolerance: float
    verification_absolute_tolerance: float
    parent_hopping_scale: float
    thresholds: SmoothFourStateConvergenceThresholds
    required_stable_refinements: int

    def __post_init__(self) -> None:
        """Require nested doubling meshes and valid single-mesh controls."""
        if (
            type(self.reciprocal_mesh_sizes) is not tuple
            or len(self.reciprocal_mesh_sizes) < 2
        ):
            raise TypeError("reciprocal_mesh_sizes must contain at least two integers")
        if any(type(size) is not int for size in self.reciprocal_mesh_sizes):
            raise TypeError("reciprocal_mesh_sizes must contain built-in integers")
        if any(
            fine != 2 * coarse
            for coarse, fine in zip(
                self.reciprocal_mesh_sizes[:-1],
                self.reciprocal_mesh_sizes[1:],
                strict=True,
            )
        ):
            raise ValueError("reciprocal_mesh_sizes must be nested doubling meshes")
        self.mesh_definition(self.reciprocal_mesh_sizes[0])
        if type(self.thresholds) is not SmoothFourStateConvergenceThresholds:
            raise TypeError("thresholds must be SmoothFourStateConvergenceThresholds")
        if type(self.required_stable_refinements) is not int:
            raise TypeError("required_stable_refinements must be a built-in int")
        if not 1 <= self.required_stable_refinements < len(self.reciprocal_mesh_sizes):
            raise ValueError("required_stable_refinements exceeds available mesh pairs")

    def mesh_definition(self, reciprocal_mesh_size: int) -> SmoothFourStateDefinition:
        """Return one immutable mesh definition from shared study controls."""
        return SmoothFourStateDefinition(
            reciprocal_mesh_size=reciprocal_mesh_size,
            amplitudes=self.amplitudes,
            minimum_external_gap=self.minimum_external_gap,
            minimum_transport_singular_value=self.minimum_transport_singular_value,
            frame_absolute_tolerance=self.frame_absolute_tolerance,
            harmonic_absolute_degeneracy_tolerance=(
                self.harmonic_absolute_degeneracy_tolerance
            ),
            harmonic_relative_degeneracy_tolerance=(
                self.harmonic_relative_degeneracy_tolerance
            ),
            verification_absolute_tolerance=self.verification_absolute_tolerance,
            parent_hopping_scale=self.parent_hopping_scale,
        )


@dataclass(frozen=True, slots=True)
class SmoothFourStateAmplitudeThresholds:
    """Declare finite built-in-float midpoint-defect thresholds."""

    maximum_correlation_midpoint_defect: float
    maximum_operator_threshold_midpoint_defect: float
    maximum_joint_threshold_midpoint_defect: float
    maximum_hopping_weight_midpoint_defect: float
    maximum_hopping_block_power_midpoint_defect: float

    def __post_init__(self) -> None:
        """Require strictly positive finite thresholds."""
        for name, value in (
            (
                "maximum_correlation_midpoint_defect",
                self.maximum_correlation_midpoint_defect,
            ),
            (
                "maximum_operator_threshold_midpoint_defect",
                self.maximum_operator_threshold_midpoint_defect,
            ),
            (
                "maximum_joint_threshold_midpoint_defect",
                self.maximum_joint_threshold_midpoint_defect,
            ),
            (
                "maximum_hopping_weight_midpoint_defect",
                self.maximum_hopping_weight_midpoint_defect,
            ),
            (
                "maximum_hopping_block_power_midpoint_defect",
                self.maximum_hopping_block_power_midpoint_defect,
            ),
        ):
            _finite_float(name, value)
            if value <= 0.0:
                raise ValueError(f"{name} must be positive")


@dataclass(frozen=True, slots=True)
class SmoothFourStateAdaptiveAmplitudeDefinition:
    """Define capped deterministic midpoint refinement on one fixed momentum mesh.

    Integer caps are exact built-in integers and are never coerced or saturated.
    """

    initial_definition: SmoothFourStateDefinition
    thresholds: SmoothFourStateAmplitudeThresholds
    maximum_refinement_levels: int
    maximum_evaluated_amplitudes: int

    def __post_init__(self) -> None:
        """Require full-family endpoints and an explicit finite refinement cap."""
        if type(self.initial_definition) is not SmoothFourStateDefinition:
            raise TypeError("initial_definition must be SmoothFourStateDefinition")
        if self.initial_definition.amplitudes[-1] != math.pi / 4.0:
            raise ValueError("initial amplitudes must end at pi/4")
        if type(self.thresholds) is not SmoothFourStateAmplitudeThresholds:
            raise TypeError("thresholds must be SmoothFourStateAmplitudeThresholds")
        if type(self.maximum_refinement_levels) is not int:
            raise TypeError("maximum_refinement_levels must be a built-in int")
        if self.maximum_refinement_levels < 1:
            raise ValueError("maximum_refinement_levels must be positive")
        if type(self.maximum_evaluated_amplitudes) is not int:
            raise TypeError("maximum_evaluated_amplitudes must be a built-in int")
        first_inventory_size = 2 * len(self.initial_definition.amplitudes) - 1
        if self.maximum_evaluated_amplitudes < first_inventory_size:
            raise ValueError(
                "maximum_evaluated_amplitudes cannot hold the first midpoint inventory"
            )

    def evaluation_definition(
        self, amplitudes: tuple[float, ...]
    ) -> SmoothFourStateDefinition:
        """Return one direct-evaluation definition with unchanged controls."""
        initial = self.initial_definition
        return SmoothFourStateDefinition(
            reciprocal_mesh_size=initial.reciprocal_mesh_size,
            amplitudes=amplitudes,
            minimum_external_gap=initial.minimum_external_gap,
            minimum_transport_singular_value=initial.minimum_transport_singular_value,
            frame_absolute_tolerance=initial.frame_absolute_tolerance,
            harmonic_absolute_degeneracy_tolerance=(
                initial.harmonic_absolute_degeneracy_tolerance
            ),
            harmonic_relative_degeneracy_tolerance=(
                initial.harmonic_relative_degeneracy_tolerance
            ),
            verification_absolute_tolerance=initial.verification_absolute_tolerance,
            parent_hopping_scale=initial.parent_hopping_scale,
        )


@dataclass(frozen=True, slots=True)
class SmoothFourStateParentFamilyDefinition:
    """Define a bounded hopping-scale homotopy at fixed numerical controls."""

    template_definition: SmoothFourStateDefinition
    parent_hopping_scales: tuple[float, ...]

    def __post_init__(self) -> None:
        """Require a complete, ordered homotopy from the onsite to full parent."""
        if type(self.template_definition) is not SmoothFourStateDefinition:
            raise TypeError("template_definition must be SmoothFourStateDefinition")
        if self.template_definition.parent_hopping_scale != 1.0:
            raise ValueError("template_definition must describe the full parent")
        if type(self.parent_hopping_scales) is not tuple:
            raise TypeError("parent_hopping_scales must be a tuple")
        if len(self.parent_hopping_scales) < 2:
            raise ValueError("parent_hopping_scales must contain at least two values")
        for index, value in enumerate(self.parent_hopping_scales):
            _finite_float(f"parent_hopping_scales[{index}]", value)
            if not 0.0 <= value <= 1.0:
                raise ValueError("parent_hopping_scales must lie in [0, 1]")
        if self.parent_hopping_scales[0] != 0.0:
            raise ValueError("parent_hopping_scales must begin at zero")
        if self.parent_hopping_scales[-1] != 1.0:
            raise ValueError("parent_hopping_scales must end at one")
        if tuple(sorted(set(self.parent_hopping_scales))) != self.parent_hopping_scales:
            raise ValueError("parent_hopping_scales must be unique and increasing")

    def definition_at(self, parent_hopping_scale: float) -> SmoothFourStateDefinition:
        """Return one family member without changing any other control."""
        template = self.template_definition
        return SmoothFourStateDefinition(
            reciprocal_mesh_size=template.reciprocal_mesh_size,
            amplitudes=template.amplitudes,
            minimum_external_gap=template.minimum_external_gap,
            minimum_transport_singular_value=(
                template.minimum_transport_singular_value
            ),
            frame_absolute_tolerance=template.frame_absolute_tolerance,
            harmonic_absolute_degeneracy_tolerance=(
                template.harmonic_absolute_degeneracy_tolerance
            ),
            harmonic_relative_degeneracy_tolerance=(
                template.harmonic_relative_degeneracy_tolerance
            ),
            verification_absolute_tolerance=(template.verification_absolute_tolerance),
            parent_hopping_scale=parent_hopping_scale,
        )


__all__ = [
    "SMOOTH_FOUR_STATE_METHOD_ID",
    "SMOOTH_FOUR_STATE_PARENT_ID",
    "SmoothFourStateAdaptiveAmplitudeDefinition",
    "SmoothFourStateAmplitudeThresholds",
    "SmoothFourStateConvergenceDefinition",
    "SmoothFourStateConvergenceThresholds",
    "SmoothFourStateDefinition",
    "SmoothFourStateParentFamilyDefinition",
]
