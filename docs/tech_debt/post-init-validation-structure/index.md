# Post-init validation structure

## Status

**Safe to defer outside currently touched classes.** Runtime invariants remain important,
but several immutable records currently place many unrelated checks directly in one
``__post_init__`` method. This is a readability and maintenance concern, not evidence
that those invariants should be removed.

## Current direction

When a record is otherwise in scope, keep ``__post_init__`` as a short, documented
entry point and delegate cohesive checks to explicitly named methods such as:

```python
def __post_init__(self) -> None:
    """Check source identities and exact replay correlation."""
    self._check_args_digest_syntax()
    self._check_args_exact_result_correlation()
```

Use comments where the code encodes scientific meaning that is not obvious from Python
syntax—for example, whether identities denote exact source bytes, finite represented
spaces, or untruncated mathematical spaces. Comments should explain the reason for a
check rather than restating the conditional expression.

## Completed bounded slices

The long mixed-purpose constructors in
``workflows/v2/core/models.py`` now keep ``__post_init__`` as a documented
entry point and delegate their existing checks to cohesive ``_check_args_*``
stages. Validation order, exception behavior, immutable fields, and identity
semantics remain unchanged.

``provenance.records.RunManifest`` now applies the same bounded structure to
its primary identities, input identities, start timestamp, lifecycle state and
terminal timestamp, output and dependency identities, and direct self-dependency
check. The original validation statements remain unchanged and in the same
order; the start-time checker returns the parsed timestamp needed by the next
ordered lifecycle check. Other packages remain deferred until they are in
scope.

## Deferred work

1. Inventory maintained frozen DataObjects and result records with long
   ``__post_init__`` methods.
2. Separate local scalar/type checks from cross-object scientific correlations.
3. Name delegated checks ``_check_args_<meaning>`` so failures can be understood from
   the owning invariant rather than tuple position or control-flow order.
4. Keep cross-object construction checks with the owning Action when the Action creates
   the entire graph; avoid repeating the same relation at every aggregate layer.
5. Preserve current exception types, public behavior, immutability, and test evidence.
6. Add focused tests only where decomposition reveals an uncovered invariant; do not
   enlarge every verifier merely to mirror constructor implementation.

## Boundaries

This debt does not authorize removing scientific invariants, weakening exact public
type contracts, introducing generic validators, or creating a registry, factory, or
discovery mechanism. It does not delay the active separation of the untruncated
periodic parent from its finite plane-wave representation. Newly added or materially
modified ``__post_init__`` methods should follow the documented decomposition pattern;
a repository-wide cleanup may proceed independently later.

## Completion criteria

The debt is complete when the maintained inventory has been reviewed, long mixed-purpose
``__post_init__`` methods have cohesive documented ``_check_args_*`` stages or a clearly
owned construction Action, affected tests pass unchanged or with stronger invariant
coverage, and no scientific or public-contract meaning has been weakened.
