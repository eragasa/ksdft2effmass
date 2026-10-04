# Migration phase 7: periodic2d scientific adoption

## Status

**In implementation on the work branch.** The cosine-potential toy parent and
scalar-hopping finite-extent defect now have nominal scientific-model membership, and
the general plane-wave representation definition remains explicitly separate.
Retained-space/operator adoption and campaign decomposition remain incomplete.

## Purpose

Apply the general hierarchy and scientific-retention contracts to periodic2d while
finishing capability parity with applicable periodic1d coverage.

## Included crosswalk entries

Phase 7 primarily implements:

- `PERIODIC-XWALK-010` and `PERIODIC-XWALK-012`;
- two-dimensional portions of `PERIODIC-XWALK-016` and
  `PERIODIC-XWALK-028` through `PERIODIC-XWALK-036`; and
- campaign families `PERIODIC-XWALK-067` through `PERIODIC-XWALK-072`.

## Scientific-model progress

- [x] `PERIODIC-XWALK-010`: adopt `Periodic2DCosinePotentialToyModel` into nominal
  `Periodic2DModel` membership with a stable family identity and exact toy role while
  preserving the dimensionless period-$2\pi$ equation and separate represented
  operators.
- [x] `PERIODIC-XWALK-012`: rename the colliding concrete defect record to
  `Periodic2DScalarHoppingDefectModel`, adopt nominal `Periodic2DDefectModel`
  membership, retain its configured and pristine-parent identities, and assign the
  exact controlled-toy role without permitting a material-reference relabeling.
- [x] `PERIODIC-XWALK-016`: retain `PlaneWaveBlochHamiltonian2DModel` as the
  established numerical name for a finite representation definition, not a nominal
  scientific model; its result remains the represented operator.

These changes establish model identity and parentage only. They do not register a toy
catalog, construct retained spaces/operators, alter campaign payloads, or establish
scientific validation.

## Represented-operator progress

- [x] `PERIODIC-XWALK-033`: keep the general 2D continuum plane-wave result as
  reusable represented-space output with its complete request, explicit identities,
  PhysKit lattice geometry, matrix unit, basis order, and duality evidence.
- [x] `PERIODIC-XWALK-034`: retain the cosine-model result as a campaign adapter whose
  constructor delegates the actual matrix assembly to the general 2D plane-wave
  constructor while preserving exact campaign correlation.
- [ ] `PERIODIC-XWALK-035`: reusable finite-difference ownership remains blocked until
  the currently implicit dimensionless matrix convention is replaced by explicit
  general state-space, ordered-basis, energy-reference, unit, and provenance metadata.
  Grid order and Bloch-seam direction must remain unchanged.
- [x] `PERIODIC-XWALK-036`: keep the common-space object as a threshold-free comparison
  result with an explicit directional transport, signed difference, and intrinsically
  correlated norms; it is neither a represented operator nor acceptance policy.

These dispositions complete the demonstrated plane-wave adapter and common-space
comparison boundaries without claiming overall Phase 7 completion. Missing metadata
for row 035 are not inferred from the toy-model implementation.

## Required migration

1. Migrate `Periodic2DCosinePotentialToyModel` into nominal `Periodic2DModel`
   membership with stable identity and unchanged equation and coefficient conventions.
2. Rename the concrete scalar-hopping `Periodic2DDefectModel` to eliminate collision
   with the nominal defect base, then adopt nominal defect membership with explicit
   parent identity.
3. Connect selected-band and composite-subspace studies to phase-4 retained spaces and
   operators.
4. Preserve distinctions among plane-wave continuum construction, finite-difference
   representation, reciprocal-mesh topology, finite-cutoff sewing, finite-periodic
   hopping, and transported common-space comparison.
5. Decompose isolated, composite, topology, effective-mass, and Wannier90 outputs into
   typed results without changing preserved campaign documents.
6. Complete stress controls, gauge/alignment, hopping transforms, route reconciliation,
   serializers, verification, tests, API documentation, and concept documentation as
   required by the
   [periodic2d capability-parity gate](../periodic2d-capability-parity.md).

## PhysKit boundary

Continue to use PhysKit direct/reciprocal lattice and applicable finite-periodic
operator constructors. Do not substitute finite-periodic scalar hopping construction
for continuum plane-wave construction. Any later migration of the temporary 2D
continuum builder to PhysKit requires a separate accepted dependency contract.

## Defect gate

No new periodic2d defect campaign proceeds until parent-model, retained-space,
represented-operator, alignment, energy-reference, compatibility, and comparison
prerequisites pass. Existing defect evidence remains unchanged.

## Excluded work

Phase 7 does not define graphene material-reference physics without a specification,
access native archives, execute Wannier90 or electronic-structure software, or claim
scientific validation from parity checks.

## Completion gate

- Concrete 2D models have correct nominal membership and stable identities.
- Retained spaces/operators and represented results identify parents, bases, gauges,
  units, geometry, and energy references.
- Periodic2d parity requirements have terminal implemented or explicitly unavailable
  dispositions.
- Encoded documents, digests, provenance, and historical experiment identifiers remain
  unchanged.
- Relevant tests, verifier CLIs, typing, Ruff, formatting, Sphinx, links, and diff
  checks pass.
