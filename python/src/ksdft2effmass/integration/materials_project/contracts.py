"""Typed Materials Project structure retrieval and canonical adaptation.

The integration owns the external MPRester boundary. Returned mutable pymatgen
structures are copied immediately into immutable project-owned periodic records using
the canonical LAMMPS ``metal`` unit inventory. Materials Project geometry remains
external reference data and does not select a production DFT lattice constant.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from pymatgen.core import Structure

from ksdft2effmass.structures import (
    AtomicSpecies,
    CoordinateConvention,
    DirectLattice,
    LengthUnit,
    PeriodicSite,
    PeriodicStructure,
    PhysicalDimension,
    UnitSystem,
)
from ksdft2effmass.units import (
    MetalQuantityConverter,
    MetalUnitConversionRequest,
    MetalUnitConversionSourceCorrelation,
    MetalUnitConversionSuccess,
    UnitIdentity,
    UnitScalar,
)

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)

__all__ = [
    "MaterialsProjectClient",
    "MaterialsProjectStructureAdapter",
    "MaterialsProjectStructureJsonSerializer",
    "MaterialsProjectStructureReference",
    "MaterialsProjectStructureRequest",
    "MaterialsProjectStructureRetriever",
]


@runtime_checkable
class MaterialsProjectClient(Protocol):
    """Minimum MPRester behavior required by this integration."""

    def get_structure_by_material_id(
        self,
        material_id: str,
        final: bool = True,
        conventional_unit_cell: bool = False,
    ) -> Structure | list[Structure]:
        """Return one final structure for an explicit Materials Project identity."""
        ...


@dataclass(frozen=True, slots=True)
class MaterialsProjectStructureRequest:
    """One explicit Materials Project structure request."""

    material_id: str
    conventional_unit_cell: bool = False

    def __post_init__(self) -> None:
        if type(self.material_id) is not str:
            raise TypeError("material_id must be str")
        if re.fullmatch(r"mp-[1-9][0-9]*", self.material_id) is None:
            raise ValueError("material_id must have canonical mp-N form")
        if type(self.conventional_unit_cell) is not bool:
            raise TypeError("conventional_unit_cell must be bool")


@dataclass(frozen=True, slots=True)
class MaterialsProjectStructureReference:
    """Canonical immutable snapshot of one externally sourced MP structure."""

    material_id: str
    source_url: str
    database_name: str
    geometry_status: str
    structure: PeriodicStructure
    mass_conversions: tuple[MetalUnitConversionSuccess, ...]

    def __post_init__(self) -> None:
        MaterialsProjectStructureRequest(self.material_id)
        for name, text in (
            ("source_url", self.source_url),
            ("database_name", self.database_name),
            ("geometry_status", self.geometry_status),
        ):
            if type(text) is not str:
                raise TypeError(f"{name} must be str")
            if not text:
                raise ValueError(f"{name} must be nonempty")
        if type(self.structure) is not PeriodicStructure:
            raise TypeError("structure must be PeriodicStructure")
        if self.structure.direct_lattice.unit_system is not UnitSystem.METAL:
            raise ValueError("Materials Project structure must use metal units")
        if type(self.mass_conversions) is not tuple or any(
            type(value) is not MetalUnitConversionSuccess
            for value in self.mass_conversions
        ):
            raise TypeError("mass_conversions must contain conversion successes")
        if len(self.mass_conversions) != len(self.structure.species):
            raise ValueError("each species must retain one mass conversion")
        if any(
            conversion.output.value != species.mass
            or conversion.output.unit is not UnitIdentity.GRAM_PER_MOLE
            for species, conversion in zip(
                self.structure.species, self.mass_conversions, strict=True
            )
        ):
            raise ValueError("species masses must match retained conversions")


@dataclass(frozen=True, slots=True)
class MaterialsProjectStructureAdapter:
    """Copy one pymatgen structure into canonical immutable project records."""

    def execute(
        self, material_id: str, source: Structure
    ) -> MaterialsProjectStructureReference:
        """Return a canonical snapshot without retaining the mutable source object."""
        request = MaterialsProjectStructureRequest(material_id)
        if type(source) is not Structure:
            raise TypeError("source must be pymatgen Structure")
        species_by_name: dict[str, AtomicSpecies] = {}
        mass_conversions: list[MetalUnitConversionSuccess] = []
        sites: list[PeriodicSite] = []
        converter = MetalQuantityConverter()
        for index, source_site in enumerate(source, start=1):
            if not source_site.is_ordered:
                raise ValueError("disordered Materials Project sites are unsupported")
            symbol = source_site.specie.symbol
            if symbol not in species_by_name:
                conversion = converter.convert(
                    MetalUnitConversionRequest(
                        UnitScalar(
                            float(source_site.specie.atomic_mass),
                            UnitIdentity.UNIFIED_ATOMIC_MASS_UNIT,
                        ),
                        UnitIdentity.GRAM_PER_MOLE,
                        MetalUnitConversionSourceCorrelation(
                            result_identity=(
                                f"materials-project:{request.material_id}:"
                                "final-structure"
                            )
                        ),
                    )
                )
                if type(conversion) is not MetalUnitConversionSuccess:
                    raise ValueError("species mass conversion must succeed")
                mass_conversions.append(conversion)
                species_by_name[symbol] = AtomicSpecies(
                    name=symbol,
                    mass=conversion.output.value,
                    mass_dimension=PhysicalDimension.MASS,
                    mass_unit=UnitIdentity.GRAM_PER_MOLE.value,
                    pseudopotential_label=None,
                )
            source_coordinates = source_site.coords
            if len(source_coordinates) != 3:
                raise ValueError(
                    "pymatgen Cartesian coordinates must have length three"
                )
            coordinates = (
                float(source_coordinates[0]),
                float(source_coordinates[1]),
                float(source_coordinates[2]),
            )
            sites.append(
                PeriodicSite(
                    index=index,
                    species_name=symbol,
                    coordinates=coordinates,
                    coordinate_convention=CoordinateConvention.CARTESIAN,
                    coordinate_dimension=PhysicalDimension.LENGTH,
                    coordinate_unit=LengthUnit.ANGSTROM,
                )
            )
        matrix = source.lattice.matrix
        if matrix.shape != (3, 3):
            raise ValueError("pymatgen lattice matrix must be three by three")
        lattice_vectors = (
            (float(matrix[0, 0]), float(matrix[0, 1]), float(matrix[0, 2])),
            (float(matrix[1, 0]), float(matrix[1, 1]), float(matrix[1, 2])),
            (float(matrix[2, 0]), float(matrix[2, 1]), float(matrix[2, 2])),
        )
        structure = PeriodicStructure(
            direct_lattice=DirectLattice(
                vectors=lattice_vectors,
                unit_system=UnitSystem.METAL,
                dimension=PhysicalDimension.LENGTH,
                unit=LengthUnit.ANGSTROM,
                coordinate_convention=CoordinateConvention.CARTESIAN,
                vector_order="pymatgen_lattice_matrix_row_order",
            ),
            species=tuple(species_by_name.values()),
            sites=tuple(sites),
        )
        return MaterialsProjectStructureReference(
            material_id=request.material_id,
            source_url=f"https://materialsproject.org/materials/{request.material_id}",
            database_name="Materials Project",
            geometry_status=("external_reference_not_production_pbe_relaxed_lattice"),
            structure=structure,
            mass_conversions=tuple(mass_conversions),
        )


@dataclass(frozen=True, slots=True)
class MaterialsProjectStructureRetriever:
    """Retrieve one explicit structure through an injected MPRester client."""

    def execute(
        self,
        client: MaterialsProjectClient,
        request: MaterialsProjectStructureRequest,
    ) -> MaterialsProjectStructureReference:
        """Retrieve the final MP structure and canonicalize it immediately."""
        if not isinstance(client, MaterialsProjectClient):
            raise TypeError("client must implement MaterialsProjectClient")
        if type(request) is not MaterialsProjectStructureRequest:
            raise TypeError("request must be MaterialsProjectStructureRequest")
        source = client.get_structure_by_material_id(
            request.material_id,
            final=True,
            conventional_unit_cell=request.conventional_unit_cell,
        )
        if type(source) is not Structure:
            raise ValueError("MPRester must return exactly one final Structure")
        return MaterialsProjectStructureAdapter().execute(request.material_id, source)


@dataclass(frozen=True, slots=True)
class MaterialsProjectStructureJsonSerializer:
    """Serialize one canonical MP structure reference to stable JSON bytes."""

    def execute(self, value: MaterialsProjectStructureReference) -> bytes:
        """Return canonical JSON without exposing credentials or mutable objects."""
        if type(value) is not MaterialsProjectStructureReference:
            raise TypeError("value must be MaterialsProjectStructureReference")
        structure = value.structure
        payload = {
            "record_version": 1,
            "source": {
                "database": value.database_name,
                "material_id": value.material_id,
                "url": value.source_url,
            },
            "geometry_status": value.geometry_status,
            "unit_system": structure.direct_lattice.unit_system.value,
            "direct_lattice": {
                "vectors": [
                    list(vector) for vector in structure.direct_lattice.vectors
                ],
                "unit": structure.direct_lattice.unit.value,
                "coordinate_convention": (
                    structure.direct_lattice.coordinate_convention.value
                ),
                "vector_order": structure.direct_lattice.vector_order,
            },
            "species": [
                {
                    "name": item.name,
                    "mass": item.mass,
                    "mass_unit": item.mass_unit,
                    "mass_conversion": self._conversion(conversion),
                }
                for item, conversion in zip(
                    structure.species, value.mass_conversions, strict=True
                )
            ],
            "sites": [
                {
                    "index": site.index,
                    "species_name": site.species_name,
                    "coordinates": list(site.coordinates),
                    "coordinate_unit": site.coordinate_unit.value,
                    "coordinate_convention": site.coordinate_convention.value,
                }
                for site in structure.sites
            ],
        }
        return (
            json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n"
        ).encode("utf-8")

    @staticmethod
    def _conversion(value: MetalUnitConversionSuccess) -> dict[str, JsonValue]:
        """Return complete maintained mass-conversion provenance."""
        definition = value.definition
        correlation = value.request.source_correlation
        authority = definition.authority
        return {
            "source": {
                "value": value.request.source.value,
                "unit": value.request.source.unit.value,
            },
            "target_unit": value.request.target_unit.value,
            "output": {"value": value.output.value, "unit": value.output.unit.value},
            "source_correlation": {
                "artifact_identity": (
                    None if correlation is None else correlation.artifact_identity
                ),
                "result_identity": (
                    None if correlation is None else correlation.result_identity
                ),
                "provenance_identity": (
                    None if correlation is None else correlation.provenance_identity
                ),
                "content_identity": (
                    None
                    if correlation is None or correlation.content_identity is None
                    else correlation.content_identity.value
                ),
            },
            "definition": {
                "identity": definition.identity,
                "version": definition.version,
                "content_identity": definition.content_identity.value,
                "decimal_scale": str(definition.decimal_scale),
                "standard_uncertainty": str(definition.standard_uncertainty),
                "numerical_policy": {
                    "identity": definition.numerical_policy.identity,
                    "version": definition.numerical_policy.version,
                },
                "implementation_identity": definition.implementation_identity,
                "authority": [
                    {
                        "identity": item.identity,
                        "version": item.version,
                        "url": item.url,
                        "content_identity": item.content_identity.value,
                        "doi": item.doi,
                    }
                    for item in (
                        authority.lammps_units_document,
                        authority.nist_codata_adjustment,
                        authority.bipm_si_brochure,
                    )
                ],
            },
            "catalog": {
                "identity": value.catalog_identity,
                "version": value.catalog_version,
                "content_identity": value.catalog_content_identity.value,
            },
            "limitations": [item.value for item in value.limitations],
        }
