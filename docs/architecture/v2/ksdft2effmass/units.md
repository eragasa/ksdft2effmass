# Canonical units and explicit conversion provenance

## Status and authority

This page is the owning architecture-v2 definition of the project canonical unit
system and the initial native-to-canonical conversion slice. Source code and API
pages implement or reference this page; they do not own a second conversion table.

The applicable human response is preserved verbatim:

> recommendation authorized but with information stored in architecture/v2 documents as units.md

The subsequent relay normalized this authorization as choices 1A and 2A. The
resulting decisions are:

1. the exact dimensional inventory of LAMMPS `units metal` is the project
   canonical unit system;
2. BIPM SI and NIST CODATA define conversion factors, while pinned LAMMPS
   documentation defines the dimensional inventory;
3. conversion results are typed in-memory ResultObjects first; this slice adds no
   conversion-result wire format and no canonical calculation-record version 2;
4. native source records and accepted version-1 Hartree/bohr bytes remain
   unchanged; and
5. the information is owned here rather than under `specification/unit-system/`
   or a separate unit-decision page.

The superseded alternatives were a Hartree-atomic project canonical system,
implicit or untyped per-domain canonicalization, LAMMPS-release-embedded constants
as the primary conversion authority, and immediate conversion-result or canonical
calculation-record persistence. These alternatives are not active contracts.

## Canonical dimensional inventory

The canonical inventory follows the pinned LAMMPS `metal` documentation exactly:

- mass: gram per mole;
- distance: angstrom;
- time: picosecond;
- energy and torque: electron volt;
- velocity: angstrom per picosecond;
- force: electron volt per angstrom;
- temperature: kelvin;
- pressure: bar;
- dynamic viscosity: poise;
- charge: multiples of elementary charge;
- dipole: charge times angstrom;
- electric field: volt per angstrom; and
- density: gram per centimeter raised to the spatial dimension.

The immutable public record `METAL_UNIT_INVENTORY` has identity
`ksdft2effmass.units.metal-canonical-inventory`, version 1, and content identity
`sha256:a6c80626e92f510b17bae0a2d3854624b796c5abdd62409b5993fad33db53120`.
Its content preimage is the literal inventory sequence below with `|` separators:

```text
v1|ksdft2effmass.units.metal-canonical-inventory|1|gram_per_mole|angstrom|picosecond|electron_volt|angstrom_per_picosecond|electron_volt_per_angstrom|electron_volt|kelvin|bar|poise|elementary_charge_multiple|elementary_charge_angstrom|volt_per_angstrom|gram_per_centimeter^dimension|442a188db85bacf28bbbe47541382c09aa6ba6f2a8271bc2aadbf35d16987834
```

This inventory does not authorize executable conversions that are not demonstrated
below. In particular, LAMMPS's timestep and neighbor-skin defaults are native
integration policy, not unit definitions. Unified atomic mass unit is a distinct
source/project unit and is explicitly converted to gram per mole; it is never
relabelled.

## Pinned authorities

The source identities below were retrieved as public reference material. Their
SHA-256 hashes identify the exact bytes inspected for this version of the contract.

| Authority role | Identity and version | URL | SHA-256 | Bytes |
|---|---|---|---|---:|
| Canonical dimensional inventory | LAMMPS `units` documentation, signed tag `stable_22Jul2025_update6`, commit `9c5ab448c78a14fd534619622162ba418d6a1fb1` | `https://raw.githubusercontent.com/lammps/lammps/stable_22Jul2025_update6/doc/src/units.rst` | `442a188db85bacf28bbbe47541382c09aa6ba6f2a8271bc2aadbf35d16987834` | 8,990 |
| Recommended conversion values | NIST complete listing, 2022 CODATA adjustment | `https://physics.nist.gov/cuu/Constants/Table/allascii.txt` | `77fb90e66c40db3e6eb16630bc9c88e4c7c8beddbe5e71be406f2f26e3f67e67` | 40,801 |
| SI definitions | BIPM *The International System of Units*, 9th edition (2019), English text updated in 2026, asset version 7.0; DOI `10.59161/AUEZ1291` | `https://www.bipm.org/documents/20126/41483022/SI-Brochure-9-EN.pdf/2d2b50bf-f2b4-9661-f402-5f9d66e4b507?version=7.0` | `5442eea2c680caf77a9d96879205a97f57c7c270b98a0bd0126c18fefe47e02c` | 1,979,202 |

A later authority update requires a new conversion-definition version and new
content identities. It must not silently change a retained definition.

## Demonstrated conversion definitions

Catalog identity `ksdft2effmass.units.metal-native-conversions`, version 1, has
content identity
`sha256:f8555a74b689f05a2f9267030b627c690839c26c4ad6d582e236d366f113fe7e`.
Only the following source-to-target conversions are executable in this slice.
The scale and standard uncertainty columns are exact retained decimal
representations; uncertainty is for one source unit expressed in the target unit.

| Definition identity, version | Source → target | Decimal scale | Standard uncertainty | Definition content identity |
|---|---|---:|---:|---|
| `hartree-to-electron-volt`, 1 | hartree → electron volt | `27.211386245981` | `0.000000000030` eV | `sha256:2fb00672d6de492db9619b4e532fbef55cc0029f4e7644f3def5eae5510d626b` |
| `rydberg-to-electron-volt`, 1 | rydberg → electron volt | `13.6056931229905` | `0.000000000015` eV | `sha256:b2aaace372a88fba0d321664512c9fcd00e49094741903e28aa0cd43ee924154` |
| `bohr-to-angstrom`, 1 | bohr → angstrom | `0.529177210544` | `0.000000000082` Å | `sha256:91adb62af983494f479467b143c4507b945af1e34f23d801fa3e9f172fac609c` |
| `unified-atomic-mass-unit-to-gram-per-mole`, 1 | unified atomic mass unit → gram per mole | `1.00000000105` | `0.00000000031` g mol$^{-1}$ | `sha256:12590b98302929d722bd5fa9f662c8da3534fdc576f86ceaea4c278727cea77b` |

The rydberg factor and uncertainty are exactly one half of the retained CODATA
Hartree values. The bohr value converts the CODATA value in meters using the exact
SI relation $1\,\text{Å}=10^{-10}\,\text{m}$. The mass factor converts the CODATA
molar mass constant from kilograms per mole to grams per mole. These operations do
not make the measured CODATA values exact; their standard uncertainties remain
attached to their definitions.

Definition content identities are SHA-256 hashes of UTF-8 preimages with this exact
field order and literal `|` separators:

```text
v1|definition identity|version|source dimension|source unit|target dimension|target unit|decimal scale|standard uncertainty|numerical policy identity|LAMMPS SHA-256 without prefix|NIST SHA-256 without prefix|BIPM SHA-256 without prefix|implementation identity
```

The catalog content preimage is:

```text
v1|ksdft2effmass.units.metal-native-conversions|1|definition SHA-256 values without prefixes in table order
```

## Arithmetic and represented limitations

Numerical-policy identity
`ksdft2effmass.units.decimal-scale-binary64.v1`, version 1, and implementation
identity `ksdft2effmass.units.MetalQuantityConverter.v1` mean:

1. accept only a finite built-in Python `float`; reject booleans, integers, numeric
   strings, NumPy scalar objects, NaNs, and infinities;
2. convert the exact input binary64 value to `Decimal` without loss;
3. multiply it by the retained exact decimal scale with decimal precision 80;
4. convert once to binary64 using round-to-nearest, ties-to-even;
5. represent nonfinite output or overflow as a closed overflow failure; and
6. represent nonzero input rounded to zero as a closed underflow failure.

A successful ResultObject requires the request source unit, selected-definition
source unit, requested target unit, selected-definition target unit, and output unit
to correlate exactly. Numeric overflow and underflow failures require the same
request-definition pair correlation. An unsupported-pair failure must cite no
conversion definition. These intrinsic invariants prevent contradictory conversion
provenance from being represented.

A successful result records that binary64 output was rounded and that the retained
conversion-factor standard uncertainty was not propagated into an output
uncertainty. Such a result is software conversion evidence only. It does not combine
or quantify parent-model, numerical, discretization, model-reduction, or scientific
uncertainty.

## Provenance and native-record preservation

Every conversion ResultObject retains:

- the exact input binary64 value and source unit;
- the exact requested target unit and, on success, its output binary64 value;
- conversion-definition identity, version, and content identity when a definition
  was selected, or an explicit unsupported-pair failure when none exists;
- catalog identity, version, and content identity;
- authority-document versions, URLs, and content identities through the cited
  definition;
- numerical-policy and converter-implementation identities;
- source artifact, source result, source provenance, and source content identities
  when the caller has them; and
- represented failure and limitation values.

A converter never mutates or replaces its source. Accepted
`KohnShamPlaneWaveCalculationRecord` version-1 records, their Hartree/bohr units,
serializers, schemas, retained JSON bytes, and producer provenance remain intact.
A domain adapter may correlate a new canonical ResultObject with those records, but
must preserve their identities and bytes.

This slice defines no durable conversion wire. Consequently, a production consumer
must not discard a conversion ResultObject and retain only its output scalar. Until
a later explicitly versioned persistence boundary is approved, any maintained use
must embed the complete typed ResultObject in its owning in-memory result or record
all listed fields in a maintained provenance artifact. The current Option-A
composition is execution-free and creates no production conversion history.

## Dependency and ownership boundary

`ksdft2effmass.units` is an inward scientific domain. It owns typed scalar values,
conversion definitions, conversion ResultObjects, and the conversion ActionObject.
It imports no calculator, integration, Workflow, analysis, or persistence package.

Native integrations identify their source units and provenance. Structure,
Kohn–Sham, operator, and analysis domains own transformations of their aggregate
objects and may compose the scalar converter. The units package does not accept an
erased generic object, infer a source unit, render native syntax, or claim backend
equivalence.

`ksdft2effmass.integration.materials_project` is an explicit external-input boundary.
It treats pymatgen lattice and Cartesian coordinate magnitudes as angstrom values,
converts pymatgen atomic masses from unified atomic mass units to grams per mole with
the retained converter, and constructs only immutable metal-unit project structures.
It retains no API credential or mutable pymatgen object. Accepted schema-version-1
plane-wave records remain the native-record exception described above.

## Deferred work

The remaining LAMMPS-metal inventory is authoritative as a unit-system boundary but
has no executable conversion in this slice. Inverse-length, velocity, force,
pressure, viscosity, charge, dipole, electric-field, density, and other derived
conversions require demonstrated consumers, their applicable CODATA correlations,
and separately versioned definitions.

A durable conversion-result wire or canonical calculation-record version 2 remains
deferred. Either would require an explicit public schema, compatibility analysis,
and migration evidence; it must not reinterpret version-1 bytes.

The prior public `PlaneWaveEnergyUnit` enum and two-argument
`PlaneWaveEnergyCutoff(value, unit)` constructor have no compatibility alias. The
replacement requires a canonical electron-volt `UnitScalar` passed to
`PlaneWaveEnergyCutoff(quantity)` after any native-unit conversion has produced its
complete provenance-retaining ResultObject.
