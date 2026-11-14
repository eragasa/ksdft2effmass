"""Independent dimension-neutral direct finite-Fourier reference arithmetic."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import final

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array, Int64Array

from ksdft2effmass.real_space_support_truncation import MetricGeometry


@dataclass(frozen=True, slots=True)
class _ErrorValues:
    maximum_matrix_frobenius: float
    root_mean_square_matrix_frobenius: float
    maximum_ordered_spectrum: float
    root_mean_square_ordered_spectrum: float


@dataclass(frozen=True, slots=True)
class _FourierChannel:
    coefficients: Complex128Array
    full_construction: Complex128Array
    full_evaluation: Complex128Array
    normalized_powers: Float64Array


@dataclass(frozen=True, slots=True)
class _ExpectedSupport:
    selected_index: int | None
    satisfying_error: float | None
    preceding_error: float | None
    minimum_observed_error: float
    largest_support_error: float


@final
class _DirectFiniteFourierGrid:
    """Own explicit construction/evaluation phases and independent metric shells."""

    __slots__ = (
        "_construction_phase",
        "_construction_shape",
        "_evaluation_phase",
        "_evaluation_shape",
        "_metric_indices",
        "_modes",
        "_ordinary",
        "_rank",
        "_transform_phase",
    )

    def __init__(
        self,
        *,
        spatial_dimension: int,
        construction_coordinates: Float64Array,
        evaluation_coordinates: Float64Array,
        construction_size: int,
        retained_rank: int,
        geometry: MetricGeometry,
    ) -> None:
        axis = np.arange(
            -construction_size // 2, construction_size // 2, dtype=np.int64
        )
        axes = tuple(axis for _ in range(spatial_dimension))
        all_modes = np.asarray(
            np.stack(np.meshgrid(*axes, indexing="ij"), axis=-1).reshape(
                -1, spatial_dimension
            ),
            dtype=np.int64,
        )
        ordinary = ~np.any(all_modes == -construction_size // 2, axis=1)
        modes = np.asarray(all_modes[ordinary], dtype=np.int64)
        construction_flat = construction_coordinates.reshape(-1, spatial_dimension)
        evaluation_flat = evaluation_coordinates.reshape(-1, spatial_dimension)
        self._transform_phase = np.asarray(
            np.exp(-2.0j * np.pi * (construction_flat @ all_modes.T)),
            dtype=np.complex128,
        )
        self._construction_phase = np.asarray(
            np.exp(2.0j * np.pi * (construction_flat @ modes.T)),
            dtype=np.complex128,
        )
        self._evaluation_phase = np.asarray(
            np.exp(2.0j * np.pi * (evaluation_flat @ modes.T)),
            dtype=np.complex128,
        )
        metric = geometry.direct_metric.metric_tensor
        metric_values = geometry.shell_metric_scale * np.einsum(
            "ri,ij,rj->r",
            modes,
            metric,
            modes,
        )
        rounded = np.rint(metric_values)
        if float(np.max(np.abs(metric_values - rounded))) > 1.0e-12:
            raise ValueError("independent scaled metric values are not integral")
        self._metric_indices = np.asarray(rounded, dtype=np.int64)
        self._modes = modes
        self._ordinary = np.asarray(ordinary, dtype=np.bool_)
        self._construction_shape = construction_coordinates.shape[:-1]
        self._evaluation_shape = evaluation_coordinates.shape[:-1]
        self._rank = retained_rank

    @property
    def metric_indices(self) -> Int64Array:
        """Return the independently classified ordinary-mode metric values."""
        return self._metric_indices

    @property
    def modes(self) -> Int64Array:
        """Return the independently enumerated ordinary Fourier modes."""
        return self._modes

    def channel(self, construction_field: Complex128Array) -> _FourierChannel:
        """Transform and evaluate one field through explicit dense finite sums."""
        point_count = math.prod(self._construction_shape)
        flattened = construction_field.reshape(point_count, self._rank * self._rank)
        all_coefficients = (self._transform_phase.T @ flattened) / float(point_count)
        coefficients = np.asarray(
            all_coefficients[self._ordinary].reshape(-1, self._rank, self._rank),
            dtype=np.complex128,
        )
        full_construction = np.asarray(
            (
                self._construction_phase @ coefficients.reshape(-1, self._rank**2)
            ).reshape(
                *self._construction_shape,
                self._rank,
                self._rank,
            ),
            dtype=np.complex128,
        )
        full_evaluation = np.asarray(
            (self._evaluation_phase @ coefficients.reshape(-1, self._rank**2)).reshape(
                *self._evaluation_shape,
                self._rank,
                self._rank,
            ),
            dtype=np.complex128,
        )
        normalized_powers = np.asarray(
            np.sum(np.abs(coefficients) ** 2, axis=(-2, -1)) / float(self._rank),
            dtype=np.float64,
        )
        return _FourierChannel(
            coefficients=coefficients,
            full_construction=full_construction,
            full_evaluation=full_evaluation,
            normalized_powers=normalized_powers,
        )

    def shell_evaluation(
        self,
        channel: _FourierChannel,
        metric_shell_value: int,
    ) -> Complex128Array:
        """Evaluate one complete cumulative physical-metric shell."""
        selected = self._metric_indices <= metric_shell_value
        return np.asarray(
            (
                self._evaluation_phase[:, selected]
                @ channel.coefficients[selected].reshape(-1, self._rank**2)
            ).reshape(*self._evaluation_shape, self._rank, self._rank),
            dtype=np.complex128,
        )


class _PeriodicRankNBandEquivalenceHoppingLocalityFourierReferenceArithmetic:
    """Own independent finite-sum arithmetic shared only between reference routes."""

    __slots__ = ()

    @staticmethod
    def _errors(
        approximation: Complex128Array,
        direct: Complex128Array,
    ) -> _ErrorValues:
        rank = int(approximation.shape[-1])
        difference = approximation - direct
        frobenius = np.linalg.norm(difference, axis=(-2, -1))
        band_difference = np.abs(
            np.linalg.eigvalsh(approximation) - np.linalg.eigvalsh(direct)
        )
        band_l2 = np.linalg.norm(band_difference, axis=-1)
        rank_scale = math.sqrt(rank)
        return _ErrorValues(
            maximum_matrix_frobenius=float(np.max(frobenius)) / rank_scale,
            root_mean_square_matrix_frobenius=(
                float(np.sqrt(np.mean(frobenius**2))) / rank_scale
            ),
            maximum_ordered_spectrum=float(np.max(band_difference)),
            root_mean_square_ordered_spectrum=(
                float(np.sqrt(np.mean(band_l2**2))) / rank_scale
            ),
        )

    @staticmethod
    def _selection(errors: tuple[float, ...], tolerance: float) -> _ExpectedSupport:
        selected = next(
            (index for index, error in enumerate(errors) if error <= tolerance),
            None,
        )
        if selected is None:
            return _ExpectedSupport(
                selected_index=None,
                satisfying_error=None,
                preceding_error=None,
                minimum_observed_error=min(errors),
                largest_support_error=errors[-1],
            )
        return _ExpectedSupport(
            selected_index=selected,
            satisfying_error=errors[selected],
            preceding_error=None if selected == 0 else errors[selected - 1],
            minimum_observed_error=min(errors),
            largest_support_error=errors[-1],
        )
