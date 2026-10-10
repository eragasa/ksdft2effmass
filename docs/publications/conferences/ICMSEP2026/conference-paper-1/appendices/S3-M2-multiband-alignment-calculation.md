# Supplementary Appendix S3 — M2 multiband alignment and gauge-resolved locality

## S3.1 Identity and boundary

M2 is the prospectively frozen local synthetic calculation
`icmsep2026.paper1.periodic1d.multiband-alignment.v1`, retained under
`calculations/ICMSEP2026/conference/paper_1/multiband-alignment/`. It composes
maintained frame, alignment, projection, Fourier, truncation, interpolation,
and band-error Actions. The retained verifier reconstructs the finite protocol
without calling the producer.

This is bounded numerical evidence for one constructed rank-two example. It is
not material validation, uncertainty quantification, continuum convergence, a
general nonconvex alignment solution, or scientific acceptance. Exact
pointwise Procrustes recovery remains distinct from the family containing one
global unitary for the whole path.

## S3.2 Parent and controls

The parent is

\[
H(k)=T_0+e^{2\pi i k}T_1+e^{-2\pi i k}T_1^\dagger,
\]

with

\[
T_0=\begin{pmatrix}
-1.20&0.06&0&0\\0.06&-0.35&0&0\\
0&0&1.00&0.04\\0&0&0.04&1.75
\end{pmatrix},\quad
T_1=\begin{pmatrix}
0.15&0&0&0\\0&-0.10&0&0\\
0.12&0&0.05&0\\0&0.10&0&-0.04
\end{pmatrix}.
\]

The lowest two states form the retained group. Training uses a 64-point
centered half-open mesh; evaluation uses 257 disjoint staggered points. The
minimum external gap is `1.0566461211497047`, above the frozen `0.5` bound.
The minimum neighboring/closure overlap singular value is
`0.9999828868735376`, above the frozen `0.8` threshold.

## S3.3 Attack and alignment channels

The transported frame is attacked by

\[
A(k)=\begin{pmatrix}\cos\theta(k)&-\sin\theta(k)\\
\sin\theta(k)&\cos\theta(k)\end{pmatrix},\qquad
\theta(k)=0.30+0.65\sin(2\pi k)+0.30\sin(4\pi k).
\]

The projector defect is `3.24e-16`, although the maximum frame defect is
`1.5056`. Pointwise Procrustes alignment recovers the inverse attack with
maximum rotation defect `6.77e-16` and aligned-frame defect `7.00e-16`.
The separately constrained one-global-unitary family leaves maximum frame
defect `1.1309`. This diagnoses that declared family rather than claiming a
failed search over arbitrary smooth gauges.

The attacked projected operator differs from the transported representation by
`0.9972` in maximum Frobenius norm. Pointwise alignment reduces the defect to
`9.83e-16`; the global-unitary channel leaves `0.7443`. Projectors and unordered
spectra are invariant channels; these matrix defects require the declared
frame identification.

## S3.4 Complete transforms and finite ranges

Complete transformed paths reconstruct within `6.76e-16` (transported),
`1.14e-15` (attacked), and `6.77e-16` (pointwise aligned). The largest
block-Hermiticity defect is `4.50e-17`.

| range | transported omitted norm | attacked omitted norm | transported withheld max error | attacked withheld max error | aligned withheld max error |
|---:|---:|---:|---:|---:|---:|
| 0 | `2.54e-1` | `5.23e-1` | `2.98e-1` | `4.45e-1` | `2.98e-1` |
| 1 | `1.98e-5` | `1.85e-1` | `2.76e-5` | `1.49e-1` | `2.76e-5` |
| 4 | `1.75e-9` | `8.28e-3` | `2.49e-9` | `6.43e-3` | `2.49e-9` |
| 8 | `1.63e-14` | `5.65e-5` | `1.15e-14` | `7.04e-5` | `1.15e-14` |

The known periodic attack redistributes invariant spectral information into a
longer hopping tail. Withheld values evaluate only fixed models; they cannot
change controls or figure selection.

![M2 summary](../../../../../../../calculations/ICMSEP2026/conference/paper_1/multiband-alignment/multiband-alignment-summary.png)

## S3.5 Verification and provenance

Independent reconstruction gives maximum dimensionless defect `1.33e-15` and
maximum energy-channel defect `7.43e-15`, below the frozen `1e-11` tolerance.
The package retains the pre-execution protocol freeze, result, verification,
figure data, figure, report, software record, source manifest, and checksums.
It used Python 3.14.6, NumPy 2.5.1, SciPy 1.18.0, Matplotlib 3.11.1, and
`ksdft2effmass 0.1.0.dev0`. No external calculator was invoked.
