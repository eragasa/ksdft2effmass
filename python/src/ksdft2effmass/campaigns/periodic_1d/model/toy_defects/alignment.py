"""Reusable basis-scrambling maps for controlled periodic-1D toy systems."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .hopping import ComplexMatrix


@dataclass(frozen=True, slots=True)
class Periodic1DBasisScramblingModel:
    """Represent a controlled site, orbital, phase, and spin basis scrambling.

    Parameters
    ----------
    translation_cells
        Integer cyclic translation applied to primitive-cell site labels.
    orbital_permutation
        Exact permutation of the two authored orbital labels.
    orbital_rotation_radians
        Finite real two-orbital rotation angle in radians.
    orbital_phases_radians
        Two finite orbital phases in radians.
    site_phase_step_radians
        Finite linear site-and-orbital phase increment in radians.
    spin_rotation_axis
        Finite nonzero three-component spin-rotation axis.
    spin_rotation_radians
        Finite spin-half rotation angle in radians.

    Notes
    -----
    This toy model owns no campaign phase, retained path, energy shift, inference
    threshold, provenance, or acceptance policy.
    """

    translation_cells: int
    orbital_permutation: tuple[int, int]
    orbital_rotation_radians: float
    orbital_phases_radians: tuple[float, float]
    site_phase_step_radians: float
    spin_rotation_axis: tuple[float, float, float]
    spin_rotation_radians: float

    def __post_init__(self) -> None:
        """Validate exact permutation, scalar types, finiteness, and spin axis."""
        if type(self.translation_cells) is not int:
            raise TypeError("translation_cells must be an integer")
        if type(self.orbital_permutation) is not tuple or any(
            type(value) is not int for value in self.orbital_permutation
        ):
            raise TypeError("orbital_permutation must contain built-in integers")
        if tuple(sorted(self.orbital_permutation)) != (0, 1):
            raise ValueError("orbital_permutation must contain zero and one")
        reals = (
            self.orbital_rotation_radians,
            *self.orbital_phases_radians,
            self.site_phase_step_radians,
            *self.spin_rotation_axis,
            self.spin_rotation_radians,
        )
        if any(
            isinstance(value, bool) or not isinstance(value, int | float)
            for value in reals
        ):
            raise TypeError("basis-scrambling angles and axis must be real numbers")
        if not np.all(np.isfinite(np.asarray(reals, dtype=np.float64))):
            raise ValueError("basis-scrambling angles and axis must be finite")
        if np.linalg.norm(np.asarray(self.spin_rotation_axis, dtype=np.float64)) == 0.0:
            raise ValueError("spin_rotation_axis must be nonzero")


@dataclass(frozen=True, slots=True)
class Periodic1DBasisScramblingRequest:
    """Request one finite periodic basis-scrambling map.

    Parameters
    ----------
    model
        Immutable scrambling controls.
    cell_count
        Positive finite-periodic cell count.
    reduced_momentum
        Finite primitive reciprocal-coordinate momentum.
    spin_count
        Represented spin factor, one for spinless or two for spin-half.
    """

    model: Periodic1DBasisScramblingModel
    cell_count: int
    reduced_momentum: float
    spin_count: int

    def __post_init__(self) -> None:
        """Require exact record types and valid geometry, momentum, and spin factor."""
        if not isinstance(self.model, Periodic1DBasisScramblingModel):
            raise TypeError("model must be Periodic1DBasisScramblingModel")
        if type(self.cell_count) is not int:
            raise TypeError("cell_count must be an integer")
        if self.cell_count < 1:
            raise ValueError("cell_count must be positive")
        if isinstance(self.reduced_momentum, bool) or not isinstance(
            self.reduced_momentum, int | float | np.float64
        ):
            raise TypeError("reduced_momentum must be a real scalar")
        if not np.isfinite(self.reduced_momentum):
            raise ValueError("reduced_momentum must be finite")
        if type(self.spin_count) is not int:
            raise TypeError("spin_count must be an integer")
        if self.spin_count not in (1, 2):
            raise ValueError("spin_count must be one or two")
        object.__setattr__(self, "reduced_momentum", float(self.reduced_momentum))


@dataclass(frozen=True, slots=True)
class Periodic1DBasisScramblingResult:
    """Store both directions of one operationally immutable unitary map.

    Parameters
    ----------
    reference_to_candidate
        Map taking reference coordinate vectors to candidate coordinates.
    candidate_to_reference
        Exact conjugate-transpose inverse map.
    """

    reference_to_candidate: ComplexMatrix
    candidate_to_reference: ComplexMatrix

    def __post_init__(self) -> None:
        """Validate square finite matrices, inverse relation, and read-only storage."""
        matrices: list[ComplexMatrix] = []
        for name in ("reference_to_candidate", "candidate_to_reference"):
            source = getattr(self, name)
            if not isinstance(source, np.ndarray):
                raise TypeError(f"{name} must be a NumPy array")
            if not np.issubdtype(source.dtype, np.number) or np.issubdtype(
                source.dtype, np.bool_
            ):
                raise TypeError(f"{name} must contain numeric non-Boolean values")
            value = np.asarray(source, dtype=np.complex128)
            if (
                value.ndim != 2
                or value.shape[0] == 0
                or value.shape[0] != value.shape[1]
            ):
                raise ValueError(f"{name} must be nonempty and square")
            if not np.all(np.isfinite(value)):
                raise ValueError(f"{name} must be finite")
            immutable = np.frombuffer(
                value.tobytes(order="C"), dtype=np.complex128
            ).reshape(value.shape)
            object.__setattr__(self, name, immutable)
            matrices.append(immutable)
        if not np.allclose(matrices[1], matrices[0].conj().T, rtol=0.0, atol=1.0e-14):
            raise ValueError("map directions must be conjugate-transpose inverses")


class Periodic1DBasisScramblingConstructor:
    """Construct controlled finite-periodic site, orbital, phase, and spin maps."""

    __slots__ = ()

    def execute(
        self, request: Periodic1DBasisScramblingRequest
    ) -> Periodic1DBasisScramblingResult:
        """Construct both unitary map directions.

        Parameters
        ----------
        request
            Validated scrambling model, periodic geometry, momentum, and spin factor.

        Returns
        -------
        Periodic1DBasisScramblingResult
            Reference-to-candidate map and its conjugate-transpose inverse.

        Raises
        ------
        TypeError
            If ``request`` has the wrong public type.
        """
        if not isinstance(request, Periodic1DBasisScramblingRequest):
            raise TypeError("request must be Periodic1DBasisScramblingRequest")
        model = request.model
        size = request.cell_count
        translation = np.zeros((size, size), dtype=np.complex128)
        for source in range(size):
            raw_target = source + model.translation_cells
            target = raw_target % size
            crossings = (raw_target - target) // size
            translation[target, source] = np.exp(
                2j * np.pi * request.reduced_momentum * size * crossings
            )
        cosine = np.cos(model.orbital_rotation_radians)
        sine = np.sin(model.orbital_rotation_radians)
        orbital_rotation = np.asarray(
            ((cosine, -sine), (sine, cosine)), dtype=np.complex128
        )
        orbital_phases = np.diag(np.exp(1j * np.asarray(model.orbital_phases_radians)))
        orbital_permutation = np.eye(2, dtype=np.complex128)[
            np.asarray(model.orbital_permutation, dtype=np.int64)
        ]
        site_orbital = np.asarray(
            np.kron(
                translation,
                orbital_phases @ orbital_permutation @ orbital_rotation,
            ),
            dtype=np.complex128,
        )
        diagonal = np.asarray(
            [
                np.exp(1j * model.site_phase_step_radians * (site + 0.5 * orbital))
                for site in range(size)
                for orbital in range(2)
            ],
            dtype=np.complex128,
        )
        reference_to_candidate = np.diag(diagonal) @ site_orbital
        if request.spin_count == 2:
            reference_to_candidate = np.asarray(
                np.kron(reference_to_candidate, self._spin_rotation(model)),
                dtype=np.complex128,
            )
        return Periodic1DBasisScramblingResult(
            reference_to_candidate=reference_to_candidate,
            candidate_to_reference=reference_to_candidate.conj().T,
        )

    @staticmethod
    def _spin_rotation(model: Periodic1DBasisScramblingModel) -> ComplexMatrix:
        """Construct the spin-half SU(2) rotation for the normalized authored axis."""
        axis = np.asarray(model.spin_rotation_axis, dtype=np.float64)
        axis /= np.linalg.norm(axis)
        pauli_x = np.asarray(((0.0, 1.0), (1.0, 0.0)), dtype=np.complex128)
        pauli_y = np.asarray(((0.0, -1j), (1j, 0.0)), dtype=np.complex128)
        pauli_z = np.asarray(((1.0, 0.0), (0.0, -1.0)), dtype=np.complex128)
        generator = axis[0] * pauli_x + axis[1] * pauli_y + axis[2] * pauli_z
        return np.asarray(
            np.cos(model.spin_rotation_radians / 2.0) * np.eye(2)
            - 1j * np.sin(model.spin_rotation_radians / 2.0) * generator,
            dtype=np.complex128,
        )
