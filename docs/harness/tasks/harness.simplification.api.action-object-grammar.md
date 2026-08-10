<!-- Generated from SQLite control state; do not edit. -->
# Normalize public ActionObject grammar

[Task index](index.md) · [Previous](./harness.simplification.agents.delegation-validation.md) · [Next](./harness.simplification.control.successor-selection.md)

## Status

`completed`: completed

## Objective

Establish and migrate the repository-wide public ActionObject naming grammar:

```text
<DataObject-or-operation-target><Actionizer>
```

The final agent noun identifies the owned operation, for example `Validator`, `Resolver`, `Evaluator`, `Serializer`, `Deserializer`, `Loader`, `Auditor`, `Inspector`, `Preparer`, `Recorder`, `Refresher`, `Adapter`, `Selector`, `Comparator`, `Analyzer`, `Differencer`, `Verifier`, `Correlator`, `Enabler`, or `Firer`. Avoid verb-first names and vague suffixes such as `Manager`, `Handler`, and `Processor`.

Examples include `ResourceManifestValidator`, `CheckpointDecisionResolver`, `ChainStateEvaluator`, `JsonRecordSerializer`, `EvidenceIdentifierAuditor`, `HumanReviewPreparer`, and `HumanReviewDecisionRecorder`.

## Parent and prerequisites

- Depends on: `harness-simplification.evidence.audit-action-conformance`

## Authority references

- .pi/chains/harness-simplification.chain.json
- harness/archive/task-control-v1/tasks/harness.simplification.api.action-object-grammar.md

## Authorized scope

- Establish and migrate the repository-wide public ActionObject naming grammar:
- Human decision: this is pre-release software with no public API consumers requiring compatibility preservation. Apply hard renames with no compatibility aliases or deprecation period. Preserve already conforming suffix-style names and migrate only the accepted nonconforming inventory. Use old/new mappings only where an owning maintained-evidence contract requires node-identity migration; do not create API-compatibility ceremony. Synchronize source, tests, documentation, skills, wrappers, schemas, fixtures, manifests, and public exports. The evidence-subpackage API must follow the accepted grammar.

## Completion criteria

- Completion requires the accepted convention in every owning surface, complete affected-object inventory, deterministic naming checks, only contract-required maintained-evidence node mappings, synchronized public surfaces, relevant tests and documentation checks, one consolidated review, and final human acceptance when required.

## Exclusions

- Human decision: this is pre-release software with no public API consumers requiring compatibility preservation. Apply hard renames with no compatibility aliases or deprecation period. Preserve already conforming suffix-style names and migrate only the accepted nonconforming inventory. Use old/new mappings only where an owning maintained-evidence contract requires node-identity migration; do not create API-compatibility ceremony. Synchronize source, tests, documentation, skills, wrappers, schemas, fixtures, manifests, and public exports. The evidence-subpackage API must follow the accepted grammar.
- This Task does not change DataObject ownership, operation behavior, scientific meaning, wire formats, dependencies, or runtime policy merely to obtain naming consistency.
- This Task does not authorize unrelated API redesign, add dependencies, introduce SQLite, perform protected execution, or activate successors.

## Historical source

`harness/archive/task-control-v1/tasks/harness.simplification.api.action-object-grammar.md` (`sha256:52c82b69dbf76b633c4c8546aa788eab12566195f9c0ad7e203df28b71ada561`)
