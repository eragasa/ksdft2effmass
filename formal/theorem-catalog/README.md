# Mechanized Theorem Catalog

This catalog states prover-neutral mathematical contracts before they are encoded in Lean, Isabelle, or Rocq. It is governed by [`docs/architecture/mechanized-proof-system.md`](../../docs/architecture/mechanized-proof-system.md).

The catalog is maintained Markdown, not executable proof software. A contract records the proposition that all three backends are intended to encode. It does not prove the proposition, establish that backend encodings are equivalent, or validate the scientific assumptions from which the proposition was derived.

## Authority

The catalog is subordinate to:

1. current human scientific decisions;
2. applicable versioned files under `specification/`;
3. accepted assumptions and conventions under `docs/research/`; and
4. the owning prose proof under `docs/proofs/ksdft2effmass/`.

If those sources do not determine one theorem statement, the contract remains blocked or proposed rather than selecting a convenient formalization.

## Contract fields

Each theorem contract records:

- **Identity** — stable `PRF-*` proof-obligation identifier.
- **Status** — contract status, distinct from proof and backend status.
- **Purpose** — why the theorem is needed downstream.
- **Authority references** — repository owners from which the statement is derived.
- **Mathematical setting** — scalar field, spaces, dimensions, and objects.
- **Definitions** — exact notation introduced by the contract.
- **Assumptions** — explicit hypotheses and quantifier order.
- **Conclusion** — the proposition to be encoded.
- **Equivalent formulation** — optional form permitted when equivalence is reviewed.
- **Nonclaims** — conclusions not supplied by the theorem.
- **Backend bindings** — intended theorem names in Lean, Isabelle, and Rocq.
- **Conformance questions** — semantic details requiring cross-backend comparison.

## Contract status

| Status | Meaning |
|---|---|
| `not drafted` | The proof identity exists, but no common theorem contract has been written. |
| `draft` | A proposed contract exists but has not been accepted as the common backend target. |
| `blocked` | A named scientific or mathematical ambiguity prevents one common statement. |
| `frozen` | The assumptions and conclusion are accepted as the current common backend target. |
| `revised` | A formerly frozen contract changed; affected backend proofs require reconciliation. |
| `retired` | The contract was superseded or rejected with a recorded disposition. |

A `frozen` contract is not a proved theorem. Backend states such as `encoded`, `checked`, and `cross-checked` are recorded separately from contract status.

## Change discipline

Changing a scalar field, state space, dimension condition, adjoint, norm, quantifier, gauge action, or conclusion is a contract revision rather than an editorial correction. A revision must identify affected prose proofs and backend encodings.

Backend-specific helper lemmas may use different names or representations, but the exported theorem associated with a `PRF-*` identity must be reviewed against the frozen contract.
