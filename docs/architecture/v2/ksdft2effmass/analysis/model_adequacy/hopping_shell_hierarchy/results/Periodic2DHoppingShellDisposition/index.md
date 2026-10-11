# `Periodic2DHoppingShellDisposition`

## Purpose and status

Prospective enum for one HSH-1 shell class. It is not implemented or supported.

## Public contract

Exact planned values are:

- `spectral-set-empty`;
- `operator-set-empty`;
- `certified-separated`;
- `compatible-common-witness`;
- `unresolved-nonempty`; and
- `invalid-premise`.

The enum classifies bounded evidence state; it is not a severity, workflow status, or
human decision.

## State and identity

Each member has one stable lowercase wire value. No aliases or truth-value ordering are
permitted.

## Invariants and failure behavior

Unknown strings fail strict decoding. `certified-separated` requires two nonempty sets
and a reconstructed lower bound above resolution. `compatible-common-witness` requires
one verified point in both sets. Empty-set values forbid a distance interval. If both
channel sets are empty, the deterministic disposition is `spectral-set-empty`, following
the declared spectral-then-operator decision order; the class result still retains both
channel nonemptiness outcomes, so the operator-set observation is not discarded.
`unresolved-nonempty` requires both sets nonempty without either decisive proof.
`invalid-premise` records a named class-local premise failure and blocks all hierarchy-
level conclusions.

## Dependencies and collaborators

`Periodic2DHoppingShellClassResult` owns member/field correlation. The serializer owns
wire conversion; the calculator and verifier assign or reconstruct members.

## Data and action flow

One member is constructed only after channel nonemptiness and proof-object checks. The
hierarchy result consumes the ordered class dispositions to decide whether minimality is
supported.

## Serialization and compatibility

Wire values are schema-versioned and case-sensitive. Changed meaning requires a new
schema, not reinterpretation.

## Scientific and numerical boundary

The enum is meaningful only with the frozen parent, class, weights, thresholds, metric,
and proof objects. It is not a material verdict.

## Prospective code mapping

| Planned code path | Symbol kind | Planned qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy/results.py` | Enum | `ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.results.Periodic2DHoppingShellDisposition` | Per-class bounded outcome vocabulary |

## Test mapping

Planned tests assert exact values and reject every invalid disposition/proof-field
combination. No test exists.

## Sphinx mapping

Prospective API page:
`doc/sphinx/api/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy.rst`.

## Provenance

Original local work under the repository license; vocabulary derives from HSH-1
protocol Section 11.

## Evidence

| Evidence kind | Status | Evidence or reason | Validity domain |
|---|---|---|---|
| Software verification | Not evaluated | Enum absent | None |
| Numerical verification | Not applicable | Vocabulary only | None |
| Scientific validation | Not evaluated | No result | None |
| Uncertainty quantification | Not applicable | No uncertainty meaning | None |
| Human acceptance | Not evaluated | Vocabulary not accepted | None |

## Limitations and deviations

`invalid-premise` is fail-honest diagnostic state, not evidence of separation or
incompatibility.
