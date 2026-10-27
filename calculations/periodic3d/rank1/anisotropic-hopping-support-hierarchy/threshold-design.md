# Exploratory threshold-design note

## Status

This note records the disclosed exploratory calculation that informed the candidate
thresholds in [protocol.md](protocol.md). It is **design provenance**, not a retained
experiment run, confirmatory result, certificate, or evidence package. The controls may
still change during review; if they are accepted, the later immutable version must bind
these exploratory values before any sealed evaluation.

The local calculation ran at `2026-10-14T11:30:47Z` with CPython `3.14.6`, NumPy
`2.5.1`, and SciPy `1.18.0` from `python/.venv`. It used direct binary64 trigonometric
sampling of the proposed `9 x 11 x 13` objective-construction mesh. It did not use the
required future
exact-rational verifier.

## Observed design quantities

For each active prefix of lengths 3, 6, 7, and 10, weighted least squares gave the
following exploratory channel minima:

| Active coefficients | Support class | Spectral minimum RMS | Operator minimum RMS |
|---:|---|---:|---:|
| 3 | `axial-nearest` | `0.09180300266023853` | `0.016253239235442616` |
| 6 | `face-diagonal` | `0.03696347706410148` | `0.0065509804028314154` |
| 7 | `body-diagonal` | `0.029713840278243368` | `0.005258950006967289` |
| 10 | `axis-second-neighbour` | approximately `1.8e-15` | `0.0` |

At the exact target truncated to each active prefix, the exploratory RMS pairs were:

| Active coefficients | Spectral RMS | Operator RMS |
|---:|---:|---:|
| 3 | `0.09210801658243434` | `0.016253239235442616` |
| 6 | `0.0370579413300982` | `0.0065509804028314154` |
| 7 | `0.02974911369478089` | `0.005258950006967289` |
| 10 | `0.0` | `0.0` |

These observations motivated the proposed exact-decimal controls

```text
spectral RMS threshold = 0.03697
operator RMS threshold = 0.006555
separation resolution  = 0.00005
```

A binary64 support calculation in the metric-weighted center-difference direction for
the six-coordinate class produced an exploratory lower-bound candidate of approximately
`0.00011314`. This suggested, but did not certify, a design containing an early empty
class, a nonempty separated class, and a later common-witness class. The note does not
promote those expected states to results. Exact rational quadratic reconstruction,
conservative square-root enclosures, box containment, strict schemas, independent
verification, and a sealed run are all still required.

## Interpretation boundary

The threshold pair was intentionally selected after inspecting synthetic channel
geometry. It is pedagogical and must never be described as blind, physically calibrated,
probabilistic, or inferred from silicon. Evaluation-mesh and locality outputs were not
computed or used for this threshold choice.
