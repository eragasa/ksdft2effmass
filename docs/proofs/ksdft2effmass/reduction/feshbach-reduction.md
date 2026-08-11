# Feshbach and Excluded-Space Reduction

> Status: Proposed proof material. Structural decomposition does not establish mathematical correctness, numerical verification, scientific validation, or human acceptance.

## 6. Controlled Elimination of Excluded States

### 6.1 Retained and excluded subspaces

Let

$$
\hat P+\hat Q=\hat I,
\qquad
\hat Q=\hat I-\hat P.
$$

### 6.2 Exact reduced operator

Derive the Feshbach or Schur-complement operator

$$
\hat H_{\mathrm{eff}}(E)
=
\hat P\hat H\hat P
+
\hat P\hat H\hat Q
\left(
E-\hat Q\hat H\hat Q
\right)^{-1}
\hat Q\hat H\hat P.
$$

### 6.3 Theorem 5: Excluded-space correction bound

Let

$$
\Delta_Q
=
\operatorname{dist}
\left(
E,\sigma(\hat Q\hat H\hat Q)
\right).
$$

Prove

$$
\left\|
\hat P\hat H\hat Q
\left(
E-\hat Q\hat H\hat Q
\right)^{-1}
\hat Q\hat H\hat P
\right\|
\leq
\frac{
\|\hat P\hat H\hat Q\|^2
}{
\Delta_Q
}.
$$

### 6.4 Physical interpretation

Use the bound to determine when:

- single-band reduction is sufficient;
- multivalley coupling must be retained;
- valence-band mixing cannot be neglected;
- excluded atomic orbitals materially affect impurity states.

---
