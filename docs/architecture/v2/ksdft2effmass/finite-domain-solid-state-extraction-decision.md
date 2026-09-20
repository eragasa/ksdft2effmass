# Solid-state extraction boundary for finite-domain lattice models

## Problem

**Human choice.** Select the public package that will own reusable solid-state
lattice-model contracts extracted during a later implementation of the accepted
finite-domain-effects design.

The decision covers immutable hopping, localized-defect, finite-supercell,
boundary-twist, point-operation, and gauge-representation contracts plus their reusable
construction and compatibility actions. It does not authorize implementation or
calculation execution, change the accepted finite-domain scientific design, select new
physics, or move campaign orchestration and retained wire formats out of
`ksdft2effmass.campaigns.research_monograph`.

The three architectures below intentionally distinguish the modeled solid-state
subject, the finite represented operator, scientific analysis, and the exact campaign.

## Observed current behavior

**Observed fact.** `ksdft2effmass.structures.periodic` owns backend-neutral atomic
crystal geometry: direct and reciprocal lattices, species, sites, units, coordinate
conventions, and direct--reciprocal compatibility. Its maintained architecture page
explicitly excludes electronic k-point sampling, calculator policy, and comparison
policy (`docs/architecture/v2/ksdft2effmass/structures/periodic.md`).

**Observed fact.** `ksdft2effmass.electronic_structure` currently owns only ordered
reciprocal-space `KPointSampling` and its weight-normalization state. It consumes
periodic-structure conventions and does not yet own reduced lattice Hamiltonians
(`python/src/ksdft2effmass/electronic_structure/sampling.py`).

**Observed fact.** `ksdft2effmass.operators` owns finite represented-operator records,
quantities, fixed-representation compatibility, eigensolution, subspace selection,
norms, and residual mechanics. Its accepted boundary excludes geometry or gauge
selection, model fitting, impurity classification, and scientific acceptance
(`docs/architecture/v2/ksdft2effmass/operators/index.md`).

**Observed fact.** `ksdft2effmass.analysis` consumes operator contracts and owns
alignment, model fitting, continuum reduction, diagnostics, numerical policy, and
claim boundaries. It does not execute calculators or decide scientific acceptance
(`docs/architecture/v2/ksdft2effmass/analysis/index.md`).

**Observed fact.** The accepted-parent calculation-local implementation currently
combines reusable solid-state ideas with campaign policy. Examples are `ParentHopping`,
`LocalBond`, `PointOperation`, `ParentMatrixConstructor`, and
`ParentHoppingConstructor` under
`calculations/research-monograph/impurity-defect-2d/stage_c_parent/`. Its names and
invariants remain tied to the historical campaign.

**Observed fact.** The accepted finite-domain contract fixes nine unique isotropic
geometries, two anisotropic orientation pairs, two defects, an 81-point twist mesh, and
2,430 proposed production operator evaluations. It requires distinct area, shape,
orientation, and boundary-phase channels and an independent seam-gauge verifier
(`calculations/research-monograph/impurity-defect-2d/finite-domain-effects-design.json`).

**Observed fact.** The bounded extraction inventory identifies the reusable geometry,
twist, hopping, localized perturbation, lattice-operation, gauge, sparse-construction,
folding, compatibility, locality, spectral, and finite-domain contracts that must be
closed over one, two, and three spatial dimensions. It separately defers multi-orbital,
spin, composite, nonorthogonal-lattice, atomic-structure mapping, and protected-execution
work
(`docs/architecture/v2/ksdft2effmass/finite-domain-solid-state-extraction-inventory.md`).

**Inference.** A reusable solid-state owner is warranted because both the accepted
parent workflow and the planned finite-domain workflow consume the same hopping,
twist, supercell, symmetry, and gauge concepts. Campaign-specific case inventories,
model-class selection, thresholds, result serialization, and protected execution are
not reusable domain meaning.

## Decision requirements

**Accepted requirement.** Preserve dependency direction toward
`ksdft2effmass.operators`; a solid-state domain owner may consume represented-operator
records, while operators must not import a concrete higher-level analysis or campaign.

**Accepted requirement.** Do not redefine atomic crystal geometry or k-point sampling.
A finite integer supercell is not automatically a `PeriodicStructure`, and a boundary
twist fiber is not automatically weighted Brillouin-zone sampling.

**Accepted requirement.** Keep the following reusable concepts explicit and immutable:
integer lattice displacement, scalar hopping term, ordered finite-rank hopping model,
localized bond perturbation, finite periodic supercell shape and ordering, twist lift,
reduced twist representative, integral point operation, and declared gauge
representation. Their spatial contracts must be closed over exactly one, two, and three
dimensions without unconstrained coordinate sequences, silent padding, or dropped axes.

**Accepted requirement.** Keep energy unit and energy-reference identities explicit.
`Unitless` is a represented unit rather than absent metadata. General units continue to
use the existing Pint-backed operator quantity contracts.

**Accepted requirement.** Compatibility, tolerance, symmetry, gauge transformation,
operator construction, and comparison are ActionObject behavior. Serialization belongs
to serializers. Area/shape/orientation/twist orchestration belongs to the campaign
Workflow. No reusable behavior may remain as an unowned module-level callable.

**Accepted requirement.** Production and independent verification must not share
construction algorithms. A public production constructor cannot be imported by the
independent seam-gauge verifier.

**Accepted requirement.** Sparse hopping structure must not be densified before an
algorithmically explicit dense boundary. Historical retained results and their source
identities remain unchanged.

**Human choice.** Decide whether these concepts belong to electronic structure, a broad
solid-state aggregate, or a focused lattice-model aggregate.

## Option A

**Conceptual model**

Place the reusable records and actions under
`ksdft2effmass.electronic_structure.lattice_models`. Electronic structure becomes the
aggregate for both reciprocal sampling and reduced translational Hamiltonians. State is
immutable in memory; a later versioned serializer would live beside the lattice-model
contracts, while exact campaign results remain campaign-owned.

**Authority**

The package owns the meaning of reduced single-particle hopping models, twist fibers,
and finite periodic representations. Atomic geometry stays in `structures.periodic`;
scientific analysis stays in `analysis`.

**Ownership/dependency**

`electronic_structure.lattice_models` imports operator quantities and represented
matrices and may import periodic coordinate conventions. `analysis` and campaigns
consume it. `operators` and `structures` do not import it.

**Runtime/dispatch**

A `TwistedSupercellHamiltonianConstructor` receives explicit model, supercell, twist,
and gauge records and returns a represented sparse operator. Campaign Workflows select
case inventories and invoke it; no registry or mutable global dispatch is introduced.

**Migration**

Introduce records first, then the production constructor, then analysis actions, and
finally switch the new finite-domain campaign. Historical Stage C remains bound to its
calculation-local implementation. No compatibility re-export is needed until a real
consumer requires one.

**Reversibility**

Records can later move to a focused package through explicit import and wire migration,
but published type identities would make that move a public compatibility event.

**Failures**

The architecture risks treating every hopping model as an electronic-structure result
and conflating a twist mesh with weighted k-point sampling. It must reject implicit
conversion between those concepts.

**Complexity**

Moderate: one subpackage extends an existing owner, but the owner broadens from one
sampling module to a heterogeneous aggregate.

**Maintenance**

Sampling and lattice-model maintainers share one public namespace and must preserve a
clear boundary between calculated electronic-structure observations and reduced model
inputs.

**Context-window consequences**

Agents inspecting electronic structure must load more unrelated contracts; however,
all reciprocal and translational concepts are discoverable beneath one aggregate.

**Future compatibility**

This option can naturally add Bloch interpolation and Wannier-derived hoppings, but may
become crowded when calculator-derived bands, occupations, and reduced Hamiltonians
expand independently.

**Advantage**

It keeps reciprocal sampling, Bloch phases, and translational Hamiltonians close and
requires no new top-level package.

**Risk**

It weakens the current narrow meaning of `electronic_structure` and invites accidental
claims that a synthetic or fitted lattice model is a calculated electronic-structure
result.

## Option B

**Conceptual model**

Create a broad `ksdft2effmass.solid_state` aggregate. It owns a curated application
layer over crystal structures, reciprocal sampling, lattice Hamiltonians, symmetry,
boundary twists, and finite-domain construction. Its persistent contracts would be
solid-state-domain records; operator matrices and campaign results remain owned by
their existing packages.

**Authority**

The aggregate owns solid-state composition and terminology spanning structures,
electronic structure, and represented operators. Existing packages retain their
primitive records.

**Ownership/dependency**

`solid_state` imports `structures.periodic`, `electronic_structure`, and `operators`.
`analysis` and campaigns import `solid_state`. Existing inward packages never import
it.

**Runtime/dispatch**

Solid-state constructors compose existing primitive records into hopping models,
twist fibers, and finite operators. Explicit ActionObjects perform construction and
compatibility; there is no service locator or plugin registry.

**Migration**

Create the aggregate and its narrowly selected public records, then migrate the new
finite-domain implementation. Later consumers may add crystal-to-model and
sampling-to-twist adapters only when demonstrated. Historical imports remain unchanged.

**Reversibility**

The aggregate can remain a stable facade while internals move, but removing it after
public adoption would require broad compatibility support.

**Failures**

The package may become a generic dumping ground. It may duplicate records from
structures, electronic structure, or operators, or hide scientific policy behind a
convenient facade. Reviews must reject re-export-only types and ambiguous ownership.

**Complexity**

High: the aggregate requires a durable charter, dependency rules, API documentation,
and continual policing across several domain boundaries.

**Maintenance**

Cross-domain maintainers must coordinate every new public concept. The package offers a
clear user-facing vocabulary but increases overlap disputes.

**Context-window consequences**

A broad package index and API surface increase inspection cost and make bounded changes
harder to reason about, even if submodules remain cohesive.

**Future compatibility**

It provides an obvious home for symmetry, band topology, Wannier models, and finite
crystals, but those prospective areas are not currently authorized and could bias the
API prematurely.

**Advantage**

It gives users an explicit solid-state entry point and supports future composition
without classifying all domain concepts as analysis or low-level operators.

**Risk**

Its breadth exceeds the demonstrated two-consumer reuse and conflicts with the rule to
extract abstractions only when actual reuse is established.

## Option C

**Conceptual model**

Create the focused top-level package `ksdft2effmass.lattice_models`. It owns only
finite-rank translational lattice-Hamiltonian meaning and finite periodic
representations: hopping inventories, localized perturbations, integer supercells,
twist fibers, integral lattice operations, gauge declarations, and their deterministic
operator construction. Atomic crystal geometry, k-point sampling, generic represented
operators, scientific analyses, and campaigns remain separate.

**Authority**

The package owns reduced lattice-model semantics without asserting that a model was
calculated by DFT or derived from a particular crystal. Provenance records state those
relationships explicitly when present.

**Ownership/dependency**

`lattice_models` imports Pint-backed quantities and represented operators from
`operators`. It does not initially import `structures.periodic` or
`electronic_structure`; future adapters require demonstrated consumers. `analysis`
imports both `lattice_models` and `operators`, and campaigns import analysis and
lattice-model contracts.

**Runtime/dispatch**

Immutable records feed explicit actions such as
`TwistedSupercellOperatorConstructor`, `LatticeModelCompatibilityAuditor`, and
`LatticeSymmetryAnalyzer`. Campaign Workflows provide exact geometries, twists,
defects, and policies. The independent verifier owns a separate seam-matrix algorithm
outside the production implementation package.

**Migration**

Implement the minimum shared slice in dependency order: immutable records and negative
contract tests; sparse uniform-link construction; gauge-bridge result records and
compatibility analysis; finite-domain analysis records; campaign orchestration and
serializers; independent verifier; then thin CLIs. The accepted Stage C calculation
remains byte- and identity-preserved and becomes a compatibility oracle, not migrated
history.

**Reversibility**

The narrow charter minimizes public surface. If a broader solid-state aggregate later
becomes justified, it can consume this package without moving its type identities.

**Failures**

The package must reject unspecified basis ordering, energy reference, unit, geometry,
twist lift, reduced representative, or gauge. It must not absorb campaign thresholds,
model-class selection, protected execution, atomic structure, weighted k-point
sampling, or scientific acceptance.

**Complexity**

Moderate initially and bounded by demonstrated concepts. It adds one top-level package
but avoids a broad facade and avoids changing existing package meanings.

**Maintenance**

The charter is cohesive: maintainers own reusable reduced lattice models and their
finite representations. Analysis and campaign changes remain independently reviewable.

**Context-window consequences**

Agents can inspect one small domain package for hopping/twist/supercell semantics and
need load analysis or campaign code only when changing policy or orchestration.

**Future compatibility**

The package can support multi-orbital Wannier and tight-binding models after a second
consumer proves the required rank, orbital-basis, spin, or gauge abstractions. It does
not predeclare those contracts now.

**Advantage**

It expresses the demonstrated solid-state reuse precisely while preserving existing
structure, sampling, operator, analysis, and campaign boundaries.

**Risk**

A new top-level package adds one public concept and requires careful terminology so
users do not mistake a generic lattice model for atomistic crystal structure or a DFT
result.

## Three-option comparison

| Criterion | Option A: electronic structure | Option B: solid-state aggregate | Option C: focused lattice models |
|---|---|---|---|
| Authority clarity | Moderate; model and calculated-observation meanings can blur | Moderate; broad composition authority | High; narrow reduced-model authority |
| Dependency direction | Acceptable but broadens an existing inward package | Clear outward aggregate | Clear focused domain to operators |
| State and persistence | Cohesive but shares namespace with sampling | Cohesive only with strong subpackage discipline | Cohesive minimal records and later serializer |
| Runtime dispatch | Explicit constructors | Explicit cross-domain composition | Explicit narrow constructors |
| Historical preservation | Preserved | Preserved | Preserved |
| Migration size | Moderate | Largest | Smallest contract-complete slice |
| Failure isolation | Sampling/model confusion risk | Ownership-overlap risk | Narrow compatibility failures |
| Reversibility | Public identities constrain later move | Durable facade is hard to remove | Broader aggregate can consume it later |
| Maintenance | Shared electronic-structure scope | Highest coordination cost | Bounded domain ownership |
| Context-window cost | Moderate | High | Low |
| Premature abstraction risk | Moderate | High | Lowest |
| Multi-orbital future | Natural but potentially crowded | Broadly accommodating | Add only after demonstrated reuse |

**Inference.** All three can preserve the accepted scientific design and retained
artifacts. Their material difference is which domain owns model meaning and which
packages future consumers must import; this is not a filename or configuration choice.

## Recommendation

Recommend **Option C: focused `ksdft2effmass.lattice_models`**.

It satisfies the request to extract reusable solid-state types without broadening
atomic structures, overloading electronic-structure observations, or creating an
open-ended solid-state facade. It also supports an adversarial implementation sequence:
first prove immutable contracts and sparse construction, then independently reconstruct
the seam route, and only afterward connect the exact finite-domain campaign. The
recommendation remains architecture advice rather than retrospective human selection.
HC20 subsequently selected Option B, the broad `ksdft2effmass.solid_state` composition
aggregate, whose implementation must preserve the cohesive submodule and dependency
boundaries identified here.

## Deferred questions

- Exact public class names and module grouping are deferred until the package owner is
  selected; names in the options are illustrative implementation consequences.
- Multi-orbital rank, spin, orbital gauge, and Wannier provenance remain deferred
  because the accepted finite-domain design is rank-one scalar.
- A bridge from physical `PeriodicStructure` to lattice-model geometry remains deferred
  until a real consumer supplies an unambiguous lattice-to-cell mapping.
- A bridge between weighted `KPointSampling` and unweighted twist fibers remains
  deferred; implicit conversion is forbidden.
- Versioned wire formats for reusable lattice models remain deferred until persistence
  outside exact campaign results is required.
- Execution authorization, resource containment, and native-root retention remain
  separate protected decisions.

## Human decision required

HC20 resolved this boundary by selecting **Option B — Broad solid-state aggregate**.
The following options are retained as the original decision interface:

- **A — Electronic-structure ownership:** place lattice-model and twist contracts under
  `ksdft2effmass.electronic_structure.lattice_models`.
- **B — Broad solid-state aggregate:** create `ksdft2effmass.solid_state` as the
  composition owner spanning existing domain packages.
- **C — Focused lattice-model package:** create
  `ksdft2effmass.lattice_models` with narrow reduced-model authority.
- **D — Reconsider or defer:** do not select an architecture and request revised scope
  or alternatives.

The later human implementation instruction authorizes bounded public solid-state source,
software-verification, and documentation work. Accepted-parent reads, finite-domain
campaign execution, dependency changes, and automatic successor activation remain
unauthorized.
