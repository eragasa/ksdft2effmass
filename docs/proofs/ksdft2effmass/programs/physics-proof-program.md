# Proof Program for `ksdft2effmass`

> Status: Provisional research program, not a record of completed proofs. See the workspace [proof status](../proof-status.md). No item establishes mathematical correctness, numerical verification, scientific validation, or human acceptance.

## 1. Purpose

Develop the mathematical results needed to support:

1. spectral–operator compatibility;
2. aligned impurity-operator extraction;
3. atomistic-to-continuum reduction;
4. error propagation from operators to physical observables;
5. validation-gated agentic workflow execution.

The physics proofs and the agentic-workflow proofs remain separate publication tracks.

---

## 12. Priority Order

### Priority 1 — Required for the bulk-Si compatibility paper

1. Gauge covariance of aligned operators.
2. Existence of minimum spectral–operator separation.
3. Certified incompatibility method.
4. Path-consistency bounds.

### Priority 2 — Required for the impurity and crossover papers

1. Gauge-compatible spatial decomposition.
2. Well-posed crossover radius.
3. Operator-error bound on binding energy.
4. Fidelity or eigenspace-error bound.
5. Excluded-space correction bound.
6. Continuum-parameter identifiability.

### Priority 3 — Stronger mathematical-physics extension

1. Atomistic-to-envelope consistency.
2. Multivalley asymptotic reduction.
3. Representation stability of the crossover radius.
4. Transferability conditions for short-range corrections.

### Priority 4 — Separate agentic-workflow paper

1. Authorization safety.
2. Marking preservation.
3. Replay determinism.
4. Provenance completeness.
5. Correct failure propagation.

---

## 14. Central Mathematical Narrative

The complete proof structure is

$$
\boxed{
\begin{aligned}
&\text{align the state spaces}
\\
&\Longrightarrow
\text{construct a covariant impurity operator}
\\
&\Longrightarrow
\text{separate short- and long-range components}
\\
&\Longrightarrow
\text{prove a well-posed crossover criterion}
\\
&\Longrightarrow
\text{bound observable errors}
\\
&\Longrightarrow
\text{validate the bounds numerically}.
\end{aligned}
}
$$

The central publishable result is not merely that an effective-mass fit can be produced. It is that the reduction is representation controlled, quantitatively bounded, and valid beyond an explicitly determined atomistic region.

---
