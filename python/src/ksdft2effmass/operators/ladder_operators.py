"""Immutable retained one-dimensional ladder-operator representation."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.linalg import CsrRealMatrixQuantity, Unitless


@dataclass(frozen=True, slots=True)
class LadderOperator1D:
    """Represent a retained ordered one-dimensional occupation-number basis.

    The finite annihilation and creation matrices obey the canonical commutator on all
    retained states except the highest state. For dimension ``K``, their commutator is
    ``I - K |K-1><K-1|``.

    Parameters
    ----------
    retained_dimension
        Positive built-in integer ``K`` defining ``|0>, ..., |K-1>``.
    """

    retained_dimension: int

    def __post_init__(self) -> None:
        if type(self.retained_dimension) is not int:
            raise TypeError("retained_dimension must be a built-in int")
        if self.retained_dimension <= 0:
            raise ValueError("retained_dimension must be positive")

    def annihilation(self) -> CsrRealMatrixQuantity:
        """Return the immutable sparse Unitless annihilation operator."""
        values = np.sqrt(np.arange(1, self.retained_dimension, dtype=np.float64))
        matrix = sparse.diags(
            values,
            offsets=1,
            shape=(self.retained_dimension, self.retained_dimension),
            format="csr",
            dtype=np.float64,
        )
        return CsrRealMatrixQuantity.from_csr(matrix, Unitless())

    def creation(self) -> CsrRealMatrixQuantity:
        """Return the immutable sparse Unitless creation operator."""
        return CsrRealMatrixQuantity.from_csr(
            self.annihilation().to_csr().transpose(), Unitless()
        )

    def number(self) -> CsrRealMatrixQuantity:
        """Return the exact diagonal immutable Unitless number operator.

        The diagonal is formed directly from integer labels so exact retained spectra
        are not perturbed by square-root roundoff from multiplying finite ladder
        matrices.
        """
        matrix = sparse.diags(
            np.arange(self.retained_dimension, dtype=np.float64),
            offsets=0,
            shape=(self.retained_dimension, self.retained_dimension),
            format="csr",
            dtype=np.float64,
        )
        return CsrRealMatrixQuantity.from_csr(matrix, Unitless())

    def commutator(self) -> CsrRealMatrixQuantity:
        """Return the finite sparse commutator ``a@adag - adag@a``."""
        annihilation = self.annihilation().to_csr()
        creation = self.creation().to_csr()
        return CsrRealMatrixQuantity.from_csr(
            annihilation @ creation - creation @ annihilation, Unitless()
        )
