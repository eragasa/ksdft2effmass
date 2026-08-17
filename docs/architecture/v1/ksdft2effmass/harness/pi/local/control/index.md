# `ksdft2effmass.harness.pi.local.control` package in v1

## Implemented compilation path

V1 does not expose the normalized `HarnessSourceSnapshot → HarnessState → HarnessArtifactSet` object model as public compiler objects. Compilation exists inside the control migration and verification implementation.

```mermaid
flowchart TB
    python["Configured Python test sources"] --> conformance["Resolve canonical conformance inputs"]
    conformance --> repository_validation["Repository conformance validation"]
    conformance --> resolve["Compose projection inputs"]
    inputs["Other explicit canonical inputs"] --> resolve
    resolve --> build["Build candidate database and projections"]
    build --> validate["Validate candidate"]
    validate --> mode{"Operation"}
    mode -->|sync| publish["Publish maintained artifact set"]
    mode -->|check| compare["Compare with maintained artifact set"]
```

## Implemented owners

| Package or module owner | Responsibility |
|---|---|
| Private projection request | Explicit repository root and canonical evidence/resource inputs |
| Private projection synchronizer | Candidate construction, validation, and publication orchestration |
| Private projection verifier | Candidate reconstruction and read-only comparison |
| `local.conformance_inputs` | Canonical Python test-module, profile, and migration-map selection shared by validation and projection composition |
| `local.input_selection` | Root-confined mechanical selection for explicit project-local files and directories |
| `local.control.inputs` | Composition of conformance inputs with the remaining canonical projection inputs |
| `local.control.generation` | Candidate SQLite and projection construction |
| `HarnessValidator` | Repository-level validation composition |
| Domain validators | Task, checkpoint, resource, skill, and Python-conformance rules |

## State model

The effective normalized model is represented by candidate relational tables and in-memory generation records rather than one public immutable `HarnessState`. Source provenance is preserved through paths and identities, but not uniformly exposed as a field-level provenance object model.

## Validation composition

`HarnessValidator` runs six ordered checks:

1. Python conformance;
2. resources;
3. Task graph;
4. checkpoints;
5. skills; and
6. control state.

The source-aware verifier separately reconstructs generated control state and compares it with maintained projections. Repository conformance and projection agreement are related but distinct claims.

## Determinism

The implementation compares normalized table content and a semantic digest, deterministic SQL, manifest content, schema version, integrity, foreign keys, and projector-owned files. Raw SQLite byte identity is diagnostic rather than the semantic contract.

## Limitations

- Loading, normalization, validation, projection, publication, and comparison are behaviorally separated but not all represented by public objects.
- Candidate generation combines compilation and projection concerns.
- The migrator owns more orchestration than a narrow synchronizer.
- Generated Task Markdown has been retired from `docs/`; Task JSON remains the maintained source.
- There is no validator composition protocol over one public `HarnessState`.

These limitations describe the implemented architecture and do not redefine it.

Generated database ownership and projection publication are detailed under
[`ksdft2effmass.harness.pi.local.dbcontrol`](../dbcontrol/index.md).
