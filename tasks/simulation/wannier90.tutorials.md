# Wannier90 tutorial programs

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `wannier90.tutorials`
- **Status:** `inactive`
- **Status detail:** Generic Wannier90 tutorial umbrella. The version-pinned Wannier90 3.1.0 bundled-examples campaign is inactive; no tutorial execution or workspace creation is authorized.
- **Parent Task:** None.
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Coordinate version-pinned Wannier90 tutorial campaigns without conflating tutorial evidence with production Wannierization, convergence, numerical verification, or scientific validation.

## Relationships

### Task prerequisites

- `P2`

### External prerequisites

- None.

### Superseded by

- None.

## Authorized scope

- Contain separately versioned Wannier90 tutorial campaigns and preserve their exact source, executable, pseudopotential, workspace, execution, and evidence boundaries.
- Require exact protected-execution authority for each scientific invocation and prohibit automatic child or successor activation.
- Keep bundled examples, event-based upstream tutorials, project-owned tutorial examples, and production bulk-silicon Wannier calculations provenance-distinct.

## Completion criteria

- Every child campaign retains an explicit version and source identity and an execution-or-deferral disposition.
- No tutorial observation is substituted for production convergence, numerical verification, scientific validation, or human acceptance.
- No child is activated by parent containment or a static task-graph edge.

## Exclusions

- This umbrella does not authorize Quantum ESPRESSO, Wannier90, MPI, remote, cluster, cloud, network, or other protected execution.
- It does not select pseudopotentials, scientific settings, material systems, dependencies, tutorial sources, or production acceptance criteria.
- It does not adopt tutorial outputs, projections, windows, gauges, or energy references as project defaults.

## Authority references

- `docs/computational/wannier/wannier-tutorial-catalog.md`
- `docs/computational/wannier90-3.1.0-installation.md`
- `docs/computational/wannier90.tutorials.v3_1_0.md`
- `tasks/simulation/wannier90.tutorials.v3_1_0.json`
