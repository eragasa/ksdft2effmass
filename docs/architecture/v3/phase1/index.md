# Phase 1 — representation foundations

## Purpose

Phase 1 establishes the smallest implemented vocabulary needed to identify finite operator
representations and directed derivation edges without performing an operation or making a
scientific qualification.

It separates:

1. finite carrier domains;
2. represented-space identity;
3. intrinsic representation identity and matrix-field storage; and
4. transformation-edge identity and nominal computational interfaces.

## Implemented scope

The source surface consists of two sibling packages:

- [`ksdft2effmass.operators.representations`](../src/ksdft2effmass/operators/representations/index.md);
- [`ksdft2effmass.operators.transformations`](../src/ksdft2effmass/operators/transformations/index.md).

The required dependency direction is

```text
representations -> transformations
```

where the arrow means “is consumed by.” Representations do not import transformations.
Both package initializers are documentation-only, and consumers import public types from
the defining modules.

## Status

The Phase 1 foundation was introduced in KSD commit
`ed9522dd25c33f2473b2a8320f5fafeeb56ece60`. The current worktree contains an uncommitted
Phase 1 correction replacing the generic operational ABC with the selected non-generic,
request-bound nominal contract and strengthening dependency guards.

This status establishes an implemented software checkpoint only. It does not establish a
released API, wire schema, numerical transformation, scientific result, retained
evidence, or formal proof.

## Phase-level views

- [Scientific scope](scientific.md)
- [Numerical scope](numerics.md)
- [Implementation boundary](implementation.md)
- [Schematics](schematics.md)

Detailed contracts flow downward through the [`src/`](../src/index.md) mirror to package,
module, and public-type documentation.
