# General periodic-model architecture

## Status and authority

This directory records the accepted target architecture for periodic scientific
models and the campaigns that execute studies over them. It is an architecture
contract and migration target. It does not claim that every named class or package is
implemented, establish a calculated result, validate graphene or silicon models, or
authorize an external calculation.

The target supersedes the earlier description of `ksdft2effmass.periodic` as only a
compatibility package. The nominal model hierarchy and immutable toy-catalog contract
are now implemented there. The package still provides its legacy geometry and sampling
exports; their removal belongs to the staged migration described in
[`migration.md`](migration.md). Historical result identifiers and retained artifacts
are not renamed merely to match the target package layout.

## North-star separation

A scientific model identifies the modeled periodic system. A campaign is the
executable Workflow or ActionObject that evaluates one or more selected models under
explicit controls. The dependency is one-way:

```text
campaign definition and execution
              |
              v
      scientific model hierarchy
              |
              v
 reusable geometry, operators, units, and numerical Actions
```

Scientific models never import campaign definitions, campaign provenance, campaign
thresholds, or campaign acceptance policy. Campaigns compose models; models do not
inherit from campaigns. Within the scientific branch, the parent model, retained
subspace, exact retained operator, matrix representation, and approximate effective
model remain distinct as specified in
[`retained-spaces-and-operators.md`](retained-spaces-and-operators.md).

## Architecture requirements

| Requirement | Accepted target |
|---|---|
| `PERIODIC-ARCH-001` | Scientific periodic models are independent of campaigns. |
| `PERIODIC-ARCH-002` | Every supported periodic model belongs nominally to the one-, two-, or three-dimensional hierarchy. Structural `Protocol` conformance is not the enforcement boundary. |
| `PERIODIC-ARCH-003` | Each dimension owns a nominal defect-model branch whose records preserve the parent model and the prerequisites for aligned comparison. |
| `PERIODIC-ARCH-004` | A campaign is the executable layer and consumes immutable definitions or requests while returning typed results. |
| `PERIODIC-ARCH-005` | Iteration over toy models uses an explicit immutable catalog with deterministic ordering and exact model identities. |
| `PERIODIC-ARCH-006` | Model comparison proceeds only through declared compatible quantities, units, geometries, bases, gauges, and aligned state spaces. |
| `PERIODIC-ARCH-007` | Graphene is the material-reference family for the two-dimensional program. |
| `PERIODIC-ARCH-008` | Bulk silicon is the material-reference family for the three-dimensional program; substitutional phosphorus and boron are its initial defect targets. |
| `PERIODIC-ARCH-009` | Software verification, numerical verification, scientific validation, uncertainty quantification, and human acceptance remain distinct. |
| `PERIODIC-ARCH-010` | No architecture record authorizes production electronic-structure execution, external computation, dependency changes, or publication actions. |
| `PERIODIC-ARCH-011` | A parent model, retained subspace, exact retained operator, finite representation, and approximate effective model are separate typed objects connected by explicit constructions or maps. |
| `PERIODIC-ARCH-012` | Scientific retention is distinct from preservation of evidence; encoded campaign documents do not become scientific models or retained operators because their bytes are preserved. |
| `PERIODIC-ARCH-013` | Projection, disentanglement, gauge change, localization, representation change, truncation, alignment, fitting, and continuum embedding remain distinct typed operations. |
| `PERIODIC-ARCH-014` | A reduction identifies its parent, retained representation, candidate model class, map, frozen training and withheld inputs, metrics, tolerances, and provenance. |
| `PERIODIC-ARCH-015` | Impurity extraction is a signed operation on compatible aligned retained operators; neither the raw doped Hamiltonian nor an arbitrary same-shaped difference is an impurity operator. |
| `PERIODIC-ARCH-016` | Reduction routes have explicit identities and may be compared only after their parents, spaces, maps, objectives, and validation domains are compatible. |
| `PERIODIC-ARCH-017` | Incompatible, unavailable, nonconverged, no-accepted-class, noncommuting-route, and no-finite-crossover outcomes remain explicit typed results over their tested domains. |
| `PERIODIC-ARCH-018` | A mathematical retained subspace does not own a projector/frame union; available represented frames own their content identities through typed bindings, digest-only projector evidence remains with its campaign result until projector coordinates exist, and band-frame records compose one lower-level reciprocal-mesh owner. |

## Implemented module map

| Source module | Canonical architecture page | Supported responsibility |
|---|---|---|
| `python/src/ksdft2effmass/periodic/model.py` | [`model/index.md`](model/index.md) | Nominal one-, two-, and three-dimensional scientific-model hierarchy |
| `python/src/ksdft2effmass/periodic/catalog.py` | [`catalog/index.md`](catalog/index.md) | Explicit immutable toy-model catalogs |
| `python/src/ksdft2effmass/periodic/retention.py` | [`retained-spaces-and-operators.md`](retained-spaces-and-operators.md) | Scientific-retention contracts; canonical module/class-page migration remains governed by the documentation standard |

## Owning documents

- [`scientific-model-hierarchy.md`](scientific-model-hierarchy.md) owns the nominal
  scientific taxonomy and the distinction between dimensional, defect, toy, and
  material-reference identities.
- [`retained-spaces-and-operators.md`](retained-spaces-and-operators.md) owns the
  software distinction among scientific retention, operators, representations, model
  classes, and preservation of evidence.
- [`band-frame-ownership-decision.md`](band-frame-ownership-decision.md) owns the
  accepted removal of the generic projector/frame union, payload-qualified frame and
  projector-evidence ownership, and lower-level reciprocal-mesh dependency direction.
- [`reduction-and-evidence-boundaries.md`](reduction-and-evidence-boundaries.md)
  owns the software consequences of representation construction, model-class
  reduction, alignment, impurity extraction, route comparison, continuum embedding,
  and evidence discipline.
- [`campaign-execution.md`](campaign-execution.md) owns the separation between
  immutable campaign records and executable campaign Actions or Workflows.
- [`catalogs-and-comparison.md`](catalogs-and-comparison.md) owns explicit toy-model
  iteration and compatibility-gated comparison.
- [`migration.md`](migration.md) defines the migration phases and invariants.
- [`documentation-and-evidence-gate.md`](documentation-and-evidence-gate.md) defines
  the scientist-facing source, test, Sphinx, architecture, and evidence dossier
  required before a crosswalk row is complete.
- [`current-to-target-class-crosswalk.md`](current-to-target-class-crosswalk.md)
  classifies current boundary-defining types and gives each migration unit a stable
  disposition.
- [`crosswalk-reconciliation.md`](crosswalk-reconciliation.md) records separate
  implementation and scientist-facing documentation status for all 73 rows.
- [`archives.md`](archives.md) points to completed migration records retained in Git
  after they leave the active architecture tree.
- [`periodic1d/index.md`](periodic1d/index.md),
  [`periodic2d/index.md`](periodic2d/index.md), and
  [`periodic3d/index.md`](periodic3d/index.md) record only dimension-specific deltas.

## Authority boundaries

Physical and mathematical definitions belong in applicable versioned files under
`specification/`. Scientific assumptions for graphene, silicon, and their defects
belong under `docs/research/` when they are authored. External calculation dependencies
and reproduction procedures belong under `docs/computational/`. Implemented public
APIs and concepts belong under `doc/sphinx/`.

These architecture pages must link to those owners rather than duplicate their
content. Mutable task activation, ownership, run state, and protected-execution
approval do not belong here.

```{toctree}
:hidden:

scientific-model-hierarchy
retained-spaces-and-operators
band-frame-ownership-decision
reduction-and-evidence-boundaries
campaign-execution
catalogs-and-comparison
migration
documentation-and-evidence-gate
current-to-target-class-crosswalk
crosswalk-reconciliation
archives
periodic1d/index
periodic2d/index
periodic3d/index
```
