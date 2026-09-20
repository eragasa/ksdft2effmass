"""Finite Born--von Karman localization diagnostics for isolated 1D bands."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

import numpy as np

from ksdft2effmass.operators import (
    MODEL_SYSTEM_UNIT_CONVERTER,
    PhysicalUnit,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.solid_state import PlaneWaveBasis1D, ReciprocalBandFramePath1D


@dataclass(frozen=True, slots=True, eq=False)
class BornVonKarmanLocalizationResult1D:
    """Retain one sampled isolated-band localization diagnostic.

    Center and spread use the declared centered Born--von Karman coordinate branch.
    They are finite-supercell diagnostics, not branch-independent modern-polarization
    observables.
    """

    source: ReciprocalBandFramePath1D
    basis: PlaneWaveBasis1D
    period: ScalarQuantity
    samples_per_cell: int
    coordinates: VectorQuantity
    normalized_density: VectorQuantity
    quadrature_norm: float
    center: ScalarQuantity
    spread: ScalarQuantity
    normalization_absolute_tolerance: float

    def __post_init__(self) -> None:
        """Validate dimensions, units, normalization, and scalar correlations."""
        if type(self.source) is not ReciprocalBandFramePath1D:
            raise TypeError("source must be ReciprocalBandFramePath1D")
        if type(self.basis) is not PlaneWaveBasis1D:
            raise TypeError("basis must be PlaneWaveBasis1D")
        if type(self.period) is not ScalarQuantity:
            raise TypeError("period must be ScalarQuantity")
        if self.period.magnitude <= 0.0:
            raise ValueError("period must be positive")
        if type(self.samples_per_cell) is not int:
            raise TypeError("samples_per_cell must be a built-in int")
        if self.samples_per_cell < 2:
            raise ValueError("samples_per_cell must be at least two")
        if type(self.coordinates) is not VectorQuantity:
            raise TypeError("coordinates must be VectorQuantity")
        if self.coordinates.unit != self.period.unit:
            raise ValueError("coordinates must use the period unit")
        expected_count = self.source.mesh.point_count * self.samples_per_cell
        if self.coordinates.magnitude.shape != (expected_count,):
            raise ValueError("coordinate count must match cells times samples per cell")
        if type(self.normalized_density) is not VectorQuantity:
            raise TypeError("normalized_density must be VectorQuantity")
        if self.normalized_density.magnitude.shape != (expected_count,):
            raise ValueError("density count must equal coordinate count")
        if np.any(self.normalized_density.magnitude < 0.0):
            raise ValueError("normalized_density must be nonnegative")
        expected_density_unit = (
            Unitless()
            if isinstance(self.period.unit, Unitless)
            else PhysicalUnit(f"1 / ({self.period.unit.expression})")
        )
        if self.normalized_density.unit != expected_density_unit:
            raise ValueError("normalized_density must use the inverse-period unit")
        if type(self.quadrature_norm) is not float:
            raise TypeError("quadrature_norm must be a built-in float")
        if not np.isfinite(self.quadrature_norm) or self.quadrature_norm <= 0.0:
            raise ValueError("quadrature_norm must be finite and positive")
        if type(self.center) is not ScalarQuantity:
            raise TypeError("center must be ScalarQuantity")
        if self.center.unit != self.period.unit:
            raise ValueError("center must use the period unit")
        if type(self.spread) is not ScalarQuantity:
            raise TypeError("spread must be ScalarQuantity")
        expected_spread_unit = (
            Unitless()
            if isinstance(self.period.unit, Unitless)
            else PhysicalUnit(f"({self.period.unit.expression}) ** 2")
        )
        if self.spread.unit != expected_spread_unit:
            raise ValueError("spread must use the squared-period unit")
        if self.spread.magnitude < 0.0:
            raise ValueError("spread must be nonnegative")
        if type(self.normalization_absolute_tolerance) is not float:
            raise TypeError(
                "normalization_absolute_tolerance must be a built-in float"
            )
        if (
            not np.isfinite(self.normalization_absolute_tolerance)
            or self.normalization_absolute_tolerance < 0.0
        ):
            raise ValueError(
                "normalization_absolute_tolerance must be finite and nonnegative"
            )
        spacing = self.period.magnitude / float(self.samples_per_cell)
        normalized_integral = float(
            spacing * np.sum(self.normalized_density.magnitude)
        )
        if abs(normalized_integral - 1.0) > self.normalization_absolute_tolerance:
            raise ValueError("normalized_density does not pass normalization tolerance")
        measured_center = float(
            spacing
            * np.sum(self.coordinates.magnitude * self.normalized_density.magnitude)
        )
        if measured_center != self.center.magnitude:
            raise ValueError("center must match the represented density")
        measured_spread = float(
            spacing
            * np.sum(
                np.square(self.coordinates.magnitude - self.center.magnitude)
                * self.normalized_density.magnitude
            )
        )
        if measured_spread != self.spread.magnitude:
            raise ValueError("spread must match the represented density")

    @property
    def center_over_period(self) -> float:
        """Return the branch-dependent center in lattice-period units."""
        return self.center.magnitude / self.period.magnitude

    @property
    def spread_over_period_squared(self) -> float:
        """Return the spread in squared lattice-period units."""
        return self.spread.magnitude / (self.period.magnitude**2)

    @property
    def density_content_sha256(self) -> str:
        """Authenticate little-endian binary64 density values in sample order."""
        canonical = np.asarray(
            self.normalized_density.magnitude, dtype="<f8", order="C"
        )
        return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()


class BornVonKarmanLocalizationAnalyzer1D:
    """Evaluate an isolated-band inverse Bloch transform on a finite supercell."""

    __slots__ = ()

    def execute(
        self,
        source: ReciprocalBandFramePath1D,
        basis: PlaneWaveBasis1D,
        period: ScalarQuantity,
        samples_per_cell: int,
        duality_absolute_tolerance: float,
        normalization_absolute_tolerance: float,
    ) -> BornVonKarmanLocalizationResult1D:
        """Sample, normalize, and summarize the centered finite-supercell density."""
        if type(source) is not ReciprocalBandFramePath1D:
            raise TypeError("source must be ReciprocalBandFramePath1D")
        if source.rank != 1:
            raise ValueError("Born-von Karman localization requires an isolated band")
        if type(basis) is not PlaneWaveBasis1D:
            raise TypeError("basis must be PlaneWaveBasis1D")
        if source.ambient_dimension != basis.dimension:
            raise ValueError("frame ambient dimension must match plane-wave basis")
        if type(period) is not ScalarQuantity:
            raise TypeError("period must be ScalarQuantity")
        if period.magnitude <= 0.0:
            raise ValueError("period must be positive")
        if type(samples_per_cell) is not int:
            raise TypeError("samples_per_cell must be a built-in int")
        if samples_per_cell < 2:
            raise ValueError("samples_per_cell must be at least two")
        for name, tolerance in (
            ("duality_absolute_tolerance", duality_absolute_tolerance),
            (
                "normalization_absolute_tolerance",
                normalization_absolute_tolerance,
            ),
        ):
            if type(tolerance) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(tolerance) or tolerance < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        if isinstance(period.unit, Unitless):
            if not isinstance(basis.reciprocal_vector.unit, Unitless):
                raise ValueError("unitless period requires unitless reciprocal vector")
            reciprocal_magnitude = basis.reciprocal_vector.magnitude
        else:
            if isinstance(basis.reciprocal_vector.unit, Unitless):
                raise ValueError("physical period requires physical reciprocal vector")
            inverse_period_unit = PhysicalUnit(f"1 / ({period.unit.expression})")
            reciprocal_magnitude = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
                basis.reciprocal_vector, inverse_period_unit
            ).magnitude
        if not np.isclose(
            reciprocal_magnitude * period.magnitude,
            2.0 * np.pi,
            rtol=0.0,
            atol=duality_absolute_tolerance,
        ):
            raise ValueError("period and plane-wave reciprocal vector are incompatible")
        mesh_period = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            source.mesh.reciprocal_period, basis.reciprocal_vector.unit
        )
        if not np.isclose(
            mesh_period.magnitude,
            basis.reciprocal_vector.magnitude,
            rtol=0.0,
            atol=duality_absolute_tolerance,
        ):
            raise ValueError("frame mesh and plane-wave reciprocal periods disagree")
        cell_count = source.mesh.point_count
        point_count = cell_count * samples_per_cell
        coordinates_magnitude = np.linspace(
            -0.5 * float(cell_count) * period.magnitude,
            0.5 * float(cell_count) * period.magnitude,
            point_count,
            endpoint=False,
            dtype=np.float64,
        )
        cell_coordinates = np.mod(coordinates_magnitude, period.magnitude)
        reciprocal_indices = np.asarray(basis.reciprocal_indices, dtype=np.float64)
        cell_basis = np.exp(
            1j
            * np.outer(
                cell_coordinates,
                reciprocal_indices * reciprocal_magnitude,
            )
        ) / np.sqrt(period.magnitude)
        coefficients = np.column_stack(
            tuple(frame.magnitude[:, 0] for frame in source.frames)
        )
        periodic_parts = cell_basis @ coefficients
        momenta = MODEL_SYSTEM_UNIT_CONVERTER.convert_vector(
            source.mesh.coordinates, basis.reciprocal_vector.unit
        ).magnitude
        bloch_states = periodic_parts * np.exp(
            1j * np.outer(coordinates_magnitude, momenta)
        )
        wannier = np.sum(bloch_states, axis=1) / float(cell_count)
        spacing = period.magnitude / float(samples_per_cell)
        unnormalized_density = np.square(np.abs(wannier))
        quadrature_norm = float(spacing * np.sum(unnormalized_density))
        if quadrature_norm <= 0.0:
            raise ValueError("sampled Wannier function has zero quadrature norm")
        density = unnormalized_density / quadrature_norm
        center_magnitude = float(
            spacing * np.sum(coordinates_magnitude * density)
        )
        spread_magnitude = float(
            spacing
            * np.sum(np.square(coordinates_magnitude - center_magnitude) * density)
        )
        density_unit = (
            Unitless()
            if isinstance(period.unit, Unitless)
            else PhysicalUnit(f"1 / ({period.unit.expression})")
        )
        spread_unit = (
            Unitless()
            if isinstance(period.unit, Unitless)
            else PhysicalUnit(f"({period.unit.expression}) ** 2")
        )
        return BornVonKarmanLocalizationResult1D(
            source,
            basis,
            period,
            samples_per_cell,
            VectorQuantity(coordinates_magnitude, period.unit),
            VectorQuantity(density, density_unit),
            quadrature_norm,
            ScalarQuantity(center_magnitude, period.unit),
            ScalarQuantity(spread_magnitude, spread_unit),
            normalization_absolute_tolerance,
        )
