# Sewing abstractions

## Purpose

`ksdft2effmass.sewing` owns the dimension-neutral abstract classes for explicit
identification between scientifically related state spaces. The package names the
mathematical sewing categories without moving concrete reciprocal, symmetry,
projected-subspace, or finite-boundary mechanics away from their domain owners.

## Abstract hierarchy

```text
IdentityReciprocalSewing
EmbeddedPositionReciprocalSewing
PermutationPhaseReciprocalSewing
PlaneWaveIndexSewing
ProjectedSubspaceSewing
SymmetrySewing
FiniteBoundarySewing
```

The seven peer classes are abstract. They preserve scientifically
distinct applicability conditions:

- exact coordinate periodicity;
- position-phase sewing derived from an ordered embedding;
- declared endpoint permutation and phases;
- reciprocal-index relabeling in a plane-wave representation;
- restriction of an admitted ambient sewing map to selected subspaces;
- unitary or antiunitary symmetry action; and
- identification across a finite real-space quotient seam.

No shared source type, target type, request, result, basis identity, map direction, or
linearity abstraction is defined. Each category exposes only an abstract, non-executable
`execute()` reservation returning `Never`. Scientifically typed values, actions, and
constructors remain subject to the applicable design gate for that category.

## Concrete ownership

Concrete implementations remain with the domain that owns their scientific data:

- reciprocal-shift maps derived from periodic basis data belong under the periodic
  domain;
- finite plane-wave reciprocal-index shifting remains with reciprocal-path or
  represented-basis mechanics;
- projected sewing consumes an admitted ambient map and explicitly selected frames;
- symmetry sewing remains with spatial, internal, or antiunitary symmetry owners; and
- finite-boundary sewing remains correlated with boundary-twist and gauge-bridge
  owners.

The top-level package is therefore an abstraction owner, not an implementation bucket
or compatibility facade.

## Source and verification

- Source: `python/src/ksdft2effmass/sewing/`
- Focused verification:
  `python/tests/software_verification/ksdft2effmass/sewing/test__Sewing.py`
- Reciprocal embedding and Wilson prerequisites:
  [`../periodic/basis_embedding/index.md`](../periodic/basis_embedding/index.md)
