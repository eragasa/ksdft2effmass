# Exploratory threshold and resolution design

## Status

This note records the disclosed exploratory calculation used to select prospective
spectral/operator thresholds and a separation resolution for the isotropic two-
dimensional hopping-shell hierarchy. It is design provenance, not an experiment run,
certificate, retained result, scientific validation, or publication evidence.

The calculation used only the already selected 15-by-15 objective-construction data,
projected block target, common coefficient box, support prefixes, spectral weights, and
maximal-space metric. It did not calculate or inspect evaluation, withheld, or locality
diagnostics and did not execute an external calculator.

Threshold refinement and resolution selection were intentionally outcome-informed. The
operator inspected channel minima, cross-channel center values, and one exploratory
support-gap construction. The prospective controls are therefore pedagogical design
choices, not blind, physically calibrated, probabilistic, or independently validated.
The previously selected parent, projection, energy shift, box, weights, supports, and
sample roles were not changed after this inspection.

## Software and methods

The local calculation ran on 2026-10-14 with CPython 3.14.6 and NumPy 2.5.1. Exact
bound owner revisions were:

```text
projectkoios-optimization@d9a82252faa1b41d82cce11149329aa91b84dff0
projectkoios-physkit@62ee89870db74b7b8b374c42add72701fd95d3a4
```

Quadratics were constructed with
`ComplexAffineResidualQuadraticConstructorFactory` and method
`NUMPY_DENSE`. Box minima used `BoxQuadraticMinimizerFactory`, method
`NUMPY_DENSE`, default absolute/relative tolerance `(1e-12, 1e-10)`, and default
maximum iteration count 10,000. The requested decimal box half-width
`0.11426128163399648` has binary64 value `0.11426128163399649`.

All returned minima were strictly interior, required one KKT-check iteration, no active-
set changes, no linear solve, and had maximum KKT ratio zero. Thus the box owner verified
that the unconstrained centers were admitted; the study does not exercise an active
bound.

An independent NumPy weighted least-squares reconstruction agreed with owner coordinates
to `2.0816681711721685e-17` and squared losses to
`2.0328790734103208e-20`. This is correlated binary64 cross-checking, not an exact or
interval proof.

## Observed objective-construction minima

The following are root-mean-square losses. They are exploratory design observations and
must not be described as confirmatory experiment results.

| Active coefficients | Support class | Spectral minimum | Operator minimum |
|---:|---|---:|---:|
| 1 | `support-r2-000` | `0.05330494928048669` | `0.0038328296805272056` |
| 2 | `support-r2-001` | `0.0059074846105551596` | `0.0004293205786068524` |
| 3 | `support-r2-002` | `0.005769302512937918` | `0.00041184352450933045` |
| 4 | `support-r2-004` | `0.0011269560991274724` | `0.00008474103096125427` |
| 6 | `support-r2-008` | `0.001002797369116659` | `0.00007308140801034696` |
| 12 | `support-r2-018` | `0.00005271308290732413` | `0.000004011318625092732` |
| 27 | `support-r2-050` | `0.0000004617259535546291` | `0.00000003207160615573846` |
| 36 | `support-r2-098` | `2.876764717979063e-15` | `5.963807241191617e-20` |

The complete-class floors are binary64 reconstruction values, not claims of exact zero.

## Selected prospective controls

The selected exact decimal controls are:

```text
spectral RMS threshold = 0.001004
operator RMS threshold = 0.00007310
separation resolution  = 0.000005
```

The threshold pair places both controls just above their respective six-coordinate
minima and below the four-coordinate minima. This makes the six-coordinate class the
first class for which both individual channels are nonempty in the exploratory
binary64 geometry. This was deliberately selected for a bounded hierarchy demonstration
and is not a physical adequacy criterion.

At the 12-coordinate class, the target truncated to the active prefix had exploratory
spectral/operator RMS losses `0.0000538644837389751` and
`0.000004011318625092732`, both below the selected thresholds. It is therefore a
prospective common-witness case, subject to later independent reconstruction.

## Exploratory six-coordinate gap

After threshold selection, a direction was formed from the spectral-to-operator center
difference under the selected complete-block metric. Full-ellipsoid support in that
direction gave:

| Diagnostic | Value |
|---|---:|
| Center metric distance | `0.000013565224899277994` |
| Directional lower-bound candidate | `0.000007872658587804812` |
| Constructive support-point distance | `0.000007991266901875964` |
| Largest absolute spectral support coordinate | `0.02855727268582518` |
| Largest absolute operator support coordinate | `0.02856295881409328` |
| Box half-width | `0.11426128163399649` |

Both support points are well inside the common box, so this particular exploratory
full-ellipsoid premise is not box clipped. A separate direct analytic ellipsoid-support
calculation agreed with the owner support points to at most
`6.776263578034403e-21`.

The candidate lower bound exceeds the selected resolution `0.000005`. This observation
motivates the resolution but is not a separation certificate: no outward-rounded or
exact enclosure has yet been selected, and the future independent verifier must
reconstruct every premise conservatively.

## Prospective hierarchy shape and interpretation

If later conservative evidence reproduces this design geometry, the intended bounded
pattern is:

1. early classes excluded by direct channel emptiness;
2. the six-coordinate class individually feasible in both channels but separated above
   resolution; and
3. the 12-coordinate and later classes containing an explicit common point.

This is an outcome-informed pedagogical hierarchy. Freezing these controls before a
later retained run prevents further tuning, but does not turn that run into a blind
scientific test or material validation.

## Remaining gates

Before an immutable version or retained execution, the experiment still requires:

- active-quadratic reconstruction and acceptance tolerances;
- reviewed intersection-witness and strict-separation methods;
- conservative arithmetic and rounding policy;
- strict schemas and canonical serialization;
- exact method identities in the input;
- an independent verifier; and
- evidence retention, failure, and interpretation policy.
