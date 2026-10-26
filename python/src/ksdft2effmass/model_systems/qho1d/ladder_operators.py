"""Retained ladder-operator representation of the harmonic oscillator."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from projectkoios.physkit.units import SparseMatrixQuantity
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.operators import LadderOperator1D

from .analytical import Qho1dAnalytical


@dataclass(frozen=True, slots=True)
class Qho1dLadderOperators:
    """Apply harmonic-oscillator energy scaling to a generic ladder basis.

    Parameters
    ----------
    analytical
        Exact oscillator model supplying the energy scale.
    ladder_operator
        Generic retained one-dimensional occupation-number basis.
    """

    analytical: Qho1dAnalytical
    ladder_operator: LadderOperator1D

    def __post_init__(self) -> None:
        if not isinstance(self.analytical, Qho1dAnalytical):
            raise TypeError("analytical must be Qho1dAnalytical")
        if not isinstance(self.ladder_operator, LadderOperator1D):
            raise TypeError("ladder_operator must be LadderOperator1D")

    @property
    def retained_dimension(self) -> int:
        """Return the generic ladder basis dimension."""
        return self.ladder_operator.retained_dimension

    def annihilation(self) -> SparseMatrixQuantity:
        """Return the composed sparse Unitless annihilation operator."""
        return self.ladder_operator.annihilation()

    def creation(self) -> SparseMatrixQuantity:
        """Return the composed sparse Unitless creation operator."""
        return self.ladder_operator.creation()

    def number(self) -> SparseMatrixQuantity:
        """Return the composed exact sparse Unitless number operator."""
        return self.ladder_operator.number()

    def hamiltonian(self) -> SparseMatrixQuantity:
        """Return the sparse retained ``hbar*omega*(N + I/2)`` matrix."""
        energies = self.analytical.number_state_energies(self.retained_dimension)
        matrix = sparse.diags(
            energies.magnitude,
            offsets=0,
            shape=(self.retained_dimension, self.retained_dimension),
            format="csr",
            dtype=np.float64,
        )
        return SparseMatrixQuantity.from_csr(matrix, energies.unit)

    def commutator(self) -> SparseMatrixQuantity:
        """Return the composed finite sparse Unitless ladder commutator."""
        return self.ladder_operator.commutator()
