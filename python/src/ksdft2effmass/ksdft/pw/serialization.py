"""Canonical closed JSON for plane-wave Kohn--Sham calculation records."""

from __future__ import annotations

import json
import math
from typing import Any, ClassVar

from ksdft2effmass.ksdft import (
    Availability,
    EnergyUnit,
    KohnShamSpectralObservations,
    TotalEnergyObservation,
)
from ksdft2effmass.periodic import (
    AtomicSpecies,
    CoordinateConvention,
    DirectLattice,
    InverseLengthUnit,
    KPointSampling,
    KPointWeightNormalization,
    LengthUnit,
    PeriodicSite,
    PeriodicStructure,
    PhysicalDimension,
    ReciprocalLattice,
    ReciprocalLatticeCompatibilityValidator,
    ReciprocalScaleConvention,
    UnitSystem,
)

from .records import (
    ArtifactProvenance,
    KohnShamPlaneWaveCalculationRecord,
    KohnShamPlaneWaveCalculationRecordValidator,
    PlaneWaveMetadataAvailability,
    PlaneWaveRepresentationMetadata,
)


class KohnShamPlaneWaveCalculationRecordJsonSerializer:
    """Serialize and reconstruct a closed schema-version-1 record.

    Parameters
    ----------
    duality_absolute_tolerance
        Positive finite built-in float used for direct--reciprocal compatibility.
        It must equal the tolerance represented by an input wire. Booleans,
        numeric strings, NumPy scalars, and nonfinite values are rejected.

    Notes
    -----
    The serializer owns direct--reciprocal compatibility policy. The configured
    tolerance is emitted during serialization and must match the wire during
    deserialization, making every accepted record round-trip without tolerance
    loss. The tolerance is operation policy, not intrinsic
    :class:`~ksdft2effmass.periodic.ReciprocalLattice` state.
    """

    SCHEMA_VERSION: ClassVar[int] = 1
    DUALITY_ABSOLUTE_TOLERANCE: ClassVar[float] = 1.0e-12
    __slots__ = ("duality_absolute_tolerance",)

    def __init__(self, duality_absolute_tolerance: float = 1.0e-12) -> None:
        if type(duality_absolute_tolerance) is not float:
            raise TypeError("duality_absolute_tolerance must be a built-in float")
        if (
            not math.isfinite(duality_absolute_tolerance)
            or duality_absolute_tolerance <= 0
        ):
            raise ValueError("duality_absolute_tolerance must be positive and finite")
        self.duality_absolute_tolerance = duality_absolute_tolerance

    def serialize(self, record: KohnShamPlaneWaveCalculationRecord) -> str:
        """Return canonical JSON after validating lattice compatibility.

        Parameters
        ----------
        record
            Complete schema-version-1 plane-wave Kohn--Sham record.

        Returns
        -------
        str
            Sorted, compact JSON with exactly one final line feed.

        Raises
        ------
        TypeError
            If ``record`` has the wrong semantic type.
        ValueError
            If its direct and reciprocal lattices exceed the configured tolerance,
            reciprocal and k-point scales differ, or sampled-point and spectrum
            counts differ.
        """
        if not isinstance(record, KohnShamPlaneWaveCalculationRecord):
            raise TypeError("record must be KohnShamPlaneWaveCalculationRecord")
        payload = self._payload(record)
        return (
            json.dumps(
                payload,
                allow_nan=False,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            )
            + "\n"
        )

    def deserialize(self, text: str) -> KohnShamPlaneWaveCalculationRecord:
        """Strictly reconstruct a compatible schema-version-1 record.

        Parameters
        ----------
        text
            JSON text whose represented tolerance must equal this serializer's
            configured ``duality_absolute_tolerance``.

        Returns
        -------
        KohnShamPlaneWaveCalculationRecord
            Immutable reconstructed record.

        Raises
        ------
        TypeError
            If ``text`` or a represented field has the wrong semantic type.
        ValueError
            If JSON is malformed, fields are unknown or duplicated, a value
            violates its invariant, the wire tolerance differs from the configured
            policy, or the represented lattices are incompatible.
        """
        if type(text) is not str:
            raise TypeError("text must be a built-in str")
        if text.startswith("\ufeff"):
            raise ValueError("a JSON byte-order mark is prohibited")
        try:
            payload = json.loads(
                text,
                object_pairs_hook=self._unique_object,
                parse_constant=self._reject_constant,
            )
        except json.JSONDecodeError as error:
            raise ValueError("malformed plane-wave calculation record JSON") from error
        root = self._object(
            payload,
            "record",
            {
                "schema_version",
                "structure",
                "reciprocal_lattice",
                "k_point_sampling",
                "spectrum",
                "total_energy",
                "plane_wave",
                "provenance",
                "exit_status",
            },
        )
        if type(root["schema_version"]) is not int or root["schema_version"] != 1:
            raise ValueError("unsupported schema_version")
        structure_obj = self._object(
            root["structure"], "structure", {"direct_lattice", "species", "sites"}
        )
        direct = self._direct_lattice(structure_obj["direct_lattice"])
        species_values = self._list(structure_obj["species"], "species")
        species = tuple(self._species(item) for item in species_values)
        site_values = self._list(structure_obj["sites"], "sites")
        sites = tuple(self._site(item) for item in site_values)
        structure = PeriodicStructure(
            direct_lattice=direct, species=species, sites=sites
        )
        reciprocal = self._reciprocal(root["reciprocal_lattice"], direct)
        k_points = self._k_points(root["k_point_sampling"])
        spectrum = self._spectrum(root["spectrum"])
        total_energy = self._total_energy(root["total_energy"])
        plane_wave = self._plane_wave(root["plane_wave"])
        provenance = self._provenance(root["provenance"])
        record = KohnShamPlaneWaveCalculationRecord(
            schema_version=1,
            structure=structure,
            reciprocal_lattice=reciprocal,
            k_point_sampling=k_points,
            spectrum=spectrum,
            total_energy=total_energy,
            plane_wave=plane_wave,
            provenance=provenance,
            exit_status=self._integer(root["exit_status"], "exit_status"),
        )
        KohnShamPlaneWaveCalculationRecordValidator().execute(record)
        return record

    def _payload(
        self, record: KohnShamPlaneWaveCalculationRecord
    ) -> dict[str, Any]:
        KohnShamPlaneWaveCalculationRecordValidator().execute(record)
        direct = record.structure.direct_lattice
        reciprocal = record.reciprocal_lattice
        ReciprocalLatticeCompatibilityValidator().execute(
            direct,
            reciprocal,
            absolute_tolerance=self.duality_absolute_tolerance,
        )
        points = record.k_point_sampling
        spectrum = record.spectrum
        energy = record.total_energy
        plane = record.plane_wave
        provenance = record.provenance
        return {
            "schema_version": record.schema_version,
            "structure": {
                "direct_lattice": {
                    "vectors": direct.vectors,
                    "unit_system": direct.unit_system.value,
                    "dimension": direct.dimension.value,
                    "unit": direct.unit.value,
                    "coordinate_convention": direct.coordinate_convention.value,
                    "vector_order": direct.vector_order,
                },
                "species": [
                    {
                        "name": item.name,
                        "mass": item.mass,
                        "mass_dimension": item.mass_dimension.value,
                        "mass_unit": item.mass_unit,
                        "pseudopotential_label": item.pseudopotential_label,
                    }
                    for item in record.structure.species
                ],
                "sites": [
                    {
                        "index": item.index,
                        "species_name": item.species_name,
                        "coordinates": item.coordinates,
                        "coordinate_convention": item.coordinate_convention.value,
                        "coordinate_dimension": item.coordinate_dimension.value,
                        "coordinate_unit": item.coordinate_unit.value,
                    }
                    for item in record.structure.sites
                ],
            },
            "reciprocal_lattice": {
                "raw_coefficients": reciprocal.raw_coefficients,
                "raw_dimension": reciprocal.raw_dimension.value,
                "raw_coordinate_convention": reciprocal.raw_coordinate_convention.value,
                "scale_convention": reciprocal.scale_convention.value,
                "scale_alat": reciprocal.scale_alat,
                "scale_alat_unit": reciprocal.scale_alat_unit.value,
                "incorporates_two_pi": reciprocal.incorporates_two_pi,
                "physical_vectors": reciprocal.physical_vectors,
                "physical_dimension": reciprocal.physical_dimension.value,
                "physical_unit": reciprocal.physical_unit.value,
                "physical_coordinate_convention": (
                    reciprocal.physical_coordinate_convention.value
                ),
                "duality_absolute_tolerance": self.duality_absolute_tolerance,
            },
            "k_point_sampling": {
                "raw_coordinates": points.raw_coordinates,
                "raw_dimension": points.raw_dimension.value,
                "coordinate_convention": points.coordinate_convention.value,
                "scale_convention": points.scale_convention.value,
                "scale_alat": points.scale_alat,
                "scale_alat_unit": points.scale_alat_unit.value,
                "incorporates_two_pi": points.incorporates_two_pi,
                "physical_coordinates": points.physical_coordinates,
                "physical_dimension": points.physical_dimension.value,
                "physical_unit": points.physical_unit.value,
                "weights": points.weights,
                "weight_normalization": points.weight_normalization.value,
            },
            "spectrum": {
                "eigenvalues": spectrum.eigenvalues,
                "eigenvalue_unit": spectrum.eigenvalue_unit.value,
                "occupations": spectrum.occupations,
                "band_count": spectrum.band_count,
                "spin_channel_availability": spectrum.spin_channel_availability.value,
                "energy_reference_availability": (
                    spectrum.energy_reference_availability.value
                ),
            },
            "total_energy": {
                "value": energy.value,
                "unit": energy.unit.value,
                "reference_availability": energy.reference_availability.value,
            },
            "plane_wave": {
                "representation": plane.representation,
                "fft_grid": plane.fft_grid,
                "fft_smooth": plane.fft_smooth,
                "fft_box": plane.fft_box,
                "basis_identity": plane.basis_identity.value,
                "retained_subspace": plane.retained_subspace.value,
                "gauge": plane.gauge.value,
                "phase_convention": plane.phase_convention.value,
            },
            "provenance": {
                "source_path": provenance.source_path,
                "source_sha256": provenance.source_sha256,
                "source_byte_count": provenance.source_byte_count,
                "source_format": provenance.source_format,
                "source_format_version": provenance.source_format_version,
                "producing_application": provenance.producing_application,
                "producing_application_version": (
                    provenance.producing_application_version
                ),
                "transformation": provenance.transformation,
            },
            "exit_status": record.exit_status,
        }

    @classmethod
    def _direct_lattice(cls, value: Any) -> DirectLattice:
        obj = cls._object(
            value,
            "direct_lattice",
            {
                "vectors",
                "unit_system",
                "dimension",
                "unit",
                "coordinate_convention",
                "vector_order",
            },
        )
        return DirectLattice(
            cls._vectors(obj["vectors"], "direct vectors"),
            UnitSystem(cls._string(obj["unit_system"], "unit_system")),
            PhysicalDimension(cls._string(obj["dimension"], "dimension")),
            LengthUnit(cls._string(obj["unit"], "unit")),
            CoordinateConvention(
                cls._string(obj["coordinate_convention"], "coordinate_convention")
            ),
            cls._string(obj["vector_order"], "vector_order"),
        )

    @classmethod
    def _species(cls, value: Any) -> AtomicSpecies:
        obj = cls._object(
            value,
            "species",
            {"name", "mass", "mass_dimension", "mass_unit", "pseudopotential_label"},
        )
        return AtomicSpecies(
            cls._string(obj["name"], "name"),
            cls._real(obj["mass"], "mass"),
            PhysicalDimension(cls._string(obj["mass_dimension"], "mass_dimension")),
            cls._string(obj["mass_unit"], "mass_unit"),
            cls._string(obj["pseudopotential_label"], "pseudopotential_label"),
        )

    @classmethod
    def _site(cls, value: Any) -> PeriodicSite:
        obj = cls._object(
            value,
            "site",
            {
                "index",
                "species_name",
                "coordinates",
                "coordinate_convention",
                "coordinate_dimension",
                "coordinate_unit",
            },
        )
        return PeriodicSite(
            cls._integer(obj["index"], "index"),
            cls._string(obj["species_name"], "species_name"),
            cls._vector(obj["coordinates"], "coordinates"),
            CoordinateConvention(
                cls._string(obj["coordinate_convention"], "coordinate_convention")
            ),
            PhysicalDimension(
                cls._string(obj["coordinate_dimension"], "coordinate_dimension")
            ),
            LengthUnit(cls._string(obj["coordinate_unit"], "coordinate_unit")),
        )

    def _reciprocal(self, value: Any, direct: DirectLattice) -> ReciprocalLattice:
        cls = type(self)
        names = {
            "raw_coefficients",
            "raw_dimension",
            "raw_coordinate_convention",
            "scale_convention",
            "scale_alat",
            "scale_alat_unit",
            "incorporates_two_pi",
            "physical_vectors",
            "physical_dimension",
            "physical_unit",
            "physical_coordinate_convention",
            "duality_absolute_tolerance",
        }
        obj = cls._object(value, "reciprocal_lattice", names)
        if type(obj["incorporates_two_pi"]) is not bool:
            raise TypeError("incorporates_two_pi must be JSON boolean")
        reciprocal = ReciprocalLattice(
            cls._vectors(obj["raw_coefficients"], "raw_coefficients"),
            PhysicalDimension(cls._string(obj["raw_dimension"], "raw_dimension")),
            CoordinateConvention(
                cls._string(
                    obj["raw_coordinate_convention"], "raw_coordinate_convention"
                )
            ),
            ReciprocalScaleConvention(
                cls._string(obj["scale_convention"], "scale_convention")
            ),
            cls._real(obj["scale_alat"], "scale_alat"),
            LengthUnit(cls._string(obj["scale_alat_unit"], "scale_alat_unit")),
            obj["incorporates_two_pi"],
            cls._vectors(obj["physical_vectors"], "physical_vectors"),
            PhysicalDimension(
                cls._string(obj["physical_dimension"], "physical_dimension")
            ),
            InverseLengthUnit(cls._string(obj["physical_unit"], "physical_unit")),
            CoordinateConvention(
                cls._string(
                    obj["physical_coordinate_convention"],
                    "physical_coordinate_convention",
                )
            ),
        )
        tolerance = cls._real(
            obj["duality_absolute_tolerance"], "duality_absolute_tolerance"
        )
        if tolerance != self.duality_absolute_tolerance:
            raise ValueError(
                "wire duality_absolute_tolerance disagrees with serializer policy"
            )
        ReciprocalLatticeCompatibilityValidator().execute(
            direct,
            reciprocal,
            absolute_tolerance=self.duality_absolute_tolerance,
        )
        return reciprocal

    @classmethod
    def _k_points(cls, value: Any) -> KPointSampling:
        names = {
            "raw_coordinates",
            "raw_dimension",
            "coordinate_convention",
            "scale_convention",
            "scale_alat",
            "scale_alat_unit",
            "incorporates_two_pi",
            "physical_coordinates",
            "physical_dimension",
            "physical_unit",
            "weights",
            "weight_normalization",
        }
        obj = cls._object(value, "k_point_sampling", names)
        if type(obj["incorporates_two_pi"]) is not bool:
            raise TypeError("incorporates_two_pi must be JSON boolean")
        return KPointSampling(
            cls._vectors(obj["raw_coordinates"], "raw_coordinates"),
            PhysicalDimension(cls._string(obj["raw_dimension"], "raw_dimension")),
            CoordinateConvention(
                cls._string(obj["coordinate_convention"], "coordinate_convention")
            ),
            ReciprocalScaleConvention(
                cls._string(obj["scale_convention"], "scale_convention")
            ),
            cls._real(obj["scale_alat"], "scale_alat"),
            LengthUnit(cls._string(obj["scale_alat_unit"], "scale_alat_unit")),
            obj["incorporates_two_pi"],
            cls._vectors(obj["physical_coordinates"], "physical_coordinates"),
            PhysicalDimension(
                cls._string(obj["physical_dimension"], "physical_dimension")
            ),
            InverseLengthUnit(cls._string(obj["physical_unit"], "physical_unit")),
            cls._real_row(obj["weights"], "weights"),
            KPointWeightNormalization(
                cls._string(obj["weight_normalization"], "weight_normalization")
            ),
        )

    @classmethod
    def _spectrum(cls, value: Any) -> KohnShamSpectralObservations:
        obj = cls._object(
            value,
            "spectrum",
            {
                "eigenvalues",
                "eigenvalue_unit",
                "occupations",
                "band_count",
                "spin_channel_availability",
                "energy_reference_availability",
            },
        )
        occupations = (
            None
            if obj["occupations"] is None
            else cls._spectrum_rows(obj["occupations"], "occupations")
        )
        return KohnShamSpectralObservations(
            cls._spectrum_rows(obj["eigenvalues"], "eigenvalues"),
            EnergyUnit(cls._string(obj["eigenvalue_unit"], "eigenvalue_unit")),
            occupations,
            cls._integer(obj["band_count"], "band_count"),
            Availability(
                cls._string(
                    obj["spin_channel_availability"], "spin_channel_availability"
                )
            ),
            Availability(
                cls._string(
                    obj["energy_reference_availability"],
                    "energy_reference_availability",
                )
            ),
        )

    @classmethod
    def _total_energy(cls, value: Any) -> TotalEnergyObservation:
        obj = cls._object(
            value, "total_energy", {"value", "unit", "reference_availability"}
        )
        return TotalEnergyObservation(
            cls._real(obj["value"], "value"),
            EnergyUnit(cls._string(obj["unit"], "unit")),
            Availability(
                cls._string(obj["reference_availability"], "reference_availability")
            ),
        )

    @classmethod
    def _plane_wave(cls, value: Any) -> PlaneWaveRepresentationMetadata:
        obj = cls._object(
            value,
            "plane_wave",
            {
                "representation",
                "fft_grid",
                "fft_smooth",
                "fft_box",
                "basis_identity",
                "retained_subspace",
                "gauge",
                "phase_convention",
            },
        )
        return PlaneWaveRepresentationMetadata(
            cls._string(obj["representation"], "representation"),
            cls._grid(obj["fft_grid"], "fft_grid"),
            cls._grid(obj["fft_smooth"], "fft_smooth"),
            cls._grid(obj["fft_box"], "fft_box"),
            PlaneWaveMetadataAvailability(
                cls._string(obj["basis_identity"], "basis_identity")
            ),
            PlaneWaveMetadataAvailability(
                cls._string(obj["retained_subspace"], "retained_subspace")
            ),
            PlaneWaveMetadataAvailability(cls._string(obj["gauge"], "gauge")),
            PlaneWaveMetadataAvailability(
                cls._string(obj["phase_convention"], "phase_convention")
            ),
        )

    @classmethod
    def _provenance(cls, value: Any) -> ArtifactProvenance:
        obj = cls._object(
            value,
            "provenance",
            {
                "source_path",
                "source_sha256",
                "source_byte_count",
                "source_format",
                "source_format_version",
                "producing_application",
                "producing_application_version",
                "transformation",
            },
        )
        version = obj["producing_application_version"]
        if version is not None:
            version = cls._string(version, "producing_application_version")
        return ArtifactProvenance(
            cls._string(obj["source_path"], "source_path"),
            cls._string(obj["source_sha256"], "source_sha256"),
            cls._integer(obj["source_byte_count"], "source_byte_count"),
            cls._string(obj["source_format"], "source_format"),
            cls._string(obj["source_format_version"], "source_format_version"),
            cls._string(obj["producing_application"], "producing_application"),
            version,
            cls._string(obj["transformation"], "transformation"),
        )

    @staticmethod
    def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON object key: {key!r}")
            result[key] = value
        return result

    @staticmethod
    def _reject_constant(value: str) -> None:
        raise ValueError(f"nonfinite JSON constant is prohibited: {value}")

    @staticmethod
    def _object(value: Any, context: str, fields: set[str]) -> dict[str, Any]:
        if type(value) is not dict:
            raise TypeError(f"{context} must be a JSON object")
        missing, unknown = fields - set(value), set(value) - fields
        if missing or unknown:
            raise ValueError(
                f"{context} fields disagree; missing={sorted(missing)}, "
                f"unknown={sorted(unknown)}"
            )
        return value

    @staticmethod
    def _list(value: Any, context: str) -> list[Any]:
        if type(value) is not list:
            raise TypeError(f"{context} must be a JSON array")
        return value

    @staticmethod
    def _string(value: Any, context: str) -> str:
        if type(value) is not str:
            raise TypeError(f"{context} must be a JSON string")
        return value

    @staticmethod
    def _integer(value: Any, context: str) -> int:
        if type(value) is not int:
            raise TypeError(f"{context} must be a JSON integer")
        return value

    @staticmethod
    def _real(value: Any, context: str) -> float:
        if type(value) not in (int, float):
            raise TypeError(f"{context} must be a JSON real number")
        result = float(value)
        if not math.isfinite(result):
            raise ValueError(f"{context} must be finite")
        return result

    @classmethod
    def _real_row(cls, value: Any, context: str) -> tuple[float, ...]:
        return tuple(cls._real(item, context) for item in cls._list(value, context))

    @classmethod
    def _vector(cls, value: Any, context: str) -> tuple[float, float, float]:
        row = cls._real_row(value, context)
        if len(row) != 3:
            raise ValueError(f"{context} must contain three components")
        return row[0], row[1], row[2]

    @classmethod
    def _vectors(
        cls, value: Any, context: str
    ) -> tuple[tuple[float, float, float], ...]:
        return tuple(cls._vector(item, context) for item in cls._list(value, context))

    @classmethod
    def _spectrum_rows(cls, value: Any, context: str) -> tuple[tuple[float, ...], ...]:
        return tuple(cls._real_row(item, context) for item in cls._list(value, context))

    @classmethod
    def _grid(cls, value: Any, context: str) -> tuple[int, int, int]:
        values = cls._list(value, context)
        if len(values) != 3 or any(type(item) is not int for item in values):
            raise TypeError(f"{context} must contain three JSON integers")
        return values[0], values[1], values[2]
