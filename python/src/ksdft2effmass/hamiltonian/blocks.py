"""Orthogonal block analysis of finite Hamiltonians."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    ComplexSparseMatrixQuantity,
    MatrixQuantity,
)

from .records import Hamiltonian
from .subspaces import OrthogonalSpectralSubspace

type HamiltonianBlockMatrix = MatrixQuantity | ComplexMatrixQuantity


@dataclass(frozen=True, slots=True, eq=False)
class OrthogonalHamiltonianBlockResult:
    r"""Retain the four parent-coordinate blocks induced by $P$ and $Q=I-P$."""

    hamiltonian: Hamiltonian
    spectral_subspace: OrthogonalSpectralSubspace
    retained: HamiltonianBlockMatrix
    retained_to_discarded: HamiltonianBlockMatrix
    discarded_to_retained: HamiltonianBlockMatrix
    discarded: HamiltonianBlockMatrix

    def __post_init__(self) -> None:
        if not isinstance(self.hamiltonian, Hamiltonian):
            raise TypeError("hamiltonian must be Hamiltonian")
        if not isinstance(self.spectral_subspace, OrthogonalSpectralSubspace):
            raise TypeError("spectral_subspace must be OrthogonalSpectralSubspace")
        full_dimension = self.spectral_subspace.full_dimension
        expected_shape = (full_dimension, full_dimension)
        expected_unit = self.hamiltonian.matrix.unit
        for name, block in (
            ("retained", self.retained),
            ("retained_to_discarded", self.retained_to_discarded),
            ("discarded_to_retained", self.discarded_to_retained),
            ("discarded", self.discarded),
        ):
            if not isinstance(block, MatrixQuantity | ComplexMatrixQuantity):
                raise TypeError(f"{name} must be a dense matrix quantity")
            if block.magnitude.shape != expected_shape:
                raise ValueError(f"{name} must match the parent dimension")
            if block.unit != expected_unit:
                raise ValueError(f"{name} unit must match the Hamiltonian")


class OrthogonalHamiltonianBlockAnalyzer:
    r"""Construct $PHP$, $PHQ$, $QHP$, and $QHQ$ without interpreting them."""

    __slots__ = ()

    def execute(
        self,
        hamiltonian: Hamiltonian,
        spectral_subspace: OrthogonalSpectralSubspace,
    ) -> OrthogonalHamiltonianBlockResult:
        """Return the four orthogonal parent-coordinate Hamiltonian blocks."""
        if not isinstance(hamiltonian, Hamiltonian):
            raise TypeError("hamiltonian must be Hamiltonian")
        if not isinstance(spectral_subspace, OrthogonalSpectralSubspace):
            raise TypeError("spectral_subspace must be OrthogonalSpectralSubspace")
        matrix = hamiltonian.matrix
        shape = (
            matrix.magnitude.shape
            if isinstance(matrix, MatrixQuantity | ComplexMatrixQuantity)
            else matrix.shape
        )
        full_dimension = spectral_subspace.full_dimension
        if shape != (full_dimension, full_dimension):
            raise ValueError("Hamiltonian and spectral subspace dimensions must agree")
        represented = (
            matrix.magnitude
            if isinstance(matrix, MatrixQuantity | ComplexMatrixQuantity)
            else matrix.to_csr()
        )
        projector = spectral_subspace.projector.magnitude
        complement = spectral_subspace.complement_projector.magnitude
        retained_values = np.asarray(projector @ represented @ projector)
        retained_to_discarded_values = np.asarray(
            projector @ represented @ complement
        )
        discarded_to_retained_values = np.asarray(
            complement @ represented @ projector
        )
        discarded_values = np.asarray(complement @ represented @ complement)
        if isinstance(matrix, ComplexMatrixQuantity | ComplexSparseMatrixQuantity):
            retained: HamiltonianBlockMatrix = ComplexMatrixQuantity(
                np.asarray(retained_values, dtype=np.complex128), matrix.unit
            )
            retained_to_discarded: HamiltonianBlockMatrix = ComplexMatrixQuantity(
                np.asarray(retained_to_discarded_values, dtype=np.complex128),
                matrix.unit,
            )
            discarded_to_retained: HamiltonianBlockMatrix = ComplexMatrixQuantity(
                np.asarray(discarded_to_retained_values, dtype=np.complex128),
                matrix.unit,
            )
            discarded: HamiltonianBlockMatrix = ComplexMatrixQuantity(
                np.asarray(discarded_values, dtype=np.complex128), matrix.unit
            )
        else:
            retained = MatrixQuantity(
                np.asarray(retained_values, dtype=np.float64), matrix.unit
            )
            retained_to_discarded = MatrixQuantity(
                np.asarray(retained_to_discarded_values, dtype=np.float64), matrix.unit
            )
            discarded_to_retained = MatrixQuantity(
                np.asarray(discarded_to_retained_values, dtype=np.float64), matrix.unit
            )
            discarded = MatrixQuantity(
                np.asarray(discarded_values, dtype=np.float64), matrix.unit
            )
        return OrthogonalHamiltonianBlockResult(
            hamiltonian=hamiltonian,
            spectral_subspace=spectral_subspace,
            retained=retained,
            retained_to_discarded=retained_to_discarded,
            discarded_to_retained=discarded_to_retained,
            discarded=discarded,
        )
