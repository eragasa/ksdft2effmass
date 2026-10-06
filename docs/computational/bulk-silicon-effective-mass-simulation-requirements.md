# Bulk-Silicon Effective-Mass Simulation Requirements

**Status:** exact proposed simulation request; inactive and unauthorized.

This document states the Quantum ESPRESSO simulations needed to evaluate the
conduction-electron observables defined by
[`SiliconEffectiveMassValidationSpecification-v1`](../../specification/ksdft2Effmass.silicon-effective-mass-validation.v1.md).
It selects a bounded simulation design, not accepted scientific values. No command in
this document may be executed without a separate protected-execution preflight and
explicit human authorization.

No Wannier90 execution is requested here. A direct parent-DFT mass reference must be
accepted first. A later Wannier request requires separately approved rank, parent-band
count, projections, windows, uniform meshes, and parent-to-Wannier accuracy thresholds.

## Exact common physical branch

All requested calculations use:

- pristine diamond silicon in the two-atom primitive cell;
- PBE;
- the scalar-relativistic, norm-conserving PseudoDojo PBE standard-table silicon
  pseudopotential `Si.upf`, SHA-256
  `39822757f53f36e3bf3bfb779356152a8d3f21199c7db9dd5a931e5d18c45282`;
- four valence electrons per silicon atom;
- non-spin-polarized, non-SOC, fixed occupations;
- `ibrav=2`, `nat=2`, and one silicon species, with the two atoms represented as
  Cartesian `alat` positions `(0,0,0)` and `(0.25,0.25,0.25)`;
- the same primitive-vector and conventional-cubic Cartesian-axis convention in every
  stage; and
- one local process unless a separately reviewed execution design changes the
  parallel decomposition.

The required executable is Quantum ESPRESSO 7.5 `pw.x` at
`/Users/eugene/projects/q-e-qe-7.5/build/bin/pw.x`, SHA-256
`87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910`.
The source identity is tag `qe-7.5`, commit
`770a0b2d12928a67048e2f3da8d10d057e52179e`. The retained QE 7.2 cutoff/mesh
results may inform the bounded candidate matrix but are not QE 7.5 numerical evidence
and are not reused as campaign observations. A different executable is another
comparison variable and requires its own compatibility and numerical-disposition
record.

Common SCF settings are the retained production-design settings:

- `calculation='scf'`;
- `occupations='fixed'`;
- `diagonalization='david'`;
- `mixing_mode='plain'`;
- `mixing_beta=0.7`;
- `electron_maxstep=100`;
- `conv_thr=1.0d-12 Ry`;
- `ecutrho=4*ecutwfc`; and
- shifted even Monkhorst--Pack meshes written as `N N N 1 1 1`.

Every NSCF child must consume an identity-verified isolated copy of its SCF parent's
native state. An NSCF must not mutate the retained authoritative parent scratch tree.
Explicit local-point NSCFs use `nosym=.true.` and `noinv=.true.` so that every listed
point and wavefunction is retained rather than symmetry-collapsed. They use `nbnd=12`,
the parent cutoff, `diagonalization='david'`, `diago_thr_init=1.0d-12`, and
`diago_full_acc=.true.`; the reported convergence of every state is retained.
Full-precision QEXSD eigenvalues, not four-decimal stdout values, are the numerical
source for derivatives.

## Stage 1 — one zero-pressure PBE variable-cell relaxation

Determine one campaign geometry with a single symmetry-preserving variable-cell
relaxation. Start from `celldm(1)=10.20 bohr` and use the conservative design setting
`ecutwfc=48 Ry`, `ecutrho=192 Ry`, and `8 8 8 1 1 1`. The required controls are:

```text
calculation='vc-relax'
ion_dynamics='bfgs'
cell_dynamics='bfgs'
cell_dofree='volume'
press=0.0 kbar
press_conv_thr=0.05 kbar
etot_conv_thr=1.0d-8 Ry
forc_conv_thr=1.0d-6 Ry/bohr
nstep=100
```

`cell_dofree='volume'` changes only the cubic scale and preserves the fcc/diamond cell
shape. This is a zero-pressure geometry search, not a requested strain series. Retain
every BFGS step, cell, energy, force, pressure, and stress observation. A nonzero exit,
missing `JOB DONE.`, exhausted step limit, unconverged pressure, broken diamond
symmetry, or cell-shape change stops the campaign.

Call the final conventional cubic lattice parameter `a_relax`. Generate and run one
new from-scratch SCF at exactly `a_relax`, with the same 48/192-Ry and shifted-8-cubed
settings, to verify the final pressure/stress and create the immutable `E48K8` parent
state. Do not reuse the mutable `vc-relax` scratch as the parent of local NSCF jobs.

The relaxation determines the fixed geometry used by every later calculation. It does
not provide an EOS fit, bulk modulus, lattice uncertainty, strain response, or the
`1e-4 Å` EOS-refinement evidence required for a separate precision lattice claim.

Stage 1 requests two `pw.x` invocations: one `vc-relax` and one final-geometry SCF.

## Stage 2 — final-geometry cutoff–mesh corner

At the fixed Stage-1 lattice `a_relax`, evaluate this complete four-corner SCF matrix:

| ID | `ecutwfc` | `ecutrho` | shifted SCF mesh |
|---|---:|---:|---|
| `E42K6` | 42 Ry | 168 Ry | `6 6 6 1 1 1` |
| `E48K6` | 48 Ry | 192 Ry | `6 6 6 1 1 1` |
| `E42K8` | 42 Ry | 168 Ry | `8 8 8 1 1 1` |
| `E48K8` | 48 Ry | 192 Ry | `8 8 8 1 1 1` |

The final Stage-1 SCF is `E48K8` and must be reused. Stage 2 therefore requests three
new SCFs. The four corners determine
cutoff sensitivity, SCF-mesh sensitivity, and the mixed cutoff–mesh contrast at the
accepted geometry. None of the four is accepted before the band-edge analysis below.

## Stage 3 — representative positive-y Delta-valley location

For each of the four Stage-2 parents, run two adaptive explicit-point NSCF jobs.
Weights are operational placeholders only and are not Brillouin-zone integration
weights.

### Locator 1

Include Gamma `(0,0,0)`, X `(0,1,0)`, and the 51 `tpiba` points

```text
(0, xi_j, 0),  xi_j = 0.800 + 0.002*j,  j = 0,...,50.
```

The coordinates are Cartesian in units of `2*pi/a_relax`, with axes fixed to the
recorded conventional cubic axes. Gamma and X are fixed-point spectral diagnostics
only: retain their conduction eigenspace multiplicities and ordered eigenvalues, but
do not require a rank-one band-5 state, include them in the quartic fit, or use them in
the valley identity chain. Their symmetry-enforced degeneracies are not a locator
failure.

Before reading the 51 local scan energies, assign even `j` to the fit set and odd `j`
to the withheld set. On those scan points only, require the target lowest-conduction
state to remain nondegenerate and spectrally isolated from adjacent states. Fit a
quartic polynomial in a scaled local coordinate to that identity-tracked local state.
Retain the interior positive-curvature stationary root, design-matrix singular values,
residuals, and withheld residuals. A boundary root or a state-identity failure within
the local scan stops the stage. Call the root `xi1`.

### Locator 2

Run 41 points

```text
(0, xi1 + 0.0005*j, 0),  j = -20,...,20.
```

Assign even `j` to the fit set and odd `j` to the withheld set before reading energies.
Use the same scaled quartic procedure and call the interior positive-curvature root
`xi2`. Require

```text
abs(xi2 - xi1) <= 0.002
```

and retain the difference between the training-only and all-point roots. `xi2` is the
center for the local tensor stencil. Locator points are not mass-fit points.

Stage 3 requests eight NSCF invocations: two for each Stage-2 parent.

## Stage 4 — full Cartesian Hessian and withheld directions

For each Stage-2 parent, construct one explicit-point NSCF centered at

```text
k0 = (0, xi2, 0)
```

using Cartesian `tpiba` axes `ex=(1,0,0)`, `ey=(0,1,0)`, and `ez=(0,0,1)`.

### Hessian points

For each `h` in

```text
0.020, 0.010, 0.005
```

include:

- `k0`;
- `k0 ± h*ei` for `i=x,y,z`; and
- `k0 + s*h*ei + t*h*ej` for each pair `i<j` and `s,t in {-1,+1}`.

After removing the repeated center, this is 55 unique points. It determines all three
diagonal and all three mixed Hessian components by centered differences. Construct
one Hessian at each radius. The primary zero-radius estimate is the componentwise
Richardson estimate from `h=0.010` and `h=0.005`; the independent larger-radius check
is the Richardson estimate from `h=0.020` and `h=0.010`. Retain both without averaging
them.

### Withheld points

The same NSCF also includes 24 points

```text
k0 + 0.0075*d
```

where `d` runs over every distinct permutation and independent sign assignment of
`(2,1,0)/sqrt(5)`. These points are not used in the centered-difference Hessian.
Pair opposite directions, construct twelve withheld directional curvatures, and
compare them with `d.T @ K @ d` from the primary Richardson tensor. Also fit an
independent symmetric tensor to the withheld set and compare it with the primary
tensor.

Require:

- the full Cartesian gradient at the center to be numerically consistent with zero;
- a nondegenerate identity-tracked conduction state throughout the stencil;
- a Hermitian real-valued scalar band-energy Hessian within extraction precision;
- positive principal curvatures;
- no more than `0.5%` relative change in longitudinal or either transverse mass
  between the two Richardson estimates; and
- no more than `0.5%` relative discrepancy for each withheld directional curvature
  and the independent withheld tensor principal masses.

If the withheld check fails while state identity and numerical precision pass, run a
new predeclared half-radius design rather than deleting points or changing the fit
after seeing the values.

Stage 4 requests four NSCF invocations, one 79-point job per Stage-2 parent.

## Stage 5 — cutoff, mesh, and interaction assessment

For valley position, indirect gap, the six Hessian components, longitudinal mass, and
both transverse masses, compare:

- `E42K6` with `E48K6` for cutoff sensitivity;
- `E42K6` with `E42K8` for SCF-mesh sensitivity;
- `E48K6` with `E48K8` and `E42K8` with `E48K8` as guard-side checks; and
- the four-corner mixed contrast.

The frozen acceptance values are `0.002` in fractional valley coordinate, `1 meV`
for the indirect Kohn–Sham gap between numerical settings, and `0.5%` relative change
for each longitudinal and transverse mass. The tensor Frobenius error, principal-axis
rotation, mixed contrast, gradients, residuals, and conditioning remain mandatory
diagnostics even when scalar thresholds pass.

If a cutoff comparison fails, add `54 Ry / 216 Ry` at both the required 6-cubed and
8-cubed mesh corners and repeat Stages 3 and 4 for those new parents. If a mesh
comparison fails, add shifted 10-cubed parents at the required 42-Ry and 48-Ry cutoff
corners and repeat Stages 3 and 4. If both axes fail, include the needed 54-Ry,
10-cubed interaction corner. No extension is automatic; report the failed bounded
matrix and obtain authorization for the exact extension.

## Stage 6 — explicit six-valley equivalence check

Only after Stage 5 identifies the smallest passing parent and its guard, run one final
explicit-point NSCF from the selected parent's isolated state. Use the six centers

```text
(+xi2,0,0), (-xi2,0,0),
(0,+xi2,0), (0,-xi2,0),
(0,0,+xi2), (0,0,-xi2).
```

At every center, include the complete 55-point three-radius Hessian design and the 24
withheld directions from Stage 4: 79 points per valley, 474 points total before any
accidental duplicate removal. Do not symmetry-collapse this list. Construct each
Cartesian tensor independently and only then apply the explicit cubic rotations that
map the six valley axes.

Require the six locations to agree within `0.002` after their explicit coordinate
maps and require the rotated longitudinal and both transverse masses to agree within
`0.5%`. Retain the two transverse values before any average, the transverse splitting,
longitudinal–transverse coupling, off-diagonal entries, and principal-axis rotation.
A failed equivalent-valley check makes the result not accepted or inconclusive; it is
not repaired by averaging.

Stage 6 requests one 474-point NSCF invocation.

## Exact bounded request and adaptive boundary

Without a failed relaxation or cutoff/mesh/mass gate, the request is:

| Stage | New `pw.x` invocations | Reuse |
|---|---:|---|
| Variable-cell relaxation and final-geometry SCF | 2 | final SCF becomes `E48K8` |
| Remaining final-geometry four-corner SCFs | 3 | Stage-1 `E48K8` |
| Two valley locators for four parents | 8 | none |
| Hessian/withheld NSCF for four parents | 4 | none |
| Six-valley equivalence NSCF | 1 | selected Stage-2 parent |
| **Total** | **18** | one QE 7.5 SCF reused within this campaign |

Any extension is a new bounded request. The 18-invocation matrix does not authorize
execution and does not include Wannier90, `pw2wannier90.x`, `bands.x`, DOS, DFPT,
phonons, SOC, dopants, strain, or tight-binding fitting.

## Required outputs and provenance

For every invocation retain:

- exact input bytes and ordered input manifest;
- executable path, SHA-256, version banner, invocation, host, process/thread counts,
  environment, and software versions;
- pseudopotential authority and execution-copy identities;
- parent/child lineage and before/after scratch inventories;
- stdout, stderr, exit status, `JOB DONE.` status, elapsed time, peak RSS, warnings,
  and failure disposition;
- full QEXSD and full-precision ordered eigenvalues;
- explicit reduced and Cartesian reciprocal coordinates and the lattice map;
- wavefunctions needed for state-overlap correlation, retained externally under
  checksummed manifests; and
- compact energy, stress, valley, fit, Hessian, mass, conditioning, residual, and
  acceptance tables.

The recurring IEEE exception report observed in the retained bootstrap matrix must be
captured and classified before final parent acceptance. A zero exit status does not
classify it.

Large wavefunctions, densities, restart trees, and scratch files remain external and
must not be committed. No output may be called converged, validated, or accepted until
the corresponding analysis gate has passed.

## Planning resources

The retained QE 7.2 one-process matrix measured approximately 2--11 seconds per small
SCF and about 0.3--0.4 seconds for three-point NSCF jobs. Those cross-version planning
observations do not measure the proposed relaxation or 79- or 474-point jobs. For
protected-execution planning, reserve up to 60 minutes for the variable-cell
relaxation, 10 minutes per SCF, 10 minutes per ordinary local NSCF, 30 minutes for the
474-point NSCF, 6 hours total wall allocation, 2 GiB peak memory, and 4 GiB external
storage.
These are conservative reservations to be replaced by recorded measurements, not
performance claims.
