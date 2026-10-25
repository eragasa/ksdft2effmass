# Numerical contract

Phase 1 contains no operation-specific numerical algorithm. Each concrete Action
implements abstract public `RepresentationTransformationABC.transform`. It must check
exact nominal request type, request/Action enum identity, exact nominal result type, and
result/Action enum identity. Protected final validators centralize those checks.

`TransformationIdentity` validates nonempty metadata, exact endpoint identity types, and
the declared role transition for its enum kind. These checks do not inspect arrays or
compute residuals.

Future concrete operations must own their exact dimensions, dtype and overflow behavior,
tolerances, diagnostics, and failure disposition. A rejected or unresolved scientific
operation must not be represented as successful merely because nominal kind checks pass.
