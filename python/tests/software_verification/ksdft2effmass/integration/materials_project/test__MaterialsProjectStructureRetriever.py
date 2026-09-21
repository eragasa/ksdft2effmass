r"""Software verification of ``MaterialsProjectStructureRetriever``.

Evidence profile: claim_bearing

Bounded artifact scope: explicit material-identity requests, injected MPRester client
calls, immediate immutable canonical adaptation, conversion provenance, stable JSON,
and rejection of disordered sites.

Facet and represented meaning

The module verifies the public retriever's boundary from one explicit external
structure response to one project-owned LAMMPS-metal-unit reference record.

Intrinsic and cross-object scope

``MaterialsProjectStructureRetriever`` is the sole system under test. It composes the
public request, adapter, serializer, unit converter, and periodic records without
reproducing their algorithms.

VVUQ and scientific exclusions

The tests use local synthetic pymatgen structures and an injected client. They perform
no network request and establish no scientific validity for Materials Project data, no
production silicon lattice constant, and no Quantum ESPRESSO execution authority.
"""

from __future__ import annotations

from dataclasses import dataclass

import pytest
from pymatgen.core import Lattice, Structure

from ksdft2effmass.integration.materials_project import (
    MaterialsProjectStructureJsonSerializer,
    MaterialsProjectStructureRequest,
    MaterialsProjectStructureRetriever,
)
from ksdft2effmass.structures import LengthUnit, UnitSystem

pytestmark = pytest.mark.software_verification
SUT = MaterialsProjectStructureRetriever


class TestMaterialsProjectStructureRetriever:
    """Own software evidence for retrieval and immediate canonical adaptation."""

    @dataclass(slots=True)
    class StubClient:
        """Provide one local structure through the exact required client protocol."""

        structure: Structure
        requested_material_id: str | None = None
        requested_final: bool | None = None
        requested_conventional: bool | None = None

        def get_structure_by_material_id(
            self,
            material_id: str,
            final: bool = True,
            conventional_unit_cell: bool = False,
        ) -> Structure | list[Structure]:
            """Record the explicit query and return the configured structure."""
            self.requested_material_id = material_id
            self.requested_final = final
            self.requested_conventional = conventional_unit_cell
            return self.structure

    @staticmethod
    def silicon_structure() -> Structure:
        """Return a local ordered two-site illustrative silicon structure."""
        return Structure(
            Lattice.cubic(5.43),
            ("Si", "Si"),
            ((0.0, 0.0, 0.0), (0.25, 0.25, 0.25)),
        )

    def test_method__execute__returns_immutable_metal_unit_snapshot(self) -> None:
        """Evidence ID: SV-MATERIALS-PROJECT-STRUCTURE-001

        Requirement: MPRester output is copied immediately into project-owned metal
        units without retaining mutable pymatgen state or pseudopotential policy.

        Method: Retrieve one local ordered silicon structure through an injected client,
        mutate the source afterward, and inspect the exact immutable result.

        Oracle: Pymatgen lattice and Cartesian coordinates are angstrom values; the
        project metal inventory requires angstrom and grams per mole.

        Acceptance: The request is exact, lattice and sites use angstrom, mass uses
        grams per mole, source mutation cannot change the result, and geometry is
        explicitly limited to external-reference status.

        Interpretation: Failure identifies request drift, mutable-state leakage, unit
        relabeling, or structure-owned pseudopotential policy.

        Limitations: Synthetic local input does not verify network access, Materials
        Project content, or a production silicon lattice constant.
        """
        source = self.silicon_structure()
        client = self.StubClient(source)
        request = MaterialsProjectStructureRequest("mp-149")

        result = MaterialsProjectStructureRetriever().execute(client, request)
        source.translate_sites((0,), (0.1, 0.0, 0.0), frac_coords=False)

        assert client.requested_material_id == "mp-149"
        assert client.requested_final is True
        assert client.requested_conventional is False
        assert result.material_id == "mp-149"
        assert result.geometry_status == (
            "external_reference_not_production_pbe_relaxed_lattice"
        )
        assert result.structure.direct_lattice.unit_system is UnitSystem.METAL
        assert result.structure.direct_lattice.unit is LengthUnit.ANGSTROM
        assert result.structure.direct_lattice.vectors[0] == (5.43, 0.0, 0.0)
        assert result.structure.sites[0].coordinates == (0.0, 0.0, 0.0)
        assert result.structure.sites[0].coordinate_unit is LengthUnit.ANGSTROM
        assert result.structure.species[0].mass_unit == "gram_per_mole"
        assert result.structure.species[0].pseudopotential_label is None
        assert result.mass_conversions[0].output.value == (
            result.structure.species[0].mass
        )
        assert result.mass_conversions[0].request.source_correlation is not None

    def test_method__execute__serializes_only_canonical_structure_units(self) -> None:
        """Evidence ID: SV-MATERIALS-PROJECT-STRUCTURE-002

        Requirement: Maintained MP snapshots store canonical metal-unit structure data
        and complete mass-conversion provenance.

        Method: Serialize one locally retrieved canonical reference and inspect exact
        unit, correlation, and conversion-definition fields.

        Oracle: The canonical inventory and retained unified-atomic-mass-unit conversion
        definition require angstrom, grams per mole, and explicit provenance.

        Acceptance: Stable JSON identifies metal units, angstrom coordinates,
        gram-per-mole masses, conversion provenance, and no native-unit,
        pseudopotential, or credential markers.

        Interpretation: Failure identifies native-unit persistence or incomplete
        maintained conversion provenance.

        Limitations: JSON structure does not establish external source authenticity or
        scientific validity.
        """
        result = MaterialsProjectStructureRetriever().execute(
            self.StubClient(self.silicon_structure()),
            MaterialsProjectStructureRequest("mp-149", conventional_unit_cell=True),
        )

        observed = MaterialsProjectStructureJsonSerializer().execute(result)

        assert b'"unit_system": "metal"' in observed
        assert b'"unit": "angstrom"' in observed
        assert b'"coordinate_unit": "angstrom"' in observed
        assert b'"mass_unit": "gram_per_mole"' in observed
        assert b'"identity": "unified-atomic-mass-unit-to-gram-per-mole"' in observed
        expected_correlation = (
            b'"result_identity": "materials-project:mp-149:final-structure"'
        )
        assert expected_correlation in observed
        assert b"bohr" not in observed
        assert b"pseudopotential" not in observed
        assert b"MP_API_KEY" not in observed
        assert b"credential" not in observed
        assert b"Bearer " not in observed

    def test_method__execute__rejects_disordered_source_site(self) -> None:
        """Evidence ID: SV-MATERIALS-PROJECT-STRUCTURE-003

        Requirement: The adapter must not silently collapse partial occupancies.

        Method: Return one synthetic mixed-occupancy site through the injected client.

        Oracle: One canonical project site requires one exact species identity.

        Acceptance: The disordered pymatgen site is rejected before a project structure
        can be represented.

        Interpretation: Failure identifies silent loss of occupancy information.

        Limitations: Other malformed or unavailable API results are outside this case.
        """
        source = Structure(
            Lattice.cubic(5.43),
            ({"Si": 0.5, "Ge": 0.5},),
            ((0.0, 0.0, 0.0),),
        )

        with pytest.raises(ValueError, match="disordered"):
            MaterialsProjectStructureRetriever().execute(
                self.StubClient(source), MaterialsProjectStructureRequest("mp-149")
            )
