# Gauge Equivariance

> Status: Proposed proof material. Structural decomposition does not establish mathematical correctness, numerical verification, scientific validation, or human acceptance.

## 3. Gauge Covariance and Representation Invariance

## Gauge and Gauge Covariance

A gauge can be understood as a **coordinate frame in electronic-state space**. Just as the same geometric vector can have different components in rotated Cartesian coordinates, the same electronic state or operator can have different numerical components in different Bloch or orbital bases.

Let $\mathbf V(\mathbf k)$ define an orthonormal coordinate frame for an $M$-dimensional retained subspace. A different frame for the same subspace is

$$
\mathbf V'(\mathbf k)
=
\mathbf V(\mathbf k)\mathbf G(\mathbf k),
\qquad
\mathbf G(\mathbf k)\in U(M).
$$

The unitary matrix $\mathbf G(\mathbf k)$ rotates the internal coordinates without changing the subspace. Consequently, the projector is gauge invariant:

$$
\mathbf P'(\mathbf k)
=
\mathbf V'(\mathbf k)\mathbf V'(\mathbf k)^\dagger
=
\mathbf P(\mathbf k).
$$

The matrix of an operator contains its components in the chosen electronic coordinate frame. When that frame changes, the components transform as

$$
\mathbf H'(\mathbf k)
=
\mathbf G(\mathbf k)^\dagger
\mathbf H(\mathbf k)
\mathbf G(\mathbf k).
$$

This consistent change of components is **gauge covariance**. The matrix entries depend on the chosen frame, while physical quantities such as the spectrum and unitary-invariant norms do not.

Computationally, separate pristine and doped DFT calculations generally return different electronic coordinate frames because Bloch-state phases and band mixing are arbitrary. Subtracting their Hamiltonian matrices before gauge alignment is like subtracting vector components expressed in differently rotated coordinate systems. The gauges must first be aligned so that the resulting impurity operator represents a physical difference rather than a mismatch of coordinates.

### 3.1 Gauge transformation

For a unitary coordinate transformation $\hat G$,

$$
\hat H_s
\mapsto
\hat G^\dagger\hat H_s\hat G.
$$

### 3.2 Theorem 1: Covariance of impurity extraction

Prove that consistent transformation of the pristine and doped representations gives

$$
\Delta\hat H_d
\mapsto
\hat G^\dagger
\Delta\hat H_d
\hat G.
$$

### 3.3 Corollary 1: Invariance of global residuals

For every unitarily invariant norm,

$$
\left\|
\hat G^\dagger
\Delta\hat H_d
\hat G
\right\|
=
\left\|
\Delta\hat H_d
\right\|.
$$

### 3.4 Spatial-locality complication

Determine whether the exterior projector satisfies

$$
[\hat P_{>R},\hat G]=0.
$$

If it does not, spatially resolved residuals are not invariant under arbitrary gauge transformations.

### 3.5 Required resolution

Either:

1. restrict the admissible gauges to transformations preserving localization centers; or
2. define the exterior restriction geometrically and transform it with the operator.

### 3.6 Publishable result

State precisely which impurity quantities are:

- gauge invariant;
- gauge covariant;
- invariant only under localization-preserving gauges;
- representation dependent.

---
