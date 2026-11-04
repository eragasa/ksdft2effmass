# `QePwResultAssembler`

## Ownership

`QePwResultAssembler` is KSD's effect-free final consistency gate for one local
Quantum ESPRESSO `pw.x` Workflow result. It does not enter or represent `bands.x`.

## Contract

The action consumes a reserved `ResultObjectIdentity`, the exact result-contract
version, and these immutable evidence owners:

- `QePwPublishedEvidence`;
- `QeDiagnosticReport`;
- `QeNativeOutputExtractionSpecification` and `QeNativeOutputManifest`;
- one closed `QeCalculatorOutcome`;
- `QeTerminalRecord`; and
- `QePublishedTerminalRecord`.

Success returns `QePwResult` directly. The assembler verifies preparation and
predecessor sources, stream identities, process and publication snapshots, provider
`execution.json` content and manifest identities, diagnostic configuration,
native-output entries, outcome consistency, terminal-record references, and the exact
terminal publication before constructing the Workflow-facing result.

There is no public correlated-evidence intermediate and no second result adapter.
`QePwResult` and its reachable QE-owned values are nested `BaseTypedRecord` owners.
Their `to_dict`/`from_dict` and `to_json`/`from_json` boundary supplies the
`quantum-espresso-simulations-result:1` payload without flattening the object graph or
routing PW results through the legacy tagged-node codec.

## Failure and claim boundary

Adaptation, publication, and result assembly share `QePwEvidenceFailureCode`.
`QePwResultAssemblyFailure` distinguishes preparation, diagnostic, native-output,
outcome, and terminal mismatches without inventing a partial successful result.

The action performs no filesystem mutation, process entry, retry, Workflow resolution,
scientific interpretation, convergence decision, or acceptance. Passing its software
checks establishes internal evidence consistency only.
