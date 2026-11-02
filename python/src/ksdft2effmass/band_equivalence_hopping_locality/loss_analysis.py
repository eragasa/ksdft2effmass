"""Production calculation of finite-rank band-equivalence/locality losses."""

from __future__ import annotations

import math

import numpy as np
from numpy.typing import NDArray

from ksdft2effmass.analysis.matrix_field import MatrixFieldHermiticityAnalyzer

from .loss_value import (
    BandEquivalenceHoppingLocalityLoss,
    BandEquivalenceHoppingLocalityLossDefinition,
    _loss_normalization,
)

type ComplexArray = NDArray[np.complex128]
type RealArray = NDArray[np.float64]


class BandEquivalenceHoppingLocalityLossAnalyzer:
    """Calculate one bound finite-rank loss through the vectorized route.

    Binary64 overflow, underflow, or a nonfinite intermediate raises
    :class:`FloatingPointError`; arithmetic is never clipped.
    """

    __slots__ = ("_approximation", "_definition", "_reference")

    def __init__(
        self,
        *,
        reference: ComplexArray,
        approximation: ComplexArray,
        definition: BandEquivalenceHoppingLocalityLossDefinition,
    ) -> None:
        if type(definition) is not BandEquivalenceHoppingLocalityLossDefinition:
            raise TypeError(
                "definition must be BandEquivalenceHoppingLocalityLossDefinition"
            )
        reference_value, approximation_value = _production_matrix_fields(
            reference,
            approximation,
            definition,
        )
        self._reference = reference_value
        self._approximation = approximation_value
        self._definition = definition

    def execute(self) -> BandEquivalenceHoppingLocalityLoss:
        """Return vectorized direct finite-sum losses normalized by rank."""
        normalization = _loss_normalization(
            self._definition.retained_rank,
            self._definition.norm_energy_scale,
        )
        weights = np.asarray(
            self._definition.sample_measure.sample_weights,
            dtype=np.float64,
        )

        difference = self._reference - self._approximation
        operator_squares = _operator_squared_norms(difference)
        operator_sum = _weighted_sum(
            weights,
            operator_squares,
            "operator-loss",
        )
        operator_loss = _normalized_loss(
            operator_sum,
            normalization,
            "operator loss",
        )

        reference_spectrum = np.linalg.eigvalsh(self._reference)
        approximation_spectrum = np.linalg.eigvalsh(self._approximation)
        if not bool(np.isfinite(reference_spectrum).all()) or not bool(
            np.isfinite(approximation_spectrum).all()
        ):
            raise FloatingPointError("ordered-spectrum calculation became nonfinite")
        spectral_squares = _ordered_spectrum_squared_errors(
            reference_spectrum,
            approximation_spectrum,
        )
        spectral_sum = _weighted_sum(
            weights,
            spectral_squares,
            "ordered-spectrum",
        )
        spectral_loss = _normalized_loss(
            spectral_sum,
            normalization,
            "ordered-spectrum loss",
        )

        return BandEquivalenceHoppingLocalityLoss(
            definition=self._definition,
            operator_loss=operator_loss,
            spectral_loss=spectral_loss,
        )


def _production_matrix_fields(
    reference: ComplexArray,
    approximation: ComplexArray,
    definition: BandEquivalenceHoppingLocalityLossDefinition,
) -> tuple[ComplexArray, ComplexArray]:
    reference_analyzer = MatrixFieldHermiticityAnalyzer(
        reference,
        definition.norm_energy_scale,
    )
    approximation_analyzer = MatrixFieldHermiticityAnalyzer(
        approximation,
        definition.norm_energy_scale,
    )
    reference_hermiticity = reference_analyzer.execute()
    approximation_hermiticity = approximation_analyzer.execute()
    reference_value = reference_analyzer.matrices
    approximation_value = approximation_analyzer.matrices
    expected_matrix_shape = (definition.retained_rank, definition.retained_rank)
    if (
        reference_value.ndim != definition.sample_measure.spatial_dimension + 2
        or reference_value.shape[-2:] != expected_matrix_shape
    ):
        raise ValueError("reference must match the loss definition")
    if tuple(int(size) for size in reference_value.shape[:-2]) != (
        definition.sample_measure.sample_shape
    ):
        raise ValueError("reference sample shape must match the loss definition")
    if approximation_value.shape != reference_value.shape:
        raise ValueError("approximation and reference shapes must match")
    if not reference_hermiticity.exactly_hermitian:
        raise ValueError("reference matrices must be exactly Hermitian")
    if not approximation_hermiticity.exactly_hermitian:
        raise ValueError("approximation matrices must be exactly Hermitian")
    return reference_value, approximation_value


def _operator_squared_norms(difference: ComplexArray) -> RealArray:
    with np.errstate(over="ignore", under="ignore", invalid="ignore"):
        real_squares = difference.real * difference.real
        imaginary_squares = difference.imag * difference.imag
    if bool(np.logical_and(difference.real != 0.0, real_squares == 0.0).any()) or bool(
        np.logical_and(difference.imag != 0.0, imaginary_squares == 0.0).any()
    ):
        raise FloatingPointError("operator-loss squared terms underflowed")
    if not bool(np.isfinite(real_squares).all()) or not bool(
        np.isfinite(imaginary_squares).all()
    ):
        raise FloatingPointError("operator-loss squared terms overflowed")
    with np.errstate(over="ignore", under="ignore", invalid="ignore"):
        squared_entries = real_squares + imaginary_squares
        squared_norms = np.sum(squared_entries, axis=(-2, -1)).reshape(-1)
    if not bool(np.isfinite(squared_norms).all()):
        raise FloatingPointError("operator-loss finite sum overflowed")
    return squared_norms


def _ordered_spectrum_squared_errors(
    reference_spectrum: RealArray,
    approximation_spectrum: RealArray,
) -> RealArray:
    difference = reference_spectrum - approximation_spectrum
    with np.errstate(over="ignore", under="ignore", invalid="ignore"):
        squared_differences = difference * difference
    if bool(np.logical_and(difference != 0.0, squared_differences == 0.0).any()):
        raise FloatingPointError("ordered-spectrum squared terms underflowed")
    if not bool(np.isfinite(squared_differences).all()):
        raise FloatingPointError("ordered-spectrum squared terms overflowed")
    with np.errstate(over="ignore", under="ignore", invalid="ignore"):
        squared_errors = np.sum(squared_differences, axis=-1).reshape(-1)
    if not bool(np.isfinite(squared_errors).all()):
        raise FloatingPointError("ordered-spectrum finite sum overflowed")
    return squared_errors


def _weighted_sum(weights: RealArray, terms: RealArray, name: str) -> float:
    with np.errstate(over="ignore", under="ignore", invalid="ignore"):
        weighted_terms = weights * terms
    if bool(
        np.logical_and(
            np.logical_and(weights != 0.0, terms != 0.0),
            weighted_terms == 0.0,
        ).any()
    ):
        raise FloatingPointError(f"{name} weighted terms underflowed")
    if not bool(np.isfinite(weighted_terms).all()):
        raise FloatingPointError(f"{name} weighted terms overflowed")
    result = float(np.sum(weighted_terms))
    if not math.isfinite(result):
        raise FloatingPointError(f"{name} finite sum overflowed")
    return result


def _normalized_loss(value: float, normalization: float, name: str) -> float:
    result = value / normalization
    if value != 0.0 and result == 0.0:
        raise FloatingPointError(f"normalized {name} underflowed")
    if not math.isfinite(result):
        raise FloatingPointError(f"normalized {name} became nonfinite")
    return result


__all__ = ["BandEquivalenceHoppingLocalityLossAnalyzer"]
