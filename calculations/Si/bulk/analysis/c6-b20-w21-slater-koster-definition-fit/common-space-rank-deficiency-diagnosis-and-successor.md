# Common-space rank deficiency: interpretation and successor proposal

## Status and scope

This note interprets the retained S110 common-space failure and proposes a
fail-closed successor sequence. A calculation-owned CSD0/CSD1 implementation and exact
unretained development request now exist beside this note, with deterministic
human-readable stdout and
exclusive-write result, transcript, and manifest outputs. This is the producer; the
separately implemented CSD1 verifier remains absent. No retained CSD execution has been
promoted, and CSD2 and CSD3 remain unperformed. This note records no new numerical
result, does not revise the immutable S110 disposition, and authorizes no fit, Quantum
ESPRESSO execution, Wannier90 execution, target-space change, or evidence promotion.

The retained result remains
`blocked-orbital-alignment-rank-deficient-no-fit`. No Slater--Koster parameter vector
or aligned operator residual exists for that attempt.

## What failed

S110 tested the ten-dimensional TB-anchored overlap

\[
B(\mathbf{k})=
[U_{\mathrm{dis}}(\mathbf{k})U(\mathbf{k})]^\dagger
A(\mathbf{k})T^\dagger.
\]

A unitary identification between the proposed two-site
\((s,p_x,p_y,p_z,s^*)\) trial frame and the retained rank-10 Wannier space requires all
ten singular values of \(B(\mathbf{k})\) to be resolved at every construction point.
Under the retained native-format uncertainty bound
\(5.890206739032098\times10^{-7}\), the resolved rank was nine at:

| Fractional reciprocal coordinate | Minimum singular value | Next singular value |
|---|---:|---:|
| \((0,0,0)\) | \(5.362000386100462\times10^{-13}\) | \(4.012285201800842\times10^{-4}\) |
| \((0,1/3,0)\) | \(2.0186562353866025\times10^{-7}\) | \(8.534562675450001\times10^{-4}\) |

At Gamma, the unresolved right-singular direction contains approximately 80.5% combined
\(s^*\) weight and 19.5% combined \(s\) weight, shared nearly equally between the two
sites. The evidence therefore identifies a missing or unresolved atomic-trial direction
inside the retained Wannier subspace under the declared projection contract.

## Why energy degeneracy is not the established cause

The rank gate concerns subspace overlap, not separation of Hamiltonian eigenvalues.
Changing the orthonormal basis inside the retained Wannier space by a unitary
\(V(\mathbf{k})\) changes the overlap to

\[
B(\mathbf{k})\longmapsto V(\mathbf{k})^\dagger B(\mathbf{k}),
\]

which leaves every singular value unchanged. Consequently, nonuniqueness of individual
eigenvectors inside an energetically degenerate band cluster cannot by itself create or
remove the observed rank deficiency when the retained subspace is unchanged.

A symmetry-enforced absence or cancellation of the identified \(s/s^*\) trial
combination remains possible, but it has not been established. The retained calculation
did not decompose the trial and Wannier spaces into little-group irreducible
representations. The additional deficient point at \((0,1/3,0)\) also prevents the
failure from being attributed solely to the nearly degenerate Gamma valence manifold.
The supported statement is therefore:

> The declared ten-orbital trial frame was not fully resolved in the retained Wannier
> subspace; energy degeneracy alone is not a diagnosis of the cause.

## Proposed diagnostic stage

Before choosing a successor reduction, perform a separately retained no-calculator,
projector-level diagnosis using the existing authenticated AMN, `u`, and `u_dis` bytes.
It should:

1. reconstruct \(B(\mathbf{k})\), \(B^\dagger B\), all principal angles, and the
   deficient right-singular directions without selecting individual degenerate
   eigenvectors;
2. track the deficient trial direction on neighboring and symmetry-related construction
   points, retaining phase/gauge-invariant projector diagnostics;
3. decompose the atomic trial representation and retained projector into little-group
   symmetry sectors at Gamma and \((0,1/3,0)\), then test whether the missing direction
   belongs to a symmetry sector absent from the retained space;
4. repeat the linear algebra in higher arithmetic precision using the same retained
   decimal data, distinguishing floating-point effects from information already lost to
   native serialization; and
5. classify the result as a symmetry-representation mismatch, target-space/projection
   mismatch, serialization-limited ambiguity, or unresolved cause.

Higher-precision arithmetic cannot recover information absent from the native files.
In particular, it is not expected to repair the approximately
\(5.36\times10^{-13}\) Gamma singular value; it is only a diagnostic control. No
singular-value floor or pseudoinverse should be promoted to a common-space map.

## Controlled sequence and decision gates

The successor is a branched sequence, not an automatic workflow. Every retained stage
requires its own immutable request, source identities, result, verification status, and
nonclaim statement.

| Stage | Purpose | Required output | Stop or progression gate |
|---|---|---|---|
| `CSD0` | Bind the existing source and failed S110 evidence | Request containing exact S30, S105, S110, AMN, `u`, `u_dis`, geometry, basis-order, unit, and energy-reference identities | Stop if any identity, dimension, basis order, or checksum differs |
| `CSD1` | Reconstruct the projector-level rank diagnosis independently | Principal angles, complete singular-value fields, deficient directions, symmetry-related point inventory, precision sensitivity, and producer checks | Stop if the retained deficient points cannot be reproduced without importing the S110 calculation implementation |
| `CSD2` | Test symmetry-sector compatibility | Little-group or symmetry-covariance report for the atomic trial and retained spaces | If existing artifacts do not determine the required symmetry action, record `INSUFFICIENT_RETAINED_SYMMETRY_DATA`; do not infer irreducible representations |
| `CSD3` | Human-owned scientific disposition | One declared cause class and one selected successor branch | No branch proceeds from an unresolved or ambiguous cause without an explicit bounded decision |
| `GU0` | Freeze a global-unitary rank-10 study | Model class, one global-unitary parameterization, objective, 108/108 roles, initializations, stop rules, validation metrics, and failure disposition | Requires completed hopping-first prerequisites and separate authorization for the retained study |
| `GU1` | Verify software behavior on synthetic controls | Synthetic recovery, non-recovery, non-identifiability, symmetry, and serialization tests | Software passage does not admit the silicon fit |
| `GU2` | Fit the retained source without calculator execution | Candidate \(Q\), parameter vector, fit and held-out residuals, spectra, observables, symmetry checks, and start-to-start diagnostics | Stop on nonunitarity, unstable solutions, non-identifiability, failed validation, or undeclared basis changes |
| `GU3` | Independently reconstruct the candidate result | Independent Hamiltonian assembly and residual/observable verification | Producer checks alone cannot qualify the candidate |
| `GU4` | Record scientific disposition | Accept, reject, or retain as unresolved development evidence | Does not establish DFT or experimental silicon validity |
| `NW0` | Freeze a new-source design when atomic semantics are mandatory | Reviewed target space, projections, windows, rank, mesh, symmetry requirements, and full-rank admission test | Requires a separate scientific decision before any input change |
| `NW1+` | Construct and qualify the new source | Separately authorized QE/Wannier occurrences followed by complete source, hopping, reduction, alignment, and validation evidence | Every external execution remains protected and fail-closed |

`CSD2` must distinguish a failed symmetry diagnosis from a negative symmetry result.
The retained AMN and transformation matrices may establish projector overlaps while
still lacking the parent-space symmetry operators needed for an irreducible-
representation decomposition. Missing information is a blocking observation, not
permission to infer orbital character from energies or labels.

## Analysis approach

### Projector-first diagnosis

The primary objects are the atomic-trial projector, the retained Wannier projector, and
their principal angles. Individual eigenvectors inside degenerate clusters are not
assigned persistent identities. Diagnostics must be invariant under independent unitary
basis changes within both represented subspaces.

The `CSD1` producer is implemented without importing or calling
`run_definition_fit.py` in the
calculation-incubated
[`common_space.diagnostics`](../../common_space/diagnostics/) package. It consumes the
same authenticated source bytes and
mathematical definition, but does not call the retained S110 rank-gate implementation.
An independent verifier should reconstruct at least the two deficient singular values,
the Gamma deficient-direction weights, and unitary-basis invariance through a distinct
linear-algebra route.

### Symmetry diagnosis

At each deficient point, the analysis should identify the little group, define its
action on the two-site \((s,p_x,p_y,p_z,s^*)\) trial space, and determine whether an
authenticated action on the retained parent/Wannier space can be constructed. When both
actions exist, compare symmetry-sector dimensions and the projection of the deficient
direction into each sector. When the retained symmetry action is unavailable, stop with
an explicit missing-data result rather than assigning an irrep from band degeneracy or
visual orbital character.

### Global-unitary rank-10 study

The global-unitary branch must preserve one \(Q\) for every \(\mathbf{k}\). A
pointwise \(Q(\mathbf{k})\) would change the model class and could absorb locality and
parameterization error. The frozen study must state:

- the exact Slater--Koster geometry, orbital order, units, and energy zero;
- the first- and second-neighbor parameter inventories evaluated as separate model
  classes;
- the unitary parameterization and deterministic multistart inventory;
- how the linear parameter solve and nonlinear unitary update are composed;
- the unchanged 108/108 construction-grid fit and held-out roles;
- operator, spectral, symmetry, valley, curvature, and mass diagnostics;
- conditioning, convergence, and identifiability criteria; and
- a default stop disposition rather than automatic regularization or model expansion.

The revealed 408-point direct-parent values remain evaluation overlays and cannot define
\(Q\), fit parameters, objectives, thresholds, model selection, or initialization. The
unobserved 402-point values remain confirmation-only.

### New-source branch

A new Wannier source is a new parent representation. Its design must state which
trial-space direction the existing source failed to retain and how the proposed target
space makes that direction admissible without silently changing the physical branch.
Band count, windows, projections, rank, construction mesh, and localization controls
must be reviewed prospectively. Successful full rank is necessary but not sufficient:
the new source must repeat provider eligibility, source reconstruction, locality,
parent-fidelity evaluation, reduction, and independent verification.

## Required error separation

The successor records must keep the following quantities separate:

1. parent-to-Wannier source error;
2. any target-space change introduced by a rank reduction or new source;
3. spatial-support truncation error;
4. alignment error under the declared global-unitary family;
5. Slater--Koster parameterization error after alignment; and
6. end-to-end error relative to the declared comparison target.

A small end-to-end spectrum residual cannot be used to erase a failed common-space,
symmetry, operator, or identifiability gate.

## Recommended successor

The preferred successor depends on the required scientific meaning.

### Operator comparison without projection-anchored atomic identification

After the hopping-first HF0--HF4 prerequisites are resolved, the preferred
no-calculator rank-10 successor is the protocol's global-unitary operator study. It
would fit one momentum-independent \(Q\in U(10)\) jointly with the declared
Slater--Koster parameters:

\[
\min_{Q,\theta}
\sum_{\mathbf{k}\in K_{\mathrm{fit}}}
\left\|
H_{\mathrm{T}}(\mathbf{k})-
QH_{\mathrm{SK}}(\mathbf{k};\theta)Q^\dagger
\right\|_F^2.
\]

This route bypasses the failed AMN-anchored identification while retaining a defined
rank-10 operator comparison if one global unitary passes prospective fit, held-out,
symmetry, stability, and identifiability gates. It does not prove that the fitted
coordinates coincide with the original projected atomic orbitals.

### Site-resolved atomic \(sp^3s^*\) semantics are essential

If the reduction must preserve the specific two-site atomic-orbital interpretation, the
scientifically clean solution is a new Wannier source whose target space, projections,
windows, and rank are prospectively designed to make the complete trial frame full rank
at every construction point. That is a new parent representation, not a repair of the
retained source. It requires separate scientific review, explicit authorization for any
new Quantum ESPRESSO or Wannier90 occurrence, and repetition of source qualification,
hopping characterization, reduction, alignment, and validation.

## Routes that do not solve the retained problem

- A spectral-only fit can test eigenvalue feasibility but defines no aligned operator
  residual.
- Singular-value flooring or a pseudoinverse makes the answer depend on an arbitrary
  regularization coordinate at the failed state-space boundary.
- A rank-nine projection changes the retained model and introduces a separate
  target-space-reduction error; it is not the original rank-10 \(sp^3s^*\) problem.
- Relabeling the failure as a consequence of degeneracy would overstate the retained
  evidence.

## Recommendation

Retain S110 unchanged. First perform the projector- and symmetry-level no-calculator
diagnosis. For a rank-10 operator study, prefer the prospectively frozen global-unitary
route. If projection-anchored atomic semantics are mandatory, construct and qualify a
new Wannier source instead. Neither continuation is authorized by this note.
