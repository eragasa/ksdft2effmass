"""Reusable Hamiltonian reduction through explicit subspace coordinates."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    ComplexSparseMatrixQuantity,
    MatrixQuantity,
    Unitless,
)

from .records import Hamiltonian, ReducedHamiltonian
from .subspaces import SpectralSubspace


@dataclass(frozen=True, slots=True, eq=False, kw_only=True)
class SpectralReduction:
    """Eagerly reduce one Hamiltonian through one represented spectral subspace.

    Parameters
    ----------
    hamiltonian
        Parent-coordinate Hamiltonian.
    spectral_subspace
        Subspace supplying explicit parent-to-reduced and reduced-to-parent maps.

    Notes
    -----
    Construction applies no tolerance or acceptance policy. A projector alone does
    not define reduced coordinates, so reduction uses the two maps supplied by the
    retained subspace. The correlated result is available through
    :attr:`reduced_hamiltonian`.
    """

    hamiltonian: Hamiltonian
    spectral_subspace: SpectralSubspace
    _reduced_hamiltonian: ReducedHamiltonian = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if not isinstance(self.hamiltonian, Hamiltonian):
            raise TypeError("hamiltonian must be Hamiltonian")
        if not isinstance(self.spectral_subspace, SpectralSubspace):
            raise TypeError("spectral_subspace must be SpectralSubspace")
        matrix = self.hamiltonian.matrix
        full_dimension = self.spectral_subspace.full_dimension
        reduced_dimension = self.spectral_subspace.dimension
        matrix_shape = (
            matrix.magnitude.shape
            if isinstance(matrix, MatrixQuantity | ComplexMatrixQuantity)
            else matrix.shape
        )
        if matrix_shape != (full_dimension, full_dimension):
            raise ValueError("Hamiltonian and spectral subspace dimensions must agree")
        reduction_map = self.spectral_subspace.reduction_map
        embedding_map = self.spectral_subspace.embedding_map
        if not isinstance(reduction_map, MatrixQuantity | ComplexMatrixQuantity):
            raise TypeError("reduction_map must be a dense matrix quantity")
        if not isinstance(reduction_map.unit, Unitless):
            raise ValueError("reduction_map must be Unitless")
        if reduction_map.magnitude.shape != (reduced_dimension, full_dimension):
            raise ValueError(
                "reduction_map shape does not match the spectral subspace"
            )
        if not isinstance(embedding_map, MatrixQuantity | ComplexMatrixQuantity):
            raise TypeError("embedding_map must be a dense matrix quantity")
        if not isinstance(embedding_map.unit, Unitless):
            raise ValueError("embedding_map must be Unitless")
        if embedding_map.magnitude.shape != (full_dimension, reduced_dimension):
            raise ValueError(
                "embedding_map shape does not match the spectral subspace"
            )
        represented = (
            matrix.magnitude
            if isinstance(matrix, MatrixQuantity | ComplexMatrixQuantity)
            else matrix.to_csr()
        )
        reduced_values = (
            reduction_map.magnitude @ represented @ embedding_map.magnitude
        )
        is_complex = isinstance(
            matrix, ComplexMatrixQuantity | ComplexSparseMatrixQuantity
        ) or isinstance(
            reduction_map, ComplexMatrixQuantity
        ) or isinstance(embedding_map, ComplexMatrixQuantity)
        reduced_matrix: MatrixQuantity | ComplexMatrixQuantity
        embedded_matrix: MatrixQuantity | ComplexMatrixQuantity
        if is_complex:
            reduced_matrix = ComplexMatrixQuantity(
                np.asarray(reduced_values, dtype=np.complex128), matrix.unit
            )
            embedded_matrix = ComplexMatrixQuantity(
                np.asarray(
                    embedding_map.magnitude
                    @ reduced_matrix.magnitude
                    @ reduction_map.magnitude,
                    dtype=np.complex128,
                ),
                matrix.unit,
            )
        else:
            reduced_matrix = MatrixQuantity(
                np.asarray(reduced_values, dtype=np.float64), matrix.unit
            )
            embedded_matrix = MatrixQuantity(
                np.asarray(
                    embedding_map.magnitude
                    @ reduced_matrix.magnitude
                    @ reduction_map.magnitude,
                    dtype=np.float64,
                ),
                matrix.unit,
            )
        object.__setattr__(
            self,
            "_reduced_hamiltonian",
            ReducedHamiltonian(
                matrix=reduced_matrix,
                spectral_subspace=self.spectral_subspace,
                embedded=Hamiltonian(matrix=embedded_matrix),
            ),
        )

    @property
    def reduced_hamiltonian(self) -> ReducedHamiltonian:
        """Return the eagerly constructed correlated reduced Hamiltonian."""
        return self._reduced_hamiltonian
