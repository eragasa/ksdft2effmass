# Accepted-S1 `C6-T1` full-parent-band outer-window preflight

This directory retains the authorized no-execution preparation for the first `C6-T1`
target-space candidate. Relative to the blocked 4000-step `C6` occurrence, the exact
native input changes only the outer-window envelope:

```text
dis_win_min = -5.85  ->  -6.0 eV
dis_win_max = 19.02  ->  21.0 eV
```

A bytewise diff confirms that these are the only WIN changes. The source window selected
12 bands at 142 points, 11 at 62, and the rank-minimum ten at 12. The revised window
selects all 12 authenticated parent bands at all 216 construction points. It encloses the
observed EIG range `[-5.8341319732, 20.803605038466] eV` with finite lower and upper
guard margins of approximately `0.165868` and `0.196395 eV`.

The rank, frozen window, projections, mesh, source order, energy reference, tolerances,
mixing, preconditioner, CG interval, line-search defaults, iteration budgets, and
NNKP/EIG/AMN/MMN bytes remain unchanged. The occurrence starts fresh and consumes no
checkpoint or failed localization output. No proposed occurrence root was created and no
calculator was invoked.

`C6-T1` is a target-space candidate, not a continuation of the one-variable mesh test.
Passing provider gates would make it eligible only for evaluation against the revealed
408-point development evidence; it would not establish scientific adequacy or authorize
prospective confirmation.

## Proposed occurrence

- root:
  `/Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier90-localization-c6-t1-full-parent-outer-dis4000-v1`
- command: `wannier90.x silicon`
- executable SHA-256:
  `c826f817f807cf069e16d6e529a52ddc15d2f677101065908bcb2030d7f7d1dd`
- one process, one invocation, zero retries
- timeout: 600 seconds
- retained-byte ceiling: 64 MiB

Eligibility requires return code zero, native completion, converged disentanglement,
converged Wannierisation, no maximum-iteration warning, declared HR and unitary outputs,
unitary/isometry residuals at most `1e-8`, k-point agreement within `1e-10`, and
Hamiltonian Hermiticity residual at most `1e-8 eV`.

If `C6-T1` fails provider eligibility, automatic optimizer tuning stops. Rank,
parent-band inventory, frozen window, and projections return to separate review.

## Identities

| Artifact | SHA-256 |
|---|---|
| prepared `silicon.win` | `54924bd20f4257ae59bd3b8d059cc5c4b07122ecda0e58bc2fd09ef6fdf6b489` |
| localization input manifest | `5f4dc7f5cbfecccfe81819a0876601fbadc257fb7c845ceece1450ec6599de92` |
| input transformation | `4150b33a85f1debac9e55277d98cdb24876003c6b7a22d1c60570c5c7822e544` |
| target-space analysis | `4a959801ea884cce9a9fb77f5446b202e0b1ff2164b482822a03e128962766a7` |
| campaign preflight | `8af62f67ebd6c9fafecd0aa300d49df5faef9aa278b3d033e42cc753066966f0` |
| authorization request | `5b2af06ad2b61ac8833ee05a4b59ae18ec9f38292f31b0e56eb789ab4d8c545d` |
| target-space decision | `9162165b70acf163c6af8e495c1714cae0f78bee1a8d96b3571c9268c43c475e` |
| amended research protocol | `d60b773b996e5c24b8333c0e4e919860b2dc8164504d581ac91ccfa208a59cbc` |

## Authorization boundary

Status: **authorization required**.

The operator authorized preparation only. The request retains
`authorization_granted: false`. `wannier90.x`, any retry, optimizer tuning, `C8`, `C12`,
direct-parent confirmation, component-operator construction, and Slater-Koster reduction
remain unauthorized.
