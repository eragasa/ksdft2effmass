"""Vogl et al. (1983) nearest-neighbor spinless ``sp3s*`` model.

Notes
-----
This module independently implements the published model equations. The Gist
and notebook listed below were reviewed as development provenance; no source
code from either is copied here.

References
----------
.. [1] P. Vogl, H. P. Hjalmarson, and J. D. Dow, "A semi-empirical
   tight-binding theory of the electronic structure of semiconductors,"
   *Journal of Physics and Chemistry of Solids* 44, 365--378 (1983).
   https://doi.org/10.1016/0022-3697(83)90064-1
.. [2] Mahdisadjadi, "Zinc-blende LCAO" Gist.
   https://gist.github.com/Mahdisadjadi/62c960d3ccad1ee1868e9370e7567229
.. [3] Simon Phillpot, ``SiliconLCAO_4sDOS-v3`` notebook, modifications dated
   2026-04-29 through 2026-05-11.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import IntEnum
from numbers import Complex

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .table1 import (
    Vogl1983Compound,
    Vogl1983Table1,
    Vogl1983Table1Parameters,
)


class Vogl1983BasisIndex(IntEnum):
    """Indices of the ten-orbital anion-then-cation basis."""

    S_A = 0
    P_X_A = 1
    P_Y_A = 2
    P_Z_A = 3
    S_STAR_A = 4
    S_C = 5
    P_X_C = 6
    P_Y_C = 7
    P_Z_C = 8
    S_STAR_C = 9


@dataclass(frozen=True, slots=True)
class Vogl1983StructureFactors:
    """The four dimensionless structure factors of Vogl equation (6).

    Attributes are named and ordered exactly as the paper's ``g0`` through
    ``g3``. Use :meth:`from_reduced_wavevector` for the paper's convention
    ``k = (2*pi/a_L) q``.
    """

    g0: complex
    g1: complex
    g2: complex
    g3: complex

    def __post_init__(self) -> None:
        """Normalize finite complex-compatible scalars and reject booleans."""
        for name in ("g0", "g1", "g2", "g3"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, Complex):
                raise TypeError(f"{name} must be a complex-compatible scalar")
            normalized = complex(value)
            if not (math.isfinite(normalized.real) and math.isfinite(normalized.imag)):
                raise ValueError(f"{name} must be finite")
            object.__setattr__(self, name, normalized)

    @classmethod
    def from_reduced_wavevector(
        cls,
        reduced_wavevector: ArrayLike,
    ) -> Vogl1983StructureFactors:
        """Evaluate equation (6) for one dimensionless wavevector ``q``.

        The paper's Cartesian phase arguments ``k_j a_L / 4`` become
        ``pi*q_j/2`` under ``k = (2*pi/a_L) q``.
        """
        q = cls._reduced_wavevector(reduced_wavevector)
        phase_x, phase_y, phase_z = 0.5 * np.pi * q
        cosine_x, cosine_y, cosine_z = np.cos((phase_x, phase_y, phase_z))
        sine_x, sine_y, sine_z = np.sin((phase_x, phase_y, phase_z))

        return cls(
            g0=cosine_x * cosine_y * cosine_z - 1j * sine_x * sine_y * sine_z,
            g1=-cosine_x * sine_y * sine_z + 1j * sine_x * cosine_y * cosine_z,
            g2=-sine_x * cosine_y * sine_z + 1j * cosine_x * sine_y * cosine_z,
            g3=-sine_x * sine_y * cosine_z + 1j * cosine_x * cosine_y * sine_z,
        )

    @staticmethod
    def _reduced_wavevector(value: ArrayLike) -> NDArray[np.float64]:
        raw = np.asarray(value)
        if raw.shape != (3,):
            raise ValueError("reduced wavevector must have shape (3,)")
        if raw.dtype.kind not in "iuf":
            raise TypeError("reduced wavevector must contain real numbers")
        result = np.asarray(raw, dtype=np.float64)
        if not np.all(np.isfinite(result)):
            raise ValueError("reduced wavevector must be finite")
        return result

    def as_array(self) -> NDArray[np.complex128]:
        """Return a read-only ``(g0, g1, g2, g3)`` array."""
        result = np.asarray((self.g0, self.g1, self.g2, self.g3), dtype=np.complex128)
        result.flags.writeable = False
        return result


@dataclass(frozen=True, slots=True)
class Vogl1983HamiltonianBlocks:
    """Paper-level blocks ``D_a``, ``T(k)``, and ``D_c`` in eV.

    Each block uses the sublattice orbital order ``(s, px, py, pz, s*)``.
    Arrays are copied into read-only complex128 storage so the frozen record is
    operationally immutable.
    """

    onsite_anion: NDArray[np.complex128]
    anion_to_cation: NDArray[np.complex128]
    onsite_cation: NDArray[np.complex128]

    def __post_init__(self) -> None:
        """Own, validate, and freeze the three five-by-five blocks."""
        for name in ("onsite_anion", "anion_to_cation", "onsite_cation"):
            block = self._immutable_block(getattr(self, name), name)
            object.__setattr__(self, name, block)
        if not np.array_equal(self.onsite_anion, self.onsite_anion.conjugate().T):
            raise ValueError("anion onsite block must be Hermitian")
        if not np.array_equal(self.onsite_cation, self.onsite_cation.conjugate().T):
            raise ValueError("cation onsite block must be Hermitian")

    @classmethod
    def from_parameters(
        cls,
        parameters: Vogl1983Table1Parameters,
        structure_factors: Vogl1983StructureFactors,
    ) -> Vogl1983HamiltonianBlocks:
        """Construct the published blocks from one Table 1 row and equation (6)."""
        return cls(
            onsite_anion=cls._onsite_block(
                s_energy=parameters.e_s_a,
                p_energy=parameters.e_p_a,
                s_star_energy=parameters.e_s_star_a,
            ),
            anion_to_cation=cls._anion_to_cation_hopping_block(
                parameters,
                structure_factors,
            ),
            onsite_cation=cls._onsite_block(
                s_energy=parameters.e_s_c,
                p_energy=parameters.e_p_c,
                s_star_energy=parameters.e_s_star_c,
            ),
        )

    @staticmethod
    def _immutable_block(
        value: NDArray[np.complex128],
        name: str,
    ) -> NDArray[np.complex128]:
        raw = np.asarray(value)
        if raw.shape != (5, 5):
            raise ValueError(f"{name} must have shape (5, 5)")
        if raw.dtype.kind not in "iufc":
            raise TypeError(f"{name} must contain numeric values")
        result = np.array(raw, dtype=np.complex128, copy=True)
        if not np.all(np.isfinite(result)):
            raise ValueError(f"{name} must be finite")
        result.flags.writeable = False
        return result

    @staticmethod
    def _onsite_block(
        *,
        s_energy: float,
        p_energy: float,
        s_star_energy: float,
    ) -> NDArray[np.complex128]:
        """Return one paper-ordered ``(s, px, py, pz, s*)`` onsite block."""
        return np.diag(
            np.asarray(
                (s_energy, p_energy, p_energy, p_energy, s_star_energy),
                dtype=np.complex128,
            )
        )

    @staticmethod
    def _anion_to_cation_hopping_block(
        parameters: Vogl1983Table1Parameters,
        structure_factors: Vogl1983StructureFactors,
    ) -> NDArray[np.complex128]:
        """Return the published anion-to-cation hopping block ``T(k)``.

        Rows belong to the anion and columns to the cation. Field names such
        as ``v_s_a_p_c`` transliterate the Table 1 symbol ``V(s_a,p_c)``.
        """
        p = parameters
        g0 = structure_factors.g0
        g1 = structure_factors.g1
        g2 = structure_factors.g2
        g3 = structure_factors.g3
        return np.asarray(
            (
                # Columns: s_c, px_c, py_c, pz_c, s*_c
                # Row s_a
                (
                    p.v_s_s * g0,
                    p.v_s_a_p_c * g1,
                    p.v_s_a_p_c * g2,
                    p.v_s_a_p_c * g3,
                    0.0,
                ),
                # Row px_a
                (
                    -p.v_s_c_p_a * g1,
                    p.v_x_x * g0,
                    p.v_x_y * g3,
                    p.v_x_y * g2,
                    -p.v_p_a_s_star_c * g1,
                ),
                # Row py_a
                (
                    -p.v_s_c_p_a * g2,
                    p.v_x_y * g3,
                    p.v_x_x * g0,
                    p.v_x_y * g1,
                    -p.v_p_a_s_star_c * g2,
                ),
                # Row pz_a
                (
                    -p.v_s_c_p_a * g3,
                    p.v_x_y * g2,
                    p.v_x_y * g1,
                    p.v_x_x * g0,
                    -p.v_p_a_s_star_c * g3,
                ),
                # Row s*_a
                (
                    0.0,
                    p.v_s_star_a_p_c * g1,
                    p.v_s_star_a_p_c * g2,
                    p.v_s_star_a_p_c * g3,
                    0.0,
                ),
            ),
            dtype=np.complex128,
        )

    def assemble(self) -> NDArray[np.complex128]:
        """Assemble the read-only ten-by-ten Hermitian Hamiltonian in eV."""
        result = np.block(
            [
                [self.onsite_anion, self.anion_to_cation],
                [self.anion_to_cation.conjugate().T, self.onsite_cation],
            ]
        )
        if not np.array_equal(result, result.conjugate().T):
            raise ArithmeticError("constructed Vogl Hamiltonian is not Hermitian")
        result.flags.writeable = False
        return result


@dataclass(frozen=True, slots=True)
class Vogl1983LcaoSp3sStarModel:
    """Ten-band empirical LCAO pseudo-Hamiltonian.

    The basis is ``(s, px, py, pz, s*)`` on the anion followed by the same
    five orbitals on the cation. Energies are in eV. The real, dimensionless
    wavevector ``q`` is defined by ``k = (2*pi/a_L) q``.
    """

    compound: Vogl1983Compound
    parameters: Vogl1983Table1Parameters

    @classmethod
    def from_table(
        cls,
        table: Vogl1983Table1,
        compound: Vogl1983Compound | str,
    ) -> Vogl1983LcaoSp3sStarModel:
        """Construct the model for one accepted Table 1 row."""
        selected = Vogl1983Compound(compound)
        return cls(
            compound=selected,
            parameters=table.parameters_for(selected),
        )

    @staticmethod
    def structure_factors(
        reduced_wavevector: ArrayLike,
    ) -> Vogl1983StructureFactors:
        """Return the named structure factors of Vogl equation (6)."""
        return Vogl1983StructureFactors.from_reduced_wavevector(reduced_wavevector)

    def hamiltonian_blocks(
        self,
        reduced_wavevector: ArrayLike,
    ) -> Vogl1983HamiltonianBlocks:
        """Return the paper-level ``D_a``, ``T(k)``, and ``D_c`` blocks."""
        return Vogl1983HamiltonianBlocks.from_parameters(
            self.parameters,
            self.structure_factors(reduced_wavevector),
        )

    def hamiltonian(self, reduced_wavevector: ArrayLike) -> NDArray[np.complex128]:
        """Return the paper-ordered ten-by-ten Hermitian Hamiltonian in eV."""
        return self.hamiltonian_blocks(reduced_wavevector).assemble()

    def band_energies(self, reduced_wavevector: ArrayLike) -> NDArray[np.float64]:
        """Return ten ascending eigenvalues in eV."""
        result = np.linalg.eigvalsh(self.hamiltonian(reduced_wavevector))
        result.flags.writeable = False
        return result
