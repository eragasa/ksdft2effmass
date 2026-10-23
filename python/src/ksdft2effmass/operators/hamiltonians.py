"""Typed finite Hamiltonian representations."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.linalg import (
    ComplexMatrixQuantity,
    CsrComplexMatrixQuantity,
    CsrRealMatrixQuantity,
    MatrixVerifier,
    RealMatrixQuantity,
)

from .subspaces import SpectralSubspace

type HamiltonianMatrix = (
    RealMatrixQuantity
    | ComplexMatrixQuantity
    | CsrRealMatrixQuantity
    | CsrComplexMatrixQuantity
)


@dataclass(frozen=True, slots=True, eq=False, kw_only=True)
class Hamiltonian:
    """Represent one general finite Hamiltonian matrix with explicit units.

    Parameters
    ----------
    matrix
        Nonempty square real or complex dense or sparse matrix quantity.
        Construction does not require Hermiticity.

    Raises
    ------
    TypeError
        If ``matrix`` is not a real or complex matrix quantity.
    ValueError
        If ``matrix`` is empty or nonsquare.
    """

    matrix: HamiltonianMatrix

    def __post_init__(self) -> None:
        if not isinstance(
            self.matrix,
            RealMatrixQuantity
            | ComplexMatrixQuantity
            | CsrRealMatrixQuantity
            | CsrComplexMatrixQuantity,
        ):
            raise TypeError("matrix must be a dense or sparse matrix quantity")
        rows, columns = (
            self.matrix.magnitude.shape
            if isinstance(self.matrix, RealMatrixQuantity | ComplexMatrixQuantity)
            else self.matrix.shape
        )
        if rows == 0 or rows != columns:
            raise ValueError("Hamiltonian matrix must be nonempty and square")


@dataclass(frozen=True, slots=True, eq=False, kw_only=True)
class HermitianHamiltonian(Hamiltonian):
    """Represent a finite Hamiltonian whose matrix is exactly Hermitian.

    Parameters
    ----------
    matrix
        Nonempty square real or complex dense or sparse matrix quantity satisfying
        exact conjugate-transpose equality.

    Raises
    ------
    TypeError
        If the inherited Hamiltonian matrix contract fails.
    ValueError
        If the inherited shape contract fails or the matrix is not exactly
        Hermitian.

    Notes
    -----
    Construction intentionally invokes :class:`MatrixVerifier` with zero relative
    and absolute tolerances. Numerically Hermitian matrices that are not exactly
    Hermitian remain general :class:`Hamiltonian` instances.
    """

    def __post_init__(self) -> None:
        Hamiltonian.__post_init__(self)
        if not MatrixVerifier(self.matrix).is_hermitian():
            raise ValueError("Hamiltonian matrix must be exactly Hermitian")

    @classmethod
    def from_hamiltonian(
        cls,
        hamiltonian: Hamiltonian,
    ) -> HermitianHamiltonian:
        """Return the exact-Hermitian refinement of ``hamiltonian``.

        Parameters
        ----------
        hamiltonian
            General finite Hamiltonian to refine without changing its matrix.

        Returns
        -------
        HermitianHamiltonian
            New refinement retaining the exact matrix quantity.

        Raises
        ------
        TypeError
            If ``hamiltonian`` is not a :class:`Hamiltonian`.
        ValueError
            If its finite matrix is not exactly equal to its conjugate transpose.
        """
        if not isinstance(hamiltonian, Hamiltonian):
            raise TypeError("hamiltonian must be Hamiltonian")
        return cls(matrix=hamiltonian.matrix)


@dataclass(frozen=True, slots=True, eq=False, kw_only=True)
class ReducedHamiltonian(Hamiltonian):
    """Bind a reduced Hamiltonian to its spectral subspace and embedding.

    Parameters
    ----------
    matrix
        The reduced Hamiltonian in spectral-subspace coordinates, with shape
        ``(M, M)`` and explicit Hamiltonian units.
    spectral_subspace
        Abstract represented spectral subspace with parent dimension ``N`` and
        subspace dimension ``M``.
    embedded
        A Hamiltonian whose ``(N, N)`` matrix represents the reduced operator in
        parent coordinates.

    Raises
    ------
    TypeError
        If ``spectral_subspace`` or ``embedded`` has the wrong domain type.
    ValueError
        If reduced or embedded dimensions disagree with the spectral subspace, or
        their units differ.

    Notes
    -----
    The spectral subspace is not a projector. Its concrete representation supplies a
    finite-matrix spectral projector through ``spectral_subspace.projector()``. The
    abstract contract does not require that projector to be orthogonal.
    """

    spectral_subspace: SpectralSubspace
    embedded: Hamiltonian

    def __post_init__(self) -> None:
        Hamiltonian.__post_init__(self)
        if not isinstance(self.spectral_subspace, SpectralSubspace):
            raise TypeError("spectral_subspace must be SpectralSubspace")
        if not isinstance(self.embedded, Hamiltonian):
            raise TypeError("embedded must be Hamiltonian")
        reduced_dimension = self.spectral_subspace.dimension
        full_dimension = self.spectral_subspace.full_dimension
        reduced_shape = (
            self.matrix.magnitude.shape
            if isinstance(self.matrix, RealMatrixQuantity | ComplexMatrixQuantity)
            else self.matrix.shape
        )
        embedded_shape = (
            self.embedded.matrix.magnitude.shape
            if isinstance(
                self.embedded.matrix,
                RealMatrixQuantity | ComplexMatrixQuantity,
            )
            else self.embedded.matrix.shape
        )
        if reduced_shape != (reduced_dimension, reduced_dimension):
            raise ValueError("matrix shape must match the spectral subspace dimension")
        if embedded_shape != (full_dimension, full_dimension):
            raise ValueError("embedded matrix shape must match the full dimension")
        if self.matrix.unit != self.embedded.matrix.unit:
            raise ValueError("matrix and embedded Hamiltonian units must match")
