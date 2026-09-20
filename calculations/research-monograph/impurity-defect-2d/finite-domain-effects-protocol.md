# Finite-domain geometry and boundary-phase protocol

## Status and authority

This protocol is an execution-free proposed design under
`research-monograph.exercises.impurity.defect-2d.finite-domain-effects`. It does
not authorize implementation, calculation, external-root mutation, or output
creation. The accepted directional/nonlocal package is immutable and is consumed only
as a compact identified predecessor.

The read-only gate audit reports `PASS`: every one of 208 route records retains all
five ordered model fits, including rejected classes and their residuals; the selected
classes agree with the frozen plants; all tolerances agree with the adopted design; and
independent reconstruction passed. This gate result permits design work only.

The intended future result would be controlled synthetic numerical verification. It
would not be material validation, scientific validation, uncertainty quantification,
or publication evidence.

## Spaces and finite geometries

For geometry $N_x\times N_y$, the represented scalar space is
$\mathbb C^{N_xN_y}$ with $x$ outer and $y$ inner. The retained rank is one per
primitive cell. Energies are measured in $E_G$, lengths in lattice cells with
$a=2\pi$, and every parent and defect operator uses the identified common parent
energy zero.

The parent hopping inventory remains truncated at
$R_x^2+R_y^2\leq18$. Its inherited truncation diagnostic is not combined with
finite-area, shape, orientation, boundary-phase, alignment, model-reduction, or
eigensolver error.

The area channel uses only

$$
(6,6),\ (8,8),\ (10,10),\ (12,12),\ (16,16).
$$

The shape channel uses only the area-144 geometries

$$
(8,18),\ (9,16),\ (12,12),\ (16,9),\ (18,8).
$$

The shared $12\times12$ operator evaluations are referenced by both channels and are
not recomputed. Area is an ordered sequence; shape is a fixed-area contrast and is not
a convergence sequence.

## Parents and defects

Area, shape, and boundary-phase records use the isotropic separable parent
$(\lambda_x,\lambda_y,\lambda_{xy})=(0.5,0.5,0)$. Orientation controls use the
anisotropic parent $(0.3,0.7,0)$ and its separately identified axis-swapped parent
$(0.7,0.3,0)$.

The inherited defects are unchanged:

1. directional nearest-neighbor changes $+0.04E_G$ along positive $x$ and
   $-0.03E_G$ along positive $y$, with Hermitian reverse bonds; and
2. the finite-range diagonal change $+0.025E_G$ at displacement $(1,1)$, with its
   Hermitian reverse bond.

Their frozen first accepted model classes remain directional nearest neighbor and
finite-range nonlocal radius two. No class, basis, order, defect strength, or tolerance
may be changed after observing finite-domain behavior.

## Boundary-phase mesh

Every applicable geometry uses the exact mesh

$$
(\phi_x,\phi_y)=\left(\frac{m}{9},\frac{n}{9}\right),
\qquad m,n\in\{0,\ldots,8\},
$$

ordered with $m$ outer and $n$ inner. A hop crossing $q_x$ and $q_y$ boundaries
receives

$$
\exp\!\left[2\pi i(q_x\phi_x+q_y\phi_y)\right].
$$

Individual vectors are never compared across different twist fibers. Degenerate
states within one fiber are compared through projectors using cluster ranks fixed from
the parent spectrum before inspecting the defect result.

## Independent construction boundary

A future producer would construct compact-parent supercells in the centered
uniform-link gauge using the unreduced twist lift. The independent verifier would
construct the same cases in the quotient seam gauge from Kronecker products of
one-dimensional seam matrices. It would apply the explicit site-diagonal gauge bridge
before comparing represented matrices.

The verifier may share only serialized contracts and immutable input identities. It
may not import production construction, eigensolution, observable, reduction, or
serialization algorithms. No route voting or averaging is permitted.

## Separate analysis channels

### Area

The two defects are evaluated on the five square geometries and all 81 twists.
Adjacent finite-area changes are retained in order. Only the final $12\times12$ to
$16\times16$ change is classified against the frozen finite-size reporting
thresholds. Failed or nonmonotone sequences remain evidence.

### Shape

The two defects are evaluated on all five area-144 geometries and all 81 twists.
The channel reports spread and pairwise contrasts relative to $12\times12$. It has no
convergence pass status. Full matrices from different geometries are not directly
subtracted, even when their dimensions happen to agree.

### Orientation

The geometry pairs are $(8,18)\leftrightarrow(18,8)$ and
$(9,16)\leftrightarrow(16,9)$. Integer coordinate and defect displacements are mapped
by $x\leftrightarrow y$, and twists map as
$(\phi_x,\phi_y)\mapsto(\phi_y,\phi_x)$.

Two results remain separate:

- the same-parent orientation contrast, which is a physical contrast with no zero
  expectation; and
- source-to-swapped-parent covariance, which is an algebraic criterion.

Combining them would conceal anisotropy and is forbidden.

### Boundary phase

Each geometry retains all twist-resolved cases. The channel reports defect-band center
and width, below-edge state count, no-bound-state count, and per-twist diagnostics.
No favorable twist may be selected, omitted, or weighted after observing results.

## Compatible comparisons

Matrices acting on different finite geometries are different representations and are
not subtracted. Cross-geometry operator comparisons use the canonical radius-two local
coefficient record and compatible scalar diagnostics only. Equal dimensions do not
establish equal geometry.

Within one compatible case, report maximum-entry, Frobenius, spectral,
core-restricted, exterior, core-exterior, and shell residuals. The radius-two core uses
minimum-image integer distance from the aligned defect origin.

Spectral and state diagnostics are host-edge-referenced binding energy, below-edge
state count, eigenpair residual, projector fidelity, core probability, inverse
participation ratio, separate $x/y$ RMS radii, and quadrupole anisotropy. A
no-bound-state case retains its status and omits unavailable state-only diagnostics; it
is not a process failure.

## Frozen numerical policies

The inherited tolerances remain:

| Quantity | Threshold |
|---|---:|
| algebraic absolute | $10^{-11}$ |
| projector Frobenius | $10^{-10}$ |
| symmetry/covariance absolute | $10^{-10}E_G$ |
| minimum alignment singular value | $0.5$ |
| degenerate adjacent gap | $10^{-8}E_G$ |
| bound-state threshold | $10^{-10}E_G$ |
| eigenpair residual | $10^{-10}E_G$ |
| independent reconstruction relative | $10^{-10}$ |
| final operator relative change | $10^{-3}$ |
| final energy change divided by parent bandwidth | $10^{-3}$ |
| center or radius absolute change | $10^{-3}$ cells |

A zero normalization denominator stops with
`DEFECT_2D.NONFINITE_DIAGNOSTIC`. Thresholds are reporting criteria, not guarantees of
a pass. There is no pooled area/shape/orientation/twist status.

## Exact proposed inventory

The area and shape channels have nine unique isotropic geometries because
$12\times12$ is shared. Two defects over nine geometries and 81 twists yield 1,458
isotropic operator evaluations.

The orientation channel has two geometry pairs, two defects, and 81 source twists,
yielding 324 comparison records. Each record contains a source evaluation, a rotated
target under the same parent, and a rotated target under the swapped parent, for 972
anisotropic operator evaluations.

The total proposed production inventory is therefore 2,430 operator evaluations. This
count does not include independent-verifier reconstruction and is not execution
authority.

## Failure and retention contract

Process failure, represented incompatibility, no-bound-state outcome, numerical
criterion failure, and nonconvergence are distinct. The inherited structured stops are
retained exactly. Missing cases, discarded failures, changed thresholds, cross-geometry
matrix subtraction, cross-fiber vector comparison, and verifier dependence are hard
failures.

A future result would retain compact case records, all channel tables, provenance,
independent verification, a report, a native-evidence manifest, and a package checksum
catalog. Dense matrices are reconstructed rather than serialized.

## Proposed resource envelope

The proposed implementation is local Python using existing NumPy and SciPy, no
external executable, no network access, maximum scalar matrix dimension 288, estimated
peak memory 2 GiB, and estimated serial runtime 20 minutes. These are design estimates
and, unless future authority explicitly adds proactive containment, would be
post-computation observations rather than hard sandbox limits.

No implementation or execution is authorized by this protocol.
