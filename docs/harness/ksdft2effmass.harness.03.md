# PI Harness Python Implementation Boundary

## Incubation namespace

Generic Python functionality is incubated under

```text
python/src/ksdft2effmass/harness/pi/
```

Project-specific extensions are isolated under

```text
python/src/ksdft2effmass/harness/pi/local/
```

This placement allows the harness to mature inside the existing Python project while preserving a visible extraction boundary.

## Import discipline

Generic modules use relative imports internally:

```python
from .checkpoints import CheckpointRecord
from .validation import HarnessValidationResult
```

They should not use incubation-specific absolute imports internally:

```python
from ksdft2effmass.harness.pi.checkpoints import CheckpointRecord
```

Relative imports reduce the mechanical work required when the generic modules later move to an independent namespace.

## Prohibited generic imports

Generic harness code must not import:

- `ksdft2effmass.workflows.cpn`;
- electronic-structure domain objects;
- QE or Wannier adapters;
- SNAKES;
- modules under `.local`;
- repository-specific task definitions.

The local layer may import the generic harness and project-domain modules when it is implementing an explicitly project-owned adapter.

## Resource loading

Generic Python code must not infer resources from `Path.cwd()`, a Git root, or a fixed repository layout. It receives a resource root or resolved resource reference through the accepted contract.

During incubation, the caller may explicitly supply `harness/pi/`. After extraction, the same resource interface may use package resources without changing the higher-level contract.

## Path safety

Any action that resolves caller-supplied relative paths must enforce confinement to the approved root. Resolution must reject traversal outside that root, including normalized `..` segments and symlink escapes where relevant.

Path validation is software verification and security hardening. It does not establish scientific validity.

## Public API discipline

The public namespace should expose only accepted records and actions. It should not export:

- project-local adapters;
- mutable repositories;
- subprocess clients;
- scheduler handles;
- undocumented filesystem helpers;
- scientific workflow objects.

Every public class receives one class-owned software-verification module. Cross-language schemas and package boundaries receive explicitly named artifact- or boundary-owned modules.

## Extraction transition

The eventual package may use an external namespace such as `pi_harness`. A temporary compatibility facade may preserve current imports during migration, but it must not become a second implementation.

The intended transition is

```text
ksdft2effmass.harness.pi      → external generic package
ksdft2effmass.harness.pi.local → retained project adapter
```

The final distribution and import names remain an H5 package-readiness decision.

## Navigation

- [Previous: Contract and versioning](./ksdft2effmass.harness.02.md)
- [Index](./ksdft2effmass.harness.00.md)
- [Next: Skills and textual resources](./ksdft2effmass.harness.04.md)
