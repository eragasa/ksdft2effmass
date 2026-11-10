# Periodic basis-identity audit

## Status

**Audit complete; the selected basis-identity contract is implemented.**

The source inventory is bound to KSD revision `682e2b08`. The later decision section
records the reviewed structured contract implemented by
`ksdft2effmass.periodic.operators.basis`. This tranche changes no retained calculation bytes and
does not authorize basis embedding, reciprocal-shift sewing, provider adaptation, or
Wilson-loop implementation.

The audit found no single current meaning of `basis_identifier`. Current uses include an
opaque ordered-basis name, a structured basis record identifier, a generated rank label,
a calculation-owned authenticated declaration, and an explicitly unavailable provider
field. Exact string equality is therefore not sufficient evidence that two represented
state spaces use the same ordered basis.

## Scope and method

The inventory covers:

- KSD periodic models, represented operators, frame transport, hopping locality, and
  band-equivalence calculations;
- the maintained `BlockHoppingModel1D` representation and retained periodic-1D replay;
- KSD finite plane-wave basis values;
- PhysKit scalar and block-hopping representations;
- the pinned Project Koios simulations QE plane-wave frame and Wannier90 records;
- reciprocal-endpoint sewing and reciprocal-axis order;
- current typed-record and calculation-owned serialization; and
- the retained C6-B20-W21 silicon analysis composition.

The maintained non-execution trees contain 202 references to `basis_identifier`, its
ambient/represented/retained/parent variants, or `basis_identity` across 66 files. Of
those, 171 references occur in 49 reusable KSD source files. The audit groups those
references by scientific role rather than treating every field spelling as one concept.

Classification terms used below are:

- **explicit**: supplied or retained under a dedicated field without derivation;
- **inferred**: constructed from rank, model-family, or other labels rather than
  supplied by an owning basis value;
- **missing**: ordering or dimension exists, but no correlated basis identity is
  retained at the relevant boundary; and
- **inconsistent**: two current surfaces assign different semantics to the same field
  spelling or retain duplicate declarations that can diverge.

## Contract inventory

| Owner or boundary | Current basis information | Classification | Serialization and provenance | Audit conclusion |
|---|---|---|---|---|
| `ksdft2effmass.operators.Basis` and `StateSpace` | `Basis` retains an identifier, kind, exact ordered unique labels, and an orthonormal flag; `StateSpace` separately retains identifier, kind, and dimension. | Explicit and structured. | Nested schema-version-1 `OperatorRecordJsonSerializer` state. Compatibility compares basis ordering and kind, not either nested identifier. | This is the strongest current KSD basis record, but it is operator-record-specific and is not used by periodic model, frame, or provider paths. Its identifier is descriptive identity, not the compatibility proof. |
| PhysKit `ScalarHoppingModel` and `BaseBlockHoppingModel` children | Nonempty `basis_identifier: str`; block shape supplies basis size. No ordered labels, spin convention, embedding, or source correlation are retained. | Explicit opaque string. | Immutable provider value; KSD has no general retained wire for these models. | Suitable as a pass-through representation label, but insufficient as a complete periodic basis identity. |
| KSD `PeriodicBlockHoppingModel` and dimensional rank-two children | Compose the PhysKit representation, unit-bearing ordered lattice geometry, and an exact dimensional structured basis identity. Construction verifies that basis coordinate count and provider block size both equal the inherited retained rank. | Explicit structured correlation. | In-memory scientific model only; basis identities retain repository-native schema-version-2 mappings at durable boundaries. | Geometry, model identity, provider basis string, and structured basis identity remain distinct. The composition establishes block row/column order but does not infer intracell embedding, gauge, frame, or provenance. |
| `FourierSeriesBlockHoppingRepresentationRequest` | Caller supplies a nonempty provider `basis_identifier`; Fourier matrix shape supplies rank. | Explicit opaque string. | No retained wire owned by the request. | Representation conversion intentionally cannot reconstruct basis identity from coefficients. The caller obligation is currently unstructured. |
| `BlockHoppingModel1D` | Retains reciprocal period, integer representatives, and ordered matrices, but no basis identity. `to_physkit_ordinary_representation()` requires the caller to inject one. | Missing in the maintained representation; explicit only at conversion. | Historical periodic-1D retained bytes reconstruct `BlockHoppingModel1D` without basis identity. | Existing bytes cannot support a new basis-compatibility claim. Migration must correlate an external declaration without rewriting historical bytes. |
| `PlaneWaveBasis1D` and `PlaneWaveReciprocalSewingResult` | The basis value explicitly determines ordered reciprocal indices `-P,...,P`; the finite-cutoff shift retains the exact basis object and coefficient map. | Explicit basis content, missing semantic identifier. | In-memory values; no independent basis wire. | This path proves ordering and map shape more strongly than a raw string, but it does not define a reusable cross-record identity. The finite-cutoff shift is nonunitary and is not an exact Wilson sewing map. |
| `Periodic2DPlaneWaveBlochHamiltonianModel` | Retains state-space identity, basis identity, cutoff, fixed `p`-outer/`q`-inner order, and spinless-scalar convention. | Explicit string plus derived structured ordering; potentially inconsistent. | In-memory model only. | The basis string is not checked against cutoff, ordering, or spin convention. Equal strings can describe different finite inventories, and different strings can describe identical inventories. |
| `KohnShamPlaneWaveCalculationRecord` | Plane-wave `basis_identity`, gauge, and phase convention are explicitly `NOT_REPRESENTED`; no retained subspace exists. | Explicitly missing. | Retained aggregate wire correlates QEXSD path, SHA-256, byte count, producer, and transformation. | The fail-closed unavailable state is scientifically honest. It must not be replaced by a guessed basis name from FFT dimensions or band count. |
| Project Koios simulations `QePlaneWaveFrame` | Retains source-ordered direct and reciprocal vectors, ordered reduced and physical k points, FFT grid, full-grid G-index mapping, Fourier convention, overlap metric, and spin dimensions. | Explicit conventions and ordering, missing basis identity. | Correlated to authenticated QEXSD and pseudopotential artifacts by the provider validator. | This is a qualified producer of basis ingredients, not a producer of a KSD periodic basis identity. A later adapter must preserve source order and artifact correlation. |
| Project Koios simulations Wannier90 records | `_u.mat`, `_u_dis.mat`, `_hr.dat`, NNKP, UNK, and localization records retain native matrix dimensions, k-point order, matrix storage order, Hamiltonian row/column order, and ordered WF-center inventories. | Explicit provider order, missing scientific basis identity. | Artifact manifests and provider correlation validate exact bytes and index chains. | Native indices identify file positions, not orbital, spin, sublattice, embedding, gauge, or accepted MLWF semantics. Artifact identity belongs in provenance, not inside a human-readable basis name. |
| Synthetic band-equivalence model definition | Retains separate parent and retained basis strings alongside the retained seed. Current installed values are hard-coded literals. | Explicit and serialized, but semantically opaque. | `BaseTypedRecord` round trip retains both strings and matrices. | The record distinguishes parent and retained bases correctly, but does not state which components make either identity or how seed-column order is correlated. |
| Periodic-1D rank-N transport and band-equivalence requests | Retain ambient-basis, retained-frame, endpoint-sewing, represented-basis, and energy-reference identifiers as separate strings. | Explicit and serialized. | Requests and owner results use repository-native typed-record mappings. | The role separation is good. Raw string equality still does not establish correspondence between the ambient basis, frame rows, represented basis, and sewing matrix. |
| Periodic-2D/3D rank-two and rank-N frame-transport requests | Retain frame arrays, rank policy, and explicit axis-ordered sewing, but no ambient-basis or retained-frame identity. | Missing at transport boundary. | In-memory requests only. | Shape checks establish dimensions, not scientific basis correspondence. This is acceptable for current synthetic diagnostics but blocks reusable Wilson claims. |
| Periodic-2D synthetic rank-N analytic baseline | The calculation-owned rank inventory supplies explicit `Periodic2DBasisIdentity` values to a concrete parent implementing `Periodic2DRankNParentModel`; legacy locality records receive only the basis display identifier. | Structured at parent/case construction; legacy locality wire remains descriptive. | The concrete calculation or verification parent owns the exact basis, while `Periodic2DRankNParentGaugeCase` correlates that parent with an independent gauge transformation. Reusable source owns neither the analytic formula nor the cross-product inventory. | Do not infer coordinates from rank or model identity. A later complete wire migration must preserve the structured value rather than elevating the descriptive identifier. |
| Periodic-3D synthetic rank-N field producers | A concrete parent implementing `Periodic3DRankNParentModel` owns an exact ordered `Periodic3DBasisIdentity`; the parent/gauge field sampler passes its display identifier into the legacy represented-field boundary. | Structured at parent/case construction; legacy locality fields remain descriptive. | The concrete calculation or verification parent owns the coordinate inventory. Reusable source owns the parent contract and exact correlation checks but does not synthesize a basis label from model identity. | Do not infer coordinates from rank, support, or model identity. A later complete represented-field migration must retain the structured value rather than elevating its display identifier. |
| Periodic-1D calculation-local workflow | Generates a legacy opaque retained-basis label from rank and validates results against the same formula. | Inferred and calculation-local. | Historical calculation records retain the generated string. | The wire is internally deterministic but not evidence of basis composition. Historical values must remain readable; future migration must not treat the formula as a global identity rule. |
| `Periodic3DRankNWannierFieldSource` | Caller supplies operator, energy, and basis strings beside frame and operator arrays. The class explicitly disclaims file provenance. | Explicit opaque string with missing provenance correlation. | In-memory only; calculation composition may retain separate source authentication. | Reusable source behavior is correctly provenance-neutral, but a calculation must bind the basis declaration to authenticated provider artifacts and ordered native indices. |
| `ReciprocalEndpointSewingMap` and inventory | Retain construction identity, exact unitless matrix, ambient dimension, and positive reciprocal-axis tuple order. They intentionally omit basis, gauge, Bloch convention, and direction. | Explicit sewing, missing basis correlation by design. | Complete repository-native typed-record wire; canonical identity bytes are preserved. | The map wire is sufficient for current explicit transport but cannot by itself prove that its rows and columns act on a stated basis. |
| `SewnBandEquivalenceResult` | Retains the complete calculation and exact axis-ordered sewing inventory. Synthetic calculation definitions retain parent and retained basis strings. | Explicit and serialized. | `BaseTypedRecord`; legacy v1 recording remains restricted to named identity sewing. | Sewing persistence is now complete for the modular result, but basis compatibility remains only a string-level assertion. |
| C6-B20-W21 silicon composition | `request.json` declares a basis string and source checksums; `run_analysis.py` independently repeats the operator, energy, and basis literals when constructing the Wannier field source. | Explicit but inconsistent duplicate ownership. | The retained execution authenticates source sizes and SHA-256 values and retains the request identity. The existing execution predates exact sewing retention; the updated script selects explicit identity sewing but has not been executed. | Before any rerun, the script must consume and validate the request-owned scientific identifiers rather than duplicate them. No retained execution bytes should be edited. |

## Identity boundaries

The audit confirms that the following values are not interchangeable:

| Value | What it identifies | Must remain separate from basis identity |
|---|---|---|
| State-space identity | The represented finite or physical state space. | A state space can admit multiple bases. |
| Ordered basis identity | The coordinate vectors associated with matrix rows and columns in exact order. | It does not select an energy zero, geometry, gauge, or embedding. |
| Retained-frame identity | A sampled ordered family of ambient-to-retained frame matrices. | Frame columns can be gauge rotated without changing the ambient basis. |
| Gauge identity | A convention or transformation acting within a represented space. | Gauge equality is not basis equality. |
| Basis embedding | Fractional positions correlated with ordered basis entries. | Equal basis order can be embedded differently; equal positions can host multiple states. |
| Sewing identity and matrix | A declared linear endpoint identification in an ordered ambient basis. | Matrix shape and construction name do not identify that basis. |
| Geometry identity | Ordered physical primitive vectors, units, and related geometry conventions. | Crystal or lattice labels cannot infer the electronic basis. |
| Energy reference and unit | Matrix scale and zero convention. | These affect operator comparison, not basis membership or ordering. |
| Artifact provenance | Exact source bytes, producer, path, checksum, and transformation. | Provenance can support a basis declaration but is not itself the mathematical basis. |

## Ordering and reciprocal-axis invariants

Current ordering evidence is distributed across several owners:

- PhysKit block matrices use matrix row/column order but retain only a basis string and
  block size.
- `operators.Basis.ordering` retains exact labels and is the current operator-record
  compatibility surface.
- `PlaneWaveBasis1D.reciprocal_indices` and the 2D `p`-outer/`q`-inner inventory define
  exact finite plane-wave order.
- `QePlaneWaveFrame` retains source-ordered reciprocal vectors, k points, and a native
  first-axis-fastest FFT/G-vector mapping.
- Wannier90 parsers retain native matrix and k-point order, while localization parsing
  verifies contiguous ordered WF indices before storing centers and spreads.
- `ReciprocalEndpointSewingInventory.positive_axis_maps` is ordered by reciprocal axis;
  each map has the same ambient dimension.
- unit-bearing KSD geometry preserves primitive vectors as ordered columns of the direct
  lattice matrix.

No current value correlates all of these orderings. In particular, reciprocal-axis order
does not determine orbital order, and native Wannier matrix indices do not determine
fractional embedding or orbital labels.

## Serialization and provenance coverage

| Information | Current complete wire | Current limitation |
|---|---|---|
| Structured finite operator basis | Nested `OperatorRecord` basis fields: identifier, kind, ordering, orthonormal. | The legacy string-valued operator record is not used as the structured periodic basis owner. A new operator correlation contract remains separate. |
| PhysKit hopping basis string | Retained in provider model values when those values are in memory. | No repository-wide model wire or ordering inventory. |
| Synthetic parent/retained basis strings | Retained through `BaseTypedRecord` model definitions. | No composition/version rule beyond exact string storage. |
| Periodic-1D rank-N ambient/frame/represented identities | Retained in typed request and result mappings. | No structured relationship among the strings and numerical matrices. |
| Exact endpoint sewing and axis order | Retained by `ReciprocalEndpointSewingInventory` and `SewnBandEquivalenceResult`. | No basis identity, Bloch convention, or source/target direction in the map. |
| Historical `BlockHoppingModel1D` results | Exact historical source document is retained and replayed. | Basis identity is absent and must not be invented during decode. |
| QE/QEXSD observations | Source path, SHA-256, byte count, producer, and transformation are retained. | Basis identity, phase convention, and gauge are explicitly unavailable. |
| QE/Wannier provider chain | Project Koios simulations manifests and validators correlate exact provider artifacts and ordered indices. | KSD has no reviewed adapter producing a basis identity from those correlated records. |
| C6-B20-W21 analysis | Request and execution retain source authentication and a basis declaration. | The producer script duplicates scientific literals; retained execution has no exact sewing record. |

Historical wires must remain unchanged. A future migration may add a new correlated
record or execution that references historical bytes by checksum, but it must not add a
basis identifier while decoding bytes that never contained one.

## Scientific and ownership boundary

PhysKit continues to own reusable lattice displacements, hopping representations, units,
and matrix storage. Project Koios simulations continues to own QE/Wannier parsing,
native ordering conventions, artifact authentication, and provider correlation. KSD
owns the scientific assertion that an admitted provider inventory represents a stated
ordered basis for a particular model, calculation, or comparison.

The implemented KSD basis identity must consume future provider evidence without copying
provider parsers or encoding artifact checksums into an opaque display string. It also
remains distinct from acceptance of Wannier localization, DFT convergence, subspace
adequacy, or material validation. Maintained analytic 2D plane-wave models now expose
their exact reciprocal-index order directly; QE and Wannier provider admission remains
unimplemented.

## Findings and recommendation

### Basis value selection

Disposition: **RESOLVED_AND_IMPLEMENTED**

Problem: The public `basis_identifier: str` spelling cannot express the current ordering,
component, and provenance distinctions. Two defensible designs remain: retain an opaque
string but require a separate structured ordered-basis inventory everywhere, or replace
the public compatibility value with a dedicated immutable open basis value and keep a
display identifier inside it.

Evidence: `operators.Basis` already requires ordered labels and compatibility ignores its
identifier; PhysKit hopping models retain only a string and size; plane-wave and provider
records retain ordering without a shared identifier; current synthetic code generates
strings from model labels.

Consequence: Selecting string equality as the compatibility rule can silently align
unrelated coordinate systems. Selecting a new value without a migration decision can
break retained wires or duplicate the operator-record basis owner.

Resolution: `PeriodicBasisIdentity` is the dedicated immutable value, with exact
family-specific ordered coordinates and a descriptive non-compatibility identifier.
The structured value is not projected through string-valued `operators.Basis` metadata.
A future operator correlation contract, provider admission, and
`PeriodicBasisEmbedding` remain separate later gates.

### Generated basis strings

Disposition: **SAFE_TO_DEFER**

Problem: Current 2D/3D synthetic producers and the calculation-local periodic-1D
analytic validation workflow generate basis strings from model family or rank.

Evidence: `periodic2d/.../analysis.py`, `periodic3d/.../represented_fields.py`, and
`calculations/periodic1d/rankN/.../workflow/definition.py` construct formatted basis
labels.

Consequence: The strings are deterministic labels, not independently owned basis
identities. Reusing their construction pattern would make future compatibility depend on
naming convention.

Next action: Preserve historical reads, but require explicitly supplied structured basis
values when these studies are individually migrated. Revisit before any of these paths
feeds basis embedding or Wilson construction.

### Frame and sewing correlation

Disposition: **SAFE_TO_DEFER**

Problem: Periodic-2D/3D frame-transport requests validate frame and sewing dimensions but
retain no ambient-basis or retained-frame identity, while sewing maps intentionally omit
basis identity and Bloch convention.

Evidence: the rank-two and rank-N transport requests accept frame arrays and
`ReciprocalEndpointSewingInventory`; the sewing wire retains only identifier and matrix.

Consequence: Current numerical diagnostics remain reproducible, but they cannot support
a cross-record claim that a sewing matrix acts on the same ordered basis as a frame.

Next action: Add correlation only after the basis-value decision. Revisit before reusable
Wilson-loop construction or nonidentity provider sewing is retained as scientific
evidence.

### Provider-to-KSD basis adaptation

Disposition: **SAFE_TO_DEFER**

Problem: QE and Wannier90 provider records preserve source order and artifact identity,
but no reviewed KSD adapter turns those values into an admitted ordered basis identity.

Evidence: `QePlaneWaveFrame` and the Wannier90 parsers retain ordering conventions and
provider correlation; `KohnShamPlaneWaveCalculationRecord` explicitly marks basis
identity unavailable.

Consequence: A calculation can declare a basis string, but reusable code cannot yet
verify that declaration against provider-native order.

Next action: Design an adapter after the identity decision. It must consume authenticated
provider values, preserve native order, and fail closed when orbital/spin/embedding
semantics are unavailable.

### Historical retained bytes

Disposition: **SAFE_TO_DEFER**

Problem: Historical periodic-1D results and the retained silicon execution do not contain
all basis and sewing information required by the prospective architecture.

Evidence: retained periodic-1D replay reconstructs `BlockHoppingModel1D` without basis
identity; the C6-B20-W21 execution predates exact sewing persistence.

Consequence: Those artifacts cannot independently support future basis-compatibility or
Wilson claims.

Next action: Leave the bytes unchanged. If reused, create a new correlated record that
references exact historical bytes and records the additional declaration and its source.

### Silicon request/producer duplication

Disposition: **SAFE_TO_DEFER**

Problem: the C6-B20-W21 request owns operator, energy, and basis declarations, but the
producer script repeats the same literals rather than consuming and checking them.

Evidence: `request.json` contains the declarations; `run_analysis.py` lines 552--555
construct the source from duplicate literals and never read `request["operator"]`.

Consequence: An edited request could be authenticated and retained while the producer
uses different scientific identifiers.

Next action: Correct the composition before any authorized rerun. Do not edit the prior
execution or its checksums.

## Selected basis-identity contract

The basis-identity gate is resolved for the first implementation by
`ksdft2effmass.periodic.operators.basis.PeriodicBasisIdentity`. The value owns a nonempty ordered
tuple of unique coordinates from exactly one concrete family. Tuple position is matrix
row/column order.

Exact compatibility is order-sensitive equality of the concrete coordinate family and
all coordinate fields. `display_identifier` is descriptive and is deliberately excluded
from equality and hashing. No string normalization, alias, permutation, provider
inference, gauge bridge, or fallback participates in compatibility.

The first wire supports four coordinate families:

| Family | Exact coordinate key | Compatibility-bearing fields |
|---|---|---|
| Labeled analytic/composite component | one exact label | `label` |
| Plane wave | reciprocal-lattice index plus optional internal component | ordered integer `reciprocal_index`; exact `component_label` or explicit scalar `None` |
| Qualified native Wannier orbital | provider-native ordinal plus scientifically qualified orbital label | zero-based `native_ordinal`; exact `qualified_orbital_label` |
| Slater--Koster orbital | primitive-cell site, orbital, and optional explicit spin component | `site_label`; closed `SlaterKosterOrbital`; exact `spin_component` or explicit spinless `None` |

The supported Slater--Koster orbital vocabulary is the current spinless `sp3s*` set
`s`, `p_x`, `p_y`, `p_z`, and `s_star` in conventional Cartesian axes. The diamond
model binds the exact order
`(diamond_origin_center:s,p_x,p_y,p_z,s*, diamond_body_diagonal_quarter_center:s,p_x,p_y,p_z,s*)`
to this structured value. These descriptive center identifiers are model-owned exact
fields, not aliases for opaque sublattice letters.

The dimensional `PeriodicBasisIdentity` wire uses schema version 2 and the
repository-native `BaseTypedRecord` mapping fields `schema_version`,
`spatial_dimension`, `display_identifier`, `family`, and the typed tuple
`coordinates`. The abstract base has no standalone wire construction; concrete
`Periodic1DBasisIdentity`, `Periodic2DBasisIdentity`, and
`Periodic3DBasisIdentity` values validate their fixed spatial dimension. Each
coordinate carries its exact `kind` and family-specific fields, and plane-wave
reciprocal-index rank must equal the identity's spatial dimension.

State-space identity, retained-frame identity, gauge, embedding, geometry, energy
reference, sewing, and artifact provenance remain separate values. In particular,
Wannier artifact identity is not folded into basis equality. A provider adapter must
fail closed if it has only an ordinal or generated label and cannot establish the
required `qualified_orbital_label` semantics.

`operators.Basis` remains the current finite-operator record owner for its existing
records, but its string ordering is not promoted to `PeriodicBasisIdentity` and is not a
target representation for new structured periodic coordinates. A future periodic
operator correlation must consume `PeriodicBasisIdentity` directly.

This decision authorizes the basis identity only. It does not authorize
`PeriodicBasisEmbedding`, `BlochBasisConvention`, `ReciprocalShiftSewingMap`, provider
adapters, or reusable Wilson-loop construction. Those capabilities remain blocked on
their own reviewed contracts and correlations.

## Dependencies and flow

```text
authenticated provider artifacts or analytic basis definition
  -> provider-native ordered indices and conventions
  -> reviewed KSD basis-admission adapter
  -> immutable ordered basis identity
  -> model / frame / represented operator correlation
  -> basis embedding and Bloch convention
  -> reciprocal-shift sewing
  -> selected-subspace transport or Wilson construction
  -> retained result plus independent verification
```

The audit adds no dependency and authorizes no external execution.

## Evidence and limitations

Primary KSD evidence:

- `python/src/ksdft2effmass/operators/records.py`
- `python/src/ksdft2effmass/operators/compatibility.py`
- `python/src/ksdft2effmass/solidstate/hopping_transforms.py`
- `python/src/ksdft2effmass/solidstate/reciprocal_paths.py`
- `python/src/ksdft2effmass/periodic/periodic2d/models/plane_waves.py`
- `python/src/ksdft2effmass/ksdft/pw/records.py`
- `python/src/ksdft2effmass/band_equivalence_hopping_locality/`
- `python/src/ksdft2effmass/periodic1d/rankN/`
- `python/src/ksdft2effmass/periodic2d/rankN/`
- `python/src/ksdft2effmass/periodic3d/rankN/`
- `python/src/ksdft2effmass/sewing/`
- `calculations/periodic1d/rankN/composite-band-alignment-locality/`
- `calculations/Si/bulk/analysis/c6-b20-w21-gauge-alignment-locality/`

Provider evidence was inspected at the dependency revisions pinned by
`python/pyproject.toml` and `python/uv.lock`, including PhysKit hopping records and
Project Koios simulations QE plane-wave frame, QE/Wannier correlation, and Wannier90
native records.

This is a source and retained-wire audit. It does not establish that any current basis
declaration is physically correct, does not validate a DFT or Wannier calculation, does
not reconstruct missing orbital semantics, and does not make a Wilson-loop or topology
claim.

## Navigation

- Prospective embedding and Wilson boundary: [`index.md`](index.md)
- Reciprocal-endpoint sewing: [`../../sewing/index.md`](../../sewing/index.md)
- Periodic model hierarchy: [`../models/index.md`](../models/index.md)
- Scientific operation taxonomy:
  [`../../scientific-operation-taxonomy.md`](../../scientific-operation-taxonomy.md)
