# `ksdft2effmass.periodic1d`

## Scientific question and status

How can one-dimensional periodic parent models, retained bands or band groups, aligned
representations, and finite-range hopping descriptions be calculated, independently
checked, and presented without confusing their state spaces, gauges, numerical errors,
or scientific families?

This Architecture v3 surface is an **active family-by-family rewrite**. Phase 1
Mathieu1D, Phase 2 compatible rank-one Fourier locality, the Phase 3 rank-two
composite-alignment family, and the confirmatory Phase 4 constrained-admissible-set
family are implemented with typed source records, direct calculation stages,
byte-owning verification, and authenticated rendering. Mathieu1D has one retained
unsealed execution; the locality and admissible-set successors have only provisional
non-retained review results. The Mathieu1D, M1, and M2 predecessor runtimes are absent
from the live tree. Four studies remain prospective, including the distinct rank-two
band-equivalence family.

The rewrite adopts the behavioral structure demonstrated by PIAB1D and QHO1D and now
implemented directly by Mathieu1D:

```text
Python-authored typed configuration
              ↓
model-owned analysis → typed result bytes
              ↓
byte-owning independent verification
              ↓
authenticated typed visualization projection
              ↓
closed calculate → verify → render calculation stages
```

It does **not** make Periodic1D one universal calculation or impose one result layout on
scientifically distinct periodic families.

## Ownership

`ksdft2effmass.periodic1d` owns one-dimensional periodic reduction and model-adequacy
behavior whose meaning is specific to the periodic program:

- scalar Fourier reduction and hopping-locality analysis;
- composite-band frame alignment and represented-operator locality;
- band-equivalence and constrained-admissible-set composition;
- family-specific typed configurations, results, verification values, and visualization
  projections; and
- deliberate public imports for those maintained families.

Neighboring owners remain distinct:

| Owner | Responsibility |
|---|---|
| `ksdft2effmass.model_systems.periodic_1d` | Unit-aware finite Fourier potentials and plane-wave or periodic finite-difference fiber construction. |
| [`ksdft2effmass.model_systems.mathieu1d`](../model_systems/mathieu1d/index.md) | The concrete implemented Mathieu1D parent and its own direct vertical slice. |
| `ksdft2effmass.solidstate` | Lattices, reciprocal paths, sewing, frames, gauge alignment, hopping transforms, and Wilson-loop behavior. |
| `ksdft2effmass.operators` and `ksdft2effmass.analysis` | Representation-independent operator values and reusable analyses. |
| `projectkoios.physkit` | Reusable lattice primitives, quantities, canonical represented linear algebra, and matrix norms. |
| `calculations/periodic1d/` and `calculations/mathieu1d/` | Scientific family selection, protocol, thresholds, execution records, evidence policy, provenance, rendering inventory, and reports. |

No installed package imports a calculation tree. Quantum ESPRESSO and Wannier90 retain
ownership of first-principles electronic-structure calculation and Wannier localization.

## Study boundaries

The rewrite contains **eight separate calculation studies**. Implementations may share
behavior, but the studies do not share protocols, thresholds, result wires, evidence
status, or conclusions:

| Study | Distinguishing question | Architecture disposition |
|---|---|---|
| 1. Mathieu1D single-band Fourier reduction | How do two finite parent representations support one scalar retained-band reduction? | Implemented [`model_systems.mathieu1d`](../model_systems/mathieu1d/index.md) vertical slice and `calculations/mathieu1d/`; not the rank-one specialization below. |
| 2. Compatible rank-one Fourier locality | What scalar locality baseline remains when internal gauge action is operator-trivial? | Implemented typed source under [`periodic1d.fourier_locality`](fourier_locality/index.md) with direct stages and provisional non-retained report material under `calculations/periodic1d/rank1/fourier-locality/`; the legacy M1 runtime is retired. |
| 3. Rank-two band equivalence versus hopping locality | Can analytically or certifiably band-equivalent represented Hamiltonians have different finite-range locality? | Separate typed source child and calculation owner. |
| 4. Rank-two composite-band alignment and locality | How do declared pointwise or global alignment choices affect block hoppings and diagnostics? | Implemented direct typed lifecycle under [`periodic1d.composite_band_alignment`](composite_band_alignment/index.md) and `calculations/periodic1d/rank2/composite-band-alignment-locality/`; no retained execution exists. |
| 5. Confirmatory constrained admissible sets | Does one common candidate satisfy all prespecified spectral and operator thresholds? | Implemented authenticated source lifecycle at [`periodic1d.admissible_sets`](admissible_sets/index.md); no retained successor execution exists. |
| 6. Minimal scalar/direct admissible-set demonstration | Can a bounded scalar construction exhibit the declared witness or separation property? | Separate analytical or numerical control; never a substitute for study 5. |
| 7. Post-hoc threshold sensitivity | How do dispositions change across one complete declared finite threshold inventory? | Separate post-hoc analysis that cannot mutate study 5. |
| 8. Higher-rank composite alignment | Which alignment and locality behavior persists at declared ranks greater than two? | Separate calculation family; reuse only behavior with unchanged meaning. |

The eight studies do not require eight reusable source children. In particular, one
cohesive `periodic1d.admissible_sets` owner may supply behavior to studies 5--7 while
their calculation records remain separate. Historical labels M1, M2, and M3 remain
searchable provenance aliases; they are not names for new studies or a version chain.

## Architectural invariants

- Every maintained scientific record is immutable, typed, and constructor-validated.
- Public numeric APIs reject booleans, numeric strings, nonfinite values, and inconsistent
  units or shapes unless a narrower contract explicitly admits them.
- Basis, state space, coordinate order, gauge, energy reference, units, reciprocal
  convention, and finite geometry are explicit before operators are compared.
- Projection, alignment, basis transformation, truncation, and fitting remain different
  operations and different result sections.
- Parent-model, finite-representation, reciprocal-sampling, eigensolver, alignment,
  Fourier-reconstruction, and truncation errors are not pooled.
- Verifiers own the exact result wire bytes, derive their SHA-256 digests internally,
  and do not call production analyzers.
- Serialization owns representation only; it does not own hashing, filesystem effects,
  verification policy, or scientific interpretation.
- Rendering consumes only a passing verification and its authenticated typed projection.
- Calculation scripts use direct module-scope composition and contain no Workflow,
  `main()`, argument parser, JSON-authored scientific input, or reusable kernel.
- Historical bytes are not rewritten into successor wires; retired predecessor payloads remain recoverable only through recorded Git identities.
- Passing software and bounded numerical checks do not establish continuum convergence,
  uncertainty quantification, material validity, publication acceptance, or release.

## Detailed plan

- [Compatible rank-one Fourier-locality architecture](fourier_locality/index.md)
- [Rank-two composite-band alignment/locality architecture](composite_band_alignment/index.md)
- [Constrained-admissible-set architecture](admissible_sets/index.md)
- [Implementation](implementation.md)
- [Numerical contract](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Schematics](schematics.md)
- [Direct run-script template](direct-scripts.md)
- [Visualization migration plan](visualizations.md)
- [Migration sequence](migration.md)
- [Phase 0 inventory and replacement boundary](phase-0-inventory.md)
- [Phase 2 legacy retirement record](../../../../../calculations/periodic1d/rank1/fourier-locality/legacy-retirement.md)
- [M2 legacy retirement record](../../../../../calculations/periodic1d/rank2/composite-band-alignment-locality/legacy-retirement.md)
- [Formal-method boundary](formal.md)
