# Mathieu1D direct evidence and failure policy

## Live evidence boundary

The only live Mathieu1D execution is
`executions/direct-finite-reduction-n64/`. Its admissible artifact graph is:

1. canonical typed configuration bytes;
2. canonical typed calculation-result bytes;
3. byte-owning independent verification and authenticated visualization-data bytes;
4. rendering metadata that binds the exact result, verification, figures, renderer, and
   technical-report snapshot; and
5. `UNSEALED.md`, which prevents the retained execution from being represented as sealed
   evidence.

Ragasa2026a and the research monograph bind these direct artifacts through their own
calculation-reference manifests. No predecessor result, checksum package, figure, source
manifest, schema, or run identifier is an admissible publication input.

## Verification and rendering admission

Verification must correlate canonical configuration bytes with the configuration
embedded in the exact result wire. It independently assembles the finite plane-wave and
periodic finite-difference fibers, evaluates explicit finite Fourier sums, and performs
weighted least squares without invoking `Mathieu1dAnalyzer` or a historical workflow.

Rendering is admitted only after:

- exact result SHA-256 correlation;
- canonical typed verification decoding;
- a passing complete verification inventory;
- a fresh independent reconstruction equal to the stored verification and projection;
- exact verification-script and visualization-source digest checks; and
- a closed two-figure inventory.

The renderer publishes its figure and report directories atomically and refuses to
overwrite a completed stage.

## Failure disposition

A calculation, typed round-trip, configuration correlation, independent comparison,
digest, figure inventory, PNG validation, report inventory, or no-overwrite failure
prevents a success disposition. Incomplete temporary directories are failures and cannot
be publication inputs.

Passing checks establish software behavior and finite numerical reconstruction only.
They do not establish continuum convergence, uncertainty quantification, material
validity, a universally adequate range, publication acceptance, sealing, release, or a
trusted timestamp.

## Removed predecessor boundary

Predecessor code and run artifacts are absent from the live tree. The compact Git
recovery locator in `legacy-run-retirement.md` is not a live evidence contract and must
not be used as a runtime or publication dependency.
