# Materials Project silicon reference structure

## Evidence status

`mp-149.structure.json` is externally sourced reference data retrieved from the
Materials Project API. It is not a calculated project result, a production input, or
scientific validation of the bulk-silicon parent model.

The physical specification assigns the production lattice constant to a separate
zero-pressure PBE relaxation using the selected silicon pseudopotential. The Materials
Project geometry must not replace that result.

## Retrieval provenance

- Materials Project identity: `mp-149`
- Public record: <https://materialsproject.org/materials/mp-149>
- Retrieval boundary: `mp_api.client.MPRester.get_structure_by_material_id`
- Retrieval time: `2026-09-20T16:26:10Z`
- Resolved `mp-api` version: `0.46.5`
- Resolved `pymatgen` version: `2026.5.4`
- Project adapter: `MaterialsProjectStructureRetriever`
- Requested form: final primitive structure (`conventional_unit_cell=false`)
- Stored unit system: canonical LAMMPS `metal`
- Credential retention: none

The adapter copied the returned mutable pymatgen structure into immutable project
records. Lattice vectors and Cartesian sites are stored in angstrom. The silicon mass
is stored in grams per mole with complete native-to-canonical conversion provenance.
No pseudopotential assignment is part of this structure.

## Catalog and derived symmetry

The canonical snapshot is imported into the external append-only structure catalog at
`~/projects/ksdft2effmass/structures/structure-catalog.sqlite3` under identity
`materials-project:mp-149`. The mutable SQLite database is not version-controlled.
`mp-149.catalog-entry.json` retains the exact credential-free catalog payload and
source snapshot correlation.

Pymatgen 2026.5.4 `SpacegroupAnalyzer`, with `symprec=0.01` angstrom and
`angle_tolerance=5.0` degrees, derives space group `Fd-3m` (number 227), Hall symbol
`F 4d 2 3 -1d`, cubic crystal system, point group `m-3m`, Wyckoff symbols `a,a`,
and equivalent-atom indices `0,0`. This is tolerance-qualified derived metadata, not
independent crystallographic or scientific validation.

`SHA256SUMS` authenticates both exact retained JSON records using SHA-256.
