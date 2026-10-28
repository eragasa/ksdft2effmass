"""Typed configuration for direct Mathieu1D finite-reduction calculations."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self, cast

import numpy as np

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue


@dataclass(frozen=True, slots=True)
class Mathieu1dConfiguration(BaseTypedRecord):
    """Declare one finite Mathieu1D parent and single-band reduction.

    Parameters
    ----------
    period, reciprocal_vector, recoil_energy
        Positive finite dimensionless direct period, reciprocal period, and energy
        scale. ``period * reciprocal_vector`` must equal ``2π`` within
        ``duality_absolute_tolerance``.
    constant_coefficient, cosine_amplitude
        Finite dimensionless potential coefficients for the first harmonic
        ``constant_coefficient + cosine_amplitude * cos(2π x / period)``.
    duality_absolute_tolerance
        Nonnegative finite direct/reciprocal consistency tolerance.
    plane_wave_cutoffs
        Strictly increasing finite plane-wave refinement inventory.
    plane_wave_reference_cutoff
        Larger represented plane-wave reference cutoff.
    production_plane_wave_cutoff
        Selected production cutoff contained in the refinement inventory.
    finite_difference_points
        Strictly increasing periodic finite-difference grid sizes.
    parent_reduced_momenta, compared_band_count
        Ordered parent-refinement coordinates and compared spectral prefix.
    selected_band_index
        Zero-based band selected for the scalar reduction.
    reciprocal_training_mesh_size, evaluation_reduced_momenta
        Complete even training mesh extent and disjoint evaluation coordinates.
    hopping_ranges, fitting_weights
        Strictly increasing nonnegative truncation ranges and one positive fitting
        weight per training sample.
    coordinate_absolute_tolerance
        Nonnegative finite coordinate consistency tolerance.
    reconstruction_absolute_tolerance
        Nonnegative finite transform-reconstruction tolerance.
    hermiticity_absolute_tolerance
        Nonnegative finite hopping Hermiticity tolerance.
    parseval_absolute_tolerance
        Nonnegative finite Parseval tolerance in squared-energy dimensions.
    imaginary_absolute_tolerance
        Nonnegative finite imaginary-residual tolerance. All quantities are
        dimensionless in this model.

    Notes
    -----
    This record declares a finite represented calculation. It does not select a
    scientifically adequate range or establish continuum isolation.
    """

    period: float
    reciprocal_vector: float
    recoil_energy: float
    constant_coefficient: float
    cosine_amplitude: float
    duality_absolute_tolerance: float
    plane_wave_cutoffs: tuple[int, ...]
    plane_wave_reference_cutoff: int
    production_plane_wave_cutoff: int
    finite_difference_points: tuple[int, ...]
    parent_reduced_momenta: tuple[float, ...]
    compared_band_count: int
    selected_band_index: int
    reciprocal_training_mesh_size: int
    evaluation_reduced_momenta: tuple[float, ...]
    hopping_ranges: tuple[int, ...]
    fitting_weights: tuple[float, ...]
    coordinate_absolute_tolerance: float
    reconstruction_absolute_tolerance: float
    hermiticity_absolute_tolerance: float
    parseval_absolute_tolerance: float
    imaginary_absolute_tolerance: float

    def __post_init__(self) -> None:
        """Validate scalar domains and correlated finite inventories.

        Raises
        ------
        TypeError
            A value does not use its exact declared Python type.
        ValueError
            A value violates its domain or a cross-field invariant.
        """
        # First admit independent scalar domains. Cross-field checks below may then
        # safely use these values without silently propagating NaNs or infinities.
        for name in ("period", "reciprocal_vector", "recoil_energy"):
            self._positive_float(getattr(self, name), name)
        for name in (
            "constant_coefficient",
            "cosine_amplitude",
        ):
            self._finite_float(getattr(self, name), name)
        for name in (
            "duality_absolute_tolerance",
            "coordinate_absolute_tolerance",
            "reconstruction_absolute_tolerance",
            "hermiticity_absolute_tolerance",
            "parseval_absolute_tolerance",
            "imaginary_absolute_tolerance",
        ):
            self._nonnegative_float(getattr(self, name), name)
        # The direct and reciprocal periods describe the same cell. A mismatch here
        # would invalidate every phase factor used by both parent representations.
        if not np.isclose(
            self.period * self.reciprocal_vector,
            2.0 * np.pi,
            rtol=0.0,
            atol=self.duality_absolute_tolerance,
        ):
            raise ValueError("period and reciprocal_vector must be Fourier duals")
        # Ordered inventories are part of the wire contract: plots and result vectors
        # use positional correlation and must not infer an order after decoding.
        self._increasing_ints(
            self.plane_wave_cutoffs, "plane_wave_cutoffs", allow_zero=False
        )
        self._increasing_ints(
            self.finite_difference_points,
            "finite_difference_points",
            allow_zero=False,
        )
        self._increasing_ints(
            self.hopping_ranges,
            "hopping_ranges",
            allow_zero=True,
        )
        for name in (
            "plane_wave_reference_cutoff",
            "production_plane_wave_cutoff",
            "compared_band_count",
            "reciprocal_training_mesh_size",
        ):
            value = getattr(self, name)
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in int")
            if value <= 0:
                raise ValueError(f"{name} must be positive")
        if type(self.selected_band_index) is not int:
            raise TypeError("selected_band_index must be a built-in int")
        if self.selected_band_index < 0:
            raise ValueError("selected_band_index must be nonnegative")
        # The reference is a larger finite representation, not a continuum oracle.
        # Requiring a strictly larger cutoff prevents accidental self-comparison.
        if self.plane_wave_reference_cutoff <= self.plane_wave_cutoffs[-1]:
            raise ValueError(
                "plane_wave_reference_cutoff must exceed every sweep cutoff"
            )
        if self.production_plane_wave_cutoff not in self.plane_wave_cutoffs:
            raise ValueError(
                "production_plane_wave_cutoff must belong to plane_wave_cutoffs"
            )
        if self.compared_band_count > 2 * self.plane_wave_cutoffs[0] + 1:
            raise ValueError("compared bands must fit every plane-wave basis")
        if self.selected_band_index + 2 > 2 * self.production_plane_wave_cutoff + 1:
            raise ValueError(
                "production basis must contain the selected band and one neighbor"
            )
        if any(
            points <= self.compared_band_count
            for points in self.finite_difference_points
        ):
            raise ValueError(
                "finite-difference points must exceed the compared band count"
            )
        # An even mesh admits the authored centered half-open representative inventory
        # ``[-N/2, ..., N/2-1]`` used by the complete finite Fourier transform.
        if (
            self.reciprocal_training_mesh_size < 2
            or self.reciprocal_training_mesh_size % 2 != 0
        ):
            raise ValueError(
                "reciprocal_training_mesh_size must be even and at least two"
            )
        if self.hopping_ranges[-1] >= self.reciprocal_training_mesh_size // 2:
            raise ValueError(
                "hopping_ranges must be smaller than half the training mesh"
            )
        # Parent refinement includes the right zone boundary, whereas the complete
        # Fourier and withheld inventories use one half-open reciprocal period.
        self._reduced_coordinates(
            self.parent_reduced_momenta,
            "parent_reduced_momenta",
            upper_closed=True,
        )
        self._reduced_coordinates(
            self.evaluation_reduced_momenta,
            "evaluation_reduced_momenta",
            upper_closed=False,
        )
        if not isinstance(self.fitting_weights, tuple) or any(
            type(value) is not float for value in self.fitting_weights
        ):
            raise TypeError("fitting_weights must be a tuple of built-in floats")
        if len(self.fitting_weights) != self.reciprocal_training_mesh_size:
            raise ValueError("one fitting weight is required per training sample")
        if any(
            not np.isfinite(value) or value <= 0.0 for value in self.fitting_weights
        ):
            raise ValueError("fitting_weights must be finite and positive")
        # Withheld evaluation is meaningful only when no coordinate is also used to
        # construct the complete transform or fit the direct finite-range model.
        training = np.asarray(self.training_reduced_momenta, dtype=np.float64)
        evaluation = np.asarray(self.evaluation_reduced_momenta, dtype=np.float64)
        minimum_separation = float(
            np.min(np.abs(training[:, np.newaxis] - evaluation[np.newaxis, :]))
        )
        reduced_tolerance = self.coordinate_absolute_tolerance / self.reciprocal_vector
        if minimum_separation <= reduced_tolerance:
            raise ValueError("training and evaluation coordinates must be disjoint")

    @property
    def training_reduced_momenta(self) -> tuple[float, ...]:
        """Return the complete centered half-open training mesh.

        Returns
        -------
        tuple[float, ...]
            Coordinates ``-1/2 + j/N`` in increasing order.
        """
        size = self.reciprocal_training_mesh_size
        return tuple(-0.5 + float(index) / float(size) for index in range(size))

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "period": self.period,
            "reciprocal_vector": self.reciprocal_vector,
            "recoil_energy": self.recoil_energy,
            "constant_coefficient": self.constant_coefficient,
            "cosine_amplitude": self.cosine_amplitude,
            "duality_absolute_tolerance": self.duality_absolute_tolerance,
            "plane_wave_cutoffs": self.plane_wave_cutoffs,
            "plane_wave_reference_cutoff": self.plane_wave_reference_cutoff,
            "production_plane_wave_cutoff": self.production_plane_wave_cutoff,
            "finite_difference_points": self.finite_difference_points,
            "parent_reduced_momenta": self.parent_reduced_momenta,
            "compared_band_count": self.compared_band_count,
            "selected_band_index": self.selected_band_index,
            "reciprocal_training_mesh_size": self.reciprocal_training_mesh_size,
            "evaluation_reduced_momenta": self.evaluation_reduced_momenta,
            "hopping_ranges": self.hopping_ranges,
            "fitting_weights": self.fitting_weights,
            "coordinate_absolute_tolerance": self.coordinate_absolute_tolerance,
            "reconstruction_absolute_tolerance": (
                self.reconstruction_absolute_tolerance
            ),
            "hermiticity_absolute_tolerance": self.hermiticity_absolute_tolerance,
            "parseval_absolute_tolerance": self.parseval_absolute_tolerance,
            "imaginary_absolute_tolerance": self.imaginary_absolute_tolerance,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        fields = {
            "period",
            "reciprocal_vector",
            "recoil_energy",
            "constant_coefficient",
            "cosine_amplitude",
            "duality_absolute_tolerance",
            "plane_wave_cutoffs",
            "plane_wave_reference_cutoff",
            "production_plane_wave_cutoff",
            "finite_difference_points",
            "parent_reduced_momenta",
            "compared_band_count",
            "selected_band_index",
            "reciprocal_training_mesh_size",
            "evaluation_reduced_momenta",
            "hopping_ranges",
            "fitting_weights",
            "coordinate_absolute_tolerance",
            "reconstruction_absolute_tolerance",
            "hermiticity_absolute_tolerance",
            "parseval_absolute_tolerance",
            "imaginary_absolute_tolerance",
        }
        if set(values) != fields:
            raise ValueError("Mathieu1D configuration fields do not match")
        float_names = (
            "period",
            "reciprocal_vector",
            "recoil_energy",
            "constant_coefficient",
            "cosine_amplitude",
            "duality_absolute_tolerance",
            "coordinate_absolute_tolerance",
            "reconstruction_absolute_tolerance",
            "hermiticity_absolute_tolerance",
            "parseval_absolute_tolerance",
            "imaginary_absolute_tolerance",
        )
        if any(type(values[name]) is not float for name in float_names):
            raise TypeError("Mathieu1D scalar controls must decode to floats")
        integer_names = (
            "plane_wave_reference_cutoff",
            "production_plane_wave_cutoff",
            "compared_band_count",
            "selected_band_index",
            "reciprocal_training_mesh_size",
        )
        if any(type(values[name]) is not int for name in integer_names):
            raise TypeError("Mathieu1D integer controls must decode to ints")
        integer_tuple_names = (
            "plane_wave_cutoffs",
            "finite_difference_points",
            "hopping_ranges",
        )
        for name in integer_tuple_names:
            value = values[name]
            if not (
                isinstance(value, tuple) and all(type(item) is int for item in value)
            ):
                raise TypeError(f"{name} must decode to a tuple of ints")
        float_tuple_names = (
            "parent_reduced_momenta",
            "evaluation_reduced_momenta",
            "fitting_weights",
        )
        for name in float_tuple_names:
            value = values[name]
            if not (
                isinstance(value, tuple) and all(type(item) is float for item in value)
            ):
                raise TypeError(f"{name} must decode to a tuple of floats")
        return cls(
            period=cast(float, values["period"]),
            reciprocal_vector=cast(float, values["reciprocal_vector"]),
            recoil_energy=cast(float, values["recoil_energy"]),
            constant_coefficient=cast(float, values["constant_coefficient"]),
            cosine_amplitude=cast(float, values["cosine_amplitude"]),
            duality_absolute_tolerance=cast(
                float, values["duality_absolute_tolerance"]
            ),
            plane_wave_cutoffs=cast(tuple[int, ...], values["plane_wave_cutoffs"]),
            plane_wave_reference_cutoff=cast(
                int, values["plane_wave_reference_cutoff"]
            ),
            production_plane_wave_cutoff=cast(
                int, values["production_plane_wave_cutoff"]
            ),
            finite_difference_points=cast(
                tuple[int, ...], values["finite_difference_points"]
            ),
            parent_reduced_momenta=cast(
                tuple[float, ...], values["parent_reduced_momenta"]
            ),
            compared_band_count=cast(int, values["compared_band_count"]),
            selected_band_index=cast(int, values["selected_band_index"]),
            reciprocal_training_mesh_size=cast(
                int, values["reciprocal_training_mesh_size"]
            ),
            evaluation_reduced_momenta=cast(
                tuple[float, ...], values["evaluation_reduced_momenta"]
            ),
            hopping_ranges=cast(tuple[int, ...], values["hopping_ranges"]),
            fitting_weights=cast(tuple[float, ...], values["fitting_weights"]),
            coordinate_absolute_tolerance=cast(
                float, values["coordinate_absolute_tolerance"]
            ),
            reconstruction_absolute_tolerance=cast(
                float, values["reconstruction_absolute_tolerance"]
            ),
            hermiticity_absolute_tolerance=cast(
                float, values["hermiticity_absolute_tolerance"]
            ),
            parseval_absolute_tolerance=cast(
                float, values["parseval_absolute_tolerance"]
            ),
            imaginary_absolute_tolerance=cast(
                float, values["imaginary_absolute_tolerance"]
            ),
        )

    @staticmethod
    def _finite_float(value: float, name: str) -> None:
        if type(value) is not float:
            raise TypeError(f"{name} must be a built-in float")
        if not np.isfinite(value):
            raise ValueError(f"{name} must be finite")

    @classmethod
    def _positive_float(cls, value: float, name: str) -> None:
        cls._finite_float(value, name)
        if value <= 0.0:
            raise ValueError(f"{name} must be positive")

    @classmethod
    def _nonnegative_float(cls, value: float, name: str) -> None:
        cls._finite_float(value, name)
        if value < 0.0:
            raise ValueError(f"{name} must be nonnegative")

    @staticmethod
    def _increasing_ints(
        values: tuple[int, ...], name: str, *, allow_zero: bool
    ) -> None:
        if not isinstance(values, tuple) or any(
            type(value) is not int for value in values
        ):
            raise TypeError(f"{name} must be a tuple of built-in ints")
        if not values or values != tuple(sorted(set(values))):
            raise ValueError(f"{name} must be nonempty and strictly increasing")
        lower = 0 if allow_zero else 1
        if values[0] < lower:
            qualifier = "nonnegative" if allow_zero else "positive"
            raise ValueError(f"{name} must contain {qualifier} values")

    @staticmethod
    def _reduced_coordinates(
        values: tuple[float, ...],
        name: str,
        *,
        upper_closed: bool,
    ) -> None:
        if not isinstance(values, tuple) or any(
            type(value) is not float for value in values
        ):
            raise TypeError(f"{name} must be a tuple of built-in floats")
        if not values or values != tuple(sorted(set(values))):
            raise ValueError(f"{name} must be nonempty and strictly increasing")
        if any(not np.isfinite(value) for value in values):
            raise ValueError(f"{name} must contain finite values")
        if upper_closed:
            outside = any(value < -0.5 or value > 0.5 for value in values)
        else:
            outside = any(value < -0.5 or value >= 0.5 for value in values)
        if outside:
            raise ValueError(f"{name} must lie in the first reciprocal period")


__all__ = ["Mathieu1dConfiguration"]
