# `C6-B20-W21` AiiDA-precise preprocessing preflight

This directory retains the consumed deterministic no-execution preprocessing preflight
for `C6-B20-W21` using the convergence-derived tuple from the precise protocol in
pinned `aiida-wannier90-workflows` 3.1.0. It supersedes the earlier ungranted hybrid
4000-step request.

For the exact two-atom cell, the adopted convergence profile is:

```text
conv_tol       = 2.0e-9 angstrom^2
conv_window    = 6
num_iter       = 40000

dis_conv_tol   = 2.0e-9  # dimensionless
dis_num_iter   = 40000

num_cg_steps   = 200
```

The maintained ProjectKoios `Wannier90PreprocessingInput.render()` produced
[`silicon.win`](silicon.win) with 20 parent bands, rank 10, outer window
`[-6.0, 21.0] eV`, frozen window `[-5.85, 8.00] eV`, `mp_grid = 6 6 6`, and all 216
source-ordered points. The saved-state verifier authenticated 219 NSCF files totaling
93,658,989 bytes. No calculator was invoked, no occurrence root was created, and no
saved-state artifact was copied.

`num_cg_steps = 200` is a localization-only control and is therefore not emitted by the
pure `-pp` renderer. It is bound in the preflight record and must be restored explicitly
in the later localization input. The same applies to other localization-only controls
that do not alter NNKP topology.

## Adaptation boundary

This preflight does not adopt AiiDA's precise factor-three band count, automatic
`0.1 inverse angstrom` mesh rule, PBEsol pseudopotential family, projections,
automatic energy windows, MPI layout, wall-clock limit, or restart handlers. The
accepted PBE parent, ordered C6 mesh, 20-band inventory, rank, windows, and declared
projection family remain calculation-owned.

The 40000-step values are fixed ceilings, not evidence that either local optimization
will converge or find a global minimum. No automatic extension follows failure at
either ceiling.

## Selected-window inventory

The outer window contains 12 states at 48 points, 13 at 108 points, and 14 at 60
points. Its upper boundary lies `0.1963949615 eV` above the observed band-12 maximum
and `0.2571673143 eV` below the band-15 minimum. The frozen window contains 4--6 states
with histogram `{4: 129, 5: 84, 6: 3}`. These establish dimensional eligibility only.

## Proposed occurrence

- root:
  `/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier90-preprocess-c6-b20-w21-aiida-precise-v1`
- command: `wannier90.x -pp silicon`
- executable SHA-256:
  `c826f817f807cf069e16d6e529a52ddc15d2f677101065908bcb2030d7f7d1dd`
- `silicon.win`: 10,413 bytes, SHA-256
  `b48069e4f8ecd7209a318c47c77691de063bd0575658eb88a1e662a359d3dcc8`
- one process, one invocation, zero retries
- timeout: 120 seconds
- retained-byte ceiling: 32 MiB

Required success evidence includes return code zero, `silicon.nnkp`, bounded maintained
NNKP parsing, direct- and reciprocal-lattice agreement, exact ordered 216-point
agreement, excluded-band agreement, and a projection inventory sufficient for rank 10.

## Identities

| Artifact | SHA-256 |
|---|---|
| AiiDA-precise adaptation decision | `9d2e8269d1f2351d1c3b3228c24f4b2baad6505c1c1039da8889412b3cba6238` |
| updated target-space decision | `526b0a265b306c13f9ae54ce34c57030277f15704a4a571295da43330005db59` |
| pinned AiiDA convergence reference | `a3486e60610ff7b1cdf4d7fdbdc5aad4195437657f0dd19a8e01cb4acb63d48d` |
| source QEXSD | `2e1b5e157142d18210d18710fb9f5f3e813b17d8331acf96e11af9b9d4f7ef8c` |
| source saved-state manifest | `24ee9d483141ab54d099bc6e6403d0da46108cc7a30c5b019992da3a1d7ef3ac` |
| `silicon.win` | `b48069e4f8ecd7209a318c47c77691de063bd0575658eb88a1e662a359d3dcc8` |
| prepared input record | `589159914744789ead9bb665912a6d44283ddb0227d8dc6d12f8a03736edbe64` |
| campaign preflight | `44aadafc9144a586e8fd299a460a59b24f8971f488c0671e6f1fd55b9e928ec7` |
| authorization request | `c7d18564bfc163aea72f0975f343cfea409c4f66c6618333d7c7da54ca06996d` |

## Authorization boundary

Status: **consumed by one completed occurrence**.

[`authorization-request.json`](authorization-request.json) remains the immutable
ungranted preflight request, while its exact identity was authorized separately and
consumed by one occurrence. Compact authenticated result evidence is retained under
[`../../evidence/sssp-1.3.0-pbe-efficiency-wannier90-3.1.0-accepted-s1-preprocess-c6-b20-w21-aiida-precise/`](../../evidence/sssp-1.3.0-pbe-efficiency-wannier90-3.1.0-accepted-s1-preprocess-c6-b20-w21-aiida-precise/).
The request cannot authorize a retry. Conversion, localization, `C6-B30`, `C8`, `C12`,
confirmation, component-operator construction, and Slater--Koster reduction remain
separately controlled occurrences or decisions.
