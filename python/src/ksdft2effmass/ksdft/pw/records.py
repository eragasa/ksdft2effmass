"""Immutable plane-wave Kohn--Sham calculation records.

The complete record composes backend-neutral periodic geometry and Kohn--Sham
observations with plane-wave metadata and generic artifact provenance.  It has no
Quantum ESPRESSO or QEXSD dependency.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum
from pathlib import PurePosixPath
from typing import ClassVar

from ksdft2effmass.ksdft import (
    KohnShamSpectralObservations,
    TotalEnergyObservation,
)
from ksdft2effmass.periodic import KPointSampling, PeriodicStructure, ReciprocalLattice


class PlaneWaveMetadataAvailability(StrEnum):
    """Unavailable plane-wave metadata states demonstrated by the artifact."""

    NOT_REPRESENTED = "not_represented"
    NO_RETAINED_SUBSPACE = "no_retained_subspace"


@dataclass(frozen=True, slots=True)
class ArtifactProvenance:
    """Generic identity and producer metadata for one source artifact."""

    _SHA256: ClassVar[re.Pattern[str]] = re.compile(r"[0-9a-f]{64}\Z")

    source_path: str
    source_sha256: str
    source_byte_count: int
    source_format: str
    source_format_version: str
    producing_application: str
    producing_application_version: str | None
    transformation: str

    def __post_init__(self) -> None:
        if type(self.source_path) is not str:
            raise TypeError("source_path must be a built-in str")
        path = PurePosixPath(self.source_path)
        if (
            not self.source_path.startswith("/")
            or self.source_path.startswith("//")
            or str(path) != self.source_path
            or any(part in {"", ".", ".."} for part in path.parts[1:])
        ):
            raise ValueError("source_path must be a canonical absolute POSIX path")
        if (
            type(self.source_sha256) is not str
            or self._SHA256.fullmatch(self.source_sha256) is None
        ):
            raise ValueError("source_sha256 must be lowercase SHA-256")
        if type(self.source_byte_count) is not int or self.source_byte_count < 0:
            raise ValueError("source_byte_count must be a nonnegative built-in integer")
        for name in (
            "source_format",
            "source_format_version",
            "producing_application",
            "transformation",
        ):
            value = getattr(self, name)
            if type(value) is not str or not value:
                raise ValueError(f"{name} must be a nonempty built-in string")
        if self.producing_application_version is not None and (
            type(self.producing_application_version) is not str
            or not self.producing_application_version
        ):
            raise ValueError("producing_application_version must be nonempty or None")


@dataclass(frozen=True, slots=True)
class PlaneWaveRepresentationMetadata:
    """FFT grids and explicitly unavailable representation conventions."""

    representation: str
    fft_grid: tuple[int, int, int]
    fft_smooth: tuple[int, int, int]
    fft_box: tuple[int, int, int]
    basis_identity: PlaneWaveMetadataAvailability
    retained_subspace: PlaneWaveMetadataAvailability
    gauge: PlaneWaveMetadataAvailability
    phase_convention: PlaneWaveMetadataAvailability

    def __post_init__(self) -> None:
        if self.representation != "plane_wave":
            raise ValueError("representation must be plane_wave")
        for name in ("fft_grid", "fft_smooth", "fft_box"):
            grid = getattr(self, name)
            if (
                type(grid) is not tuple
                or len(grid) != 3
                or any(type(value) is not int or value <= 0 for value in grid)
            ):
                raise ValueError(f"{name} must contain three positive integers")
        if self.basis_identity is not PlaneWaveMetadataAvailability.NOT_REPRESENTED:
            raise ValueError("basis identity must be explicitly unavailable")
        if (
            self.retained_subspace
            is not PlaneWaveMetadataAvailability.NO_RETAINED_SUBSPACE
        ):
            raise ValueError("retained subspace must be explicitly unavailable")
        if self.gauge is not PlaneWaveMetadataAvailability.NOT_REPRESENTED:
            raise ValueError("gauge must be explicitly unavailable")
        if self.phase_convention is not PlaneWaveMetadataAvailability.NOT_REPRESENTED:
            raise ValueError("phase convention must be explicitly unavailable")


@dataclass(frozen=True, slots=True)
class KohnShamPlaneWaveCalculationRecord:
    """Complete immutable semantic observation of one plane-wave KS calculation.

    Attributes
    ----------
    schema_version
        Built-in integer ``1`` for the retained aggregate wire.
    structure
        Intrinsically valid periodic structure.
    reciprocal_lattice
        Intrinsically valid reciprocal-lattice representation.
    k_point_sampling
        Intrinsically valid ordered sampled k points.
    spectrum
        Representation-neutral Kohn--Sham spectral observations.
    total_energy
        Representation-neutral total-energy observation.
    plane_wave
        Plane-wave representation metadata.
    provenance
        Generic source-artifact identity and producer metadata.
    exit_status
        Built-in integer process status in the inclusive range 0 through 255.

    Notes
    -----
    Cross-object scale and sampled-point-count compatibility belongs to
    :class:`KohnShamPlaneWaveCalculationRecordValidator`.
    """

    schema_version: int
    structure: PeriodicStructure
    reciprocal_lattice: ReciprocalLattice
    k_point_sampling: KPointSampling
    spectrum: KohnShamSpectralObservations
    total_energy: TotalEnergyObservation
    plane_wave: PlaneWaveRepresentationMetadata
    provenance: ArtifactProvenance
    exit_status: int

    def __post_init__(self) -> None:
        if type(self.schema_version) is not int:
            raise TypeError("schema_version must be a built-in integer")
        if self.schema_version != 1:
            raise ValueError("schema_version must be 1")
        if not isinstance(self.structure, PeriodicStructure):
            raise TypeError("structure must be PeriodicStructure")
        if not isinstance(self.reciprocal_lattice, ReciprocalLattice):
            raise TypeError("reciprocal_lattice must be ReciprocalLattice")
        if not isinstance(self.k_point_sampling, KPointSampling):
            raise TypeError("k_point_sampling must be KPointSampling")
        if not isinstance(self.spectrum, KohnShamSpectralObservations):
            raise TypeError("spectrum must be KohnShamSpectralObservations")
        if not isinstance(self.total_energy, TotalEnergyObservation):
            raise TypeError("total_energy must be TotalEnergyObservation")
        if not isinstance(self.plane_wave, PlaneWaveRepresentationMetadata):
            raise TypeError("plane_wave must be PlaneWaveRepresentationMetadata")
        if not isinstance(self.provenance, ArtifactProvenance):
            raise TypeError("provenance must be ArtifactProvenance")
        if type(self.exit_status) is not int:
            raise TypeError("exit_status must be a built-in integer")
        if not 0 <= self.exit_status <= 255:
            raise ValueError("exit_status must be in 0..255")


class KohnShamPlaneWaveCalculationRecordValidator:
    """Validate compatibility among one aggregate record's domain objects.

    The immutable record owns only intrinsic field types and values. This
    ActionObject owns exact cross-object scale and sampled-point-count agreement.
    It performs no scientific acceptance or external execution.
    """

    __slots__ = ()

    def execute(self, record: KohnShamPlaneWaveCalculationRecord) -> None:
        """Raise when independently valid record components are incompatible.

        Parameters
        ----------
        record
            Complete plane-wave Kohn--Sham calculation record.

        Raises
        ------
        TypeError
            If ``record`` has the wrong semantic type.
        ValueError
            If reciprocal and k-point scales differ or the spectrum row count
            differs from the sampled k-point count.
        """
        if type(record) is not KohnShamPlaneWaveCalculationRecord:
            raise TypeError("record must be KohnShamPlaneWaveCalculationRecord")
        if record.k_point_sampling.scale_alat != record.reciprocal_lattice.scale_alat:
            raise ValueError("k-point and reciprocal-lattice scales must agree")
        if len(record.spectrum.eigenvalues) != len(
            record.k_point_sampling.raw_coordinates
        ):
            raise ValueError("spectrum and k-point counts must agree")
