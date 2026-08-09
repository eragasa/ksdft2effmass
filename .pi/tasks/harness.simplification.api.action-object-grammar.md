# Normalize public ActionObject grammar

Status: proposed_inactive

Task identity: `harness.simplification.api.action-object-grammar`

Prerequisite: `harness-simplification.agents.delegation-validation:completed`

## Objective

Establish and migrate the repository-wide public ActionObject naming grammar:

```text
<DataObject-or-operation-target><Actionizer>
```

The final agent noun identifies the owned operation, for example `Validator`, `Resolver`, `Evaluator`, `Serializer`, `Deserializer`, `Loader`, `Auditor`, `Inspector`, `Preparer`, `Recorder`, `Refresher`, `Adapter`, `Selector`, `Comparator`, `Analyzer`, `Differencer`, `Verifier`, `Correlator`, `Enabler`, or `Firer`. Avoid verb-first names and vague suffixes such as `Manager`, `Handler`, and `Processor`.

Examples include `ResourceManifestValidator`, `CheckpointDecisionResolver`, `ChainStateEvaluator`, `JsonRecordSerializer`, `EvidenceIdentifierAuditor`, `HumanReviewPreparer`, and `HumanReviewDecisionRecorder`.

## Authoritative surfaces

The implementation task must synchronize:

1. `.pi/skills/design-data-action-objects/references/data-action-architecture.md` as the complete architecture convention;
2. `.pi/skills/design-data-action-objects/SKILL.md` as concise operational guidance;
3. `docs/development/source-documentation.rst` as the public API documentation requirement; and
4. deterministic public-API naming verification.

## Migration boundary

Human decision: this is pre-release software with no public API consumers requiring compatibility preservation. Apply hard renames with no compatibility aliases or deprecation period. Preserve already conforming suffix-style names and migrate only the accepted nonconforming inventory. Use old/new mappings only where an owning maintained-evidence contract requires node-identity migration; do not create API-compatibility ceremony. Synchronize source, tests, documentation, skills, wrappers, schemas, fixtures, manifests, and public exports. The evidence-subpackage API must follow the accepted grammar.

This Task does not change DataObject ownership, operation behavior, scientific meaning, wire formats, dependencies, or runtime policy merely to obtain naming consistency.

## Completion gates

Completion requires the accepted convention in every owning surface, complete affected-object inventory, deterministic naming checks, only contract-required maintained-evidence node mappings, synchronized public surfaces, relevant tests and documentation checks, one consolidated review, and final human acceptance when required.

## Exclusions and stop boundary

This record does not activate the migration, authorize unrelated API redesign, add dependencies, introduce SQLite, perform protected execution, or activate successors. It remains proposed and inactive until separately authorized.
