# `ksdft2effmass.operators`

## Purpose and status

`ksdft2effmass.operators` owns representation-independent finite matrices, quantities,
eigensolvers, compression, and matrix norms. Typed state-space and subspace contracts
are assigned prospectively to the separate [`spaces`](../spaces/index.md) owner rather
than added beneath `operators`.

Existing modules remain documented by their current source, tests, Sphinx pages, and
older architecture records until touched. This page does not replace those records.

## Ownership boundary

This package establishes finite operator values and operations on already identified
spaces. It does not select a physical model, analytical states, retained dimension,
diagnostic list, parameter sweep, norm interpretation, or scientific acceptance
threshold.

## Dependency rules

The prospective `spaces` owner may consume immutable operator quantity records. The
reverse dependency must be justified by a concrete contract and is not selected by
this tranche. `operators` must not depend on `analysis`, model systems, experiments,
calculations, serializers, plotting, or provenance owners.

## Evidence and limitations

No new `operators` source contract is introduced by this documentation tranche.
Existing implementation and evidence status remain unchanged.
