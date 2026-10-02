# Migration phase 5: periodic1d scientific adoption

## Status

**In implementation on the work branch.** Existing Appendix G calculations and typed
results remain evidence; this phase does not rerun them. Completed rows are listed
below. This status does not mean merged, reviewed, released, or scientifically
validated.

## Purpose

Migrate the best-defined one-dimensional scientific models first and connect their
existing represented evidence to the phase-4 retention contracts.

## Included crosswalk entries

Phase 5 primarily implements:

- model candidates `PERIODIC-XWALK-011` and `PERIODIC-XWALK-013` through
  `PERIODIC-XWALK-018`;
- retention and operator mappings `PERIODIC-XWALK-019` through
  `PERIODIC-XWALK-033` where one-dimensional; and
- campaign families `PERIODIC-XWALK-058` through `PERIODIC-XWALK-066`.

## Implementation progress

- [x] `PERIODIC-XWALK-019`: keep `ContiguousBandSelection` as reusable numerical
  selection data and compose it into the parent-qualified
  `Periodic1DSelectedBandRetentionDefinition` under canonical `periodic1d`
  ownership. The aggregate requires a one-dimensional parent, selected-band kind,
  and exact rank/count agreement without constructing a subspace or gauge.
- [ ] Remaining Phase 5 rows are not implemented by this entry.

## Required migration

1. Define a complete 1D periodic parent model rather than treating
   `PeriodicFourierPotential1D` as the whole system.
2. Migrate `Periodic1DFiniteHoppingToyModel` into nominal `Periodic1DModel`
   membership with stable identity and unchanged block semantics.
3. Treat `Periodic1DGaussianOnsiteDefectModel` as a perturbation definition until a
   separate defect model composes it with an explicit pristine parent.
4. Connect isolated and composite band selections to parent-qualified retained spaces
   and exact retained operators.
5. Distinguish complete `BlockHoppingModel1D` representations from truncated or fitted
   effective models through their construction Results.
6. Migrate canonical new ownership from `ksdft2effmass.campaigns.periodic_1d` toward
   `ksdft2effmass.periodic1d` without preserving obsolete alpha import aliases.
7. Keep campaign definitions, execution, serializers, and verification outside the
   scientific-model hierarchy.

## Appendix G preservation

The migration preserves:

- lattice, reciprocal, energy, and dimensionless conventions;
- band and group ordering;
- frame, gauge, hopping, and Fourier conventions;
- exact encoded campaign documents and identities;
- complete versus truncated/fitted route identity;
- training and withheld sample separation; and
- the evidentiary status of every retained result.

## Excluded work

Phase 5 does not generalize 1D formulas to 2D or 3D by notation, register incomplete
models, alter Appendix G, rerun calculations, or promote numerical verification to
scientific validation.

## Completion gate

- Every migrated concrete model has nominal 1D membership, stable identity, exact role,
  and complete documented physical/numerical conventions.
- Retained spaces and operators identify their parents and represented coordinates.
- Exact and approximate hopping objects cannot be confused by type or construction
  result.
- Campaigns consume models and scientific objects without becoming their bases.
- Existing encoded bytes and digests remain unchanged.
- Affected software and numerical tests, retained verifier CLIs, typing, formatting,
  Ruff, Sphinx, links, and diff checks pass.
