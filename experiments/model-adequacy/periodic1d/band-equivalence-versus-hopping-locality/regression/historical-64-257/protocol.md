# Historical 64/257 regression controls

## Scope

These non-decisive controls reproduce a local synthetic historical calculation for
software regression only. They do not define a maintained experiment version or a
scientific acceptance protocol. The regression composes one exact
rank-two periodic one-dimensional multiband baseline, one compact two-parameter
candidate family, nine global real rotations, two threshold cases, one constructive
witness, and one bounded separation certificate. It invokes no external electronic-
structure or localization calculator.

## Parent and sample roles

The parent is the four-state, three-block toy hopping model identified in canonical
`input.json` when a run is retained. The composed baseline uses:

- 64 complete centered objective-construction coordinates;
- 257 disjoint staggered objective-evaluation coordinates;
- retained rank two;
- hopping ranges `0, 1, 2, 3, 4, 6, 8`;
- attack angle `0.3` with sine coefficients `0.65, 0.3`;
- external-gap lower bound `0.5` in the parent energy unit;
- overlap singular-value threshold `0.8`;
- coordinate tolerance `1e-14`;
- orthonormality, reconstruction, and Hermiticity tolerances `1e-12`; and
- parent verification tolerance `1e-11`.

Only objective-construction samples define quadratics, selected angles, witnesses,
certificate points, bounds, or dispositions. Objective-evaluation samples are used only
after those objects are fixed.

## Candidate and losses

For represented reference Hamiltonian `H(k)`, rank `r=2`, trace mean
`E_bar(k)=tr(H(k))/2`, energy scale `E_G=1`, and parameter
`p=(s, lambda)`, the candidate is

```text
H_p(k) = E_bar(k) I + s E_G I + lambda (H(k) - E_bar(k) I).
```

The closed parameter rectangle is `s in [-0.25, 0.25]` and
`lambda in [0.4, 1.2]`. The splitting scale is positive, preserving ordered-eigenvalue
association. Both spectral and represented-operator channels use Frobenius RMS per
sample and retained rank, divided by `E_G`. The represented-operator channel is the
minimum over the ordered angles
`[-1.2, -0.9, -0.6, -0.3, 0.0, 0.3, 0.6, 0.9, 1.2]` radians.
This finite family is not continuous or pointwise alignment optimization.

Raw positive objective weights are `1 / (N * r * E_G**2)` for each flattened complex
observation. They are not pre-square-rooted. The reviewed Optimization owner constructs
completed-square losses, evaluates them, minimizes them over the rectangle, computes
full-ellipsoid support, and performs ordered finite selection. KSD owns scientific
coordinates, labels, thresholds, containment, evidence, and interpretation.

## Threshold cases and certificate

The compatible case uses spectral/operator RMS thresholds `0.03/0.33` and the
prospective witness `(0.0, 1.0)`. Compatibility requires that retained constructive
witness.

The separated case uses thresholds `0.03/0.31`. The experiment filters operator
components by exact rectangle minimization, obtains the spectral support in direction
`(0, -1)`, obtains every feasible operator support in direction `(0, 1)`, and selects
the largest operator splitting coordinate with deterministic first-on-tie behavior.
The splitting-coordinate gap is a lower bound and the Euclidean distance between the
two feasible support points is an upper bound. Every support point must lie inside the
rectangle; otherwise the full-ellipsoid premise is invalid and execution fails. A
`certified-separated` disposition requires the lower bound to exceed resolution `0.05`.

## Evaluation and locality

At every retained witness or certificate point, the experiment reports spectral and
operator RMS losses on both sample roles. It also reports omitted-block L2 norms for
the reference, attacked, and selected aligned candidate at maximum ranges
`0, 1, 2, 3, 4, 6, 8`. These are finite-mesh, frame-dependent diagnostics, not general
locality or compressibility guarantees.

The finite Fourier convention is a negative-exponent forward transform with `1/N`
normalization and a positive-exponent unit-normalized inverse.

## Verification and failure

The independent typed verifier invokes only the composed parent verifier. It does not
call the constrained-set producer or Optimization solvers. It separately reconstructs
quadratics, rectangle minima, support points, finite choices, objective-evaluation
losses, finite Fourier blocks, locality norms, bounds, roles, and dispositions.
Dimensionless and parent-energy defects remain separate. Both must not exceed `1e-11`.

The regression test compares every retained numerical channel with the immutable
historical `result.json` within `1e-11`. It also authenticates the historical files
against `baseline.json`. This fixture cannot create a successful maintained-run or
scientific disposition.
