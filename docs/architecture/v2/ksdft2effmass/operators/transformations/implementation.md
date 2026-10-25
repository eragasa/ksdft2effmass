# Implementation

## Source boundary

Source owner: `python/src/ksdft2effmass/operators/transformations/`.

The initializer is documentation-only. `identities.py` owns the enum and directed edge
identity. `base.py` owns the generic request/result/Action skeleton. Consumers import from
defining modules; neither package nor `operators.__init__` re-exports symbols.

## Dependency direction

This package may import `operators.representations`. Representations must never import
transformations. Neither generic package imports concrete operator families. This package
also excludes analysis, campaigns, Workflow, serializers, schemas, retained data, and
formal runtime code.

Concrete operator-family packages may consume both generic packages. Reusable
cross-operator transformations may be added here after review; operator-specific
transformations remain with their concrete operator package.

## Factory boundary

`TransformationIdentityFactory` is an identity-only constructor. There is no universal
operational `TransformationFactory` and no enum dispatch registry. Each future concrete
Action refines the nominal ABCs and implements public `transform(request, /) -> result`,
using the protected validators or equally strict checks to reject kind disagreement.

## Compatibility and evidence

No compatibility facade or root re-export preserves the discarded provisional singular
path. No codec, schema, certificate, retained-result, or proof contract exists in Phase 1.
A transformation Action instance is not evidence of correctness.
