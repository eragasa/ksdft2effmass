"""Immutable native-QEXSD and backend-neutral periodic calculation records.

The records retain ordered finite binary64 values and explicit native units.  They
represent one supported QEXSD extraction boundary; they do not establish energy
alignment, basis or gauge identity, convergence, numerical verification, or
scientific validation.  XML parsing, semantic construction, and JSON
serialization are owned by separate ActionObjects.
"""

from __future__ import annotations

import hashlib
import math
import re
from dataclasses import dataclass
from enum import StrEnum
from pathlib import PurePosixPath
from typing import ClassVar

type Vector3 = tuple[float, float, float]
type Vector3Sequence = tuple[Vector3, ...]
type SpeciesDeclaration = tuple[str, float, str]
type AtomDeclaration = tuple[int, str, Vector3]
type Spectrum = tuple[tuple[float, ...], ...]


class UnavailableReason(StrEnum):
    """Closed reasons for required semantics unavailable from the QEXSD source.

    Attributes
    ----------
    NOT_REPRESENTED_IN_QEXSD
        The accepted XML contains no value or convention for the concept.
    NO_SPIN_RESOLVED_ARRAYS
        The accepted XML has no explicit spin-resolved spectral arrays.
    NO_RETAINED_SUBSPACE
        QEXSD reports Kohn--Sham bands but no retained reduced subspace.
    """

    NOT_REPRESENTED_IN_QEXSD = "not_represented_in_qexsd"
    NO_SPIN_RESOLVED_ARRAYS = "no_spin_resolved_arrays_in_qexsd"
    NO_RETAINED_SUBSPACE = "no_retained_subspace_represented_in_qexsd"


@dataclass(frozen=True, slots=True)
class QexsdSource:
    """Explicit immutable QEXSD bytes and their external source identity.

    Parameters
    ----------
    canonical_path
        Canonical absolute POSIX path supplied by the caller.  The object does
        not discover, resolve, or open this path.
    sha256
        Expected lowercase SHA-256 digest of ``content``.
    byte_count
        Expected exact byte count of ``content``.
    content
        Exact XML bytes, defensively immutable by the built-in ``bytes`` type.

    Raises
    ------
    TypeError
        If field semantic types are wrong; booleans are not byte counts.
    ValueError
        If path or identity syntax is invalid or content identity disagrees.
    """

    _SHA256: ClassVar[re.Pattern[str]] = re.compile(r"[0-9a-f]{64}\Z")

    canonical_path: str
    sha256: str
    byte_count: int
    content: bytes

    def __post_init__(self) -> None:
        """Validate the explicit path, bytes, and exact source identity."""
        if type(self.canonical_path) is not str:
            raise TypeError("canonical_path must be a built-in str")
        path = PurePosixPath(self.canonical_path)
        if (
            not self.canonical_path.startswith("/")
            or self.canonical_path.startswith("//")
            or any(part in {"", ".", ".."} for part in path.parts[1:])
        ):
            raise ValueError("canonical_path must be a canonical absolute POSIX path")
        if str(path) != self.canonical_path:
            raise ValueError("canonical_path must be lexically canonical")
        if type(self.sha256) is not str:
            raise TypeError("sha256 must be a built-in str")
        if self._SHA256.fullmatch(self.sha256) is None:
            raise ValueError("sha256 must be 64 lowercase hexadecimal characters")
        if type(self.byte_count) is not int:
            raise TypeError("byte_count must be a built-in int excluding bool")
        if self.byte_count < 0:
            raise ValueError("byte_count must be nonnegative")
        if type(self.content) is not bytes:
            raise TypeError("content must be built-in bytes")
        if len(self.content) != self.byte_count:
            raise ValueError("QEXSD source byte-count mismatch")
        if hashlib.sha256(self.content).hexdigest() != self.sha256:
            raise ValueError("QEXSD source SHA-256 mismatch")


@dataclass(frozen=True, slots=True)
class QexsdDocument:
    """Immutable mechanically parsed values from one supported QEXSD document.

    All tuple order is source order.  Units and coordinate-convention strings
    are retained labels; no unit conversion, normalization, reordering,
    deduplication, or scientific interpretation is performed.
    """

    _SHA256: ClassVar[re.Pattern[str]] = re.compile(r"[0-9a-f]{64}\Z")

    source_path: str
    source_sha256: str
    source_byte_count: int
    namespace: str
    qexsd_version: str
    producing_application: str
    producing_application_version: str | None
    declared_units: str
    direct_lattice_vectors: Vector3Sequence
    direct_lattice_unit: str
    direct_lattice_convention: str
    reciprocal_lattice_vectors: Vector3Sequence
    reciprocal_lattice_unit: str
    reciprocal_lattice_convention: str
    species: tuple[SpeciesDeclaration, ...]
    atoms: tuple[AtomDeclaration, ...]
    declared_atom_count: int
    position_unit: str
    position_convention: str
    k_points: Vector3Sequence
    k_point_weights: tuple[float, ...]
    sampled_k_point_count: int
    k_point_convention: str
    eigenvalues: Spectrum
    occupations: Spectrum | None
    energy_unit: str
    band_count: int
    spin_channels: tuple[str, ...] | None
    total_energy: float
    total_energy_unit: str
    fft_grid: tuple[int, int, int]
    fft_smooth: tuple[int, int, int]
    fft_box: tuple[int, int, int]
    exit_status: int

    def __post_init__(self) -> None:
        """Validate native structural, cardinality, finiteness, and order state."""
        strings = (
            self.source_path,
            self.source_sha256,
            self.namespace,
            self.qexsd_version,
            self.producing_application,
            self.declared_units,
            self.direct_lattice_unit,
            self.direct_lattice_convention,
            self.reciprocal_lattice_unit,
            self.reciprocal_lattice_convention,
            self.position_unit,
            self.position_convention,
            self.k_point_convention,
            self.energy_unit,
            self.total_energy_unit,
        )
        if any(type(value) is not str for value in strings):
            raise TypeError("QEXSD document text fields must be built-in strings")
        if any(value == "" for value in strings):
            raise ValueError("QEXSD document text fields must not be empty")
        source_path = PurePosixPath(self.source_path)
        if (
            not self.source_path.startswith("/")
            or self.source_path.startswith("//")
            or str(source_path) != self.source_path
            or any(part in {"", ".", ".."} for part in source_path.parts[1:])
        ):
            raise ValueError("source_path must be a canonical absolute POSIX path")
        if self._SHA256.fullmatch(self.source_sha256) is None:
            raise ValueError(
                "source_sha256 must be 64 lowercase hexadecimal characters"
            )
        if self.producing_application_version is not None:
            if type(self.producing_application_version) is not str:
                raise TypeError("producing_application_version must be str or None")
            if self.producing_application_version == "":
                raise ValueError("producing_application_version must not be empty")
        for name, value in (
            ("source_byte_count", self.source_byte_count),
            ("declared_atom_count", self.declared_atom_count),
            ("sampled_k_point_count", self.sampled_k_point_count),
            ("band_count", self.band_count),
            ("exit_status", self.exit_status),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in int excluding bool")
        if self.source_byte_count < 0:
            raise ValueError("source_byte_count must be nonnegative")
        self._require_vectors(self.direct_lattice_vectors, "direct lattice", exactly=3)
        self._require_vectors(
            self.reciprocal_lattice_vectors, "reciprocal lattice", exactly=3
        )
        self._require_vectors(self.k_points, "k-point")
        if type(self.species) is not tuple or not self.species:
            raise ValueError("species must be a nonempty tuple")
        species_names: list[str] = []
        for declaration in self.species:
            if type(declaration) is not tuple or len(declaration) != 3:
                raise TypeError("species declarations must be three-item tuples")
            name, mass, pseudo = declaration
            if type(name) is not str or type(pseudo) is not str:
                raise TypeError("species name and pseudopotential must be strings")
            if not name or not pseudo:
                raise ValueError("species name and pseudopotential must not be empty")
            self._require_finite(mass, "species mass")
            species_names.append(name)
        if len(set(species_names)) != len(species_names):
            raise ValueError("species names must be unique")
        if type(self.atoms) is not tuple:
            raise TypeError("atoms must be a tuple")
        for expected_index, atom in enumerate(self.atoms, start=1):
            if type(atom) is not tuple or len(atom) != 3:
                raise TypeError("atom declarations must be three-item tuples")
            index, species, position = atom
            if type(index) is not int or type(species) is not str:
                raise TypeError("atom index and species reference have invalid types")
            if index != expected_index:
                raise ValueError("atom indices must preserve contiguous source order")
            if species not in species_names:
                raise ValueError("atom has an unresolved species reference")
            self._require_vector(position, "atomic position")
        if self.declared_atom_count != len(self.atoms):
            raise ValueError("declared atom count disagrees with ordered atoms")
        if type(self.k_point_weights) is not tuple:
            raise TypeError("k_point_weights must be a tuple")
        for weight in self.k_point_weights:
            self._require_finite(weight, "k-point weight")
            if weight < 0:
                raise ValueError("k-point weights must be nonnegative")
        if len(self.k_points) != len(self.k_point_weights):
            raise ValueError("k-point and weight counts disagree")
        if self.sampled_k_point_count != len(self.k_points):
            raise ValueError("declared sampled-point count disagrees with k-points")
        if type(self.eigenvalues) is not tuple or len(self.eigenvalues) != len(
            self.k_points
        ):
            raise ValueError("spectrum and k-point counts disagree")
        for row in self.eigenvalues:
            self._require_spectrum_row(row, "eigenvalues")
            if len(row) != self.band_count:
                raise ValueError("eigenvalue rows have inconsistent fixed band counts")
        if self.occupations is not None:
            if type(self.occupations) is not tuple or len(self.occupations) != len(
                self.eigenvalues
            ):
                raise ValueError("occupation and eigenvalue shapes disagree")
            for eigenvalues, occupations in zip(
                self.eigenvalues, self.occupations, strict=True
            ):
                self._require_spectrum_row(occupations, "occupations")
                if len(occupations) != len(eigenvalues):
                    raise ValueError("occupation and eigenvalue shapes disagree")
        if self.spin_channels is not None:
            if type(self.spin_channels) is not tuple or not all(
                type(channel) is str and channel for channel in self.spin_channels
            ):
                raise TypeError("spin_channels must be a nonempty string tuple or None")
        self._require_finite(self.total_energy, "total energy")
        for name, grid in (
            ("fft_grid", self.fft_grid),
            ("fft_smooth", self.fft_smooth),
            ("fft_box", self.fft_box),
        ):
            if (
                type(grid) is not tuple
                or len(grid) != 3
                or any(
                    type(component) is not int or component <= 0 for component in grid
                )
            ):
                raise ValueError(f"{name} must contain three positive integers")
        if not 0 <= self.exit_status <= 255:
            raise ValueError(
                "exit_status must be in the represented process range 0..255"
            )

    @classmethod
    def _require_vectors(
        cls, vectors: object, name: str, *, exactly: int | None = None
    ) -> None:
        """Validate an immutable ordered vector collection without conversion."""
        if type(vectors) is not tuple:
            raise TypeError(f"{name} vectors must be a tuple")
        if exactly is not None and len(vectors) != exactly:
            raise ValueError(f"{name} must contain exactly {exactly} vectors")
        for vector in vectors:
            cls._require_vector(vector, name)

    @classmethod
    def _require_vector(cls, vector: object, name: str) -> None:
        """Validate one exact finite three-component tuple."""
        if type(vector) is not tuple or len(vector) != 3:
            raise ValueError(f"{name} vectors must have exactly three components")
        for component in vector:
            cls._require_finite(component, f"{name} component")

    @classmethod
    def _require_spectrum_row(cls, row: object, name: str) -> None:
        """Validate one immutable nonempty finite spectral row."""
        if type(row) is not tuple or not row:
            raise ValueError(f"{name} rows must be nonempty tuples")
        for value in row:
            cls._require_finite(value, f"{name} value")

    @staticmethod
    def _require_finite(value: object, name: str) -> None:
        """Validate an exact finite built-in float without numeric coercion."""
        if type(value) is not float:
            raise TypeError(f"{name} must be a built-in float")
        if not math.isfinite(value):
            raise ValueError(f"{name} must be finite")


@dataclass(frozen=True, slots=True)
class PeriodicCalculationRecord:
    """Immutable backend-neutral semantics for one periodic calculation observation.

    The record preserves source order and native QEXSD units.  Unavailable fields
    are typed reasons, never inferred placeholders.  Kohn--Sham eigenvalues are
    reported observations, not a complete many-body spectrum or a uniquely
    identified basis-independent operator.
    """

    schema_version: int
    source_path: str
    source_sha256: str
    source_byte_count: int
    qexsd_namespace: str
    qexsd_version: str
    producing_application: str
    producing_application_version: str | None
    direct_lattice_vectors: Vector3Sequence
    direct_lattice_unit: str
    direct_lattice_convention: str
    reciprocal_lattice_vectors: Vector3Sequence
    reciprocal_lattice_unit: str
    reciprocal_lattice_convention: str
    species: tuple[SpeciesDeclaration, ...]
    atoms: tuple[AtomDeclaration, ...]
    atom_count: int
    position_unit: str
    position_convention: str
    k_points: Vector3Sequence
    k_point_weights: tuple[float, ...]
    k_point_count: int
    k_point_convention: str
    eigenvalues: Spectrum
    occupations: Spectrum | None
    energy_unit: str
    band_count: int
    spin_channels: tuple[str, ...] | None
    total_energy: float
    total_energy_unit: str
    fft_grid: tuple[int, int, int]
    fft_smooth: tuple[int, int, int]
    fft_box: tuple[int, int, int]
    exit_status: int
    absolute_energy_reference: UnavailableReason
    fermi_alignment_convention: UnavailableReason
    retained_subspace: UnavailableReason
    gauge: UnavailableReason
    phase_convention: UnavailableReason
    basis_identity: UnavailableReason
    spin_convention: UnavailableReason

    def __post_init__(self) -> None:
        """Reapply complete semantic-record invariants after decoding."""
        if type(self.schema_version) is not int or self.schema_version != 1:
            raise ValueError("schema_version must be built-in integer 1")
        # Reuse the native record's public constructor as a complete independent
        # invariant oracle over represented fields; this performs no XML parsing.
        QexsdDocument(
            source_path=self.source_path,
            source_sha256=self.source_sha256,
            source_byte_count=self.source_byte_count,
            namespace=self.qexsd_namespace,
            qexsd_version=self.qexsd_version,
            producing_application=self.producing_application,
            producing_application_version=self.producing_application_version,
            declared_units=self.direct_lattice_unit,
            direct_lattice_vectors=self.direct_lattice_vectors,
            direct_lattice_unit=self.direct_lattice_unit,
            direct_lattice_convention=self.direct_lattice_convention,
            reciprocal_lattice_vectors=self.reciprocal_lattice_vectors,
            reciprocal_lattice_unit=self.reciprocal_lattice_unit,
            reciprocal_lattice_convention=self.reciprocal_lattice_convention,
            species=self.species,
            atoms=self.atoms,
            declared_atom_count=self.atom_count,
            position_unit=self.position_unit,
            position_convention=self.position_convention,
            k_points=self.k_points,
            k_point_weights=self.k_point_weights,
            sampled_k_point_count=self.k_point_count,
            k_point_convention=self.k_point_convention,
            eigenvalues=self.eigenvalues,
            occupations=self.occupations,
            energy_unit=self.energy_unit,
            band_count=self.band_count,
            spin_channels=self.spin_channels,
            total_energy=self.total_energy,
            total_energy_unit=self.total_energy_unit,
            fft_grid=self.fft_grid,
            fft_smooth=self.fft_smooth,
            fft_box=self.fft_box,
            exit_status=self.exit_status,
        )
        unavailable = (
            self.absolute_energy_reference,
            self.fermi_alignment_convention,
            self.retained_subspace,
            self.gauge,
            self.phase_convention,
            self.basis_identity,
            self.spin_convention,
        )
        if not all(isinstance(value, UnavailableReason) for value in unavailable):
            raise TypeError("unavailable semantic fields require UnavailableReason")
