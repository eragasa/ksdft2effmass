# Spin–orbit-coupled impurity operators for substitutional phosphorus and boron in silicon

**Eugene Joseph M. Ragasa**<br>
Department of Physics, De La Salle University, Manila, Philippines<br>
eugene.ragasa@dlsu.edu.ph

## Abstract

A defect-induced Hamiltonian is not obtained by subtracting independently generated
first-principles matrices solely because their dimensions agree. This paper defines a
fail-closed spin–orbit-coupled program for substitutional phosphorus and boron in
silicon. Each neutral doped supercell is paired with a pristine-silicon calculation in
the same supercell, fully relativistic convention, numerical representation, and
spinorial Wannier construction. A unitary or explicitly qualified partial identification
places the pristine and defect projected operators on a common retained space before a
scalar energy reference is aligned and the impurity operator is formed. The protocol
keeps donor and acceptor branches separate, resolves spinor, site, orbital, and surviving-
symmetry semantics, and distinguishes parent-model, numerical, projection, localization,
alignment, finite-supercell, impurity-reduction, and continuum errors. Nested impurity
models range from scalar onsite terms to the full nonlocal spinorial perturbation and are
tested against operator, bound-state, subspace, and observable criteria. The current
physical specification authorizes a fully relativistic SOC branch for final B:Si claims
but selects a scalar-relativistic non-SOC primary P:Si branch. The proposed SOC P:Si
branch is therefore blocked pending a reviewed specification amendment or successor.
No production calculation, retained impurity operator, donor or acceptor result, or
continuum conclusion is reported.

**Keywords:** impurity operator, silicon, phosphorus donor, boron acceptor, spin–orbit
coupling, Wannier representation, common-space alignment

## I. Introduction

Kohn–Sham density-functional theory supplies a periodic one-particle parent operator
whose reduction can be assessed independently of the parent approximation itself
[[1](#ref-hohenberg), [2](#ref-kohnsham)]. Localized Wannier representations make a
selected projected operator accessible as real-space matrix blocks
[[3](#ref-marzari), [4](#ref-pizzi)]. Introducing a substitutional dopant, however,
changes the ionic potential, electron count, local relaxation, symmetry, and potentially
the retained electronic content. A pristine and a doped Wannier matrix therefore cannot
be subtracted until their lattices, state spaces, coordinates, gauges, and energy
references have been reconciled.

This issue is sharper with spin–orbit coupling (SOC). The retained coordinates are
spinors; spin-up and spin-down are not independently conserved labels. Symmetry acts
through double-valued representations, and a neutral odd-electron defect requires an
explicit magnetic-state interpretation. Equal rank guarantees an abstract unitary map
between two finite fibers, but it neither chooses a physical orbital correspondence nor
establishes a smooth periodic map over the Brillouin zone. Principal angles and polar
decomposition diagnose a proposed common space, but they do not replace site, orbital,
spinor, and symmetry semantics [[5](#ref-bjorck), [6](#ref-higham)].

The target object for dopant $d\in\{\mathrm P,\mathrm B\}$ is the aligned projected
impurity operator

$$
\Delta H_d
=
\overline H_d-U_d\overline H_{b,d}U_d^\dagger,
$$

where $H_d$ is the doped-supercell operator, $H_{b,d}$ is its matched pristine-Si
supercell reference, bars denote a common scalar energy convention, and $U_d$ is a
validated map from pristine to doped retained coordinates. This is a constructed
operator conditional on the selected parent, projectors, Wannier gauges, structural
branch, and alignment. It is not an automatically unique defect potential.

Phosphorus and boron serve different low-energy problems. A phosphorus donor is tied to
the multivalley conduction manifold and may require short-range valley-orbit coupling
[[7](#ref-kohn-luttinger), [8](#ref-wellard)]. A boron acceptor is tied to a degenerate
SOC valence manifold, for which a scalar single-band description is not the natural
starting point [[9](#ref-baldereschi)]. Their results must not be averaged into one
nominal “dopant” model.

The paper has three goals. First, it states the matched fully relativistic parent and
spinorial representation contract. Second, it defines common-space impurity extraction
and a nested operator-reduction hierarchy. Third, it fixes the evidence and decision
boundaries required before donor, acceptor, or continuum statements are admitted. The
paper is pre-results: it reports a protocol and explicit blockers, not a material
calculation.

## II. Physical and state-space contract

<div style="color:#b90000">

### 2.1 Branches and specification gate

The proposed study contains three separately qualified branches:

1. pristine silicon with SOC in every comparison supercell;
2. neutral substitutional $\mathrm P_{\mathrm{Si}}^0$ with SOC; and
3. neutral substitutional $\mathrm B_{\mathrm{Si}}^0$ with SOC.

Each doped calculation must have its own matched pristine-Si SOC parent with identical
supercell lattice vectors, reciprocal sampling convention, plane-wave representation,
relativistic convention, spinor ordering, numerical tolerances, and compatible Wannier
interface. A primitive-cell host calculation or the scalar non-SOC Paper 4 operator is a
methodological predecessor, not the matrix subtracted from either defect branch.

The current physical specification freezes a fully relativistic noncollinear SOC branch
for final B:Si acceptor claims. It freezes the primary P:Si branch instead as neutral,
scalar-relativistic, collinear spin-polarized, and non-SOC. Consequently, the SOC P:Si
branch proposed here is **blocked** until an authorized specification amendment or
successor selects it. This manuscript does not make that decision.

The three branches also require exact compatible fully relativistic pseudopotential files
and hashes. The existing bulk numerical specification selects only a scalar-relativistic
Si file for the non-SOC pilot; it supplies convergence and provenance patterns but no
SOC Si, P, or B pseudopotential selection for this study.

### 2.2 Matched supercell parent

Let $\mathcal L_{\mathrm{sc},d}$ be the comparison supercell lattice for dopant $d$ and
$\mathrm{BZ}_{\mathrm{sc},d}$ its Brillouin zone. The parent pair is

$$
H_{b,d}^{\mathrm{KS}}(\mathbf k),
\qquad
H_d^{\mathrm{KS}}(\mathbf k),
\qquad
\mathbf k\in\mathrm{BZ}_{\mathrm{sc},d}.
$$

The pristine member is recalculated in the same supercell rather than inferred by raw
primitive-cell matrix subtraction. Any primitive-to-supercell folding used for analysis
must be explicit and independently checked. Both cells retain the approved PBE parent
approximation and compatible PseudoDojo ONCV family [[10](#ref-pbe),
[11](#ref-hamann), [12](#ref-pseudodojo)]. Exact production values for cutoffs, meshes,
occupations, smearing, relaxation, and supercell sizes remain unselected.

The substitutional site replaces one Si atom. Internal coordinates of the primary defect
branch are relaxed at fixed approved host lattice vectors; unrelaxed structures are
separate diagnostics. Every finite supercell represents a periodic dopant array.
Isolated-impurity interpretation requires explicit supercell-size convergence and cannot
follow from one completed periodic calculation.

### 2.3 Spinorial retained spaces

For $s\in\{b,d\}$, let $P_s(\mathbf k)$ be the selected spinorial projector and

$$
\mathcal H_{s,\mathbf k}^{(P)}=\operatorname{Range}P_s(\mathbf k),
\qquad
H_s^{(P)}(\mathbf k)=P_s(\mathbf k)H_s^{\mathrm{KS}}(\mathbf k)P_s(\mathbf k).
$$

A common orbital index is

$$
a=(\mathbf R,\tau,\mu,\varsigma),
$$

where $\mathbf R$ is a supercell translation, $\tau$ a site, $\mu$ a localized orbital
semantic, and $\varsigma$ a spinor-coordinate label. The label $\varsigma$ records a
basis convention; it is not a conserved spin quantum number under SOC.

The ten-spatial-orbital non-SOC $sp^3s^*$ representation of Paper 4 corresponds to
twenty spinor coordinates before any separately justified rank change. This counting
observation does not select the Paper 7 projector, projections, windows, or final rank.
Defect-localized states that change retained-space content must be admitted explicitly,
matched through a declared projection or embedding, or reported as a rank-compatibility
failure.

For each branch, Wannier construction must retain separately:

- disentanglement and localization maps;
- outer and frozen windows;
- trial spinors and projection semantics;
- centers, spreads, and orbital/site assignments;
- reciprocal-boundary sewing;
- spinor ordering and phase conventions; and
- sensitivity to initial projections and localization settings.

Localization selects a frame after the projected subspace has been selected. It does not
repair an incompatible projector or prove a unique optimizer basin.

### 2.4 Common-space admission

Assume first that the pristine and defect fibers have equal rank $M_d$. In a common
ambient representation, define the cross-overlap

$$
S_d(\mathbf k)=F_d^\dagger(\mathbf k)F_{b,d}(\mathbf k)
=L_d(\mathbf k)\Sigma_d(\mathbf k)R_d^\dagger(\mathbf k).
$$

The singular values $\sigma_{j,d}(\mathbf k)$ give principal angles through
$\sigma_{j,d}=\cos\theta_{j,d}$. When the overlap is full rank, the polar candidate is

$$
U_d^{\mathrm{pol}}(\mathbf k)=L_d(\mathbf k)R_d^\dagger(\mathbf k).
$$

This is an overlap-maximizing coordinate map, not automatically the physically admitted
map. The admissible family must also preserve the frozen correspondence among sites,
Wannier centers, orbital semantics, spinor convention, translations, and surviving
symmetry representations. Where a pristine double-space-group operation survives in the
defect subgroup, the map must satisfy the declared intertwining relation. Broken
symmetries are not imposed on the defect.

Admission requires at least:

$$
\sigma_{\min,d}
=
\min_{\mathbf k,j}\sigma_{j,d}(\mathbf k)
\ge \sigma_{\mathrm{rank},d},
$$

$$
\varepsilon_{\mathrm{unit},d}
=
\max_{\mathbf k}\lVert U_d^\dagger U_d-I\rVert
\le\tau_{\mathrm{unit},d},
$$

and separately frozen periodic-sewing, center-assignment, orbital-character, symmetry-
intertwining, and conditioning gates. Their numerical thresholds remain open. If the
rank differs, the overlap is deficient, a required global periodic map is obstructed, or
orbital semantics conflict, subtraction is blocked. Paper 6 supplies the escalation path
for genuine topological or required-symmetry obstruction; a sewing defect alone is not
relabeled as topology.

### 2.5 Scalar energy alignment

Independent Kohn–Sham calculations have arbitrary additive energy references. Define

$$
\overline H_s=H_s-E_{\mathrm{ref},s}I.
$$

The same physical estimator must be applied to pristine and doped supercells, preferably
using a reproducible bulk-like region or another reviewed far-field reference. The
estimator, spatial sampling region, supercell dependence, and uncertainty are part of the
result. Energy alignment removes only a scalar identity term; it cannot correct a
mismatched projector, gauge, lattice, spinor order, or orbital correspondence.

### 2.6 Extracted SOC impurity operator

After admission, the defect-induced operator is

$$
\boxed{
\Delta H_d^{\mathrm{SOC}}
=
\overline H_d-U_d\overline H_{b,d}U_d^\dagger
}.
$$

In the aligned Wannier representation,

$$
\Delta H_d^{\mathrm{SOC}}(-\mathbf R)
=
\Delta H_d^{\mathrm{SOC}}(\mathbf R)^\dagger.
$$

Under compatible changes of pristine and defect frames, $U_d$ transforms with both
frames and the extracted operator transforms covariantly in the defect space. Unitarily
invariant norms, spectra, and subspace angles are unchanged, while individual onsite and
hopping entries remain gauge dependent.

The extracted operator is the full neutral-supercell perturbation. For
$\mathrm P_{\mathrm{Si}}^0$ it contains both the donor-core difference and the response
of the additional electron. It must not be silently interpreted as the potential of an
ionized $\mathrm P_{\mathrm{Si}}^+$ center. Charged branches require their own background,
finite-size, and electrostatic-correction specifications [[16](#ref-freysoldt)].

</div>

## III. Reduction and validation protocol

<div style="color:#b90000">

### 3.1 Spinorial impurity hierarchy

In the fixed aligned gauge, decompose

$$
\Delta H_d^{\mathrm{SOC}}
=
\Delta H_{\mathrm{sc},d}
+
\Delta H_{\mathrm{orb},d}
+
\Delta H_{\mathrm{mix},d}
+
\Delta H_{\mathrm{hop},d}.
$$

The terms denote scalar onsite, orbital- and spinor-dependent onsite, onsite mixing, and
nonlocal hopping/hybridization changes. The nested model classes are

$$
\mathfrak M_{\mathrm{scalar}}
\subset
\mathfrak M_{\mathrm{orbital}}
\subset
\mathfrak M_{\mathrm{onsite}}
\subset
\mathfrak M_{R_c}
\subset
\mathfrak M_{\mathrm{full}}.
$$

This nesting exists only after gauge, site partition, spinor ordering, metric, and support
conventions are fixed. “Central cell” does not imply scalar or onsite: the required
short-range operator structure is determined from the residual rather than from the
name.

### 3.2 Branch-specific observables

The P branch targets donor binding energies relative to the compatible SOC conduction
edge, valley-channel populations, valley-orbit splittings when resolved, target-subspace
fidelity, localization radii, and shell-resolved impurity norms. The B branch targets
acceptor binding energies relative to the compatible SOC valence edge, the appropriate
multiband valence subspace, resolved level splittings, subspace fidelity, localization,
and shell-resolved norms. Individual states are compared only when nondegenerate and
identity tracked; degenerate or nearly degenerate manifolds are compared through
projectors.

For a model $m$, let

$$
E_{m,d}=\Delta H_{m,d}-\Delta H_{\mathrm{ref},d}.
$$

The required metrics include global and weighted operator errors, target-subspace error,
leakage, binding-energy and splitting errors, and subspace fidelity:

$$
\varepsilon_{\Pi,m,d}
=
\frac{\lVert\Pi_{\mathrm{ref},d}E_{m,d}\Pi_{\mathrm{ref},d}\rVert_2}
{\lVert\Pi_{\mathrm{ref},d}\Delta H_{\mathrm{ref},d}\Pi_{\mathrm{ref},d}\rVert_2},
$$

$$
F_{m,d}
=
\frac{1}{r_d}\operatorname{Tr}
\left(\Pi_{\mathrm{ref},d}\Pi_{m,d}\right).
$$

A relative error with a zero reference denominator is replaced by its declared absolute
form. No scalar aggregate score replaces these channels. A model is accepted only when
every prespecified component of $\boldsymbol\varepsilon_{m,d}$ passes its corresponding
component of $\boldsymbol\tau_d$.

### 3.3 Spatial and finite-supercell controls

For orbitals centered at $\bar{\mathbf r}_{a,d}$, assign onsite distance from the dopant
by $\rho_{a,d}=|\bar{\mathbf r}_{a,d}-\mathbf r_d|$. A nonlocal element may be assigned
by its midpoint distance, but this is a declared bookkeeping convention and must be
varied if conclusions depend on it. Complete symmetry-compatible supports are preferred
to entrywise magnitude pruning.

Every result carries supercell size $L_{\mathrm{sc}}$. Selected operator blocks,
binding energies, splittings, localization measures, energy-alignment estimates, and
exterior tails must be refined with supercell size. Numerical cutoff/mesh convergence,
finite-supercell image error, Wannier/projector sensitivity, and impurity-model reduction
remain separate channels.

### 3.4 Continuum handoff

A later continuum comparison requires an explicit embedding
$J_d:\mathcal H_{\mathrm{cont},d}\rightarrow\mathcal H_{\mathrm W,d}^{(P)}$ before an
atomistic matrix can be subtracted from an effective-mass operator. The P channel is a
multivalley conduction problem; the B channel is a multiband SOC valence problem. Each
has its own continuum state space.

For exterior projector $P_{>r,d}$, a candidate continuum model may define exterior and
cross-region errors and a crossover radius only under frozen norms and tolerances. An
empty admissible radius set gives $r_{c,d}=+\infty$ for that model; it does not authorize
post-hoc removal of a channel. No continuum extraction is part of the present evidence.

### 3.5 Decision table

| Gate or evidence | Passing interpretation | Failure or absence |
|---|---|---|
| Reviewed physical specialization | branch eligible for protocol freeze | execution blocked |
| Matched parent identity | numerical comparison geometry admitted | subtraction undefined |
| Equal rank or justified embedding | retained-space comparison admitted | rank incompatibility |
| Full-rank, well-conditioned overlap | polar candidate available | alignment blocked |
| Periodic and symmetry-semantic map | global common space admitted | unresolved or Paper 6 escalation |
| Stable scalar energy alignment | aligned subtraction admitted | impurity operator unresolved |
| Hermiticity and independent reconstruction | extracted representation verified | calculation failure |
| Supercell and numerical refinement | bounded finite-size/numerical claims admitted | isolated-defect claim blocked |
| All branch-specific error gates | selected reduced model acceptable | advance hierarchy or report no acceptable tested model |

</div>

## IV. Current evidence boundary

No maintained experiment under `experiments/` implements this Paper 7 protocol. No
fully relativistic Si/P/B pseudopotential triplet, production supercell, SOC Kohn–Sham
parent, spinorial Wannier representation, common-space map, aligned impurity operator,
supercell refinement, reduced impurity hierarchy, or continuum embedding has been
selected or executed.

The scalar-relativistic, non-SOC Paper 4 bulk program [[13](#ref-paper4)] cannot serve
as a direct subtraction reference. Synthetic gauge, locality, strain, and higher-rank
studies in Papers 1–3 test software and mathematical mechanisms but are not material
evidence. Paper 5 [[14](#ref-paper5)] currently supplies a prospective common-space
methodology, and Paper 6 [[15](#ref-paper6)] supplies only a prospective obstruction
scope. Neither has a retained execution that Paper 7 can inherit.

The current branch disposition is:

| Branch | Specification status | Execution status | Permitted statement |
|---|---|---|---|
| Matched pristine Si/SOC | required by proposed Paper 7 | absent | required future reference |
| Neutral Si:P/SOC | conflicts with current primary P:Si v1 branch pending amendment | blocked and absent | proposed branch only |
| Neutral Si:B/SOC | physically selected for final B claims, specialization still incomplete | absent | eligible only after specialization and numerical gates |
| Scalar non-SOC Paper 4 Si | separate bulk baseline | pre-results | methodological predecessor only |

These are administrative and scientific readiness states, not numerical findings.
Passing software tests in the future will establish implementation behavior only; it
will not by itself validate the parent physics or authorize material claims.

## V. Discussion

The principal methodological claim is that a spinorial impurity operator is a
common-space construction rather than a raw matrix difference. This protects the defect
signal from contamination by rank changes, unrelated gauges, energy-zero shifts,
spinor-order permutations, incompatible symmetries, and primitive/supercell mismatch.
The same construction also makes failure scientifically legible: a failed rank,
conditioning, sewing, or semantic gate yields no impurity operator instead of a
numerically convenient subtraction.

The donor and acceptor branches share infrastructure but not physical outputs. Their
odd electron counts, magnetic interpretations, band-edge channel spaces, SOC responses,
defect states, pseudopotentials, and continuum reductions remain branch specific. A
common workflow schema may compare their evidence structure; it must not average their
operators or tolerances.

The neutral-supercell convention also limits interpretation. The extracted P operator is
not automatically an ionized screened-Coulomb donor potential, and the B operator is not
a scalar acceptor potential. Screened and central-cell continuum forms are hypotheses to
be tested after atomistic extraction. Parent PBE error, pseudopotential transferability,
periodic-image effects, and model-reduction error must remain visible even if the final
reduced operator passes its internal criteria.

## VI. Conclusions

This pre-results manuscript defines a matched fully relativistic route from pristine and
substitutional-silicon Kohn–Sham parents to aligned spinorial impurity operators. The
route requires compatible supercells and numerical identities, explicit retained spaces,
qualified global alignment, scalar energy-reference alignment, gauge-covariant
subtraction, independent reconstruction, finite-size refinement, and branch-specific
operator and bound-state validation.

No Paper 7 material conclusion follows yet. The next scientific decision is not an
execution parameter: it is whether to amend or supersede the physical specification to
admit the proposed SOC P:Si branch. Only after that decision and the separate B:Si
specialization may exact pseudopotentials, structures, occupations, meshes, Wannier
windows, tolerances, resource estimates, and protected execution requests be reviewed.

## Appendix A. Pre-execution commitment ledger

| Item | Must be frozen before execution | Current state |
|---|---|---|
| Physical branch | charge, relativistic treatment, spin/magnetic interpretation | B/SOC selected in principle; P/SOC blocked |
| Pseudopotentials | exact Si/P/B files, versions, relativistic form, hashes | unselected |
| Geometry | host lattice, supercell sizes, substitution site, relaxation branch | convention only; sizes unselected |
| Numerical parent | cutoffs, meshes, occupations, solver tolerances, executable identity | unselected |
| Projected space | rank, windows, projectors, defect-state policy | unselected |
| Wannier representation | spinor order, centers, sewing, localization controls | unselected |
| Alignment | admissible family, singular-value/rank thresholds, symmetry semantics | method only |
| Energy reference | estimator, region, uncertainty and finite-size rule | requirement only |
| Impurity hierarchy | supports, norms, weights, model order | mathematical hierarchy only |
| Validation | training/withheld roles, tolerances, convergence and failure policy | unselected |
| Resources | executable, scale, output inventory, runtime/memory estimate | unreported |
| Evidence | immutable version, schemas, verifier, run and package identities | absent |

## Appendix B. Required result record

A future retained result must report, separately for P and B:

1. immutable physical, numerical, software, and pseudopotential identities;
2. pristine and defect supercell provenance and convergence tables;
3. projected ranks, windows, projector diagnostics, and defect-state dispositions;
4. Wannier centers, spreads, sewing, spinor order, and optimizer sensitivity;
5. overlap singular values, principal angles, alignment maps, and symmetry residuals;
6. energy-alignment estimate, region sensitivity, and uncertainty;
7. complete $\Delta H_d^{\mathrm{SOC}}(\mathbf R)$ blocks with Hermiticity and independent reconstruction;
8. supercell-size dependence and periodic-image diagnostics;
9. full and reduced impurity spectra, target projectors, fidelities, and observable errors;
10. accepted, rejected, failed, and unresolved model classes without selective omission; and
11. checksums, manifests, commands, platform, verifier identity, and evidence-package identity.

Empty or failed records remain evidence of disposition. They are not replaced by zeros or
omitted from the hierarchy.

## References

1. <a id="ref-hohenberg"></a>P. Hohenberg and W. Kohn, “Inhomogeneous Electron Gas,” *Physical Review* **136**, B864–B871 (1964), doi:10.1103/PhysRev.136.B864.
2. <a id="ref-kohnsham"></a>W. Kohn and L. J. Sham, “Self-Consistent Equations Including Exchange and Correlation Effects,” *Physical Review* **140**, A1133–A1138 (1965), doi:10.1103/PhysRev.140.A1133.
3. <a id="ref-marzari"></a>N. Marzari, A. A. Mostofi, J. R. Yates, I. Souza, and D. Vanderbilt, “Maximally Localized Wannier Functions: Theory and Applications,” *Reviews of Modern Physics* **84**, 1419–1475 (2012), doi:10.1103/RevModPhys.84.1419.
4. <a id="ref-pizzi"></a>G. Pizzi *et al.*, “Wannier90 as a Community Code: New Features and Applications,” *Journal of Physics: Condensed Matter* **32**, 165902 (2020), doi:10.1088/1361-648X/ab51ff.
5. <a id="ref-bjorck"></a>Å. Björck and G. H. Golub, “Numerical Methods for Computing Angles Between Linear Subspaces,” *Mathematics of Computation* **27**, 579–594 (1973), doi:10.1090/S0025-5718-1973-0348991-3.
6. <a id="ref-higham"></a>N. J. Higham, “Computing the Polar Decomposition—with Applications,” *SIAM Journal on Scientific and Statistical Computing* **7**, 1160–1174 (1986), doi:10.1137/0907079.
7. <a id="ref-kohn-luttinger"></a>W. Kohn and J. M. Luttinger, “Theory of Donor States in Silicon,” *Physical Review* **98**, 915–922 (1955), doi:10.1103/PhysRev.98.915.
8. <a id="ref-wellard"></a>C. J. Wellard and L. C. L. Hollenberg, “Donor Electron Wave Functions for Phosphorus in Silicon: Beyond Effective-Mass Theory,” *Physical Review B* **72**, 085202 (2005), doi:10.1103/PhysRevB.72.085202.
9. <a id="ref-baldereschi"></a>A. Baldereschi and N. O. Lipari, “Spherical Model of Shallow Acceptor States in Semiconductors,” *Physical Review B* **8**, 2697–2709 (1973), doi:10.1103/PhysRevB.8.2697.
10. <a id="ref-pbe"></a>J. P. Perdew, K. Burke, and M. Ernzerhof, “Generalized Gradient Approximation Made Simple,” *Physical Review Letters* **77**, 3865–3868 (1996), doi:10.1103/PhysRevLett.77.3865.
11. <a id="ref-hamann"></a>D. R. Hamann, “Optimized Norm-Conserving Vanderbilt Pseudopotentials,” *Physical Review B* **88**, 085117 (2013), doi:10.1103/PhysRevB.88.085117.
12. <a id="ref-pseudodojo"></a>M. J. van Setten *et al.*, “The PseudoDojo: Training and Grading a 85 Element Optimized Norm-Conserving Pseudopotential Table,” *Computer Physics Communications* **226**, 39–54 (2018), doi:10.1016/j.cpc.2018.01.012.
13. <a id="ref-paper4"></a>E. J. M. Ragasa, “Compatibility of Spectral and Operator Reductions of a First-Principles Silicon Hamiltonian,” unpublished manuscript (2026).
14. <a id="ref-paper5"></a>E. J. M. Ragasa, “Common-Space Construction of Periodic Defect Operators,” unpublished pre-results manuscript (2026).
15. <a id="ref-paper6"></a>E. J. M. Ragasa, “Topological and Symmetry Obstructions to Multiband Operator Alignment,” unpublished pre-results manuscript (2026).
16. <a id="ref-freysoldt"></a>C. Freysoldt, J. Neugebauer, and C. G. Van de Walle, “First-Principles Calculations for Point Defects in Solids,” *Reviews of Modern Physics* **86**, 253–305 (2014), doi:10.1103/RevModPhys.86.253.
