# Lower-energy frozen-window construction decision

## Problem

The blocked conduction-frozen rank-10 construction freezes all eight conduction bands
and no valence bands at every source k point. Rank 10 therefore has only two remaining
dimensions with which to represent four valence states. This ordering protects the
highest sampled states while allowing the chemically bonding and valence subspace to
vary, and it produced a difficult, gauge-sensitive localization problem.

Further iteration and optimizer combinations have stopped. The prospective
Wannierisation policy is now `2.0e-9 angstrom^2`, window 6 for the exact two-atom cell.
A successor must change the scientific construction rather than relabel the blocked
operator.

## Selected construction

Retain the rank-10 `sp3s*` route, all 12 parent bands, the outer window
`[-5.85, 19.02] eV`, the `4 x 4 x 4` Gamma-origin full mesh, and the separate `Si:sp3`
and `Si:l=0:r=2` projections. Replace the conduction-only frozen interval with the
lower-energy interval

```text
dis_froz_min = -5.85 eV
dis_froz_max = 8.00 eV
```

The energy zero remains the native QE Kohn--Sham reference.

On the authenticated 64-point EIG inventory this interval:

- freezes all four valence bands at every k point;
- freezes zero, one, or two sampled conduction states depending on k;
- produces 4--6 frozen states at every k point, below rank 10;
- freezes 304 of the 768 sampled band states;
- has 45 k points with at least one frozen conduction state and 3 with two;
- excludes bands 7--12 everywhere;
- has maximum included energy `7.937879250936 eV` and minimum excluded energy
  `8.420321216132 eV`, a `0.482441965196 eV` source-mesh clearance around the declared
  threshold.

This protects the complete lower-energy bonding/valence manifold and sampled
conduction-edge states while leaving four to six rank dimensions for localization and
higher-energy conduction representation. The threshold is a calculation-owned starting
coordinate for the target observable domain, not a claim that every unsampled state
below 8 eV is already qualified.

## Alternatives not selected

- A rank-8 `sp3` construction is strong silicon literature precedent, but it changes
  rank, projection inventory, and the intended higher-rank `sp3s*` route simultaneously.
- A `6.5 eV` upper frozen boundary freezes no conduction state on this exact source mesh
  because the sampled band-5 minimum is `6.736696896102 eV`; it therefore does not
  protect a sampled conduction-edge state in this calculation's native energy reference.
- Retaining the all-conduction frozen interval would not address the demonstrated target
  imbalance.

## Optimizer and convergence coordinates

Use one fresh occurrence with:

- `precond = true`;
- `dis_mix_ratio = 0.2`;
- `dis_num_iter = 1000`;
- dimensionless `dis_conv_tol = 1.0e-10`, window 3;
- `num_cg_steps = 200`;
- `num_iter = 4000`;
- `conv_tol = 2.0e-9 angstrom^2`, window 6;
- native parabolic line search and default `trial_step = 2.0`; and
- no guiding centres, fixed step, checkpoint continuation, or convergence noise.

These are fixed production-practice coordinates for this new construction, not another
optimizer search.

## Prospective disposition

Both native convergence messages remain mandatory. Convergence makes the operator only
eligible for construction- and withheld-mesh tests of spectra, valley identity and
location, edge energies, derivatives, curvature/effective masses, and locality/tail
sensitivity. It does not establish scientific acceptance.

Failure under these fixed coordinates ends this rank-10 projection/window candidate.
A successor would require a separately reviewed rank/projection construction, with the
rank-8 `sp3` literature route as the leading alternative.

This decision authorizes exact preflight preparation only. Calculator execution remains
a separate bounded action.
