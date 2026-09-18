# Proposed protocol: controlled two-dimensional defect extraction

## Status and evidence boundary

This versioned protocol is human-accepted and fixes the intended synthetic
inputs, maps, metrics, tolerances, adverse controls, stopping rules, and
verification split. The durable execution checkpoint and bound machine record authorized one local
Stage A null-and-folding execution only; that authority was consumed by the
retained `stage-a-result.json`. The separate acceptance checkpoint human-accepts
that exact Stage A evidence and authorizes managed closeout. Neither decision
authorizes a rerun or work on Stages B--E.

The completed and human-accepted execution produced software and
numerical-verification evidence
for represented finite operators. It did not
perform DFT, production Wannier90, material transfer, silicon or dopant
validation, uncertainty quantification, or spin-space revalidation.

The accepted periodic-2D scalar and composite results are immutable parents.
Stages A--D use the separable scalar entry $\lambda_{xy}=0$; Stage E repeats the
applicable controls at $\lambda_{xy}=0.15$ and adds the rank-three smooth
projected composite parent. The accepted defect-1D and spin-space results supply
inherited contracts; they are not rerun. Exact parent paths and SHA-256 identities are fixed in `study-design.json` and
are checked against the authorization record before execution.

## Spaces, orderings, and energy references

For a supercell with shape $N_x\times N_y$, the scalar represented space is
$\mathbb C^{N_xN_y}$. Its ordering is $x$ outer and $y$ inner. The composite
space is $\mathbb C^{3N_xN_y}$ with orbital index fastest. The energy unit is
$E_G$, and all pristine and defect operators use the identified parent zero
before the deliberate energy-reference attack.

Let $h_{\mathbf R}\in\mathbb C^{r\times r}$ be a retained parent hopping block,
with $r=1$ or $3$. Both parents use the already retained shell
$R_x^2+R_y^2\leq18$; its truncation error remains a separate inherited parent
error and is not relabeled as defect error. For boundary twists
$\boldsymbol\phi=(\phi_x,\phi_y)$ measured in turns, a hop crossing $q_x$ and
$q_y$ supercell boundaries receives

$$
\exp\!\left[2\pi i(q_x\phi_x+q_y\phi_y)\right].
$$

The supercell folding map has entries

$$
F_{\mathbf n\alpha,\mathbf j\beta}
  =(N_xN_y)^{-1/2}
    \exp\!\left[2\pi i\left(
      \frac{j_x+\phi_x}{N_x}n_x+
      \frac{j_y+\phi_y}{N_y}n_y
    \right)\right]\delta_{\alpha\beta}.
$$

The Stage A runner verifies $F^\dagger F=I$, off-block suppression in
$F^\dagger H_{N_x,N_y}F$, agreement with the primitive Bloch blocks, spectral
agreement, Hermiticity, and the seam phases. Folding is tested on both $6^2$ and
$8^2$ cells and at the four frozen twists in `study-design.json`.

## Matched construction and extraction

Every planted control is first constructed in the canonical frame:

$$
H_{\mathrm{def}}=H_{\mathrm{pris}}+\Delta_{\mathrm{plant}}.
$$

The defect frame is then changed by a declared unitary $G$ containing a lattice
translation, a point-group operation, site phases, and, for the rank-three
parent, a permutation, two real plane rotations, and orbital phases. A scalar
shift $c=0.137E_G$ is added:

$$
\widetilde H_{\mathrm{def}}
  =G H_{\mathrm{def}}G^\dagger+cI.
$$

Only after geometry, boundary phase, site correspondence, retained rank,
subspace, and energy reference are compatible may the aligned extraction be
formed:

$$
\Delta_{\mathrm{rec}}
 =G^\dagger(\widetilde H_{\mathrm{def}}-cI)G-H_{\mathrm{pris}}.
$$

The declared-map route and a blind route are separate. The blind route may use
operator blocks and invariant site/orbital fingerprints, but may not read the
planted map. It exhausts the frozen periodic translations and admissible point
group, minimizes the Frobenius mismatch over all off-diagonal site blocks,
synchronizes site phases over the nonzero pristine hopping graph with site
$(0,0)$ as the phase anchor, and uses the singular-value polar factor for the
retained orbital subspace. It is applied only to the three frozen subset cases. Its output is a
recovered map, an ambiguity set, minimum singular values, and a residual. A
disconnected phase graph or candidates tied within $10^{-10}$ stop rather than
being resolved from the plant.

A deliberately unaligned subtraction and an omitted-$cI$ subtraction are
negative controls. Neither is an impurity estimate. Their nonlocal residuals
must remain visible.

## Planted controls and nested model classes

The frozen sequence is:

1. null defect;
2. central scalar onsite defect;
3. an off-axis onsite defect and its complete $D_4$ orbit;
4. unequal horizontal and vertical nearest-neighbor bond changes;
5. a diagonal finite-range nonlocal bond change; and
6. a real Hermitian rank-three onsite block.

Every bond modification includes its Hermitian reverse. Compact planted blocks,
canonical full-matrix digests, and exact support sets must be retained.

The frozen model classes are nested: point scalar onsite; finite-support
diagonal onsite; onsite plus isotropic nearest neighbor; onsite plus directional
nearest neighbor; and finite-range nonlocal radius two. Projection into a model
class is an orthogonal projection in the represented Frobenius inner product.
The first accepted class must satisfy every applicable frozen operator and
observable criterion. A favorable eigenvalue alone cannot accept a class.

## Symmetry and orientation

For the isotropic scalar parent on the frozen $8\times8$ square, each $D_4$
operation is represented as an exact permutation/unitary $U_g$ on the periodic
supercell. The covariance residual is

$$
\left\|\Delta_{g\cdot p}-U_g\Delta_pU_g^\dagger\right\|,
$$

where $p$ identifies defect placement and orientation. At nonzero twist, the
same integer point-group matrix $M_g$ also maps
$\boldsymbol\phi\mapsto M_g\boldsymbol\phi\pmod 1$; covariance therefore
compares the transformed fiber, not the original twist. Keeping a generic twist
fixed under a quarter turn is a mandatory negative control. Site coordinates
are wrapped only after the integer point-group action, avoiding a floating-point
nearest-site rule.

The anisotropic parent has only the declared $D_2$ symmetry. A quarter turn is
not tested as self-covariance: it maps to the separately reconstructed parent
with $\lambda_x$ and $\lambda_y$ exchanged. Claiming $D_4$ for that parent is a
mandatory negative control.

## Degenerate clusters and composite alignment

Individual eigenvectors inside an exactly or numerically degenerate cluster are
not invariant. Clusters are identified from the frozen parent spectrum using
the fixed absolute adjacent-gap threshold $10^{-8}E_G$; their rank may not be
changed after looking at the defect result. For orthonormal cluster bases $V$
and $W$, the primary objects are projectors $P=VV^\dagger$ and $Q=WW^\dagger$.
The retained diagnostics are
$\|P-Q\|_F$, principal angles from the singular values of $V^\dagger W$, and the
minimum alignment singular value.

If an attempted comparison addresses individual vectors in a degenerate
cluster, it stops with `DEFECT_2D.DEGENERATE_PROJECTOR_REQUIRED`. If the minimum
alignment singular value is below 0.5, subtraction stops with
`DEFECT_2D.SUBSPACE_OVERLAP_TOO_SMALL`.

## Area, shape, orientation, and boundary phase

Area refinement uses only the frozen square sequence
$6^2,8^2,10^2,12^2,16^2$. Shape refinement uses only the five area-144
rectangles. These sequences answer different questions and are never pooled.
The $8\times18$ and $18\times8$ pair, and the $9\times16$ and $16\times9$
pair, are also orientation controls for the anisotropic parent.

At each applicable geometry, the $9\times9$ twist mesh is exactly
$(\phi_x,\phi_y)=(m/9,n/9)$ turns for $m,n\in\{0,\ldots,8\}$. It is used for
defect-band center and width. Boundary-phase changes, shape changes, and area
changes remain separate axes. The common radius-two core is defined by the
minimum-image integer distance from the defect site.

Reported operator diagnostics are maximum-entry, Frobenius, spectral,
core-restricted, exterior, core--exterior, and spatial-shell norms. Spectral and
state diagnostics are host-edge-referenced binding, below-edge state count,
defect-band center and width, projector fidelity, core probability, inverse
participation ratio, separate $x/y$ RMS radii, and quadrupole anisotropy. A
no-bound-state result is a retained scientific outcome, not a failed process.

The frozen finite-size thresholds are reporting criteria, not guarantees of a
pass. Operator change is normalized by the reference operator norm; energy
change is normalized by the identified parent bandwidth; center and radius
changes use absolute cell units. Zero denominators cause a structured
nonfinite-diagnostic stop rather than an altered normalization. The below-edge
classification uses the fixed $10^{-10}E_G$ energy threshold, and every retained
eigenpair must have residual at most $10^{-10}E_G$. A failed or nonmonotone
sequence remains evidence. Parent truncation, finite area, shape, boundary
phase, alignment, model reduction, eigensolver, and serialization errors must
be tabulated separately.

## Structured stops

No operator residual is returned after any of these issues:

- parent identity mismatch;
- nonunitary folding map;
- incompatible geometry;
- incompatible boundary phase;
- unresolved site map;
- insufficient subspace overlap;
- an individual-vector request for a degenerate cluster;
- unknown energy-reference relation; or
- a nonfinite diagnostic.

The exact pristine/candidate metadata and issue codes for the four Stage A
controls are frozen in `study-design.json`. The runner must derive rather than
copy each issue code, and the verifier must independently derive it from the
retained metadata. Process failure, structured incompatibility, no-bound-state
outcomes, and numerical criterion failures are distinct statuses.

## Independent verification contract

`verify_stage_a.py` does not import the runner or reuse its folding,
alignment, symmetry, model-projection, or observable functions. It must:

1. verify every identified input digest;
2. reconstruct parent blocks from retained parent records;
3. build supercells through Kronecker products of independently constructed
   one-dimensional seam matrices rather than the runner's site-and-hop route;
4. reconstruct the folding matrix from Kronecker Fourier factors;
5. reconstruct each planted defect from the compact support record;
6. enumerate $D_4$ and $D_2$ maps from integer matrices;
7. recover blind maps without reading planted maps;
8. diagonalize independently and compare degenerate projectors;
9. reproduce all area, shape, twist, shell, and model-class tables; and
10. reject missing failures, discarded trajectories, changed tolerances, or
    checksum mismatches.

A deterministic plotter, if later authorized, may read only the retained result.
It may not recompute or replace evidence.

## Fail-closed execution authorization

The Stage A runner requires a separate schema-version-2 JSON authorization
record. The accepted design is deliberately insufficient. The current record
binds an authorization identifier; durable checkpoint path and SHA-256;
canonical absolute repository root; repository-relative design, runner,
parent, and output paths; SHA-256 identities for every immutable input; the
exact Stage A resource envelope; and the verbatim human response. The runner
also validates the resolved checkpoint's task, scope, response, and
authoritative-file inventory.

The runner rejects absolute, traversing, noncanonical, or out-of-root retained
paths; refuses a different stage, changed digest, larger resource envelope, or
network access; hashes and retains every authority/provenance input; and refuses
to overwrite an existing output. The independent verifier repeats the binding,
canonical-path, digest, checkpoint, exact-case-inventory, seam-sign, stop, and
criterion checks.

## Staged authorization and future reproduction

Execution is separately authorized by stage. Stage A is human-accepted and its
managed closeout is authorized; Stage B may
begin only after a separate explicit human decision based on Stage A's complete
retained record. Stages C--E are not implicitly authorized by an earlier stage.
No stage may tune defects, tolerances, cluster ranks, or model classes in
response to observed outcomes.

The authorized Stage A envelope is local Python with existing NumPy and SciPy
dependencies, no external executable, no network access, matrix dimension at
most 64, at most 2 GiB peak memory, and at most 120 seconds runtime. Broader
full-sequence estimates remain proposed work rather than execution authority or
measured results.
