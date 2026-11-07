# Numerical behavior

The request and result ABCs require only a `RepresentationTransformationKind` property.
The non-generic transformation ABC exposes `transform(self)` at the nominal result
boundary. A concrete final override narrows that return covariantly to its exact result.

The protected helpers reject non-nominal values, non-enum kinds, and kind disagreement.
They do not identify the concrete request or result type and cannot force an override to
invoke them. Exact type checks and helper calls are obligations of every actual concrete
triple and require direct tests for that triple.
