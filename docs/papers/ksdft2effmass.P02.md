# PAPER II: OBSERVABLE-PRESERVING SPARSE REDUCTION OF FIRST-PRINCIPLES IMPURITY OPERATORS IN SILICON

## Status

- **Paper position:** Paper II
- **Primary program notes:** `ksdft2Effmass.07` and `ksdft2Effmass.08`
- **Required input:** aligned Wannier impurity operators from Paper I
- **Primary systems:** substitutional phosphorus and boron in silicon
- **Primary output:** minimal reduced impurity operators preserving specified low-energy states and observables
- **Continuum fitting:** reserved for Paper III

---

## Central Research Question

For each dopant

$$
d
\in
\mathcal D
=
\{
\mathrm P,
\mathrm B
\},
$$

what is the smallest physically interpretable impurity operator

$$
\Delta\mathbf H_{\mathrm{red},d}
$$

that reproduces the target states, subspaces, spectra, and observables of the aligned first-principles Wannier impurity operator

$$
\Delta\mathbf H_{\mathrm W,d}
$$

within prescribed error tolerances?

---

## Central Claim

The first-principles impurity operator is compressible in a localized Wannier basis, but the degree and physical form of this compression must be determined from observable-preserving error criteria rather than from matrix-element magnitude alone.

The reduction is

$$
\Delta\mathbf H_{\mathrm W,d}
\longrightarrow
\Delta\mathbf H_{\mathrm{red},d}
=
\sum_{j=1}^{J}
\theta_{j,d}
\mathbf O_j,
$$

where:

- $\mathbf O_j$ is a Hermitian operator component with a specified physical interpretation;
- $\theta_{j,d}$ is its fitted coefficient for dopant $d$;
- $J$ is the number of candidate operator components.

The selected model is the least complex model satisfying all required validation criteria.

---

## Dependencies

Paper I must provide:

1. a validated bulk Wannier Hamiltonian

   $$
   \overline{\mathbf H}_{\mathrm W,\mathrm b};
   $$

2. a validated dopant Wannier Hamiltonian

   $$
   \overline{\mathbf H}_{\mathrm W,d};
   $$

3. a physically justified bulk–dopant alignment map

   $$
   \mathbf U_d;
   $$

4. the aligned impurity operator

   $$
   \Delta\mathbf H_{\mathrm W,d}
   =
   \overline{\mathbf H}_{\mathrm W,d}
   -
   \mathbf U_d
   \overline{\mathbf H}_{\mathrm W,\mathrm b}
   \mathbf U_d^\dagger.
   $$

Paper II treats these objects as fixed inputs. It does not repeat the entire alignment construction, although sufficient definitions must be included to make the paper self-contained.

---

## Working Hypotheses

### Hypothesis 1: Spatial Compressibility

The magnitude of the impurity-induced matrix elements decreases with distance from the dopant, permitting a finite-range approximation

$$
\Delta\mathbf H_{\mathrm W,d}
\approx
\Delta\mathbf H_{R,d},
$$

where $\Delta\mathbf H_{R,d}$ retains only operator components associated with sites or bonds inside a radius $R$ of the dopant.

### Hypothesis 2: Near-Defect Orbital Structure

A scalar onsite perturbation may be insufficient near the dopant. Orbital-dependent onsite terms or hopping modifications may be required to preserve the target impurity subspace.

### Hypothesis 3: Dopant-Dependent Minimal Models

The minimal operator structures for phosphorus and boron need not be identical:

$$
\Delta\mathbf H_{\mathrm{red},\mathrm P}
\not\sim
\Delta\mathbf H_{\mathrm{red},\mathrm B}.
$$

Their differences may arise from the distinct orbital characters of donor and acceptor states.

### Hypothesis 4: Operator Error and Observable Error Are Distinct

A model with a small global matrix-reconstruction error does not necessarily preserve the bound-state spectrum or target subspace. Model selection must therefore include both operator-level and observable-level errors.

---

# 1. Introduction

## 1.1 Effective Models of Semiconductor Impurities

Introduce the hierarchy of semiconductor impurity descriptions:

$$
\text{first-principles electronic structure}
\longrightarrow
\text{localized lattice Hamiltonian}
\longrightarrow
\text{reduced impurity operator}
\longrightarrow
\text{continuum impurity model}.
$$

Explain why first-principles calculations contain substantially more information than is normally retained by semiconductor effective models.

## 1.2 The Model-Selection Problem

State that the existence of a Wannier Hamiltonian does not determine:

- which onsite terms must be retained;
- whether orbital dependence is required;
- which hopping modifications are significant;
- how far the defect perturbation extends;
- which terms control the impurity bound states.

The problem is therefore an operator-selection problem.

## 1.3 Limitations of Band-Only Fitting

Explain that agreement between band energies does not guarantee agreement between:

- eigenvectors;
- target subspaces;
- localized defect states;
- valley composition;
- binding energies;
- spatial envelopes;
- operator matrix elements.

## 1.4 Relationship to Existing Tight-Binding and Machine-Learning Work

Review work on:

- Wannier-derived tight-binding Hamiltonians;
- truncation of real-space hopping matrices;
- parameterized defect tight-binding models;
- sparse tight-binding parameter selection;
- machine-learned Hamiltonians;
- defect fitting using densities of states or projected densities of states.

State the distinction of the present work:

> The target is the aligned first-principles impurity operator itself, and model selection is constrained by preservation of specified low-energy subspaces and observables.

## 1.5 Contributions

The paper contributes:

1. a physically structured dictionary for decomposing first-principles impurity operators;
2. a hierarchy of nested reduced impurity models;
3. an observable-preserving sparse-selection procedure;
4. operator-, subspace-, spectral-, and state-level validation metrics;
5. a comparison of the minimal impurity operators required for P:Si and B:Si;
6. a validated lattice-level input for the continuum reduction of Paper III.

---

# 2. First-Principles Impurity Operators

## 2.1 Aligned Wannier Representation

Let

$$
\{
\lvert w_{i\alpha}\rangle
\}
$$

denote the common aligned Wannier basis, where:

- $i$ labels a localized lattice site;
- $\alpha$ labels an orbital associated with that site.

The aligned bulk and dopant Hamiltonians are represented by

$$
\overline{\mathbf H}_{\mathrm W,\mathrm b}
$$

and

$$
\overline{\mathbf H}_{\mathrm W,d}.
$$

The corresponding impurity perturbation is

$$
\Delta\mathbf H_{\mathrm W,d}
=
\overline{\mathbf H}_{\mathrm W,d}
-
\overline{\mathbf H}_{\mathrm W,\mathrm b}.
$$

Clarify that the alignment transformation has already been incorporated into the barred matrices.

## 2.2 Reference and Reduced Hamiltonians

Define the full reference Hamiltonian for dopant $d$ as

$$
\mathbf H_{\mathrm{ref},d}
=
\overline{\mathbf H}_{\mathrm W,\mathrm b}
+
\Delta\mathbf H_{\mathrm W,d}.
$$

For a candidate reduced impurity operator $\Delta\mathbf H_{\mathrm{red},d}$, define

$$
\mathbf H_{\mathrm{red},d}
=
\overline{\mathbf H}_{\mathrm W,\mathrm b}
+
\Delta\mathbf H_{\mathrm{red},d}.
$$

The reduction is evaluated by comparing both the operators and the physical predictions of these two Hamiltonians.

## 2.3 Matrix-Element Classification

Each matrix element is

$$
\left[
\Delta\mathbf H_{\mathrm W,d}
\right]_{i\alpha,j\beta}
=
\left\langle
w_{i\alpha}
\middle|
\Delta\hat H_d
\middle|
w_{j\beta}
\right\rangle.
$$

Classify the elements as:

- onsite if $i=j$;
- hopping or nonlocal if $i\neq j$;
- orbital diagonal if $\alpha=\beta$;
- orbital mixing if $\alpha\neq\beta$.

## 2.4 Distance Measures

Let $\mathbf R_d$ denote the dopant position and $\mathbf R_i$ the center associated with site $i$.

Define the site distance

$$
r_i
=
\left|
\mathbf R_i
-
\mathbf R_d
\right|.
$$

For a bond connecting sites $i$ and $j$, define a dopant-relative bond distance, for example,

$$
r_{ij}
=
\left|
\frac{
\mathbf R_i+\mathbf R_j
}{2}
-
\mathbf R_d
\right|.
$$

State the convention used consistently throughout the analysis.

---

# 3. Physically Structured Operator Dictionary

## 3.1 General Expansion

Construct the candidate reduced operator as

$$
\Delta\mathbf H_{\mathrm{red},d}
=
\sum_{j=1}^{J}
\theta_{j,d}
\mathbf O_j.
$$

Every dictionary element $\mathbf O_j$ must:

- be Hermitian;
- have a physical interpretation;
- preserve required symmetry relations;
- belong to a defined spatial shell or orbital channel.

## 3.2 Scalar Onsite Operators

Define a scalar onsite contribution as

$$
\mathbf O_{\mathrm{scalar}}
=
\sum_i
v_i
\sum_\alpha
\lvert w_{i\alpha}\rangle
\langle w_{i\alpha}\rvert.
$$

The same onsite shift is applied to all retained orbitals on site $i$.

## 3.3 Orbital-Dependent Onsite Operators

Define

$$
\mathbf O_{\mathrm{orbital}}
=
\sum_{i,\alpha}
v_{i\alpha}
\lvert w_{i\alpha}\rangle
\langle w_{i\alpha}\rvert.
$$

This permits different impurity-induced shifts for different orbital channels.

## 3.4 Onsite Orbital-Mixing Operators

If required by symmetry and the extracted operator, include

$$
\mathbf O_{\mathrm{mix}}
=
\sum_i
\sum_{\alpha\neq\beta}
v_i^{\alpha\beta}
\lvert w_{i\alpha}\rangle
\langle w_{i\beta}\rvert.
$$

Hermiticity requires

$$
v_i^{\beta\alpha}
=
\left(
v_i^{\alpha\beta}
\right)^*.
$$

## 3.5 Hopping Perturbations

Define the impurity-induced hopping correction

$$
\mathbf O_{\mathrm{hop}}
=
\sum_{i\neq j}
\sum_{\alpha,\beta}
\delta t_{i\alpha,j\beta}
\lvert w_{i\alpha}\rangle
\langle w_{j\beta}\rvert.
$$

Hermiticity requires

$$
\delta t_{j\beta,i\alpha}
=
\left(
\delta t_{i\alpha,j\beta}
\right)^*.
$$

## 3.6 Spatial-Shell Grouping

Partition the operator components into shells

$$
\mathcal G
=
\{
G_1,
G_2,
\ldots,
G_{N_G}
\},
$$

where each group may represent:

- one dopant-relative radial shell;
- one bond shell;
- one orbital sector;
- one symmetry-equivalent family of matrix elements;
- one physical operator class.

Group selection should retain or remove complete physically related blocks rather than unrelated individual matrix entries.

---

# 4. Hierarchy of Reduced Impurity Models

## 4.1 Prescribed Nested Hierarchy

Define nested model classes

$$
\mathfrak M_0
\subset
\mathfrak M_1
\subset
\cdots
\subset
\mathfrak M_J.
$$

An initial hierarchy is:

### Model $\mathfrak M_0$: Scalar Onsite

$$
\Delta\mathbf H_d^{(0)}
=
\Delta\mathbf H_{\mathrm{scalar},d}.
$$

### Model $\mathfrak M_1$: Orbital-Dependent Onsite

$$
\Delta\mathbf H_d^{(1)}
=
\Delta\mathbf H_{\mathrm{orbital},d}.
$$

### Model $\mathfrak M_2$: Onsite Plus Local Hopping

$$
\Delta\mathbf H_d^{(2)}
=
\Delta\mathbf H_{\mathrm{orbital},d}
+
\Delta\mathbf H_{\mathrm{hop},d}^{(1)}.
$$

### Model $\mathfrak M_3$: Extended Local Operator

$$
\Delta\mathbf H_d^{(3)}
=
\Delta\mathbf H_{\mathrm{orbital},d}
+
\sum_{\ell=1}^{L}
\Delta\mathbf H_{\mathrm{hop},d}^{(\ell)}.
$$

Here $\ell$ labels successive hopping or dopant-relative spatial shells.

## 4.2 Finite-Range Operator

For a spatial cutoff $R$, define

$$
\left[
\Delta\mathbf H_{R,d}
\right]_{i\alpha,j\beta}
=
\begin{cases}
\left[
\Delta\mathbf H_{\mathrm W,d}
\right]_{i\alpha,j\beta},
&
r_{ij}\leq R,
\\[4pt]
0,
&
r_{ij}>R.
\end{cases}
$$

The finite-range hierarchy is

$$
\Delta\mathbf H_{R_1,d}
\subset
\Delta\mathbf H_{R_2,d}
\subset
\cdots
\subset
\Delta\mathbf H_{\mathrm W,d}.
$$

## 4.3 Complexity Measure

Define the model complexity as either the number of active parameters

$$
K_d
=
\#\{
\theta_{j,d}\neq0
\},
$$

or the number of active physical groups

$$
K_{G,d}
=
\#\{
G:
\|\boldsymbol\theta_{G,d}\|_2>0
\}.
$$

Define the retained fraction

$$
\rho_d
=
\frac{
K_{G,d}
}{
K_{G,d}^{\mathrm{full}}
}.
$$

---

# 5. Observable-Preserving Sparse Reduction

## 5.1 Operator Reconstruction Error

Define the normalized global operator error

$$
\varepsilon_{H,d}
=
\frac{
\left\|
\Delta\mathbf H_{\mathrm W,d}
-
\Delta\mathbf H_{\mathrm{red},d}
\right\|_F
}{
\left\|
\Delta\mathbf H_{\mathrm W,d}
\right\|_F
}.
$$

## 5.2 Target-Subspace Error

Let $\mathbf\Pi_d$ denote the projector onto the target impurity-state subspace.

Define

$$
\varepsilon_{\Pi,d}
=
\frac{
\left\|
\mathbf\Pi_d
\left(
\Delta\mathbf H_{\mathrm W,d}
-
\Delta\mathbf H_{\mathrm{red},d}
\right)
\mathbf\Pi_d
\right\|_F
}{
\left\|
\mathbf\Pi_d
\Delta\mathbf H_{\mathrm W,d}
\mathbf\Pi_d
\right\|_F
}.
$$

## 5.3 Binding-Energy Error

For a target bound state $a$, define

$$
\Delta E_{b,d}^{(a)}
=
E_{b,d,\mathrm{red}}^{(a)}
-
E_{b,d,\mathrm{ref}}^{(a)}.
$$

If several target states are retained, report the maximum and root-mean-square errors.

## 5.4 Subspace Fidelity

Let $\mathbf\Pi_{\mathrm{ref},d}$ and $\mathbf\Pi_{\mathrm{red},d}$ project onto target subspaces of equal dimension $m_d$.

Define

$$
F_d
=
\frac{1}{m_d}
\operatorname{Tr}
\left(
\mathbf\Pi_{\mathrm{ref},d}
\mathbf\Pi_{\mathrm{red},d}
\right).
$$

Then

$$
0
\leq
F_d
\leq
1,
$$

with $F_d=1$ indicating identical target subspaces.

## 5.5 Composite Objective

Define a physically weighted objective

$$
\begin{aligned}
\mathcal L_d
={}&
w_H
\varepsilon_{H,d}^2
+
w_{\Pi}
\varepsilon_{\Pi,d}^2
\\
&+
w_E
\sum_a
\left(
\Delta E_{b,d}^{(a)}
\right)^2
+
w_F
\left(
1-F_d
\right)^2.
\end{aligned}
$$

The weights

$$
w_H,
\quad
w_\Pi,
\quad
w_E,
\quad
w_F
$$

must be specified before model comparison.

## 5.6 Group-Sparse Selection

Determine the reduced model through

$$
\boldsymbol\theta_d^\star
=
\operatorname*{arg\,min}_{\boldsymbol\theta_d}
\left[
\mathcal L_d(\boldsymbol\theta_d)
+
\lambda
\sum_{G\in\mathcal G}
\omega_G
\left\|
\boldsymbol\theta_{G,d}
\right\|_2
\right],
$$

where:

- $\lambda\geq0$ is the regularization strength;
- $\omega_G$ compensates for differences in group size;
- $\boldsymbol\theta_{G,d}$ contains the parameters belonging to group $G$.

## 5.7 Constrained Model Selection

The final model should be selected by constrained complexity minimization:

$$
\begin{aligned}
\operatorname*{minimize}
\quad&
K_{G,d},
\\
\operatorname{subject\ to}
\quad&
\varepsilon_{H,d}
\leq
\varepsilon_H^{\max},
\\
&
\varepsilon_{\Pi,d}
\leq
\varepsilon_\Pi^{\max},
\\
&
\left|
\Delta E_{b,d}^{(a)}
\right|
\leq
\varepsilon_E^{\max},
\\
&
F_d
\geq
F^{\min}.
\end{aligned}
$$

This defines the minimal acceptable model without relying on an arbitrary regularization strength alone.

---

# 6. Computational Methodology

## 6.1 First-Principles Inputs

Summarize the fixed Paper I specifications:

- exchange-correlation approximation;
- pseudopotentials;
- lattice constant;
- supercell sizes;
- structural-relaxation protocol;
- plane-wave cutoffs;
- Brillouin-zone sampling;
- number of bands;
- convergence tolerances.

## 6.2 Wannier Construction

Report:

- target bands;
- initial projections;
- outer windows;
- frozen windows;
- number of Wannier functions;
- Wannier centers and spreads;
- interpolation errors.

## 6.3 Alignment Inputs

Summarize:

- common site ordering;
- orbital correspondence;
- phase and gauge alignment;
- symmetry matching;
- principal-angle or overlap diagnostics.

## 6.4 Operator-Dictionary Construction

Specify:

- site and orbital labels;
- radial-shell definitions;
- bond-shell definitions;
- symmetry-equivalent groups;
- onsite and hopping classes;
- Hermiticity constraints.

## 6.5 Optimization

Specify:

- numerical optimizer;
- regularization path;
- convergence criteria;
- parameter initialization;
- normalization of operator groups;
- treatment of complex matrix elements;
- enforcement of Hermiticity and symmetry.

## 6.6 Validation Protocol

Separate fitting and validation information.

Possible validation divisions include:

- held-out spatial shells;
- held-out matrix-element classes;
- held-out wavevectors;
- held-out target states;
- larger supercells;
- independently generated Wannier specifications.

The bound-state energies and subspace fidelities should not be used only as fitting targets and then reported as independent validation.

## 6.7 Reproducibility

Archive:

- aligned reference matrices;
- operator dictionaries;
- group definitions;
- optimization configurations;
- selected parameters;
- validation scripts;
- software versions;
- input and output hashes.

---

# 7. Results

## 7.1 Structure of the Full Impurity Operators

Present:

- onsite perturbation maps;
- orbital-resolved onsite shifts;
- hopping perturbation magnitudes;
- radial decay profiles;
- symmetry structure;
- comparison between P and B.

## 7.2 Compressibility in the Wannier Basis

Plot cumulative retained norm:

$$
\eta_d(R)
=
\frac{
\left\|
\Delta\mathbf H_{R,d}
\right\|_F^2
}{
\left\|
\Delta\mathbf H_{\mathrm W,d}
\right\|_F^2
}.
$$

Determine how rapidly the full impurity operator is reconstructed as $R$ increases.

## 7.3 Performance of the Prescribed Hierarchy

Compare:

- scalar onsite;
- orbital-dependent onsite;
- onsite plus local hopping;
- extended local operator;
- full Wannier impurity operator.

Report all `.08` validation metrics for each model.

## 7.4 Sparse-Selection Path

Present error versus complexity as $\lambda$ varies:

$$
K_{G,d}(\lambda)
\quad\text{versus}\quad
\varepsilon_{H,d}(\lambda),
\qquad
\varepsilon_{\Pi,d}(\lambda),
\qquad
\Delta E_{b,d}(\lambda),
\qquad
F_d(\lambda).
$$

Identify the Pareto-optimal models.

## 7.5 Minimal Phosphorus Impurity Operator

Report:

- retained onsite terms;
- retained orbital channels;
- retained hopping shells;
- active spatial extent;
- parameter count;
- operator error;
- bound-state errors;
- subspace fidelity.

## 7.6 Minimal Boron Impurity Operator

Report the same quantities for B:Si.

## 7.7 Donor–Acceptor Comparison

Determine which operator components are:

- common to both dopants;
- required only for phosphorus;
- required only for boron;
- associated with donor or acceptor orbital character.

## 7.8 Robustness

Test sensitivity to:

- supercell size;
- Wannier outer window;
- frozen window;
- initial projections;
- alignment tolerance;
- operator-group definition;
- regularization strength;
- validation thresholds.

## 7.9 Compression and Computational Benefit

Report:

$$
\operatorname{CompressionRatio}_d
=
\frac{
K_{G,d}^{\mathrm{full}}
}{
K_{G,d}^{\mathrm{selected}}
}.
$$

Compare:

- matrix storage;
- Hamiltonian assembly cost;
- diagonalization cost;
- accuracy of target observables.

---

# 8. Discussion

## 8.1 Is the Impurity Operator Sparse?

Discuss whether the extracted perturbations admit compact local descriptions in the selected Wannier basis.

## 8.2 What Physics Is Lost by Scalar Onsite Reduction?

Identify which target quantities first fail when orbital or hopping structure is removed.

## 8.3 Donor–Acceptor Asymmetry

Interpret differences between the minimal P and B operators in terms of their target band-edge and orbital characters.

## 8.4 Operator Accuracy Versus Observable Accuracy

Discuss cases in which:

- a large global operator error produces small bound-state errors;
- a small global operator error produces unacceptable subspace errors.

This establishes why multiple validation levels are necessary.

## 8.5 Dependence on Representation

Discuss the extent to which sparsity and locality depend on:

- Wannier gauge;
- selected target subspace;
- orbital character;
- spatial localization;
- alignment quality.

## 8.6 Implications for Continuum Reduction

Identify which parts of the selected lattice operator are candidates for:

- long-range scalar potential;
- short-range central-cell correction;
- orbital-dependent local correction;
- nonlocal correction.

Do not yet fit or claim a continuum crossover radius. That analysis belongs to Paper III.

## 8.7 Limitations

Discuss:

- dependence on the Kohn–Sham approximation;
- finite-supercell effects;
- charged-defect corrections;
- incompleteness of the retained subspace;
- Wannier gauge dependence;
- uncertainty in alignment;
- limitations of the chosen operator dictionary;
- absence of explicit many-body excitation physics.

---

# 9. Conclusions

Summarize:

1. whether the first-principles impurity operators are compressible;
2. the minimum required operator structure for P:Si;
3. the minimum required operator structure for B:Si;
4. whether hopping corrections are required;
5. how operator compression affects target states and binding energies;
6. which reduced operators should be passed to the continuum analysis.

Conclude with the transition

$$
\Delta\mathbf H_{\mathrm W,d}
\longrightarrow
\Delta\mathbf H_{\mathrm{red},d}
\longrightarrow
V_{\mathrm{eff},d}(\mathbf r),
$$

where the second reduction is addressed in Paper III.

---

# Required Figures

## Figure 1: Reduction Workflow

$$
\Delta\mathbf H_{\mathrm W,d}
\longrightarrow
\text{operator dictionary}
\longrightarrow
\text{sparse selection}
\longrightarrow
\Delta\mathbf H_{\mathrm{red},d}
\longrightarrow
\text{validation}.
$$

## Figure 2: Full Impurity-Operator Structure

Heatmaps or block plots of:

- onsite terms;
- orbital-mixing terms;
- hopping perturbations;
- P/B comparison.

## Figure 3: Radial Decay

Plot impurity-operator norm by radial shell.

## Figure 4: Error–Complexity Pareto Front

Plot validation errors against the number of active operator groups.

## Figure 5: Bound-State Validation

Compare reference and reduced:

- bound-state energies;
- target-state spatial distributions;
- subspace fidelities.

## Figure 6: Selected Minimal Operators

Graphical representation of retained onsite and hopping contributions for P and B.

---

# Required Tables

## Table 1: First-Principles and Wannier Specifications

Include supercell, cutoff, $k$ mesh, band count, Wannier functions, windows, spreads, and interpolation errors.

## Table 2: Operator Dictionary

| Group | Physical meaning | Spatial support | Orbital support | Parameter count |
|---|---|---|---|---:|

## Table 3: Prescribed Model Hierarchy

| Model | Onsite scalar | Orbital onsite | Orbital mixing | Hopping range | Parameters |
|---|---:|---:|---:|---:|---:|

## Table 4: Validation Results

| Dopant | Model | $\varepsilon_H$ | $\varepsilon_\Pi$ | $\Delta E_b$ | $F$ | Active groups |
|---|---|---:|---:|---:|---:|---:|

## Table 5: Final Minimal Operators

| Dopant | Required onsite structure | Required hopping range | Spatial extent | Parameters | Compression ratio |
|---|---|---|---:|---:|---:|

## Table 6: Robustness Tests

| Variation | Selected model changed? | Maximum metric change | Interpretation |
|---|---:|---:|---|

---

# Scope Boundary

Paper II includes:

- the extracted Wannier impurity operator;
- physically structured operator decomposition;
- sparse or constrained model selection;
- state-, subspace-, spectral-, and observable-level validation;
- comparison of phosphorus and boron.

Paper II excludes:

- fitting a screened Coulomb potential;
- determining the final continuum dielectric response;
- defining the continuum crossover radius;
- solving the large-scale effective-mass impurity problem.

Those tasks belong to Paper III.

---

# One-Sentence Paper Result Template

> The aligned first-principles impurity operators of substitutional phosphorus and boron in silicon can be compressed to distinct local operator structures, with specified orbital and hopping components required to preserve their target bound-state subspaces within controlled errors.