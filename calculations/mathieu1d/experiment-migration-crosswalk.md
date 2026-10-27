# Mathieu1D experiment migration crosswalk

## Scientific scope

The scientific question is whether one retained band of the finite periodic Mathieu
Hamiltonian can be represented and checked through its finite Fourier hopping channels.
This audit does not rerun that calculation or reinterpret its numerical results. It
assigns every file in the old experiment location to the existing Mathieu1D calculation
owner while preserving the basis, units, energy reference, finite meshes, and evidence
claims already recorded by version 1 (`v1`).

## File audit result

The baseline is Git revision
`c73aa96077ee03e1f7438ecbb44349b445a3eec8`. Its experiment source tree contains 65
tracked files. The machine-readable
[`experiment-migration-manifest.json`](experiment-migration-manifest.json) records each
source path, source SHA-256 digest, calculation destination when applicable, explicit
disposition, content role, and byte relation.

All 65 files have a calculation-side destination or explicit disposition:

- 53 files are exact-byte duplicates;
- 10 files have explicit adapted or integrated successors;
- two development-environment files are provenance-only because the repository Python
  project owns live dependencies.

After this closed, non-destructive audit and separate operator authorization, exactly the
65 manifest-bound experiment files were removed at `2026-10-27T14:02:06Z`. Their source
bytes remain recoverable from the baseline revision.

The 53 exact duplicates include all 44 files inside the four retained run directories,
the three strict `v1` schemas, the family protocol and evidence policy, both repository
policy files, the runs README, and the historical source package `__init__.py`.

## Content classification

| Content role | Files | Disposition |
|---|---:|---|
| Immutable retained execution bytes | 44 | Preserve byte-for-byte under `calculations/mathieu1d/runs/`; the experiment copies are exact duplicates. |
| Strict `v1` schemas | 3 | Preserve byte-for-byte under `calculations/mathieu1d/schemas/`. |
| Historical execution source | 6 | The package initializer is exact. Five calculation-side modules are adapted successors using the current canonical import owners; the baseline records the old bytes. |
| Family documentation | 5 | Exact protocol, evidence policy, and runs README are already calculation-owned; the two source READMEs are integrated documentation donors. |
| Repository and environment policy | 4 | The attribute and ignore files are exact. The experiment project and lock files are provenance-only donors; the repository Python project owns live dependencies. |
| Producer, verifier, and test entry points | 3 | Each has a named calculation-side successor. |

## Adapted and integrated successors

| Experiment-relative source | Calculation destination | Relation |
|---|---|---|
| `README.md` | `README.md` | Container documentation integrated into the calculation README. |
| `periodic1d/README.md` | `README.md` | Family documentation integrated with calculation ownership and migration status. |
| `periodic1d/pyproject.toml` | Provenance-only | Historical experiment environment declaration. Live dependencies are owned only by `python/pyproject.toml`. |
| `periodic1d/run_experiment.py` | `run_01_experiment.py` | The maintained entry point reads `input.json` and calls `ksdft2effmass.model_systems.mathieu1d` directly. |
| `periodic1d/src/single_band_fourier_reduction/definition.py` | `src/single_band_fourier_reduction/definition.py` | Adapted historical-source successor using the canonical PhysKit unit owner. |
| `periodic1d/src/single_band_fourier_reduction/experiment.py` | `src/single_band_fourier_reduction/experiment.py` | Adapted historical-source successor using canonical `solidstate` and PhysKit imports. |
| `periodic1d/src/single_band_fourier_reduction/results.py` | `src/single_band_fourier_reduction/results.py` | Adapted historical-source successor using the canonical PhysKit unit owner. |
| `periodic1d/src/single_band_fourier_reduction/serialization.py` | `src/single_band_fourier_reduction/serialization.py` | Adapted historical-source successor using the canonical PhysKit unit owner. |
| `periodic1d/src/single_band_fourier_reduction/verify.py` | `src/single_band_fourier_reduction/verify.py` | Adapted historical-source successor using canonical `solidstate` and PhysKit imports. |
| `periodic1d/tests/test__SingleBandFourierReductionExperiment.py` | `tests/test__SingleBandFourierReductionExperiment.py` | Adapted calculation test for current imports, dependency revisions, and the canonical entry-point boundary. |
| `periodic1d/uv.lock` | Provenance-only | Historical experiment lock. Live resolved dependencies are owned only by `python/uv.lock`. |
| `periodic1d/verify_package.py` | `run_02_experiment_verification.py` | Adapted maintained verifier that authenticates the predecessor from its recorded Git revision and tree instead of requiring a live historical directory. |

The calculation-local `src/single_band_fourier_reduction/` tree is not an exact copy of
every current experiment file and is not a maintained import owner. Its purpose is to
audit the historical `v1` boundary. Exact old bytes remain recoverable from the baseline
revision and from earlier revisions recorded by each retained `source.sha256` manifest.

## Maintained source ownership

No maintained Python source, package test, or calculation entry point imports
`calculations/mathieu1d/src/`. The live producer imports the canonical owners directly.
The historical-to-maintained mapping is:

| Historical class or behavior | Maintained owner |
|---|---|
| `SingleBandFourierReductionExperimentIdentity` | `ModelSystemStudyIdentity` with the Mathieu1D model and schema identifiers |
| `SingleBandFourierReductionExperimentDefinition` | `Mathieu1dStudyDefinition` |
| `SingleBandFourierReductionExperiment` | `Mathieu1dStudyEvaluator` |
| `PlaneWaveRefinementObservation` | `Mathieu1dPlaneWaveRefinementObservation` |
| `FiniteDifferenceRefinementObservation` | `Mathieu1dFiniteDifferenceRefinementObservation` |
| `SingleBandFourierReductionExperimentResult` | `Mathieu1dStudyResult` |
| Input, result, and verification serialization | `Mathieu1dStudyInputSerializer`, `Mathieu1dStudyResultSerializer`, and `Mathieu1dStudyVerificationSerializer` |
| `SingleBandFourierReductionVerificationResult` | `Mathieu1dStudyVerificationResult` |
| `SingleBandFourierReductionExperimentVerifier` | `Mathieu1dStudyVerifier` |

## Provenance

The baseline experiment Git tree is
`bf20cf55a06c9eaae72f34093b72da0ea00c9240`. The sorted 65-path inventory has SHA-256
`e3539e76a97c5d83b18d23221f88634f96628ee5aa5a5558f7d1915526be0123`.
The migration manifest has SHA-256
`6c5f7178b84413517c81b020df9d4e4cce2e9fbe68b0d68ad56816ed50e65e2b`.
These identities establish file inventory, byte correspondence, and recovery only; they
do not establish convergence, uncertainty quantification, scientific validation, or
publication acceptance. The removal authorization and execution record are documented
separately in
[`experiment-removal-readiness.md`](experiment-removal-readiness.md).
