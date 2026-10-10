# Controlled isolated-band calculation report

## Status

The frozen local synthetic calculation completed and the retained independent verifier
passed. This report describes finite numerical behavior under `input.json` and
`protocol.md`. It does not establish material validity, uncertainty quantification,
continuum convergence outside the declared sequences, transferability, or scientific
acceptance for a later application.

The calculation did not invoke an external electronic-structure calculator, scheduler,
or remote resource.

## Frozen parent

The dimensionless benchmark was

$$
H(k)=-\frac{d^2}{dx^2}+0.5\cos x,
\qquad a=2\pi,\quad G=1,\quad E_G=1.
$$

The finite represented reference used plane-wave cutoff 15. Production training and
withheld targets used plane-wave cutoff 11. Three ordered bands were compared at the
five frozen parent momenta.

## Parent-representation observations

The maximum absolute plane-wave errors relative to the cutoff-15 represented reference
were:

| cutoff | maximum absolute error ($E_G$) |
|---:|---:|
| 3 | $1.2107868154753731\times10^{-5}$ |
| 5 | $5.311306949806749\times10^{-13}$ |
| 7 | $6.483702463810914\times10^{-14}$ |
| 9 | $8.038014698286133\times10^{-14}$ |
| 11 | $8.448797217397441\times10^{-14}$ |

The cutoff-7 through cutoff-11 values fluctuate at the scale of the represented
calculation rather than forming a strictly monotone sequence. They are therefore
reported as observed finite-representation discrepancies, not as an exact continuum
error estimate.

The centered finite-difference observations were:

| periodic grid points | maximum absolute error ($E_G$) |
|---:|---:|
| 31 | $1.75327419749558\times10^{-2}$ |
| 63 | $4.2534045602447\times10^{-3}$ |
| 127 | $1.0471636947908536\times10^{-3}$ |
| 255 | $2.597716946719508\times10^{-4}$ |

This declared sequence decreases consistently with the expected behavior of the
centered second-order discretization. The observation does not certify other grids or
replace a continuum error bound.

## Complete hopping transform

The complete 64-point scalar Fourier transform reconstructed its training samples with
maximum absolute error
$4.166137705498387\times10^{-17}E_G$. The maximum modular Hermiticity defect was
$2.0907097393389345\times10^{-18}E_G$.

The complete training mesh and frozen 257-point staggered withheld mesh were exactly
disjoint under the retained coordinate rule.

## Finite-range reduction observations

| range | training max error ($E_G$) | withheld max error ($E_G$) | direct/mediated coefficient defect ($E_G$) | omitted-block norm ($E_G$) |
|---:|---:|---:|---:|---:|
| 0 | $4.6235761234918529\times10^{-2}$ | $4.6235757038421116\times10^{-2}$ | $4.163336342344337\times10^{-17}$ | $3.0304371873761445\times10^{-2}$ |
| 1 | $3.4907261091598474\times10^{-3}$ | $3.4907249362493321\times10^{-3}$ | $3.4428416195293114\times10^{-17}$ | $2.1876792982638178\times10^{-3}$ |
| 2 | $4.1809353420569836\times10^{-4}$ | $4.180932306706471\times10^{-4}$ | $5.9106172770672265\times10^{-17}$ | $2.5574448521400637\times10^{-4}$ |
| 3 | $6.0054872740911147\times10^{-5}$ | $6.0054797139896116\times10^{-5}$ | $7.3812041609811699\times10^{-17}$ | $3.618563479657382\times10^{-5}$ |
| 4 | $9.5136496848433061\times10^{-6}$ | $9.5136312846764992\times10^{-6}$ | $6.0865104451078002\times10^{-17}$ | $5.6738480443118724\times10^{-6}$ |
| 6 | $2.8158443984849235\times10^{-7}$ | $2.8158339336961657\times10^{-7}$ | $4.755787418686525\times10^{-17}$ | $1.6575039069379447\times10^{-7}$ |
| 8 | $9.4653549650991486\times10^{-9}$ | $9.4652957589869136\times10^{-9}$ | $6.471583497827925\times10^{-17}$ | $5.5272060152212862\times10^{-9}$ |

Training and withheld errors decrease over the frozen range sequence and remain close
without being identical. Because withheld points were not used in either route, their
values remain evaluation-only.

Across all frozen ranges, the largest direct-versus-mediated coefficient defect was
$7.38120416098117\times10^{-17}E_G$, and the largest sampled maximum defect was
$1.564917933602745\times10^{-16}E_G$. The largest Parseval absolute residual was
$6.938893903907228\times10^{-18}E_G^2$. The largest imaginary residual among the
reported band-shape diagnostics was $9.479926314907974\times10^{-16}E_G$, below the
frozen $10^{-12}E_G$ numerical-consistency tolerance.

No hopping range is designated scientifically acceptable by this package. The table
makes the range-versus-error tradeoff visible but does not turn the frozen tolerances
into a model-selection rule.

## Independent retained verification

`verify_result.py` does not import `run.py`. It strictly decodes the retained input and
result identities and independently reconstructs the plane-wave and finite-difference
matrices, spectra, Fourier coefficients, truncations, direct least-squares fits,
route defects, Hermiticity, Parseval quantities, and band-shape diagnostics.

The retained verification passed with:

- maximum spectral absolute reconstruction defect: $0$;
- maximum hopping absolute reconstruction defect:
  $4.781392881215698\times10^{-17}$; and
- maximum diagnostic absolute reconstruction defect:
  $2.731148640577885\times10^{-14}$.

All were below the frozen $10^{-12}$ absolute verification tolerance. These
reconstruction defects are software-consistency observations and are not physical
uncertainty estimates.

## Figure and retained identities

`isolated-band-summary.png` was generated by `run.py` from the same typed result that
was serialized to `result.json`. `figure-data.csv` retains the tabular finite-range
values used in panel (d). The result schema is
`ksdft2effmass.periodic1d.isolated-band-calculation-result.v1` and is separate from the
historical Appendix G result identity and from the parent direct admissible-set package.

The historical Mathieu, common-low-mode, weak-potential, and stress channels were not
recalculated here and are not claims of this retained result.
