# Withheld-parent validation preflight

## Status

This package froze the recommendation before execution. The operator subsequently
authorized exactly one invocation. The local QE 7.5 Davidson NSCF completed once with
no retry; retained evidence and the frozen comparison are under
[`../../simulations/evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-withheld-parent-nscf-408-david/`](../../simulations/evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-withheld-parent-nscf-408-david/).

The occurrence used the accepted S1 parent,
accepted 42/336 Ry cutoffs, 12 bands, fixed occupations, and disabled symmetry and
inversion reduction. The QE input reuses the exact eight-decimal cell text that produced
the accepted parent saved state; the point design retains the full-precision accepted-S1
basis and records their `3.1798967903284847e-09 angstrom` maximum component difference.
The exact proposed input is [`pw.in`](pw.in).

## Frozen validation design

The point inventory is candidate-conditioned but construction-disjoint. Candidate
locations came from the authenticated provider-eligible operator characterization;
no direct-parent values were observed while selecting points.

For each of six Delta-valley candidates the inventory contains:

- the candidate center;
- complete Cartesian quadratic stencils at `0.002`, `0.005`, and `0.010 inverse
  angstrom` (six axial and twelve mixed points per scale);
- axial capture points at `0.020` and `0.040 inverse angstrom`; and
- one separate Cartesian symmetry anchor at the mean candidate-valley radius for each
  signed cubic axis.

After exact periodic de-duplication, the manifest contains 408 points. None overlaps the
Gamma-origin `4 x 4 x 4` Wannier construction mesh. The design supports direct energy
residuals, local gradients, three-dimensional Hessians, mass tensors, fit-window
sensitivity, and a bounded check that a matched parent minimum remains inside the
sampled neighborhood. A joint direct-parent quadratic fit through radii no greater than
`0.010 inverse angstrom` locates the matched parent minimum. The gating mass comparison
uses parent and candidate three-dimensional fits on the identical `0.002 inverse
angstrom` stencil, matching the primary scale already frozen by the candidate
characterization; `0.005` and `0.010 inverse angstrom` fits remain sensitivity
observations. Full Cartesian mass tensors and their basis are reported.

The point order, roles, fractional coordinates, QE weights, lattice convention, source
identities, and separation check are retained in
[`withheld-kpoint-manifest.json`](withheld-kpoint-manifest.json).

## Intended-use criteria

The [tolerance authority review](tolerance-authority-review.md) adopts existing
publication-program targets rather than thresholds inferred from the candidate. This is
a necessary pilot screen, not an additive allocation or proof of the publication
program's still-blocked PseudoDojo and independent-toolchain gates:

- indirect gap relative error no greater than `5%`;
- valley-position error no greater than `3%` of Gamma--X, equal to
  `0.03446503626832577 inverse angstrom` for accepted S1; and
- relative error no greater than `8%` for every longitudinal and transverse electron
  effective mass.

The indirect gap uses the authenticated existing Gamma-point parent VBM as a declared
construction-point support datum and the newly withheld conduction minimum. Complete
spectral residuals use gauge-invariant injective matching of the rank-10 candidate
spectrum into the 12 parent eigenvalues; no unaligned operators are subtracted.
Spectral residuals, symmetry splittings, gradients, fit residuals, and stencil
sensitivity are mandatory observations but non-gating because no reviewed intended-use
tolerance currently owns them. The exact machine-readable criteria are in
[`validation-criteria.json`](validation-criteria.json).

A criterion failure means inadequate for this declared intended use; it does not mean
the finite operator is intrinsically invalid. Missing domain capture, unsuitable fits,
band-tracking ambiguity, unconverged eigenvalues, nonfinite data, or undefined relative
metrics produce an inconclusive outcome.

## Protected occurrence

The machine-readable [`authorization-request.json`](authorization-request.json) bound:

- one invocation and no retry;
- `/Users/eugene/projects/q-e-qe-7.5/build/bin/pw.x` with its accepted SHA-256;
- the exact generated input and validation records;
- the accepted SSSP pseudopotential identity;
- a verified isolated copy of the accepted parent saved state, never mutation of the
  source tree;
- one local process;
- required outputs and blocking diagnostic policy; and
- a `2 GiB` retained-byte ceiling.

The 408-point set is 6.375 times the point count of the prior 64-point Davidson NSCF.
The observed QE wall time was `62.67 s`. The verified child saved state contains 411
files and 108,034,728 bytes. The whole external occurrence remained below the `2 GiB`
retention bound.

The repository request remains `authorization_granted: false` as immutable preflight
evidence. The later explicit operator instruction is retained separately as consumed by
the one completed occurrence. No retry is authorized.

Prepared identities:

| Artifact | SHA-256 |
|---|---|
| `withheld-kpoint-manifest.json` | `754bce5030ef0e34eb092406b27d9094287b4f749e358ef36404040f44b8d2b4` |
| `validation-criteria.json` | `ab2a9f18876f773e8c6535e00a6ce65be5c65b32117b258d503423007389c5cb` |
| `pw.in` | `3b13803d8ec296d02140f1e9c2521e2eb4d8620b380dd26ede880ae5230ac3f6` |
| `authorization-request.json` | `9721b01ca70834a9ff6ae98da39442aba0fe7e207b7ed19b447ea641256c4c3a` |

## Result

The six valley-position comparisons met their frozen target. The indirect-gap error was
`14.5009%`, two longitudinal-mass comparisons and all transverse-mass comparisons
exceeded their intended-use targets, and the candidate disposition is
`not-adequate-for-declared-intended-use`. This is an intended-use result, not an
intrinsic-invalidity claim.

[`analyze_validation.py`](analyze_validation.py) retains the object-oriented,
no-calculator comparison implementation. Its exact retained result has SHA-256
`46f3716e20037187989863fccad9181402a7dc4f4b89e3c143527b10353c7aa6`.

The revealed parent data are now development evidence for successors. The
[construction-mesh adequacy recommendation](../construction-mesh-adequacy-recommendation/)
records the protocol-first `C6` one-variable revision and a separate 402-point
successor-confirmation geometry whose parent values remain unobserved. No successor
calculator occurrence is authorized by that recommendation.

## Reproduce preparation

From the repository root:

```text
PYTHONPATH=python/src:/Users/eugene/worktrees/projectkoios-simulations-pw-dft-wannierization-tranche-1/src/python \
  python/.venv/bin/python \
  calculations/Si/bulk/analysis/withheld-parent-validation-preflight/prepare_validation.py
```

The object-oriented preparation authenticates its source structure and candidate
characterization, constructs the point inventory with PhysKit lattice primitives, and
uses KSD's generic typed JSON serializer for all machine-readable records.
