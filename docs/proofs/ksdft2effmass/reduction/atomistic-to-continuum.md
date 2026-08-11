# Atomistic-to-Continuum Reduction

> Status: Proposed proof material. Structural decomposition does not establish mathematical correctness, numerical verification, scientific validation, or human acceptance.

## 7. Atomistic-to-Envelope Consistency

### 7.1 Scale-separation assumption

Let:

- $a$ be the lattice spacing;
- $L$ be the characteristic envelope length.

Assume

$$
\frac{a}{L}\ll 1.
$$

### 7.2 Band expansion

Near a band extremum $\mathbf k_0$,

$$
E_n(\mathbf k_0+\mathbf q)
=
E_n(\mathbf k_0)
+
\frac{\hbar^2}{2}
\mathbf q^{\mathsf T}
\mathbf m_n^{*-1}
\mathbf q
+
O(|\mathbf q|^3).
$$

### 7.3 Theorem 6: Effective-mass consistency

Derive an error estimate for replacing the atomistic host operator with the quadratic effective-mass operator.

Express the leading error in powers of

$$
\frac{a}{L}.
$$

### 7.4 Silicon-specific structure

The proof must retain:

- six conduction-band valleys for donor states;
- valence-band degeneracy for acceptor states;
- anisotropic effective masses;
- spin–orbit coupling where required.

A scalar single-valley derivation can be introductory but cannot be the final silicon result.

---
