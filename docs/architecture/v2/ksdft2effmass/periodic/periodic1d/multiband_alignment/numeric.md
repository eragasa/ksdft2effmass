# M2 numerical contract

## Mesh and rank

M2 v1 requires `retained_rank == 2`. The reciprocal training mesh is even and at least
four points; every finite hopping range is nonnegative and smaller than half the mesh
extent. The staggered evaluation mesh has at least three points and uses the exact
offset $1/(N+1)$.

## Frame transport

Raw eigenspaces are transported by polar overlap factors. The minimum singular value
across neighbor and closure overlaps is retained and compared with
`overlap_singular_value_threshold`. Orthonormality is checked with a separate absolute
tolerance. Closure eigenphases are diagnostics of the finite transported path.

## Norm channels

- projector and frame defects use dimensionless Frobenius norms;
- represented-operator defects use the parent energy unit;
- Hermiticity defects use the parent energy unit;
- omitted-block locality uses an $\ell^2$ Frobenius aggregate in energy units; and
- spectral range errors are maximum absolute retained-band energy errors.

Invariant projector defects and frame-dependent represented-matrix defects must not be
combined into one unnamed metric.

## Global-unitary computation

The global channel minimizes a finite Frobenius objective over one unitary matrix. The
implementation constructs the aggregate cross-covariance and takes its polar/SVD
factor. This is not a solver over momentum-dependent unitary functions.

## Tolerances

| Control | Purpose | Contract |
|---|---|---|
| `external_gap_lower_bound` | minimum finite-mesh retained/excluded separation | nonnegative energy quantity |
| `overlap_singular_value_threshold` | reject ill-conditioned transport links | finite `float` in $[0,1)$ |
| `orthonormality_absolute_tolerance` | frame isometry | finite nonnegative `float` |
| `coordinate_absolute_tolerance` | common reciprocal coordinates | finite nonnegative `float` |
| `reconstruction_absolute_tolerance` | Fourier round trip | finite nonnegative `float` |
| `hermiticity_absolute_tolerance` | block-pair Hermiticity | nonnegative energy quantity |
| `verification_absolute_tolerance` | independent reconstructed defects | finite nonnegative `float` |

## Determinism and limitations

The calculation uses deterministic finite linear algebra and canonical JSON. Results may
depend on binary64 eigensolver and SVD conventions across platforms. No continuum,
infinite-range, or arbitrary-gauge limit is inferred from the finite sequences.
