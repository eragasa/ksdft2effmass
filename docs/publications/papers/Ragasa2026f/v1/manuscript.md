# Topological and Symmetry Obstructions to Multiband Operator Alignment

**Eugene Joseph M. Ragasa**<br>
Department of Physics, De La Salle University, Manila, Philippines<br>
<eugene.ragasa@dlsu.edu.ph>

*Unpublished pre-results manuscript*

## Abstract

Equal rank of two periodic retained spaces guarantees pointwise unitary maps but does not
guarantee the global periodic, smooth, or symmetry-compatible identification required to
compare their operators. This paper develops a prospective obstruction protocol for
multiband alignment. Periodic projector fields define vector bundles over the Brillouin
torus; local frames are related by transition functions, and an alignment is a relative
bundle isomorphism subject to any additional time-reversal, crystalline, real, or
orientation-preserving structure required by the scientific question. The protocol
distinguishes rank or gap failure, numerical nonresolution, complex-bundle obstruction,
symmetry-equivariant obstruction, and obstruction created only by a restricted real or
$SO(r)$ frame class. It specifies qualified uses of projector Chern formulas,
gauge-invariant lattice curvature, Wilson-loop flow, time-reversal sewing, symmetry
intertwining, and real-bundle diagnostics. A nonidentity Wilson loop, a finite-grid
winding, or a failed gauge optimizer is not by itself classified as topology. When two
nontrivial bundles are nevertheless isomorphic, their operators may be compared through
compatible patchwise representatives even though neither admits the requested global
frame. When the relative bundles are nonisomorphic, no global operator difference is
defined. A flat-band projector grammar constructs globally framed, relatively
isomorphic, complex-obstructed, and category-restricted synthetic controls with exact
rank and gap. A staged controlled-model suite, independent verification, convergence
gates, and fail-closed dispositions are proposed. No model suite or invariant protocol
has yet been frozen, and no maintained experiment or material classification is reported.

**Keywords:** Bloch bundle; topological obstruction; symmetry obstruction; multiband
alignment; Wilson loop; Chern number; time reversal; patchwise frame

## I. Introduction

A periodic rank-$r$ projector field $P(\mathbf k)$ defines more than a collection of
$r$-dimensional vector spaces. As $\mathbf k$ moves over the Brillouin torus, the fibers
form a vector bundle whose global structure controls whether one can choose a smooth
periodic Bloch frame and, under suitable analytic hypotheses, exponentially localized
Wannier functions [[1](#ref-brouder), [2](#ref-panati)]. Local smooth eigenvectors always
exist across a sufficiently small gapped neighborhood; the obstruction concerns gluing
them into the global frame required by a chosen representation.

This distinction matters for operator alignment. Paper 5 asks for a periodic unitary map
between pristine and defect retained spaces before subtraction [[3](#ref-paper5)]. Equal
fiber rank establishes an abstract unitary at each $\mathbf k$, but those unitaries may
fail to glue globally or may fail only after a time-reversal, crystalline, real, or
orientation-preserving constraint is imposed. A numerical seam defect can also arise
from a poor gauge on a trivial bundle. These outcomes require different scientific
dispositions.

Wilson loops, plaquette phases, and sewing matrices are powerful tools, but their
interpretation depends on the symmetry class, base space, rank, gap, discretization, and
required frame category [[4](#ref-fukui), [5](#ref-fukane), [6](#ref-soluyanov),
[7](#ref-yu)]. A nonidentity Wilson loop can occur in a trivial bundle. A zero total
Chern number does not establish a time-reversal-compatible frame. A complex bundle can
be trivial while a required real or crystalline-equivariant framing remains obstructed.
Conversely, a failed localization or phase-smoothing algorithm does not prove any of
these obstructions.

The purpose of this paper is to define a hierarchy and a fail-closed protocol for those
cases. It owns the escalation path from the topologically trivial controls in Paper 3
[[8](#ref-paper3)] and the minimal compatibility screen in Paper 5. It does not classify
silicon or its dopants and does not replace the material-specific contract of Paper 7
[[9](#ref-paper7)]. All numerical model choices and tolerances remain prospective.

<div style="color:#b90000">

## II. Bundle and alignment problem

### II.A. Projector bundles and local frames

Let $\mathbb T^D$ be an oriented Brillouin torus and let

$$
P_s(\mathbf k)^2=P_s(\mathbf k)=P_s(\mathbf k)^\dagger,
\qquad s\in\{0,1\},
$$

be periodic rank-$r_s$ projector fields separated from excluded states under a declared
gap or disentanglement contract. Their ranges form complex vector bundles
$\mathcal E_s\rightarrow\mathbb T^D$.

Choose an open cover $\{\Omega_\alpha\}$ and local orthonormal frames

$$
F_{s,\alpha}(\mathbf k):\mathbb C^{r_s}\rightarrow
\operatorname{Range}P_s(\mathbf k).
$$

On overlaps,

$$
F_{s,\beta}=F_{s,\alpha}g^s_{\alpha\beta},
\qquad g^s_{\alpha\beta}:\Omega_\alpha\cap\Omega_\beta\rightarrow U(r_s),
$$

with cocycle consistency on triple overlaps. A global complex periodic frame exists
precisely when the bundle is trivial in the declared category. Additional regularity is
needed before topological triviality becomes a localization statement; a numerically
smooth finite mesh is not by itself an analytic frame certificate.

### II.B. Relative alignment

For equal rank $r_0=r_1=r$, an unconstrained global alignment is a bundle isomorphism

$$
U(\mathbf k):\mathcal E_{0,\mathbf k}\rightarrow\mathcal E_{1,\mathbf k}.
$$

In local frames write

$$
U F_{0,\alpha}=F_{1,\alpha}W_\alpha,
\qquad W_\alpha:\Omega_\alpha\rightarrow U(r).
$$

The local matrices glue exactly when

$$
W_\beta=(g^1_{\alpha\beta})^\dagger
W_\alpha g^0_{\alpha\beta}
$$

on every overlap. Thus the relevant question is relative: two individually nontrivial
bundles may admit a global isomorphism. Requiring a separate global frame for each would
be unnecessarily strong. Conversely, different bundle classes cannot be made globally
comparable by pointwise polar alignment.

Characteristic data supply necessary compatibility tests, and in carefully stated low-
dimensional categories may be complete. This manuscript does not assume completeness
outside a selected theorem domain. Matching sampled Chern or Wilson diagnostics alone is
not accepted as a general proof of bundle isomorphism.

### II.C. Patchwise operator comparison

Let $H_{s,\alpha}=F_{s,\alpha}^\dagger H_sF_{s,\alpha}$. When the $W_\alpha$ satisfy the
gluing condition, define

$$
\Delta H_\alpha
=H_{1,\alpha}-W_\alpha H_{0,\alpha}W_\alpha^\dagger.
$$

The matrices $\Delta H_\alpha$ transform on overlaps by conjugation with
$g^1_{\alpha\beta}$ and therefore represent one global endomorphism of $\mathcal E_1$.
Its spectrum, traces, and unitarily invariant fiber norms are global even when no single
frame is admitted. A conventional global Wannier matrix and one globally labeled hopping
table are not available in that obstructed frame category.

If the two bundles are not isomorphic, arbitrary local differences do not glue into one
operator. They may diagnose where compatibility fails, but they are not pieces of a
global impurity operator. This boundary prevents “patchwise comparison” from becoming a
way to conceal a relative obstruction.

### II.D. Required category

An obstruction is meaningful only relative to a requested structure:

1. **complex periodic:** frames and maps take values in $U(r)$;
2. **time-reversal compatible:** an antiunitary $\Theta$ and its square are fixed, and
   frames obey the declared Kramers sewing rule;
3. **crystalline equivariant:** maps intertwine selected unitary or antiunitary space-
   group representations;
4. **real:** a real structure is fixed and transition functions are restricted to
   $O(r)$; or
5. **oriented real:** transitions and alignments are restricted to $SO(r)$.

Failure in a narrower category does not imply failure in a broader one. If the scientific
comparison only requires a complex unitary, a real-frame obstruction is inapplicable. If
time reversal or a crystalline representation is physically mandatory, discarding it to
obtain a complex frame changes the problem and requires an explicit human decision.

### II.E. Controlled constructions with guaranteed properties

Obstruction tests require positive and negative controls whose bundle properties do not
depend on the tested numerical classifier. A common parent grammar starts from any
periodic rank-$r$ projector $P(\mathbf k)$ with $Q=I-P$ and defines the flat-band
Hamiltonian

$$
H_P(\mathbf k)=E_-P(\mathbf k)+E_+Q(\mathbf k),
\qquad E_+-E_-=\Delta>0.
$$

Hermiticity, rank, periodicity, the retained projector, and the isolation gap $\Delta$
are then exact construction guarantees. The topology is carried by $P$, not created by
diagonalizing sampled values of $H_P$.

Four related routes construct the required comparison classes.

1. **Globally framed control.** Choose a periodic orthonormal frame $F$ and set
   $P=FF^\dagger$. This guarantees a complex-trivial bundle and a supplied global frame.
   Paper 3's periodic-unitary grammar is a higher-rank source of such controls.
2. **Relatively isomorphic control.** Start from any $P_0$, including an analytically
   certified nontrivial one, choose a periodic ambient unitary $V$, and set

   $$
   P_1=VP_0V^\dagger,
   \qquad U=VP_0.
   $$

   Exactly $U^\dagger U=P_0$, $UU^\dagger=P_1$, and $P_1U=UP_0=U$. Hence $U$ is a
   supplied relative isomorphism even when neither bundle has a global frame. If local
   frames are used, their matrices $W_\alpha$ obey the gluing equation by construction,
   and patchwise operator differences form one global endomorphism.
3. **Complex-obstructed control.** Choose $P_0$ and $P_1$ with analytically certified
   unequal characteristic data in a domain where that mismatch is a valid no-go result.
   Over a two-dimensional Brillouin torus, $C[P_0]\ne C[P_1]$ is sufficient to forbid a
   global complex relative isomorphism. For rank-one two-level controls, a smooth
   periodic nonvanishing field $\mathbf d_s$ supplies

   $$
   P_s=\frac{I-\widehat{\mathbf d}_s\cdot\boldsymbol\sigma}{2},
   \qquad
   \widehat{\mathbf d}_s=\frac{\mathbf d_s}{|\mathbf d_s|},
   $$

   and its Chern class is fixed by the degree of $\widehat{\mathbf d}_s$ under the frozen
   orientation and sign convention. Equal certified degree can seed a relative control;
   unequal degree seeds an obstruction control.
4. **Category-restricted control.** Supply a complex isomorphism as in route 2, but
   choose exact symmetry sewing or real transition data with a separately proved
   incompatibility in the narrower category. Inequivalent representation content at a
   symmetry-invariant momentum, a certified time-reversal invariant mismatch, or a
   qualified real characteristic-class mismatch can then forbid the corresponding
   equivariant, real, or $SO(r)$ map without forbidding the supplied complex map. The
   applicable theorem and its completeness domain are part of the construction, not
   inferred from optimizer failure.

These routes separate what is guaranteed from what remains measured. Analytic formulas,
transition-function cocycles, or theorem-qualified invariants certify the intended rank,
gap, bundle class, and relative disposition. Numerical execution verifies the serialized
implementation and measures discretization, link conditioning, branch stability,
constructive residuals, and convergence under mesh refinement and gauge attacks. A
sampled integer or a failed frame search cannot replace the independent certificate.

The grammar is not an assertion that arbitrary topology, symmetry representations,
spectra, and locality can be combined independently. They must satisfy projector
regularity, cocycle, symmetry, and representation-compatibility conditions in one finite
state space. Global periodic frames realize only trivial bundles, while nontrivial cases
require projectors or patchwise frames with certified transition data. Nor does an exact
synthetic class imply material realism. Paper 5 uses the trivial or relatively admitted
side of this grammar to authorize subtraction; Paper 6 owns the controlled obstruction
and patchwise cases. No Paper 3 or Paper 5 mesh, threshold, result, or evidence status is
transferred by this lineage, and no particular C0--S1 model is selected here.

## III. Obstruction hierarchy and diagnostics

### III.A. Rank and isolation precede topology

Topology is assigned only after constant rank and the defining isolation or
entanglement-stability condition pass on the full parameter domain. A rank change or gap
closing is reported directly. In a parameter sweep it may locate a candidate phase
boundary, but no invariant is assigned at the singular point unless a separate nodal
classification is in scope.

Numerical inability to resolve a small gap, a rank-deficient neighbor overlap, or a mesh-
dependent projector is **NUMERICALLY_UNRESOLVED**, not topological evidence.

### III.B. Complex Chern obstruction

For a sufficiently regular two-dimensional projector and frozen orientation, define

$$
C[P]=\frac{1}{2\pi i}\int_{\mathbb T^2}
\operatorname{Tr}\!\left(P[\partial_{k_x}P,\partial_{k_y}P]\right)
\,d^2\mathbf k.
$$

A nonzero first Chern number obstructs a global smooth periodic complex frame and the
corresponding orthonormal exponentially localized Wannier representation under the
standard hypotheses [[1](#ref-brouder), [2](#ref-panati)]. For relative alignment,
$C[P_0]\ne C[P_1]$ proves that the two complex bundles are not isomorphic. Equality is a
compatibility condition, not a universal certificate in arbitrary dimension or symmetry
class.

On a mesh, the proposed primary calculation uses gauge-invariant link determinants or
projector Bargmann loops. For frame overlaps $M_\mu(\mathbf k)=F^\dagger(\mathbf k)
F(\mathbf k+\hat\mu)$, define the determinant link only when its magnitude passes a
frozen conditioning gate,

$$
\mathcal U_\mu(\mathbf k)=
\frac{\det M_\mu(\mathbf k)}{|\det M_\mu(\mathbf k)|}.
$$

Oriented plaquette phases yield a lattice Chern sum [[4](#ref-fukui)]. An integer-looking
finite sum is admitted as evidence only with a gap record, orientation and branch
convention, independent projector-route reconstruction, gauge attacks, mesh refinement,
and agreement with an analytic or separately certified control where available.

For three-dimensional families, Chern calculations on two-dimensional slices are
reported slice by slice. A slice invariant may change only where the assumptions fail;
it is not automatically a complete three-dimensional classification.

### III.C. Wilson loops

A non-Abelian Wilson matrix is constructed from unitary polar factors of conditioned
neighbor-overlap matrices along a closed loop. Its eigenphases are invariant as a set
under periodic gauge transformations. The protocol retains the loop path, base point,
orientation, sewing closure, eigenphase matching rule, degeneracy handling, and
refinement.

A nonidentity Wilson matrix or nonzero Berry phase does not establish an obstruction.
Even a trivial bundle can have nontrivial connection holonomy. Topological use requires
a qualified spectral-flow or winding statement tied to the applicable invariant and
symmetry [[10](#ref-alexandradinata)]. Ordinary closure failures are first tested as
numerical or gauge-sewing defects.

### III.D. Time-reversal-compatible obstruction

For fermionic time reversal, $\Theta^2=-1$ and the retained rank is even. A local frame
defines the sewing matrix

$$
w_{mn}(\mathbf k)=
\langle u_m(-\mathbf k)|\Theta u_n(\mathbf k)\rangle.
$$

The protocol verifies the antiunitary representation, Kramers degeneracy at
 time-reversal-invariant momenta, reciprocal sewing, and the required covariance of
$P(\mathbf k)$. A vanishing total Chern number does not establish a global
Kramers-compatible frame. The $\mathbb Z_2$ channel must use a reviewed gauge-invariant
formulation, such as time-reversal polarization, Pfaffian/sewing data, or qualified
Wilson-loop partner switching, with cross-method agreement where their assumptions
overlap [[5](#ref-fukane)--[7](#ref-yu)].

A time-reversal obstruction can coexist with an unconstrained complex frame. The correct
disposition is therefore **GLOBAL_COMPLEX_BUT_TR_OBSTRUCTED**, not “no global frame”
without qualification.

### III.E. Crystalline and fragile obstruction

If a space-group or point-group action is required, the bundle and alignment must be
equivariant. At invariant momenta and lines, the retained representation content and
compatibility relations provide necessary tests. A proposed relative map must intertwine
the two sewing representations. Topological quantum chemistry and related band-
representation methods make these distinctions systematic [[11](#ref-bradlyn)].

Stable, fragile, and obstructed-atomic-limit statements must remain separate. A fragile
Wannier obstruction can disappear after adding selected trivial bands
[[12](#ref-po)]. Such an enlargement changes the retained space and cannot be performed
silently to pass an alignment gate. Representation matching at finitely many special
momenta is not assumed to be sufficient unless a theorem for the declared symmetry and
band class is part of the protocol.

### III.F. Real and orientation-preserving restrictions

An antiunitary symmetry squaring to $+1$, or another reviewed real structure, can reduce
the admissible gauge group from $U(r)$ to $O(r)$. Requiring oriented real frames further
restricts it to $SO(r)$. Orientation and higher real-bundle obstructions may then be
probed through Stiefel–Whitney data, transition-function determinants, and qualified
Wilson diagnostics [[13](#ref-ahn)].

These channels are evaluated only when the real structure and gauge restriction are
part of the scientific contract. The protocol records whether $w_1$, $w_2$, or another
quantity is complete for the declared dimension and rank. A complex-trivial bundle must
not be called topologically obstructed without naming the narrower real or symmetry
category.

### III.G. Obstruction ladder

| Level | Question | Failure disposition |
|---|---|---|
| 0 | Are rank and defining gaps/stability conditions valid? | **RANK_OR_GAP_FAILURE** |
| 1 | Are projectors, overlaps, seams, and invariants numerically resolved? | **NUMERICALLY_UNRESOLVED** |
| 2 | Are the complex bundles relatively isomorphic in the declared domain? | **COMPLEX_RELATIVE_OBSTRUCTION** |
| 3 | Does a required time-reversal or crystalline-equivariant isomorphism exist? | **SYMMETRY_RELATIVE_OBSTRUCTION** |
| 4 | Does a required real or $SO(r)$ isomorphism exist? | **RESTRICTED_FRAME_OBSTRUCTION** |
| 5 | Can the admitted map be constructed with the required regularity? | **CONSTRUCTION_UNRESOLVED** |

The ladder is ordered by logical dependency, not by severity. A lower-level failure stops
higher-level claims whose premises it removes.

## IV. Prospective controlled-model protocol

### IV.A. Model roles

The initial study should select the smallest exact models needed to distinguish the
following roles:

- **C0:** a gapped complex-trivial family with a supplied global periodic frame;
- **C1:** a rank-one Chern family with topological and trivial parameter controls;
- **C2:** two copies or deformations with the same nonzero Chern class, testing a global
  relative isomorphism despite absent individual global frames;
- **C3:** equal-rank families with different Chern class, testing a certified relative
  obstruction;
- **T0/T1:** time-reversal-trivial and nontrivial even-rank controls with zero total
  Chern number;
- **R0/R1:** complex-trivial controls that are respectively trivial and obstructed under
  a declared real or orientation-preserving restriction; and
- **S0/S1:** crystalline-equivariant compatible and incompatible controls with explicit
  representation data.

No model family is selected by this manuscript. Standard two-dimensional Chern models,
including Qi–Wu–Zhang and Haldane families [[14](#ref-qwz), [15](#ref-haldane)], are
candidates only after their state spaces, parameter conventions, energy units, analytic
phase boundaries, and publication roles are reviewed. A first immutable version may
legitimately cover only C0–C3; later symmetry classes would receive separate versioned
protocols rather than loosely extending the same result.

### IV.B. Required analytic contracts

Each model case must state:

1. base torus, orientation, reciprocal coordinates, and boundary identifications;
2. finite Bloch state space, matrix ordering, units, and exact Hamiltonian;
3. target projector rank and analytic or independently certified gap domain;
4. required frame category and symmetry representations;
5. known invariant or transition functions and sign convention;
6. the expected relative-alignment disposition;
7. singular parameter values excluded from invariant claims; and
8. the exact distinction between theorem, analytic certificate, and sampled diagnostic.

Models with different state spaces or energy scales are not treated as approximations of
one another and their errors are not pooled.

### IV.C. Numerical and verification design

A frozen mesh ladder must refine independently in each reciprocal direction and avoid
placing unqualified conclusions exactly at analytic singularities. The primary route
computes spectra, projectors, conditioned links, plaquette invariants, Wilson data,
transition functions, and constructive alignment residuals. A deterministic periodic
$U(r)$ phase or frame attack is applied to every case.

An independent verifier reconstructs each Bloch operator from the serialized model
contract and uses projector traces or Bargmann invariants rather than importing primary
eigenvectors or link routines. It checks:

- Hermiticity, rank, gaps, and reciprocal periodicity;
- projector equality at represented seams;
- integer and branch stability under mesh refinement;
- invariance under deterministic frame attacks;
- analytic expectations away from phase boundaries;
- transition-function cocycles and relative gluing residuals;
- constructive global frames or alignments where they are expected; and
- explicit failure certificates where topology forbids them.

A failed optimizer is never the obstruction certificate. The positive evidence is the
qualified invariant or incompatibility of transition data; the constructive failure is a
secondary consistency check.

### IV.D. Acceptance and dispositions

A case is admitted only if all prespecified component gates pass. The final technical
outcomes are:

| Outcome | Meaning |
|---|---|
| **GLOBAL_COMPLEX_ALIGNMENT_ADMITTED** | A periodic complex relative map is constructively qualified. |
| **GLOBAL_SYMMETRY_ALIGNMENT_ADMITTED** | The map also satisfies every declared symmetry constraint. |
| **PATCHWISE_GLOBAL_OPERATOR_ADMITTED** | Relative bundles are isomorphic and local matrices glue, but the requested individual global frame is obstructed. |
| **COMPLEX_RELATIVE_OBSTRUCTION** | Qualified complex-bundle data forbid a global relative map. |
| **SYMMETRY_RELATIVE_OBSTRUCTION** | A complex map exists but no map in the required symmetry category is certified. |
| **RESTRICTED_FRAME_OBSTRUCTION** | Failure occurs only in the declared real or $SO(r)$ category. |
| **RANK_OR_GAP_FAILURE** | The invariant or alignment premises fail. |
| **NUMERICALLY_UNRESOLVED** | Refinement, conditioning, or independent verification does not support classification. |
| **OUT_OF_SCOPE** | The requested invariant is not defined by the frozen protocol. |

Operator authorization is downstream. For example, **PATCHWISE_GLOBAL_OPERATOR_ADMITTED**
permits invariant and patchwise operator comparison but does not create a conventional
global Wannier hopping representation.

</div>

## V. Current evidence boundary

No maintained experiment under `experiments/` supplies Paper 6 obstruction evidence. No
model suite, immutable protocol, schema, verifier identity, frozen mesh ladder,
convergence threshold, or retained run has been selected.

Historical development calculations under
`calculations/research-monograph/periodic-2d/` include separate Qi–Wu–Zhang,
Hofstadter, and Haldane Chern diagnostics and parameter sweeps. They remain calculation-
tree synthetic records. They have not undergone the evidence review, migration, protocol
freeze, and maintained successor packaging required for use as Paper 6 publication
evidence. This manuscript therefore reports none of their numerical values as Paper 6
results.

The Wilson loops and closure phases in Papers 2 and 3 remain transport and sewing
controls in explicitly topologically trivial families. They are not retrospectively
reclassified as continuum topological evidence. Likewise, a future failed Paper 5
alignment enters Paper 6 only after rank, numerical conditioning, semantics, and ordinary
sewing failures have been excluded.

No Chern, $\mathbb Z_2$, crystalline, fragile, Stiefel–Whitney, real-bundle, silicon, or
dopant classification is claimed here.

## VI. Discussion

The relative formulation changes the practical question. Operator comparison does not
always require trivializing each bundle independently. If two nontrivial bundles are
isomorphic, an alignment can exist and a global abstract operator difference can be
represented consistently in patches. What fails is the requested single global frame or
its Wannier representation, not necessarily the comparison itself.

Symmetry adds a second distinction. A complex alignment may exist while a
Kramers-compatible, crystalline-equivariant, real, or orientation-preserving alignment
does not. Reporting only “topological” would hide which scientific requirement caused
the failure. The ordered obstruction ladder and dispositions keep that requirement
visible.

Finite-mesh calculations require particular caution. Lattice Chern formulas can be
exactly integer valued on a fixed mesh, and Wilson phases can show visually convincing
flow, while the target gap, link conditioning, branch convention, or continuum
refinement remains unresolved. Integer output is therefore one channel in a certification
protocol, not an automatic theorem.

The proposed scope also prevents topology from becoming an explanation of last resort.
Rank mismatch, state misassignment, optimizer-basin variation, discontinuous input data,
and incorrect reciprocal sewing all have prior diagnostics. Only after those alternatives
are excluded should the workflow escalate to bundle classification.

## VII. Conclusions

This paper defines a prospective hierarchy for global multiband alignment. It distinguishes
complex bundle isomorphism from individual frame triviality, then separates
symmetry-equivariant and restricted real-frame requirements. Projector invariants,
transition functions, Wilson flows, and constructive maps are assigned qualified roles;
no single diagnostic is allowed to prove every obstruction.

The immediate next step is a reviewed C0–C3 synthetic protocol with exact model
contracts, a frozen refinement ladder, independent projector verification, transition-
function checks, and immutable evidence identities. Time-reversal, crystalline, and real
classes should enter only through separately frozen successors. No material or dopant
calculation is required to establish these controlled mathematical boundaries.

## Appendix A. Pre-execution commitment ledger

| Item | Required commitment | Current state |
|---|---|---|
| Version scope | Exact subset of C, T, R, and S roles | Unselected |
| Model contracts | Hamiltonians, spaces, parameters, units, controls | Unselected |
| Base geometry | Dimension, torus, orientation, seams, loop paths | Method only |
| Projectors | Rank, gap/stability rule, singular-point policy | Unselected |
| Category | Complex, TR, crystalline, real, or $SO(r)$ requirement | Case roles only |
| Invariants | Formula, sign, branch, completeness domain | Method only |
| Numerics | Meshes, conditioning gates, tolerances, convergence | Unselected |
| Construction | Frame/alignment algorithm and gluing tests | Unselected |
| Verification | Independent projector route and attack family | Method only |
| Evidence | Schemas, version, run, verifier, package identities | Absent |
| Resources | Executable, outputs, runtime and memory ceilings | Unreported |

## Appendix B. Required result record

A future retained Paper 6 result must include:

1. immutable model, state-space, symmetry, coordinate, and software identities;
2. exact analytic expectations and excluded singular parameter sets;
3. complete gap, rank, periodicity, and projector-convergence records;
4. overlap conditioning and every omitted or invalid link;
5. lattice-curvature values with orientation, branch, and mesh refinement;
6. Wilson spectra with loop, base point, sewing, matching, and degeneracy rules;
7. time-reversal, crystalline, or real-structure residuals when applicable;
8. local frames, transition functions, cocycle residuals, and patch definitions;
9. relative gluing maps and constructive global-alignment attempts;
10. deterministic gauge-attack and independent-verifier results;
11. separate technical disposition for every case and mesh;
12. the theorem, certificate, diagnostic, and evidence boundary for each claim; and
13. manifests, hashes, commands, environment, schemas, verifier, run, and package identities.

## References

1. <a id="ref-brouder"></a>C. Brouder, G. Panati, M. Calandra, C. Mourougane, and N. Marzari, “Exponential Localization of Wannier Functions in Insulators,” *Physical Review Letters* **98**, 046402 (2007), doi:10.1103/PhysRevLett.98.046402.
2. <a id="ref-panati"></a>G. Panati, “Triviality of Bloch and Bloch–Dirac Bundles,” *Annales Henri Poincaré* **8**, 995–1011 (2007), doi:10.1007/s00023-007-0326-8.
3. <a id="ref-paper5"></a>E. J. M. Ragasa, “Common-Space Construction of Periodic Defect Operators,” unpublished pre-results manuscript (2026).
4. <a id="ref-fukui"></a>T. Fukui, Y. Hatsugai, and H. Suzuki, “Chern Numbers in Discretized Brillouin Zone: Efficient Method of Computing (Spin) Hall Conductances,” *Journal of the Physical Society of Japan* **74**, 1674–1677 (2005), doi:10.1143/JPSJ.74.1674.
5. <a id="ref-fukane"></a>L. Fu and C. L. Kane, “Time Reversal Polarization and a $\mathbb Z_2$ Adiabatic Spin Pump,” *Physical Review B* **74**, 195312 (2006), doi:10.1103/PhysRevB.74.195312.
6. <a id="ref-soluyanov"></a>A. A. Soluyanov and D. Vanderbilt, “Wannier Representation of $\mathbb Z_2$ Topological Insulators,” *Physical Review B* **83**, 035108 (2011), doi:10.1103/PhysRevB.83.035108.
7. <a id="ref-yu"></a>R. Yu, X. L. Qi, A. Bernevig, Z. Fang, and X. Dai, “Equivalent Expression of $\mathbb Z_2$ Topological Invariant for Band Insulators Using the Non-Abelian Berry Connection,” *Physical Review B* **84**, 075119 (2011), doi:10.1103/PhysRevB.84.075119.
8. <a id="ref-paper3"></a>E. J. M. Ragasa, “Multiband Gauge Structure, Aligned Operators, and Hopping Locality,” unpublished manuscript (2026).
9. <a id="ref-paper7"></a>E. J. M. Ragasa, “Spin–Orbit-Coupled Impurity Operators for Substitutional Phosphorus and Boron in Silicon,” unpublished pre-results manuscript (2026).
10. <a id="ref-alexandradinata"></a>A. Alexandradinata, X. Dai, and B. A. Bernevig, “Wilson-Loop Characterization of Inversion-Symmetric Topological Insulators,” *Physical Review B* **89**, 155114 (2014), doi:10.1103/PhysRevB.89.155114.
11. <a id="ref-bradlyn"></a>B. Bradlyn *et al.*, “Topological Quantum Chemistry,” *Nature* **547**, 298–305 (2017), doi:10.1038/nature23268.
12. <a id="ref-po"></a>H. C. Po, H. Watanabe, and A. Vishwanath, “Fragile Topology and Wannier Obstructions,” *Physical Review Letters* **121**, 126402 (2018), doi:10.1103/PhysRevLett.121.126402.
13. <a id="ref-ahn"></a>J. Ahn, S. Park, and B.-J. Yang, “Failure of Nielsen–Ninomiya Theorem and Fragile Topology in Two-Dimensional Systems with Space-Time Inversion Symmetry: Application to Twisted Bilayer Graphene at Magic Angle,” *Physical Review X* **9**, 021013 (2019), doi:10.1103/PhysRevX.9.021013.
14. <a id="ref-qwz"></a>X.-L. Qi, Y.-S. Wu, and S.-C. Zhang, “Topological Quantization of the Spin Hall Effect in Two-Dimensional Paramagnetic Semiconductors,” *Physical Review B* **74**, 085308 (2006), doi:10.1103/PhysRevB.74.085308.
15. <a id="ref-haldane"></a>F. D. M. Haldane, “Model for a Quantum Hall Effect without Landau Levels: Condensed-Matter Realization of the ‘Parity Anomaly’,” *Physical Review Letters* **61**, 2015–2018 (1988), doi:10.1103/PhysRevLett.61.2015.
