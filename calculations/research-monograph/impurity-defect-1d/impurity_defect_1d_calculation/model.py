"""Defect-1D model ownership."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
import numpy.typing as npt

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type ComplexMatrix = npt.NDArray[np.complex128]
type ComplexVector = npt.NDArray[np.complex128]
type RealVector = npt.NDArray[np.float64]
type RealMatrixTuple = tuple[tuple[float, ...], ...]
type ComplexMatrixTuple = tuple[tuple[complex, ...], ...]
type ComparisonStatus = Literal["compatible", "stopped"]


@dataclass(frozen=True, slots=True)
class ParentSourceReference:
    """Identify the accepted periodic-parent records used by the exercise."""

    isolated_path: str
    isolated_sha256: str
    composite_path: str
    composite_sha256: str
    composite_group_id: str
    hopping_range: int

    def __post_init__(self) -> None:
        values = (
            self.isolated_path,
            self.isolated_sha256,
            self.composite_path,
            self.composite_sha256,
            self.composite_group_id,
        )
        if not all(values):
            raise ValueError("parent source identities must be nonempty")
        if self.hopping_range < 1:
            raise ValueError("parent hopping range must be positive")


@dataclass(frozen=True, slots=True)
class FoldingControl:
    """Represent the exact primitive-to-supercell folding cases."""

    supercell_size: int
    reduced_momentum_times_supercell: tuple[float, ...]

    def __post_init__(self) -> None:
        if self.supercell_size < 3:
            raise ValueError("folding supercell must contain at least three cells")
        if not self.reduced_momentum_times_supercell:
            raise ValueError("folding momenta must be nonempty")
        if any(
            not np.isfinite(value) or not -0.5 <= value < 0.5
            for value in self.reduced_momentum_times_supercell
        ):
            raise ValueError("folding momenta must lie in the reduced half-open zone")


@dataclass(frozen=True, slots=True)
class ExtractionControl:
    """Represent authored planted-defect blocks for exact recovery."""

    supercell_size: int
    reduced_momentum_times_supercell: float
    scalar_onsite_strength: float
    orbital_onsite: RealMatrixTuple
    nearest_neighbor: RealMatrixTuple
    range_two: RealMatrixTuple
    collinear_independent: RealMatrixTuple
    collinear_splitting: RealMatrixTuple
    spin_x: RealMatrixTuple
    spin_y: RealMatrixTuple
    spin_z: RealMatrixTuple

    def __post_init__(self) -> None:
        if self.supercell_size < 7:
            raise ValueError("extraction supercell must separate range-two defects")
        if not np.isfinite(self.reduced_momentum_times_supercell):
            raise ValueError("extraction momentum must be finite")
        if not -0.5 <= self.reduced_momentum_times_supercell < 0.5:
            raise ValueError("extraction momentum must lie in the reduced zone")
        if not np.isfinite(self.scalar_onsite_strength):
            raise ValueError("scalar onsite strength must be finite")
        matrices = (
            self.orbital_onsite,
            self.nearest_neighbor,
            self.range_two,
            self.collinear_independent,
            self.collinear_splitting,
            self.spin_x,
            self.spin_y,
            self.spin_z,
        )
        if any(
            len(matrix) != 2 or any(len(row) != 2 for row in matrix)
            for matrix in matrices
        ):
            raise ValueError("every authored orbital block must be two by two")


@dataclass(frozen=True, slots=True)
class AlignmentControl:
    """Represent the declared coordinate and energy-reference scrambling."""

    translation_cells: int
    orbital_permutation: tuple[int, int]
    orbital_rotation_angle: float
    orbital_phases: tuple[float, float]
    site_phase_step: float
    spin_axis: tuple[float, float, float]
    spin_rotation_angle: float
    energy_shift: float

    def __post_init__(self) -> None:
        values = np.asarray(
            (
                self.orbital_rotation_angle,
                *self.orbital_phases,
                self.site_phase_step,
                *self.spin_axis,
                self.spin_rotation_angle,
                self.energy_shift,
            ),
            dtype=np.float64,
        )
        if not np.all(np.isfinite(values)):
            raise ValueError("alignment values must be finite")
        if tuple(sorted(self.orbital_permutation)) != (0, 1):
            raise ValueError("orbital permutation must contain zero and one")
        if np.linalg.norm(np.asarray(self.spin_axis, dtype=np.float64)) == 0.0:
            raise ValueError("spin rotation axis must be nonzero")


@dataclass(frozen=True, slots=True)
class FiniteSizeControl:
    """Represent the periodic-image sequence for one localized defect."""

    supercell_sizes: tuple[int, ...]
    momentum_mesh_size: int
    gaussian_width: float
    gaussian_strength: float
    orbital_block: RealMatrixTuple
    core_radius: int

    def __post_init__(self) -> None:
        if tuple(sorted(set(self.supercell_sizes))) != self.supercell_sizes:
            raise ValueError("supercell sizes must be strictly increasing")
        if not self.supercell_sizes or self.supercell_sizes[0] <= 2 * self.core_radius:
            raise ValueError("every supercell must contain the declared core")
        if self.momentum_mesh_size < 3 or self.momentum_mesh_size % 2 == 0:
            raise ValueError("momentum mesh size must be odd and at least three")
        if (
            not np.isfinite(self.gaussian_width)
            or self.gaussian_width <= 0.0
            or not np.isfinite(self.gaussian_strength)
        ):
            raise ValueError("Gaussian controls must be finite with positive width")
        if len(self.orbital_block) != 2 or any(
            len(row) != 2 for row in self.orbital_block
        ):
            raise ValueError("finite-size orbital block must be two by two")
        if self.core_radius < 0:
            raise ValueError("core radius must be nonnegative")


@dataclass(frozen=True, slots=True)
class SmoothnessControl:
    """Represent the fixed-peak and fixed-integrated Gaussian scans."""

    supercell_size: int
    widths: tuple[float, ...]
    fixed_peak_strength: float
    fixed_integrated_strength: float

    def __post_init__(self) -> None:
        if self.supercell_size < 16 or self.supercell_size % 2 != 0:
            raise ValueError("smoothness supercell must be even and at least sixteen")
        if tuple(sorted(set(self.widths))) != self.widths or any(
            not np.isfinite(value) or value <= 0.0 for value in self.widths
        ):
            raise ValueError("smoothness widths must be positive and increasing")
        if not np.isfinite(self.fixed_peak_strength) or not np.isfinite(
            self.fixed_integrated_strength
        ):
            raise ValueError("smoothness strengths must be finite")


@dataclass(frozen=True, slots=True)
class MetricContrastControl:
    """Represent two controlled operator-versus-observable counterexamples."""

    profile_family: str
    width: float
    excited_residual_strength: float
    coupling_to_gap_ratio: float

    def __post_init__(self) -> None:
        if self.profile_family != "fixed-integrated":
            raise ValueError("metric contrast must use the fixed-integrated family")
        values = (
            self.width,
            self.excited_residual_strength,
            self.coupling_to_gap_ratio,
        )
        if any(not np.isfinite(value) or value <= 0.0 for value in values):
            raise ValueError("metric contrast controls must be positive and finite")


@dataclass(frozen=True, slots=True)
class DefectExerciseInput:
    """Represent the complete frozen synthetic exercise input."""

    experiment_id: str
    parent: ParentSourceReference
    folding: FoldingControl
    extraction: ExtractionControl
    alignment: AlignmentControl
    finite_size: FiniteSizeControl
    smoothness: SmoothnessControl
    metric_contrast: MetricContrastControl
    algebraic_tolerance: float
    bound_threshold_tolerance: float

    def __post_init__(self) -> None:
        if not self.experiment_id:
            raise ValueError("experiment_id must be nonempty")
        tolerances = (self.algebraic_tolerance, self.bound_threshold_tolerance)
        if any(not np.isfinite(value) or value <= 0.0 for value in tolerances):
            raise ValueError("tolerances must be positive and finite")


@dataclass(frozen=True, slots=True)
class SupercellBasis:
    """Identify comparison-critical metadata for one supercell representation."""

    state_space_id: str
    cell_count: int
    orbital_count: int
    spin_count: int
    reduced_momentum: float
    site_ordering: str
    orbital_ordering: str
    spin_ordering: str
    coordinate_frame: str
    energy_unit: str
    energy_reference: str
    geometry_id: str
    subspace_id: str

    def __post_init__(self) -> None:
        text = (
            self.state_space_id,
            self.site_ordering,
            self.orbital_ordering,
            self.spin_ordering,
            self.coordinate_frame,
            self.energy_unit,
            self.energy_reference,
            self.geometry_id,
            self.subspace_id,
        )
        if not all(text):
            raise ValueError("basis metadata must be nonempty")
        if self.cell_count < 1 or self.orbital_count < 1 or self.spin_count < 1:
            raise ValueError("basis dimensions must be positive")
        if not np.isfinite(self.reduced_momentum):
            raise ValueError("reduced momentum must be finite")

    @property
    def dimension(self) -> int:
        """Return the matrix dimension implied by the represented factors."""
        return self.cell_count * self.orbital_count * self.spin_count


@dataclass(frozen=True, slots=True)
class RepresentedOperator:
    """Store one operationally immutable represented finite operator."""

    identifier: str
    basis: SupercellBasis
    matrix: ComplexMatrix

    def __post_init__(self) -> None:
        if not self.identifier:
            raise ValueError("operator identifier must be nonempty")
        value = np.asarray(self.matrix, dtype=np.complex128)
        if value.shape != (self.basis.dimension, self.basis.dimension):
            raise ValueError("operator matrix shape must agree with basis metadata")
        if not np.all(np.isfinite(value)):
            raise ValueError("operator matrix must be finite")
        immutable = np.frombuffer(
            value.tobytes(order="C"), dtype=np.complex128
        ).reshape(value.shape)
        object.__setattr__(self, "matrix", immutable)


@dataclass(frozen=True, slots=True)
class CompatibilityResult:
    """Record direct comparison compatibility or structured stop codes."""

    status: ComparisonStatus
    issue_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        if (self.status == "compatible") == bool(self.issue_codes):
            raise ValueError("compatibility status must agree with issue codes")
        if self.issue_codes != tuple(sorted(set(self.issue_codes))):
            raise ValueError("compatibility issues must be sorted and unique")


@dataclass(frozen=True, slots=True)
class ParentData:
    """Retain accepted scalar and two-orbital hopping records in immutable form."""

    period: float
    scalar_hoppings: tuple[tuple[int, complex], ...]
    composite_hoppings: tuple[tuple[int, ComplexMatrixTuple], ...]
    source_identities: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        if not np.isfinite(self.period) or self.period <= 0.0:
            raise ValueError("period must be positive and finite")
        scalar_representatives = tuple(value[0] for value in self.scalar_hoppings)
        composite_representatives = tuple(value[0] for value in self.composite_hoppings)
        if scalar_representatives != tuple(sorted(set(scalar_representatives))):
            raise ValueError("scalar hopping representatives must be sorted and unique")
        if composite_representatives != tuple(sorted(set(composite_representatives))):
            raise ValueError("composite representatives must be sorted and unique")
        if not self.source_identities:
            raise ValueError("source identities must be retained")
