# `Periodic2DHoppingShellClassResult`

## Purpose and status

Prospective immutable ResultObject for one shell class in HSH-1. It is not implemented
or supported.

## Public contract

The object exposes its shell identity, active orbit inventory, channel quadratics and
minima, nonemptiness outcomes, feasible points, optional common witness, optional
support certificate, distance interval, withheld diagnostics, and exact disposition.
It provides no mutating or refitting method.

Planned supported route:
`ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.Periodic2DHoppingShellClassResult`.

## State and identity

Stable identity is the definition identity plus class index and squared-radius shell.
Every maximal-space point has fixed length and exact zeros on inactive coordinates.
Training and withheld observations are explicitly separated. Distances/losses are
dimensionless; withheld spectral errors retain the source energy unit.

## Invariants and failure behavior

The object enforces:

- exact shell-mask and active-index correlation;
- two channel quadratics for valid nonempty/empty decisions;
- threshold/minimum/nonemptiness consistency;
- no distance for an empty channel;
- a verified same-point witness for `compatible-common-witness`;
- two verified feasible points and an upper bound for nonempty noncompatible cases;
- a support certificate and lower bound above resolution for `certified-separated`;
- lower bound not exceeding upper bound;
- no decisive proof attached to `unresolved-nonempty`; and
- a named failed premise with no hierarchy contribution for `invalid-premise`.

Wrong types raise `TypeError`; inconsistent correlations raise `ValueError`.

## Dependencies and collaborators

The object composes `Periodic2DHoppingShellDisposition`, two quadratic-loss objects, and
optionally a support certificate. The hierarchy result validates cross-class nesting
and minimality.

## Data and action flow

The calculator constructs a class result only after all training geometry for that
class is fixed. Withheld evaluation is appended as immutable diagnostic fields without
changing the disposition.

## Serialization and compatibility

All optional fields are discriminated by disposition. Schema decoding must reject
field combinations that cannot arise from the typed constructor.

## Scientific and numerical boundary

A class result applies only to one nested class under the frozen definition. Empty,
separated, compatible, and unresolved have distinct evidentiary meanings. Withheld
errors do not certify training compatibility or separation.

## Prospective code mapping

| Planned code path | Symbol kind | Planned qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy/results.py` | Class | `ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.results.Periodic2DHoppingShellClassResult` | Correlated per-shell outcome |

## Test mapping

Planned tests cover every allowed disposition and all forbidden optional-field,
threshold, feasibility, interval, inactive-coordinate, and withheld-role combinations.
No test exists.

## Sphinx mapping

Prospective API page:
`doc/sphinx/api/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy.rst`.

## Provenance

Original local work under the repository license.

## Evidence

| Evidence kind | Status | Evidence or reason | Validity domain |
|---|---|---|---|
| Software verification | Not evaluated | ResultObject absent | None |
| Numerical verification | Not evaluated | No class result exists | None |
| Scientific validation | Not evaluated | Synthetic parent | None |
| Uncertainty quantification | Not evaluated | Bounds are deterministic certificates, not UQ | None |
| Human acceptance | Not evaluated | No class accepted | None |

## Limitations and deviations

The precise withheld-diagnostic field inventory remains draft and cannot influence the
training disposition.
