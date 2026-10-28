# Mathieu1D canonical-infrastructure migration

This is the distributed checklist for the calculation inventory in
[`README.md`](README.md). A checked item records only the stated migration fact; it does
not establish scientific validation, authorize evidence replacement, or permit retained
bytes to change.

## Experiment-tree migration

- [x] Assign all 65 tracked files under `experiments/periodic-reduction/single-band-fourier-reduction/` to this calculation owner.
- [x] Create a file-by-file experiment → calculation destination/digest crosswalk in [`experiment-migration-crosswalk.md`](experiment-migration-crosswalk.md) and [`experiment-migration-manifest.json`](experiment-migration-manifest.json).
- [x] Confirm that all 65 files have destinations or explicit dispositions: 53 exact duplicates, 10 adapted or integrated successors, and two provenance-only environment donors.
- [x] Complete consumer migration before treating the destination set as removal-ready.
- [x] Update every maintained consumer to the calculation path while preserving artifact digests and evidence-package identity.
- [x] Prove no maintained code, test, documentation, publication, or build depends on the experiment path; remaining occurrences are qualified migration or immutable provenance records.
- [x] Remove exactly the 65 manifest-bound experiment files after exact parity, predecessor recovery, and separate operator authorization.

## Historical inventory and retirement

- [x] Enumerate the four version-one executions and their former dispositions.
- [x] Identify the calculation-root and experiment-root filesystem surfaces.
- [x] Record a file-by-file digest crosswalk between the two former filesystem surfaces.
- [x] Verify all eight predecessor evidence-package copies, identities, and checksum catalogs before donor removal.
- [x] Bind the predecessor revision, tree, path, and recorded digests to direct Git-object recovery.
- [x] Reconcile the package verifier with Git-bound predecessor recovery without restoring the removed experiment tree.
- [x] Complete the donor removal review in [`experiment-removal-readiness.md`](experiment-removal-readiness.md).
- [x] Recalculate the direct result, independently verify it, render authenticated replacement figures, migrate all publication consumers, and retain a buildable technical report.
- [x] After separate operator authorization, remove all 45 files under `calculations/mathieu1d/runs/` and record only the compact recovery boundary in [`legacy-run-retirement.md`](legacy-run-retirement.md).
- [x] Confirm that the version-one `input.json` and three JSON schemas have no consumer, then remove them after separate authorization and record their recovery boundary in [`legacy-contract-retirement.md`](legacy-contract-retirement.md).

## Maintained ownership

- [x] Map each calculation-local source class to its maintained owner and classify the local package as adapted historical audit support.
- [x] Prove that maintained source, package tests, and calculation entry points do not import `calculations/mathieu1d/src/`.
- [x] Confirm that `input.json` and `run_01_experiment.py` use `ksdft2effmass.model_systems.mathieu1d.study`; keep the retained-run identity separate from a future direct successor.
- [x] Remove the duplicate calculation-local dependency authority, use the repository Python environment, and align the live-revision test without altering retained provenance identities.
- [x] Remove no other duplicate or retained surface; the exact donor removal was separately authorized and left calculation-owned retained bytes unchanged.

## Direct successor lifecycle

- [x] Define non-`.vN` calculation family `mathieu1d-finite-reduction` and fresh temporary-test execution identifier `direct-finite-reduction-n64`.
- [x] Define typed constructor-owned configuration and result records, including calculation family, execution identifier, evidence status, and claim boundary in the exact result wire.
- [x] Correlate parent, training, evaluation, transform, range, and tolerance inventories with the embedded configuration during typed result construction.
- [x] Define exact result-wire ownership, require canonical producer round trips, and reject semantically invalid typed values; verification hashes the exact admitted bytes.
- [x] Require canonical configuration bytes to equal the configuration embedded in the result before independent verification.
- [x] Require rendering to reconcile the complete typed verification and projection with a fresh independent reconstruction before plotting.
- [x] Implement `run_01_calculation.py` as thin direct composition.
- [x] Implement a byte-owning independent `run_02_verification.py` that does not invoke the producer.
- [x] Implement authenticated `run_03_render.py` with a closed two-figure/report inventory: a complete four-panel technical view and compact publication summary.
- [ ] Define sealing and read-only package-verification contracts separately; this implementation performs neither action.
- [x] Establish named numerical and typed-wire parity against the selected predecessor channels.
- [x] After separate operator authorization, retain `executions/direct-finite-reduction-n64/` as an explicitly unsealed calculate → verify → render execution with dirty-worktree Git qualification.
- [x] Add a buildable calculation-facing TeX/PDF technical report and exact local copies of both authenticated figures.
- [x] Migrate Ragasa2026a v1--v3 and the research monograph to direct calculation and authenticated rendering artifacts.
- [x] Remove predecessor provenance blocks from live publication manifests; recovery ownership belongs only to `legacy-run-retirement.md`.

## Calculation-code retirement

- [x] Receive explicit operator authorization to retire Periodic1D calculation-side code, including `calculations/mathieu1d/`.
- [x] Record the exact ten-path retirement inventory, SHA-256 digests, recovery revision, and calculation-local package tree in [`direct-successor-retirement.md`](direct-successor-retirement.md).
- [x] Verify all ten predecessor tests and the Git-bound publication-facing retained-package verifier before removal.
- [x] Verify zero-binary64-defect parity for the retained parent spectrum, both refinement sweeps, complete hopping coefficients, every mediated/direct range coefficient inventory, and every evaluation maximum-error value.
- [x] Retire the two legacy scripts, six-file calculation-local package, and two calculation-local tests.
- [x] After direct publication/report replacement and separate authorization, remove every predecessor run artifact from the live tree.

## Installed predecessor retirement

- [x] Receive explicit operator authorization to replace existing installed Mathieu1D source.
- [x] Replace the legacy package-root and `model_systems` exports with the direct typed lifecycle.
- [x] Record the exact six-file `study/` inventory, predecessor export-module digests, Git blobs, package trees, and recovery revision in [`installed-successor-retirement.md`](installed-successor-retirement.md).
- [x] Retire `python/src/ksdft2effmass/model_systems/mathieu1d/study/` without adding a compatibility facade or live historical-wire decoder.
- [x] Add direct public-export and legacy-absence tests.
- [x] Remove the temporary live predecessor-parity test after the predecessor run bytes were retired.
