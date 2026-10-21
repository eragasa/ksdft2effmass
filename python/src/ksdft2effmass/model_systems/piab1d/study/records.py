"""Immutable records for PIAB1D studies."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from projectkoios.numerics.quadrature.numpy.uniform_1d import (
    NumpyHomogeneousDirichletInteriorQuadrature1D,
)
from projectkoios.physkit.qm.piab1d import Piab1D

from ksdft2effmass.model_systems.study import (
    ModelId,
    ModelSystemStudyBase,
    ModelSystemStudyIdentity,
    ModelSystemStudySchemaId,
)
from ksdft2effmass.operators import (
    MatrixQuantity,
    ScalarQuantity,
    SparseMatrixQuantity,
    VectorQuantity,
)


@dataclass(frozen=True, slots=True)
class Piab1dStudyDefinition(ModelSystemStudyBase):
    """Define one finite PIAB1D spectral-reduction study."""

    model: Piab1D
    Nx_pts_interior: int
    N_retained_eigenpairs: int
    quadrature: bool = True
    model_id: ModelId = field(default=ModelId.piab1d, init=False)
    schema_id: ModelSystemStudySchemaId = field(
        default=ModelSystemStudySchemaId.piab1d_v2,
        init=False,
    )

    def __post_init__(self) -> None:
        if not isinstance(self.model, Piab1D):
            raise TypeError("model must be Piab1D")
        if type(self.Nx_pts_interior) is not int:
            raise TypeError("Nx_pts_interior must be a built-in int")
        if self.Nx_pts_interior <= 0:
            raise ValueError("Nx_pts_interior must be positive")
        if type(self.N_retained_eigenpairs) is not int:
            raise TypeError("N_retained_eigenpairs must be a built-in int")
        if not 0 < self.N_retained_eigenpairs <= self.Nx_pts_interior:
            raise ValueError(
                "N_retained_eigenpairs must be positive and not exceed "
                "Nx_pts_interior"
            )
        if type(self.quadrature) is not bool:
            raise TypeError("quadrature must be a built-in bool")

    def study_identity(self) -> ModelSystemStudyIdentity:
        """Return the fixed model and schema identity."""
        return ModelSystemStudyIdentity(self.model_id, self.schema_id)


@dataclass(frozen=True, slots=True, eq=False)
class Piab1dResidualStudyResult:
    """Retain represented matrices, spectra, residuals, and scalar diagnostics."""

    definition: Piab1dStudyDefinition
    hamiltonian: SparseMatrixQuantity
    eigenvalues: VectorQuantity
    eigenvectors: MatrixQuantity
    quadrature_rule: NumpyHomogeneousDirichletInteriorQuadrature1D | None
    quadrature_normalized_eigenvectors: MatrixQuantity | None
    retained_vectors: MatrixQuantity
    projector: MatrixQuantity
    retained_embedded: MatrixQuantity
    retained_coordinates: MatrixQuantity
    cyclic_reference: MatrixQuantity
    consistently_compressed: MatrixQuantity
    unmatched_compression: MatrixQuantity
    discarded_sector: MatrixQuantity
    boundary_realization: MatrixQuantity
    discrete_closed_form: VectorQuantity
    continuum_closed_form: VectorQuantity
    diagnostics: tuple[tuple[str, ScalarQuantity], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.definition, Piab1dStudyDefinition):
            raise TypeError("definition must be Piab1dStudyDefinition")
        if not isinstance(self.hamiltonian, SparseMatrixQuantity):
            raise TypeError("hamiltonian must be SparseMatrixQuantity")
        if not isinstance(self.eigenvalues, VectorQuantity):
            raise TypeError("eigenvalues must be VectorQuantity")
        if not isinstance(self.eigenvectors, MatrixQuantity):
            raise TypeError("eigenvectors must be MatrixQuantity")
        if self.definition.quadrature:
            if not isinstance(
                self.quadrature_rule,
                NumpyHomogeneousDirichletInteriorQuadrature1D,
            ):
                raise TypeError(
                    "quadrature_rule must retain the enabled interior rule"
                )
            if not isinstance(
                self.quadrature_normalized_eigenvectors,
                MatrixQuantity,
            ):
                raise TypeError(
                    "quadrature_normalized_eigenvectors must be MatrixQuantity"
                )
        elif self.quadrature_rule is not None or (
            self.quadrature_normalized_eigenvectors is not None
        ):
            raise ValueError("disabled quadrature must not retain quadrature results")
        for quantity in (
            self.retained_vectors,
            self.projector,
            self.retained_embedded,
            self.retained_coordinates,
            self.cyclic_reference,
            self.consistently_compressed,
            self.unmatched_compression,
            self.discarded_sector,
            self.boundary_realization,
        ):
            if not isinstance(quantity, MatrixQuantity):
                raise TypeError("represented result matrices must be MatrixQuantity")
        if not isinstance(self.discrete_closed_form, VectorQuantity):
            raise TypeError("discrete_closed_form must be VectorQuantity")
        if not isinstance(self.continuum_closed_form, VectorQuantity):
            raise TypeError("continuum_closed_form must be VectorQuantity")
        if not isinstance(self.diagnostics, tuple) or not all(
            isinstance(item, tuple)
            and len(item) == 2
            and type(item[0]) is str
            and isinstance(item[1], ScalarQuantity)
            for item in self.diagnostics
        ):
            raise TypeError("diagnostics must be immutable named scalar quantities")
        full_dimension = self.definition.Nx_pts_interior
        retained_dimension = self.definition.N_retained_eigenpairs
        full_shape = (full_dimension, full_dimension)
        retained_shape = (retained_dimension, retained_dimension)
        if self.hamiltonian.shape != full_shape:
            raise ValueError("hamiltonian shape must match the full state space")
        if self.eigenvalues.magnitude.shape != (full_dimension,):
            raise ValueError("eigenvalues must span the full state space")
        if self.eigenvectors.magnitude.shape != full_shape:
            raise ValueError("eigenvectors must span the full state space")
        if self.quadrature_rule is not None:
            if self.quadrature_rule.interval != (0.0, self.definition.model.length):
                raise ValueError("quadrature interval must match the PIAB1D model")
            if self.quadrature_rule.point_count != full_dimension + 2:
                raise ValueError(
                    "quadrature point count must include both Dirichlet endpoints"
                )
            quadrature_vectors = self.quadrature_normalized_eigenvectors
            if quadrature_vectors is None:
                raise RuntimeError("enabled quadrature vectors must be retained")
            if quadrature_vectors.magnitude.shape != full_shape:
                raise ValueError(
                    "quadrature_normalized_eigenvectors must span the full state space"
                )
            weights = self.quadrature_rule.interior_weights
            expected_vectors = self.eigenvectors.magnitude / np.sqrt(weights[:, None])
            tolerance = 256.0 * np.finfo(np.float64).eps
            if not np.allclose(
                quadrature_vectors.magnitude,
                expected_vectors,
                rtol=tolerance,
                atol=tolerance,
            ):
                raise ValueError(
                    "quadrature-normalized eigenvectors must rescale solver vectors"
                )
            weighted_gram = (
                quadrature_vectors.magnitude.T
                @ (weights[:, None] * quadrature_vectors.magnitude)
            )
            if not np.allclose(
                weighted_gram,
                np.eye(full_dimension),
                rtol=tolerance,
                atol=tolerance,
            ):
                raise ValueError(
                    "quadrature-normalized eigenvectors must have unit weighted Gram"
                )
        if self.retained_vectors.magnitude.shape != (
            full_dimension,
            retained_dimension,
        ):
            raise ValueError("retained_vectors must map retained to full coordinates")
        for name, quantity in (
            ("projector", self.projector),
            ("retained_embedded", self.retained_embedded),
            ("cyclic_reference", self.cyclic_reference),
            ("consistently_compressed", self.consistently_compressed),
            ("unmatched_compression", self.unmatched_compression),
            ("discarded_sector", self.discarded_sector),
            ("boundary_realization", self.boundary_realization),
        ):
            if quantity.magnitude.shape != full_shape:
                raise ValueError(f"{name} shape must match the full state space")
        if self.retained_coordinates.magnitude.shape != retained_shape:
            raise ValueError(
                "retained_coordinates shape must match the retained state space"
            )
        for name, vector_quantity in (
            ("discrete_closed_form", self.discrete_closed_form),
            ("continuum_closed_form", self.continuum_closed_form),
        ):
            if vector_quantity.magnitude.shape != (full_dimension,):
                raise ValueError(f"{name} must span the full state space")
        diagnostic_names = tuple(name for name, _ in self.diagnostics)
        if len(set(diagnostic_names)) != len(diagnostic_names):
            raise ValueError("diagnostic names must be unique")
