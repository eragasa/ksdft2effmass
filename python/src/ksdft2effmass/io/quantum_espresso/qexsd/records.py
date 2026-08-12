"""Immutable mechanically faithful QEXSD source and document values."""

from __future__ import annotations

import hashlib
import math
import re
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import ClassVar

type Vector3 = tuple[float, float, float]
type Vector3Sequence = tuple[Vector3, ...]
type SpeciesDeclaration = tuple[str, float, str]
type AtomDeclaration = tuple[int, str, Vector3]
type Spectrum = tuple[tuple[float, ...], ...]


@dataclass(frozen=True, slots=True)
class QexsdSource:
    """Explicit QEXSD bytes and verified external source identity."""

    _SHA256: ClassVar[re.Pattern[str]] = re.compile(r"[0-9a-f]{64}\Z")

    canonical_path: str
    sha256: str
    byte_count: int
    content: bytes

    def __post_init__(self) -> None:
        if type(self.canonical_path) is not str:
            raise TypeError("canonical_path must be a built-in str")
        path = PurePosixPath(self.canonical_path)
        if (
            not self.canonical_path.startswith("/")
            or self.canonical_path.startswith("//")
            or str(path) != self.canonical_path
            or any(part in {"", ".", ".."} for part in path.parts[1:])
        ):
            raise ValueError("canonical_path must be a canonical absolute POSIX path")
        if type(self.sha256) is not str:
            raise TypeError("sha256 must be a built-in str")
        if self._SHA256.fullmatch(self.sha256) is None:
            raise ValueError("sha256 must be lowercase SHA-256")
        if type(self.byte_count) is not int:
            raise TypeError("byte_count must be a built-in integer excluding bool")
        if self.byte_count < 0:
            raise ValueError("byte_count must be nonnegative")
        if type(self.content) is not bytes:
            raise TypeError("content must be built-in bytes")
        if (
            len(self.content) != self.byte_count
            or hashlib.sha256(self.content).hexdigest() != self.sha256
        ):
            raise ValueError("QEXSD source identity mismatch")


@dataclass(frozen=True, slots=True)
class QexsdDocument:
    """Mechanically parsed raw values in exact QEXSD source order.

    Labels describe source locations only.  No unit, coordinate, scale, weight,
    spin, or energy-reference interpretation is performed here.
    """

    _SHA256: ClassVar[re.Pattern[str]] = re.compile(r"[0-9a-f]{64}\Z")

    source_path: str
    source_sha256: str
    source_byte_count: int
    namespace: str
    qexsd_version: str
    producing_application: str
    producing_application_version: str | None
    declared_unit_system_label: str
    atomic_structure_alat: float
    direct_lattice_vectors: Vector3Sequence
    direct_lattice_source_label: str
    reciprocal_lattice_coefficients: Vector3Sequence
    reciprocal_lattice_source_label: str
    species: tuple[SpeciesDeclaration, ...]
    atoms: tuple[AtomDeclaration, ...]
    declared_atom_count: int
    atomic_positions_source_label: str
    k_points: Vector3Sequence
    k_point_weights: tuple[float, ...]
    sampled_k_point_count: int
    k_point_source_label: str
    eigenvalues: Spectrum
    occupations: Spectrum | None
    eigenvalue_source_label: str
    band_count: int
    total_energy: float
    total_energy_source_label: str
    fft_grid: tuple[int, int, int]
    fft_smooth: tuple[int, int, int]
    fft_box: tuple[int, int, int]
    exit_status: int

    def __post_init__(self) -> None:
        strings = (
            self.source_path,
            self.source_sha256,
            self.namespace,
            self.qexsd_version,
            self.producing_application,
            self.declared_unit_system_label,
            self.direct_lattice_source_label,
            self.reciprocal_lattice_source_label,
            self.atomic_positions_source_label,
            self.k_point_source_label,
            self.eigenvalue_source_label,
            self.total_energy_source_label,
        )
        if any(type(value) is not str or not value for value in strings):
            raise ValueError("QEXSD document string fields must be nonempty strings")
        if self._SHA256.fullmatch(self.source_sha256) is None:
            raise ValueError("source_sha256 must be lowercase SHA-256")
        if (
            type(self.atomic_structure_alat) is not float
            or not math.isfinite(self.atomic_structure_alat)
            or self.atomic_structure_alat <= 0
        ):
            raise ValueError("atomic_structure_alat must be a positive built-in float")
        self._vectors(self.direct_lattice_vectors, "direct lattice", 3)
        self._vectors(self.reciprocal_lattice_coefficients, "reciprocal lattice", 3)
        self._vectors(self.k_points, "k points", None)
        if type(self.species) is not tuple or not self.species:
            raise ValueError("species must be a nonempty tuple")
        species_names = tuple(item[0] for item in self.species)
        if len(set(species_names)) != len(species_names):
            raise ValueError("species names must be unique")
        if type(self.atoms) is not tuple or len(self.atoms) != self.declared_atom_count:
            raise ValueError("atom count disagrees")
        for expected, atom in enumerate(self.atoms, start=1):
            if (
                type(atom) is not tuple
                or len(atom) != 3
                or atom[0] != expected
                or atom[1] not in species_names
            ):
                raise ValueError("atom ordering or species reference is invalid")
            self._vector(atom[2], "atomic position")
        if (
            type(self.k_point_weights) is not tuple
            or len(self.k_point_weights) != len(self.k_points)
            or self.sampled_k_point_count != len(self.k_points)
        ):
            raise ValueError("k-point counts disagree")
        if any(
            type(value) is not float or not math.isfinite(value) or value < 0
            for value in self.k_point_weights
        ):
            raise ValueError("k-point weights must be finite nonnegative floats")
        if type(self.eigenvalues) is not tuple or len(self.eigenvalues) != len(
            self.k_points
        ):
            raise ValueError("eigenvalue and k-point counts disagree")
        for row in self.eigenvalues:
            self._row(row, "eigenvalues")
            if len(row) != self.band_count:
                raise ValueError("eigenvalue band counts disagree")
        if self.occupations is not None:
            if type(self.occupations) is not tuple or len(self.occupations) != len(
                self.eigenvalues
            ):
                raise ValueError("occupation shape disagrees")
            for occupations, eigenvalues in zip(
                self.occupations, self.eigenvalues, strict=True
            ):
                self._row(occupations, "occupations")
                if len(occupations) != len(eigenvalues):
                    raise ValueError("occupation shape disagrees")
        if type(self.total_energy) is not float or not math.isfinite(self.total_energy):
            raise ValueError("total_energy must be a finite built-in float")
        for name in ("fft_grid", "fft_smooth", "fft_box"):
            grid = getattr(self, name)
            if (
                type(grid) is not tuple
                or len(grid) != 3
                or any(type(value) is not int or value <= 0 for value in grid)
            ):
                raise ValueError(f"{name} must contain three positive integers")
        if type(self.exit_status) is not int or not 0 <= self.exit_status <= 255:
            raise ValueError("exit_status must be in 0..255")

    @classmethod
    def _vectors(cls, vectors: object, name: str, count: int | None) -> None:
        if type(vectors) is not tuple or (count is not None and len(vectors) != count):
            raise ValueError(f"{name} vector collection is invalid")
        for vector in vectors:
            cls._vector(vector, name)

    @staticmethod
    def _vector(vector: object, name: str) -> None:
        if (
            type(vector) is not tuple
            or len(vector) != 3
            or any(
                type(value) is not float or not math.isfinite(value) for value in vector
            )
        ):
            raise ValueError(f"{name} must contain finite three-component tuples")

    @staticmethod
    def _row(row: object, name: str) -> None:
        if (
            type(row) is not tuple
            or not row
            or any(
                type(value) is not float or not math.isfinite(value) for value in row
            )
        ):
            raise ValueError(f"{name} rows must contain finite floats")
