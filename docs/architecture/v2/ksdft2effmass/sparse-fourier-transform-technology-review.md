# Sparse and nonuniform Fourier-transform technology review

## Scope and status

This review supports the periodic-operator transform implementation. It does not
select or authorize a new dependency. Timings below are development measurements,
not scientific results or retained performance evidence.

The current contract transforms a complete uniform reciprocal mesh of dense reduced
$d\times d$ operator blocks into every centered Born--von Karman hopping block. The
word *sparse* can refer to three different properties that must not be conflated:

1. sparse storage within each represented operator matrix;
2. a sparse set of nonzero Fourier coefficients; or
3. nonuniform or incomplete reciprocal samples.

These properties require different algorithms.

## Uniform complete meshes

NumPy defines the forward DFT with the negative exponential, supports
``norm="forward"`` for the required $1/N$ normalization, and uses ``fftshift`` to
place negative representatives before zero. The periodic-1D implementation therefore
uses ``numpy.fft.fft`` along the reciprocal-sample axis, followed by ``fftshift`` and
the explicit phase $(-1)^R$ induced by the half-open mesh origin $-G/2$.

A local development timing compared the prior direct matrix DFT with the FFT kernel:

| Mesh points | Block size | Observed kernel ratio, direct/FFT |
|---:|---:|---:|
| 8 | 2 | 0.99 |
| 128 | 2 | 1.62 |
| 128 | 8 | 1.01 |
| 1024 | 8 | 7.94 |

The retained Appendix G scale is small, so this change is principally an
algorithmic-scaling correction. The public result still performs independent direct
interpolation for reconstruction assessment; end-to-end speedup is therefore smaller
than the kernel ratio.

SciPy's FFT API is a superset with worker controls and guarantees $O(N\log N)$
behavior for poorly factorizable sizes through Bluestein's algorithm. It is not needed
for the current small one-dimensional transform, and replacing NumPy would require a
representative end-to-end profile.

## Sparse matrix storage

Sparse storage of the orbital matrix axes is not expected to accelerate this
transform. Fourier summation combines all reciprocal samples, and the reduced band
blocks are generally dense even when a parent real-space operator was sparse.
PyData/Sparse provides multidimensional sparse-array storage, but its documented
public API does not provide FFT operations. Converting sparse matrices to a dense
sample tensor merely to call an FFT would add conversion cost without changing the
required dense output.

**Recommendation:** do not pursue a sparse-array FFT for the current projected-block
contract. Preserve CSR only in the finite-domain and finite-difference operators where
locality produces structural sparsity.

## Sparse-frequency algorithms

MIT's sparse Fourier transform algorithms target signals whose Fourier-domain output
has only $k\ll N$ significant coefficients and can return a succinct subset in
sublinear time. That is not the current contract: complete transforms, Parseval
accounting, truncation error, and route comparisons require every finite-mesh hopping
coefficient before an explicit truncation decision.

The public 2013 C/C++/Python SFFT implementation describes itself as experimental,
not a drop-in FFT replacement, and GPL-2.0-or-later licensed. It is therefore not a
suitable project dependency. The similarly named ``sfft`` Python package found on
package indexes concerns astronomical image subtraction rather than this sparse
Fourier algorithm.

**Recommendation:** do not integrate an SFFT library. Reconsider only if a future
accepted contract requests approximate top-$k$ hopping discovery, defines error and
failure probabilities, and does not require complete Parseval or truncation evidence.

## Nonuniform transforms

FINUFFT addresses arbitrary reciprocal coordinates rather than sparse matrix storage.
It supports one-, two-, and three-dimensional NUFFTs with requested relative accuracy,
CPU/GPU implementations, and Python interfaces. Its type-1 transform maps nonuniform
samples to a complete centered Fourier-mode inventory, making it the closest candidate
for a future demonstrated nonuniform reciprocal-mesh contract.

FINUFFT is still inappropriate for the current complete uniform mesh. It is
approximate, introduces a dependency and license decision, and its documentation notes
that inverse fitting from off-grid data may require a separate regularized linear
solve when quadrature weights are absent.

**Recommendation:** retain FINUFFT as the only candidate worth a future benchmark if
nonuniform authenticated $k$-point evidence is introduced. Do not add it now.

## Decision summary

| Use case | Recommended implementation |
|---|---|
| Complete uniform periodic mesh | ``numpy.fft.fft`` / ``fftn`` |
| Sparse finite-domain operator | CSR operations; no FFT substitution |
| Complete nonuniform samples with known transform semantics | Evaluate FINUFFT under a dependency checkpoint |
| Incomplete weighted fitting | Existing explicit least-squares contract |
| Approximate top-$k$ Fourier discovery | No current implementation; requires a new scientific contract |

## Sources

- [NumPy discrete Fourier transform documentation](https://numpy.org/doc/stable/reference/routines.fft.html)
- [SciPy ``fft`` documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.fft.html)
- [FINUFFT overview](https://finufft.readthedocs.io/en/v2.5.0/overview.html)
- [PyData/Sparse public API](https://sparse.pydata.org/en/stable/api/)
- [MIT Sparse Fast Fourier Transform project](https://groups.csail.mit.edu/netmit/sFFT/)
- [Experimental SFFT implementation](https://github.com/davidediger/sfft)
