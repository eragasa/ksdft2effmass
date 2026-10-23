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
before using any value. `run_02_experiment_verification.py` performs those byte,
schema, and predecessor checks without running the producer. `verification.json`
records the successful producer-independent direct-formula numerical reconstruction.

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

The live development and verification lock follows the current repository owner pins:
Optimization `3cd32ea8985a855bcdbaffbf89af95e970b3bf14` and PhysKit
`2aaa4ba5ff4c51f5c5068ac895ef4ec5de293439`. The retained v1 producer and package
verifier continue to require and report their historical execution-time revisions;
advancing the live lock neither rewrites those records nor authorizes a replacement
retained run.

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

The calculation-local `src/single_band_fourier_reduction/` tree preserves the exact
version-one execution-source implementation recorded by the retained source manifests.
It is historical evidence, not a maintained reusable owner or compatibility facade.
Calculation-local tests may replay it to audit that retained boundary, but new
production code must import the canonical `ksdft2effmass` owners instead.

## Reproduction and checks

Using the repository Python environment:

```console
cd calculations/mathieu1d
../../python/.venv/bin/pytest
../../python/.venv/bin/mypy --config-file pyproject.toml --strict \
    src tests run_01_experiment.py run_02_experiment_verification.py
../../python/.venv/bin/ruff format --check \
    src tests run_01_experiment.py run_02_experiment_verification.py
../../python/.venv/bin/ruff check \
    src tests run_01_experiment.py run_02_experiment_verification.py
uv lock --check
../../python/.venv/bin/python run_02_experiment_verification.py
```

`run_01_experiment.py` uses an immutable no-overwrite run identity. It performs only cheap
local deterministic synthetic work and does not invoke Quantum ESPRESSO, Wannier90, a
scheduler, remote resources, or external calculators.
