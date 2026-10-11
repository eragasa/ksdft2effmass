# Compatibility of spectral and operator reductions of a first-principles silicon Hamiltonian

**Eugene Joseph M. Ragasa**<br>
Department of Physics, De La Salle University, Manila, Philippines<br>
eugene.ragasa@dlsu.edu.ph

## Abstract

First-principles Hamiltonians can be reduced to compact lattice models by fitting
selected spectra or by approximating an aligned localized operator. These objectives
constrain different information and need not select the same Hamiltonian. This paper
defines a first-principles bulk-silicon test of their compatibility within a nested
hierarchy of orthogonal ten-orbital $sp^3s^\ast$ Slater–Koster models. The intended
common parent is a numerically qualified, non-spin-polarized, non-spin–orbit-coupled PBE
Kohn–Sham calculation represented in a validated Wannier basis. A spectral loss
constrains training bands and declared band-edge observables. A normalized operator
loss compares real-space hopping matrices after an explicit space-group-compatible
orbital alignment and finite-domain tail gate. The two losses define spectral and
operator admissible sets. A common feasible witness supports compatibility; certified
lower and feasible upper bounds on their minimum distance distinguish class-relative
incompatibility from an inconclusive search. Withheld validation reserves the indirect
gap, conduction-valley location, longitudinal mass, both unaveraged transverse masses,
and shell- and orbital-resolved operator residuals. Parent-model,
numerical-discretization, local-extraction, and model-reduction errors remain separate.
This pre-results manuscript freezes the analysis and evidence contract but reports no
production silicon compatibility or model-selection conclusion. The protected
calculation sequence and pending result records remain in the appendices until
authenticated evidence is available.

**Keywords:** model selection, operator compatibility, silicon, tight-binding
reduction, Wannier Hamiltonian

## I. Introduction

Density-functional theory (DFT) supplies a first-principles Kohn–Sham description of
crystalline electronic structure [1,2]. Plane waves provide a systematic periodic
representation but are inconvenient for interpolation, large cells, and local model
construction. Maximally localized Wannier functions transform a selected Kohn–Sham
subspace into a localized representation whose real-space matrix elements support
interpolation [3–6]. Parameterized tight-binding models impose a smaller basis, finite
hopping range, and symmetry structure [7,8]. This additional restriction introduces
model-reduction error.

A band fit and an operator reduction answer different questions. Eigenvalues do not
uniquely determine eigenvectors, orbital coordinates, onsite matrices, or hopping
blocks. Models with similar selected bands can therefore differ as represented
operators. Conversely, a small matrix residual under one weighting does not guarantee
accurate valley curvature or other band-edge observables. Neither criterion should be
used as an undeclared substitute for the other.

An operator comparison is meaningful only after the state spaces are identified. The
Wannier and tight-binding matrices must share compatible dimensions, orbital content,
lattice translations, units, energy reference, and coordinate ordering. Their
remaining coordinate freedom must be related by an admissible alignment map. Polar
decomposition and principal-angle methods support alignment diagnostics [9,10], but a
small residual alone does not prove that a map respects the silicon space group or
orbital semantics.

This paper asks whether spectral and operator requirements admit a common reduced
silicon Hamiltonian in a prescribed class. Instead of comparing two isolated best fits,
it defines the complete sets accepted by each criterion. If those sets intersect, a
common witness satisfies both reductions. If they are certified to be disjoint, their
minimum separation measures a class-relative obstruction. Failure to find an
intersection without such a certificate remains inconclusive.

The physical branch is restricted to pristine bulk silicon in a scalar-relativistic,
non-spin-polarized, non-SOC treatment. Experimental agreement is not an independent
fit target. All reduction errors are relative to the selected PBE/Wannier parent.
Consequently, even a compatible result would not remove parent-model discrepancy or
establish transfer to defects, optical response, strain, transport, or another physical
branch.

A companion controlled-model manuscript verifies common-space transport, hopping
reconstruction, finite-range reduction, gauge attacks, and changed fitting objectives
in synthetic one- and two-dimensional systems. Those results motivate this application
but cannot select or validate silicon settings.

## II. Methodology

### *2.1 First-principles parent and reference*

The planned production parent fixes the crystal structure, exchange–correlation
functional, pseudopotential, spin treatment, and numerical settings. It uses Quantum
ESPRESSO [11], the Perdew–Burke–Ernzerhof generalized gradient approximation [12], and
an optimized norm-conserving pseudopotential from the PseudoDojo family [13,14]. The
exact executable, pseudopotential content hash, lattice, cutoffs, reciprocal mesh,
convergence tolerances, retained bands, and runtime environment form the immutable
parent identity.

The converged self-consistent density defines the Kohn–Sham potential. Subsequent
non-self-consistent and band calculations solve

$$
\hat H_{\mathrm{KS}}[n_{\mathrm{SCF}}]\psi_{n\mathbf k}
=
\epsilon_{n\mathbf k}\psi_{n\mathbf k}.
\tag{1}
$$

Density convergence, band-path visualization, valley location, local effective-mass
extraction, and Wannier construction use distinct wavevector designs. Numerical
convergence is judged against downstream quantities rather than total energy alone.
The retained observables include fixed-point band energies, indirect Kohn–Sham gap,
valley coordinate, longitudinal mass, and both unaveraged transverse masses.

### *2.2 Wannier representation and real-space support*

A ten-orbital target subspace contains the valence and low conduction states needed for
the silicon valley analysis. Its Wannier matrix elements are

$$
[\mathbf H_{\mathrm W}(\mathbf R)]_{\alpha\beta}
=
\left\langle w_{\alpha\mathbf0}\middle|
\hat H_{\mathrm{KS}}
\middle|w_{\beta\mathbf R}\right\rangle.
\tag{2}
$$

Initial projections, separately declared frozen and outer windows, reciprocal mesh,
centers, spreads, and real-space inventory are part of the representation identity.
Direct-parent and interpolated Wannier eigenvalues are compared on wavevectors excluded
from construction. Unresolved subspace identity, gauge, decay, or projection/window
sensitivity stops the operator analysis.

The comparison domain $\mathcal S_H$ is drawn from the complete retained translation
inventory $\mathcal S_{\mathrm{all}}$. The excluded squared operator-norm fraction is

$$
\varepsilon_{\mathrm{tail}}^2(\mathcal S_H)
=
\frac{
\displaystyle\sum_{\mathbf R\in
\mathcal S_{\mathrm{all}}\setminus\mathcal S_H}
\omega_{\mathbf R}\|\mathbf H_{\mathrm W}(\mathbf R)\|_{\mathrm F}^2
}{
\displaystyle\sum_{\mathbf R\in\mathcal S_{\mathrm{all}}}
\omega_{\mathbf R}\|\mathbf H_{\mathrm W}(\mathbf R)\|_{\mathrm F}^2
}.
\tag{3}
$$

This is not a physical energy fraction and does not prove decay beyond the represented
Wannier mesh. The domain is enlarged until the diagnostic is stable and its square is
below a separately frozen threshold $\tau_{\mathrm{tail}}$.

### *2.3 Orbital alignment contract*

A unitary map $\mathbf C$ transforms tight-binding coordinates into Wannier coordinates.
The admissible family $\mathcal U$ is not unrestricted $U(10)$. It binds site identity,
orbital semantics, centers, and authenticated representations of retained symmetry
operations. Every map must satisfy

$$
\mathbf C\mathbf D_{\mathrm{TB}}(g)
=
\mathbf D_{\mathrm W}(g)\mathbf C,
\qquad g\in G_{\mathrm{bind}}.
\tag{4}
$$

The symbol $\mathbf D(g)$ includes the declared action of fractional translations,
sublattice permutations, cell relabeling, and wavevector phases where applicable.
Equation (4) is only a constraint. Calling it a realization of $Fd\bar{3}m$ additionally
requires the two space-group representations, origins, translations, and induced maps
to be independently constructed and authenticated.

The frozen family may contain declared site/orbital permutations, phases in one-
dimensional blocks, and block-unitary transformations inside explicit equivalent
multiplicity spaces. It prohibits mixing incompatible sites, irreducible
representations, or orbital-semantic classes unless that freedom is justified and
predeclared. Principal angles, intertwining residuals, singular values, alignment
nonuniqueness, and initialization stability are retained separately from operator
approximation error.

### *2.4 Losses and admissible sets*

Each candidate class $\mathfrak M_j$ fixes its canonical parameter vector
$\boldsymbol\theta$, orbital semantics, neighbor shells, and symmetry constraints. The
planned hierarchy begins with a nearest-neighbor orthogonal ten-orbital
$sp^3s^\ast$ class and adds longer-range or selected symmetry-allowed terms in a frozen
sequence.

The dimensionless spectral loss is

$$
\mathcal L_E(\boldsymbol\theta)
=
\sum_{n,\mathbf k}w_{n\mathbf k}
\left|
\frac{\epsilon_{n\mathbf k}^{\mathrm{TB}}(\boldsymbol\theta)
-\epsilon_{n\mathbf k}^{\mathrm W}}{s_{n\mathbf k}}
\right|^2
+
\sum_m w_m
\left|
\frac{O_m^{\mathrm{TB}}(\boldsymbol\theta)-O_m^{\mathrm W}}{s_m}
\right|^2.
\tag{5}
$$

Training and withheld points, band identities, observable components, weights, and
nonzero scales are frozen before fitting. Longitudinal and two transverse masses remain
separate components.

The normalized operator loss is

$$
\mathcal L_H(\mathbf C,\boldsymbol\theta)
=
\frac{
\displaystyle\sum_{\mathbf R\in\mathcal S_H}\omega_{\mathbf R}
\left\|\mathbf H_{\mathrm W}(\mathbf R)
-\mathbf C\mathbf H_{\mathrm{TB}}(\mathbf R;\boldsymbol\theta)
\mathbf C^\dagger\right\|_{\mathrm F}^{2}
}{
\displaystyle\sum_{\mathbf R\in\mathcal S_H}\omega_{\mathbf R}
\left\|\mathbf H_{\mathrm W}(\mathbf R)\right\|_{\mathrm F}^{2}
}.
\tag{6}
$$

The tight-binding matrix is zero on comparison-domain translations outside its model
support. Long-range parent terms therefore remain visible rather than being silently
aliased into shorter-range parameters. Residuals are also reported by onsite/hopping
role, orbital block, symmetry channel, and neighbor shell.

The admissible sets are

$$
\mathfrak A_{E,j}
=
\{\mathbf H(\boldsymbol\theta)\in\mathfrak M_j:
\mathcal L_E(\boldsymbol\theta)\leq\tau_E\},
\tag{7}
$$

and

$$
\mathfrak A_{H,j}
=
\{\mathbf H(\boldsymbol\theta)\in\mathfrak M_j:
\min_{\mathbf C\in\mathcal U}\mathcal L_H(\mathbf C,\boldsymbol\theta)
\leq\tau_H\}.
\tag{8}
$$

Threshold-derivation rules are declared before production evidence is inspected. Their
final values may reflect demonstrated numerical and extraction floors, but are frozen
before compatibility fitting and are not retuned after model outcomes are known.

### *2.5 Separation, validation, and model selection*

Canonical parameter scales $s_q$ and weights $v_q$ define

$$
d_{\mathrm{TB}}(\boldsymbol\theta_1,\boldsymbol\theta_2)
=
\left[
\sum_qv_q
\left(\frac{\theta_{1,q}-\theta_{2,q}}{s_q}\right)^2
\right]^{1/2}.
\tag{9}
$$

The minimum separation and numerical bounds are

$$
\delta_j^\ast
=
\inf_{\substack{
\mathbf H(\boldsymbol\theta_E)\in\mathfrak A_{E,j}\\
\mathbf H(\boldsymbol\theta_H)\in\mathfrak A_{H,j}}}
 d_{\mathrm{TB}}(\boldsymbol\theta_E,\boldsymbol\theta_H),
\tag{10}
$$

and

$$
0\leq\underline\delta_j\leq\delta_j^\ast\leq\overline\delta_j.
\tag{11}
$$

A common feasible witness supports compatibility. A feasible pair provides an upper
bound; multistart optimization alone does not certify the lower bound. A certified
lower bound above the map resolution supports incompatibility only within the frozen
class and domain. Otherwise the result is inconclusive.

Withheld evidence includes excluded band energies, the indirect gap, valley coordinate,
longitudinal mass, both transverse masses, and declared operator blocks or translations.
Mass observations require identity-tracked nondegenerate branches and stable primary/
guard stencils before entering a loss. Stencil variation is local-extraction error and
is not hidden by enlarging $\tau_E$.

The decision keeps four channels separate: parent-model discrepancy,
numerical/discretization error, local-extraction error, and model-reduction error. The
first hierarchy member with a verified compatibility witness and passing withheld gates
is selected. Missing, conflicting, or ill-conditioned required evidence produces an
inconclusive disposition.

## III. Results and Discussion

### *3.1 Current production evidence boundary*

No production silicon result is reported in this working draft. The project has not yet
accepted, for this paper, a production lattice and Kohn–Sham parent, a numerically
qualified ten-orbital Wannier operator, authenticated silicon symmetry intertwiners,
complete spectral and operator admissible sets, a compatibility witness, certified
separation bounds, or withheld effective masses. Consequently, this draft contains no
silicon parameter table, accepted mass values, or model-selection conclusion.

This absence is an evidence boundary rather than a numerical result. Successful
software tests, controlled toy-model calculations, tutorial runs, and proposed
thresholds cannot substitute for the production gates.

### *3.2 Permitted future outcomes*

When authenticated evidence becomes available, Table 1 governs its interpretation.

**Table 1. Decision logic for one frozen silicon candidate class.**

| Evidence | Supported interpretation | Unsupported interpretation |
|---|---|---|
| Common feasible witness and passed withheld gates | Compatible within the frozen protocol | Experimental accuracy or universal transferability |
| $\overline\delta_j$ below map resolution | Resolution-limited compatibility | Proof of exact continuous-set intersection |
| Certified $\underline\delta_j$ above map resolution | Incompatible within the frozen class and domain | Failure of tight binding in general |
| Separated samples without a lower-bound certificate | Inconclusive | Proof of disjoint admissible sets |
| Failed parent, Wannier, alignment, or extraction gate | Inconclusive | Permission to relax or omit that gate |

A nearest-neighbor failure would identify a limitation of that model class under the
frozen basis, range, symmetry, domain, and tolerances. It would not establish that all
tight-binding descriptions fail. Conversely, a compatible model would remain relative
to the selected PBE/Wannier parent and would not validate unmeasured response functions.

### *3.3 Results reserved for authenticated evidence*

The eventual results section will report parent convergence, direct/Wannier withheld
bands, real-space tail convergence, alignment diagnostics, admissible-set evidence,
separation bounds, withheld band-edge observables, and residual attribution. Training
and withheld quantities will appear separately. Failed and inconclusive hierarchy
members will be retained rather than omitted.

The empty records in Appendix B define the required fields. They are not estimates or
implied findings.

## IV. Conclusions and Recommendations

The proposed silicon test treats spectral and operator reduction as a common-model
problem. It requires a qualified first-principles parent, validated localized
representation, symmetry-constrained alignment, independently normalized losses,
controlled real-space support, bounded set-separation evidence, and withheld
observables. This structure prevents band agreement, matrix agreement, numerical
convergence, and material validity from being conflated.

No production compatibility conclusion follows from the present draft. The scientific
result must remain withheld until all prerequisite and validation gates have produced
authenticated evidence. If completed, the method will select the smallest tested class
that satisfies both criteria, report a certified class-relative obstruction, or return
an inconclusive result without post-hoc threshold relaxation.

## Appendices

The appendices are maintained as separate planning and evidence files:

- [Appendix A — Planned Protected Calculation Sequence](appendices/A-planned-protected-calculation-sequence.md)
- [Appendix B — Pending Evidence Records](appendices/B-pending-evidence-records.md)
- [Appendix C — Non-Production Bootstrap](appendices/C-non-production-bootstrap.md)

## Nomenclature

| Symbol | Description | Unit |
|---|---|---|
| $\mathfrak A_E,\mathfrak A_H$ | Spectral and operator admissible sets | — |
| $\mathbf C$ | Orbital-coordinate alignment | — |
| $\mathbf D(g)$ | Representation of symmetry operation $g$ | — |
| $d_{\mathrm{TB}}$ | Canonical tight-binding parameter distance | — |
| DFT | Density-functional theory | — |
| $\mathbf H_{\mathrm{KS}}$ | Kohn–Sham Hamiltonian | energy |
| $\mathbf H_{\mathrm W}(\mathbf R)$ | Wannier real-space Hamiltonian | energy |
| $\mathbf H_{\mathrm{TB}}(\mathbf R)$ | Tight-binding real-space Hamiltonian | energy |
| $\mathcal L_E,\mathcal L_H$ | Spectral and operator losses | dimensionless |
| $\mathfrak M_j$ | Candidate tight-binding model class | — |
| NSCF | Non-self-consistent field | — |
| PBE | Perdew–Burke–Ernzerhof approximation | — |
| $\mathcal S_H$ | Operator-comparison translation domain | — |
| SCF | Self-consistent field | — |
| SOC | Spin–orbit coupling | — |
| $\boldsymbol\theta$ | Canonical tight-binding parameters | mixed |
| $\tau_E,\tau_H,\tau_{\mathrm{tail}}$ | Frozen thresholds | dimensionless |
| $\delta_j^\ast$ | Minimum admissible-set separation | — |
| $\underline\delta_j,\overline\delta_j$ | Lower and upper separation bounds | — |
| $\varepsilon_{\mathrm{tail}}$ | Retained-inventory operator-norm tail diagnostic | — |
| $\mathcal U$ | Admissible alignment family | — |

## Acknowledgments

> **Author action before submission.** Add verified funding, computing-resource,
> institutional, and technical acknowledgments.

## References

[1] Hohenberg P, Kohn W. 1964. Inhomogeneous electron gas. Physical Review.
136(3B):B864–B871. doi:10.1103/PhysRev.136.B864.

[2] Kohn W, Sham LJ. 1965. Self-consistent equations including exchange and
correlation effects. Physical Review. 140(4A):A1133–A1138.
doi:10.1103/PhysRev.140.A1133.

[3] Marzari N, Mostofi AA, Yates JR, Souza I, Vanderbilt D. 2012. Maximally
localized Wannier functions: Theory and applications. Reviews of Modern Physics.
84:1419–1475. doi:10.1103/RevModPhys.84.1419.

[4] Souza I, Marzari N, Vanderbilt D. 2001. Maximally localized Wannier functions for
entangled energy bands. Physical Review B. 65:035109.
doi:10.1103/PhysRevB.65.035109.

[5] Pizzi G, Vitale V, Arita R, Blügel S, Freimuth F, Géranton G, Gibertini M,
Gresch D, Johnson C, Koretsune T, et al. 2020. Wannier90 as a community code: New
features and applications. Journal of Physics: Condensed Matter. 32(16):165902.
doi:10.1088/1361-648X/ab51ff.

[6] Yates JR, Wang X, Vanderbilt D, Souza I. 2007. Spectral and Fermi surface
properties from Wannier interpolation. Physical Review B. 75:195121.
doi:10.1103/PhysRevB.75.195121.

[7] Slater JC, Koster GF. 1954. Simplified LCAO method for the periodic potential
problem. Physical Review. 94:1498–1524. doi:10.1103/PhysRev.94.1498.

[8] Vogl P, Hjalmarson HP, Dow JD. 1983. A semi-empirical tight-binding theory of the
electronic structure of semiconductors. Journal of Physics and Chemistry of Solids.
44(5):365–378. doi:10.1016/0022-3697(83)90064-1.

[9] Björck Å, Golub GH. 1973. Numerical methods for computing angles between linear
subspaces. Mathematics of Computation. 27(123):579–594.
doi:10.1090/S0025-5718-1973-0348991-3.

[10] Higham NJ. 1986. Computing the polar decomposition—with applications. SIAM
Journal on Scientific and Statistical Computing. 7(4):1160–1174.
doi:10.1137/0907079.

[11] Giannozzi P, Baroni S, Bonini N, Calandra M, Car R, Cavazzoni C, Ceresoli D,
Chiarotti GL, Cococcioni M, Dabo I, et al. 2009. QUANTUM ESPRESSO: A modular and
open-source software project for quantum simulations of materials. Journal of
Physics: Condensed Matter. 21(39):395502.
doi:10.1088/0953-8984/21/39/395502.

[12] Perdew JP, Burke K, Ernzerhof M. 1996. Generalized gradient approximation made
simple. Physical Review Letters. 77:3865–3868. doi:10.1103/PhysRevLett.77.3865.

[13] Hamann DR. 2013. Optimized norm-conserving Vanderbilt pseudopotentials. Physical
Review B. 88:085117. doi:10.1103/PhysRevB.88.085117.

[14] van Setten MJ, Giantomassi M, Bousquet E, Verstraete MJ, Hamann DR, Gonze X,
Rignanese G-M. 2018. The PseudoDojo: Training and grading a 85 element optimized
norm-conserving pseudopotential table. Computer Physics Communications. 226:39–54.
doi:10.1016/j.cpc.2018.01.012.
