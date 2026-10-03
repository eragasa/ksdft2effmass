# Migration phase 4: scientific-retention owners

## Status

**Implemented on the work branch.** Phase 3 established encoded-document ownership.
Phase 4 now supplies campaign-independent scientific-retention records and binding
Actions. No concrete periodic campaign was migrated and no new calculation was
executed. This status does not mean merged, reviewed, released, or scientifically
validated.

## Purpose

Introduce the typed scientific objects required to distinguish a modeled periodic
system, retained mathematical space, exact retained operator, and finite represented
operator. The phase must not treat an operator, matrix, or preserved document as a
`PeriodicModel`.

The complete contract is owned by
[`retained-spaces-and-operators.md`](retained-spaces-and-operators.md). This page owns
migration scope, implementation order, and completion gates.

## Accepted phase boundary

Phase 4 uses stable immutable parent identities instead of embedding arbitrary concrete
parent implementations. `PeriodicOperatorReference` records model, operator,
state-space, and spatial-dimension identities. Identity resolution, filesystem access,
artifact loading, and concrete numerical construction remain separate future Actions.

This phase supplies no generic encoded-document abstraction, generic operator factory,
repository loader, model registry, persistence schema, or polymorphic DataObject base.

## Required public owners

Phase 4 introduces the following supported route from `ksdft2effmass.periodic`:

1. **`PeriodicRetentionKind`.** Closed construction classification for spectral
   restriction, selected-band retention, and disentangled subspaces.
2. **`PeriodicRetainedOperatorConstructionKind`.** Distinguishes restriction to the
   retained domain/codomain from ambient-space compression.
3. **`PeriodicHermiticityStatus`.** Records whether Hermiticity is declared,
   non-Hermiticity is declared, or no assessment is recorded; it is not a numerical
   analyzer result.
4. **`PeriodicOperatorReference`.** Stable parent model/operator/state-space identity
   with exact dimension.
5. **`PeriodicRetentionDefinition`.** Parent-qualified selection identity, rank,
   ordered retained labels, reciprocal-domain identity, assumptions, construction
   record, and provenance.
6. **`PeriodicRetainedSubspace`.** Retained-space identity with ambient dimension,
   projector-or-frame record, spin, internal-degree, reciprocal-boundary, and
   provenance conventions.
7. **`PeriodicRetainedOperator`.** Exact operator identity whose domain and codomain
   are the retained space, with parent, construction, energy reference, Hermiticity
   declaration, and provenance.
8. **`PeriodicRepresentedRetainedOperator`.** Binding between the exact retained
   operator and one `OperatorRecord`, with representation-map, gauge, and provenance
   identity.
9. **Construction ActionObjects.** `PeriodicRetainedSubspaceConstructor`,
   `PeriodicRetainedOperatorConstructor`, and
   `PeriodicRepresentedRetainedOperatorConstructor` provide the supported explicit
   construction routes and reject incompatible inputs.

All records are frozen and slotted. They preserve exact identity spelling and ordering;
they do not trim, normalize, reorder, convert, infer, or repair scientific metadata.

## Construction sequence

The implementation sequence is:

```text
PeriodicOperatorReference
        +
PeriodicRetentionDefinition
        |
        v
PeriodicRetainedSubspaceConstructor
        |
        v
PeriodicRetainedSubspace
        +
exact-operator metadata
        |
        v
PeriodicRetainedOperatorConstructor
        |
        v
PeriodicRetainedOperator
        +
OperatorRecord + representation/gauge identities
        |
        v
PeriodicRepresentedRetainedOperatorConstructor
        |
        v
PeriodicRepresentedRetainedOperator
```

Each output is a typed immutable construction result in the ordinary semantic sense;
no redundant one-field `...Result` wrapper is introduced. Dedicated ResultObjects will
be added only when an operation has multiple outputs or diagnostics that need their own
contract.

## Intrinsic and cross-object invariants

### Parent and retention definition

- IDs and conventions are nonempty exact strings.
- Spatial dimension is exactly a built-in integer in `{1, 2, 3}`.
- Rank is exactly a positive built-in integer.
- Ordered retained labels are a nonempty tuple of unique nonempty strings whose length
  equals rank.
- Assumption identifiers are an ordered tuple of unique nonempty strings.
- Retention kind is an exact enum member.

### Retained space

- The definition's parent state-space identity equals the declared ambient state-space
  identity.
- Ambient dimension is a positive built-in integer not smaller than retained rank.
- Projector-or-frame, spin, internal-degree, reciprocal-boundary, and provenance
  identities are nonempty.
- No orthogonality, smoothness, isolation, or topology claim is inferred from these
  identities.

### Exact retained operator

- Parent reference exactly equals the retained definition's parent reference.
- Domain and codomain are the one retained-space identity.
- Construction kind, `EnergyReference`, Hermiticity declaration, and provenance have
  exact semantic types.
- A Hermiticity declaration is not substituted for represented numerical analysis.

### Represented retained operator

- The finite `OperatorRecord` state-space identifier equals the retained-space
  identifier.
- Its state-space and matrix dimension equal retained rank.
- Its basis ordering equals the ordered retained labels.
- Its energy unit and energy-zero convention exactly equal those of the exact retained
  operator.
- Representation-map, gauge, and provenance identities are nonempty.
- Geometry remains owned by `OperatorRecord`; exact binding does not establish physical
  compatibility with another represented operator.

## Existing mechanics and later composition

Applicable existing mechanics remain unchanged:

- `ContiguousBandSelection`;
- `OrthogonalSpectralSubspace`;
- `ReciprocalBandFramePath1D`;
- `ReciprocalOperatorSamples1D`;
- `OperatorCompressionResult`;
- `OperatorRecord`; and
- `ScalarFiniteLatticeOperator` where its finite-periodic scalar contract applies.

These are numerical or represented data, not the scientific owners introduced here.
Phase 5 connects selected one-dimensional results to phase-4 identities through
specialized constructions. Phase 4 neither moves these classes nor widens their public
contracts.

## Required separations

- Retained-space identity is distinct from a gauge-dependent frame representation.
- The exact retained operator is distinct from an ambient compression and every finite
  matrix representation.
- Complete Fourier transformation is distinct from truncation or fitting.
- An effective model is distinct from the exact retained operator it approximates.
- Alignment diagnostics are distinct from the directional transport map.
- Scalar energy alignment is distinct from unitary or partial-isometry transport.
- A stable parent identity is distinct from resolving or loading a parent object.
- Scientific retention is distinct from preserving evidence bytes.

## Verification plan

Focused software-verification tests establish:

- exact enum values and supported public imports;
- strict scalar and tuple type rejection, including Boolean and numeric-string cases;
- immutable identity propagation;
- retained rank, ambient dimension, and ordered-label invariants;
- parent-reference agreement through retained-space and retained-operator construction;
- represented state-space, matrix, basis-ordering, and energy-reference agreement; and
- explicit rejection of incompatible construction inputs.

The tests use synthetic records and make no claim of numerical verification,
scientific validation, uncertainty quantification, projector adequacy, gauge
smoothness, or material realism.

## Documentation deliverables

- the architecture contract and equations in
  `retained-spaces-and-operators.md`;
- this bounded migration plan;
- complete NumPy-style public source documentation in `retention.py`;
- a Sphinx concept page explaining the four-layer separation;
- a Sphinx API page exposing only the supported `ksdft2effmass.periodic` route; and
- synchronized package exports and navigation.

The monograph is an input reference and is not modified by this phase.

## Excluded work

Phase 4 does not:

- migrate concrete 1D, 2D, or 3D models;
- connect retained campaign results to the new owners;
- populate the toy catalog;
- run Quantum ESPRESSO, Wannier90, or any campaign;
- define graphene or silicon material-reference physics;
- authorize pristine/defect subtraction;
- select or align gauges;
- define effective-model fitting or truncation;
- define a wire format or persistence migration; or
- claim a proof, numerical result, scientific validation, or uncertainty
  quantification.

## Completion gate

- Public contracts document parentage, domain/codomain, rank, construction, units,
  gauge, energy reference, geometry ownership, and provenance.
- Runtime validation rejects wrong semantic types and incompatible identities or
  dimensions.
- DataObjects remain immutable, and Actions own supported reusable construction.
- Tests establish construction, invalid-input rejection, identity propagation, and
  represented-dimension agreement without broader scientific claims.
- Exports and Sphinx documentation expose only deliberately supported routes.
- Source and targeted tests pass Ruff, formatting, mypy, pytest, Sphinx
  warnings-as-errors, links, and `git diff --check`.
