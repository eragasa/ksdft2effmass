back_to: [[ksdft2Effmass.papers.00]]

# P01: Operator-Constrained Tight-Binding Reduction of First-Principles Silicon

## Manuscript record

| Field | Value |
|---|---|
| Paper ID | `P01` |
| Combined scope | `P01` + `P02` |
| State | `Waiting` |
| Required gates | `G02`, `G03`, `G04` |
| Primary material | Bulk silicon |
| Parent theory | PBE Kohn--Sham DFT |
| Reference representation | Wannier Hamiltonian |
| Reduced model | Orthogonal, non-SOC $sp^3s^*$ tight-binding Hamiltonian |
| Intended output | Journal article or full conference paper |

The manuscript remains `Waiting` until the computational gates pass. Its
Introduction and Methodology may be drafted before numerical results are
available.

# Working title

**Operator-Constrained Tight-Binding Reduction of First-Principles Silicon in a Wannier Representation**

Alternative title:

**From Kohn--Sham DFT to an $sp^3s^*$ Hamiltonian: Controlled Operator Reduction of Bulk Silicon**

# Central claim

A parameterized tight-binding Hamiltonian should be evaluated as an
approximation to a localized first-principles operator, rather than solely as a
fit to selected band energies.

For bulk silicon, a validated Wannier Hamiltonian provides the finite-dimensional
reference operator. Projection onto a prescribed $sp^3s^*$ model class then
separates:

1. error caused by the restricted tight-binding model class;
2. error caused by parameter fitting;
3. error in the resulting spectra and band-edge observables.

The paper will determine whether reproducing the indirect gap, conduction-valley
position, and electron effective masses also implies that the corresponding
localized operator has been reproduced.

# Research questions

## Primary question

Given a validated bulk-silicon Wannier Hamiltonian, what is the best
approximation within a prescribed orthogonal $sp^3s^*$ Slater--Koster model
class?

## Secondary questions

1. How does an operator-constrained tight-binding model differ from a model
   fitted directly to Kohn--Sham band energies?

2. Which onsite, orbital, hopping, and neighbor-shell components dominate the
   residual operator?

3. What operator accuracy is required to preserve the indirect gap,
   conduction-valley position, and longitudinal and transverse electron
   effective masses?

4. Does agreement on fitted band energies persist at withheld wavevectors?

# Falsifiable claim

Let $\mathbf H_{\mathrm W}$ be the validated Wannier Hamiltonian and let
$\mathfrak M_{sp^3s^*}$ be the selected tight-binding model class.

The primary hypothesis is that there exists

$$\begin{gather}
    \mathbf H_{\mathrm{TB}}^* \in \mathfrak M_{sp^3s^*}
\end{gather}$$

that satisfies the declared band-edge tolerances while retaining a quantitatively
bounded fraction of the Wannier operator.

The hypothesis fails if no model in the declared class simultaneously satisfies:

$$\begin{gather}
\left|\delta E_g\right| \leq 0.05 E_g^{\mathrm{DFT}},
\end{gather}$$

$$\begin{gather}
    \left|\delta k_{\mathrm v}\right| \leq 0.03 \left|\Gamma X\right|,
\end{gather}$$

and

$$\begin{gather}
    \frac{
    \left|
    m_i^{\mathrm{TB}}
    -
    m_i^{\mathrm{DFT}}
    \right|
    }{
    \left|
    m_i^{\mathrm{DFT}}
    \right|
    }
    \leq
    0.08,
    \qquad
    i\in\{l,t\},
\end{gather}$$

where:

- $E_g^{\mathrm{DFT}}$ is the indirect Kohn--Sham gap;
- $k_{\mathrm v}$ is the conduction-valley position;
- $m_l$ is the longitudinal electron effective mass;
- $m_t$ is the transverse electron effective mass.

These tolerances test reduction fidelity relative to the converged Kohn--Sham
parent. They are not claims of agreement between PBE and experiment.

# Operator construction

## Wannier reference

Let $\mathbf H_{\mathrm W}(\mathbf R) \in \mathbb C^{M_{\mathrm W}\times M_{\mathrm W}}$ denote the real-space Wannier Hamiltonian, where $\mathbf{R}$ is a lattice translation and $M_{\mathrm{W}}$ is the number of Wannier orbitals per primitive cell.

Its Bloch representation is

$$\begin{gather}
    \mathbf{H}_{\mathrm{W}}(\mathbf{k})
    =
    \sum_{\mathbf{R}}
    e^{i\mathbf{k} \cdot \mathbf{R}}
    \mathbf{H}_{\mathrm{W}}(\mathbf{R)}.
\end{gather}$$

The Wannier construction must reproduce the selected Kohn--Sham bands within a separately declared interpolation tolerance before it can be used as the operator reference.

## Tight-binding model

Let $\mathbf{H}_{\mathrm{TB}}\left(\mathbf{R};\boldsymbol\theta\right)$ be an orthogonal $sp^3s^*$ tight-binding Hamiltonian with parameter vector $\boldsymbol\theta\in\Theta$. For spinless diamond-structure silicon, the primitive cell contains two sites with five orbitals per site:

$$\begin{gather}
    M_{\mathrm{TB}} = 2 \times 5 = 10.
\end{gather}$$

The orbital set on each site is

$$
  \{
  |s\rangle,
  |p_x\rangle,
  |p_y\rangle,
  |p_z\rangle,
  |s^*\rangle
 \}.
$$

The model specification must freeze:

- orbital ordering;
- onsite parameters;
- Slater-Koster hopping channels;
- hopping range;
- crystal-symmetry constraints;
- energy-zero convention.

# Common operator space

A matrix difference is meaningful only after the Wannier and tight-binding
operators have been placed in a common coordinate space.

For the primary construction, require $M_{\mathrm W} = M_{\mathrm{TB}} = 10$. Let $\mathbf C(\mathbf k) \in U(10)$ map tight-binding coordinates into Wannier coordinates. The aligned tight-binding operator is

$$\begin{gather}
 \widetilde{\mathbf H}_{\mathrm{TB}}
 \left( \mathbf k; \boldsymbol\theta \right)
 =
 \mathbf C(\mathbf k)
 \mathbf H_{\mathrm{TB}}
 \left( \mathbf k; \boldsymbol\theta \right)
 \mathbf C(\mathbf k)^\dagger.
\end{gather}$$

The operator residual is

$$\begin{gather}
 \boxed{
 \mathbf R_{\mathrm{TB}}
 \left(
 \mathbf k;
 \boldsymbol\theta
 \right)
 =
\mathbf H_{\mathrm W}(\mathbf k)
-
\widetilde{\mathbf H}_{\mathrm{TB}}
\left(
\mathbf k;
\boldsymbol\theta
\right)
}.
\end{gather}$$

If a cell-local, $\mathbf k$-independent alignment $\mathbf C$ is available,
the real-space residual is

$$\begin{gather}
  \mathbf{R}_{\mathrm{TB}}
  \left (\mathbf{R}; \boldsymbol{\theta} \right)
  =
  \mathbf{H}_{\mathrm{W}}(\mathbf{R})
  - \mathbf{C} \mathbf{H}_{\mathrm{TB}}
   \left(
     \mathbf R;\boldsymbol\theta
   \right)
   \mathbf C^\dagger
\end{gather}$$

The real-space form permits decomposition by neighbor shell and orbital channel.

# Two reduction objectives

## Direct spectral fit

The direct DFT-to-TB parameters are

$$\begin{gather}
\boldsymbol\theta_E^*
=
\operatorname*{arg\,min}_{\boldsymbol\theta\in\Theta}
\sum_{
(\mathbf k,n)\in\mathcal T
}
q_{n\mathbf k}
\left[
E_{n}^{\mathrm{TB}}
\left(
\mathbf k;
\boldsymbol\theta
\right)
-
E_{n}^{\mathrm{DFT}}(\mathbf k)
\right]^2,
\end{gather}$$

where:

- $\mathcal T$ is the spectral training set;
- $q_{n\mathbf k}\geq0$ is the fitting weight;
- $E_n^{\mathrm{TB}}$ and $E_n^{\mathrm{DFT}}$ are corresponding band energies.

A disjoint set $\mathcal V$ is withheld for validation.

## Operator-constrained fit

The Wannier-to-TB parameters are

$$\begin{gather}
\boldsymbol\theta_H^*
=
\operatorname*{arg\,min}_{\boldsymbol\theta\in\Theta}
\sum_{\mathbf R}
w_{\mathbf R}
\left\|
\mathbf H_{\mathrm W}(\mathbf R)
-
\mathbf C
\mathbf H_{\mathrm{TB}}
\left(
\mathbf R;
\boldsymbol\theta
\right)
\mathbf C^\dagger
\right\|_{\mathrm F}^{2},
\end{gather}$$

where $w_{\mathbf R}\geq0$ is the declared weight for lattice displacement $\mathbf R$ and $\|\cdot\|_{\mathrm F}$ is the Frobenius norm.

The normalized operator error is

$$\begin{gather}
\varepsilon_H
=
\frac{
\left[
\displaystyle
\sum_{\mathbf R}
w_{\mathbf R}
\left\|
\mathbf R_{\mathrm{TB}}(\mathbf R)
\right\|_{\mathrm F}^{2}
\right]^{1/2}
}{
\left[
\displaystyle
\sum_{\mathbf R}
w_{\mathbf R}
\left\|
\mathbf H_{\mathrm W}(\mathbf R)
\right\|_{\mathrm F}^{2}
\right]^{1/2}
}.
\end{gather}$$

The two fitted models, $\mathbf H_{\mathrm{TB}} \left(\boldsymbol\theta_E^*\right)$ and $\mathbf{H}_{\mathrm{TB}}\left(\boldsymbol\theta_{H}^*\right)$ belong to the same model class but optimize different notions of fidelity.
# Manuscript outline

## 1. Introduction

The Introduction will establish:

1. why localized Hamiltonians are needed beyond plane-wave DFT;
2. the role of Wannier interpolation as a representation of a selected
   Kohn--Sham subspace;
3. the role of parameterized tight binding as restriction to a prescribed model
   class;
4. why spectral agreement alone does not define operator agreement;
5. the paper's contribution: a common-space comparison of spectral and
   operator-constrained reductions for bulk silicon.

The Introduction must avoid claiming that Wannierization and tight-binding
fitting are equivalent procedures.

## 2. First-principles reference

Describe:

- PBE Kohn--Sham parent calculation;
- PseudoDojo PBE ONCV pseudopotential;
- PBE-relaxed lattice constant;
- scalar-relativistic, non-SOC, non-spin-polarized treatment;
- SCF and NSCF calculations;
- convergence of the band-edge observables;
- training and withheld validation datasets.

## 3. Wannier Hamiltonian

Describe:

- target rank and energy windows;
- initial projections;
- disentanglement procedure;
- Wannier centers and spreads;
- real-space hopping decay;
- interpolation validation.

## 4. Tight-binding model class

Define:

- the orthogonal $sp^3s^*$ basis;
- onsite and hopping parameters;
- Slater--Koster symmetry constraints;
- neighbor-shell hierarchy;
- parameter bounds and identifiability.

## 5. Alignment and objective functions

Define:

- Wannier and tight-binding state spaces;
- the alignment map $\mathbf C$;
- the spectral objective;
- the operator objective;
- training and validation separation;
- uncertainty and sensitivity procedures.

## 6. Results

### 6.1 Converged Kohn--Sham reference

Report the converged parent band structure and band-edge quantities.

### 6.2 Validated Wannier representation

Report interpolation errors, centers, spreads, and hopping decay.

### 6.3 Direct spectral fit

Report parameters, training errors, and withheld validation errors for

$$\boldsymbol\theta_E^*.$$

### 6.4 Operator-constrained reduction

Report parameters and operator residuals for

$$\boldsymbol\theta_H^*.$$

### 6.5 Comparison of objectives

Compare:

- parameter vectors;
- operator errors;
- spectral errors;
- gap errors;
- valley-position errors;
- effective-mass errors.

### 6.6 Residual operator structure

Resolve the residual by:

- neighbor shell;
- onsite versus hopping contribution;
- orbital block;
- crystal-symmetry channel.

## 7. Discussion

Discuss:

- whether spectral accuracy implies operator fidelity;
- which physical quantities are sensitive to discarded operator components;
- whether nearest-neighbor $sp^3s^*$ is adequate;
- which additional terms are justified by the residual;
- consequences for later impurity-operator reductions.

## 8. Conclusions

State:

- the accepted tight-binding model class;
- its validated domain;
- the measured loss of operator information;
- the limits of the reduction;
- the role of the bulk reference in later P:Si and B:Si work.

# Required figures

1. **Reduction structure**

   ```mermaid
   flowchart LR
       KS["Converged KS reference"]
       W["Validated Wannier operator"]
       D["Direct spectral fit"]
       O["Operator-constrained fit"]
       TB_E["TB model: spectral objective"]
       TB_H["TB model: operator objective"]
       V["Common validation"]

       KS --> W
       KS --> D
       D --> TB_E
       W --> O
       O --> TB_H
       TB_E --> V
       TB_H --> V
       W --> V
   ```

2. **DFT and Wannier validation**

   Band structure with an interpolation-error panel.

3. **Tight-binding comparison**

   DFT, Wannier, direct-fit TB, and operator-fit TB bands over identical
   wavevectors.

4. **Operator residual**

   Residual norm resolved by neighbor shell and orbital block.

5. **Band-edge validation**

   Gap, valley-position, and effective-mass errors for both fitting objectives.

6. **Model-complexity curve**

   Operator and observable errors versus the retained tight-binding model class.

# Required tables

1. First-principles and Wannier calculation specification.
2. Tight-binding model classes and parameter counts.
3. Fitted parameter vectors $\boldsymbol\theta_E^*$ and
   $\boldsymbol\theta_H^*$.
4. Training and withheld-validation errors.
5. Band-edge observables and declared acceptance thresholds.
6. Operator residuals by shell and orbital sector.

# Null-result interpretations

The paper remains interpretable if:

- the nearest-neighbor $sp^3s^*$ model reproduces band edges but has a large
  operator residual;
- operator fitting worsens selected band-edge quantities relative to spectral
  fitting;
- the two objectives produce materially different parameter sets;
- a larger hopping range is required to meet the declared tolerances;
- no stable full-space alignment exists, provided the failure is diagnosed and
  the resulting limitation is reported.

The paper should not claim successful operator reduction if the Wannier--TB
alignment is nonunique or unstable over the validation domain.

# Provisional abstract

Wannier interpolation and parameterized tight-binding fitting provide distinct
reductions of first-principles electronic structure. The former represents a
selected Kohn--Sham subspace in a localized basis, whereas the latter restricts
the Hamiltonian to a prescribed model class. We construct a validated Wannier
Hamiltonian for bulk silicon and compare two reductions to an orthogonal
$sp^3s^*$ Slater--Koster model: direct fitting to Kohn--Sham band energies and
operator-constrained fitting to the aligned Wannier Hamiltonian. The models are
evaluated using withheld band energies, the indirect gap, conduction-valley
position, longitudinal and transverse electron effective masses, and
real-space operator residuals. [Insert principal quantitative result.] The
comparison determines which first-principles operator content is retained by
the compact model and establishes the validated bulk reference required for
subsequent impurity-operator reduction.

# Publication gate

Move this manuscript from `Waiting` to `Analysis` only when:

- `G02`, `G03`, and `G04` have passed;
- the common Wannier--TB alignment is reproducible;
- both fitting objectives have frozen training and validation data;
- the central band/operator comparison figure can be generated;
- the result remains interpretable under the declared null outcomes.

Move it to `Drafting` only after the principal quantitative claim has survived
sensitivity analysis.