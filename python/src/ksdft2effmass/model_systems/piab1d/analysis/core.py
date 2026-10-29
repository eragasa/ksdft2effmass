"""Complete KSD analysis of one finite PIAB1D solution."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from projectkoios.numerics.quadrature.numpy.uniform_1d import (
    NumpyHomogeneousDirichletInteriorQuadrature1D,
    NumpyUniformClosedIntervalTrapezoidalRule,
)
from projectkoios.numerics.quadrature.uniform_1d import (
    UniformClosedIntervalTrapezoidalRuleDefinition,
)
from projectkoios.physkit.linalg.matrix.norm import MatrixNormEnum
from projectkoios.physkit.qm.piab1d.tise_analytical import Piab1DAnalyticalSolution
from projectkoios.physkit.qm.piab1d.tise_fd import Piab1dTiseFdSolution
from projectkoios.physkit.units import (
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.analysis.diagnostics import (
    BaseDiagnosticAnalyzer,
    DiagnosticObservation,
    MatrixNormDiagnosticOptions,
)
from ksdft2effmass.analysis.operators import (
    RealSymmetricEigenpairDiagnosticAnalyzer,
    RealSymmetricEigenpairDiagnosticRequest,
    RealSymmetricEigenpairDiagnosticResult,
)
from ksdft2effmass.hamiltonian import (
    HermitianHamiltonian,
    OrthogonalHamiltonianBlockAnalyzer,
    OrthogonalHamiltonianBlockRequest,
    OrthogonalHamiltonianBlockResult,
    OrthogonalSpectralSubspace,
    OrthogonalSpectralSubspaceSelectionRequest,
    OrthogonalSpectralSubspaceSelector,
    ReducedHamiltonian,
    SpectralReduction,
)

from ..diagnostics import (
    DiagnosticMethodsEnum,
    DiscreteSpectrumMaximumAbsoluteErrorAnalyzer,
    Piab1dDiagnostics,
    ProjectorIdempotencyAnalyzer,
    ScaledEigenpairResidualAnalyzer,
    SpectralReconstructionErrorAnalyzer,
    WeightedGramErrorAnalyzer,
    WeightedProjectorErrorAnalyzer,
)


@dataclass(frozen=True, slots=True, eq=False)
class Piab1dAnalysis:
    """Retain the complete correlated analysis of one finite PIAB1D solution."""

    solution: Piab1dTiseFdSolution
    reduced_hamiltonian: ReducedHamiltonian
    hamiltonian_blocks: OrthogonalHamiltonianBlockResult
    eigenpair_diagnostics: RealSymmetricEigenpairDiagnosticResult
    discrete_closed_form: VectorQuantity
    continuum_closed_form: VectorQuantity
    quadrature_rule: NumpyHomogeneousDirichletInteriorQuadrature1D
    quadrature_normalized_eigenvectors: MatrixQuantity
    weighted_gram: MatrixQuantity
    weighted_projector: MatrixQuantity
    cyclic_reference: MatrixQuantity
    boundary_realization: MatrixQuantity
    consistent_reduction: MatrixQuantity
    unmatched_reduction: MatrixQuantity
    discarded_sector: MatrixQuantity
    diagnostics: Piab1dDiagnostics

    def __post_init__(self) -> None:
        if not isinstance(self.solution, Piab1dTiseFdSolution):
            raise TypeError("solution must be Piab1dTiseFdSolution")
        if not isinstance(self.reduced_hamiltonian, ReducedHamiltonian):
            raise TypeError("reduced_hamiltonian must be ReducedHamiltonian")
        if not isinstance(
            self.reduced_hamiltonian.spectral_subspace,
            OrthogonalSpectralSubspace,
        ):
            raise TypeError("PIAB1D reduction must use OrthogonalSpectralSubspace")
        if not isinstance(self.hamiltonian_blocks, OrthogonalHamiltonianBlockResult):
            raise TypeError(
                "hamiltonian_blocks must be OrthogonalHamiltonianBlockResult"
            )
        if not isinstance(
            self.eigenpair_diagnostics, RealSymmetricEigenpairDiagnosticResult
        ):
            raise TypeError(
                "eigenpair_diagnostics must be RealSymmetricEigenpairDiagnosticResult"
            )
        if not isinstance(
            self.quadrature_rule,
            NumpyHomogeneousDirichletInteriorQuadrature1D,
        ):
            raise TypeError(
                "quadrature_rule must be NumpyHomogeneousDirichletInteriorQuadrature1D"
            )
        full_dimension = self.solution.interior_points
        full_shape = (full_dimension, full_dimension)
        if not isinstance(self.weighted_gram, MatrixQuantity):
            raise TypeError("weighted_gram must be MatrixQuantity")
        retained_dimension = self.reduced_hamiltonian.spectral_subspace.dimension
        if self.weighted_gram.magnitude.shape != (
            retained_dimension,
            retained_dimension,
        ):
            raise ValueError("weighted_gram must match the retained dimension")
        for name, matrix in (
            (
                "quadrature_normalized_eigenvectors",
                self.quadrature_normalized_eigenvectors,
            ),
            ("weighted_projector", self.weighted_projector),
            ("cyclic_reference", self.cyclic_reference),
            ("boundary_realization", self.boundary_realization),
            ("consistent_reduction", self.consistent_reduction),
            ("unmatched_reduction", self.unmatched_reduction),
            ("discarded_sector", self.discarded_sector),
        ):
            if not isinstance(matrix, MatrixQuantity):
                raise TypeError(f"{name} must be MatrixQuantity")
            if matrix.magnitude.shape != full_shape:
                raise ValueError(f"{name} must match the PIAB1D parent dimension")
        if not isinstance(self.diagnostics, Piab1dDiagnostics):
            raise TypeError("diagnostics must be Piab1dDiagnostics")


class Piab1dAnalyzer:
    """Perform the complete KSD analysis of one PhysKit PIAB1D solution."""

    __slots__ = ()

    def execute(
        self,
        solution: Piab1dTiseFdSolution,
        retained_dimension: int,
    ) -> Piab1dAnalysis:
        """Analyze one finite PhysKit PIAB1D eigensolution.

        Parameters
        ----------
        solution
            Full-grid homogeneous-Dirichlet solution with represented Hamiltonian,
            eigensystem, model, and grid spacing.
        retained_dimension
            Positive number of lowest-energy eigenvectors defining the orthogonal
            retained subspace.

        Returns
        -------
        Piab1dAnalysis
            Correlated reduction, Hamiltonian blocks, analytical references,
            quadrature values, residual matrices, and diagnostic observations.

        Raises
        ------
        TypeError
            ``solution`` or ``retained_dimension`` has the wrong exact type.
        ValueError
            The retained dimension is unavailable or the Hamiltonian and quadrature
            grid conventions disagree.

        Notes
        -----
        The method distinguishes the continuum reference, finite-difference closed
        form, eigensolver residual, boundary realization, and reduction residual.
        These values represent different error sources.
        """
        if not isinstance(solution, Piab1dTiseFdSolution):
            raise TypeError("solution must be Piab1dTiseFdSolution")
        if type(retained_dimension) is not int:
            raise TypeError("retained_dimension must be a built-in int")
        if retained_dimension <= 0 or retained_dimension > solution.interior_points:
            raise ValueError("retained_dimension must select available eigenpairs")

        parent_hamiltonian = HermitianHamiltonian(matrix=solution.hamiltonian)
        subspace = OrthogonalSpectralSubspaceSelector(
            OrthogonalSpectralSubspaceSelectionRequest(
                solution.eigensystem, retained_dimension
            )
        ).execute()
        reduced_hamiltonian = SpectralReduction(
            hamiltonian=parent_hamiltonian,
            spectral_subspace=subspace,
        ).reduced_hamiltonian
        if not isinstance(reduced_hamiltonian.matrix, MatrixQuantity) or not isinstance(
            reduced_hamiltonian.embedded.matrix, MatrixQuantity
        ):
            raise TypeError("PIAB1D reduced Hamiltonian matrices must be real")

        hamiltonian_blocks = OrthogonalHamiltonianBlockAnalyzer(
            OrthogonalHamiltonianBlockRequest(parent_hamiltonian, subspace)
        ).execute()
        if not isinstance(
            hamiltonian_blocks.retained, MatrixQuantity
        ) or not isinstance(hamiltonian_blocks.discarded, MatrixQuantity):
            raise TypeError("PIAB1D Hamiltonian blocks must be real")
        eigenpair_diagnostics = RealSymmetricEigenpairDiagnosticAnalyzer(
            RealSymmetricEigenpairDiagnosticRequest(solution.eigensystem)
        ).execute()

        hamiltonian = solution.hamiltonian.to_dense()
        hamiltonian_values = hamiltonian.magnitude
        eigenvectors = solution.eigenvectors.magnitude
        discrete_closed_form = solution.closed_form_discrete_energies()
        continuum_closed_form = (
            Piab1DAnalyticalSolution(model=solution.model)
            .evaluate(count=solution.interior_points)
            .energies
        )
        embedded = reduced_hamiltonian.embedded.matrix.magnitude
        reconstructed_embedding = (
            subspace.embedding_map.magnitude
            @ reduced_hamiltonian.matrix.magnitude
            @ subspace.reduction_map.magnitude
        )

        cyclic_values = hamiltonian_values.copy()
        if solution.interior_points > 1:
            cyclic_values[0, -1] = hamiltonian_values[0, 1]
            cyclic_values[-1, 0] = hamiltonian_values[1, 0]
        cyclic_reference = MatrixQuantity(cyclic_values, hamiltonian.unit)
        boundary_realization = MatrixQuantity(
            hamiltonian_values - cyclic_values, hamiltonian.unit
        )

        full_quadrature_rule = NumpyUniformClosedIntervalTrapezoidalRule().calculate(
            UniformClosedIntervalTrapezoidalRuleDefinition(
                0.0,
                solution.model.length,
                solution.interior_points + 2,
            )
        )
        quadrature_rule = full_quadrature_rule.restrict_homogeneous_dirichlet()
        if quadrature_rule.spacing != solution.grid_spacing.magnitude:
            raise ValueError("quadrature and Hamiltonian grid spacings must agree")
        quadrature_vectors = MatrixQuantity(
            eigenvectors / np.sqrt(quadrature_rule.spacing),
            Unitless(),
        )
        retained_quadrature_vectors = quadrature_vectors.magnitude[
            :, :retained_dimension
        ]
        weighted_gram = retained_quadrature_vectors.T @ (
            quadrature_rule.interior_weights[:, None] * retained_quadrature_vectors
        )
        weighted_projector = (
            retained_quadrature_vectors
            @ (
                quadrature_rule.interior_weights[:, None] * retained_quadrature_vectors
            ).T
        )
        weighted_gram_quantity = MatrixQuantity(weighted_gram, Unitless())
        weighted_projector_quantity = MatrixQuantity(weighted_projector, Unitless())
        energy_atol = ScalarQuantity(1.0e-12, hamiltonian.unit)
        unitless_atol = ScalarQuantity(1.0e-12, Unitless())
        matrix_norm_options = MatrixNormDiagnosticOptions(
            matrix_norm=MatrixNormEnum.frobenius
        )
        diagnostic_analyzers: set[BaseDiagnosticAnalyzer[DiagnosticMethodsEnum]] = {
            DiscreteSpectrumMaximumAbsoluteErrorAnalyzer(
                computed=solution.energies,
                reference=discrete_closed_form,
                atol=energy_atol,
                rtol=0.0,
            ),
            ScaledEigenpairResidualAnalyzer(
                residuals=eigenpair_diagnostics.scaled_column_residuals,
                atol=unitless_atol,
                rtol=0.0,
            ),
            SpectralReconstructionErrorAnalyzer(
                hamiltonian=hamiltonian,
                eigenvalues=solution.energies,
                eigenvectors=solution.eigenvectors,
                atol=energy_atol,
                rtol=0.0,
                options=matrix_norm_options,
            ),
            ProjectorIdempotencyAnalyzer(
                projector=subspace.projector,
                atol=unitless_atol,
                rtol=0.0,
                options=matrix_norm_options,
            ),
            WeightedGramErrorAnalyzer(
                weighted_gram=weighted_gram_quantity,
                atol=unitless_atol,
                rtol=0.0,
                options=matrix_norm_options,
            ),
            WeightedProjectorErrorAnalyzer(
                weighted_projector=weighted_projector_quantity,
                projector=subspace.projector,
                atol=unitless_atol,
                rtol=0.0,
                options=matrix_norm_options,
            ),
        }
        diagnostic_observations: dict[DiagnosticMethodsEnum, DiagnosticObservation] = {}
        for diagnostic_analyzer in diagnostic_analyzers:
            if diagnostic_analyzer.method in diagnostic_observations:
                raise ValueError("diagnostic analyzer methods must be unique")
            diagnostic_observations[diagnostic_analyzer.method] = (
                diagnostic_analyzer.result()
            )

        return Piab1dAnalysis(
            solution=solution,
            reduced_hamiltonian=reduced_hamiltonian,
            hamiltonian_blocks=hamiltonian_blocks,
            eigenpair_diagnostics=eigenpair_diagnostics,
            discrete_closed_form=discrete_closed_form,
            continuum_closed_form=continuum_closed_form,
            quadrature_rule=quadrature_rule,
            quadrature_normalized_eigenvectors=quadrature_vectors,
            weighted_gram=weighted_gram_quantity,
            weighted_projector=weighted_projector_quantity,
            cyclic_reference=cyclic_reference,
            boundary_realization=boundary_realization,
            consistent_reduction=MatrixQuantity(
                embedded - reconstructed_embedding,
                hamiltonian.unit,
            ),
            unmatched_reduction=MatrixQuantity(
                embedded - hamiltonian_values,
                hamiltonian.unit,
            ),
            discarded_sector=MatrixQuantity(
                -hamiltonian_blocks.discarded.magnitude,
                hamiltonian.unit,
            ),
            diagnostics=Piab1dDiagnostics(diagnostic_observations),
        )
