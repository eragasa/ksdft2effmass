# Common-Space Construction of Periodic Defect Operators

**Eugene Joseph M. Ragasa**<br>
Department of Physics, De La Salle University, Manila, Philippines<br>
<eugene.ragasa@dlsu.edu.ph>

*Unpublished pre-results manuscript*

## Abstract

A defect-induced operator is not defined by subtracting independently constructed
Hamiltonian matrices merely because their dimensions agree. The pristine and defect
operators may live on different lattices, Bloch bundles, projected subspaces, localized
frames, orbital orderings, and energy references. This paper develops a fail-closed
common-space construction for periodic defect operators. The two calculations are first
placed on a matched comparison lattice and Brillouin torus. Constant rank, projector
compatibility, reciprocal-boundary sewing, and bundle topology are then screened before
an overlap-derived unitary is admitted. Wannier centers, site and orbital semantics, and
surviving symmetries constrain the remaining correspondence. A separately qualified
scalar energy reference completes the alignment, after which the pristine operator can
be transported to the defect space and subtracted. The resulting impurity operator is
gauge covariant rather than entrywise gauge invariant. Rank-changing defect states are
handled by an explicit common-core projection or enlarged retained space, never by zero
padding. The protocol separates geometry, projection, localization, alignment, energy,
numerical, and finite-supercell errors and assigns explicit blocked or unresolved
dispositions when a common space cannot be certified. Phosphorus and boron in silicon
are stated only as future specialization contracts. No production defect calculation,
retained common-space map, or material impurity operator is reported.

**Keywords:** defect Hamiltonian; common state space; operator alignment; principal
angles; polar decomposition; Wannier representation; impurity operator

## I. Introduction

The difference between two linear operators is meaningful only when their domains and
codomains have been identified. In first-principles defect calculations this elementary
requirement is obscured by matrix output: pristine and doped workflows can produce
arrays of the same shape even though their supercell coordinates, target projectors,
Wannier gauges, orbital meanings, and additive energy zeros differ. Direct subtraction
then mixes a physical perturbation with representation mismatch.

Localized Wannier representations provide a natural finite periodic language for
operator comparison [[1](#ref-marzari), [2](#ref-mostofi), [3](#ref-pizzi)]. They do not,
however, make independently selected retained spaces identical. Equal rank provides an
abstract pointwise unitary map, not a unique physical correspondence. Principal angles
and polar decomposition quantify and align subspaces [[4](#ref-bjorck),
[5](#ref-higham)], but they must be embedded in a contract that also controls lattice
folding, periodic sewing, orbital semantics, surviving symmetry, and energy alignment.

For defect label $d$, the intended object is

$$
\Delta H_d^{(P)}
=
\overline H_d^{(P)}
-U_d\overline H_b^{(P)}U_d^\dagger,
$$

where $H_b^{(P)}$ and $H_d^{(P)}$ are pristine and defect projected operators,
$U_d$ identifies their retained spaces, and the bars denote a shared scalar energy
convention. Every element of this expression is conditional on a declared physical and
numerical construction. The formula is the endpoint of alignment, not its substitute.

This paper formalizes that endpoint and its admission gates. It treats the common-space
problem independently of the scalar-relativistic bulk-silicon reduction of Paper 4
[[6](#ref-paper4)], the general obstruction theory reserved for Paper 6
[[7](#ref-paper6)], and the SOC impurity application reserved for Paper 7
[[8](#ref-paper7)]. The result is a prospective methodology. No numerical threshold,
material specialization, or execution evidence is implied by the definitions below.

<div style="color:#b90000">

## II. Comparison geometry and retained spaces

### II.A. Matched periodic geometry

Let $\mathcal L_c$ be the common comparison lattice and $\mathbb T_c^D$ its Brillouin
torus. For a periodic defect supercell, the default comparison is a pristine calculation
repeated in the same supercell:

$$
H_b(\mathbf k),H_d(\mathbf k):\mathcal H_{\mathrm{amb},\mathbf k}
\longrightarrow\mathcal H_{\mathrm{amb},\mathbf k},
\qquad \mathbf k\in\mathbb T_c^D.
$$

The two branches must share lattice vectors, reciprocal-coordinate convention,
plane-wave or other ambient representation, boundary convention, units, relativistic
and spin convention, and a declared coordinate ordering. Atomic positions may differ
because of defect relaxation, but the mapping between comparison sites and translations
must remain explicit.

A primitive-cell pristine calculation may be folded into the defect supercell only
through a recorded isometry that specifies reciprocal preimages, degeneracy ordering,
normalization, and translation phases. Folded and directly recalculated pristine
operators must not be interchanged silently. Agreement of their selected invariants is a
validation test, not an identity assumed from equal spectra.

### II.B. Projected fibers

For $s\in\{b,d\}$, let

$$
P_s(\mathbf k)^2=P_s(\mathbf k)=P_s(\mathbf k)^\dagger,
\qquad
\mathcal E_{s,\mathbf k}=\operatorname{Range}P_s(\mathbf k),
$$

and define

$$
H_s^{(P)}(\mathbf k)=P_s(\mathbf k)H_s(\mathbf k)P_s(\mathbf k).
$$

The projector construction records target bands, outer and frozen windows,
disentanglement, excluded states, and any defect-localized state policy. A common matrix
size after localization does not retroactively establish compatible projectors.

The primary route requires constant equal rank

$$
\operatorname{rank}P_b(\mathbf k)=\operatorname{rank}P_d(\mathbf k)=M
$$

throughout $\mathbb T_c^D$. The spectral isolation or entangled-subspace stability used
to define each projector is checked separately from cross-system compatibility.

### II.C. Rank-changing defect states

A defect can introduce or remove a localized state from the selected window. Three
scientifically distinct responses are permitted:

1. **revise the retained spaces:** enlarge or otherwise redefine both branches under a
   reviewed physical rule and repeat all projection tests;
2. **identify a common core:** choose rank-$q$ projectors $Q_b\leq P_b$ and $Q_d\leq P_d$
   and construct only the explicitly named common-core perturbation
   $\Delta H_d^{(q)}$, while retaining omitted-space weights and couplings as error
   channels; or
3. **block subtraction:** report incompatible retained content when neither construction
   is physically justified.

Zero padding, duplicate orbitals, or deletion chosen after inspecting the desired answer
do not create a common space. A separate defect-only sector may be retained in a block
operator, but the host-to-defect subtraction is then defined only on the admitted common
block and its couplings to the extra sector remain visible.

## III. Alignment map

### III.A. Cross-overlap and principal angles

Let $F_s(\mathbf k):\mathbb C^M\rightarrow\mathcal H_{\mathrm{amb},\mathbf k}$ be
orthonormal frame matrices for the retained fibers. The cross-overlap is

$$
S_d(\mathbf k)=F_d(\mathbf k)^\dagger F_b(\mathbf k)
=L_d(\mathbf k)\Sigma_d(\mathbf k)R_d(\mathbf k)^\dagger.
$$

Its singular values obey $\sigma_j=\cos\theta_j$ and define the principal angles between
retained subspaces. Full rank is required for the polar candidate

$$
G_d^{\mathrm{pol}}(\mathbf k)=L_d(\mathbf k)R_d(\mathbf k)^\dagger,
$$

which maps pristine frame coordinates to defect frame coordinates and minimizes the
Frobenius-distance Procrustes objective. The associated fiber map is

$$
U_d(\mathbf k)=F_d(\mathbf k)G_d(\mathbf k)F_b(\mathbf k)^\dagger
:\mathcal E_{b,\mathbf k}\rightarrow\mathcal E_{d,\mathbf k}.
$$

A small $\sigma_{\min}$ indicates an ill-conditioned physical identification even when
$G_d^{\mathrm{pol}}$ is exactly unitary. Thresholds for rank, conditioning, principal
angles, and their mesh refinement must be frozen before execution.

Overlap maximization is meaningful only in a common ambient representation. It is not a
physical labeling rule by itself. Degenerate singular values can leave a family of
equally optimal polar correspondences that must be resolved, or explicitly retained as
alignment uncertainty, using independent semantics.

### III.B. Global periodicity and topology screen

A pointwise map is admitted globally only when $U_d(\mathbf k)$ is periodic, sufficiently
regular for the intended representation, and compatible with reciprocal-face sewing.
Equal rank does not guarantee this. The pristine and defect projector families must
define compatible Bloch bundles. Paper 5 applies only a minimal screen:

- verify constant rank and projector continuity;
- compute declared seam and loop residuals on refined meshes;
- attempt an explicit periodic alignment and test its closure; and
- escalate any suspected complex, time-reversal, crystalline, or real-bundle
  obstruction to Paper 6 rather than assigning a topology label here.

A nonidentity Wilson loop is not by itself a failure. Holonomy can be nontrivial in a
bundle that still admits a global frame. Conversely, a small finite-grid seam residual
is not a continuum triviality certificate.

### III.C. Orbital semantics and constrained correspondence

In a localized representation, the common coordinate label is

$$
a=(\mathbf R,\tau,\mu,\eta),$$

where $\mathbf R$ is a comparison-lattice translation, $\tau$ a site, $\mu$ an orbital
semantic, and $\eta$ any internal degree of freedom such as spinor coordinate. A
candidate correspondence must satisfy frozen constraints on:

- translation and supercell image;
- Wannier center and localization region;
- site identity and the substitutional-site rule;
- orbital character or trial-projector ancestry;
- internal-coordinate ordering;
- continuity under a declared pristine-to-defect interpolation, when used; and
- irreducible or corepresentation labels of symmetries that survive in both systems.

The defect generally lowers symmetry. Only the common surviving subgroup may constrain
the map. If $D_s(g,\mathbf k)$ represents a required operation $g$, an equivariant map
obeys the appropriate momentum-dependent intertwining relation, schematically

$$
D_d(g,\mathbf k)U_d(\mathbf k)
=U_d(g\mathbf k)D_b(g,\mathbf k).
$$

For antiunitary operations the conjugation rule must be written explicitly rather than
inherited from this unitary shorthand.

Assignment may be formulated as a constrained matching problem, but an optimizer score
is not a scientific certificate. The admissible set, tie handling, assignment margins,
and sensitivity to windows and localization starts are retained. If two physically
different pairings remain indistinguishable under the declared data, the alignment is
reported as ambiguous.

### III.D. Admission diagnostics

At minimum, a future protocol freezes norms and tolerances for

$$
\varepsilon_{\mathrm{unit}}
=\max_{\mathbf k}\|G_d^\dagger G_d-I\|,
\qquad
\sigma_{\min}=\min_{\mathbf k,j}\sigma_j(\mathbf k),
$$

$$
\varepsilon_{\mathrm{sew}}
=\max_{f}\|U_d(\mathbf k_f^+)-
T_d(f)U_d(\mathbf k_f^-)T_b(f)^\dagger\|,
$$

and the applicable symmetry, center, character, assignment-margin, and mesh-refinement
residuals. $T_s(f)$ denotes the declared reciprocal-face sewing map. These channels are
not combined into one score. Failure of any mandatory channel blocks the corresponding
comparison.

## IV. Energy alignment and impurity construction

### IV.A. Scalar energy reference

Independent Kohn--Sham operators are defined only up to an additive scalar for the
present comparison. Let

$$
\overline H_s^{(P)}(\mathbf k)
=H_s^{(P)}(\mathbf k)-E_{\mathrm{ref},s}I.
$$

The same physical estimator must be used for both branches: for example, an approved
bulk-like electrostatic region, compatible deep state, or other reproducible reference.
The estimator, region, finite-supercell drift, parameter sensitivity, and uncertainty are
retained. A band edge may be used only if the same state identity and finite-size
convention are maintained.

Energy alignment removes one scalar identity component. It does not correct an
incompatible projector, gauge, lattice, orbital assignment, spinor ordering, or local
electrostatic response.

### IV.B. Transport and subtraction

The pristine operator transported to the defect fiber is

$$
H_{b\rightarrow d}^{(P)}(\mathbf k)
=U_d(\mathbf k)\overline H_b^{(P)}(\mathbf k)U_d(\mathbf k)^\dagger.
$$

The aligned defect-induced operator is

$$
\boxed{
\Delta H_d^{(P)}(\mathbf k)
=\overline H_d^{(P)}(\mathbf k)
-H_{b\rightarrow d}^{(P)}(\mathbf k)
}.
$$

In aligned Wannier coordinates this becomes

$$
\Delta H_{W,d}(\mathbf R)
=\frac{1}{|\mathbb T_c^D|}
\int_{\mathbb T_c^D}e^{-i\mathbf k\cdot\mathbf R}
\Delta H_d^{(P)}(\mathbf k)\,d\mathbf k,
$$

with a declared discrete-transform convention in computation. Hermiticity requires
$\Delta H_{W,d}(-\mathbf R)=\Delta H_{W,d}(\mathbf R)^\dagger$.

The direct-looking expression
$\Delta H_{W,d}=\overline H_{W,d}-\overline H_{W,b}$ is permitted only after the
coordinates have been aligned so that the matrix of $U_d$ is the identity. Equal shape
alone is insufficient.

### IV.C. Gauge covariance

Under independent retained-space frame changes $V_b$ and $V_d$,

$$
H_s\mapsto V_s^\dagger H_sV_s,
\qquad
G_d\mapsto V_d^\dagger G_dV_b,
$$

and therefore

$$
\Delta H_d\mapsto V_d^\dagger\Delta H_dV_d.
$$

The spectrum, singular values, traces, and unitarily invariant norms of the defect-space
operator are unchanged. Individual onsite and hopping entries, orbital decompositions,
and apparent spatial support generally are not. Such quantities are reportable only in
the frozen aligned localized gauge.

A controlled covariance attack recomputes the full pipeline after independent admissible
frame rotations and checks

$$
\varepsilon_{\mathrm{cov}}
=\|\Delta H_d'-V_d^\dagger\Delta H_dV_d\|.
$$

Rotating only the final matrix tests algebra, not the alignment implementation.

### IV.D. Independent reconstruction

A second implementation must reconstruct the transported pristine operator and defect
difference without importing the primary alignment routine. It verifies spectra,
Hermiticity, trace identities, selected real-space blocks, covariance, and reciprocal/
real-space reconstruction. Agreement establishes implementation consistency under the
frozen contract, not physical validation of the projector or parent model.

## V. Validation, failure semantics, and specialization

### V.A. Separated error ledger

The protocol retains at least these distinct channels:

1. parent-model error;
2. basis, cutoff, and Brillouin-mesh error;
3. finite-supercell and image-interaction error;
4. primitive-to-supercell folding error, if applicable;
5. projection and disentanglement sensitivity;
6. localization and optimizer-basin sensitivity;
7. common-space alignment and assignment uncertainty;
8. scalar energy-reference uncertainty;
9. reciprocal-to-real-space transform and aliasing error; and
10. later impurity-model reduction error.

They are not quadratically combined without a separately justified statistical model.
A relative error with zero reference norm is replaced by its declared absolute form.

### V.B. Fail-closed dispositions

Every attempted comparison receives one of the following human-readable dispositions:

| Disposition | Meaning |
|---|---|
| **COMMON_SPACE_ADMITTED** | All mandatory geometry, rank, global, semantic, energy, and verification gates pass. |
| **COMMON_CORE_ONLY** | A reviewed lower-rank common block is admitted; omitted states and couplings remain explicit. |
| **RANK_INCOMPATIBLE** | Retained content differs and no approved common-core or enlargement exists. |
| **ALIGNMENT_ILL_CONDITIONED** | Cross-overlap is singular or below its frozen conditioning gate. |
| **GLOBAL_COMPATIBILITY_UNRESOLVED** | Periodic or topological compatibility is not certified. |
| **SEMANTIC_ASSIGNMENT_AMBIGUOUS** | More than one physically distinct correspondence survives. |
| **ENERGY_ALIGNMENT_UNRESOLVED** | No stable common scalar reference passes its gate. |
| **NUMERICALLY_UNRESOLVED** | Refinement or independent reconstruction fails without diagnosing a structural obstruction. |

A blocked disposition does not create a zero impurity operator. Optional human choices,
such as revising the projector family, remain separate from technical review and require
a new versioned contract.

### V.C. Silicon specialization contracts

A later P:Si or B:Si specialization must freeze separate pristine/defect pairs,
pseudopotentials, charge and magnetic states, structural relaxation rules, projectors,
spin conventions, supercells, alignment regions, thresholds, and finite-size sequences.
The two dopants do not inherit one another's orbital assignment or tolerances.

Paper 4's scalar-relativistic non-SOC ten-spatial-orbital bulk model is a predecessor, not
the direct common-space parent for an SOC defect calculation. Paper 7 therefore requires
matched pristine-Si/SOC references. Its proposed SOC P:Si branch is additionally blocked
by the current physical specification, which selects a scalar-relativistic non-SOC
primary P:Si branch; only a reviewed amendment or successor can change that selection.

</div>

## VI. Current evidence boundary

No maintained experiment under `experiments/` implements this common-space defect
construction. No matched pristine/defect calculation, ambient cross-overlap, admitted
alignment map, energy-alignment estimate, common-core construction, extracted impurity
operator, independent verifier, or immutable Paper 5 evidence package exists.

The synthetic gauge and locality calculations associated with Papers 1–3 can motivate
software diagnostics but do not instantiate a pristine/defect comparison. Paper 4 has no
production bulk-silicon parent, and Paper 7 has no production dopant branch. Historical
files under `calculations/` do not transfer their identities, tolerances, or evidence
status into this paper.

Accordingly, this manuscript supports definitions, decision gates, and a prospective
record schema only. It does not establish that P:Si, B:Si, or any other material pair has
compatible retained spaces. It reports no impurity matrix element, range, spectrum,
binding energy, or continuum parameter.

## VII. Discussion

The construction separates three questions that are often conflated. First, do the two
calculations use a compatible periodic geometry? Second, do their retained projector
families admit the required global identification? Third, does a particular alignment
respect the scientific semantics assigned to its coordinates? A positive answer to one
question does not imply the others.

The polar factor is useful precisely because its role is limited. It gives the nearest
unitary to a full-rank cross-overlap, but it cannot decide whether two orbitals represent
the same site or physical channel. Similarly, topology is relevant only to the required
global structure. Two individually nontrivial bundles can still be relatively
isomorphic, while a symmetry-compatible identification can be obstructed even when an
unconstrained complex unitary exists. Paper 6 owns those distinctions.

A common-core construction can preserve useful information in a rank-changing problem,
but it changes the scientific object. Its result is a projected common-core perturbation,
not the full defect operator. The discarded weights and couplings are therefore part of
the result rather than preprocessing debris.

Finally, gauge covariance is not gauge independence of entries. Local impurity language
such as “onsite shift” or “modified hopping” becomes meaningful only after a localized
and semantically aligned gauge has been declared. Operator invariants can test the
construction across admissible gauges; they cannot make an arbitrary decomposition
unique.

## VIII. Conclusions

A periodic defect operator is obtained by transport and subtraction on a certified
common retained space. The required evidence includes matched geometry, compatible
projectors, a regular periodic alignment, physical orbital correspondence, stable scalar
energy alignment, covariance, and independent reconstruction. Rank change, global
obstruction, semantic ambiguity, and numerical nonconvergence each receive distinct
fail-closed dispositions.

The framework is ready to guide a reviewed experiment design, but no immutable Paper 5
protocol or execution exists. Before material work, the project must select a bounded
synthetic common-space benchmark, schemas and verifier identities, exact tolerances, and
then separate P:Si and B:Si specializations consistent with the physical specification.

## Appendix A. Pre-execution commitment ledger

| Item | Required commitment | Current state |
|---|---|---|
| Comparison pair | Exact pristine/defect identities and physical branches | Unselected |
| Geometry | Common lattice, folding route, site and translation maps | Method only |
| Parent numerics | Code, versions, pseudopotentials, cutoffs, meshes, tolerances | Unselected |
| Retained spaces | Ranks, windows, projectors, defect-state policy | Unselected |
| Global structure | Sewing conventions and minimal topology screen | Method only |
| Correspondence | Center, site, orbital, internal, and symmetry constraints | Method only |
| Alignment gates | Norms, singular-value, seam, semantic, and refinement thresholds | Unselected |
| Energy reference | Estimator, region, uncertainty, stability rule | Unselected |
| Verification | Independent route, attacks, reconstruction tolerances | Unselected |
| Evidence | Immutable version, schemas, package and verifier identities | Absent |
| Resources | Executables, inputs, scale, outputs, runtime and memory | Unreported |

## Appendix B. Required result record

A future retained Paper 5 result must contain:

1. immutable parent, code, environment, and pseudopotential identities;
2. pristine and defect geometry plus folding and translation maps;
3. projector ranks, windows, spectral gaps, and defect-state dispositions;
4. all cross-overlap singular values and principal-angle summaries;
5. periodic-sewing, topology-screen, and surviving-symmetry residuals;
6. orbital assignments, constraints, margins, ties, and localization sensitivity;
7. the alignment map and its unitarity, conditioning, and covariance diagnostics;
8. energy-reference estimates, spatial regions, sensitivities, and uncertainties;
9. complete reciprocal- and real-space impurity operators with Hermiticity checks;
10. independent reconstruction and controlled frame-attack results;
11. separated numerical, finite-size, projection, localization, alignment, and transform errors;
12. every admitted, failed, blocked, and unresolved disposition; and
13. manifests, hashes, commands, platform, schema, run, verifier, and evidence-package identities.

## References

1. <a id="ref-marzari"></a>N. Marzari, A. A. Mostofi, J. R. Yates, I. Souza, and D. Vanderbilt, “Maximally Localized Wannier Functions: Theory and Applications,” *Reviews of Modern Physics* **84**, 1419–1475 (2012), doi:10.1103/RevModPhys.84.1419.
2. <a id="ref-mostofi"></a>A. A. Mostofi *et al.*, “wannier90: A Tool for Obtaining Maximally-Localised Wannier Functions,” *Computer Physics Communications* **178**, 685–699 (2008), doi:10.1016/j.cpc.2007.11.016.
3. <a id="ref-pizzi"></a>G. Pizzi *et al.*, “Wannier90 as a Community Code: New Features and Applications,” *Journal of Physics: Condensed Matter* **32**, 165902 (2020), doi:10.1088/1361-648X/ab51ff.
4. <a id="ref-bjorck"></a>Å. Björck and G. H. Golub, “Numerical Methods for Computing Angles Between Linear Subspaces,” *Mathematics of Computation* **27**, 579–594 (1973), doi:10.1090/S0025-5718-1973-0348991-3.
5. <a id="ref-higham"></a>N. J. Higham, “Computing the Polar Decomposition—with Applications,” *SIAM Journal on Scientific and Statistical Computing* **7**, 1160–1174 (1986), doi:10.1137/0907079.
6. <a id="ref-paper4"></a>E. J. M. Ragasa, “Compatibility of Spectral and Operator Reductions of a First-Principles Silicon Hamiltonian,” unpublished manuscript (2026).
7. <a id="ref-paper6"></a>E. J. M. Ragasa, “Topological and Symmetry Obstructions to Multiband Operator Alignment,” unpublished pre-results manuscript (2026).
8. <a id="ref-paper7"></a>E. J. M. Ragasa, “Spin–Orbit-Coupled Impurity Operators for Substitutional Phosphorus and Boron in Silicon,” unpublished pre-results manuscript (2026).
