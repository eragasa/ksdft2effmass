# `LabeledComponentBasisCoordinate`

## Contract and identity

Frozen coordinate for an analytic, synthetic, or composite component identified by one
exact nonempty `label`.

## Invariants

Spelling, case, and punctuation are semantic. Labels are neither normalized nor joined
from other values by this class.

## Dependencies and flow

An admitted label enters this record and then an ordered `PeriodicBasisIdentity`.

## Serialization

The record stores `kind = labeled_component` and `label` through `BaseTypedRecord`.

## Scientific boundary

The label identifies a coordinate, not a state space, gauge, embedding, or provenance
source. Generated labels require separate scientific justification.

## Mappings

Source: `python/src/ksdft2effmass/periodic/operators/basis.py`; tests:
`python/tests/ksdft2effmass/periodic/operators/test__PeriodicBasisIdentity.py`; Sphinx:
`doc/sphinx/api/periodic-basis.rst`.

## Provenance and evidence

The family covers existing analytic/composite inventories without approving historical
naming conventions as scientific evidence. Tests are software verification.

## Limitations

Opaque labels cannot substitute for plane-wave, Wannier, or Slater--Koster coordinates.

## Navigation

- [Module](../index.md)
- [`PeriodicBasisIdentity`](../PeriodicBasisIdentity/index.md)
