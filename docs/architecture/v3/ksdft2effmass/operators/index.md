# `ksdft2effmass.operators`

## Purpose and status

`ksdft2effmass.operators` owns general represented-operator records and operations,
including finite-difference and ladder operators, represented differences, residual
metrics, matrix norms, exact compatibility decisions, and the retained
complex-Hermitian sparse solver boundary.

Hamiltonian records, spectral subspaces, reduction, and decomposition belong to
[`ksdft2effmass.hamiltonian`](../hamiltonian/index.md), not this package.

## External ownership

Generic quantities, unit conversion, matrix admission and verification, eigensystems,
and real-symmetric spectral decomposition belong to PhysKit. Maintained KSD source
imports canonical objects directly from `projectkoios.physkit`. KSD has no
`ksdft2effmass.linalg` compatibility package and `operators` does not re-export
PhysKit objects.

## Ownership boundary

This package establishes general finite-operator values and operations on already
identified spaces. It does not select a physical model, retained dimension, diagnostic
inventory, parameter sweep, norm interpretation, or scientific acceptance threshold.

## Dependency rules

`operators` may consume PhysKit directly. It must not depend on KSD analysis, model
systems, calculations, experiment composition, serializers, plotting, or provenance
owners. Hamiltonian-specific behavior must not be added here.

## Evidence and limitations

Tests cover the maintained represented-operator contracts. Generic quantity and matrix
verification evidence remains with PhysKit. Software checks do not establish physical
or model-reduction adequacy.
