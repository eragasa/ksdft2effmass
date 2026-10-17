"""KSD-owned Fourier error channels and complete-shell composition.

ProjectKoios Numerics owns centered finite-mesh transforms, matrix-series evaluation,
Parseval arithmetic, and cyclic Hermiticity diagnostics. This module retains only the
band-equivalence study's physical-support selection and its matrix/band error channels.
"""

from __future__ import annotations

import math
from collections.abc import Iterator

import numpy as np
from numpy.typing import NDArray
from projectkoios.numerics.finite_periodic.meshes import CenteredUniformMesh
from projectkoios.numerics.finite_periodic.numpy.matrix_series import (
    NumpyFiniteFourierMatrixSeries,
)
from projectkoios.numerics.finite_periodic.numpy.tensor_product_evaluation import (
    NumpyTensorProductFourierMatrixEvaluationDefinition,
    NumpyTensorProductFourierMatrixSeriesEvaluator,
)

from .records import ErrorChannels

type ComplexArray = NDArray[np.complex128]
type FloatArray = NDArray[np.float64]
type IntArray = NDArray[np.int64]


def iter_complete_shell_fields(
    source_mesh: CenteredUniformMesh,
    series: NumpyFiniteFourierMatrixSeries,
    coordinate_axes: tuple[FloatArray, ...],
    metric_indices: IntArray,
    shells: tuple[int, ...],
) -> Iterator[ComplexArray]:
    """Evaluate cumulative KSD-selected complete physical-metric supports."""
    evaluator = NumpyTensorProductFourierMatrixSeriesEvaluator()
    for shell in shells:
        selected = metric_indices <= shell
        shell_series = NumpyFiniteFourierMatrixSeries.from_arrays(
            series.dimension,
            series.integer_modes[selected],
            series.matrix_coefficients[selected],
        )
        definition = NumpyTensorProductFourierMatrixEvaluationDefinition.from_arrays(
            source_mesh,
            shell_series,
            coordinate_axes,
        )
        yield evaluator.evaluate(definition).matrix_values


def maximum_matrix_defect(left: ComplexArray, right: ComplexArray) -> float:
    """Return the maximum pointwise matrix Frobenius defect."""
    return float(np.max(np.linalg.norm(left - right, axis=(-2, -1))))


def error_channels(approximation: ComplexArray, direct: ComplexArray) -> ErrorChannels:
    """Return separate normalized matrix and sorted-band error channels."""
    difference = approximation - direct
    matrix_norms = np.linalg.norm(difference, axis=(-2, -1)) / math.sqrt(2.0)
    approximation_bands = np.linalg.eigvalsh(approximation)
    direct_bands = np.linalg.eigvalsh(direct)
    band_difference = np.abs(approximation_bands - direct_bands)
    return ErrorChannels(
        maximum_hamiltonian=float(np.max(matrix_norms)),
        rms_hamiltonian=float(np.sqrt(np.mean(matrix_norms**2))),
        maximum_band=float(np.max(band_difference)),
        rms_band=float(np.sqrt(np.mean(band_difference**2))),
    )


__all__ = [
    "error_channels",
    "iter_complete_shell_fields",
    "maximum_matrix_defect",
]
