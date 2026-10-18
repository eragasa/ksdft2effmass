# Periodic 1-D single-band Fourier reduction

## Retained status

This is the maintained, publication-independent experiment family

```text
ksdft2effmass.campaign.periodic-reduction.periodic1d.single-band-fourier-reduction
```

Immutable version `v1` and a retained local synthetic run now exist. Historical `M1`
and `isolated-band` labels are publication aliases only. The retained outcome is
bounded software and finite-protocol numerical-verification evidence; it is not a
continuum isolation certificate, scientific acceptance, material validation, or
uncertainty quantification.

The publication-facing retained run is:

```text
ksdft2effmass.campaign.periodic-reduction.periodic1d.single-band-fourier-reduction.v1.run-20261014T184707Z
```

Its evidence package lives under `runs/<run-id>/`; [`runs/README.md`](runs/README.md)
distinguishes prior non-publication development executions. Consumers must verify
`evidence-package-identity.txt`, `SHA256SUMS`, canonical JSON, and the strict schemas
before using any value. `verify_package.py` performs those byte/schema/predecessor
checks without running the producer. `verification.json` records the successful
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

The live development and verification lock follows the current repository owner pins:
Optimization `2c6dd7f717722f6b0495feb8cfe1287a104268a6` and PhysKit
`7120b735c7e3e450aa8924780a71deb59d812632`. The retained v1 producer and package
verifier continue to require and report their historical execution-time revisions;
advancing the live lock neither rewrites those records nor authorizes a replacement
retained run.

The matched historical channels have zero retained binary64 defect in `parity.json`.
The new sampled gaps are diagnostics only and do not retroactively alter historical M1.
Historical files remain unchanged and are bound by exact Git revision, path, tree, and
SHA-256 digests in successor provenance. The retained version-one runs were executed
before the family-first directory relocation, so their immutable `source.sha256` files
preserve the execution-time path
`experiments/periodic-reduction/periodic1d/single-band-fourier-reduction/`; live
publication manifests resolve the current family-first path.

## Ownership

The experiment owns the finite Fourier toy parent, refinement inventories, represented
reference, retained-band selection, sample roles, objective weights, range inventory,
versioned schemas, interpretation, verification, and evidence policy.

`ksdft2effmass.analysis.single_band_reduction.SingleBandHoppingReductionWorkflow1D`
owns the model-independent transform, truncation, weighted direct route, route
comparison, and diagnostics. The experiment calls these owner APIs directly and
contains no duplicate producer implementation. Its independent verifier separately
reconstructs formulas for evidence checking.

## Reproduction and checks

Using the repository Python environment:

```console
cd experiments/periodic-reduction/single-band-fourier-reduction/periodic1d
../../../../python/.venv/bin/pytest
../../../../python/.venv/bin/mypy src tests
../../../../python/.venv/bin/ruff check src tests
uv lock --check
../../../../python/.venv/bin/python verify_package.py
```

`run_experiment.py` uses an immutable no-overwrite run identity. It performs only cheap
local deterministic synthetic work and does not invoke Quantum ESPRESSO, Wannier90, a
scheduler, remote resources, or external calculators.
