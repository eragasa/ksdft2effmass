# Periodic model catalogs and comparison

## Explicit toy-model catalog

Iteration over all supported toy models uses an immutable explicit catalog. The
catalog is a maintained scientific-software record, not directory scanning,
`__subclasses__()` discovery, import side effects, naming conventions, or plugin
entry-point discovery.

Each catalog entry binds:

- a stable model identity;
- exact nominal periodic-model type;
- spatial dimension;
- toy model role;
- model definition or construction inputs;
- supported evaluation capabilities; and
- deterministic catalog order.

Catalog construction rejects non-model values, unsupported dimensions, duplicate
identities, non-toy roles, and entries whose declared metadata disagrees with their
nominal model family. A campaign consumes one exact catalog snapshot so additions or
reordering cannot silently change an existing run.

## Evaluation before comparison

Campaign objects execute evaluations over catalog entries and return typed per-model
observations. Comparators consume those observations or represented scientific
results; they do not execute campaign objects or inspect campaign internals.

```text
explicit toy-model catalog
          |
          v
 evaluation campaign
          |
          v
 typed observations
          |
 compatibility and alignment
          |
          v
 comparison ActionObject
```

## Compatibility-gated comparison

“All toy models” means all models with a declared comparison quantity, not arbitrary
matrix subtraction. A comparison family states the quantity and its domain, unit,
normalization, geometry assumptions, and admissible dimensions.

Examples of potentially shared quantities include scalar convergence diagnostics or
normalized spectral summaries. Represented operators require matching or explicitly
transported state spaces, basis ordering, gauge, units, geometry, and energy reference.
Dimension-specific topology, tensor, or defect-locality quantities remain in their
own comparison families when no common definition exists.

An incompatible pair or unavailable channel produces an explicit typed outcome. It is
not dropped, coerced, assigned zero error, or treated as a failed scientific model.
Comparisons apply no scientific acceptance threshold unless an owning campaign or
verification request supplies one.

## Material-reference comparisons

Graphene and silicon results do not enter the toy-model catalog. A separate
material-reference evaluation may reuse verified numerical Actions, but comparisons
with toy models require a declared shared quantity and evidentiary interpretation.
Agreement with a toy model is not material validation, and disagreement does not by
itself identify parent-model, numerical, or reduction error.
