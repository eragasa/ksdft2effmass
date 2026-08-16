<!-- Generated from SQLite control state; do not edit. -->
# Quantum ESPRESSO integration and local execution boundary

[Task index](index.md) · [Previous](./quantumespresso.simulations.graphene.md) · [Next](./quantumespresso.simulations.jdos-silicon.md)

## Status

`inactive`: Planned non-scientific prerequisite; inactive pending explicit implementation activation, ownership, DataObject/ActionObject design, software-verification evidence, and review.

## Objective

Implement and verify the initial ksdft2effmass.integration.quantumespresso anti-corruption boundary for exact input staging, root-confined local invocation, deterministic workspace manifests, separate stdout/stderr, terminal process records, native artifact discovery, and project failure mapping.

## Parent and prerequisites

- Parent: `quantumespresso.simulations`
- Depends on: `P2`

## Authority references

- docs/architecture/v2/ksdft2effmass/calculators/quantum-espresso.md
- docs/computational/quantum-espresso-tutorial-simulations.md

## Authorized scope

- Apply the DataObject/ActionObject model to narrowly owned QE serialization, staging, invocation, snapshot, artifact-discovery, and parsing behavior without a generic integration base class.
- Implement dry-run validation for root confinement, exact argument vectors, separate stream targets, snapshot scope, disk availability, and protected-execution authorization identities.
- Add software-verification evidence using deterministic test executables for success, nonzero exit, signal termination, missing executable, before/after snapshot failure, changing files, symlinks, atomic terminal records, cleanup, and nonmutation boundaries.
- Keep all Quantum ESPRESSO, optional scheduler, and third-party types out of project core public signatures and persisted neutral records.

## Completion criteria

- The ksdft2effmass.integration namespace and concrete quantumespresso package obey the documented inward dependency direction and introduce no generic base class or plugin registry.
- A dry run cannot invoke a scientific executable and reports the exact command, workspace, stream, and snapshot destinations.
- Deterministic test executables demonstrate separate stdout/stderr, terminal process records, before/after manifests, process-creation failure, and snapshot-failure behavior.
- No Quantum ESPRESSO, Wannier90, MPI, scheduler, remote service, or scientific calculation is used in software verification.
- Implementation, maintained tests, documentation, independent review, and final verification pass under explicit non-overlapping ownership.

## Exclusions

- This Task does not run Quantum ESPRESSO, Wannier90, PWTK, MPI workloads, remote jobs, or scientific calculations.
- It does not create AiiDA or Airflow packages, add optional dependencies, or adopt their runtime or persistence models.
- It does not define scientific settings, choose pseudopotentials, interpret numerical results, or grant execution authority.
- It does not add a shared integration base class, universal backend, engine hierarchy, service locator, or plugin framework.
- It does not commit ignored simulation artifacts.

## Historical source

No archived source.
