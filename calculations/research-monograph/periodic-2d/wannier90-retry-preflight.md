# Corrected Wannier90 embedding retry preflight

## Execution outcome

The human authorized Option A at
`RM-PERIODIC-2D-WANNIER90-EMBEDDING-RETRY-HC04`. Corrected preprocessing
completed with six neighbors, and localization converged after 94 iterations.
The bounded run used 0.28 s and 22.6 MB maximum resident memory for
preprocessing and 0.47 s and 27.3 MB for localization. The extracted comparison
and independent reconstruction are retained in `wannier90-balanced-result.json`
and `verify_wannier90_balanced.py`.

## Prior failure

The attempt authorized at `RM-PERIODIC-2D-WANNIER90-EXECUTION-HC02` stopped in
preprocessing with
`kmesh_get: something wrong, found too many nearest neighbours`. No `.nnkp`,
`.mmn`, or localization result was produced, and no retry occurred. The failure
is retained in `wannier90-execution.json` and diagnosed in
`wannier90-failure-diagnosis.md`.

## Exact correction

The proposed retry changes only the auxiliary inactive direct-lattice vector in
`low_triple.win`:

```diff
- 0.0 0.0 1.0
+ 0.0 0.0 15.0000000000000000
```

The active cell, parent operator, $15\times15\times1$ reciprocal mesh,
plane-wave cutoff, three retained bands, $s/p_x/p_y$ projections, energy file,
localization controls, and comparison criteria are unchanged. The inactive
reciprocal increment then has magnitude $2\pi/15$, matching the active
increments. The inactive overlap remains a declared unit transverse form
factor.

The corrected deterministic initial identities are:

- `.win`: `a5fb239057c8495fb4f4d5e892ff52bdb12e4b5afab5c2852eb35c07e4de3e88`
- `.eig`: `092b286beb4e21eaf7e9364597249343f90baee2e2a9f0d38427f0cdfd2b02c4`
- `.amn`: `d61948e296b7fdb1b9983c6458eb9547f4b2dc0e7796596548c017f7bed65ef6`
- corrected interface generator:
  `4c5d6bf857710fc4322c6a7b6f3d69898b1645e66ebef588e4ac585ee3eb2696`

The generator's default `unit` mode still reproduces the failed input exactly;
the retry requires explicit `--embedding balanced`.

## Executable, scale, and resources

- Executable: `/Users/eugene/.local/bin/wannier90.x`
- Version: Wannier90 3.1.0
- Executable SHA-256:
  `c826f817f807cf069e16d6e529a52ddc15d2f677101065908bcb2030d7f7d1dd`
- Scale: 225 reciprocal points, three bands, three Wannier functions, and a
  49-component active plane-wave basis
- Processes: one local preprocessing process and, only if preprocessing passes,
  one local localization process
- Limit: five minutes per stage, 512 MiB resident memory, and 50 MiB total
  external output

## Exact stages

```text
prepare_wannier90.py --stage initial --embedding balanced
wannier90.x -pp low_triple
prepare_wannier90.py --stage interface --embedding balanced
wannier90.x low_triple
```

Expected outputs remain `.nnkp`, `.mmn`, `.wout`, `.chk`, `.u.mat`, `_hr.dat`,
centers, spreads, and convergence diagnostics. Only active-plane centers and
spreads may be compared; the auxiliary transverse contribution must remain
separately labeled.

The retry must stop without another retry if preprocessing or localization
fails, does not converge, produces nonfinite values, exceeds a resource limit,
or requires any further interface or scientific change. Native outputs remain
outside Git. A compact failure or extracted comparison record, checksums,
figures, and manuscript updates may be retained.

Successful execution would establish only an independently implemented
localization comparison for the frozen synthetic represented parent. It would
not establish material validity, production readiness, scientific validation,
transferability, or human acceptance.
