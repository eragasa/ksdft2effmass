# Accepted-S1 `C6` Wannier90 preprocessing preflight

This directory retains the no-execution preflight for the next distinct `C6` route
occurrence. It consumes the verified 216-point/12-band Davidson NSCF saved state and
uses the unchanged rank-10 target, `Si:sp3` plus `Si:l=0:r=2` projections, outer window
`[-5.85, 19.02] eV`, and frozen window `[-5.85, 8.00] eV`.

The maintained ProjectKoios `Wannier90PreprocessingInput.render()` produced
[`silicon.win`](silicon.win) with `mp_grid = 6 6 6` and all 216 source-ordered points.
The saved-state verifier authenticated 219 NSCF files totaling 58,433,245 bytes. No
calculator was invoked and no artifact was copied.

The pure preprocessing renderer includes the convergence and window controls it owns.
`precond`, `num_cg_steps`, `trial_step`, `fixed_step`, `guiding_centres`, and unitary
matrix output controls do not alter `wannier90.x -pp` neighbor topology and are not
rendered here. They remain fixed by the research protocol and must be restored explicitly
in the later localization input. Their absence from this `-pp`-only occurrence is not a
localization-policy revision.

## Fixed-window inventory

Over the `C6` source mesh, the outer window contains 10--12 states per point: 142 points
with 12, 62 with 11, and 12 with 10. The frozen window contains 4--6 states per point:
129 points with four, 84 with five, and three with six. The minimum outer count equals
the Wannier rank and the maximum frozen count remains below it, so the fixed windows are
dimensionally eligible. This does not establish interpolation adequacy.

## Proposed occurrence

- root:
  `/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier90-preprocess-c6-lower-energy-frozen-v1`
- command: `wannier90.x -pp silicon`
- executable SHA-256:
  `c826f817f807cf069e16d6e529a52ddc15d2f677101065908bcb2030d7f7d1dd`
- `silicon.win`: 10,417 bytes, SHA-256
  `2d5e4f0486e5062a8dd89a202845b8deac65efffea8acc0be05c192a4c12b604`
- one process, one invocation, zero retries
- timeout: 120 seconds
- retained-byte ceiling: 32 MiB

Required success evidence includes return code zero, `silicon.nnkp`, bounded maintained
NNKP parsing, direct- and reciprocal-lattice agreement, exact ordered 216-point
agreement, excluded-band agreement, and a projection inventory sufficient for rank 10.

## Identities

| Artifact | SHA-256 |
|---|---|
| `silicon.win` | `2d5e4f0486e5062a8dd89a202845b8deac65efffea8acc0be05c192a4c12b604` |
| prepared input record | `8f0443d37bc6b554a520c5415afa318e4964f33047062b202a2ce046b0d6163b` |
| campaign preflight | `88b3bf7988327461a19b14fe6f770bfbefdeab3e3d93e8c171d999ba481a0307` |
| authorization request | `28599fee49e6b4b7050f2a9d714770bcaf6246be2aa99837a191352c5120a430` |

## Authorization boundary

Status: **authorization required**.

The consumed C6 `pw.x` authorization does not authorize `wannier90.x -pp`. The request
retains `authorization_granted: false`. Preprocessing, conversion, localization, retries,
`C8`, and `C12` remain separately controlled occurrences or decisions.
