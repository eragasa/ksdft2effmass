---
document_id: ksdft2effmass.harness.002.001.006
task_id: harness-simplification.agents.executable-tool-placement-contract
parent: ksdft2effmass.harness.002.001.000
status: current
sphinx: excluded
---

# Executable harness-tool placement contract

This accepted contract governs conversion of ad hoc harness scripts into maintained deterministic tools. The Python test-evidence validator and bounded task-state inspector described below are completed maintained tools. They do not implement SQLite or authorize scientific or protected work.

## Placement and dependency direction

| Surface | Owner |
|---|---|
| `python/src/ksdft2effmass/harness/pi/` | Reusable, project-neutral DataObjects, ResultObjects, ActionObjects, validation algorithms, and deterministic transformations. |
| `python/src/ksdft2effmass/harness/pi/local/` | Repository-specific composition, profiles, compatibility behavior, lifecycle policy, and explicit project routing. |
| `harness/pi/` | Generic non-executable schemas, manifests, descriptors, textual conventions, and fixtures. |
| `harness/local/` | Project-local non-executable profiles, extensions, manifests, compatibility declarations, and fixtures. |
| `python/tests/software_verification/ksdft2effmass/harness/pi/` | Generic maintained software-verification tests. |
| `python/tests/software_verification/ksdft2effmass/harness/pi/local/` | Project-local maintained software-verification tests. |

`ksdft2effmass.harness.pi.local` may depend on `ksdft2effmass.harness.pi`; the reverse dependency is prohibited. Generic code must not import local policy, task identities, implicit repository state, or scientific semantics. Callers supply every input and root explicitly; current-working-directory discovery is not a contract.

## Maintained-tool object model

A **DataObject** is a concrete immutable request, configuration, identity, or represented record. It owns only intrinsic invariants. A **ResultObject** is an immutable semantic specialization of DataObject:

```text
ResultObject ⊂ DataObject
```

This is a semantic relation, not a requirement for a nominal `DataObject` base class. Introduce no base class unless concrete shared behavior or typing requires one.

A stateless concrete **ActionObject** owns validation, transformation, serialization, or other nontrivial behavior and exposes a public `execute` boundary. Its inputs and dependencies are explicit DataObjects or constructor configuration, and its output is an immutable ResultObject. Structured issues or failures are data, deterministically ordered by the tool's declared contract. Small private functions may retain cohesive mechanical details; they must not hide policy or scientific meaning.

Every maintained tool declares concisely:

- stable identity and purpose;
- immutable request DataObject;
- ActionObject and public `execute` boundary;
- immutable ResultObject and structured issues or failures;
- explicit inputs, roots, filesystem reads, and deterministic output ordering;
- declared mutations, normally none;
- command-wrapper exit mapping, when exposed;
- environment assumptions;
- generic or project-local ownership; and
- the boundary of its scientific, numerical-verification, scientific-validation, and uncertainty-quantification claims.

Avoid reflective registries, service locators, plugin frameworks, hidden global state, implicit repository discovery, speculative abstractions, and public classes created only to eliminate every private helper. Nontrivial behavior must have one clear owner.

## Thin compatibility wrappers

Existing scripts under `harness/pi/validation/` and `harness/local/validation/` may temporarily remain as compatibility wrappers. A wrapper may only parse command arguments, construct public request DataObjects, invoke one public ActionObject, render its ResultObject deterministically, and translate the result to an exit status. It must not retain validation algorithms, repository discovery, hidden policy, or duplicate domain logic.

The migrated pilot retains this supported compatibility-command form:

```text
python/.venv/bin/python harness/pi/validation/validate_python_test_evidence.py \
  --ownership OWNERSHIP.json [--migration-map MIGRATION.json] TEST_MODULE.py [...]
```

The package does not implement a `-m` entry point. Maintained Python callers instead use the public package API:

```python
from ksdft2effmass.harness.pi import (
    PythonTestEvidenceRequest,
    PythonTestEvidenceSource,
    ValidatePythonTestEvidence,
)

request = PythonTestEvidenceRequest(
    sources=(PythonTestEvidenceSource("test__example.py", source_bytes),),
    ownership_path="ownership.json",
    ownership_payload=ownership_bytes,
)
result = ValidatePythonTestEvidence().execute(request)
```

Here `source_bytes` and `ownership_bytes` are caller-supplied `bytes`. No `just` installation, new CLI framework, or other dependency is required.

## Proportional execution classes

### Routine bounded work

Small prose or formatting corrections, narrow deterministic record cleanup, isolated test corrections, and checksum synchronization normally use the root agent or one qualified writer, exact bounded paths, focused validation, a concise handoff, and a commit when requested. A new chain, task, ownership manifest, documentation sweep, independent review, replay cycle, or checkpoint is not required by default. Escalate only for an observed conflict.

### Public-contract or cross-surface work

Public APIs or serialization and persisted schemas require an explicit contract, software-verification tests, and compatibility review. Generic/local boundaries, maintained-tool contracts, and multi-writer changes also use focused tests and documentation and one independent review when materially applicable. A durable task and exact non-overlapping ownership are added when their normal triggers apply. A human decision is required only when a genuine unresolved human-owned choice remains.

### Scientific, protected, or release work

Scientific meaning or acceptance, numerical-validation disposition, UQ conclusions, external scientific execution, credentials, scheduler actions, publication, and release use the applicable full repository controls and explicit human authorization. Technical capability, deterministic output, test success, or review never authorizes these actions.

These classes prevent maintained tooling from automating governance ceremony that the risk and observed facts do not require.

## Delegation proportionality

Delegation is optional, not a completion requirement. Use one agent directly when work is cohesive. Use multiple writers only for genuinely independent, non-overlapping surfaces, and use a reviewer only when independence materially improves confidence. Context isolation is a legitimate reason to delegate. Delegation never expands authority, and historical role availability never justifies spawning. Each delegated run returns a concise durable handoff. Routine work must not create permanent records solely to prove delegation occurred.

### Shared subagent command discipline

Subagents use native read, search, edit, and write operations directly and use Bash only for existing focused commands. They do not generate Bash scripts, Python heredocs, or temporary command programs; run unbounded diffs or flood full output; or inspect large files except in bounded sections. They keep one command session active, wait for it to complete before launching another command, avoid rerunning unchanged commands, and report a maintained-tool requirement instead of generating repeated command fragments.

The current durable-agent loader has no repository-defined include mechanism for injecting one harness-only shared prompt fragment. Until that capability exists, the paragraph above is the authoritative shared wording and the same bounded rule is repeated only in the five durable harness agent records.

## Bounded task-state inspection

`TaskStateInspectionRequest`, `InspectTaskState`, and `TaskStateInspectionResult` provide one root-confined operation for reconstructing the declared durable repository state of an exact task. The request contains an explicit absolute repository root, one root-relative chain path, and one exact task identity. The action reads only that chain and exact task-record, ownership-manifest, completion-validator, artifact, run-record, and handoff-record paths declared by the selected chain entry or ownership manifest. It rejects absolute, traversal, escaping, missing, non-file, and symlinked references and performs no recursive directory search, Git command, subprocess, network access, temporary-log inspection, session inspection, or mutation.

The project-local command wrapper is:

```text
python/.venv/bin/python -m ksdft2effmass.harness.pi.local.inspect_task_state \
  --root . \
  --chain .pi/chains/harness-simplification.chain.json \
  --task-id harness-simplification.agents.validator-migration-pilot
```

The command emits deterministic JSON. Exit status `0` means inspection completed with no invalid durable references, `1` means declared repository state is invalid or unresolved, `2` means request construction failed, and `3` is reserved for an unexpected command-boundary failure. Undeclared runtime or session history is a limitation, not an invalid reference.

This command replaces improvised recursive `find` or `rg` reconstruction. It does not infer artifacts from task prose and does not search `.pi`, Git history, worktrees, temporary logs, sessions, or unrelated evidence. `not_declared`, `declared_missing`, and `inspected` distinguish durable run and handoff declaration state. Interactive observations remain separate from repository facts.

For the completed validator pilot, the inspector reports `completed`, one declared reviewer role, and `not_declared` for both durable run and handoff records. The intended policy was one final review; the human observed four duplicate completed reviewer assignments in the interface. That runtime observation is outside declared repository state, the exact launch count is not reconstructible by this tool, and the duplicate assignments are not independent review evidence.

## Completed validator-migration pilot

Under the completed task `harness-simplification.agents.validator-migration-pilot`, the implemented pilot completes the first bounded migration under this contract. Reusable behavior now belongs to the generic `ksdft2effmass.harness.pi.test_evidence` module and is exported from `ksdft2effmass.harness.pi` through these public types:

- `PythonTestEvidenceSource`, an immutable representation of one caller-supplied path, byte payload, and caller-observed read outcome;
- `PythonTestEvidenceRequest`, an immutable closed request containing explicit sources, ownership JSON bytes, and optional migration-map JSON bytes;
- `PythonTestEvidenceFinding`, an immutable structured `TE.*` diagnostic;
- `PythonTestEvidenceValidationResult`, an immutable result containing status, findings, paths, compatibility counts, and explicit claim boundaries; and
- `ValidatePythonTestEvidence`, a fieldless stateless ActionObject whose `execute(request)` method returns the validation result.

The package boundary is pure with respect to external state: it parses and validates only the bytes and metadata supplied in the request. It performs no filesystem reads, root or current-working-directory discovery, Git inspection, subprocess execution, or mutation. The old `harness/pi/validation/validate_python_test_evidence.py` path remains a controlled thin compatibility wrapper. It parses explicit arguments, reads only those named paths, constructs the public request, invokes `ValidatePythonTestEvidence.execute`, renders deterministic JSON, and maps `PASS` to exit status 0 and `FAIL` to exit status 1. Focused software-verification tests cover the public objects and action, generic dependency direction, and controlled wrapper/API agreement.

The pilot intended one final integration review, but observed execution did not reliably enforce that policy. The interface displayed four completed assignments with identical review text and reviewer identity. Local durable mission artifacts identify one pilot review run, while the committed repository lacks enough run identity to reconstruct the exact execution count. Duplicate dispatch is therefore an orchestration defect. Duplicate outputs are not independent review evidence and are neither merged nor voted.

Validation is structural software verification of the supplied Python source and metadata representation. It covers the maintained static syntax, documentation, ownership, evidence-identifier, parameter-inventory, and optional migration-map conventions and reports deterministic findings and inventory counts. A passing result does not establish oracle independence, mathematical or property/surface correctness, test cohesion, tolerance adequacy, numerical or scientific validation, uncertainty quantification, or human acceptance.

The compatibility wrapper is retained temporarily; this pilot does not promise its permanent public availability or retire historical command records. Broader validator migration, live discovery, historical-agent retirement, delegation validation, SQLite or other evidence storage, scientific work, protected execution, and release work remain deferred and unauthorized.

## Navigation

- **Index:** [Harness documentation](ksdft2effmass.harness.000.000.000.md)
- **Parent:** [First harness simplification round](ksdft2effmass.harness.002.001.000.md)
- **Previous:** [Simplify durable project roles](ksdft2effmass.harness.002.001.005.md)
- **Next:** [Maintained execution interface](ksdft2effmass.harness.002.001.007.md)
