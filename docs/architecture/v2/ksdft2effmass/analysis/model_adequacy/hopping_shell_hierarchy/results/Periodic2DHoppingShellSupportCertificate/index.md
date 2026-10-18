# `Periodic2DHoppingShellSupportCertificate`

## Purpose and status

Prospective immutable proof object for one directional lower bound on HSH-1 channel-set
distance. It is not implemented or supported.

## Public contract

Read-only properties expose the dimensionless maximal-space covector, orientation,
energy-valued conservative spectral/operator support endpoints, energy-valued dual
metric norm and raw directional gap, dimensionless outward-rounded lower bound,
arithmetic-policy identity, and premise defects. No method invokes an optimizer.

Planned supported route:
`ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.Periodic2DHoppingShellSupportCertificate`.

## State and identity

The certificate is identified by definition, shell class, metric identity, channel
orientation, covector components, support construction (`enclosing-ellipsoid` or a
future accepted stronger bounded method), arithmetic backend/version, precision, and
rounding policy.

## Invariants and failure behavior

The covector is finite, nonzero, and has maximal-space length. Its dual norm is finite
and strictly positive. Conservative endpoints must agree with the declared orientation.
The raw conservative directional gap is a finite signed value; the retained lower bound
is nonnegative and cannot exceed $\max(0,g)/\lVert u\rVert_{M^{-1}}$ under the declared
outward-rounding policy. Every premise defect is finite and within a named tolerance
before the certificate can support `certified-separated`.

A nonpositive or rounding-ambiguous outward gap may be retained only with a zero lower
bound and cannot support separation.

## Dependencies and collaborators

Quadratic-loss objects and the common metric define support bounds. The calculator may
use a solver to propose a direction, but this object contains only reconstructable proof
data. The verifier recomputes every endpoint and rounding enclosure independently.

## Data and action flow

Candidate direction $\rightarrow$ conservative channel support bounds $\rightarrow$
dual normalization $\rightarrow$ outward-rounded lower bound. The class result then
compares that bound with the frozen resolution.

## Serialization and compatibility

Schema v1 retains enough arithmetic metadata to reproduce the conservative enclosure.
A backend or rounding-policy change creates a distinct certificate identity and may
require a schema revision.

## Scientific and numerical boundary

The certificate lower-bounds distance only for the two frozen class-specific channel
sets in the fixed metric. It does not prove global model inadequacy or physical
interaction range.

## Prospective code mapping

| Planned code path | Symbol kind | Planned qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy/results.py` | Class | `ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.results.Periodic2DHoppingShellSupportCertificate` | Reconstructable lower-bound proof object |

## Test mapping

Planned tests mutate directions, orientation, support endpoints, metric norm, arithmetic
identity, raw gap, rounded bound, and premise tolerances. A rational/high-precision
oracle qualifies outward rounding. No test exists.

## Sphinx mapping

Prospective API page:
`doc/sphinx/api/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy.rst`.

## Provenance

Original local work under the repository license. The support-bound construction derives
from HSH-1 protocol Section 9 and Equation
[EQ-HSH-SUPPORT-BOUND-006](../../scientific.md#eq-hsh-support-bound-006).

## Evidence

| Evidence kind | Status | Evidence or reason | Validity domain |
|---|---|---|---|
| Software verification | Not evaluated | Proof object absent | None |
| Numerical verification | Not evaluated | Outward rounding unqualified | None |
| Scientific validation | Not evaluated | Synthetic hierarchy | None |
| Uncertainty quantification | Not applicable | Certificate is not probabilistic | None |
| Human acceptance | Not evaluated | Method not frozen | None |

## Limitations and deviations

The exact directed-rounding backend remains unresolved. Solver status is intentionally
absent from the proof semantics.
