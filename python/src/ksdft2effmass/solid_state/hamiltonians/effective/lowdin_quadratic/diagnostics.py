"""Intrinsic matrix diagnostics for Löwdin quadratic effective Hamiltonians.

These functions validate retained finite arrays. They do not derive a reduction,
perform an eigensolve, select a subspace, or establish scientific validity.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

type ComplexArray = npt.NDArray[np.complex128]


def maximum_frobenius(tensor: ComplexArray) -> float:
    """Return the largest matrix Frobenius norm in one tensor."""
    matrices = tensor.reshape((-1, tensor.shape[-2], tensor.shape[-1]))
    return float(max(np.linalg.norm(matrix) for matrix in matrices))


def antihermitian_maximum_frobenius(tensor: ComplexArray) -> float:
    """Return the largest matrix anti-Hermitian Frobenius defect."""
    matrices = tensor.reshape((-1, tensor.shape[-2], tensor.shape[-1]))
    return float(max(np.linalg.norm(matrix - matrix.conj().T) for matrix in matrices))


def covariance_maximum_frobenius(
    original: ComplexArray,
    transformed: ComplexArray,
    gauge: ComplexArray,
) -> float:
    """Return the largest selected-basis covariance defect."""
    matrices = original.reshape((-1, original.shape[-2], original.shape[-1]))
    changed = transformed.reshape((-1, transformed.shape[-2], transformed.shape[-1]))
    return float(
        max(
            np.linalg.norm(after - gauge.conj().T @ before @ gauge)
            for before, after in zip(matrices, changed, strict=True)
        )
    )


__all__ = [
    "antihermitian_maximum_frobenius",
    "covariance_maximum_frobenius",
    "maximum_frobenius",
]
