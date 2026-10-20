"""Reusable evaluation of one finite particle-in-a-box discretization.

The evaluator constructs a homogeneous-Dirichlet interval with ``N`` interior
coordinates, assembles the sparse centered-difference Hamiltonian, and requests its
complete real-symmetric eigensystem. The retained result binds the continuum model,
finite representation, represented operator, and eigenpairs without assigning
campaign-specific acceptance criteria.
"""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.operators import (
    PhysicalUnit,
    RealSymmetricEigenpairResult,
    RealSymmetricEigenpairSolver,
    ScalarQuantity,
    SparseMatrixQuantity,
    Unitless,
)

from ..boundary_conditions import DirichletBoundaryCondition
from ..cartesian_grids import UniformCartesianGrid1D
from ..intervals import DirichletInterval
from .model import (
    Piab1dAnalytical,
    Piab1dFiniteDifference,
    Piab1dParameters,
)


@dataclass(frozen=True, slots=True)
class Piab1dGridEvaluation:
    """Retain one model definition, finite representation, and complete eigensystem.

    Parameters
    ----------
    analytical
        Continuum homogeneous-Dirichlet box model.
    finite_difference
        Finite representation using the same analytical model.
    eigenpairs
        Complete ascending real-symmetric eigensystem of the represented sparse
        Hamiltonian.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type or the eigensystem does not retain a
        sparse represented operator.
    ValueError
        If the models disagree or the eigensystem shape does not match the finite
        coordinate-space dimension.
    """

    analytical: Piab1dAnalytical
    finite_difference: Piab1dFiniteDifference
    eigenpairs: RealSymmetricEigenpairResult

    def __post_init__(self) -> None:
        if not isinstance(self.analytical, Piab1dAnalytical):
            raise TypeError("analytical must be Piab1dAnalytical")
        if not isinstance(self.finite_difference, Piab1dFiniteDifference):
            raise TypeError("finite_difference must be Piab1dFiniteDifference")
        if not isinstance(self.eigenpairs, RealSymmetricEigenpairResult):
            raise TypeError("eigenpairs must be RealSymmetricEigenpairResult")
        if self.finite_difference.analytical != self.analytical:
            raise ValueError("finite_difference must use the retained analytical model")
        if not isinstance(self.eigenpairs.operator, SparseMatrixQuantity):
            raise TypeError("eigenpairs operator must be SparseMatrixQuantity")
        expected_shape = (self.finite_difference.interior_points,) * 2
        if self.eigenpairs.operator.shape != expected_shape:
            raise ValueError(
                "eigenpairs must match the finite representation dimension"
            )

    @property
    def interior_points(self) -> int:
        """Return the finite full-space dimension."""
        return self.finite_difference.interior_points


class Piab1dGridEvaluator:
    """Construct and solve one homogeneous-Dirichlet finite box representation.

    Parameters
    ----------
    eigenpair_solver
        Optional explicit ``RealSymmetricEigenpairSolver``. ``None`` constructs the
        supported default solver, which uses the represented tridiagonal structure.

    Notes
    -----
    The evaluator selects no convergence sequence, retained subspace, residual norm,
    or scientific acceptance threshold. Those policies belong to campaign owners.
    Physical parameter records use coordinate units for the grid and inverse-square-
    root-length units for the homogeneous wavefunction boundary value.
    """

    __slots__ = ("eigenpair_solver",)

    def __init__(self, eigenpair_solver: RealSymmetricEigenpairSolver | None = None):
        """Construct with an explicit or default sparse-capable eigensolver."""
        if eigenpair_solver is not None and not isinstance(
            eigenpair_solver, RealSymmetricEigenpairSolver
        ):
            raise TypeError(
                "eigenpair_solver must be RealSymmetricEigenpairSolver or None"
            )
        self.eigenpair_solver = eigenpair_solver or RealSymmetricEigenpairSolver()

    def execute(
        self, parameters: Piab1dParameters, interior_points: int
    ) -> Piab1dGridEvaluation:
        """Return one complete sparse-Hamiltonian grid evaluation.

        Parameters
        ----------
        parameters
            Positive physical or explicitly nondimensional particle-in-a-box
            parameters.
        interior_points
            Positive built-in integer dimension of the interior coordinate space.

        Returns
        -------
        Piab1dGridEvaluation
            Immutable continuum model, finite representation, and complete ascending
            eigensystem.

        Raises
        ------
        TypeError
            If ``parameters`` or ``interior_points`` has the wrong semantic type;
            booleans are rejected as integers.
        ValueError
            If ``interior_points`` is not positive or a composed interval/model
            invariant is violated.
        """
        if not isinstance(parameters, Piab1dParameters):
            raise TypeError("parameters must be Piab1dParameters")
        if type(interior_points) is not int:
            raise TypeError("interior_points must be a built-in int")
        if interior_points <= 0:
            raise ValueError("interior_points must be positive")
        spacing = parameters.length.magnitude / (interior_points + 1)
        field_unit: PhysicalUnit | Unitless
        if parameters.is_nondimensional:
            field_unit = Unitless()
        else:
            field_unit = PhysicalUnit("meter ** -0.5")
        analytical = Piab1dAnalytical(parameters)
        interval = DirichletInterval(
            UniformCartesianGrid1D(
                ScalarQuantity(0.0, parameters.length.unit),
                parameters.length,
                ScalarQuantity(spacing, parameters.length.unit),
            ),
            DirichletBoundaryCondition(ScalarQuantity(0.0, field_unit)),
        )
        finite_difference = Piab1dFiniteDifference(analytical, interval)
        hamiltonian = finite_difference.hamiltonian()
        eigenpairs = self.eigenpair_solver.execute(hamiltonian)
        return Piab1dGridEvaluation(
            analytical=analytical,
            finite_difference=finite_difference,
            eigenpairs=eigenpairs,
        )
