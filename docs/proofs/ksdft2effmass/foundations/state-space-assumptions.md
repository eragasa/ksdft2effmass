# State-Space Assumptions

> Status: Proposed proof material. Structural decomposition does not establish mathematical correctness, numerical verification, scientific validation, or human acceptance.

## Mathematical Setting

### State Spaces for Atomistic-to-Continuum Reduction

#### System Labels and Comparison Setting

Let $s\in\{b,d\}$ where $b$ denotes the pristine bulk-Si reference and $d$ denotes a substitutionally doped system, such as $d=\mathrm P$ or $d=\mathrm B$.

For direct impurity extraction, the pristine and doped calculations must use compatible:
- supercell geometries;
- boundary conditions;
- Brillouin-zone sampling;
- spin conventions;
- numerical basis conventions;
- retained-subspace dimensions.

The pristine reference may originate from a primitive-cell calculation, but it must be folded or reconstructed in the doped-supercell representation before operator subtraction.

Let $\Omega_L\subset\mathbb R^3$ denote the periodic supercell used for the comparison, where $L$ collectively denotes its linear dimensions.
#### Ambient Numerical State Spaces

Let $\mathcal K_L$ be the finite set of supercell Bloch wavevectors used in the calculation. For each system $s$ and wavevector $\mathbf k\in\mathcal K_L$, let $\mathcal H_s^{\mathrm{num}}(\mathbf k) \cong \mathbb C^{D_s(\mathbf k)}$ denote the ambient numerical Bloch-fiber space.

Here, $D_s(\mathbf k)$ is the dimension of the numerical basis used to represent the Kohn–Sham problem at $\mathbf k$.

The complete finite numerical state space is

$$
\mathcal H_s^{\mathrm{num}}
=
\bigoplus_{\mathbf k\in\mathcal K_L}
\mathcal H_s^{\mathrm{num}}(\mathbf k).
$$

For vectors

$$
|\Psi_s\rangle
=
\bigoplus_{\mathbf k}
|\psi_s(\mathbf k)\rangle,
\qquad
|\Phi_s\rangle
=
\bigoplus_{\mathbf k}
|\phi_s(\mathbf k)\rangle,
$$

the numerical inner product is

$$
\langle\Psi_s|\Phi_s\rangle
=
\sum_{\mathbf k\in\mathcal K_L}
w_{\mathbf k}
\langle
\psi_s(\mathbf k)
|
\phi_s(\mathbf k)
\rangle,
$$

where $w_{\mathbf k}>0$ are the normalized Brillouin-zone weights satisfying

$$
\sum_{\mathbf k\in\mathcal K_L}w_{\mathbf k}=1.
$$

For a $\Gamma$-only supercell calculation,

$$
\mathcal K_L=\{\mathbf 0\},
$$

and the direct sum contains only one fiber.

#### Pristine Retained Space

For each $\mathbf k\in\mathcal K_L$, let $\hat P_b(\mathbf k): \mathcal H_b^{\mathrm{num}}(\mathbf k) \rightarrow \mathcal H_b^{\mathrm{num}}(\mathbf k)$ be an orthogonal projector satisfying

$$\begin{gather}
\hat P_b(\mathbf k)^2 = \hat P_b(\mathbf k) \\
\hat P_b(\mathbf k)^\dagger = \hat P_b(\mathbf k).
\end{gather}$$

Its range is the retained pristine Bloch-fiber subspace:

$$
\mathcal H_b^{(P)}(\mathbf k)
=
\operatorname{Ran}\hat P_b(\mathbf k).
$$

The complete pristine retained space is

$$
\boxed{
\mathcal H_b^{(P)}
=
\bigoplus_{\mathbf k\in\mathcal K_L}
\mathcal H_b^{(P)}(\mathbf k)
}.
$$

Equivalently, define

$$
\hat P_b
=
\bigoplus_{\mathbf k\in\mathcal K_L}
\hat P_b(\mathbf k),
$$

so that

$$
\mathcal H_b^{(P)}
=
\operatorname{Ran}\hat P_b
\subset
\mathcal H_b^{\mathrm{num}}.
$$

Let $m_b(\mathbf k)=\operatorname{rank}\hat P_b(\mathbf k)$ denote the retained dimension at $\mathbf k$. The total finite dimension is

$$
M_b
=
\sum_{\mathbf k\in\mathcal K_L}
m_b(\mathbf k).
$$

The pristine retained Hamiltonian is the operator

$$
\hat H_b^{(P)}
=
\left.
\hat P_b\hat H_b\hat P_b
\right|_{\mathcal H_b^{(P)}}:
\mathcal H_b^{(P)}
\rightarrow
\mathcal H_b^{(P)}.
$$

The ambient compression

$$
\hat P_b\hat H_b\hat P_b
$$

and the restricted operator $\hat H_b^{(P)}$ represent the same action but have different declared domains and codomains.

#### Doped Retained Space

For each $\mathbf k\in\mathcal K_L$, let

$$
\hat P_d(\mathbf k):
\mathcal H_d^{\mathrm{num}}(\mathbf k)
\rightarrow
\mathcal H_d^{\mathrm{num}}(\mathbf k)
$$

be an orthogonal projector onto the selected doped subspace.

Define

$$
\mathcal H_d^{(P)}(\mathbf k)
=
\operatorname{Ran}\hat P_d(\mathbf k).
$$

The complete doped retained space is

$$
\boxed{
\mathcal H_d^{(P)}
=
\bigoplus_{\mathbf k\in\mathcal K_L}
\mathcal H_d^{(P)}(\mathbf k)
}.
$$

Equivalently,

$$
\hat P_d
=
\bigoplus_{\mathbf k\in\mathcal K_L}
\hat P_d(\mathbf k),
$$

and

$$
\mathcal H_d^{(P)}
=
\operatorname{Ran}\hat P_d
\subset
\mathcal H_d^{\mathrm{num}}.
$$

Let

$$
m_d(\mathbf k)
=
\operatorname{rank}\hat P_d(\mathbf k),
$$

with total dimension

$$
M_d
=
\sum_{\mathbf k\in\mathcal K_L}
m_d(\mathbf k).
$$

The doped retained Hamiltonian is

$$
\hat H_d^{(P)}
=
\left.
\hat P_d\hat H_d\hat P_d
\right|_{\mathcal H_d^{(P)}}:
\mathcal H_d^{(P)}
\rightarrow
\mathcal H_d^{(P)}.
$$

#### 5. Compatibility of the Retained Atomistic Spaces

The spaces $\mathcal H_b^{(P)}$ and  $\mathcal H_d^{(P)}$ are distinct physical subspaces. Even if they have the same dimension, they are not automatically identified.

A unitary identification map $\hat U_d: \mathcal H_b^{(P)} \rightarrow\mathcal H_d^{(P)}$ can exist only if $M_b=M_d$.

For fiberwise alignment, the stronger condition is $m_b(\mathbf k)=m_d(\mathbf k)$ for every $\mathbf k\in\mathcal K_L$.

The identification map must satisfy

$$\begin{gather}
\hat U_d^\dagger\hat U_d = \hat I_{\mathcal H_b^{(P)}} \\
\hat U_d\hat U_d^\dagger = \hat I_{\mathcal H_d^{(P)}}
\end{gather}$$

The doped Hamiltonian pulled back to the pristine retained space is
$$
\hat H_{d\rightarrow b}^{(P)}
=
\hat U_d^\dagger
\hat H_d^{(P)}
\hat U_d.
$$

Both

$$
\hat H_{d\rightarrow b}^{(P)}
\qquad\text{and}\qquad
\hat H_b^{(P)}
$$

then act on the common state space $\mathcal H_b^{(P)}$.

The aligned impurity operator is therefore

$$
\boxed{
\Delta\hat H_d^{(P)}
=
\hat U_d^\dagger
\hat H_d^{(P)}
\hat U_d
-
\hat H_b^{(P)}
}
:
\mathcal H_b^{(P)}
\rightarrow
\mathcal H_b^{(P)}.
$$

If $M_b\neq M_d$, the map cannot be unitary. A partial isometry or common lower-dimensional comparison space would then have to be defined explicitly.

#### Localized Wannier-Coordinate Space

Choose an orthonormal localized basis for the doped retained space:

$$
\mathcal W_d = \{|w_{\alpha,d}\rangle\}_{\alpha=1}^{M_d},
$$
satisfying

$$
\langle
w_{\alpha,d}
|
w_{\beta,d}
\rangle
=
\delta_{\alpha\beta},
$$

and

$$
\operatorname{span}\mathcal W_d
=
\mathcal H_d^{(P)}.
$$

Define the Wannier synthesis map

$$
\hat W_d:
\mathbb C^{M_d}
\rightarrow
\mathcal H_d^{(P)}
$$

by

$$
\hat W_d\mathbf c
=
\sum_{\alpha=1}^{M_d}
c_\alpha
|w_{\alpha,d}\rangle.
$$

Because the Wannier basis is orthonormal and complete in the retained space,

$$
\hat W_d^\dagger\hat W_d
=
\mathbf I_{M_d},
$$

and

$$
\hat W_d\hat W_d^\dagger
=
\hat I_{\mathcal H_d^{(P)}}.
$$

Therefore,

$$
\boxed{
\mathbb C^{M_d}
\cong
\mathcal H_d^{(P)}
}
$$

through the unitary coordinate map $\hat W_d$.

The coordinate vector of a retained doped state $|\psi_d\rangle$ is

$$
\mathbf c_d
=
\hat W_d^\dagger|\psi_d\rangle,
$$

with components

$$
c_{\alpha,d}
=
\langle
w_{\alpha,d}
|
\psi_d
\rangle.
$$

The Wannier matrix of the doped retained Hamiltonian is

$$
\mathbf H_{W,d}
=
\hat W_d^\dagger
\hat H_d^{(P)}
\hat W_d
\in
\mathbb C^{M_d\times M_d}.
$$

The space $\mathbb C^{M_d}$ is not an additional physical approximation. It is the finite coordinate representation of the same retained atomistic state space:

$$
\mathcal H_d^{(P)}
\xleftrightarrow[\hat W_d^\dagger]{\hat W_d}
\mathbb C^{M_d}.
$$

---

## Common Wannier Coordinates for Impurity Extraction

Choose corresponding orthonormal Wannier synthesis maps

$$
\hat W_b:
\mathbb C^M
\rightarrow
\mathcal H_b^{(P)},
$$

and

$$
\hat W_d:
\mathbb C^M
\rightarrow
\mathcal H_d^{(P)},
$$

where

$$
M=M_b=M_d.
$$

Let

$$
\mathbf A_d\in\mathbb C^{M\times M}
$$

be a unitary coordinate-alignment matrix. Then the physical identification map can be written as

$$
\hat U_d
=
\hat W_d
\mathbf A_d
\hat W_b^\dagger.
$$

The pristine and doped Wannier matrices are

$$
\mathbf H_{W,b}
=
\hat W_b^\dagger
\hat H_b^{(P)}
\hat W_b,
$$

and

$$
\mathbf H_{W,d}
=
\hat W_d^\dagger
\hat H_d^{(P)}
\hat W_d.
$$

The aligned doped matrix in pristine coordinates is

$$
\mathbf H_{W,d\rightarrow b}
=
\mathbf A_d^\dagger
\mathbf H_{W,d}
\mathbf A_d.
$$

The impurity matrix in the shared coordinate space is therefore

$$
\boxed{
\Delta\mathbf H_{W,d}
=
\mathbf A_d^\dagger
\mathbf H_{W,d}
\mathbf A_d
-
\mathbf H_{W,b}
}.
$$

This subtraction is meaningful because both matrices now act on the same coordinate space $\mathbb C^M$ with the same orbital, site, spin, and lattice ordering.

#### Continuum Envelope-Function Space

Let $\mathcal V_d$ denote the finite-dimensional internal band-edge space retained by the effective-mass model:

$$
\mathcal V_d \cong \mathbb C^{g_d}.
$$

The dimension $g_d$ counts the internal envelope components required by the model. Depending on the physical approximation, these components may represent:

- conduction-band valleys;
- valence-band components;
- spin components;
- spin–orbit-coupled band-edge states.

The continuum state is a vector-valued envelope function

$$
\mathbf F_d:
\Omega
\rightarrow
\mathcal V_d.
$$

For direct comparison with a finite periodic supercell, take

$$
\Omega=\Omega_L
$$

and impose periodic boundary conditions.

The finite-supercell continuum state space is

$$
\boxed{
\mathcal H_{\mathrm{EMT},d}^{(L)}
=
L_{\mathrm{per}}^2
\left(
\Omega_L;
\mathcal V_d
\right)
}.
$$

Its inner product is

$$
\langle
\mathbf F_d,
\mathbf G_d
\rangle_{\mathrm{EMT}}
=
\int_{\Omega_L}
\mathbf F_d(\mathbf r)^\dagger
\mathbf G_d(\mathbf r)
\,\mathrm d^3r.
$$

For the isolated-impurity limit, the state space becomes

$$
\boxed{
\mathcal H_{\mathrm{EMT},d}^{(\infty)}
=
L^2
\left(
\mathbb R^3;
\mathcal V_d
\right)
}.
$$

The isolated bound-state envelopes satisfy appropriate decay conditions:

$$
\lim_{|\mathbf r|\rightarrow\infty}
\mathbf F_d(\mathbf r)
=
\mathbf 0.
$$

The distinction is therefore

$$
\mathcal H_{\mathrm{EMT},d}^{(L)}
\quad\text{for finite-supercell comparison},
$$

and

$$
\mathcal H_{\mathrm{EMT},d}^{(\infty)}
\quad\text{for the physical isolated-impurity limit}.
$$

---

## 9. Effective-Mass Operator and Its Domain

The continuum state space is $L^2$, but the differential Hamiltonian is not defined on every $L^2$ function.

For a second-order effective-mass operator, define an operator domain such as

$$
\mathcal D(
\hat H_{\mathrm{EMT},d}^{(L)}
)
\subset
H_{\mathrm{per}}^2
\left(
\Omega_L;
\mathcal V_d
\right).
$$

The effective-mass Hamiltonian is

$$
\hat H_{\mathrm{EMT},d}^{(L)}
:
\mathcal D(
\hat H_{\mathrm{EMT},d}^{(L)}
)
\rightarrow
\mathcal H_{\mathrm{EMT},d}^{(L)}.
$$

A general multicomponent form is

$$
\hat H_{\mathrm{EMT},d}
=
\hat T_d^{\mathrm{EMT}}
+
\hat V_{\mathrm{scr},d}
+
\hat V_{\mathrm{sr},d},
$$

where:

- $\hat T_d^{\mathrm{EMT}}$ is the band-edge kinetic operator;
- $\hat V_{\mathrm{scr},d}$ is the long-range screened impurity operator;
- $\hat V_{\mathrm{sr},d}$ is a short-range correction.

For a single anisotropic band,

$$
\hat T_d^{\mathrm{EMT}}
=
-\frac{\hbar^2}{2}
\nabla\cdot
\mathbf m_d^{*-1}
\nabla.
$$

For multivalley or multiband models, $\hat T_d^{\mathrm{EMT}}$ is matrix valued on $\mathcal V_d$.
#### Continuum and Wannier Spaces Are Not Automatically Identical

The spaces $\mathcal H_{\mathrm{EMT},d}$ and $\mathbb C^{M_d}$ must not be identified directly.

The continuum space is generally infinite dimensional:

$$
\dim\mathcal H_{\mathrm{EMT},d}
=
\infty,
$$

whereas

$$
\dim\mathbb C^{M_d}
=
M_d<\infty.
$$

A discretization or comparison map must therefore be introduced.

Choose a finite-dimensional continuum trial space

$$
\mathcal X_{h,d}
\subset
\mathcal H_{\mathrm{EMT},d}^{(L)},
$$

where $h$ denotes the continuum discretization scale.

Let

$$
N_{h,d}
=
\dim\mathcal X_{h,d}.
$$

A discretized continuum state then has coordinates in

$$
\mathbb C^{N_{h,d}}.
$$

To compare it with the Wannier representation, define an explicit map

$$
\mathbf J_{h,d}:
\mathbb C^{N_{h,d}}
\rightarrow
\mathbb C^{M_d}.
$$

This map may perform:

- sampling at Wannier centers;
- projection onto localized orbitals;
- interpolation between continuum and lattice coordinates;
- valley-to-orbital reconstruction;
- quadrature-weight normalization.

The continuum operator represented in Wannier coordinates is then constructed from:

1. the continuum discretization;
2. the chosen continuum basis;
3. the comparison map $\mathbf J_{h,d}$;
4. any required overlap or metric matrices.

No atomistic–continuum operator residual is meaningful until $\mathbf J_{h,d}$ has been specified.

#### State-Space Hierarchy

The atomistic side is

$$
\mathcal H_s^{\mathrm{num}}
\supset
\mathcal H_s^{(P)}
\cong
\mathbb C^{M_s}.
$$

The continuum side is

$$
\mathcal H_{\mathrm{EMT},d}
\supset
\mathcal X_{h,d}
\cong
\mathbb C^{N_{h,d}}.
$$

The two numerical coordinate spaces are related by

$$
\mathbf J_{h,d}:
\mathbb C^{N_{h,d}}
\rightarrow
\mathbb C^{M_d}.
$$

The complete comparison structure is therefore

$$
\boxed{
\begin{aligned}
\mathcal H_b^{(P)}
&\xrightarrow{\hat U_d}
\mathcal H_d^{(P)}
\xleftrightarrow{\hat W_d}
\mathbb C^{M_d},
\\[4pt]
\mathcal H_{\mathrm{EMT},d}
&\supset
\mathcal X_{h,d}
\cong
\mathbb C^{N_{h,d}}
\xrightarrow{\mathbf J_{h,d}}
\mathbb C^{M_d}.
\end{aligned}
}
$$

This structure distinguishes:

- the physical atomistic retained spaces;
- their finite Wannier coordinates;
- the infinite-dimensional continuum state space;
- the finite continuum discretization;
- the map required to compare continuum and atomistic operators.

---

## 12. Definitions

##### Definition 1: Pristine retained space
The pristine retained space is

$$
\mathcal H_b^{(P)}
=
\operatorname{Ran}\hat P_b,
$$

where $\hat P_b$ is the orthogonal projector onto the selected pristine Kohn–Sham subspace represented in the comparison supercell.

### Definition 2: Doped retained space

The doped retained space is

$$
\mathcal H_d^{(P)}
=
\operatorname{Ran}\hat P_d,
$$

where $\hat P_d$ is the orthogonal projector onto the selected doped Kohn–Sham subspace.

### Definition 3: Continuum envelope-function space

The finite-supercell continuum envelope-function space is

$$
\mathcal H_{\mathrm{EMT},d}^{(L)}
=
L_{\mathrm{per}}^2(
\Omega_L;\mathcal V_d
),
$$

where $\mathcal V_d$ contains the retained band-edge, valley, and spin components.

The isolated-impurity space is

$$
\mathcal H_{\mathrm{EMT},d}^{(\infty)}
=
L^2(
\mathbb R^3;\mathcal V_d
).
$$

### Definition 4: Localized Wannier-coordinate space

The localized Wannier-coordinate space is

$$
\mathbb C^{M_d},
$$

together with the unitary synthesis map

$$
\hat W_d:
\mathbb C^{M_d}
\rightarrow
\mathcal H_d^{(P)}.
$$

It is a coordinate representation of the retained atomistic space and is not itself a continuum approximation.
### 2.1 State spaces

Define:

- pristine retained space $\mathcal H_b^{(P)}$;
- doped retained space $\mathcal H_d^{(P)}$;
- continuum envelope-function space $\mathcal H_{\mathrm{EMT},d}$;
- localized Wannier-coordinate space $\mathbb C^{M_d}$.

### 2.2 Operators

Introduce:

$$
\hat H_b,
\qquad
\hat H_d,
\qquad
\hat U_d:
\mathcal H_b^{(P)}
\rightarrow
\mathcal H_d^{(P)}.
$$

Define the aligned impurity operator:

$$
\Delta\hat H_d
=
\hat U_d^\dagger
\hat H_d
\hat U_d
-
\hat H_b.
$$

### 2.3 Localized representation

Let $\{|w_\alpha\rangle\}$ be a localized basis. Define

$$
\Delta H_{W,d}[\alpha\beta]
=
\langle w_\alpha|
\Delta\hat H_d
|w_\beta\rangle.
$$

### 2.4 Continuum model

Define

$$
\hat H_{\mathrm{EMT},d}
=
-\frac{\hbar^2}{2}
\nabla\cdot
\mathbf m_d^{*-1}
\nabla
+
V_{\mathrm{scr},d}(\mathbf r)
+
V_{\mathrm{sr},d}(\mathbf r).
$$

Specify the map that represents the continuum operator in the retained atomistic state space.

### 2.5 Norms and geometric restrictions

Define:

- operator norm;
- Frobenius or Hilbert–Schmidt norm;
- orbital-block norms;
- neighbor-shell norms;
- exterior projector $\hat P_{>R}$.

The selected norm must be stated explicitly for every theorem and numerical metric.

---
