# `ksdft2effmass.periodic1d.admissible_sets.calculate`

## Purpose and status

Implemented M3 producer module. It composes the M2 baseline, constructs analytic
squared-loss quadratics over the continuous shift/splitting rectangle for the frozen
finite angle family, retains a common witness, and derives a bounded separation
certificate.

## Public contract

- [`Periodic1DConstrainedAdmissibleSetCalculator`](Periodic1DConstrainedAdmissibleSetCalculator/index.md)

Private methods own decisive mathematics: normalized spectral/operator losses,
quadratic construction, axis extrema, domain minima, feasible-angle sets, splitting-axis
separation, candidate rotations, and evaluation-role reconstruction.

## Ownership and dependencies

The calculator owns M3 orchestration, continuous-domain policy, and finite-angle policy. M2 owns baseline
alignment data; reusable Fourier/interpolation machinery stays with its domain owner.
No external execution or file I/O occurs.

## Mapping and evidence

Source: `python/src/ksdft2effmass/periodic1d/admissible_sets/calculate.py`.
See [scientific](../scientific.md), [implementation](../implementation.md), and
[testing](../testing.md).

## Limitations

The certificate applies only to the declared two-parameter, nine-angle family and
unclipped quadratic geometry.
