# `Periodic2DHoppingShellHierarchyVerificationResult`

## Purpose and status

Prospective immutable ResultObject summarizing independent HSH-1 reconstruction. It is
not implemented or supported.

## Public contract

Construction accepts exact premise outcomes, named maximum defects, corresponding
positive tolerances, and one derived pass flag. Read-only properties expose the worst
normalized defect and checked-premise inventory.

Planned supported route:
`ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.Periodic2DHoppingShellHierarchyVerificationResult`.

## State and identity

The record correlates definition and result identities with source-projection, orbit,
shell, quadratic, minimum/nonemptiness, feasible-point, witness, metric, support-bound,
distance-interval, hierarchy, and withheld defects. Premise names are unique and
canonically ordered.

## Invariants and failure behavior

All defects are finite nonnegative built-in floats and all tolerances are finite
strictly positive built-in floats. `passed` is true exactly when every required premise
is true and every defect is within its named tolerance. Missing decisive checks or
inconsistent pass state raise `ValueError`.

## Dependencies and collaborators

The verifier constructs this object. It has no dependency on the producer, serializer,
files, or external execution.

## Data and action flow

Independent comparisons enter once; the immutable summary is then serialized separately
from the scientific result if retained.

## Serialization and compatibility

A retained verification schema must identify the verified result digest and exact
verification controls. Re-verification creates a new record rather than mutating an old
one.

## Scientific and numerical boundary

`passed` means the declared bounded reconstruction checks passed. It does not mean
scientific validation, uncertainty quantification, material adequacy, or human
acceptance.

## Prospective code mapping

| Planned code path | Symbol kind | Planned qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy/verify.py` | Class | `ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.verify.Periodic2DHoppingShellHierarchyVerificationResult` | Immutable verification summary |

## Test mapping

Planned tests reject negative/nonfinite defects, nonpositive tolerances, duplicate or
missing premise names, and inconsistent pass flags. No test exists.

## Sphinx mapping

Prospective API page:
`doc/sphinx/api/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy.rst`.

## Provenance

Original local work under the repository license.

## Evidence

| Evidence kind | Status | Evidence or reason | Validity domain |
|---|---|---|---|
| Software verification | Not evaluated | ResultObject absent | None |
| Numerical verification | Not evaluated | No reconstruction result | None |
| Scientific validation | Not applicable | Verification summary only | None |
| Uncertainty quantification | Not applicable | No uncertainty semantics | None |
| Human acceptance | Not evaluated | No decision | None |

## Limitations and deviations

The exact defect inventory will be finalized with the verifier implementation and must
remain explicit rather than collapsed into one opaque score.
