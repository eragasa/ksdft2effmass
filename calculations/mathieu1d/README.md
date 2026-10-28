# Mathieu1D single-band Fourier reduction

This calculation uses the scalar periodic Mathieu Hamiltonian

\[
H=-\frac{d^2}{dx^2}+\lambda\cos x,
\]

with retained case \(\lambda=0.5\). Its filesystem owner follows the same model-system
convention as `calculations/qho1d/` and `calculations/piab1d/`.

## Current status

The only live calculation route is the direct typed lifecycle:

```text
run_01_calculation.py → run_02_verification.py → run_03_render.py
```

Its retained unsealed execution is
[`executions/direct-finite-reduction-n64/`](executions/direct-finite-reduction-n64/).
[`executions/README.md`](executions/README.md) records the exact direct artifact
inventory. Ragasa2026a and the research monograph consume the direct result, independent
verification, authenticated publication figure, and technical report.

The four version-one predecessor runs and all of their JSON, CSV, Markdown, checksum,
source-manifest, identity, and PNG bytes were removed from the live tree after explicit
operator authorization. They are not supported data or compatibility contracts. The
compact Git recovery boundary is recorded in
[`legacy-run-retirement.md`](legacy-run-retirement.md). The orphaned version-one input
and three JSON schemas were also removed; their recovery boundary is
[`legacy-contract-retirement.md`](legacy-contract-retirement.md).

## Direct capability

The direct lifecycle owns:

- immutable typed configuration and result records;
- explicit objective-construction and disjoint evaluation coordinates;
- caller-selected hopping ranges and positive fitting weights;
- direct use of canonical plane-wave, finite-difference, Fourier-transform, truncation,
  least-squares, interpolation, and diagnostic owners;
- explicit units, energy reference, Fourier signs, and normalization;
- rank, conditioning, residual, reconstruction, sampled-gap, route, and locality
  diagnostics;
- canonical typed JSON;
- byte-owning independent verification that bypasses the producer; and
- authenticated rendering from verifier-derived typed projections.

The repository Python project is the only live dependency authority. It pins Optimization
`2a18e485109e307b2f7928bd0418bcf796aeb0d5` and PhysKit
`9c74ffa2fa0f40792117ccaa6c0bf0bcb0e70fe5`; this calculation does not maintain a second
`pyproject.toml` or lock file.

## Ownership

The calculation owns the finite Fourier toy parent, refinement inventories, represented
reference, retained-band selection, sample roles, objective weights, range inventory,
protocol, interpretation, and evidence policy. Typed source records own the live wire
contracts.

The direct successor under `ksdft2effmass.model_systems.mathieu1d` owns typed
configuration, model-specific composition, result semantics, independent verification,
and authenticated visualization. Production calculation calls the canonical
plane-wave, periodic finite-difference, Fourier-transform, truncation, fitting,
interpolation, and diagnostic owners directly. The independent verifier reconstructs
the finite formulas without invoking the producer or a reusable Workflow.

The former calculation-local `src/single_band_fourier_reduction/` audit package and its
two legacy scripts were retired after exact behavioral parity and Git recovery checks.
The installed `ksdft2effmass.model_systems.mathieu1d.study` predecessor was then retired
after separate source authorization, and the package roots now expose only the direct
typed lifecycle. These predecessors are not maintained import owners or compatibility
facades. Their exact bytes remain recoverable through
[`direct-successor-retirement.md`](direct-successor-retirement.md) and
[`installed-successor-retirement.md`](installed-successor-retirement.md). The
Architecture v3 [legacy disposition](../../docs/architecture/v3/ksdft2effmass/model_systems/mathieu1d/legacy-disposition.md)
consolidates the current ownership decision and links every detailed recovery record.

## Reproduction and checks

Using the repository Python environment, run the package-owned direct lifecycle tests:

```console
cd python
.venv/bin/pytest -c pyproject.toml \
    tests/ksdft2effmass/model_systems/mathieu1d
```

The integration tests copy the three direct scripts to a temporary calculation root and
execute calculate → verify → render without changing the retained repository execution.
They check typed calculation behavior, byte-owning verification, modified-wire rejection,
the two-figure authenticated plot inventory, and no-overwrite behavior. The direct scripts perform only local deterministic synthetic work and do not
invoke Quantum ESPRESSO, Wannier90, a scheduler, remote resources, or external
calculators.

The retained direct execution was separately authorized and records dirty-worktree Git
qualification at committed base `2ea109d5165366bc507d8900cf85a67de1a2bf73`. Its exact
result SHA-256 is `83d25e824a0aedf085e77e86a998c02a17d4a51c320375b0bfb395986dae3fe6`;
its independent verification has SHA-256
`61553c16636efc39452706006dc480b827c2f2d04f3e318e02e3c2eec4f24664`.
The execution remains explicitly unsealed.

## Migration inventory

This README owns the local inventory; [`migration.md`](migration.md) owns its distributed
checklist. The 65-file destination and digest partition is recorded in
[`experiment-migration-crosswalk.md`](experiment-migration-crosswalk.md) and
[`experiment-migration-manifest.json`](experiment-migration-manifest.json). The completed
exact removal and recovery authority are recorded in
[`experiment-removal-readiness.md`](experiment-removal-readiness.md).

| Surface | Current disposition |
|---|---|
| Retired version-one runs | Removed from the live tree. Only the compact Git recovery boundary in `legacy-run-retirement.md` remains. |
| Retired version-one input and schemas | Removed from the live tree after consumer audit. Only `legacy-contract-retirement.md` records their Git recovery boundary. |
| Retired `src/single_band_fourier_reduction/` | Removed live audit package; exact bytes remain Git-recoverable through `direct-successor-retirement.md`. It is not a supported import or wire owner. |
| Direct `ksdft2effmass.model_systems.mathieu1d` modules | Typed configuration, calculation, result, byte-owning verification, authenticated projection, and rendering behavior. Existing canonical numerical owners remain authoritative for reusable operations. |
| `run_01_calculation.py`, `run_02_verification.py`, and `run_03_render.py` | Current direct calculation-root composition. The scripts produced the authorized retained unsealed `executions/direct-finite-reduction-n64/` execution and refuse to overwrite it. Tests continue to execute only in temporary roots. |
| `technical-report/` | Buildable three-page calculation-facing report with exact local copies of both authenticated direct figures and retained PDF review snapshot. |
| Retired `run_01_experiment.py` and `run_02_experiment_verification.py` | Removed legacy producer/package-verifier routes; exact source and test bytes remain recoverable from the recorded retirement revision. |
| Repository `python/pyproject.toml` and `python/uv.lock` | Sole live dependency declarations; the calculation has no parallel environment authority. |
| Experiment-side `pyproject.toml` and `uv.lock` | Provenance-only development-environment donors recoverable from the baseline; they are not migrated as live calculation dependencies. |
| Removed `experiments/periodic-reduction/single-band-fourier-reduction/` | Historical 65-file migration donor: 53 exact duplicates, 10 adapted or integrated successors, and two provenance-only environment donors. It was removed after exact-manifest review and separate operator authorization and remains recoverable from `c73aa96077ee03e1f7438ecbb44349b445a3eec8`. |
| `periodic1d/rank1/fourier-locality/` and historical M1 isolated-band work | Related donors only; scientifically distinct from Mathieu1D. |
