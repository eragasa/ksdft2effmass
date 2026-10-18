# `Periodic2DHoppingShellHierarchyResultVerifier`

## Purpose and status

Prospective stateless ActionObject for independent typed HSH-1 reconstruction. It is
not implemented or supported.

## Public contract

`execute(definition, result)` returns one
`Periodic2DHoppingShellHierarchyVerificationResult`. It never rewrites the result,
changes a disposition, or supplies a missing certificate.

Planned supported route:
`ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.Periodic2DHoppingShellHierarchyResultVerifier`.

## State and identity

The verifier has no maintained instance state. Its arithmetic/backend identity and
verification tolerances are explicit inputs or result provenance.

## Invariants and failure behavior

The verifier independently reconstructs all decisive premises. It cannot return a pass
when a check is missing, a source identity is inconsistent, a class is skipped, or a
certificate relies only on solver status. Malformed typed objects fail immediately;
valid but mismatching objects produce a failed verification summary with bounded
defects.

## Dependencies and collaborators

The verifier consumes definition/result objects and may use low-level NumPy/SciPy,
periodic parent/model primitives, and the accepted outward-rounding backend. It may read
the stored center, canonical matrix entries, minimum, and backend selection from a
result's Optimization facade, but it
must not use the common constructor, `squared_loss`, or `root_loss` as verification
logic. It independently validates shape, finiteness, symmetry, and positive curvature;
reconstructs the energy-scale normalization and all coefficients; and evaluates direct
and quadratic formulas through an independent code path. It must not call calculator
private methods or `execute()`. Standalone wire verification is a separate retained-
script boundary.

## Data and action flow

The action independently composes PhysKit source projection and orbit/shell invariants,
then rebuilds both channel quadratics,
box-constrained minima, feasible points, metric distances, support endpoints, lower
bounds, class/hierarchy logic, and withheld diagnostics, then constructs the immutable
verification result.

## Serialization and compatibility

The verifier is schema-independent at the typed boundary. A standalone adapter decodes
a specific schema version before calling it and separately verifies file/manifests.

## Scientific and numerical boundary

Passing verification supports only agreement with the frozen finite HSH-1 problem. The
shared numerical stack remains a common-mode risk, and verification is not scientific
validation.

## Prospective code mapping

| Planned code path | Symbol kind | Planned qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy/verify.py` | Class | `ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.verify.Periodic2DHoppingShellHierarchyResultVerifier` | Independent typed verifier |
| same | Method | `...Periodic2DHoppingShellHierarchyResultVerifier.execute` | Definition/result reconstruction |

## Test mapping

Planned verification tests mutate every decisive proof field and inspect the
producer-call/import boundary. See [testing](../../testing.md). No test exists.

## Sphinx mapping

Prospective API page:
`doc/sphinx/api/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy.rst`.

## Provenance

Original local work under the repository license.

## Evidence

| Evidence kind | Status | Evidence or reason | Validity domain |
|---|---|---|---|
| Software verification | Not evaluated | Verifier absent | None |
| Numerical verification | Not evaluated | No independent execution | None |
| Scientific validation | Not evaluated | Synthetic parent only | None |
| Uncertainty quantification | Not evaluated | No uncertainty model | None |
| Human acceptance | Not evaluated | No accepted evidence | None |

## Limitations and deviations

Independent algorithms may still share libraries and conventions. The interval backend
and platform scope must be frozen before implementation can support certificate claims.

## Detail navigation

- [Implementation plan](../../implementation.md)
- [Numerical contract](../../numeric.md)
- [Testing plan](../../testing.md)
