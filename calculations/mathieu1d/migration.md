# Mathieu1D canonical-infrastructure migration

This is the distributed checklist for the calculation inventory in
[`README.md`](README.md). A checked item records only the stated migration fact; it does
not establish scientific validation, authorize evidence replacement, or permit retained
bytes to change.

## Experiment-tree migration

- [x] Assign all 65 tracked files under `experiments/periodic-reduction/single-band-fourier-reduction/` to this calculation owner.
- [ ] Create a file-by-file experiment → calculation destination/digest crosswalk.
- [ ] Migrate every protocol, schema, script, source, test, run, and evidence file not already byte-identical here.
- [ ] Update every maintained consumer to the calculation path.
- [ ] Prove no maintained code, test, documentation, publication, or build depends on the experiment path.
- [ ] Remove the experiment files only after exact parity, predecessor recovery, and separate authorization.

## Inventory and preservation

- [x] Enumerate the four immutable `v1` executions and their dispositions.
- [x] Identify the calculation-root and experiment-root filesystem surfaces.
- [x] Identify the retained schemas, execution-source copy, manifests, reports, and figures.
- [ ] Record a file-by-file digest crosswalk between the two live filesystem surfaces.
- [ ] Record every publication manifest that consumes the publication-facing run.
- [ ] Verify every retained evidence-package identity and checksum catalog without rewriting files.
- [ ] Bind predecessor recovery paths and Git revisions in the successor design.

## Maintained ownership

- [ ] Map each calculation-local source class to its maintained owner or mark it evidence-only.
- [ ] Prove that maintained code does not import `calculations/mathieu1d/src/`.
- [ ] Reconcile the current input and direct scripts with `ksdft2effmass.model_systems.mathieu1d.study`.
- [ ] Remove no duplicate or retained surface without separate authorization.

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
