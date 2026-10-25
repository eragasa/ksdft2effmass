"""Immutable results for the smooth non-flat four-state realization."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from projectkoios.optimization.selection.harmonic import PeriodicHarmonicMaximum

from ._validation import _finite_float
from .nonflat_definition import (
    SmoothFourStateAdaptiveAmplitudeDefinition,
    SmoothFourStateConvergenceDefinition,
    SmoothFourStateDefinition,
    SmoothFourStateParentFamilyDefinition,
)


@dataclass(frozen=True, slots=True)
class SmoothFourStateHoppingBlockResult:
    """Retain reference and comparison power at one finite-mesh displacement."""

    displacement: int
    reference_normalized_squared_frobenius_norm: float
    comparison_normalized_squared_frobenius_norm: float

    def __post_init__(self) -> None:
        """Validate one finite nonnegative range-resolved result."""
        if type(self.displacement) is not int:
            raise TypeError("displacement must be a built-in int")
        for name, value in (
            (
                "reference_normalized_squared_frobenius_norm",
                self.reference_normalized_squared_frobenius_norm,
            ),
            (
                "comparison_normalized_squared_frobenius_norm",
                self.comparison_normalized_squared_frobenius_norm,
            ),
        ):
            _finite_float(name, value)
            if value < 0.0:
                raise ValueError(f"{name} must be nonnegative")


@dataclass(frozen=True, slots=True)
class SmoothFourStatePointResult:
    """Retain non-flat band, restricted-alignment, and hopping channels."""

    amplitude: float
    maximum_band_defect: float
    splitting_scale: float
    harmonic_maximum: PeriodicHarmonicMaximum
    discrete_maximum_correlation: float
    minimum_operator_threshold: float
    exact_spectrum_joint_operator_threshold: float
    minimum_loss_reconstruction_defect: float
    reference_nonzero_hopping_weight: float
    comparison_nonzero_hopping_weight: float
    reference_parseval_defect: float
    comparison_parseval_defect: float
    hopping_blocks: tuple[SmoothFourStateHoppingBlockResult, ...]

    def __post_init__(self) -> None:
        """Validate scalar channels and complete ordered block inventory."""
        for name, value in (
            ("amplitude", self.amplitude),
            ("maximum_band_defect", self.maximum_band_defect),
            ("splitting_scale", self.splitting_scale),
            ("minimum_operator_threshold", self.minimum_operator_threshold),
            (
                "exact_spectrum_joint_operator_threshold",
                self.exact_spectrum_joint_operator_threshold,
            ),
            (
                "minimum_loss_reconstruction_defect",
                self.minimum_loss_reconstruction_defect,
            ),
            (
                "reference_nonzero_hopping_weight",
                self.reference_nonzero_hopping_weight,
            ),
            (
                "comparison_nonzero_hopping_weight",
                self.comparison_nonzero_hopping_weight,
            ),
            ("reference_parseval_defect", self.reference_parseval_defect),
            ("comparison_parseval_defect", self.comparison_parseval_defect),
        ):
            _finite_float(name, value)
            if value < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        _finite_float("discrete_maximum_correlation", self.discrete_maximum_correlation)
        if self.splitting_scale == 0.0:
            raise ValueError("splitting_scale must be positive")
        if not -1.0 <= self.discrete_maximum_correlation <= 1.0:
            raise ValueError("discrete_maximum_correlation must lie in [-1, 1]")
        if type(self.harmonic_maximum) is not PeriodicHarmonicMaximum:
            raise TypeError("harmonic_maximum must be PeriodicHarmonicMaximum")
        if type(self.hopping_blocks) is not tuple or not self.hopping_blocks:
            raise TypeError("hopping_blocks must be a nonempty tuple")
        if any(
            type(item) is not SmoothFourStateHoppingBlockResult
            for item in self.hopping_blocks
        ):
            raise TypeError("hopping_blocks must contain typed block results")
        displacements = tuple(item.displacement for item in self.hopping_blocks)
        if tuple(sorted(set(displacements))) != displacements:
            raise ValueError(
                "hopping block displacements must be unique and increasing"
            )
        if 0 not in displacements:
            raise ValueError("hopping_blocks must contain the onsite block")


@dataclass(frozen=True, slots=True)
class SmoothFourStateResult:
    """Retain one complete non-flat calculation on one reciprocal mesh."""

    definition: SmoothFourStateDefinition
    minimum_external_gap: float
    minimum_transport_singular_value: float
    maximum_frame_orthonormality_defect: float
    periodic_closure_defect: float
    maximum_reference_hermiticity_defect: float
    points: tuple[SmoothFourStatePointResult, ...]

    def __post_init__(self) -> None:
        """Validate parent diagnostics and amplitude correlation."""
        if type(self.definition) is not SmoothFourStateDefinition:
            raise TypeError("definition must be SmoothFourStateDefinition")
        for name, value in (
            ("minimum_external_gap", self.minimum_external_gap),
            (
                "minimum_transport_singular_value",
                self.minimum_transport_singular_value,
            ),
            (
                "maximum_frame_orthonormality_defect",
                self.maximum_frame_orthonormality_defect,
            ),
            ("periodic_closure_defect", self.periodic_closure_defect),
            (
                "maximum_reference_hermiticity_defect",
                self.maximum_reference_hermiticity_defect,
            ),
        ):
            _finite_float(name, value)
            if value < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        if self.minimum_external_gap < self.definition.minimum_external_gap:
            raise ValueError("minimum_external_gap fails its declared lower bound")
        if (
            self.minimum_transport_singular_value
            <= self.definition.minimum_transport_singular_value
        ):
            raise ValueError(
                "minimum_transport_singular_value fails its declared lower bound"
            )
        if type(self.points) is not tuple or any(
            type(point) is not SmoothFourStatePointResult for point in self.points
        ):
            raise TypeError("points must be a typed tuple")
        if (
            tuple(point.amplitude for point in self.points)
            != self.definition.amplitudes
        ):
            raise ValueError("points must match the declared amplitudes")


@dataclass(frozen=True, slots=True)
class SmoothFourStateParentFamilyResult:
    """Retain every member of the bounded parent-hopping homotopy."""

    definition: SmoothFourStateParentFamilyDefinition
    members: tuple[SmoothFourStateResult, ...]

    def __post_init__(self) -> None:
        """Correlate family members with their declared hopping scales."""
        if type(self.definition) is not SmoothFourStateParentFamilyDefinition:
            raise TypeError("definition must be SmoothFourStateParentFamilyDefinition")
        if type(self.members) is not tuple or any(
            type(item) is not SmoothFourStateResult for item in self.members
        ):
            raise TypeError("members must be a typed tuple")
        expected_definitions = tuple(
            self.definition.definition_at(scale)
            for scale in self.definition.parent_hopping_scales
        )
        if tuple(item.definition for item in self.members) != expected_definitions:
            raise ValueError("members must match every declared family control")


class SmoothFourStateConvergenceDisposition(StrEnum):
    """Classify only demonstrated momentum stability."""

    CONVERGED = "converged"
    UNRESOLVED = "unresolved"


@dataclass(frozen=True, slots=True)
class SmoothFourStateRefinementResult:
    """Retain maximum changes across one momentum-mesh refinement."""

    coarse_mesh_size: int
    fine_mesh_size: int
    maximum_parent_diagnostic_change: float
    maximum_shared_parent_eigenvalue_defect: float
    maximum_shared_projector_defect: float
    maximum_correlation_change: float
    maximum_threshold_change: float
    maximum_hopping_weight_change: float
    maximum_hopping_block_power_change: float
    maximum_angle_change: float
    maximizing_angle_dispositions_stable: bool
    maximum_band_defect: float
    maximum_reconstruction_defect: float
    maximum_parseval_defect: float
    within_tolerances: bool

    def __post_init__(self) -> None:
        """Validate nested identities and nonnegative refinement metrics."""
        if (
            type(self.coarse_mesh_size) is not int
            or type(self.fine_mesh_size) is not int
        ):
            raise TypeError("mesh sizes must be built-in integers")
        if self.fine_mesh_size != 2 * self.coarse_mesh_size:
            raise ValueError("mesh sizes must form one doubling pair")
        for name, value in (
            ("maximum_parent_diagnostic_change", self.maximum_parent_diagnostic_change),
            (
                "maximum_shared_parent_eigenvalue_defect",
                self.maximum_shared_parent_eigenvalue_defect,
            ),
            ("maximum_shared_projector_defect", self.maximum_shared_projector_defect),
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
            if value < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        if type(self.maximizing_angle_dispositions_stable) is not bool:
            raise TypeError(
                "maximizing_angle_dispositions_stable must be a built-in bool"
            )
        if type(self.within_tolerances) is not bool:
            raise TypeError("within_tolerances must be a built-in bool")


@dataclass(frozen=True, slots=True)
class SmoothFourStateAmplitudeRefinementResult:
    """Retain direct midpoint defects for one adaptive refinement level."""

    level_index: int
    interpolation_nodes: tuple[float, ...]
    evaluated_amplitudes: tuple[float, ...]
    maximum_correlation_midpoint_defect: float
    maximum_operator_threshold_midpoint_defect: float
    maximum_joint_threshold_midpoint_defect: float
    maximum_hopping_weight_midpoint_defect: float
    maximum_hopping_block_power_midpoint_defect: float
    failing_interval_count: int
    within_tolerances: bool

    def __post_init__(self) -> None:
        """Validate the deterministic midpoint inventory and nonnegative defects."""
        if type(self.level_index) is not int or self.level_index < 0:
            raise ValueError("level_index must be a nonnegative built-in int")
        for name, values in (
            ("interpolation_nodes", self.interpolation_nodes),
            ("evaluated_amplitudes", self.evaluated_amplitudes),
        ):
            if type(values) is not tuple or len(values) < 2:
                raise TypeError(f"{name} must contain at least two amplitudes")
            if tuple(sorted(set(values))) != values:
                raise ValueError(f"{name} must be unique and increasing")
            for index, value in enumerate(values):
                _finite_float(f"{name}[{index}]", value)
        expected = tuple(
            sorted(
                set(self.interpolation_nodes)
                | {
                    0.5 * (left + right)
                    for left, right in zip(
                        self.interpolation_nodes[:-1],
                        self.interpolation_nodes[1:],
                        strict=True,
                    )
                }
            )
        )
        if self.evaluated_amplitudes != expected:
            raise ValueError(
                "evaluated_amplitudes must contain every interval midpoint"
            )
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
            if value < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        if type(self.failing_interval_count) is not int:
            raise TypeError("failing_interval_count must be a built-in int")
        if not 0 <= self.failing_interval_count < len(self.interpolation_nodes):
            raise ValueError("failing_interval_count exceeds the interval count")
        if type(self.within_tolerances) is not bool:
            raise TypeError("within_tolerances must be a built-in bool")
        if self.within_tolerances is not (self.failing_interval_count == 0):
            raise ValueError("within_tolerances must match failing_interval_count")


@dataclass(frozen=True, slots=True)
class SmoothFourStateAmplitudeValidationResult:
    """Retain disjoint quarter-point validation for one frozen node inventory."""

    level_index: int
    interpolation_nodes: tuple[float, ...]
    evaluated_amplitudes: tuple[float, ...]
    maximum_correlation_defect: float
    maximum_operator_threshold_defect: float
    maximum_joint_threshold_defect: float
    maximum_hopping_weight_defect: float
    maximum_hopping_block_power_defect: float
    failing_point_count: int
    within_tolerances: bool

    def __post_init__(self) -> None:
        """Validate disjoint identities and nonnegative direct-evaluation defects."""
        if type(self.level_index) is not int or self.level_index < 0:
            raise ValueError("level_index must be a nonnegative built-in int")
        if (
            type(self.interpolation_nodes) is not tuple
            or len(self.interpolation_nodes) < 2
        ):
            raise TypeError("interpolation_nodes must contain at least two amplitudes")
        if tuple(sorted(set(self.interpolation_nodes))) != self.interpolation_nodes:
            raise ValueError("interpolation_nodes must be unique and increasing")
        if type(self.evaluated_amplitudes) is not tuple:
            raise TypeError("evaluated_amplitudes must be a tuple")
        if tuple(sorted(set(self.evaluated_amplitudes))) != self.evaluated_amplitudes:
            raise ValueError("evaluated_amplitudes must be unique and increasing")
        if set(self.evaluated_amplitudes) & set(self.interpolation_nodes):
            raise ValueError(
                "validation amplitudes must be disjoint from interpolation nodes"
            )
        expected_amplitudes = tuple(
            sample
            for left, right in zip(
                self.interpolation_nodes[:-1],
                self.interpolation_nodes[1:],
                strict=True,
            )
            for sample in (
                left + 0.25 * (right - left),
                left + 0.75 * (right - left),
            )
        )
        expected_count = len(expected_amplitudes)
        if self.evaluated_amplitudes != expected_amplitudes:
            raise ValueError("validation must contain two quarter points per interval")
        for index, value in enumerate(self.evaluated_amplitudes):
            _finite_float(f"evaluated_amplitudes[{index}]", value)
        for name, value in (
            ("maximum_correlation_defect", self.maximum_correlation_defect),
            (
                "maximum_operator_threshold_defect",
                self.maximum_operator_threshold_defect,
            ),
            ("maximum_joint_threshold_defect", self.maximum_joint_threshold_defect),
            ("maximum_hopping_weight_defect", self.maximum_hopping_weight_defect),
            (
                "maximum_hopping_block_power_defect",
                self.maximum_hopping_block_power_defect,
            ),
        ):
            _finite_float(name, value)
            if value < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        if type(self.failing_point_count) is not int:
            raise TypeError("failing_point_count must be a built-in int")
        if not 0 <= self.failing_point_count <= expected_count:
            raise ValueError("failing_point_count exceeds the validation inventory")
        if type(self.within_tolerances) is not bool:
            raise TypeError("within_tolerances must be a built-in bool")
        if self.within_tolerances is not (self.failing_point_count == 0):
            raise ValueError("within_tolerances must match failing_point_count")


@dataclass(frozen=True, slots=True)
class SmoothFourStateConvergenceResult:
    """Retain every non-flat momentum mesh and conservative disposition."""

    definition: SmoothFourStateConvergenceDefinition
    mesh_results: tuple[SmoothFourStateResult, ...]
    refinements: tuple[SmoothFourStateRefinementResult, ...]
    disposition: SmoothFourStateConvergenceDisposition

    def __post_init__(self) -> None:
        """Correlate mesh identities and derive the disposition."""
        if type(self.definition) is not SmoothFourStateConvergenceDefinition:
            raise TypeError("definition must be SmoothFourStateConvergenceDefinition")
        if type(self.mesh_results) is not tuple or any(
            type(item) is not SmoothFourStateResult for item in self.mesh_results
        ):
            raise TypeError("mesh_results must be a typed tuple")
        expected_mesh_definitions = tuple(
            self.definition.mesh_definition(size)
            for size in self.definition.reciprocal_mesh_sizes
        )
        if (
            tuple(item.definition for item in self.mesh_results)
            != expected_mesh_definitions
        ):
            raise ValueError("mesh_results must match every declared mesh control")
        expected_pairs = tuple(
            zip(
                self.definition.reciprocal_mesh_sizes[:-1],
                self.definition.reciprocal_mesh_sizes[1:],
                strict=True,
            )
        )
        actual_pairs = tuple(
            (item.coarse_mesh_size, item.fine_mesh_size) for item in self.refinements
        )
        if actual_pairs != expected_pairs:
            raise ValueError("refinements must match adjacent declared meshes")
        if type(self.disposition) is not SmoothFourStateConvergenceDisposition:
            raise TypeError("disposition must be SmoothFourStateConvergenceDisposition")
        required = self.definition.required_stable_refinements
        expected = (
            SmoothFourStateConvergenceDisposition.CONVERGED
            if all(item.within_tolerances for item in self.refinements[-required:])
            else SmoothFourStateConvergenceDisposition.UNRESOLVED
        )
        if self.disposition is not expected:
            raise ValueError("disposition must match required final refinements")


@dataclass(frozen=True, slots=True)
class SmoothFourStateAdaptiveAmplitudeResult:
    """Retain bounded adaptive amplitude refinement and its final direct samples."""

    definition: SmoothFourStateAdaptiveAmplitudeDefinition
    levels: tuple[SmoothFourStateAmplitudeRefinementResult, ...]
    validations: tuple[SmoothFourStateAmplitudeValidationResult, ...]
    all_evaluated_amplitudes: tuple[float, ...]
    final_evaluation: SmoothFourStateResult
    disposition: SmoothFourStateConvergenceDisposition

    def __post_init__(self) -> None:
        """Correlate all levels, final samples, and conservative disposition."""
        if type(self.definition) is not SmoothFourStateAdaptiveAmplitudeDefinition:
            raise TypeError(
                "definition must be SmoothFourStateAdaptiveAmplitudeDefinition"
            )
        if (
            type(self.levels) is not tuple
            or not self.levels
            or any(
                type(item) is not SmoothFourStateAmplitudeRefinementResult
                for item in self.levels
            )
        ):
            raise TypeError("levels must be a nonempty typed tuple")
        if len(self.levels) > self.definition.maximum_refinement_levels:
            raise ValueError("levels exceed maximum_refinement_levels")
        if tuple(item.level_index for item in self.levels) != tuple(
            range(len(self.levels))
        ):
            raise ValueError("levels must have contiguous zero-based identities")
        thresholds = self.definition.thresholds
        margin = self.definition.initial_definition.verification_absolute_tolerance
        for item in self.levels:
            expected_within = all(
                defect + margin <= threshold
                for defect, threshold in zip(
                    (
                        item.maximum_correlation_midpoint_defect,
                        item.maximum_operator_threshold_midpoint_defect,
                        item.maximum_joint_threshold_midpoint_defect,
                        item.maximum_hopping_weight_midpoint_defect,
                        item.maximum_hopping_block_power_midpoint_defect,
                    ),
                    (
                        thresholds.maximum_correlation_midpoint_defect,
                        thresholds.maximum_operator_threshold_midpoint_defect,
                        thresholds.maximum_joint_threshold_midpoint_defect,
                        thresholds.maximum_hopping_weight_midpoint_defect,
                        thresholds.maximum_hopping_block_power_midpoint_defect,
                    ),
                    strict=True,
                )
            )
            if item.within_tolerances is not expected_within:
                raise ValueError("amplitude level violates conservative thresholds")
        for previous, current in zip(self.levels[:-1], self.levels[1:], strict=True):
            if not set(previous.interpolation_nodes).issubset(
                current.interpolation_nodes
            ):
                raise ValueError("interpolation nodes must be nested")
        if type(self.validations) is not tuple or any(
            type(item) is not SmoothFourStateAmplitudeValidationResult
            for item in self.validations
        ):
            raise TypeError("validations must be a typed tuple")
        if any(item.level_index >= len(self.levels) for item in self.validations):
            raise ValueError("validation level identity is out of range")
        if tuple(item.level_index for item in self.validations) != tuple(
            sorted({item.level_index for item in self.validations})
        ):
            raise ValueError("validations must have unique increasing level identities")
        for validation in self.validations:
            if (
                validation.interpolation_nodes
                != self.levels[validation.level_index].interpolation_nodes
            ):
                raise ValueError("validation nodes must match their refinement level")
            expected_within = all(
                defect + margin <= threshold
                for defect, threshold in zip(
                    (
                        validation.maximum_correlation_defect,
                        validation.maximum_operator_threshold_defect,
                        validation.maximum_joint_threshold_defect,
                        validation.maximum_hopping_weight_defect,
                        validation.maximum_hopping_block_power_defect,
                    ),
                    (
                        thresholds.maximum_correlation_midpoint_defect,
                        thresholds.maximum_operator_threshold_midpoint_defect,
                        thresholds.maximum_joint_threshold_midpoint_defect,
                        thresholds.maximum_hopping_weight_midpoint_defect,
                        thresholds.maximum_hopping_block_power_midpoint_defect,
                    ),
                    strict=True,
                )
            )
            if validation.within_tolerances is not expected_within:
                raise ValueError("validation violates conservative thresholds")
        if (
            type(self.all_evaluated_amplitudes) is not tuple
            or not self.all_evaluated_amplitudes
        ):
            raise TypeError("all_evaluated_amplitudes must be a nonempty tuple")
        if (
            tuple(sorted(set(self.all_evaluated_amplitudes)))
            != self.all_evaluated_amplitudes
        ):
            raise ValueError("all_evaluated_amplitudes must be unique and increasing")
        if (
            len(self.all_evaluated_amplitudes)
            > self.definition.maximum_evaluated_amplitudes
        ):
            raise ValueError("all_evaluated_amplitudes exceeds the declared cap")
        required_amplitudes = {
            amplitude
            for level in self.levels
            for amplitude in level.evaluated_amplitudes
        } | {
            amplitude
            for validation in self.validations
            for amplitude in validation.evaluated_amplitudes
        }
        if not required_amplitudes.issubset(self.all_evaluated_amplitudes):
            raise ValueError("all_evaluated_amplitudes omits a direct sample")
        if type(self.final_evaluation) is not SmoothFourStateResult:
            raise TypeError("final_evaluation must be SmoothFourStateResult")
        final_inventory = self.levels[-1].evaluated_amplitudes
        if (
            self.validations
            and self.validations[-1].level_index == len(self.levels) - 1
        ):
            final_inventory = tuple(
                sorted(
                    set(self.validations[-1].interpolation_nodes)
                    | set(self.validations[-1].evaluated_amplitudes)
                )
            )
        if self.final_evaluation.definition.amplitudes != final_inventory:
            raise ValueError("final_evaluation must match the last direct inventory")
        if type(self.disposition) is not SmoothFourStateConvergenceDisposition:
            raise TypeError("disposition must be SmoothFourStateConvergenceDisposition")
        final_validation_passes = bool(
            self.validations
            and self.validations[-1].level_index == len(self.levels) - 1
            and self.validations[-1].within_tolerances
        )
        expected = (
            SmoothFourStateConvergenceDisposition.CONVERGED
            if self.levels[-1].within_tolerances and final_validation_passes
            else SmoothFourStateConvergenceDisposition.UNRESOLVED
        )
        if self.disposition is not expected:
            raise ValueError("disposition must match the final amplitude level")


__all__ = [
    "SmoothFourStateAdaptiveAmplitudeResult",
    "SmoothFourStateAmplitudeRefinementResult",
    "SmoothFourStateAmplitudeValidationResult",
    "SmoothFourStateConvergenceDisposition",
    "SmoothFourStateConvergenceResult",
    "SmoothFourStateHoppingBlockResult",
    "SmoothFourStateParentFamilyResult",
    "SmoothFourStatePointResult",
    "SmoothFourStateRefinementResult",
    "SmoothFourStateResult",
]
