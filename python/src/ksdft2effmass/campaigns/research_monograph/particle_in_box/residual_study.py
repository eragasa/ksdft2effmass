"""Evaluation of the core particle-in-a-box residual study."""

from __future__ import annotations

import numpy as np

from ksdft2effmass.analysis.model_systems import (
    ParticleInBoxGridEvaluator,
    ParticleInBoxParameters,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.operators import (
    MatrixQuantity,
    OperatorCompression,
    OrthogonalSpectralSubspaceSelector,
    RealSymmetricEigenpairSolver,
    SparseMatrixQuantity,
)

from .records import ParticleInBoxResidualStudyResult, ParticleInBoxStudyDefinition


class ParticleInBoxResidualStudyEvaluator:
    """Evaluate the retained one-dimensional residual experiment."""

    __slots__ = ("compression", "grid_evaluator", "subspace_selector")

    def __init__(self, eigenpair_solver: RealSymmetricEigenpairSolver | None = None):
        """Construct with an explicit or default sparse-capable eigensolver."""
        if eigenpair_solver is not None and not isinstance(
            eigenpair_solver, RealSymmetricEigenpairSolver
        ):
            raise TypeError(
                "eigenpair_solver must be RealSymmetricEigenpairSolver or None"
            )
        self.grid_evaluator = ParticleInBoxGridEvaluator(eigenpair_solver)
        self.subspace_selector = OrthogonalSpectralSubspaceSelector()
        self.compression = OperatorCompression()

    def execute(
        self, definition: ParticleInBoxStudyDefinition
    ) -> ParticleInBoxResidualStudyResult:
        """Return the deterministic finite residual study result."""
        if not isinstance(definition, ParticleInBoxStudyDefinition):
            raise TypeError("definition must be ParticleInBoxStudyDefinition")
        parameters = ParticleInBoxParameters(
            length=ScalarQuantity(definition.length, Unitless()),
            mass=ScalarQuantity(definition.mass, Unitless()),
            hbar=ScalarQuantity(definition.hbar, Unitless()),
        )
        evaluation = self.grid_evaluator.execute(parameters, definition.interior_points)
        analytical = evaluation.analytical
        finite_difference = evaluation.finite_difference
        eigenpairs = evaluation.eigenpairs
        if not isinstance(eigenpairs.operator, SparseMatrixQuantity):
            raise TypeError("grid evaluation must retain a sparse Hamiltonian")
        hamiltonian = eigenpairs.operator
        hamiltonian_dense = hamiltonian.to_dense().magnitude
        eigenvalues = eigenpairs.eigenvalues.magnitude
        eigenvectors = eigenpairs.eigenvectors.magnitude
        retained = definition.retained_dimension
        subspace = self.subspace_selector.execute(eigenpairs, retained)
        compression = self.compression.execute(hamiltonian, subspace)
        retained_vectors = subspace.basis_vectors.magnitude
        projector = subspace.projector().magnitude
        complement = np.eye(definition.interior_points) - projector
        retained_embedded = compression.embedded.magnitude
        retained_kinetic = projector @ hamiltonian_dense.copy() @ projector
        retained_coordinates = compression.coordinates.magnitude
        consistently_compressed = retained_embedded - retained_kinetic
        unmatched_compression = retained_embedded - hamiltonian_dense
        discarded_sector = -(complement @ hamiltonian_dense @ complement)
        cyclic_reference = hamiltonian_dense.copy()
        if definition.interior_points > 1:
            cyclic_reference[0, -1] = hamiltonian_dense[0, 1]
            cyclic_reference[-1, 0] = hamiltonian_dense[1, 0]
        boundary_realization = hamiltonian_dense - cyclic_reference
        discrete = finite_difference.discrete_energy_levels().magnitude
        continuum = analytical.energy_levels(definition.interior_points).magnitude
        expected_retained = np.diag(discrete[:retained])
        identity = np.eye(definition.interior_points)
        diagnostics = (
            (
                "discrete_spectrum_maximum_absolute_error",
                ScalarQuantity(
                    float(np.max(np.abs(eigenvalues - discrete))), hamiltonian.unit
                ),
            ),
            (
                "spectral_reconstruction_frobenius_error",
                ScalarQuantity(
                    self.frobenius_norm(
                        hamiltonian_dense
                        - eigenvectors @ np.diag(eigenvalues) @ eigenvectors.T
                    ),
                    hamiltonian.unit,
                ),
            ),
            (
                "projector_idempotency_frobenius_error",
                ScalarQuantity(
                    self.frobenius_norm(projector @ projector - projector), Unitless()
                ),
            ),
            (
                "projector_complement_frobenius_error",
                ScalarQuantity(
                    self.frobenius_norm(projector + complement - identity), Unitless()
                ),
            ),
            (
                "retained_embedding_frobenius_error",
                ScalarQuantity(
                    self.frobenius_norm(
                        retained_embedded
                        - retained_vectors @ retained_coordinates @ retained_vectors.T
                    ),
                    hamiltonian.unit,
                ),
            ),
            (
                "retained_coordinate_frobenius_error",
                ScalarQuantity(
                    self.frobenius_norm(retained_coordinates - expected_retained),
                    hamiltonian.unit,
                ),
            ),
            (
                "consistently_compressed_residual_frobenius_norm",
                ScalarQuantity(
                    self.frobenius_norm(consistently_compressed), hamiltonian.unit
                ),
            ),
            (
                "unmatched_equals_discarded_frobenius_error",
                ScalarQuantity(
                    self.frobenius_norm(unmatched_compression - discarded_sector),
                    hamiltonian.unit,
                ),
            ),
            (
                "unmatched_compression_frobenius_norm",
                ScalarQuantity(
                    self.frobenius_norm(unmatched_compression), hamiltonian.unit
                ),
            ),
            (
                "boundary_realization_frobenius_norm",
                ScalarQuantity(
                    self.frobenius_norm(boundary_realization), hamiltonian.unit
                ),
            ),
        )
        return ParticleInBoxResidualStudyResult(
            definition=definition,
            hamiltonian=hamiltonian,
            eigenvalues=eigenpairs.eigenvalues,
            eigenvectors=eigenpairs.eigenvectors,
            retained_vectors=MatrixQuantity(retained_vectors, Unitless()),
            projector=MatrixQuantity(projector, Unitless()),
            retained_embedded=MatrixQuantity(retained_embedded, hamiltonian.unit),
            retained_coordinates=MatrixQuantity(retained_coordinates, hamiltonian.unit),
            cyclic_reference=MatrixQuantity(cyclic_reference, hamiltonian.unit),
            consistently_compressed=MatrixQuantity(
                consistently_compressed, hamiltonian.unit
            ),
            unmatched_compression=MatrixQuantity(
                unmatched_compression, hamiltonian.unit
            ),
            discarded_sector=MatrixQuantity(discarded_sector, hamiltonian.unit),
            boundary_realization=MatrixQuantity(boundary_realization, hamiltonian.unit),
            discrete_closed_form=VectorQuantity(discrete, hamiltonian.unit),
            continuum_closed_form=VectorQuantity(continuum, hamiltonian.unit),
            diagnostics=diagnostics,
        )

    @staticmethod
    def frobenius_norm(
        matrix: np.ndarray[tuple[int, ...], np.dtype[np.float64]],
    ) -> float:
        """Return the historical square-sum Frobenius norm evaluation."""
        return float(np.sqrt(np.sum(np.square(matrix))))
