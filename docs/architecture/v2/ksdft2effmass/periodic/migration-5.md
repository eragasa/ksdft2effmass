# Migration phase 5: periodic1d scientific adoption

## Status

**In implementation on the work branch.** Existing Appendix G calculations and typed
results remain evidence. Row 023 used one separately authorized deterministic local
replay solely to retain previously omitted compact frame/projector and effective-model
artifacts; historical files remain unchanged. Completed rows are listed below. This
status does not mean merged, reviewed, released, or scientifically validated.

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

- [x] `PERIODIC-XWALK-011`: move `Periodic1DFiniteHoppingToyModel` and its
  intrinsic hopping-block data to canonical `periodic1d` ownership, add stable
  configured-model identity and nominal `Periodic1DModel` membership, and retain
  the ordered blocks, energy unit, absolute Hermiticity tolerance, and existing
  primitive/supercell numerical constructors without a campaign-owned model alias.
- [x] `PERIODIC-XWALK-014`: keep `BlockHoppingModel1D` as reusable coefficient
  data; classify complete centered-mesh Fourier transforms as representations of
  exact retained operators; and construct separately identified truncation- and
  fit-derived effective models through distinct result types without changing
  coefficients, representatives, units, or numerical route results.
- [x] `PERIODIC-XWALK-017`: keep `PeriodicFourierPotential1D` as reusable
  potential data and compose it into the complete
  `Periodic1DFourierHamiltonianToyModel`, whose stable model, Bloch state-space,
  primitive reciprocal-domain, potential, positive recoil-energy scale, nominal
  one-dimensional membership, and exact toy role identify the untruncated parent
  separately from any finite matrix representation.
- [x] `PERIODIC-XWALK-018`: rename `Periodic1DBasisScramblingModel` to
  `Periodic1DBasisScramblingDefinition`, make the numerical request refer to the
  definition explicitly, and retain the site, orbital, phase, spin, map-direction,
  and unitary construction conventions without a compatibility alias.
- [x] `PERIODIC-XWALK-019`: keep `ContiguousBandSelection` as reusable numerical
  selection data and compose it into the parent-qualified
  `Periodic1DSelectedBandRetentionDefinition` under canonical `periodic1d`
  ownership. The aggregate requires a one-dimensional parent, selected-band kind,
  and exact rank/count agreement without constructing a subspace or gauge.
- [x] `PERIODIC-XWALK-020`: replace the campaign-local retained-band group with
  canonical `Periodic1DRetainedBandGroupDefinition`, compose each schema-one group
  with the explicit Fourier parent and a complete parent-qualified selected-band
  retention definition, and preserve the historical encoded JSON bytes.
- [x] `PERIODIC-XWALK-021`: keep `OrthogonalSpectralSubspace` as reusable numerical
  eigenspace data and compose it with a parent-qualified one-dimensional retained
  space through `Periodic1DOrthogonalSpectralRetainedSubspace`, requiring exact
  retained-rank and ambient-dimension agreement.
- [x] `PERIODIC-XWALK-022`: keep `ReciprocalBandFramePath1D` as gauge-dependent
  represented frame data and bind it separately to the scientific retained space
  through `Periodic1DBandFrameRetainedSubspace`, preserving rank, ambient dimension,
  mesh, frame order, sewing map, and the distinction between frame and subspace.
- [x] `PERIODIC-XWALK-023`: preserve the historical aggregate diagnostic result and
  exact source bytes; retain an authenticated deterministic replay sidecar containing
  the rank-one frame, reconstructed-projector identity, and separate complete,
  truncated, and directly fitted coefficient routes; then construct the complete
  Fourier parent, selected-band retention, retained mathematical space, represented
  frame, exact retained operator, one zone-center finite representation, complete
  hopping representation, and separately identified truncated and fitted effective
  models. The ordinary route tolerance defaults to the documented campaign policy of
  $10^{-10}$ and remains software/numerical verification rather than validation or UQ.
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
models, alter historical Appendix G files, perform unapproved production or external
calculations, or promote numerical verification to scientific validation. The
separately authorized row-023 replay was bounded to the frozen local illustrative
input and retained new provenance-bound sidecar artifacts.

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
