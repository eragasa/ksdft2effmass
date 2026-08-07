# Stabilize the validator-migration pilot

Status: completed under `.pi/chains/harness-simplification.chain.json`

Task identity: `harness-simplification.execution.validator-pilot-stabilization`

Starting revision: `83110dc294111f6ba0173312d0c4ed02448451b5` (`origin/dev` at task start; verified as a descendant of itself).

Authority: the current human instruction authorized this one bounded root-agent stabilization. It prohibited subagents, another integration review, broader validator migration, SQLite, live discovery, historical retirement, delegation validation, and scientific or protected work.

## Corrections

The task-local executable `.pi/tasks/validate_validator_migration_pilot.py` was removed without replacement. The completed pilot now specifies one direct focused pytest invocation in its task record; Ruff, mypy, imports, route, documentation, dependency, lockfile, ownership, chain, and diff checks remain parent verification. Executable maintained harness behavior remains owned by `python/src/ksdft2effmass/harness/pi/` and `python/src/ksdft2effmass/harness/pi/local/`, with the explicitly retained thin compatibility-wrapper locations under `harness/pi/validation/` and `harness/local/validation/`. Tests and controlled source fixtures remain test inputs, not completion drivers.

The accepted public validator API and validation semantics were not changed. No production decomposition was applied.

## `test_evidence.py` cohesion and ownership audit

Structural accounting:

- public DataObjects: `PythonTestEvidenceSource`, `PythonTestEvidenceRequest`;
- public ResultObjects: `PythonTestEvidenceFinding`, `PythonTestEvidenceValidationResult`;
- public ActionObjects: `ValidatePythonTestEvidence`;
- internal records: `ParameterCaseInventory`;
- module-level functions: 19;
- nested functions: one (`visit` inside `module_scope_statements`);
- intrinsic validation owners: each public frozen record's `__post_init__`;
- validation-policy owner: `ValidatePythonTestEvidence`, implemented through module-local static-analysis operations;
- parsing and AST analysis: source decoding/parsing, module/function documentation, naming, parameter inventory, evidence identifiers, static case counts, and source-level finding construction;
- ownership agreement: `load_ownership` parses the closed ownership payload, validates entries, and checks exact supplied-path coverage;
- migration agreement: `validate_migration` validates the closed inventories and complete one-to-one mapping;
- deterministic ordering and result construction: `execute` preserves request and traversal order, sorts keyed count tuples, and constructs the immutable result.

Required surface classification:

| Surface | Classification | Owner rationale |
|---|---|---|
| `claims_complete_equality`, `claims_complete_frozen` | ActionObject policy | Recognize maintained-evidence claims that trigger field-inventory rules. |
| `finding` | domain-independent mechanical helper | Constructs the fixed-severity finding representation. |
| `sections` | ActionObject policy | Enforces ordered, nonempty maintained-document sections. |
| `ParameterCaseInventory` | domain-independent mechanical helper | Internal immutable carrier for one AST-resolution outcome. |
| `assigned_names`, `module_scope_statements`, nested `visit`, `imported_module_names`, `module_assignments` | domain-independent mechanical helper | Traverse AST structure without independently selecting validation policy. |
| `inventory_mutation_findings`, `resolve_parameter_case_inventory` | ActionObject policy | Enforce the accepted named-inventory restrictions. |
| `semantic_parameter_id_problem`, `decorator_parameter_findings` | ActionObject policy | Enforce semantic ID and parameterization conventions. |
| `section_body`, `literal_string_inventory`, `parameter_case_ids` | domain-independent mechanical helper | Extract static representations consumed by owned policy. |
| `validate_file` | ActionObject policy | Applies the cohesive per-module convention set. |
| `static_parameter_case_count` | domain-independent mechanical helper | Derives the deterministic static count consumed by result construction. |
| `load_ownership` | separate cohesive action | Performs independently meaningful ownership-payload and coverage agreement inside the closed validator operation. |
| `validate_migration` | separate cohesive action | Performs independently meaningful migration-map agreement inside the optional closed input. |
| `ValidatePythonTestEvidence.execute` | ActionObject policy | Owns request-level orchestration, relational validation, ordering, counts, and result construction. |

No inspected surface is obsolete or duplicated. The two cohesive suboperations remain private implementation details of the single public static-evidence validation action: neither has a separate public request/result contract or independent caller, and moving them would change file placement without improving behavioral ownership. The remaining functions are either owner-local policy implementation or mechanical AST helpers permitted by the architecture. Splitting the 1,593-line module solely by length would obscure its one domain owner, so the module is retained intact.

## Review-dispatch truth and successor contract

The intended pilot policy was one final integration review. The interface visibly displayed four completed identical assignments. Local durable mission artifacts identify one pilot review run (`233ade96`), while the committed repository has no run-identity ledger sufficient to map every displayed assignment or prove an exact count. The execution count is therefore indeterminate, duplicate dispatch is recorded as a defect, and duplicate outputs are not independent evidence and must not be merged or voted.

The inactive successor `harness-simplification.execution.review-dispatch-idempotency` must implement an atomically claimed immutable assignment identity over:

```text
task_id
reviewer_role
reviewed_revision
normalized_scope_hash
review_round
```

`normalized_scope_hash` is the digest of a deterministic, versioned canonical scope representation. The minimum behavior is:

```text
no matching assignment       -> one launch permitted
matching assignment active   -> attach or wait; no new launch
matching assignment complete -> reuse durable handoff
matching assignment failed   -> stop; retry requires a new attempt identity
```

A retry retains the same review round unless a new round is explicitly authorized. The successor must choose an atomic persistence boundary before implementation; this task deliberately creates no partial JSON ledger and performs no SQLite work.

## Shared command discipline

The current durable-agent loader appends each agent record but has no repository-defined include mechanism for one harness-only shared prompt fragment. The authoritative shared wording is therefore maintained in `docs/harness/ksdft2effmass.harness.010.030.030.md` and temporarily repeated, without expansion, in only the five durable harness agent records.

## Final control state

`active_task` is `null`; automatic successor activation is disabled. Review-dispatch idempotency, live discovery, historical retirement, delegation validation, and evidence/SQLite remain inactive and unauthorized. No scientific or protected work was activated.
