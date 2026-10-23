"""Immutable records for PIAB1D studies."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from projectkoios.numerics.quadrature.numpy.uniform_1d import (
    NumpyHomogeneousDirichletInteriorQuadrature1D,
)
from projectkoios.physkit.qm.piab1d import Piab1D

from ksdft2effmass.linalg import (
    CsrRealMatrixQuantity,
    RealMatrixQuantity,
    ScalarQuantity,
    VectorQuantity,
)
from ksdft2effmass.model_systems.study import (
    ModelId,
    ModelSystemStudyBase,
    ModelSystemStudyIdentity,
    ModelSystemStudySchemaId,
)
from ksdft2effmass.operators import (
    OrthogonalSpectralSubspace,
    ReducedHamiltonian,
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
                "N_retained_eigenpairs must be positive and not exceed Nx_pts_interior"
            )
        if type(self.quadrature) is not bool:
            raise TypeError("quadrature must be a built-in bool")

    def study_identity(self) -> ModelSystemStudyIdentity:
        """Return the fixed model and schema identity."""
        return ModelSystemStudyIdentity(self.model_id, self.schema_id)


@dataclass(frozen=True, slots=True, eq=False)
class Piab1dResidualStudyResult:
    r"""Retain represented matrices, spectra, residuals, and scalar diagnostics.

    Attributes
    ----------
    reduced_hamiltonian
        The complete reduced representation. Its ``spectral_subspace.basis_vectors``
        is :math:`\Phi_M`; the subspace derives
        :math:`P_M=\Phi_M\Phi_M^{\mathsf T}` when requested. Its inherited ``matrix``
        is :math:`\Phi_M^{\mathsf T}H\Phi_M`, and ``embedded.matrix`` is
        :math:`\Phi_M(\Phi_M^{\mathsf T}H\Phi_M)\Phi_M^{\mathsf T}`. For the maintained
        core calculation, their shapes are 8 by 3, 8 by 8, 3 by 3, and 8 by 8,
        respectively.
    """

    definition: Piab1dStudyDefinition
    hamiltonian: CsrRealMatrixQuantity
    eigenvalues: VectorQuantity
    eigenvectors: RealMatrixQuantity
    quadrature_rule: NumpyHomogeneousDirichletInteriorQuadrature1D | None
    quadrature_normalized_eigenvectors: RealMatrixQuantity | None
    reduced_hamiltonian: ReducedHamiltonian
    cyclic_reference: RealMatrixQuantity
    consistently_compressed: RealMatrixQuantity
    unmatched_compression: RealMatrixQuantity
    discarded_sector: RealMatrixQuantity
    boundary_realization: RealMatrixQuantity
    discrete_closed_form: VectorQuantity
    continuum_closed_form: VectorQuantity
    diagnostics: tuple[tuple[str, ScalarQuantity], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.definition, Piab1dStudyDefinition):
            raise TypeError("definition must be Piab1dStudyDefinition")
        if not isinstance(self.hamiltonian, CsrRealMatrixQuantity):
            raise TypeError("hamiltonian must be CsrRealMatrixQuantity")
        if not isinstance(self.eigenvalues, VectorQuantity):
            raise TypeError("eigenvalues must be VectorQuantity")
        if not isinstance(self.eigenvectors, RealMatrixQuantity):
            raise TypeError("eigenvectors must be RealMatrixQuantity")
        if self.definition.quadrature:
            if not isinstance(
                self.quadrature_rule,
                NumpyHomogeneousDirichletInteriorQuadrature1D,
            ):
                raise TypeError("quadrature_rule must retain the enabled interior rule")
            if not isinstance(
                self.quadrature_normalized_eigenvectors,
                RealMatrixQuantity,
            ):
                raise TypeError(
                    "quadrature_normalized_eigenvectors must be RealMatrixQuantity"
                )
        elif self.quadrature_rule is not None or (
            self.quadrature_normalized_eigenvectors is not None
        ):
            raise ValueError("disabled quadrature must not retain quadrature results")
        if not isinstance(self.reduced_hamiltonian, ReducedHamiltonian):
            raise TypeError("reduced_hamiltonian must be ReducedHamiltonian")
        for quantity in (
            self.cyclic_reference,
            self.consistently_compressed,
            self.unmatched_compression,
            self.discarded_sector,
            self.boundary_realization,
        ):
            if not isinstance(quantity, RealMatrixQuantity):
                raise TypeError(
                    "represented result matrices must be RealMatrixQuantity"
                )
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
            weighted_gram = quadrature_vectors.magnitude.T @ (
                weights[:, None] * quadrature_vectors.magnitude
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
        reduction = self.reduced_hamiltonian
        reduced_matrix = reduction.matrix
        embedded_matrix = reduction.embedded.matrix
        if not isinstance(reduced_matrix, RealMatrixQuantity) or not isinstance(
            embedded_matrix, RealMatrixQuantity
        ):
            raise TypeError("PIAB1D reduced Hamiltonian matrices must be real")
        subspace = reduction.spectral_subspace
        if not isinstance(subspace, OrthogonalSpectralSubspace):
            raise TypeError(
                "PIAB1D reduced Hamiltonian requires OrthogonalSpectralSubspace"
            )
        if subspace.basis_vectors.magnitude.shape != (
            full_dimension,
            retained_dimension,
        ):
            raise ValueError("spectral subspace must map reduced to full coordinates")
        for name, quantity in (
            ("projector", subspace.projector()),
            ("embedded", embedded_matrix),
            ("cyclic_reference", self.cyclic_reference),
            ("consistently_compressed", self.consistently_compressed),
            ("unmatched_compression", self.unmatched_compression),
            ("discarded_sector", self.discarded_sector),
            ("boundary_realization", self.boundary_realization),
        ):
            if quantity.magnitude.shape != full_shape:
                raise ValueError(f"{name} shape must match the full state space")
        if reduced_matrix.magnitude.shape != retained_shape:
            raise ValueError("reduced matrix must match the reduced state space")
        for name, vector_quantity in (
            ("discrete_closed_form", self.discrete_closed_form),
            ("continuum_closed_form", self.continuum_closed_form),
        ):
            if vector_quantity.magnitude.shape != (full_dimension,):
                raise ValueError(f"{name} must span the full state space")
        diagnostic_names = tuple(name for name, _ in self.diagnostics)
        if len(set(diagnostic_names)) != len(diagnostic_names):
            raise ValueError("diagnostic names must be unique")
