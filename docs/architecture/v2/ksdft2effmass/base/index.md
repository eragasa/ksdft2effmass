# `ksdft2effmass.base` data-object hierarchy

## Responsibility

`ksdft2effmass.base` owns the package-wide structural and functional base
hierarchy:

- `DataObject` and `DataObjectModel`;
- `DataObjectActionRequest` and `DataObjectActionResult`;
- `DataObjectActionizer[RequestT, ResultT]`;
- immutable, identity, validation, and derivation abstractions; and
- configurable actionizer configuration and request abstractions.

These are thin nominal bases. They contain no workflow policy, scientific
algorithm, persistence, discovery, registry, serialization, or external effect.
The package structure duplicates the accepted ProjectKoios Ingestion base
pattern observed at commit
`dc229a33e6e9e711072c5742b4d2c55dbbdd29ee` (base-directory Git tree
`07fb4b02a5db9d3adeeb7731cfd5594fea4adbc0`) while allowing an explicit later
mapping to the stable ProjectKoios base owner.

## Operation boundary

A materially changed operation follows:

```text
DataObjectActionRequest -> DataObjectActionizer -> DataObjectActionResult
```

Concrete actionizers use meaningful performer nouns and expose
`action(*, request) -> result`. Requests and results are immutable models.
Constructors, `__post_init__`, properties, intrinsic validation, and cheap
identity derivation are not modeled as separate actions.

## Current consumer

The provisional [`ksdft2effmass.workflows.v2`](../workflows/v2/index.md)
runtime consumes this hierarchy. Workflow-specific requests and actionizers
remain under that runtime; they are not part of `ksdft2effmass.base`.
