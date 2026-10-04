"""Public orthogonal spectral-subspace selection and operator compression."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .eigenpairs import RealSymmetricEigenpairResult, RealSymmetricOperator
from .quantities import MatrixQuantity, SparseMatrixQuantity, Unitless, VectorQuantity


@dataclass(frozen=True, slots=True, eq=False)
class OrthogonalSpectralSubspace:
    """Retain selected eigenvalues and an orthonormal column embedding."""

    eigenvalues: VectorQuantity
    basis_vectors: MatrixQuantity

    def __post_init__(self) -> None:
        if not isinstance(self.eigenvalues, VectorQuantity):
            raise TypeError("eigenvalues must be VectorQuantity")
        if not isinstance(self.basis_vectors, MatrixQuantity):
            raise TypeError("basis_vectors must be MatrixQuantity")
        if not isinstance(self.basis_vectors.unit, Unitless):
            raise ValueError("basis_vectors must be Unitless")
        rows, columns = self.basis_vectors.magnitude.shape
        if rows <= 0 or columns <= 0 or columns > rows:
            raise ValueError("basis_vectors must have shape N by K with 1 <= K <= N")
        if self.eigenvalues.magnitude.shape != (columns,):
            raise ValueError("eigenvalues must match the retained dimension")
        gram = self.basis_vectors.magnitude.T @ self.basis_vectors.magnitude
        tolerance = 128.0 * np.finfo(np.float64).eps * max(rows, columns)
        if not np.allclose(gram, np.eye(columns), rtol=0.0, atol=tolerance):
            raise ValueError(
                "basis_vectors must be orthonormal within binary64 tolerance"
            )

    @property
    def full_dimension(self) -> int:
        """Return the represented full-space dimension."""
        return int(self.basis_vectors.magnitude.shape[0])

    @property
    def retained_dimension(self) -> int:
        """Return the selected spectral-subspace dimension."""
        return int(self.basis_vectors.magnitude.shape[1])

    def projector(self) -> MatrixQuantity:
        """Materialize the full-space orthogonal projector at an explicit boundary."""
        vectors = self.basis_vectors.magnitude
        return MatrixQuantity(vectors @ vectors.T, Unitless())

    def complement_projector(self) -> MatrixQuantity:
        """Materialize the complementary full-space orthogonal projector."""
        projector = self.projector().magnitude
        return MatrixQuantity(np.eye(self.full_dimension) - projector, Unitless())


class OrthogonalSpectralSubspaceSelector:
    """Select the lowest ordered eigenpairs as one orthogonal spectral subspace."""

    __slots__ = ()

    def execute(
        self, eigenpairs: RealSymmetricEigenpairResult, retained_dimension: int
    ) -> OrthogonalSpectralSubspace:
        """Return the first ``retained_dimension`` ordered eigenpairs."""
        if not isinstance(eigenpairs, RealSymmetricEigenpairResult):
            raise TypeError("eigenpairs must be RealSymmetricEigenpairResult")
        if type(retained_dimension) is not int:
            raise TypeError("retained_dimension must be a built-in int")
        available = eigenpairs.eigenvalues.magnitude.size
        if retained_dimension <= 0 or retained_dimension > available:
            raise ValueError("retained_dimension must select available eigenpairs")
        return OrthogonalSpectralSubspace(
            eigenvalues=VectorQuantity(
                eigenpairs.eigenvalues.magnitude[:retained_dimension],
                eigenpairs.eigenvalues.unit,
            ),
            basis_vectors=MatrixQuantity(
                eigenpairs.eigenvectors.magnitude[:, :retained_dimension], Unitless()
            ),
        )


@dataclass(frozen=True, slots=True, eq=False)
class OperatorCompressionResult:
    r"""Retain numerical coordinate and ambient forms of one compression.

    Parameters
    ----------
    operator
        Finite real matrix :math:`H` in the ambient represented space.
    subspace
        Orthonormal column embedding :math:`Q` for the retained numerical subspace.
    coordinates
        Retained-coordinate matrix :math:`Q^T H Q`.
    embedded
        Ambient-space matrix :math:`P H P=Q(Q^T H Q)Q^T`, where
        :math:`P=QQ^T`.

    Raises
    ------
    TypeError
        If a member has the wrong represented-data type.
    ValueError
        If the ambient or retained dimensions disagree, or if either result matrix
        uses a unit different from the parent represented operator.

    Notes
    -----
    This is a numerical result for finite real matrices. It does not identify a parent
    scientific model, mathematical state space, retention definition, basis or gauge,
    energy zero, construction provenance, or invariance status. Consequently it is not
    by itself a scientific retained operator. If the subspace is invariant under the
    operator, ``coordinates`` represents the exact restriction of this finite operator;
    otherwise its eigenvalues are Ritz values for a projected compression. Neither
    case is energy-dependent downfolding.

    Direct construction validates intrinsic types, dimensions, and units. The
    :class:`OperatorCompression` Action owns evaluation of the matrix products.
    """

    operator: RealSymmetricOperator
    subspace: OrthogonalSpectralSubspace
    coordinates: MatrixQuantity
    embedded: MatrixQuantity

    def __post_init__(self) -> None:
        """Check member types, dimensions, and parent-operator units."""
        self._check_args_member_types()
        self._check_args_dimensions()
        self._check_args_units()

    def _check_args_member_types(self) -> None:
        """Require represented operator, subspace, and matrix result types."""
        if not isinstance(self.operator, MatrixQuantity | SparseMatrixQuantity):
            raise TypeError("operator must be a dense or sparse matrix quantity")
        if not isinstance(self.subspace, OrthogonalSpectralSubspace):
            raise TypeError("subspace must be OrthogonalSpectralSubspace")
        if not isinstance(self.coordinates, MatrixQuantity):
            raise TypeError("coordinates must be MatrixQuantity")
        if not isinstance(self.embedded, MatrixQuantity):
            raise TypeError("embedded must be MatrixQuantity")

    def _check_args_dimensions(self) -> None:
        """Correlate parent, retained-coordinate, and ambient-space dimensions."""
        retained = self.subspace.retained_dimension
        full = self.subspace.full_dimension
        operator_shape = (
            self.operator.magnitude.shape
            if isinstance(self.operator, MatrixQuantity)
            else self.operator.shape
        )
        if operator_shape != (full, full):
            raise ValueError("operator dimension must match the subspace ambient space")
        if self.coordinates.magnitude.shape != (retained, retained):
            raise ValueError("coordinates must match the retained dimension")
        if self.embedded.magnitude.shape != (full, full):
            raise ValueError("embedded must match the full dimension")

    def _check_args_units(self) -> None:
        """Require both matrix forms to preserve the parent operator unit."""
        if self.coordinates.unit != self.operator.unit:
            raise ValueError("coordinate unit must equal the operator unit")
        if self.embedded.unit != self.operator.unit:
            raise ValueError("embedded unit must equal the operator unit")


class OperatorCompression:
    r"""Compress one represented operator through an orthogonal embedding.

    For an ambient real matrix :math:`H` and an orthonormal column embedding
    :math:`Q`, this Action constructs the retained-coordinate matrix
    :math:`Q^T H Q` and its ambient embedding :math:`P H P`, with
    :math:`P=QQ^T`. It performs finite represented-matrix mechanics only and does not
    assign scientific parentage, invariance, retention, or effective-model meaning.
    """

    __slots__ = ()

    def execute(
        self, operator: RealSymmetricOperator, subspace: OrthogonalSpectralSubspace
    ) -> OperatorCompressionResult:
        r"""Return :math:`Q^T H Q` and :math:`Q(Q^T H Q)Q^T`.

        Parameters
        ----------
        operator
            Dense or sparse finite real operator matrix :math:`H`.
        subspace
            Orthonormal column embedding :math:`Q` with ambient dimension equal to
            the operator dimension.

        Returns
        -------
        OperatorCompressionResult
            Correlated retained-coordinate and ambient-space compression matrices.

        Raises
        ------
        TypeError
            If either input has the wrong represented-data type.
        ValueError
            If the operator and subspace ambient dimensions disagree.
        """
        if not isinstance(operator, MatrixQuantity | SparseMatrixQuantity):
            raise TypeError("operator must be a dense or sparse matrix quantity")
        if not isinstance(subspace, OrthogonalSpectralSubspace):
            raise TypeError("subspace must be OrthogonalSpectralSubspace")
        shape = (
            operator.magnitude.shape
            if isinstance(operator, MatrixQuantity)
            else operator.shape
        )
        if shape != (subspace.full_dimension, subspace.full_dimension):
            raise ValueError("operator and subspace full dimensions must agree")
        vectors = subspace.basis_vectors.magnitude
        dense = (
            operator.magnitude
            if isinstance(operator, MatrixQuantity)
            else operator.to_dense().magnitude
        )
        projector = subspace.projector().magnitude
        coordinates = vectors.T @ dense @ vectors
        embedded = projector @ dense @ projector
        return OperatorCompressionResult(
            operator=operator,
            subspace=subspace,
            coordinates=MatrixQuantity(coordinates, operator.unit),
            embedded=MatrixQuantity(embedded, operator.unit),
        )
