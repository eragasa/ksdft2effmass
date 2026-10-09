# Scientific reasoning and claim boundary

## What the retained study asks

The standalone campaign probes how a finite set of deterministic smooth periodic initial
gauges affects local Wannier90 localization trajectories while varying numerical
configuration and optimizer arm. The starts are design controls. They are not a random
sample, a probability distribution over gauges, or an exhaustive search of the unitary
gauge manifold.

The spread symbols \(\Omega_I\), \(\Omega_D\), and \(\Omega_{OD}\) follow the
maximally-localized Wannier-function decomposition reviewed by Marzari, Mostofi, Yates,
Souza, and Vanderbilt [^marzari2012]. That citation supports terminology and the
mathematical decomposition only. It does not qualify this retained campaign, its
thresholds, or its basin labels as a scientific oracle.

## What the observations say

The retained compact result records 256 completed initial processes, 120 continuation
attempts, 196 effective native-converged endpoints, and 60 stopped nonconverged endpoints.
Its exact disposition is **does not support the frozen standalone finite-sequence
criteria**.

This is a bounded negative statement about one finite design. It does not prove that no
convergence limit exists. A native convergence statement identifies a reported local
termination outcome; it does not prove a global optimum. Likewise, an observed basin is
an operational quotient under retained spread, periodic-center, symmetry, permutation,
and density thresholds. It is not proof of a distinct mathematical stationary point.

The result also records that the planned pre-execution basin-tolerance control lacks a
retained record. Post-hoc exact-equivalence and threshold-sensitivity controls are useful
diagnostics but do not retroactively establish protocol compliance.

## Error separation

The campaign must not collapse these distinct sources of discrepancy:

- parent-model and finite-basis error;
- reciprocal-mesh sampling and plane-wave cutoff error;
- auxiliary embedding and finite-supercell postprocessing error;
- retained-subspace and initial-gauge choices;
- local localization trajectory and stopping behavior;
- interpolation or hopping truncation error; and
- basin comparison and threshold sensitivity.

Endpoint arithmetic and checksum identity do not estimate any of those error classes.

## Unsupported conclusions

Passing portable verification does not authenticate the external native run tree, rerun
Quantum ESPRESSO or Wannier90, prove local or global optimizer convergence, establish
population inference, quantify physical uncertainty, validate a material-property
prediction, establish scientific adequacy, or record acceptance.

[^marzari2012]: N. Marzari, A. A. Mostofi, J. R. Yates, I. Souza, and D. Vanderbilt,
    “Maximally localized Wannier functions: Theory and applications,” *Reviews of Modern
    Physics* **84**, 1419–1475 (2012),
    [doi:10.1103/RevModPhys.84.1419](https://doi.org/10.1103/RevModPhys.84.1419).
