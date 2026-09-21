# QE 7.2 bundled PHonon Image_example example

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `quantumespresso.simulations.qe_examples.phonon.image-example`
- **Status:** `blocked`
- **Status detail:** Inventory-only Task for the bundled Quantum ESPRESSO 7.2 source group `PHonon/examples/Image_example`. No script has been invoked by this Task. Exact source, executable, input, pseudopotential, dependency, resource, retention, and protected-execution preflights remain required.
- **Parent Task:** `quantumespresso.simulations.qe_examples`
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Preflight and, only after exact protected-execution authorization, execute or deliberately defer the Quantum ESPRESSO 7.2 bundled example group `PHonon/examples/Image_example` containing `PHonon/examples/Image_example/run_example`, `PHonon/examples/Image_example/run_example_1`.

## Relationships

### Task prerequisites

- `P2`
- `quantumespresso.simulations.integration`

### External prerequisites

- `bundled_example_preflight_completed`
- `local_execution_resource_authorization`
- `pseudopotential_selection_and_license`
- `qe_7_2_bundled_example_execution_authorization`
- `qe_7_2_source_identity_verified`

### Superseded by

- None.

## Authorized scope

- Inventory source group `PHonon/examples/Image_example` and candidate script(s): `PHonon/examples/Image_example/run_example`, `PHonon/examples/Image_example/run_example_1`.
- Inspect the script, referenced inputs, executables, pseudopotentials, downloads, environment assumptions, expected cost, and output behavior without executing it.
- If separately authorized, copy the minimum required assets into an isolated ignored run tree and invoke only the exact preflighted script or explicitly bounded constituent commands.
- Retain exact source and executable identities, inputs, pseudopotential identities and terms, commands, attempts, streams, runtimes, exit states, and compact artifact inventories.
- Record a completed, failed, unsupported, or deliberately deferred learning disposition without automatically activating another bundled example.

## Completion criteria

- Every candidate script in this source group has an explicit evidence-backed execution or deferral disposition.
- Any invocation is covered by exact protected-execution authorization and remains within its declared resource and retry envelope.
- Retained evidence distinguishes bundled-example behavior from project numerical verification, production convergence, scientific validation, and human acceptance.
- No large native output, restart state, wavefunction, charge density, dense matrix, or ambient source-tree mutation is committed to Git.

## Exclusions

- This Task record does not authorize execution, dependency installation, pseudopotential download, network access, remote computation, or source-tree mutation.
- Bundled settings and outputs do not override project specifications or become production defaults.
- A successful bundled example does not establish scientific correctness, cross-version equivalence, or support for its material system.
- Automatic retries, successor activation, and unbounded execution are prohibited.

## Authority references

- `docs/computational/quantumespresso.simulations.qe_examples.md`
