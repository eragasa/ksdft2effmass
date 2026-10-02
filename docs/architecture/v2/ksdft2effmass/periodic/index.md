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
inherit from campaigns.

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

## Owning documents

- [`scientific-model-hierarchy.md`](scientific-model-hierarchy.md) owns the nominal
  scientific taxonomy and the distinction between dimensional, defect, toy, and
  material-reference identities.
- [`campaign-execution.md`](campaign-execution.md) owns the separation between
  immutable campaign records and executable campaign Actions or Workflows.
- [`catalogs-and-comparison.md`](catalogs-and-comparison.md) owns explicit toy-model
  iteration and compatibility-gated comparison.
- [`migration.md`](migration.md) maps current source surfaces to the target without
  rewriting retained evidence.
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
campaign-execution
catalogs-and-comparison
migration
periodic1d/index
periodic2d/index
periodic3d/index
```
