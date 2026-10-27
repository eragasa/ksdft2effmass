# Mathieu1D single-band Fourier reduction

This calculation uses the scalar periodic Mathieu Hamiltonian

\[
H=-\frac{d^2}{dx^2}+\lambda\cos x,
\]

with retained case \(\lambda=0.5\). Its filesystem owner follows the same model-system
convention as `calculations/qho1d/` and `calculations/piab1d/`.

## Retained status

This calculation package maintains the publication-independent experiment family

```text
ksdft2effmass.campaign.periodic-reduction.periodic1d.single-band-fourier-reduction
```

Immutable version `v1` and four retained local synthetic runs now exist. Historical
`M1` and `isolated-band` labels are publication aliases only. The retained outcomes are
bounded software and finite-protocol numerical-verification evidence; they are not a
continuum isolation certificate, scientific acceptance, material validation, or
uncertainty quantification.

The publication-facing retained run is:

```text
ksdft2effmass.campaign.periodic-reduction.periodic1d.single-band-fourier-reduction.v1.run-20261014T184707Z
```

Its evidence package lives under `runs/<run-id>/`; [`runs/README.md`](runs/README.md)
distinguishes prior non-publication development executions. Consumers must verify
`evidence-package-identity.txt`, `SHA256SUMS`, canonical JSON, and the strict schemas
before using any value. `run_02_experiment_verification.py` is the maintained
producer-independent package verifier. It authenticates the removed predecessor from
its recorded Git revision and tree rather than requiring the historical directory in
the current filesystem. The retained `verification.json` records the execution-time
producer-independent direct-formula numerical reconstruction.

## Version-one capability

Version `v1` retains the historical synthetic controls and adds:

- strictly positive caller-supplied objective weights;
- explicit objective-construction and disjoint evaluation roles;
- caller-selected hopping ranges;
- direct use of reviewed owner APIs, including the Optimization least-squares owner;
- typed immutable definition, result, identity, and verification records;
- explicit units, fixed energy reference, Fourier signs, and normalization;
- rank, conditioning, residual, reconstruction, sampled-gap, route, and locality
  diagnostics;
- canonical finite JSON and strict version-bound schemas;
- a producer-independent verifier that does not call the experiment or reusable
  reduction Workflow Actions; and
- exact dirty-worktree source, execution-time dependency, runtime,
  historical-predecessor, file, run, and evidence-package identities, retained
  separately from later repository-level dependency advances.

The repository Python project is the only live dependency authority. It pins Optimization
`2a18e485109e307b2f7928bd0418bcf796aeb0d5` and PhysKit
`9c74ffa2fa0f40792117ccaa6c0bf0bcb0e70fe5`; this calculation does not maintain a second
`pyproject.toml` or lock file. The retained `v1` producer and package provenance continue
to report their distinct historical execution-time revisions. Removing the duplicate
calculation environment did not rewrite those records or create a replacement retained
run.

The matched historical channels have zero retained binary64 defect in `parity.json`.
The new sampled gaps are diagnostics only and do not retroactively alter historical M1.
Historical files remain unchanged and are bound by exact Git revision, path, tree, and
SHA-256 digests in successor provenance. The retained version-one runs were executed
before the model-system directory relocation, so their immutable `source.sha256` files
preserve the execution-time path
`experiments/periodic-reduction/periodic1d/single-band-fourier-reduction/`; live
publication manifests resolve the current `calculations/mathieu1d/` path.

## Ownership

The experiment owns the finite Fourier toy parent, refinement inventories, represented
reference, retained-band selection, sample roles, objective weights, range inventory,
versioned schemas, interpretation, verification, and evidence policy.

`ksdft2effmass.model_systems.mathieu1d.study` owns the maintained Mathieu1D study
composition. It calls
`ksdft2effmass.analysis.single_band_reduction.SingleBandHoppingReductionWorkflow1D`,
which owns the model-independent transform, truncation, weighted direct route, route
comparison, and diagnostics. The calculation entry point calls those owners directly;
its independent verifier separately reconstructs formulas for evidence checking.

The calculation-local `src/single_band_fourier_reduction/` tree is an adapted successor
to the version-one execution source: its imports were updated to canonical `solidstate`
and PhysKit unit owners. It is historical audit support, not a maintained reusable owner
or compatibility facade. Exact execution-time bytes remain identified by the retained
source manifests and their Git revisions. Calculation-local tests may replay the adapted
boundary, but new production code must import the canonical `ksdft2effmass` owners
instead.

## Reproduction and checks

Using the repository Python environment:

```console
cd python
PYTHONPATH=../calculations/mathieu1d:../calculations/mathieu1d/src \
    .venv/bin/pytest -c pyproject.toml ../calculations/mathieu1d/tests
MYPYPATH=../calculations/mathieu1d/src \
    .venv/bin/mypy --strict \
    ../calculations/mathieu1d/src \
    ../calculations/mathieu1d/tests \
    ../calculations/mathieu1d/run_01_experiment.py \
    ../calculations/mathieu1d/run_02_experiment_verification.py
.venv/bin/ruff format --check \
    ../calculations/mathieu1d/src \
    ../calculations/mathieu1d/tests \
    ../calculations/mathieu1d/run_01_experiment.py \
    ../calculations/mathieu1d/run_02_experiment_verification.py
.venv/bin/ruff check \
    ../calculations/mathieu1d/src \
    ../calculations/mathieu1d/tests \
    ../calculations/mathieu1d/run_01_experiment.py \
    ../calculations/mathieu1d/run_02_experiment_verification.py
cd ..
python/.venv/bin/python calculations/mathieu1d/run_02_experiment_verification.py
```

The package verifier passes with Git-bound predecessor recovery. All live checks consume
the repository Python environment; retained execution-time dependency identities remain
unchanged.

`run_01_experiment.py` uses an immutable no-overwrite run identity. It performs only cheap
local deterministic synthetic work and does not invoke Quantum ESPRESSO, Wannier90, a
scheduler, remote resources, or external calculators.

## Migration inventory

This README owns the local inventory; [`migration.md`](migration.md) owns its distributed
checklist. The 65-file destination and digest partition is recorded in
[`experiment-migration-crosswalk.md`](experiment-migration-crosswalk.md) and
[`experiment-migration-manifest.json`](experiment-migration-manifest.json). The completed
exact removal and recovery authority are recorded in
[`experiment-removal-readiness.md`](experiment-removal-readiness.md).

| Surface | Current disposition |
|---|---|
| Four immutable `v1` run directories | Preserve: three development runs and one publication-facing run, each with its own result, verification, parity, provenance, source, checksum, report, figure, and evidence identity. |
| `schemas/` | Retained strict `v1` input/result/verification contracts; not silently revised. |
| `src/single_band_fourier_reduction/` | Adapted historical-source successor using current canonical imports; exact execution-time bytes remain recoverable from manifest-bound Git revisions. Not a maintained import owner. |
| `ksdft2effmass.model_systems.mathieu1d.study` | Maintained study composition for new code. |
| `run_01_experiment.py` and `run_02_experiment_verification.py` | Current calculation-root composition; the verifier authenticates the removed predecessor from its recorded Git objects. This is not yet the complete canonical calculate → verify → render → seal lifecycle. |
| Repository `python/pyproject.toml` and `python/uv.lock` | Sole live dependency declarations; the calculation has no parallel environment authority. |
| Experiment-side `pyproject.toml` and `uv.lock` | Provenance-only development-environment donors recoverable from the baseline; they are not migrated as live calculation dependencies. |
| Removed `experiments/periodic-reduction/single-band-fourier-reduction/` | Historical 65-file migration donor: 53 exact duplicates, 10 adapted or integrated successors, and two provenance-only environment donors. It was removed after exact-manifest review and separate operator authorization and remains recoverable from `c73aa96077ee03e1f7438ecbb44349b445a3eec8`. |
| `periodic1d/rank1/fourier-locality/` and historical M1 isolated-band work | Related donors only; scientifically distinct from Mathieu1D. |
