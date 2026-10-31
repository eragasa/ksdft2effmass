"""Spinless ten-orbital diamond ``sp3s*`` Bloch Hamiltonian."""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import IntEnum

import numpy as np
from projectkoios.numerics.numpy.typing import (
    Complex128Matrix,
    Float64Array,
    Float64Matrix,
)
from projectkoios.physkit.units import ComplexMatrixQuantity

from ksdft2effmass.hamiltonian import HermitianHamiltonian

from .geometry import DiamondNeighborBond, DiamondSp3sStarGeometry
from .parameters import (
    ELECTRON_VOLT,
    DiamondSp3sStarFirstNeighbor,
    DiamondSp3sStarParameters,
    DiamondSp3sStarSecondNeighbor,
)


class Sp3sStarOrbitalIndex(IntEnum):
    """Orbital order within either diamond sublattice."""

    S = 0
    P_X = 1
    P_Y = 2
    P_Z = 3
    S_STAR = 4


@dataclass(frozen=True, slots=True)
class DiamondSp3sStarModel:
    r"""Orthogonal homopolar first/second-neighbor ``sp3s*`` model.

    The ten-orbital basis is ``(A:s,px,py,pz,s*, B:s,px,py,pz,s*)`` with real
    Slater--Koster parameters and conventional Cartesian orbital axes. Input k points
    are fractional coordinates in the reciprocal basis dual to
    ``geometry.normalized_direct_lattice``.

    Bloch sums include each orbital center ``R + tau``. Consequently a hopping from
    source site ``s`` to target site ``t`` uses

    .. math::

       \exp\left[2\pi i\,k_{\rm frac}\cdot
       (R_{t}-R_s+\tau_t-\tau_s)_{\rm frac}\right].

    The represented matrix is therefore reciprocal-lattice covariant rather than
    elementwise periodic; its spectrum is periodic. The energy reference is exactly
    the reference encoded by the onsite parameters.
    """

    geometry: DiamondSp3sStarGeometry
    parameters: DiamondSp3sStarParameters

    def __post_init__(self) -> None:
        if type(self.geometry) is not DiamondSp3sStarGeometry:
            raise TypeError("geometry must be DiamondSp3sStarGeometry")
        if type(self.parameters) is not DiamondSp3sStarParameters:
            raise TypeError("parameters must be DiamondSp3sStarParameters")

    def hamiltonian_at(self, fractional_k: Float64Array) -> HermitianHamiltonian:
        """Construct the exact-Hermitian ten-by-ten Bloch Hamiltonian in eV.

        Boolean arrays, numeric strings, nonfinite values, and non-arrays are
        rejected rather than coerced. Arithmetic uses binary64/complex128 without
        clipping; phase or matrix overflow raises :class:`OverflowError`.
        """
        k_point = self._fractional_k(fractional_k)
        with np.errstate(over="ignore", invalid="ignore"):
            onsite = self._onsite_block()
            same_sublattice = self._second_neighbor_block(k_point)
            cross_sublattice = self._first_neighbor_block(k_point)

            matrix = np.zeros((10, 10), dtype=np.complex128)
            matrix[0:5, 0:5] = onsite + same_sublattice
            matrix[5:10, 5:10] = onsite + same_sublattice
            matrix[0:5, 5:10] = cross_sublattice
            matrix[5:10, 0:5] = cross_sublattice.conjugate().T
        if not np.all(np.isfinite(matrix)):
            raise OverflowError("Slater-Koster matrix arithmetic overflowed")
        if not np.array_equal(matrix, matrix.conjugate().T):
            raise ArithmeticError("constructed Slater-Koster matrix is not Hermitian")
        return HermitianHamiltonian(matrix=ComplexMatrixQuantity(matrix, ELECTRON_VOLT))

    def two_center_hopping(
        self,
        shell: int,
        direction_cosines: Float64Array,
    ) -> Float64Matrix:
        r"""Return the real five-by-five two-center hopping map in eV.

        Rows are source orbitals and columns are target orbitals. For direction
        ``(l,m,n)`` from source to target, the sign convention is
        ``<s|H|p_i> = l_i V_sp`` and ``<p_i|H|s> = -l_i V_sp``. It follows that
        ``T(-d) = T(d).T``. Arithmetic uses binary64 without clipping and raises
        :class:`OverflowError` if a finite input produces a nonfinite matrix.
        """
        if type(shell) is not int:
            raise TypeError("shell must be an int")
        if shell not in (1, 2):
            raise ValueError("shell must be 1 or 2")
        direction = self._direction_cosines(direction_cosines)
        integrals: DiamondSp3sStarFirstNeighbor | DiamondSp3sStarSecondNeighbor
        if shell == 1:
            integrals = self.parameters.first_neighbor
            s_s_star = 0.0
            s_star_s_star = 0.0
        else:
            integrals = self.parameters.second_neighbor
            s_s_star = integrals.s_s_star_sigma.magnitude
            s_star_s_star = integrals.s_star_s_star_sigma.magnitude

        matrix = np.zeros((5, 5), dtype=np.float64)
        matrix[0, 0] = integrals.ss_sigma.magnitude
        matrix[0, 1:4] = direction * integrals.sp_sigma.magnitude
        matrix[1:4, 0] = -direction * integrals.sp_sigma.magnitude
        matrix[4, 1:4] = direction * integrals.s_star_p_sigma.magnitude
        matrix[1:4, 4] = -direction * integrals.s_star_p_sigma.magnitude
        matrix[0, 4] = s_s_star
        matrix[4, 0] = s_s_star
        matrix[4, 4] = s_star_s_star

        with np.errstate(over="ignore", invalid="ignore"):
            outer = np.outer(direction, direction)
            p_block = (
                outer * integrals.pp_sigma.magnitude
                + (np.eye(3) - outer) * integrals.pp_pi.magnitude
            )
            matrix[1:4, 1:4] = p_block
        if not np.all(np.isfinite(matrix)):
            raise OverflowError("two-center hopping arithmetic overflowed")
        immutable = np.frombuffer(matrix.astype("<f8").tobytes(), dtype="<f8")
        return immutable.reshape((5, 5))

    def _onsite_block(self) -> Float64Matrix:
        onsite = self.parameters.onsite
        return np.diag(
            np.asarray(
                (
                    onsite.s.magnitude,
                    onsite.p.magnitude,
                    onsite.p.magnitude,
                    onsite.p.magnitude,
                    onsite.s_star.magnitude,
                ),
                dtype=np.float64,
            )
        )

    def _first_neighbor_block(self, k_point: Float64Array) -> Complex128Matrix:
        block = np.zeros((5, 5), dtype=np.complex128)
        for bond in self.geometry.first_neighbor_bonds:
            direction = self.geometry.direction_cosines(bond)
            hopping = self.two_center_hopping(1, direction)
            block += hopping * self._phase(k_point, bond)
        if not np.all(np.isfinite(block)):
            raise OverflowError("first-neighbor block arithmetic overflowed")
        return block

    def _second_neighbor_block(self, k_point: Float64Array) -> Complex128Matrix:
        block = np.zeros((5, 5), dtype=np.complex128)
        for bond in self.geometry.second_neighbor_positive_bonds:
            direction = self.geometry.direction_cosines(bond)
            hopping = self.two_center_hopping(2, direction)
            term = hopping * self._phase(k_point, bond)
            block += term + term.conjugate().T
        if not np.all(np.isfinite(block)):
            raise OverflowError("second-neighbor block arithmetic overflowed")
        if not np.array_equal(block, block.conjugate().T):
            raise ArithmeticError("second-neighbor block is not Hermitian")
        return block

    def _phase(self, k_point: Float64Array, bond: DiamondNeighborBond) -> complex:
        displacement = self.geometry.primitive_displacement(bond)
        with np.errstate(over="ignore", invalid="ignore"):
            angle = 2.0 * math.pi * float(k_point @ displacement)
        if not math.isfinite(angle):
            raise OverflowError("Bloch phase argument overflowed")
        return complex(math.cos(angle), math.sin(angle))

    @staticmethod
    def _fractional_k(value: Float64Array) -> Float64Array:
        if not isinstance(value, np.ndarray):
            raise TypeError("fractional_k must be a numpy.ndarray")
        if value.dtype.kind not in "iuf":
            raise TypeError("fractional_k must contain real numbers excluding booleans")
        result = np.asarray(value, dtype=np.float64)
        if result.shape != (3,):
            raise ValueError("fractional_k must have shape (3,)")
        if not np.all(np.isfinite(result)):
            raise ValueError("fractional_k must be finite")
        return result

    @staticmethod
    def _direction_cosines(value: Float64Array) -> Float64Array:
        if not isinstance(value, np.ndarray):
            raise TypeError("direction_cosines must be a numpy.ndarray")
        if value.dtype.kind not in "iuf":
            raise TypeError(
                "direction_cosines must contain real numbers excluding booleans"
            )
        result = np.asarray(value, dtype=np.float64)
        if result.shape != (3,):
            raise ValueError("direction_cosines must have shape (3,)")
        if not np.all(np.isfinite(result)):
            raise ValueError("direction_cosines must be finite")
        if not math.isclose(
            float(np.linalg.norm(result)),
            1.0,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ):
            raise ValueError("direction_cosines must be a unit vector")
        return result
