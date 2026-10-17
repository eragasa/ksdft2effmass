"""Frozen-parent gauge-locality diagnostics along synthetic finite-strain paths."""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum

import numpy as np
import numpy.typing as npt
from projectkoios.physkit.periodic.lattice import DirectLattice3D, DirectLatticeMetric

FloatArray = npt.NDArray[np.float64]
ComplexArray = npt.NDArray[np.complex128]
IntArray = npt.NDArray[np.int64]

# If n_B is a Bain/BCT reduced lattice coordinate and n_F is the existing FCC
# primitive coordinate, n_F = U n_B.  det(U)=1, so this is a bijection modulo
# every finite periodic size as well as on the infinite lattice.
BAIN_FCC_UNIMODULAR_MAP: tuple[tuple[int, int, int], ...] = (
    (1, 1, 0),
    (0, 0, 1),
    (0, -1, 0),
)
BAIN_DIAMOND_BASIS_OFFSETS: tuple[tuple[float, float, float], ...] = (
    (0.0, 0.0, 0.0),
    (0.5, -0.25, 0.25),
)


class SyntheticStrainPath(StrEnum):
    """Name one volume-normalized homogeneous deformation path."""

    RHOMBIC_2D = "area-preserving-rhombic-triangular-to-square"
    BAIN_3D = "volume-preserving-bain-fcc-to-bcc"


@dataclass(frozen=True, slots=True)
class BainPathPoint:
    """Represent one point on the continuous unit-volume Bain path."""

    strain_fraction: float
    aspect_ratio: float
    transverse_scale: float
    longitudinal_scale: float
    direct_lattice: DirectLattice3D

    def __post_init__(self) -> None:
        if type(self.direct_lattice) is not DirectLattice3D:
            raise TypeError("direct_lattice must be DirectLattice3D")

    @property
    def direct_metric(self) -> DirectLatticeMetric:
        """Return PhysKit's metric representation of this path point."""
        return DirectLatticeMetric(self.direct_lattice)

    @property
    def primitive_volume(self) -> float:
        """Return the primitive-cell volume owned by the direct lattice."""
        return self.direct_lattice.measure


class BainPath:
    """Evaluate the continuous unit-volume FCC-to-BCC Bain deformation."""

    __slots__ = ()

    def evaluate(self, strain_fraction: float) -> BainPathPoint:
        """Evaluate the path on the closed interval containing its endpoints."""
        if type(strain_fraction) is not float or not 0.0 <= strain_fraction <= 1.0:
            raise ValueError("strain_fraction must be a built-in float in [0, 1]")
        aspect_ratio = math.sqrt(2.0) + strain_fraction * (1.0 - math.sqrt(2.0))
        transverse_scale = (2.0 / aspect_ratio) ** (1.0 / 3.0)
        longitudinal_scale = aspect_ratio * transverse_scale
        direct_lattice = DirectLattice3D(
            a1=np.asarray(
                (
                    transverse_scale / 2.0,
                    transverse_scale / 2.0,
                    longitudinal_scale / 2.0,
                ),
                dtype=np.float64,
            ),
            a2=np.asarray(
                (
                    -transverse_scale / 2.0,
                    transverse_scale / 2.0,
                    longitudinal_scale / 2.0,
                ),
                dtype=np.float64,
            ),
            a3=np.asarray(
                (
                    transverse_scale / 2.0,
                    -transverse_scale / 2.0,
                    longitudinal_scale / 2.0,
                ),
                dtype=np.float64,
            ),
        )
        return BainPathPoint(
            strain_fraction=strain_fraction,
            aspect_ratio=aspect_ratio,
            transverse_scale=transverse_scale,
            longitudinal_scale=longitudinal_scale,
            direct_lattice=direct_lattice,
        )


@dataclass(frozen=True, slots=True)
class StrainPointDiagnostic:
    """Retain physical-radius locality diagnostics at one strain point."""

    strain_fraction: float
    path_parameter: float
    metric: tuple[tuple[float, ...], ...]
    minimum_bond_length: float
    maximum_bond_length: float
    distinct_bond_lengths: int
    restricted_alignment_residual: float
    ordinary_fourier_power: float
    nyquist_power: float
    first_passing_radius: tuple[float | None, ...]
    first_passing_blocks: tuple[int | None, ...]


@dataclass(frozen=True, slots=True)
class SyntheticStrainResult:
    """Retain one bounded frozen-parent strain sequence."""

    path: SyntheticStrainPath
    construction_size: int
    maximum_rotation_amplitude: float
    tail_tolerances: tuple[float, ...]
    maximum_parseval_defect: float
    maximum_strain_invariance_defect: float
    points: tuple[StrainPointDiagnostic, ...]
    status: str = "bounded-synthetic-strain-development-not-retained-evidence"


def _metric(path: SyntheticStrainPath, fraction: float) -> FloatArray:
    if path is SyntheticStrainPath.RHOMBIC_2D:
        angle = math.pi / 3.0 + fraction * math.pi / 6.0
        sine = math.sin(angle)
        cosine = math.cos(angle)
        return np.array(((1.0, cosine), (cosine, 1.0)), dtype=np.float64) / sine
    return np.asarray(
        BainPath().evaluate(fraction).direct_metric.metric_tensor,
        dtype=np.float64,
    )


def _path_parameter(path: SyntheticStrainPath, fraction: float) -> float:
    if path is SyntheticStrainPath.RHOMBIC_2D:
        return math.pi / 3.0 + fraction * math.pi / 6.0
    return BainPath().evaluate(fraction).aspect_ratio


def _bonds(path: SyntheticStrainPath) -> IntArray:
    if path is SyntheticStrainPath.RHOMBIC_2D:
        return np.array(((1, 0), (0, 1), (1, -1)), dtype=np.int64)
    return np.array(
        (
            (1, 0, 0),
            (1, -1, 0),
            (1, 0, -1),
            (1, -1, -1),
            (0, 1, 0),
            (0, 0, 1),
        ),
        dtype=np.int64,
    )


def _fourier_power(
    path: SyntheticStrainPath, size: int, amplitude: float
) -> tuple[IntArray, FloatArray, float, float, float]:
    dimension = 2 if path is SyntheticStrainPath.RHOMBIC_2D else 3
    axis = -0.5 + (np.arange(size, dtype=np.float64) + 0.5) / float(size)
    coordinates = np.stack(np.meshgrid(*(axis,) * dimension, indexing="ij"), axis=-1)
    bonds = _bonds(path).astype(np.float64)
    arguments = np.einsum("...d,bd->...b", coordinates, bonds)
    angles = (
        amplitude
        * np.sum(np.sin(2.0 * np.pi * arguments), axis=-1)
        / float(bonds.shape[0])
    )
    field = np.empty((*angles.shape, 2, 2), dtype=np.complex128)
    cosine = np.cos(2.0 * angles)
    sine = np.sin(2.0 * angles)
    field[..., 0, 0] = cosine
    field[..., 0, 1] = -sine
    field[..., 1, 0] = -sine
    field[..., 1, 1] = -cosine
    axes = tuple(range(dimension))
    blocks = np.fft.fftshift(np.fft.fftn(field, axes=axes), axes=axes) / float(
        size**dimension
    )
    integer_axis = np.arange(-size // 2, size // 2, dtype=np.int64)
    displacements = np.stack(
        np.meshgrid(*(integer_axis,) * dimension, indexing="ij"), axis=-1
    )
    origin = -0.5 + 0.5 / float(size)
    phase = np.exp(-2.0j * np.pi * origin * np.sum(displacements, axis=-1))
    blocks *= phase[..., None, None]
    flat_displacements = displacements.reshape((-1, dimension))
    flat_blocks = blocks.reshape((-1, 2, 2))
    powers = np.sum(np.abs(flat_blocks) ** 2, axis=(-2, -1)) / 2.0
    parseval = abs(1.0 - float(np.sum(powers)))
    nyquist = np.any(flat_displacements == -size // 2, axis=1)
    onsite = np.all(flat_displacements == 0, axis=1)
    restricted_residual = 1.0 - float(powers[onsite][0])
    return (
        flat_displacements[~nyquist],
        powers[~nyquist],
        float(np.sum(powers[nyquist])),
        parseval,
        restricted_residual,
    )


def _first_passing(
    squared_radii: FloatArray,
    powers: FloatArray,
    nyquist_power: float,
    tolerances: tuple[float, ...],
) -> tuple[tuple[float | None, ...], tuple[int | None, ...]]:
    order = np.argsort(squared_radii, kind="stable")
    sorted_radii = squared_radii[order]
    sorted_powers = powers[order]
    unique_radii: list[float] = []
    cumulative_powers: list[float] = []
    cumulative = 0.0
    index = 0
    while index < sorted_radii.size:
        radius = float(sorted_radii[index])
        stop = index + 1
        tolerance = 1.0e-12 * max(1.0, abs(radius))
        while (
            stop < sorted_radii.size
            and abs(float(sorted_radii[stop]) - radius) <= tolerance
        ):
            stop += 1
        cumulative += float(np.sum(sorted_powers[index:stop]))
        unique_radii.append(radius)
        cumulative_powers.append(cumulative)
        index = stop
    radii: list[float | None] = []
    blocks: list[int | None] = []
    for target in tolerances:
        selected: int | None = None
        for candidate, retained in enumerate(cumulative_powers):
            if max(nyquist_power, 1.0 - retained) <= target:
                selected = candidate
                break
        if selected is None:
            radii.append(None)
            blocks.append(None)
        else:
            radius_squared = unique_radii[selected]
            radii.append(math.sqrt(max(0.0, radius_squared)))
            cutoff_tolerance = 1.0e-12 * max(1.0, abs(radius_squared))
            blocks.append(
                int(
                    np.count_nonzero(squared_radii <= radius_squared + cutoff_tolerance)
                )
            )
    return tuple(radii), tuple(blocks)


class SyntheticStrainCalculator:
    """Calculate bounded frozen-parent gauge-locality strain sequences."""

    __slots__ = ()

    def execute(
        self,
        path: SyntheticStrainPath,
        construction_size: int,
        strain_fractions: tuple[float, ...],
        maximum_rotation_amplitude: float,
        tail_tolerances: tuple[float, ...],
    ) -> SyntheticStrainResult:
        """Calculate one bounded frozen-parent gauge-locality strain sequence."""
        if type(path) is not SyntheticStrainPath:
            raise TypeError("path must be SyntheticStrainPath")
        if (
            type(construction_size) is not int
            or construction_size < 4
            or construction_size % 2
        ):
            raise ValueError(
                "construction_size must be an even built-in integer at least four"
            )
        if (
            type(maximum_rotation_amplitude) is not float
            or not 0.0 <= maximum_rotation_amplitude <= math.pi / 4.0
        ):
            raise ValueError(
                "maximum_rotation_amplitude must be a built-in float in [0, pi/4]"
            )
        if not strain_fractions or strain_fractions != tuple(
            sorted(set(strain_fractions))
        ):
            raise ValueError("strain_fractions must be nonempty, sorted, and unique")
        if any(
            type(value) is not float or not 0.0 <= value <= 1.0
            for value in strain_fractions
        ):
            raise ValueError("strain fractions must be built-in floats in [0, 1]")
        if not tail_tolerances or any(
            type(value) is not float or not 0.0 < value < 1.0
            for value in tail_tolerances
        ):
            raise ValueError("tail tolerances must be built-in floats in (0, 1)")
        displacements, powers, nyquist, parseval, residual = _fourier_power(
            path, construction_size, maximum_rotation_amplitude
        )
        bonds = _bonds(path).astype(np.float64)
        points: list[StrainPointDiagnostic] = []
        reference_power = float(np.sum(powers))
        maximum_invariance = 0.0
        for fraction in strain_fractions:
            metric = _metric(path, fraction)
            if abs(float(np.linalg.det(metric)) - 1.0) > 2.0e-13:
                raise RuntimeError("strain metric lost unit determinant")
            squared_radii = np.einsum(
                "ri,ij,rj->r", displacements, metric, displacements
            )
            bond_squared = np.einsum("bi,ij,bj->b", bonds, metric, bonds)
            first_radii, first_blocks = _first_passing(
                squared_radii, powers, nyquist, tail_tolerances
            )
            rounded_lengths = np.round(np.sqrt(bond_squared), decimals=12)
            maximum_invariance = max(
                maximum_invariance, abs(float(np.sum(powers)) - reference_power)
            )
            points.append(
                StrainPointDiagnostic(
                    strain_fraction=fraction,
                    path_parameter=_path_parameter(path, fraction),
                    metric=tuple(
                        tuple(float(value) for value in row) for row in metric
                    ),
                    minimum_bond_length=float(np.sqrt(np.min(bond_squared))),
                    maximum_bond_length=float(np.sqrt(np.max(bond_squared))),
                    distinct_bond_lengths=len(set(rounded_lengths.tolist())),
                    restricted_alignment_residual=residual,
                    ordinary_fourier_power=float(np.sum(powers)),
                    nyquist_power=nyquist,
                    first_passing_radius=first_radii,
                    first_passing_blocks=first_blocks,
                )
            )
        return SyntheticStrainResult(
            path=path,
            construction_size=construction_size,
            maximum_rotation_amplitude=maximum_rotation_amplitude,
            tail_tolerances=tail_tolerances,
            maximum_parseval_defect=parseval,
            maximum_strain_invariance_defect=maximum_invariance,
            points=tuple(points),
        )


__all__ = [
    "BAIN_DIAMOND_BASIS_OFFSETS",
    "BAIN_FCC_UNIMODULAR_MAP",
    "BainPath",
    "BainPathPoint",
    "StrainPointDiagnostic",
    "SyntheticStrainCalculator",
    "SyntheticStrainPath",
    "SyntheticStrainResult",
]
