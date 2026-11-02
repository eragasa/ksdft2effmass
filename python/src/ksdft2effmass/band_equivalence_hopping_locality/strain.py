"""Frozen-parent gauge-locality diagnostics along synthetic finite-strain paths."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

import numpy as np
import numpy.typing as npt
from projectkoios.physkit.periodic.lattice import DirectLattice3D, DirectLatticeMetric

from ksdft2effmass.serialization import (
    BaseTypedRecord,
    SerializableValue,
    StringWireEnum,
)

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


class SyntheticStrainPathEnum(StringWireEnum):
    """Name one volume-normalized homogeneous deformation path."""

    @property
    def spatial_dimension(self) -> int:
        """Return the path's spatial dimension."""
        return 2 if self is SyntheticStrainPathEnum.RHOMBIC_2D else 3

    def metric(self, fraction: float) -> FloatArray:
        """Return the direct metric at one path fraction."""
        if self is SyntheticStrainPathEnum.RHOMBIC_2D:
            angle = math.pi / 3.0 + fraction * math.pi / 6.0
            sine = math.sin(angle)
            cosine = math.cos(angle)
            return np.array(((1.0, cosine), (cosine, 1.0)), dtype=np.float64) / sine
        return np.asarray(
            BainPath(strain_fraction=fraction).result().direct_metric.metric_tensor,
            dtype=np.float64,
        )

    def path_parameter(self, fraction: float) -> float:
        """Return the scalar path coordinate at one fraction."""
        if self is SyntheticStrainPathEnum.RHOMBIC_2D:
            return math.pi / 3.0 + fraction * math.pi / 6.0
        return BainPath(strain_fraction=fraction).result().aspect_ratio

    def rotation_bonds(self) -> IntArray:
        """Return the positive bond inventory defining the gauge rotation."""
        if self is SyntheticStrainPathEnum.RHOMBIC_2D:
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

    def parent_translations(self) -> IntArray:
        """Return the synthetic parent's positive translation inventory."""
        if self is SyntheticStrainPathEnum.RHOMBIC_2D:
            return np.asarray(((0, 0), (1, 0), (0, 1)), dtype=np.int64)
        return np.asarray(
            ((0, 0, 0), (1, 0, 0), (0, 0, 1), (1, -1, 0)),
            dtype=np.int64,
        )

    def basis_offset(self) -> FloatArray:
        """Return the non-Bravais basis offset used by the synthetic parent."""
        if self is SyntheticStrainPathEnum.RHOMBIC_2D:
            return np.asarray((1.0 / 3.0, 1.0 / 3.0), dtype=np.float64)
        return np.asarray(BAIN_DIAMOND_BASIS_OFFSETS[1], dtype=np.float64)

    def bond_lengths(self, metric: FloatArray) -> FloatArray:
        """Return basis-to-translation bond lengths in one direct metric."""
        translations = self.parent_translations().astype(np.float64)
        vectors = self.basis_offset()[None, :] - translations
        squared = np.einsum("bi,ij,bj->b", vectors, metric, vectors)
        return np.asarray(np.sqrt(squared), dtype=np.float64)

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
    """Bind one point on the continuous unit-volume FCC-to-BCC Bain deformation."""

    __slots__ = ("_strain_fraction",)

    def __init__(self, *, strain_fraction: float) -> None:
        if type(strain_fraction) is not float or not 0.0 <= strain_fraction <= 1.0:
            raise ValueError("strain_fraction must be a built-in float in [0, 1]")
        self._strain_fraction = strain_fraction

    def result(self) -> BainPathPoint:
        """Evaluate the constructor-bound point on the closed path interval."""
        strain_fraction = self._strain_fraction
        aspect_ratio = math.sqrt(2.0) + strain_fraction * (1.0 - math.sqrt(2.0))
        transverse_scale = math.cbrt(2.0 / aspect_ratio)
        # Use l=2/t^2 (algebraically l=gamma*t) so t^2*l/2 rounds to unit volume.
        longitudinal_scale = 2.0 / (transverse_scale * transverse_scale)
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
class StrainPointDiagnostic(BaseTypedRecord):
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

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "strain_fraction": self.strain_fraction,
            "path_parameter": self.path_parameter,
            "metric": self.metric,
            "minimum_bond_length": self.minimum_bond_length,
            "maximum_bond_length": self.maximum_bond_length,
            "distinct_bond_lengths": self.distinct_bond_lengths,
            "restricted_alignment_residual": self.restricted_alignment_residual,
            "ordinary_fourier_power": self.ordinary_fourier_power,
            "nyquist_power": self.nyquist_power,
            "first_passing_radius": self.first_passing_radius,
            "first_passing_blocks": self.first_passing_blocks,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "strain_fraction",
            "path_parameter",
            "metric",
            "minimum_bond_length",
            "maximum_bond_length",
            "distinct_bond_lengths",
            "restricted_alignment_residual",
            "ordinary_fourier_power",
            "nyquist_power",
            "first_passing_radius",
            "first_passing_blocks",
        }
        if set(values) != required:
            raise ValueError("strain-point fields do not match")
        strain_fraction = values["strain_fraction"]
        path_parameter = values["path_parameter"]
        minimum_bond_length = values["minimum_bond_length"]
        maximum_bond_length = values["maximum_bond_length"]
        restricted_alignment_residual = values["restricted_alignment_residual"]
        ordinary_fourier_power = values["ordinary_fourier_power"]
        nyquist_power = values["nyquist_power"]
        if (
            type(strain_fraction) is not float
            or type(path_parameter) is not float
            or type(minimum_bond_length) is not float
            or type(maximum_bond_length) is not float
            or type(restricted_alignment_residual) is not float
            or type(ordinary_fourier_power) is not float
            or type(nyquist_power) is not float
        ):
            raise TypeError("strain-point scalars must decode to built-in floats")
        metric = values["metric"]
        radii = values["first_passing_radius"]
        blocks = values["first_passing_blocks"]
        distinct = values["distinct_bond_lengths"]
        if not isinstance(metric, tuple) or any(
            not isinstance(row, tuple)
            or any(type(component) is not float for component in row)
            for row in metric
        ):
            raise TypeError("metric must decode to a tuple of float tuples")
        if not isinstance(radii, tuple) or any(
            value is not None and type(value) is not float for value in radii
        ):
            raise TypeError("first-passing radii must decode to floats or None")
        if not isinstance(blocks, tuple) or any(
            value is not None and type(value) is not int for value in blocks
        ):
            raise TypeError("first-passing blocks must decode to integers or None")
        if type(distinct) is not int:
            raise TypeError("distinct_bond_lengths must decode to an integer")
        return cls(
            strain_fraction=strain_fraction,
            path_parameter=path_parameter,
            metric=metric,
            minimum_bond_length=minimum_bond_length,
            maximum_bond_length=maximum_bond_length,
            distinct_bond_lengths=distinct,
            restricted_alignment_residual=restricted_alignment_residual,
            ordinary_fourier_power=ordinary_fourier_power,
            nyquist_power=nyquist_power,
            first_passing_radius=radii,
            first_passing_blocks=blocks,
        )


@dataclass(frozen=True, slots=True)
class SyntheticStrainResult(BaseTypedRecord):
    """Retain one bounded frozen-parent strain sequence."""

    path: SyntheticStrainPathEnum
    construction_size: int
    maximum_rotation_amplitude: float
    tail_tolerances: tuple[float, ...]
    maximum_parseval_defect: float
    maximum_strain_invariance_defect: float
    points: tuple[StrainPointDiagnostic, ...]
    status: str = "bounded-synthetic-strain-development-not-retained-evidence"

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "path": self.path.to_wire(),
            "construction_size": self.construction_size,
            "maximum_rotation_amplitude": self.maximum_rotation_amplitude,
            "tail_tolerances": self.tail_tolerances,
            "maximum_parseval_defect": self.maximum_parseval_defect,
            "maximum_strain_invariance_defect": (self.maximum_strain_invariance_defect),
            "points": self.points,
            "status": self.status,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "path",
            "construction_size",
            "maximum_rotation_amplitude",
            "tail_tolerances",
            "maximum_parseval_defect",
            "maximum_strain_invariance_defect",
            "points",
            "status",
        }
        if set(values) != required:
            raise ValueError("synthetic-strain result fields do not match")
        path = values["path"]
        size = values["construction_size"]
        amplitude = values["maximum_rotation_amplitude"]
        tolerances = values["tail_tolerances"]
        parseval = values["maximum_parseval_defect"]
        invariance = values["maximum_strain_invariance_defect"]
        points_value = values["points"]
        status = values["status"]
        if type(path) is not str or type(status) is not str:
            raise TypeError("synthetic-strain labels must decode to strings")
        if type(size) is not int:
            raise TypeError("construction_size must decode to an integer")
        if (
            type(amplitude) is not float
            or type(parseval) is not float
            or type(invariance) is not float
        ):
            raise TypeError("synthetic-strain scalars must decode to floats")
        if not isinstance(tolerances, tuple) or any(
            type(value) is not float for value in tolerances
        ):
            raise TypeError("tail_tolerances must decode to a float tuple")
        if not isinstance(points_value, tuple) or any(
            not isinstance(value, Mapping) for value in points_value
        ):
            raise TypeError("points must decode to a tuple of mappings")
        return cls(
            path=SyntheticStrainPathEnum.from_wire(path),
            construction_size=size,
            maximum_rotation_amplitude=amplitude,
            tail_tolerances=tolerances,
            maximum_parseval_defect=parseval,
            maximum_strain_invariance_defect=invariance,
            points=tuple(
                StrainPointDiagnostic.from_dict(value) for value in points_value
            ),
            status=status,
        )


class SyntheticStrainNumerics:
    """Own path-specific metric, bond, Fourier-power, and cutoff numerics."""

    __slots__ = ("_amplitude", "_path", "_size", "_tolerances")

    def __init__(
        self,
        *,
        path: SyntheticStrainPathEnum,
        size: int,
        amplitude: float,
        tolerances: tuple[float, ...],
    ) -> None:
        self._path = path
        self._size = size
        self._amplitude = amplitude
        self._tolerances = tolerances

    def metric(self, fraction: float) -> FloatArray:
        """Return the direct metric at one path fraction."""
        return self._path.metric(fraction)

    def path_parameter(self, fraction: float) -> float:
        """Return the scalar path coordinate at one fraction."""
        return self._path.path_parameter(fraction)

    def bonds(self) -> IntArray:
        """Return the positive-bond inventory for the bound path."""
        return self._path.rotation_bonds()

    def fourier_power(self) -> tuple[IntArray, FloatArray, float, float, float]:
        """Return ordinary powers, Nyquist power, Parseval defect, and residual."""
        dimension = 2 if self._path is SyntheticStrainPathEnum.RHOMBIC_2D else 3
        axis = -0.5 + (np.arange(self._size, dtype=np.float64) + 0.5) / float(
            self._size
        )
        coordinates = np.stack(
            np.meshgrid(*(axis,) * dimension, indexing="ij"),
            axis=-1,
        )
        bonds = self.bonds().astype(np.float64)
        arguments = np.einsum("...d,bd->...b", coordinates, bonds)
        angles = (
            self._amplitude
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
        blocks = np.fft.fftshift(
            np.fft.fftn(field, axes=axes),
            axes=axes,
        ) / float(self._size**dimension)
        integer_axis = np.arange(
            -self._size // 2,
            self._size // 2,
            dtype=np.int64,
        )
        displacements = np.stack(
            np.meshgrid(*(integer_axis,) * dimension, indexing="ij"),
            axis=-1,
        )
        origin = -0.5 + 0.5 / float(self._size)
        phase = np.exp(-2.0j * np.pi * origin * np.sum(displacements, axis=-1))
        blocks *= phase[..., None, None]
        flat_displacements = displacements.reshape((-1, dimension))
        flat_blocks = blocks.reshape((-1, 2, 2))
        powers = np.sum(np.abs(flat_blocks) ** 2, axis=(-2, -1)) / 2.0
        parseval = abs(1.0 - float(np.sum(powers)))
        nyquist = np.any(flat_displacements == -self._size // 2, axis=1)
        onsite = np.all(flat_displacements == 0, axis=1)
        restricted_residual = 1.0 - float(powers[onsite][0])
        return (
            flat_displacements[~nyquist],
            powers[~nyquist],
            float(np.sum(powers[nyquist])),
            parseval,
            restricted_residual,
        )

    def first_passing(
        self,
        *,
        squared_radii: FloatArray,
        powers: FloatArray,
        nyquist_power: float,
    ) -> tuple[tuple[float | None, ...], tuple[int | None, ...]]:
        """Return the first attained radius and block count per bound tolerance."""
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
        for target in self._tolerances:
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
                        np.count_nonzero(
                            squared_radii <= radius_squared + cutoff_tolerance
                        )
                    )
                )
        return tuple(radii), tuple(blocks)


class SyntheticStrainCalculator:
    """Own one bounded frozen-parent gauge-locality strain calculation."""

    __slots__ = (
        "_construction_size",
        "_maximum_rotation_amplitude",
        "_path",
        "_strain_fractions",
        "_tail_tolerances",
    )

    def __init__(
        self,
        *,
        path: SyntheticStrainPathEnum,
        construction_size: int,
        strain_fractions: tuple[float, ...],
        maximum_rotation_amplitude: float,
        tail_tolerances: tuple[float, ...],
    ) -> None:
        if type(path) is not SyntheticStrainPathEnum:
            raise TypeError("path must be SyntheticStrainPathEnum")
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
        self._path = path
        self._construction_size = construction_size
        self._strain_fractions = strain_fractions
        self._maximum_rotation_amplitude = maximum_rotation_amplitude
        self._tail_tolerances = tail_tolerances

    def execute(self) -> SyntheticStrainResult:
        """Calculate the constructor-bound gauge-locality strain sequence."""
        numerics = SyntheticStrainNumerics(
            path=self._path,
            size=self._construction_size,
            amplitude=self._maximum_rotation_amplitude,
            tolerances=self._tail_tolerances,
        )
        displacements, powers, nyquist, parseval, residual = numerics.fourier_power()
        path = self._path
        construction_size = self._construction_size
        strain_fractions = self._strain_fractions
        maximum_rotation_amplitude = self._maximum_rotation_amplitude
        tail_tolerances = self._tail_tolerances
        bonds = numerics.bonds().astype(np.float64)
        points: list[StrainPointDiagnostic] = []
        reference_power = float(np.sum(powers))
        maximum_invariance = 0.0
        for fraction in strain_fractions:
            metric = numerics.metric(fraction)
            if abs(float(np.linalg.det(metric)) - 1.0) > 2.0e-13:
                raise RuntimeError("strain metric lost unit determinant")
            squared_radii = np.einsum(
                "ri,ij,rj->r", displacements, metric, displacements
            )
            bond_squared = np.einsum("bi,ij,bj->b", bonds, metric, bonds)
            first_radii, first_blocks = numerics.first_passing(
                squared_radii=squared_radii,
                powers=powers,
                nyquist_power=nyquist,
            )
            rounded_lengths = np.round(np.sqrt(bond_squared), decimals=12)
            maximum_invariance = max(
                maximum_invariance, abs(float(np.sum(powers)) - reference_power)
            )
            points.append(
                StrainPointDiagnostic(
                    strain_fraction=fraction,
                    path_parameter=numerics.path_parameter(fraction),
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
    "SyntheticStrainPathEnum",
    "SyntheticStrainResult",
]
