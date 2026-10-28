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

At the experiment-removal gate, the 53 exact duplicates included all 44 files inside the
four calculation-side predecessor run directories, the three strict `v1` schemas, the
family protocol and evidence policy, both repository policy files, the runs README, and
the historical source package `__init__.py`. The 44 run files and runs README were later
removed from the live tree after direct recalculation and separate authorization; their
compact recovery boundary is [`legacy-run-retirement.md`](legacy-run-retirement.md).
The calculation-local producer, package verifier, source package, and tests were also
removed after direct-lifecycle parity and separate authorization; their recovery
boundary is [`direct-successor-retirement.md`](direct-successor-retirement.md). The
orphaned input and three strict `v1` schemas were subsequently removed after a consumer
audit and separate authorization; their recovery boundary is
[`legacy-contract-retirement.md`](legacy-contract-retirement.md).

## Content classification

| Content role | Files | Disposition |
|---|---:|---|
| Predecessor execution bytes | 44 | Exact duplicates at the donor-removal gate; subsequently removed from the live tree after direct replacement. |
| Strict `v1` schemas | 3 | Exact duplicates at the donor-removal gate; subsequently removed after the direct typed wire superseded them and the consumer audit found no references. |
| Historical execution source | 6 | The package initializer was exact and five calculation-side modules were adapted successors at the donor-removal gate. All six were later removed after direct-lifecycle parity. |
| Family documentation | 5 | Exact protocol, evidence policy, and runs README were calculation-owned at the donor-removal gate; the two source READMEs are integrated documentation donors. The runs README was later removed with the predecessor executions. |
| Repository and environment policy | 4 | The ignore file remains exact. The attribute file that applied only to removed run CSV paths was subsequently removed. The experiment project and lock files are provenance-only donors; the repository Python project owns live dependencies. |
| Producer, verifier, and test entry points | 3 | Each had a named calculation-side successor at the donor-removal gate; those predecessor entry points and the calculation-side test were later removed. |

## Adapted and integrated successors at the donor-removal gate

The destination column records the historical calculation-side state at that gate, not
current live ownership. Later-removed destinations carry explicit machine-readable
dispositions in the manifest and exact recovery identities in the retirement ledgers.

| Experiment-relative source | Historical calculation destination | Relation |
|---|---|---|
| `README.md` | `README.md` | Container documentation integrated into the calculation README. |
| `periodic1d/README.md` | `README.md` | Family documentation integrated with calculation ownership and migration status. |
| `periodic1d/pyproject.toml` | Provenance-only | Historical experiment environment declaration. Live dependencies are owned only by `python/pyproject.toml`. |
| `periodic1d/run_experiment.py` | `run_01_experiment.py` | Historical adapted entry point; later removed after direct-lifecycle parity. |
| `periodic1d/src/single_band_fourier_reduction/definition.py` | `src/single_band_fourier_reduction/definition.py` | Historical adapted source; later removed after direct-lifecycle parity. |
| `periodic1d/src/single_band_fourier_reduction/experiment.py` | `src/single_band_fourier_reduction/experiment.py` | Historical adapted source; later removed after direct-lifecycle parity. |
| `periodic1d/src/single_band_fourier_reduction/results.py` | `src/single_band_fourier_reduction/results.py` | Historical adapted source; later removed after direct-lifecycle parity. |
| `periodic1d/src/single_band_fourier_reduction/serialization.py` | `src/single_band_fourier_reduction/serialization.py` | Historical adapted source; later removed after direct-lifecycle parity. |
| `periodic1d/src/single_band_fourier_reduction/verify.py` | `src/single_band_fourier_reduction/verify.py` | Historical adapted source; later removed after direct-lifecycle parity. |
| `periodic1d/tests/test__SingleBandFourierReductionExperiment.py` | `tests/test__SingleBandFourierReductionExperiment.py` | Historical adapted test; later removed after direct-lifecycle parity. |
| `periodic1d/uv.lock` | Provenance-only | Historical experiment lock. Live resolved dependencies are owned only by `python/uv.lock`. |
| `periodic1d/verify_package.py` | `run_02_experiment_verification.py` | Historical adapted package verifier; later removed after direct-lifecycle parity. |

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

This table records the completed experiment-tree migration and does not make those
intermediate successor classes permanent contracts. A later direct lifecycle established
behavioral parity and retired the calculation-local package, its legacy producer and
package-verifier scripts, their calculation-local tests, and—after separate source
authorization—the installed `mathieu1d.study` predecessor. The current direct route is
`run_01_calculation.py` → `run_02_verification.py` → `run_03_render.py`; exact retirement
and recovery details are consolidated by the Architecture v3
[legacy disposition](../../docs/architecture/v3/ksdft2effmass/model_systems/mathieu1d/legacy-disposition.md),
which links the exact calculation-side retirement ledgers. The historical bytes were
not rewritten into the new wire; no predecessor run artifact, input, or schema remains
in the live tree.

## Provenance

The baseline experiment Git tree is
`bf20cf55a06c9eaae72f34093b72da0ea00c9240`. The sorted 65-path inventory has SHA-256
`e3539e76a97c5d83b18d23221f88634f96628ee5aa5a5558f7d1915526be0123`.
After recording the later calculation-code, predecessor-run, and orphaned-contract
deletion dispositions, the migration manifest has SHA-256
`81a9d24064a120b91de66aa1c157234b9d777aa95b98b0f62b8133f26160cd7b`.
These identities establish file inventory, byte correspondence, and recovery only; they
do not establish convergence, uncertainty quantification, scientific validation, or
publication acceptance. The removal authorization and execution record are documented
separately in
[`experiment-removal-readiness.md`](experiment-removal-readiness.md).
