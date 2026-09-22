# Quantum ESPRESSO 7.2 bundled examples campaign

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `quantumespresso.simulations.qe_examples`
- **Status:** `inactive`
- **Status detail:** Inventory-only campaign for 134 runnable source groups covering 149 bundled run_example scripts across 13 Quantum ESPRESSO 7.2 components. No bundled example is activated or authorized for execution.
- **Parent Task:** `quantumespresso.simulations`
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Coordinate separate preflight, execution-or-deferral, and evidence dispositions for every discovered run_example script group bundled with the inspected Quantum ESPRESSO 7.2 source snapshot.

## Relationships

### Task prerequisites

- `P2`

### External prerequisites

- None.

### Superseded by

- None.

## Authorized scope

- Maintain a source-relative inventory of bundled run_example scripts grouped by their cohesive example directory, with root-level named XSpectra scripts kept as separate runnable groups.
- Preflight one child independently for exact source identity, executable availability, inputs, pseudopotentials and terms, dependencies, resources, retention, and protected-execution authority.
- Activate at most one child only after its exact authorization; keep all other children inactive or blocked.
- Retain compact execution and artifact provenance outside the upstream source tree and classify all observations as bundled-example learning evidence.
- Review campaign-wide portability and integration findings only after each child has an explicit execution or deferral disposition.

## Completion criteria

- All 134 runnable groups covering all 149 discovered scripts have durable evidence-backed execution or deferral dispositions.
- Each attempted invocation has exact source, executable, input, pseudopotential, command, attempt, stream, runtime, exit, and artifact provenance.
- The campaign review separates reusable software findings from unsupported scientific, production, convergence, validation, or acceptance claims.
- No child is activated automatically and no upstream source tree is used as a mutable run workspace.

## Exclusions

- This campaign does not itself authorize Quantum ESPRESSO, MPI, Wannier90, network, remote, cluster, cloud, or other protected execution.
- It does not adopt bundled pseudopotentials, dependencies, numerical settings, material systems, or workflows as project defaults.
- It does not copy upstream example assets into the repository or imply that their licenses cover separately distributed pseudopotentials or downloaded data.
- It does not establish production readiness, numerical verification, scientific validation, uncertainty quantification, or human acceptance.

## Authority references

- `docs/computational/quantumespresso.simulations.qe_examples.md`
