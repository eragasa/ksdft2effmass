# Lean backend

This directory contains the project-owned Lean encoding of frozen theorem
contracts from [`../theorem-catalog/`](../theorem-catalog/).

## Current bounded scope

Only `PRF-05.01` is authorized, implemented, and checked by the pinned Lean
toolchain. The remaining `PRF-05` contracts are frozen but unencoded. Isabelle and Rocq remain separate future
backends.

The checked theorem establishes a finite-dimensional matrix identity under the
assumptions in the catalog. It does not establish physical adequacy, numerical
verification, scientific validation, or cross-backend semantic conformance.

## Pinned toolchain

- Lean 4: `v4.33.0`
- mathlib: `v4.33.0`, with exact transitive revisions retained in
  `lake-manifest.json`
- Lean and mathlib upstream licenses observed for this trial: Apache-2.0

The toolchain is managed by `elan` and the package by Lake. Neither is a Python
runtime dependency.

## Local verification

```bash
cd formal/lean
~/.elan/bin/lake build
```

The installer could not modify the local shell profile, so repository verification uses the explicit `~/.elan/bin/lake` path rather than assuming it is on `PATH`.

Generated `.lake/` content is ignored and must not be committed. The retained
source contains no `sorry` or `admit`; `#print axioms` reports the standard Lean
foundational dependencies `propext`, `Classical.choice`, and `Quot.sound` for the
exported theorem.
