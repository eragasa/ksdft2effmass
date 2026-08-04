# PI Harness Architecture and Ownership

## Core principle

The harness owns reusable procedure. The project owns scientific meaning, local policy, and instantiated state.

This separation prevents the workflow infrastructure from silently acquiring assumptions about colored Petri nets, electronic-structure backends, pseudopotentials, numerical tolerances, or campaign authorization.

## Five ownership regions

### Generic Python functionality

`python/src/ksdft2effmass/harness/pi/` contains reusable Python objects and actions. Candidate responsibilities include structured task and checkpoint records, profile loading, resource resolution, deterministic validators, and structured diagnostic results.

Only capabilities approved by the harness contract belong here.

### Project-local Python functionality

`python/src/ksdft2effmass/harness/pi/local/` connects the generic interfaces to this repository. It may know about repository paths, evidence-ID namespaces, pytest markers, task-chain conventions, and project-specific validation policy.

It may depend on the generic layer. The generic layer may not depend on it.

### Generic textual resources

`harness/pi/` contains operational resources intended to move with a future harness package:

- `SKILL.md` files;
- agent-facing references;
- templates;
- JSON Schemas;
- resource manifests;
- parameterized validation resources.

These are executable governance resources rather than scientific or user-guide documentation.

### Project-local textual resources

`harness/local/` contains profiles and extensions that make the generic harness useful for `ksdft2effmass`. Project task IDs, scientific terminology, and local evidence prefixes belong here.

### Runtime state

`.pi/` contains instantiated state:

- tasks;
- chains;
- checkpoints;
- evidence;
- checksums;
- current authorization status.

Runtime state is neither library code nor reusable skill source.

## Dependency rules

The allowed dependency graph is

```text
.pi state ───────────────┐
                        ↓
harness/local ─→ ksdft2effmass.harness.pi.local
                        ↓
harness/pi ───→ ksdft2effmass.harness.pi
```

The following edges are prohibited:

```text
generic Python → local Python
generic Python → CPN/QE/Wannier domain modules
generic resources → project task IDs
generic resources → repository-relative paths
generic validators → implicit .pi discovery
```

All project context enters through an explicit profile or explicit caller-supplied path.

## Ownership tests

The boundary must be mechanically checked. At minimum, tests should detect:

- imports from generic code into `.local`;
- imports from generic code into scientific packages;
- project-specific strings in generic skills and schemas;
- resource discovery based on the current working directory;
- duplicate generic rules in local files;
- package contents that accidentally include local resources.

Human review remains necessary when a rule is syntactically generic but semantically tied to one project.

## Non-goals

Harness incubation does not authorize:

- a universal workflow engine;
- a scientific-backend plugin framework;
- replacement of the accepted CPN contract;
- migration of historical accepted evidence;
- QE or Wannier90 execution;
- package publication.

## Navigation

- [Index](./ksdft2effmass.harness.00.md)
- [Next: Contract and versioning](./ksdft2effmass.harness.02.md)
