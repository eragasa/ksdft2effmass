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

## Inventory and preservation

- [x] Enumerate the four immutable `v1` executions and their dispositions.
- [x] Identify the calculation-root and experiment-root filesystem surfaces.
- [x] Identify the retained schemas, execution-source surfaces, manifests, reports, and figures.
- [x] Record a file-by-file digest crosswalk between the two live filesystem surfaces.
- [x] Record both publication manifests and every maintained path consumer in [`experiment-removal-readiness.md`](experiment-removal-readiness.md).
- [x] Verify all eight retained evidence-package copies, identities, and checksum catalogs without rewriting files.
- [x] Bind the predecessor revision, tree, path, and recorded digests to direct Git-object recovery.
- [x] Reconcile the maintained package verifier with Git-bound predecessor recovery without restoring the removed predecessor tree or changing retained bytes.
- [x] Complete the non-destructive removal review in [`experiment-removal-readiness.md`](experiment-removal-readiness.md).

## Maintained ownership

- [x] Map each calculation-local source class to its maintained owner and classify the local package as adapted historical audit support.
- [x] Prove that maintained source, package tests, and calculation entry points do not import `calculations/mathieu1d/src/`.
- [x] Confirm that `input.json` and `run_01_experiment.py` use `ksdft2effmass.model_systems.mathieu1d.study`; keep the retained-run identity separate from a future direct successor.
- [x] Remove the duplicate calculation-local dependency authority, use the repository Python environment, and align the live-revision test without altering retained provenance identities.
- [x] Remove no other duplicate or retained surface; the exact donor removal was separately authorized and left calculation-owned retained bytes unchanged.

## Direct successor lifecycle

- [ ] Define a non-`.vN` calculation-family and fresh execution identity for a successor.
- [ ] Define typed constructor-owned configuration and result records.
- [ ] Define exact result-wire bytes and reject noncanonical or semantically invalid values.
- [ ] Implement `run_01_calculation.py` as thin direct composition.
- [ ] Implement a byte-owning independent `run_02_verification.py` that does not invoke the producer.
- [ ] Implement authenticated `run_03_render.py` with a closed figure/report inventory.
- [ ] Define sealing and read-only package-verification contracts separately.
- [ ] Establish named numerical and typed-wire parity against the selected predecessor channels.
- [ ] Create or retain no successor execution until its protocol and evidence policy are reviewed.
