# `ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.serialization`

## Purpose and status

Prospective strict canonical JSON boundary for HSH-1. No source module or schema exists.

## Prospective public contract inventory

- [`Periodic2DHoppingShellHierarchyResultJsonSerializer`](Periodic2DHoppingShellHierarchyResultJsonSerializer/index.md) — deterministic encoder and strict decoder for schema identity `ksdft2effmass.periodic2d.hopping-shell-hierarchy-result.v1`.

## Represented wire object

The schema preserves definition/source identities, conventions, orbit and shell
inventories, weights, thresholds, tolerances, quadratics, feasible points, support
certificates, distance intervals, dispositions, hierarchy conclusion, withheld roles,
provenance, limitations, and explicit nonclaims.

## Invariants and failure behavior

Decoding rejects unknown/missing fields, duplicate semantic identities, booleans in
numeric positions, numeric strings, nonfinite numbers, malformed digests, noncanonical
enum values, and inconsistent nested lengths. Encoding rejects objects that cannot be
represented without loss under the declared schema. JSON key ordering and separators
are canonical; one trailing newline is planned for retained documents.

## Dependencies and neighboring owners

Serialization constructs and validates typed objects but does not calculate quadratics,
repair certificates, infer dispositions, or access manifests. Schema v1 may nest or
inline the common completed-square coefficients, but HSH retains its own wire identity;
no universal quadratic serializer is introduced. Retained scripts own file I/O and
exact manifest-entry correlation.

## Class navigation

- [`Periodic2DHoppingShellHierarchyResultJsonSerializer`](Periodic2DHoppingShellHierarchyResultJsonSerializer/index.md)

## Prospective code mapping

| Planned path | Symbol kind | Planned qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy/serialization.py` | Module | `ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.serialization` | Schema-v1 typed codec |

## Test mapping

Planned tests establish deterministic bytes, exact round trip, strict unknown-field and
numeric rejection, enum/optional-field correlation, and schema-version failure. No test
exists.

## Sphinx mapping

No Sphinx page exists. The intended page is
`doc/sphinx/api/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy.rst`.

## Provenance

Original local work under the repository license.

## Evidence

| Evidence kind | Status | Evidence or reason | Validity domain |
|---|---|---|---|
| Software verification | Not evaluated | Codec and schema do not exist | None |
| Numerical verification | Not applicable | Codec transports values | None |
| Scientific validation | Not applicable | Wire format has no validation authority | None |
| Uncertainty quantification | Not applicable | No uncertainty semantics | None |
| Human acceptance | Not evaluated | Schema not accepted | None |

## Limitations and deviations

The final schema field inventory is gated on the unresolved interval-arithmetic and
configuration choices.
