# Numerical contract

## Conventions

The direct calculation is nondimensional. The retained execution uses period
\(a=2\pi\), reciprocal vector \(G=1\), recoil energy \(E_G=1\), and the fixed
parent-model energy zero. Reduced momentum \(q=k/G\) lies in one centered reciprocal
period.

The potential is

\[
V(x)=V_0+V_1\cos(2\pi x/a),
\]

with \(V_0=0\) and \(V_1=0.5\) in the retained execution.

## Finite parent representations

For plane-wave cutoff \(M\), the represented basis has indices
\(n=-M,\ldots,M\). At reduced momentum \(q\), the kinetic diagonal is

\[
E_G(n+q)^2,
\]

and the first cosine harmonic contributes \(V_1/2\) on the first upper and lower
off-diagonals. The cutoff-15 spectrum is a larger finite reference, not the continuum
spectrum.

The second route uses a periodic uniform grid and a centered second-order finite
difference kinetic matrix. Bloch momentum enters through conjugate seam phases. The
sparse fibers are diagonalized only for the declared lowest spectral prefix; the sparse
route is not implicitly densified.

Refinement values are maximum absolute differences from the represented plane-wave
reference at the same authored momenta and ordered band indices. They are finite-
representation comparisons, not continuum error estimates.

## Complete finite transform

For the even \(N\)-point training mesh \(q_j=-1/2+j/N\), the complete representative
inventory is \(R=-N/2,\ldots,N/2-1\). For selected-band samples \(E(q_j)\),

\[
t_R=\frac{1}{N}\sum_j e^{-2\pi i Rq_j}E(q_j),
\qquad
\widetilde E(q)=\sum_R e^{2\pi iRq}t_R.
\]

The transform stores all representatives, complex hopping coefficients, reconstructed
training samples, the maximum reconstruction defect, and negation-closed Hermitian
pairing diagnostics. Signed complex zeros are canonicalized before serialization so the
same numerical value has stable typed bytes.

## Range routes and diagnostics

For maximum range \(r\), the mediated route keeps the complete symmetric inventory
\(-r,\ldots,r\) and discards the complement. The direct route independently solves the
positive-weight least-squares problem on the same representatives. The result records
rank, condition number, residuals, and coefficient and sampled defects between routes.

The omitted-block norm is

\[
\left(\sum_{|R|>r}|t_R|^2\right)^{1/2}.
\]

The finite Parseval check compares the squared training reconstruction residual with
\(N\) times the squared omitted-block norm. Evaluation errors use the disjoint 257-point
staggered inventory and cannot alter coefficients or range selection.

Bandwidth and zone-center curvature are finite sampled/model diagnostics. The maximum
imaginary residual checks both evaluation values and the reconstructed curvature. No
one diagnostic selects a scientifically adequate range.

## Independent numerical route

Production delegates to canonical model, transform, fit, and diagnostic owners.
Verification deliberately duplicates only the finite formulas needed for independence:
dense NumPy plane-wave matrices, sparse SciPy twisted-grid matrices, explicit Fourier
phase matrices, and `numpy.linalg.lstsq`. Both routes use binary64 arithmetic. Their
tolerances bound route agreement; they are not uncertainty intervals.
