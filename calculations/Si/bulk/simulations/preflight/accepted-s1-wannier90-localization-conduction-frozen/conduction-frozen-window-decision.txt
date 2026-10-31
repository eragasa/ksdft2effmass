# Conduction-frozen localization decision

## Purpose

The conditioned and damped rank-10 occurrence converged Wannierisation but its
10-dimensional subspace continued to drift within the 12-band outer space after 1000
disentanglement iterations. The next candidate tests a conduction-owned target space
rather than weakening the dimensionless fractional convergence tolerance.

## Exact frozen window

On the authenticated 64-point Davidson QEXSD mesh, in the native QE Kohn–Sham energy
reference:

- the maximum of band 4 is `5.9831191281189176 eV`;
- the minimum of band 5 is `6.736696896102439 eV`; and
- the maximum of band 12 is `19.008744989627342 eV`.

The clean sampled valence–conduction separation permits the frozen interval
`[6.00, 19.02] eV`. It excludes all four valence bands and contains all eight
conduction bands at every sampled k point. Because the retained rank is 10, the eight
conduction states are required exactly and the remaining two dimensions are selected
from the four valence states by disentanglement.

The outer window remains `[-5.85, 19.02] eV`; no band is added or removed from the
12-band parent space. The structure, reciprocal grid, projections, NNKP topology, and
AMN/MMN/EIG bytes remain unchanged.

## Optimization controls

Keep the previously declared convergence controls so that the frozen window is the
only new scientific variable:

- `precond = .true.`;
- `num_iter = 500`;
- absolute Wannierisation `conv_tol = 1.0e-10 angstrom^2`, window 3;
- `dis_mix_ratio = 0.2`;
- `dis_num_iter = 1000`; and
- dimensionless fractional `dis_conv_tol = 1.0e-10`, window 3.

The occurrence starts fresh and does not consume either blocked checkpoint.

## Interpretation boundary

This candidate prioritizes exact representation of the eight sampled conduction bands.
It does not retain the complete four-band valence manifold and therefore cannot by
itself support a claim of full valence-band fidelity. A successful internal convergence
result would still require interpolation and effective-mass sensitivity checks before
operator acceptance.

This decision authorizes exact preflight preparation only. Calculator execution remains
a separate bounded action.
