# `ksdft2effmass.periodic2d.campaign.nbands_1.result_documents`

## Purpose

This module owns exact encoded result-document representation for the version-one
isolated periodic-2D campaign. It is separate from the typed campaign definition,
calculation Actions, JSON serializer, exact two-document bundle, correlation, and
verification owners.

## Child map

- [`Periodic2DIsolatedBandResultDocument`](Periodic2DIsolatedBandResultDocument/index.md)

## Responsibility boundary

The module may retain exact result bytes and derive their SHA-256 content identity. It
does not decode JSON, infer a schema, authenticate a repository location, prove that a
calculation occurred, or assign physical-model, finite-representation, retained-space,
operator, basis, gauge, geometry, unit, convergence, validation, uncertainty, or
acceptance meaning.

```text
calculation or retained artifact
        |
        v
exact result bytes -> Periodic2DIsolatedBandResultDocument
        |                         |
        |                         +-> SHA-256 content identity
        v
explicit campaign consumer
```

The defining module contains no registry, factory, plugin point, compatibility alias, or
forwarding class.
