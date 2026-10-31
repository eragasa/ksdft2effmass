# Accepted-S1 `C6-B20-W21` Wannier90 preprocessing preflight

**Status: superseded before authorization; do not execute or authorize this input.**
[`supersession.json`](supersession.json) binds the operator-directed replacement by the
pinned AiiDA precise convergence-derived tuple.

This directory retains the historical deterministic no-execution preflight for the
selected `C6-B20-W21` target-space candidate. It binds the verified 216-point/20-band Davidson
NSCF saved state and uses rank 10, outer window `[-6.0, 21.0] eV`, frozen window
`[-5.85, 8.00] eV`, and the `Si:sp3` plus `Si:l=0:r=2` projection family.

The maintained ProjectKoios `Wannier90PreprocessingInput.render()` produced
[`silicon.win`](silicon.win) with `mp_grid = 6 6 6` and all 216 source-ordered points.
The saved-state verifier authenticated 219 NSCF files totaling 93,658,989 bytes. No
calculator was invoked, no occurrence root was created, and no saved-state artifact was
copied.

The pure preprocessing renderer includes the convergence and window controls it owns.
`precond`, `num_cg_steps`, `trial_step`, `fixed_step`, `guiding_centres`, and unitary
matrix output controls do not alter `wannier90.x -pp` neighbor topology and are not
rendered here. They remain fixed by the research protocol and must be restored
explicitly in a later localization input. Their absence from this `-pp`-only occurrence
is not an optimizer-policy revision.

## Selected-window inventory

The authenticated 20-band QEXSD gives the following outer-space distribution:

- 48 points contain 12 states;
- 108 points contain 13 states; and
- 60 points contain 14 states.

Every point therefore has at least two outer-space dimensions beyond rank 10. The upper
boundary lies `0.1963949615 eV` above the observed band-12 maximum and
`0.2571673143 eV` below the band-15 minimum. The frozen window contains 4--6 states per
point with histogram `{4: 129, 5: 84, 6: 3}`. These checks establish dimensional
eligibility only; they do not establish optimizer convergence, a global minimum,
interpolation adequacy, or intended-use validity.

## Proposed occurrence

- root:
  `/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier90-preprocess-c6-b20-w21-v1`
- command: `wannier90.x -pp silicon`
- executable SHA-256:
  `c826f817f807cf069e16d6e529a52ddc15d2f677101065908bcb2030d7f7d1dd`
- `silicon.win`: 10,411 bytes, SHA-256
  `50a01489e58d8551a7aa177f53ed2e9b65bf764d2664cebc1ca39a6e53bb433a`
- one process, one invocation, zero retries
- timeout: 120 seconds
- retained-byte ceiling: 32 MiB

Required success evidence includes return code zero, `silicon.nnkp`, bounded maintained
NNKP parsing, direct- and reciprocal-lattice agreement, exact ordered 216-point
agreement, excluded-band agreement, and a projection inventory sufficient for rank 10.

## Identities

| Artifact | SHA-256 |
|---|---|
| target-space decision | `a6f95574137f4b69fd42fc1040d21bc1fd4691487d36a6c1de643d5b1d3c1e2e` |
| source QEXSD | `2e1b5e157142d18210d18710fb9f5f3e813b17d8331acf96e11af9b9d4f7ef8c` |
| source saved-state manifest | `24ee9d483141ab54d099bc6e6403d0da46108cc7a30c5b019992da3a1d7ef3ac` |
| `silicon.win` | `50a01489e58d8551a7aa177f53ed2e9b65bf764d2664cebc1ca39a6e53bb433a` |
| prepared input record | `75527829277d8f48a1142205510ef70c6d2892075e9f2c8d9967a053f2fa9702` |
| campaign preflight | `a106f37e183e018e7ac76303540f98c49f324715e7332b93c7ce03effbcc02ea` |
| authorization request | `f94dd22f911a83aa2779996bfccef211e32ebfbcba2c689fccab476e3c9ad033` |

## Authorization boundary

Status: **superseded before authorization**.

[`authorization-request.json`](authorization-request.json) remains ungranted, and its
SHA-256 `f94dd22f911a83aa2779996bfccef211e32ebfbcba2c689fccab476e3c9ad033` must not be
authorized or replayed. The consumed `C6-B20` `pw.x` authorization and the outer-window
decision do not authorize `wannier90.x -pp`. A distinct precise-derived input and new
request replace this preflight. Conversion, localization, retries, `C6-B30`, `C8`,
`C12`, confirmation, component-operator construction, and Slater--Koster reduction
remain separately controlled occurrences or decisions.
