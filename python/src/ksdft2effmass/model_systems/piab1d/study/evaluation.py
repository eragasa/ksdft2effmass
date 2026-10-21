"""Evaluation of the core particle-in-a-box residual study."""

from __future__ import annotations

import numpy as np
from projectkoios.numerics.quadrature.numpy.uniform_1d import (
    NumpyHomogeneousDirichletInteriorQuadrature1D,
    NumpyUniformClosedIntervalTrapezoidalRule,
)
from projectkoios.numerics.quadrature.uniform_1d import (
    UniformClosedIntervalTrapezoidalRuleDefinition,
)
from projectkoios.physkit.qm.piab1d.tise_analytical import (
    Piab1DAnalyticalSolution,
)
from projectkoios.physkit.qm.piab1d.tise_fd import Piab1dTiseFdSolver
from projectkoios.physkit.qm.sampled_states import SampledQuantumState1D
from projectkoios.physkit.units import (
    ComplexVectorQuantity as PhysKitComplexVectorQuantity,
)
from projectkoios.physkit.units import Unitless as PhysKitUnitless
from projectkoios.physkit.units import VectorQuantity as PhysKitVectorQuantity

from ksdft2effmass.analysis.operators import OrthogonalCompressionResidualAnalyzer
from ksdft2effmass.operators import (
    MatrixQuantity,
    OperatorCompression,
    OrthogonalSpectralSubspaceSelector,
    RealSymmetricEigenpairResult,
    ScalarQuantity,
    SparseMatrixQuantity,
    Unitless,
    VectorQuantity,
)

from .records import Piab1dResidualStudyResult, Piab1dStudyDefinition


class Piab1dResidualStudyEvaluator:
    """Evaluate the retained one-dimensional residual experiment."""

    __slots__ = (
        "compression",
        "finite_difference_solver",
        "residual_analyzer",
        "subspace_selector",
    )

    def __init__(
        self, finite_difference_solver: Piab1dTiseFdSolver | None = None
    ) -> None:
        """Construct with the pinned PhysKit PIAB1D finite-difference solver."""
        if finite_difference_solver is not None and not isinstance(
            finite_difference_solver, Piab1dTiseFdSolver
        ):
            raise TypeError(
                "finite_difference_solver must be Piab1dTiseFdSolver or None"
            )
        self.finite_difference_solver = (
            finite_difference_solver or Piab1dTiseFdSolver()
        )
        self.subspace_selector = OrthogonalSpectralSubspaceSelector()
        self.compression = OperatorCompression()
        self.residual_analyzer = OrthogonalCompressionResidualAnalyzer()

    def execute(
        self, definition: Piab1dStudyDefinition
    ) -> Piab1dResidualStudyResult:
        """Return the deterministic finite residual study result."""
        if not isinstance(definition, Piab1dStudyDefinition):
            raise TypeError("definition must be Piab1dStudyDefinition")
        finite_difference = self.finite_difference_solver.solve(
            model=definition.model,
            interior_points=definition.Nx_pts_interior,
        )
        hamiltonian = SparseMatrixQuantity.from_csr(
            finite_difference.hamiltonian.to_csr(),
            Unitless(),
        )
        eigenpairs = RealSymmetricEigenpairResult(
            operator=hamiltonian,
            eigenvalues=VectorQuantity(
                finite_difference.eigenpairs.eigenvalues,
                hamiltonian.unit,
            ),
            eigenvectors=MatrixQuantity(
                finite_difference.eigenpairs.eigenvectors,
                Unitless(),
            ),
        )
        quadrature_rule: NumpyHomogeneousDirichletInteriorQuadrature1D | None = None
        quadrature_vectors: MatrixQuantity | None = None
        if definition.quadrature:
            full_rule = NumpyUniformClosedIntervalTrapezoidalRule().calculate(
                UniformClosedIntervalTrapezoidalRuleDefinition(
                    0.0,
                    definition.model.length,
                    definition.Nx_pts_interior + 2,
                )
            )
            quadrature_rule = full_rule.restrict_homogeneous_dirichlet()
            if quadrature_rule.spacing != finite_difference.grid_spacing.magnitude:
                raise ValueError("quadrature spacing must match the PhysKit grid")
            quadrature_vectors = MatrixQuantity(
                self.normalize_eigenvectors(
                    finite_difference.eigenpairs.eigenvectors,
                    finite_difference.interval.grid.interior_coordinates(),
                    PhysKitVectorQuantity(
                        magnitude=quadrature_rule.interior_weights,
                        unit=finite_difference.grid_spacing.unit,
                    ),
                ),
                Unitless(),
            )
        hamiltonian_dense = hamiltonian.to_dense().magnitude
        eigenvalues = eigenpairs.eigenvalues.magnitude
        eigenvectors = eigenpairs.eigenvectors.magnitude
        retained = definition.N_retained_eigenpairs
        subspace = self.subspace_selector.execute(eigenpairs, retained)
        compression = self.compression.execute(hamiltonian, subspace)
        retained_vectors = subspace.basis_vectors.magnitude
        projector = subspace.projector().magnitude
        complement = np.eye(definition.Nx_pts_interior) - projector
        retained_embedded = compression.embedded.magnitude
        retained_coordinates = compression.coordinates.magnitude
        residuals = self.residual_analyzer.execute(
            hamiltonian, subspace, compression
        )
        consistently_compressed = residuals.consistent.magnitude
        unmatched_compression = residuals.unmatched.magnitude
        discarded_sector = residuals.discarded_sector.magnitude
        cyclic_reference = hamiltonian_dense.copy()
        if definition.Nx_pts_interior > 1:
            cyclic_reference[0, -1] = hamiltonian_dense[0, 1]
            cyclic_reference[-1, 0] = hamiltonian_dense[1, 0]
        boundary_realization = hamiltonian_dense - cyclic_reference
        discrete = finite_difference.closed_form_discrete_energies().magnitude
        continuum = Piab1DAnalyticalSolution(model=definition.model).evaluate(
            count=definition.Nx_pts_interior
        ).energies.magnitude
        expected_retained = np.diag(discrete[:retained])
        identity = np.eye(definition.Nx_pts_interior)
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
                "spectral_leakage_frobenius_norm",
                ScalarQuantity(
                    self.frobenius_norm(
                        complement @ hamiltonian_dense @ retained_vectors
                    ),
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
        return Piab1dResidualStudyResult(
            definition=definition,
            hamiltonian=hamiltonian,
            eigenvalues=eigenpairs.eigenvalues,
            eigenvectors=eigenpairs.eigenvectors,
            quadrature_rule=quadrature_rule,
            quadrature_normalized_eigenvectors=quadrature_vectors,
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
    def normalize_eigenvectors(
        eigenvectors: np.ndarray[tuple[int, int], np.dtype[np.float64]],
        coordinates: PhysKitVectorQuantity,
        quadrature_weights: PhysKitVectorQuantity,
    ) -> np.ndarray[tuple[int, int], np.dtype[np.float64]]:
        """Apply PhysKit's unit-aware sampled-state normalizer by column."""
        normalized_columns: list[np.ndarray[tuple[int], np.dtype[np.float64]]] = []
        for column in range(eigenvectors.shape[1]):
            normalized = SampledQuantumState1D(
                coordinates=coordinates,
                amplitudes=PhysKitComplexVectorQuantity(
                    magnitude=np.asarray(
                        eigenvectors[:, column],
                        dtype=np.complex128,
                    ),
                    unit=PhysKitUnitless(),
                ),
            ).normalize(quadrature_weights=quadrature_weights)
            amplitudes = normalized.normalized_state.amplitudes.magnitude
            if np.any(amplitudes.imag != 0.0):
                raise ValueError("real PIAB1D eigenvectors must remain real")
            normalized_columns.append(np.asarray(amplitudes.real, dtype=np.float64))
        return np.column_stack(normalized_columns)

    @staticmethod
    def frobenius_norm(
        matrix: np.ndarray[tuple[int, ...], np.dtype[np.float64]],
    ) -> float:
        """Return the historical square-sum Frobenius norm evaluation."""
        return float(np.sqrt(np.sum(np.square(matrix))))
