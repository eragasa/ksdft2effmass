# Source package ownership

This document records where maintained Python code belongs today. It is derived from
`python/src/ksdft2effmass/` and does not authorize a package migration, compatibility
layer, or new framework.

Selected package, module, and class contracts are documented in the canonical
[`ksdft2effmass` source mirror](ksdft2effmass/index.md). Prospective pages there are
explicitly labeled and do not claim implemented or supported source.

## Ownership map

| Package | Owns | Does not own |
|---|---|---|
| `operators` | KSD Hamiltonian wrappers, spectral subspaces, operator compression, residual policy, operator records, compatibility, matrix comparison, and the retained complex-Hermitian sparse solver boundary | Generic quantities, matrix verification, real-symmetric spectral decomposition, state-space ownership, lattices, Bloch paths, hopping models, scientific campaigns, or external calculators |
| `spaces` | Prospective finite state-space and subspace identities, injections, and intrinsic invariants; the initial documented leaf is the analytical trial subspace | Hamiltonians, operator reduction, scientific model construction, or experiment composition |
| `solidstate` | Lattices, reciprocal paths, boundary twists, band frames, gauge alignment, hopping transforms, Wilson loops, and finite-lattice operator construction | Generic matrix utilities, campaign policy, or external-tool integration |
| `model_systems` | Controlled physical and mathematical systems, shared finite-domain geometry, exact solutions, finite representations, and model-specific comparisons | General-purpose analysis, campaign authority, or external-tool integration |
| `analysis` | Calculator-independent scientific analyses, model-adequacy calculations, and quantities of interest | Model definitions, campaign orchestration, native file formats, or execution authority |
| `campaigns` | Project-specific composition of declared inputs, analyses, verification, retained results, and campaign serialization | Reusable mathematics already owned by `operators`, `solidstate`, or `analysis` |
| `periodic1d` and `periodic2d` | Existing dimension-specific controlled-model capabilities and their established public APIs | Generic operator, lattice, workflow, or provenance infrastructure |
| `periodic` | The existing periodic-model hierarchy, toy-model catalog, and explicitly transitional imports | New representation or transformation frameworks |
| `calculators` | Calculator-facing requests and calculator-independent execution contracts | Native-format decoding or campaign acceptance policy |
| `integration` | Native calculator/file-format adapters such as Quantum ESPRESSO and Wannier90 integration | Generic scientific analysis or workflow policy |
| `workflows` | Calculator-independent task, workflow, gate, run-state, and execution-authority contracts | Scientific algorithms and native external-tool behavior |
| `provenance` | Portable artifact, execution, lineage, and external-tool provenance records | Scientific validity or campaign-specific result meaning |
| `serialization` | Shared typed JSON contracts, scientific-value normalization, mapping byte actions, and final typed-record boundaries | Domain schemas, filesystem persistence, provenance policy, or scientific interpretation |
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
- [`calculations/`](calculations/implementation.md) is an inventory of retained or
  historical calculation packages. Its implementation contract defines the target
  staged execution-package layout and the boundary between pre-arXiv execution identity
  and publication versioning. Hash-bound executable files are evidence bytes and are
  not rewritten merely to match current source organization. New reusable behavior is
  not added there. An unsealed calculation that is migrated uses installed library
  behavior and retains only thin calculation-specific entry points.

There is no top-level `campaigns/` source tree. In repository documentation,
“campaign library” means `python/src/ksdft2effmass/campaigns/`.

The QHO1D and PIAB1D vertical slices are owned directly by
`model_systems/qho1d/` and `model_systems/piab1d/`. Their `study/` subpackages preserve
historical retained-result contracts. The PIAB1D and QHO1D successors use typed root
records, independent reference analyzers, and authenticated visualization data outside
the historical study wire. `model_systems/study/base.py` defines the nominal identity
boundary consumed by historical serializers. `QHO1D` and `Piab1d` are
intentionally dimension-specific names; a plain `QHO` or `PIAB` owner is reserved for
a future implementation with a reviewed dimension-neutral contract. The QHO1D and
PIAB1D composition roots are consolidated under `calculations/qho1d/` and
`calculations/piab1d/`. Both implement direct calculate → verify → render successors;
QHO1D retains its predecessor development surface separately, while PIAB1D retains its
historical flat calculation surface. Each calculation owner also owns its paths,
provenance, verification composition, plots, and technical report. The former top-level
`campaigns/qho1d/` and `campaigns/piab1d/` packages are not retained as compatibility
facades. Reusable finite-operator analyses live under
`analysis/operators/`. Research-monograph documentation points to the canonical
calculation rather than owning another implementation or calculation tree. The
`campaigns.research_monograph` root retains only unrelated bounded adapters still
required by their calculation owners.

## Placement rule

Before creating a package or module, identify a current caller and use the narrowest
existing owner:

1. Put representation-independent matrix behavior in `operators`.
2. Put finite state-space and subspace identities, injections, and intrinsic invariants
   in `spaces` when they are independent of one represented operator.
3. Put controlled physical or mathematical systems and their finite realizations in
   `model_systems`.
4. Put lattice-, Bloch-, frame-, gauge-, or hopping-specific behavior in `solidstate`.
5. Put reusable scientific interpretation in `analysis`.
6. Put experiment or retained-result composition in the existing campaign/capability
   owner.
7. Put external syntax and tool adaptation in `integration`.
8. Put task/run state in `workflows` and evidence lineage in `provenance`.

Do not create a parallel `representation`, `representations`, `transformation`, or
`transformations` hierarchy merely to rename existing concepts. Introduce a new owner
only when a real caller cannot coherently use an existing one.

## Existing overlap

The tree contains both capability packages (`periodic1d`, `periodic2d`) and remaining
campaign packages (`campaigns/periodic_1d` and others). This is current
source state, not a template for duplication. New work stays with the established owner
of the edited capability. A later migration requires its own caller inventory and must
update supported imports directly rather than add a compatibility facade.

## YAGNI boundary

Do not add identities, registries, graph services, generic transformation bases,
serializers, schemas, or metadata aggregates until a maintained caller needs that exact
contract. Prefer deleting an unused abstraction over documenting it as future
architecture.
