# Source package ownership

This document records where maintained Python code belongs today. It is derived from
`python/src/ksdft2effmass/` and does not authorize a package migration, compatibility
layer, or new framework.

## Ownership map

| Package | Owns | Does not own |
|---|---|---|
| `operators` | Generic finite represented matrices, units, operator records, eigensolvers, subspace compression, residuals, compatibility, and matrix comparison | Lattices, Bloch paths, hopping models, scientific campaigns, or external calculators |
| `solid_state` | Lattices, reciprocal paths, boundary twists, band frames, gauge alignment, hopping transforms, Wilson loops, and finite-lattice operator construction | Generic matrix utilities, campaign policy, or external-tool integration |
| `analysis` | Calculator-independent scientific analyses, model-adequacy calculations, quantities of interest, and controlled model systems | Campaign orchestration, native file formats, or execution authority |
| `campaigns` | Project-specific composition of declared inputs, analyses, verification, retained results, and campaign serialization | Reusable mathematics already owned by `operators`, `solid_state`, or `analysis` |
| `periodic1d` and `periodic2d` | Existing dimension-specific controlled-model capabilities and their established public APIs | Generic operator, lattice, workflow, or provenance infrastructure |
| `periodic` | The existing periodic-model hierarchy, toy-model catalog, and explicitly transitional imports | New representation or transformation frameworks |
| `calculators` | Calculator-facing requests and calculator-independent execution contracts | Native-format decoding or campaign acceptance policy |
| `integration` | Native calculator/file-format adapters such as Quantum ESPRESSO and Wannier90 integration | Generic scientific analysis or workflow policy |
| `workflows` | Calculator-independent task, workflow, gate, run-state, and execution-authority contracts | Scientific algorithms and native external-tool behavior |
| `provenance` | Portable artifact, execution, lineage, and external-tool provenance records | Scientific validity or campaign-specific result meaning |
| `serialization` | Shared serialization contracts only | Domain schemas that belong beside their domain or campaign owner |
| `structures` | Atomic periodic-structure records | Finite represented matrices or lattice-model calculations |
| `electronic_structure` | General electronic-structure sampling records | Calculator execution or campaign composition |

## Repository-tree boundary

The three similarly named source areas have different roles:

- `python/src/ksdft2effmass/campaigns/` owns importable campaign definitions,
  calculations, result records, verification, schemas, and serialization.
- `experiments/` owns protocols, declared parameter selections, thin executable and
  plotting entry points, and lifecycle-appropriate outputs. New or mutable experiments
  must not contain a second installable implementation package or an experiment-local
  dependency lock. Tests for installed campaign behavior belong under `python/tests/`.
  An immutable retained version may preserve hash-bound source and lock bytes as part of
  its evidence package; that exception is not a template for new development.
- `calculations/` is an inventory of retained or historical calculation packages.
  Hash-bound executable files are evidence bytes and are not rewritten merely to match
  current source organization. New reusable behavior is not added there. An unsealed
  calculation that is migrated uses installed library behavior and retains at most a
  thin input/output adapter.

There is no top-level `campaigns/` source tree. In repository documentation,
“campaign library” means `python/src/ksdft2effmass/campaigns/`.

## Placement rule

Before creating a package or module, identify a current caller and use the narrowest
existing owner:

1. Put representation-independent matrix behavior in `operators`.
2. Put lattice-, Bloch-, frame-, gauge-, or hopping-specific behavior in `solid_state`.
3. Put reusable scientific interpretation in `analysis`.
4. Put experiment or retained-result composition in the existing campaign/capability
   owner.
5. Put external syntax and tool adaptation in `integration`.
6. Put task/run state in `workflows` and evidence lineage in `provenance`.

Do not create a parallel `representation`, `representations`, `transformation`, or
`transformations` hierarchy merely to rename existing concepts. Introduce a new owner
only when a real caller cannot coherently use an existing one.

## Existing overlap

The tree contains both capability packages (`periodic1d`, `periodic2d`) and campaign
packages (`campaigns/periodic_1d`, `campaigns/piab1d`, and others). This is current
source state, not a template for duplication. New work stays with the established owner
of the edited capability. A later migration requires its own caller inventory and must
update supported imports directly rather than add a compatibility facade.

## YAGNI boundary

Do not add identities, registries, graph services, generic transformation bases,
serializers, schemas, or metadata aggregates until a maintained caller needs that exact
contract. Prefer deleting an unused abstraction over documenting it as future
architecture.
