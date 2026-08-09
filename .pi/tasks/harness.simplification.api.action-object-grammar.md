# Normalize public ActionObject grammar

Status: implementation_complete_awaiting_human_acceptance

Task identity: `harness.simplification.api.action-object-grammar`

Authority: current human instruction authorized removal of the unrelated delegation-validation prerequisite and activation of this bounded Task.

Prerequisite: `harness-simplification.evidence.audit-action-conformance:completed`

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

## Implemented result

- inventoried 43 public `execute()` ActionObjects: 28 hard-renamed, 13 already conforming, and 2 evidence-package names explicitly deferred to `harness.simplification.evidence.naming` to avoid a double rename;
- removed old live exports and compatibility aliases;
- migrated generic and project-local source, wrappers, schemas, resources, skills, documentation, manifests, and public tests;
- split the 15 project-local public ActionObjects into class-owned `test__<ActionObject>.py` modules;
- standardized maintained evidence docstrings as `Label: value` paragraphs with exactly one blank line and added deterministic enforcement;
- retained 73 one-to-one predecessor node mappings and added nine new evidence nodes without predecessors; and
- retained the inventory and task-local ownership records under `.pi/evidence/action-object-grammar/`.

## Validation and residual limitations

Ruff, mypy, structural maintained-evidence validation, the repository evidence gate, evidence-identifier audit, resource hash agreement, Sphinx warnings-as-errors, task-state checks, and diff checks pass. The affected suite passes, as do 2,869 tests when the two wheel tests are excluded. The full 2,871-node run reaches only two wheel-test setup errors because `python/.venv` has no `pip`; no test assertion fails after the wrapper-fixture correction.

The H3 resource validator still reports its two pre-existing generic/local leakage and stale manifest-version-boundary findings; this Task did not redefine those unrelated accepted resource boundaries. Passing software checks establish no scientific validation or UQ.

## Exclusions and stop boundary

This Task does not authorize unrelated API redesign, add dependencies, introduce SQLite, perform protected execution, or activate successors.
