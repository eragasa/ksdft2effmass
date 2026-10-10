# M1 numerical contract

## Discretization channels

Plane-wave sweeps use every `plane_wave_cutoffs` entry and compare the lowest
`compared_band_count` eigenvalues with the separately declared
`plane_wave_reference_cutoff`. The reference cutoff exceeds every sweep cutoff; it is a
finite numerical reference, not continuum truth.

Finite-difference sweeps use each `finite_difference_points` extent and compare against
the same finite plane-wave reference. Each grid has at least three points and enough
degrees of freedom for the requested band count.

## Reciprocal meshes

The reduction mesh has even extent `reciprocal_mesh_size`. Symmetric retained ranges
must satisfy

$$
0\leq L < \frac{N}{2},
$$

which prevents duplicate periodic representatives. The evaluation mesh follows
`EQ-M1-WITHHELD-MESH-003` and has at least three points.

## Error and norm conventions

- spectral errors are maximum absolute energy differences at identified coordinates;
- hopping and route defects use Frobenius norms in the model energy unit;
- the omitted-block diagnostic is an $\ell^2$ aggregate over discarded blocks;
- Parseval compares squared Frobenius energies and therefore requires a squared-energy
  tolerance; and
- the scalar imaginary residual and Hermiticity defect use energy units.

## Tolerances

| Control | Domain | Validation rule |
|---|---|---|
| `coordinate_absolute_tolerance` | coordinate matching | finite, nonnegative built-in `float` |
| `reconstruction_absolute_tolerance` | Fourier reconstruction and independent verification | finite, nonnegative built-in `float` in the retained model convention |
| `hermiticity_absolute_tolerance` | block-pair Hermiticity | nonnegative energy quantity |
| `parseval_absolute_tolerance` | squared-energy residual | nonnegative squared-energy quantity |
| `imaginary_absolute_tolerance` | scalar interpolation residual | nonnegative energy quantity |

Boolean controls and numeric strings are rejected at public numeric boundaries.

## Determinism and conditioning

The retained calculation fixes its eigensolver seed and serializes sorted, compact JSON
with `allow_nan=False`. Direct fitting retains design rank and condition number; those
values diagnose finite-design identifiability but do not establish uncertainty bounds.
Binary64 determinism is tested for the retained environment, not promised across all
BLAS/LAPACK implementations.

## Complexity

The dominant work is repeated dense/sparse eigenvalue construction across parent,
training, and evaluation coordinates. Memory is bounded by the declared finite bases
and meshes. M1 is an in-process synthetic calculation and must not dispatch an external
program.

## Numerical limitations

No extrapolation to infinite cutoff, zero grid spacing, or infinite hopping range is
performed. The finite reference and declared tolerances bound only the frozen protocol.
