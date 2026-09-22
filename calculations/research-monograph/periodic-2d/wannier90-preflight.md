# Wannier90 comparison preflight

## Status and authority

The periodic-2D Task remains active after the human selected Option B at
`RM-PERIODIC-2D-ACCEPTANCE-HC01` and requested an independent Wannier90
localization comparison. This preflight defines the exact protected local
execution boundary. It does not itself authorize execution, Quantum ESPRESSO,
material-specific inputs, remote computation, dependency changes, or production
claims.

## Execution outcome

The human authorized Option A at
`RM-PERIODIC-2D-WANNIER90-EXECUTION-HC02`. The single attempt stopped during
preprocessing with
`kmesh_get: something wrong, found too many nearest neighbours`. It produced no
`.nnkp`, `.mmn`, or localization result and was not retried. Exact facts are
retained in `wannier90-execution.json`; the embedding diagnosis and separately
protected correction are retained in `wannier90-failure-diagnosis.md` and
`wannier90-retry-preflight.md`.

## Executable

- Command: `/Users/eugene/.local/bin/wannier90.x`
- Reported version: Wannier90 3.1.0
- SHA-256: `c826f817f807cf069e16d6e529a52ddc15d2f677101065908bcb2030d7f7d1dd`
- Invocation: one local process, without MPI

The version probe exits successfully and emits the previously documented
`IEEE_OVERFLOW_FLAG` notice. Preprocessing and localization stderr must be
retained so this and any input-specific diagnostics remain visible.

## Input system

The input is the synthetic two-dimensional continuum parent

$$
H=-\nabla^2+0.5\cos x+0.5\cos y+0.15\cos x\cos y
$$

in the dimensionless convention $a=2\pi$, $G=1$, and $E_G=1$. The represented
parent uses plane-wave cutoff $P=3$, a uniform $15\times15\times1$ mesh, and the
isolated lowest-three-band subspace. Its minimum sampled exterior gap is
$3.4784\times10^{-2}E_G$.

One seed, `low_triple`, has three bands and three Wannier functions. No
disentanglement is used. The `.amn` projections are independently generated
from the same centered Gaussian $s$, $p_x$, and $p_y$ trial functions used by
the direct projected gauge; the minimum retained projection singular value is
0.8861. The interface generator owns `.win`, `.eig`, `.amn`, and, after
preprocessing, `.mmn`. Reciprocal-boundary overlaps use explicit two-dimensional
plane-wave index sewing. The inactive third direction has a declared unit
transverse form factor.

The initial generated interface occupies 164 KiB. Its identities are:

- `.win`: `ec1ccafdb921af8ef6a1b697bf5f4f32e8e6f2deedec7672e61474ab0850e59d`
- `.eig`: `092b286beb4e21eaf7e9364597249343f90baee2e2a9f0d38427f0cdfd2b02c4`
- `.amn`: `d61948e296b7fdb1b9983c6458eb9547f4b2dc0e7796596548c017f7bed65ef6`

## Frozen localization controls

The first authorized attempt, if approved, uses:

```text
num_bands = 3
num_wann = 3
num_iter = 5000
conv_tol = 1.0d-12
conv_window = 5
precond = true
search_shells = 130
write_hr = true
write_u_matrices = true
translate_home_cell = true
```

`precond = true` and `search_shells = 130` are retained from the accepted
periodic-1D synthetic interface because the same inactive-direction embedding
and strict spread criterion are used. They are declared initial settings here,
not post-failure corrections.

## Scale and resources

The seed contains 225 reciprocal points, three bands, three Wannier functions,
and a 49-component plane-wave parent basis. The expected execution is one local
process for preprocessing and one for localization, seconds to five minutes per
stage, below 512 MiB resident memory, and below 50 MiB total external output.
The run must stop if any bound is exceeded.

## Commands and anticipated outputs

After generating initial files in a fresh external run directory:

```text
wannier90.x -pp low_triple
prepare_wannier90.py --stage interface
wannier90.x low_triple
```

Anticipated outputs include `.nnkp`, `.mmn`, `.wout`, `.chk`, `.u.mat`,
`_hr.dat`, centers, spreads, and convergence diagnostics. Native and scratch
outputs remain outside the repository. Only sanitized interface metadata,
execution facts, checksums, compact extracted comparisons, figures, and report
updates may be retained in Git.

The extracted comparison must align translations and constant orbital freedom
before comparing retained projectors, Wilson-center phases, active-plane
centers and spreads, mesh spectra, and hopping blocks with the direct projected
gauge.

## Stop conditions

Stop without retry if preprocessing or localization fails, reports nonfinite
values, does not meet the frozen convergence criterion, exceeds the resource
envelope, or requires changing the parent, mesh, rank, projections, convergence
settings, topology policy, or symmetry policy. A failed attempt remains
retained evidence and requires a new human checkpoint before any retry.

Successful execution would establish only an independently implemented
localization comparison for this synthetic represented parent. It would not
establish material validity, production readiness, scientific validation,
transferability, or human acceptance.
