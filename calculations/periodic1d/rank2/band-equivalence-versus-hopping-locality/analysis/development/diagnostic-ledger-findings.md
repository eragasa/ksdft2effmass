# Diagnostic-ledger findings

## Status

These are derived analyses of the existing sampled calculations. Provenance belongs to
the source calculations; this narrative, the derived tables, and the figures have no
separate provenance identity. The analysis does not provide a continuous-amplitude or
continuous-parent-homotopy certificate. Cutoff statements minimize over the dense
integer development inventory $R_c=0,\ldots,16$; they do not establish behavior beyond
the declared cap.

The packaged analysis contains 14 source tables, 77,191 long-form diagnostic rows, 110
catalogued quantities, and 660 sampled cutoff decisions across five parent scales, 33
amplitudes, and four error targets.

## Subspace, frame, and sewing diagnostics

Across the sampled parent scales from `rho = 0` to `rho = 1`:

- the sampled external isolation gap decreases from `1.343658 E_{\mathrm{ref}}` to `1.056646 E_{\mathrm{ref}}` and remains
  above the declared sampled gate;
- the minimum neighbor-or-closure overlap singular value decreases only from `1` to
  `0.9999989292`;
- the maximum neighboring Procrustes residual grows from zero to about `1.831e-3`;
- the ordered closure-holonomy phase set grows from numerical zero to approximately
  `(0.014181, 0.018807)` radians;
- transport-unitarity, closure-holonomy-unitarity, frame-orthonormality, and periodic-
  closure discrepancies remain at binary64 scale, all below about `3.4e-15` in the sampled
  summary.

The closure phases are Wilson-loop-like sewing diagnostics. Their smooth growth with
parent hopping is not interpreted as a topological invariant or as a cause of hopping-
range inflation.

## Hamiltonian and spectral consequence channels

At the fully dispersive endpoint `(rho, a) = (1, pi/4)`, the first sampled passing ranges
are:

| Target | Reference bands | Reference Hamiltonian | Comparison bands | Comparison Hamiltonian | Band inflation | Hamiltonian inflation |
|---:|---:|---:|---:|---:|---:|---:|
| `1e-6` | 3 | 2 | 8 | 8 | 5 | 6 |
| `1e-8` | 4 | 4 | 10 | 10 | 6 | 6 |
| `1e-10` | 6 | 5 | 12 | 12 | 6 | 7 |
| `1e-12` | 7 | 7 | 14 | 14 | 7 | 7 |

Thus endpoint range inflation persists under the separately reported Hamiltonian
criterion. The two criteria agree exactly at the endpoint for `1e-8` and `1e-12`; their
reference decisions differ by one integer cutoff at `1e-6` and `1e-10`. Rank-normalized
Frobenius and maximum-band normalizations answer different questions, so neither
criterion should be called universally stricter.

Across all 165 sampled `(rho, a)` points:

- at `1e-6`, the comparison Hamiltonian and band cutoffs agree at 153 points;
- at `1e-8`, they agree at 158 points;
- at `1e-10`, they agree at 153 points;
- at `1e-12`, they agree at 155 points;
- the reference decisions agree at all 165 points for `1e-8` and `1e-12`;
- most comparison differences occur in the flat parent at isolated sampled amplitudes,
  where eigenvalue cancellation can make band error smaller than matrix error;
- sampled reference-versus-comparison inflation is never negative for either the band or
  Hamiltonian criterion on the present inventory.

These counts support presenting spectral and Hamiltonian range requirements separately.
They do not justify replacing one with the other or combining their thresholds.

## Numerical identities

The maximum absolute discrepancies in the rank-normalized truncation Parseval identity are
approximately

- `8.33e-17` for the reference; and
- `1.11e-16` for the comparison.

All sampled maximum band errors satisfy their Frobenius perturbation bounds. Depending on
cutoff and channel, the ratio

```text
maximum band error / (sqrt(2) * maximum normalized Hamiltonian error)
```

ranges from about `0.0087` to `0.9984`. Values near one show a nearly saturated bound;
small values expose matrix perturbations that are weakly expressed in the ordered
spectrum.

The maximum off-node interpolation errors over all sampled parents and amplitudes are
about

- `2.46e-14` for the normalized Hamiltonian channel; and
- `2.35e-14` for the band channel.

They are below every displayed range-accuracy target and become relevant only near the
binary64-scale floor.

## Candidate scientific emphasis

The complete ledger suggests three potentially useful observations for later review:

1. **Range inflation is robust to the reported error representation.** The endpoint and
   nearly all sampled controls give the same first passing cutoff under matrix and band
   criteria.
2. **Spectral agreement can hide matrix error.** Isolated flat-parent cases require a
   larger Hamiltonian cutoff than band cutoff, and the perturbation-bound ratio can be
   far below one.
3. **Frame transport remains well conditioned while its holonomy changes smoothly.**
   This separates range inflation from an obvious gap, rank, or sewing failure.

These are exploratory observations to guide figures and protocol freeze. They are not
novelty, causality, or validation claims.
