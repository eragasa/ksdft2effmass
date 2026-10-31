# C6-B20-W21 outer-window decision

## Decision

Select `C6-B20-W21` as the next target-space candidate. It uses the authenticated
20-band `C6-B20` parent inventory and the outer window `[-6.0, 21.0] eV`. The
prospective Wannier rank remains 10, the frozen window remains `[-5.85, 8.00] eV`, and
the `Si:sp3` plus `Si:l=0:r=2` projection family remains fixed.

This decision authorizes deterministic no-calculator preprocessing preparation only. It
does not authorize `wannier90.x -pp`, `pw2wannier90.x`, localization, retry, `C6-B30`,
`C8`, `C12`, confirmation, component-operator construction, or Slater--Koster
reduction.

## Evidence basis

The authenticated `C6-B20` QEXSD has SHA-256
`2e1b5e157142d18210d18710fb9f5f3e813b17d8331acf96e11af9b9d4f7ef8c` and contains 216
ordered Gamma-origin points and 20 finite bands spanning
`[-5.8341319732, 30.2720123939] eV`. Its first 12 eigenvalues reproduce the earlier
12-band occurrence within `4.14e-11 eV`. The saved-state manifest has SHA-256
`24ee9d483141ab54d099bc6e6403d0da46108cc7a30c5b019992da3a1d7ef3ac` and verifies 219
files totaling 93,658,989 bytes.

Under the selected outer window, the parent-state inventory is:

```text
12 states:  48 points
13 states: 108 points
14 states:  60 points
```

Thus every construction point has at least two outer-space dimensions beyond rank 10.
Bands 13 and 14 enter according to energy, contributing 228 states in total. Band 15
has a global minimum of `21.2571673143 eV`, so bands 15--20 do not enter the selected
window on the construction mesh.

The upper boundary has two observed clearances:

- `21.0 - max(band 12) = 0.1963949615 eV`; and
- `min(band 15) - 21.0 = 0.2571673143 eV`.

The lower boundary lies `0.1658680268 eV` below the observed band-1 minimum. The frozen
window still selects 4--6 states per point with histogram `{4: 129, 5: 84, 6: 3}`; no
band 13--20 state enters it.

## Alternatives and attribution

The inherited `[-5.85, 19.02] eV` outer window remains dimensionally legal, but it has
only exactly rank 10 at 12 points. The two blocked `C6` localizations establish
optimizer nonconvergence for that target-space declaration, not that the zero-slack
points caused the failure. It is not selected for the broader-parent candidate because
the authenticated 20-band inventory now supports a controlled target-space redesign
with at least two excess dimensions everywhere.

Using all 20 calculated bands as the outer space is not selected. The factor-two parent
inventory was introduced to observe the available spectrum before choosing a window;
it was not a declaration that all 20 states belong to the target. No evidence currently
justifies admitting bands 15--20, whose energies extend to `30.2720123939 eV`.

`C6-B20-W21` is distinct from the unexecuted `C6-T1` proposal. They share the numeric
window, rank, frozen window, and projections, but `C6-T1` was defined on a 12-band
parent and could not observe the 228 admitted band-13/14 states. The `C6-T1`
authorization request remains ungranted and is not transferable.

## Optimizer and interface policy

The later
[`AiiDA-precise convergence adaptation`](aiida-precise-convergence-adaptation-decision.md)
supersedes the initially prepared hybrid optimizer tuple for this prospective route.
The current profile uses `dis_conv_tol = 2.0e-9` (dimensionless),
`dis_num_iter = 40000`, `num_iter = 40000`, `num_cg_steps = 200`,
`conv_tol = 2.0e-9 angstrom^2`, and `conv_window = 6`, derived exactly from the pinned
precise convergence protocol for the two-atom cell. These remain eligibility gates,
not evidence of a global minimum. No automatic iteration extension beyond 40000 is
allowed.

The existing 12-band NNKP, AMN, MMN, EIG, checkpoint, `u`, `u_dis`, and HR artifacts
are not inputs to this candidate. A fresh 20-band route requires distinct preprocessing,
conversion, and localization occurrences, each with exact bounded authorization. The
failed localization outputs remain diagnostic evidence only.

## Stop rule

If a future `C6-B20-W21` localization fails provider eligibility, do not automatically
extend either optimizer budget, change optimizer controls, escalate to `C6-B30`, or
escalate the construction mesh. Return target rank, window, projections, and numerical
trajectory to a separate scientific review. If it becomes provider-eligible, full
operator characterization and the revealed 408-point development comparison still
precede the unobserved 402-point confirmation set.
