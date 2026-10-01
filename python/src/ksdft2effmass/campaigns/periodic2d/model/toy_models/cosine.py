"""Dimensionless two-dimensional cosine-potential toy Hamiltonians."""

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

type ComplexMatrix = npt.NDArray[np.complex128]


@dataclass(frozen=True, slots=True)
class Periodic2DCosinePotentialToyModel:
    """Represent a spinless dimensionless periodic cosine potential.

    The represented potential is
    ``lambda_x*cos(x) + lambda_y*cos(y) + lambda_xy*cos(x)*cos(y)`` on a
    square cell of period ``2*pi``. Energies use the reciprocal kinetic scale.
    """

    lambda_x: float
    lambda_y: float
    lambda_xy: float

    def __post_init__(self) -> None:
        """Require exact finite floating-point coupling coefficients."""
        for name, value in (
            ("lambda_x", self.lambda_x),
            ("lambda_y", self.lambda_y),
            ("lambda_xy", self.lambda_xy),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a float")
            if not np.isfinite(value):
                raise ValueError(f"{name} must be finite")


@dataclass(frozen=True, slots=True)
class Periodic2DPlaneWaveHamiltonianRequest:
    """Request a finite plane-wave representation of the toy Hamiltonian."""

    model: Periodic2DCosinePotentialToyModel
    reduced_momentum_x: float | np.float64
    reduced_momentum_y: float | np.float64
    cutoff: int

    def __post_init__(self) -> None:
        """Validate the model, momentum coordinates, and symmetric cutoff."""
        if type(self.model) is not Periodic2DCosinePotentialToyModel:
            raise TypeError("model must be Periodic2DCosinePotentialToyModel")
        for name, value in (
            ("reduced_momentum_x", self.reduced_momentum_x),
            ("reduced_momentum_y", self.reduced_momentum_y),
        ):
            if type(value) not in (float, np.float64):
                raise TypeError(f"{name} must be a float or numpy.float64")
            if not np.isfinite(value):
                raise ValueError(f"{name} must be finite")
            object.__setattr__(self, name, float(value))
        if isinstance(self.cutoff, bool) or not isinstance(self.cutoff, int):
            raise TypeError("cutoff must be an integer")
        if self.cutoff < 0:
            raise ValueError("cutoff must be nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic2DFiniteDifferenceHamiltonianRequest:
    """Request a centered finite-difference representation on the square cell."""

    model: Periodic2DCosinePotentialToyModel
    reduced_momentum_x: float | np.float64
    reduced_momentum_y: float | np.float64
    points_per_direction: int

    def __post_init__(self) -> None:
        """Validate the model, momentum coordinates, and odd grid size."""
        if type(self.model) is not Periodic2DCosinePotentialToyModel:
            raise TypeError("model must be Periodic2DCosinePotentialToyModel")
        for name, value in (
            ("reduced_momentum_x", self.reduced_momentum_x),
            ("reduced_momentum_y", self.reduced_momentum_y),
        ):
            if type(value) not in (float, np.float64):
                raise TypeError(f"{name} must be a float or numpy.float64")
            if not np.isfinite(value):
                raise ValueError(f"{name} must be finite")
            object.__setattr__(self, name, float(value))
        if isinstance(self.points_per_direction, bool) or not isinstance(
            self.points_per_direction, int
        ):
            raise TypeError("points_per_direction must be an integer")
        if self.points_per_direction < 5 or self.points_per_direction % 2 == 0:
            raise ValueError("points_per_direction must be odd and at least five")


@dataclass(frozen=True, slots=True)
class Periodic2DHamiltonianResult:
    """Retain one operationally immutable finite represented Hamiltonian."""

    matrix: ComplexMatrix

    def __post_init__(self) -> None:
        """Copy one finite square Hermitian matrix into immutable storage."""
        matrix = np.asarray(self.matrix, dtype=np.complex128)
        if (
            matrix.ndim != 2
            or matrix.shape[0] == 0
            or matrix.shape[0] != matrix.shape[1]
        ):
            raise ValueError("matrix must be nonempty and square")
        if not np.all(np.isfinite(matrix)):
            raise ValueError("matrix must contain only finite values")
        if not np.array_equal(matrix, matrix.conj().T):
            raise ValueError("matrix must be exactly Hermitian")
        immutable = np.frombuffer(
            matrix.tobytes(order="C"), dtype=np.complex128
        ).reshape(matrix.shape)
        object.__setattr__(self, "matrix", immutable)


class Periodic2DPlaneWaveHamiltonianConstructor:
    """Construct finite plane-wave matrices in ``p``-outer, ``q``-inner order."""

    __slots__ = ()

    def execute(
        self, request: Periodic2DPlaneWaveHamiltonianRequest
    ) -> Periodic2DHamiltonianResult:
        """Construct kinetic and cosine Fourier blocks without implicit truncation."""
        model = request.model
        cutoff = request.cutoff
        pairs = tuple(
            (p, q)
            for p in range(-cutoff, cutoff + 1)
            for q in range(-cutoff, cutoff + 1)
        )
        lookup = {pair: index for index, pair in enumerate(pairs)}
        matrix = np.zeros((len(pairs), len(pairs)), dtype=np.complex128)
        for index, (p, q) in enumerate(pairs):
            matrix[index, index] = (request.reduced_momentum_x + p) ** 2 + (
                request.reduced_momentum_y + q
            ) ** 2
            for delta_p in (-1, 1):
                target = lookup.get((p + delta_p, q))
                if target is not None:
                    matrix[index, target] += model.lambda_x / 2.0
            for delta_q in (-1, 1):
                target = lookup.get((p, q + delta_q))
                if target is not None:
                    matrix[index, target] += model.lambda_y / 2.0
            for delta_p in (-1, 1):
                for delta_q in (-1, 1):
                    target = lookup.get((p + delta_p, q + delta_q))
                    if target is not None:
                        matrix[index, target] += model.lambda_xy / 4.0
        return Periodic2DHamiltonianResult(matrix)


class Periodic2DFiniteDifferenceHamiltonianConstructor:
    """Construct centered Bloch finite-difference matrices on the square cell."""

    __slots__ = ()

    def execute(
        self, request: Periodic2DFiniteDifferenceHamiltonianRequest
    ) -> Periodic2DHamiltonianResult:
        """Construct the Kronecker kinetic operator and sampled cosine potential."""
        points = request.points_per_direction
        period = 2.0 * np.pi
        kinetic_x = self._one_dimensional(request.reduced_momentum_x, points, period)
        kinetic_y = self._one_dimensional(request.reduced_momentum_y, points, period)
        identity = np.eye(points, dtype=np.complex128)
        matrix = np.kron(kinetic_x, identity) + np.kron(identity, kinetic_y)
        coordinate = np.arange(points, dtype=np.float64) * period / points
        model = request.model
        potential = (
            model.lambda_x * np.cos(coordinate)[:, None]
            + model.lambda_y * np.cos(coordinate)[None, :]
            + model.lambda_xy
            * np.cos(coordinate)[:, None]
            * np.cos(coordinate)[None, :]
        )
        matrix += np.diag(potential.ravel())
        return Periodic2DHamiltonianResult(matrix)

    @staticmethod
    def _one_dimensional(momentum: float, points: int, period: float) -> ComplexMatrix:
        spacing = period / points
        matrix = np.diag(np.full(points, 2.0 / spacing**2)).astype(np.complex128)
        off_diagonal = -1.0 / spacing**2
        matrix += np.diag(np.full(points - 1, off_diagonal), 1)
        matrix += np.diag(np.full(points - 1, off_diagonal), -1)
        matrix[0, -1] = off_diagonal * np.exp(-1j * momentum * period)
        matrix[-1, 0] = off_diagonal * np.exp(1j * momentum * period)
        return matrix
