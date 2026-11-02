"""Independent reconstruction of finite-rank band-equivalence/locality losses."""

from __future__ import annotations

import math

import numpy as np
from numpy.typing import NDArray
from scipy.linalg import eigvalsh as scipy_eigvalsh  # type: ignore[import-untyped]

from ksdft2effmass.analysis.matrix_field import matrix_field

from .loss_value import (
    BandEquivalenceHoppingLocalityLoss,
    BandEquivalenceHoppingLocalityLossDefinition,
)

type ComplexArray = NDArray[np.complex128]


class BandEquivalenceHoppingLocalityLossIndependentReferenceAnalyzer:
    """Reconstruct one bound loss without production analyzers or arithmetic.

    Matrix admission, denominator reconstruction, scalar matrix-element sums, SciPy
    ordered spectra, weighting, and normalization are independent of the production
    loss route. Binary64 overflow, underflow, or a nonfinite intermediate raises
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
        reference_value = _independent_matrix_field("reference", reference)
        approximation_value = _independent_matrix_field(
            "approximation",
            approximation,
        )
        expected_shape = definition.sample_measure.sample_shape + (
            definition.retained_rank,
            definition.retained_rank,
        )
        if reference_value.shape != expected_shape:
            raise ValueError("reference must match the loss definition")
        if approximation_value.shape != reference_value.shape:
            raise ValueError("approximation and reference shapes must match")
        if not _independently_exactly_hermitian(reference_value):
            raise ValueError("reference matrices must be exactly Hermitian")
        if not _independently_exactly_hermitian(approximation_value):
            raise ValueError("approximation matrices must be exactly Hermitian")
        self._reference = reference_value
        self._approximation = approximation_value
        self._definition = definition

    def execute(self) -> BandEquivalenceHoppingLocalityLoss:
        """Return independent scalar finite-sum and ordered-spectrum losses."""
        normalization = _independent_loss_normalization(self._definition)
        operator_terms: list[float] = []
        spectral_terms: list[float] = []
        rank = self._definition.retained_rank

        for flat_index, index in enumerate(np.ndindex(self._reference.shape[:-2])):
            reference = self._reference[index]
            approximation = self._approximation[index]
            matrix_terms: list[float] = []
            for row in range(rank):
                for column in range(rank):
                    difference = complex(reference[row, column]) - complex(
                        approximation[row, column]
                    )
                    matrix_terms.append(
                        _independent_square(difference.real, "operator-loss")
                        + _independent_square(difference.imag, "operator-loss")
                    )
            try:
                matrix_square = math.fsum(matrix_terms)
            except OverflowError as error:
                raise FloatingPointError(
                    "independent operator finite sum overflowed"
                ) from error
            if not math.isfinite(matrix_square):
                raise FloatingPointError("independent operator finite sum overflowed")

            reference_spectrum = scipy_eigvalsh(
                reference,
                lower=True,
                check_finite=False,
                driver="evr",
            )
            approximation_spectrum = scipy_eigvalsh(
                approximation,
                lower=True,
                check_finite=False,
                driver="evr",
            )
            if not bool(np.isfinite(reference_spectrum).all()) or not bool(
                np.isfinite(approximation_spectrum).all()
            ):
                raise FloatingPointError(
                    "independent ordered-spectrum calculation became nonfinite"
                )
            spectrum_terms = [
                _independent_square(
                    float(reference_spectrum[state])
                    - float(approximation_spectrum[state]),
                    "ordered-spectrum",
                )
                for state in range(rank)
            ]
            try:
                spectrum_square = math.fsum(spectrum_terms)
            except OverflowError as error:
                raise FloatingPointError(
                    "independent ordered-spectrum finite sum overflowed"
                ) from error
            if not math.isfinite(spectrum_square):
                raise FloatingPointError(
                    "independent ordered-spectrum finite sum overflowed"
                )

            weight = self._definition.sample_measure.sample_weights[flat_index]
            operator_terms.append(
                _independent_weighted_term(weight, matrix_square, "operator-loss")
            )
            spectral_terms.append(
                _independent_weighted_term(
                    weight,
                    spectrum_square,
                    "ordered-spectrum",
                )
            )

        try:
            operator_sum = math.fsum(operator_terms)
            spectral_sum = math.fsum(spectral_terms)
        except OverflowError as error:
            raise FloatingPointError(
                "independent loss finite sum overflowed"
            ) from error
        if not math.isfinite(operator_sum) or not math.isfinite(spectral_sum):
            raise FloatingPointError("independent loss finite sum became nonfinite")

        return BandEquivalenceHoppingLocalityLoss(
            definition=self._definition,
            operator_loss=_independent_normalized_loss(
                operator_sum,
                normalization,
                "operator loss",
            ),
            spectral_loss=_independent_normalized_loss(
                spectral_sum,
                normalization,
                "ordered-spectrum loss",
            ),
        )


def _independent_matrix_field(name: str, value: ComplexArray) -> ComplexArray:
    admitted = matrix_field(name, value)
    result = np.array(admitted, dtype=np.complex128, copy=True)
    result.setflags(write=False)
    return result


def _independently_exactly_hermitian(value: ComplexArray) -> bool:
    rank = int(value.shape[-1])
    for index in np.ndindex(value.shape[:-2]):
        matrix = value[index]
        for row in range(rank):
            for column in range(rank):
                if (
                    complex(matrix[row, column])
                    != complex(matrix[column, row]).conjugate()
                ):
                    return False
    return True


def _independent_loss_normalization(
    definition: BandEquivalenceHoppingLocalityLossDefinition,
) -> float:
    try:
        scale_squared = definition.norm_energy_scale * definition.norm_energy_scale
        normalization = definition.retained_rank * scale_squared
    except OverflowError as error:
        raise FloatingPointError("independent loss normalization overflowed") from error
    if not math.isfinite(scale_squared) or not math.isfinite(normalization):
        raise FloatingPointError("independent loss normalization overflowed")
    if scale_squared == 0.0 or normalization == 0.0:
        raise FloatingPointError("independent loss normalization underflowed")
    return normalization


def _independent_square(value: float, name: str) -> float:
    try:
        result = value * value
    except OverflowError as error:
        raise FloatingPointError(
            f"independent {name} squared term overflowed"
        ) from error
    if value != 0.0 and result == 0.0:
        raise FloatingPointError(f"independent {name} squared term underflowed")
    if not math.isfinite(result):
        raise FloatingPointError(f"independent {name} squared term overflowed")
    return result


def _independent_weighted_term(weight: float, value: float, name: str) -> float:
    result = weight * value
    if weight != 0.0 and value != 0.0 and result == 0.0:
        raise FloatingPointError(f"independent {name} weighted term underflowed")
    if not math.isfinite(result):
        raise FloatingPointError(f"independent {name} weighted term overflowed")
    return result


def _independent_normalized_loss(
    value: float,
    normalization: float,
    name: str,
) -> float:
    result = value / normalization
    if value != 0.0 and result == 0.0:
        raise FloatingPointError(f"independent normalized {name} underflowed")
    if not math.isfinite(result):
        raise FloatingPointError(f"independent normalized {name} became nonfinite")
    return result


__all__ = ["BandEquivalenceHoppingLocalityLossIndependentReferenceAnalyzer"]
