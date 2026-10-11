# `Periodic2DHoppingShellHierarchyResultJsonSerializer`

## Purpose and status

Prospective strict serializer for HSH-1 schema v1. It is not implemented or supported.

## Public contract

Planned methods encode one definition/result pair to canonical UTF-8 JSON bytes and
decode untrusted bytes to strict typed objects. The schema identity is
`ksdft2effmass.analysis.model-adequacy.hopping-shell-hierarchy-result.v1`.

Planned supported route:
`ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.Periodic2DHoppingShellHierarchyResultJsonSerializer`.

## State and identity

The serializer is stateless. Schema identity and version are exact constants. Encoded
ordering follows canonical orbit, shell, coordinate, and class order.

## Invariants and failure behavior

Encoding rejects nonfinite or semantically inconsistent typed content. Decoding rejects
unknown or missing fields, duplicate identities, unsupported versions, Boolean numeric
impostors, numeric strings, malformed complex/tuple encodings, invalid enums, and
length/correlation defects. Failures do not produce partial objects.

## Dependencies and collaborators

The serializer constructs HSH types from `definition` and `results`. It inlines
canonical quadratic coefficients plus explicit dense/sparse selection rather than
serializing NumPy/SciPy objects; it retains the HSH schema and
does not create a universal primitive serializer. It cannot run the calculator,
verifier, source projection, optimizer, or manifest correlation.

## Data and action flow

Typed objects enter the encoder and canonical bytes leave. The decoder performs the
reverse conversion and then relies on every DataObject constructor to re-enforce domain
invariants.

## Serialization and compatibility

Schema v1 is closed. Field addition, changed units/order, or altered disposition meaning
requires a new schema version and explicit migration. Canonical bytes use sorted keys,
fixed separators, UTF-8, forbidden NaN/Infinity, and one final newline.

## Scientific and numerical boundary

Successful round trip establishes wire behavior only. It does not establish numerical
reconstruction, source authenticity, chronology, or scientific validity.

## Prospective code mapping

| Planned code path | Symbol kind | Planned qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy/serialization.py` | Class | `ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.serialization.Periodic2DHoppingShellHierarchyResultJsonSerializer` | Strict canonical schema-v1 codec |

## Test mapping

Planned nodes cover deterministic bytes, exact round trip, unknown fields, Boolean and
string numerics, nonfinite values, invalid enums, malformed lengths, and unsupported
versions. No test exists.

## Sphinx mapping

Prospective API page:
`doc/sphinx/api/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy.rst`.

## Provenance

Original local work under the repository license.

## Evidence

| Evidence kind | Status | Evidence or reason | Validity domain |
|---|---|---|---|
| Software verification | Not evaluated | Serializer absent | None |
| Numerical verification | Not applicable | Serialization only | None |
| Scientific validation | Not applicable | Serialization only | None |
| Uncertainty quantification | Not applicable | No uncertainty semantics | None |
| Human acceptance | Not evaluated | Schema not accepted | None |

## Limitations and deviations

The final field inventory awaits interval-policy review. File I/O and manifest handling
remain outside this class.
