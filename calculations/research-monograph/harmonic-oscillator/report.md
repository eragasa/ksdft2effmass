# Appendix E harmonic-oscillator comparison report

## Status

This is a **calculated illustrative numerical result** for the parameter sweep
in `input.json`. The complete retained result is `result.json`; the verifier
passes against independent analytic oscillator states and finite-difference
identities. The result is numerical verification for this controlled model,
not scientific validation or semiconductor evidence.

## Calculated spatial-refinement behavior

At the widest retained box, $b=8$, the relative Frobenius discrepancies are:

| $K$ | $\eta=0.2$ | $\eta=0.1$ | $\eta=0.05$ | final observed order |
|---:|---:|---:|---:|---:|
| 2 | $4.01258\times10^{-3}$ | $1.00662\times10^{-3}$ | $2.51873\times10^{-4}$ | 1.99875 |
| 4 | $8.42743\times10^{-3}$ | $2.11905\times10^{-3}$ | $5.30527\times10^{-4}$ | 1.99792 |
| 6 | $1.33701\times10^{-2}$ | $3.37081\times10^{-3}$ | $8.44482\times10^{-4}$ | 1.99696 |

Here “final observed order” is
$\log_2[\delta_F(0.1)/\delta_F(0.05)]$. These values support the expected
second-order spatial-discretization behavior for this fixed-box sequence. They
do not establish a continuum limit uniformly in $K$.

## Calculated box and retained-space behavior

At the finest grid spacing, $\eta=0.05$, the relative discrepancies are:

| $b$ | $K=2$ | $K=4$ | $K=6$ |
|---:|---:|---:|---:|
| 4 | $2.21378\times10^{-4}$ | $1.10317\times10^{-3}$ | $2.43722\times10^{-2}$ |
| 6 | $2.51873\times10^{-4}$ | $5.30527\times10^{-4}$ | $8.44479\times10^{-4}$ |
| 8 | $2.51873\times10^{-4}$ | $5.30527\times10^{-4}$ | $8.44482\times10^{-4}$ |

For $K=4$ and $K=6$, increasing $b$ from 4 to 6 sharply reduces the boundary
contribution, after which the fixed-$\eta$ discretization contribution
predominates. The $K=2$ total discrepancy is slightly smaller at $b=4$ than at
$b=6$ or 8. This is not evidence that the narrower box is independently more
accurate: the total matrix difference combines boundary-domain and
spatial-discretization contributions, which can partially cancel.

Retaining more oscillator states makes the finite-box restriction more
demanding. At $b=4$, $\eta=0.05$, the $K=6$ sampled-state Gram deviation is
$3.76019\times10^{-3}$ and the relative operator discrepancy is
$2.43722\times10^{-2}$. At $b=8$ the corresponding Gram deviation is at
binary64 roundoff and the relative discrepancy is $8.44482\times10^{-4}$.

## Diagonal and off-diagonal information

For $b=8$, $\eta=0.05$, $K=6$, the absolute discrepancy components in units of
$\hbar\omega$ are

- diagonal: $6.15808\times10^{-3}$; and
- off-diagonal: $3.61501\times10^{-3}$.

Both components are retained because eigenvalue or diagonal information alone
would omit representation-induced mixing. The stored values satisfy
$D_F^2=D_{\mathrm{diag}}^2+D_{\mathrm{off}}^2$ within the verifier's binary64
tolerance.

## Map quality

Every Gram matrix in the retained sweep is positive definite. The largest
reported condition number is close to one for this parameter set: it is 1.00536
at $b=4$, $\eta=0.2$, $K=6$. The numerical injections satisfy $J^TJ=I_K$ at
binary64 roundoff. These diagnostics
establish that the selected maps are numerically usable for the declared sweep;
they do not establish physical equivalence between the finite-box and
real-line operators.

## Figures

`convergence-summary.png` shows the box, spatial, diagonal/off-diagonal, and
map-quality studies. `operator-difference-heatmap.png` shows the common-space
matrix difference at $b=8$, $\eta=0.05$, $K=6$. The figures visualize retained
JSON values and are not independent evidence.

## Limitations

The finite-box boundary effect, spatial-discretization effect, and dependence
on retained dimension remain distinct. The calculation does not compare
unmapped matrices, does not infer an infinite-space norm difference, and does
not validate a semiconductor or material model.
