# Reduction-challenge numerical techniques and scientific reasoning

## Scope

The retained campaign challenges a finite periodic reduction of the dimensionless
one-dimensional cosine Hamiltonian. It separates represented parent discretization,
band isolation, gauge behavior, complete hopping representation, and fitted/truncated
route assumptions. It is illustrative and is not a semiconductor model or validation
study.

## Independent finite representations

For reciprocal index set $n=-P,\ldots,P$, the verifier directly assembles the finite
plane-wave Galerkin matrix

$$
H_{nm}(k)=(n+k)^2\delta_{nm}+V_{n-m},
$$

using only the declared Fourier coefficient map. For an $N$-point half-open periodic
coordinate grid, it independently assembles the centered second-difference operator
with conjugate Bloch seam phases. These are distinct finite representations; agreement
between them does not prove convergence to the untruncated parent.

Dense Hermitian eigensolves scale as $O(d^3)$ in matrix dimension $d$ and require
$O(d^2)$ storage. The campaign imposes no arbitrary size cap; allocation and linear
algebra failures remain explicit.

## Complete hopping representation

For a complete uniform reciprocal mesh with centered cell representatives $r$, the
verifier uses

$$
t_r=\frac{1}{N_k}\sum_k e^{-2\pi i k r}H(k),
\qquad
H(k)=\sum_r e^{2\pi i k r}t_r.
$$

The finite transform and inverse are exact relations for the sampled represented
operator up to floating-point error. They do not establish locality or justify a
finite-range effective model.

## Gauge covariance

The deterministic phase attack changes eigenvector representatives while preserving
the rank-one projectors. The verifier compares three retained gauge diagnostics:
projector defects, aligned parallel-transported-frame defects, and closure-holonomy
differences modulo $2\pi$. Complete hopping reconstruction belongs to the separate
mesh/band channel, and fitting coefficients belong to the route channel. Gauge
covariance does not imply gauge-independent locality or truncation quality.

## Route challenges

The baseline direct fit uses the same complete uniform mesh, equal weights, and full
Fourier class as the mediated transform. Separate challenges change weights or train on
only part of reciprocal space. Ordinary complex least squares is solved directly with
`numpy.linalg.lstsq`. Failure of equality under changed objectives is expected and is
not hidden or converted into a numerical failure.

## Error and claim separation

The campaign keeps parent-model, plane-wave cutoff, finite-difference, reciprocal-mesh,
band-isolation, gauge, transform, truncation, fitting, and sampling/aliasing effects
separate. One inclusive tolerance compares independently reconstructed values with the
retained reported values. It is a software/numerical comparison tolerance, not a
rigorous forward-error bound, physical uncertainty, validation criterion, or human
acceptance threshold.
