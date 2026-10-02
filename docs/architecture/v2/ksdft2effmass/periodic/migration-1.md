# Migration phase 1: scientific-retention documentation

## Status

**Implemented on `work/periodic2d-parity` in `94f5330b`.** The commit is a work-branch
architecture record, not a reviewed release or scientific-validation result.

## Purpose

Correct the architecture's earlier archival reading of “retained” before changing
source. The manuscript uses retention scientifically: a parent operator is restricted
to an identified retained subspace and may then receive a finite representation or an
approximate effective-model reduction.

## Delivered boundary

Phase 1 established that:

- scientific retention differs from preservation of evidence and encoded bytes;
- `PeriodicModel`, parent operator, retained subspace, exact retained operator,
  represented matrix, and approximate effective model are distinct;
- retained operators do not inherit from `PeriodicModel` solely because they are
  scientifically important;
- projection, disentanglement, gauge change, localization, representation change,
  truncation, alignment, fitting, and continuum embedding remain distinct operations;
- operator comparison requires compatible or explicitly aligned state spaces and
  energy references; and
- negative and unavailable reduction outcomes remain explicit results.

The owning architecture pages are:

- [`retained-spaces-and-operators.md`](retained-spaces-and-operators.md); and
- [`reduction-and-evidence-boundaries.md`](reduction-and-evidence-boundaries.md).

## Excluded work

Phase 1 changed no manuscript, Python source, tests, schemas, calculation payloads,
checksums, provenance, or public API. It did not authorize implementation of the target
scientific objects.

## Gate evidence

The phase passed local Markdown-link validation, Sphinx warnings-as-errors, and
`git diff --check` before commit. Those checks establish documentation integrity only.
