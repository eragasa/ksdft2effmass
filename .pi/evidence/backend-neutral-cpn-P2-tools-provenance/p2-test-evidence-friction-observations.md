# P2 test-evidence friction observations

Status: **contemporaneous process observation; no implementation activated**

Repository boundary observed through revision
`1327e279daa8ba9e431b82aa58bc51b65780ff41` on `dev`.

## Purpose and authority boundary

This record captures workflow friction observed during the bounded P2-A02,
P2-A03, and P2-A04 Python test-evidence corrections. It is descriptive evidence
for the inactive `TEST-EVIDENCE-CONVENTIONS-2` backlog proposal. It does not
change accepted test conventions, invalidate a cleared audit item, advance the
active P2 queue, authorize harness implementation, or weaken any completion
gate.

No prospective timing instrument was active for these corrections. This record
therefore does not estimate elapsed time, token use, labor cost, defect rate, or
causal effect. It distinguishes controls worth preserving from candidate
accidental friction based on versioned commands, records, and correction
boundaries.

## Controls worth preserving

The following work protected an accepted boundary and should not be removed
merely to reduce command or record volume:

- explicit `class_owned` or `artifact_owned` primary ownership;
- complete one-to-one migration of historical pytest nodes;
- unique, stable evidence IDs and explicit semantic parameter IDs;
- independent human judgment about cohesion, oracle quality, lifecycle meaning,
  and requirement completeness;
- focused production-source nonmutation checks;
- exact scoped pytest, Ruff, mypy, schema/fixture, serialization, and public API
  checks where applicable; and
- durable queue, task, chain, completion, and Git boundary state.

These controls preserve traceability, prevent silent production changes, and
separate structural PASS from semantic, numerical, scientific, UQ, provenance,
and human-acceptance claims.

## Candidate accidental friction

### Validator and formatter interoperability

The `ExternalExecutionOutcome` artifact owner required a fully qualified raw
module opening. That exact opening exceeded the ordinary Ruff line limit. A
blanket E501 suppression initially passed the structural validator and Ruff but
later failed the aggregate P2-A03 rule prohibiting file-level suppression. The
bounded resolution retained the exact structural opening and used a targeted
closing-line suppression.

The underlying ownership and formatting controls were useful; discovering a
compatible spelling through a stop/resume cycle was accidental friction. A
validator/formatter fixture should cover long fully qualified artifact names.

Evidence:

- `p2-a03-external-execution-result-partial-correction.md`;
- `p2-a03-completion.json`; and
- `p2-a03-parent-verification.md`.

### Repeated scoped command assembly

Each file correction manually assembled closely related commands for structural
validation, pytest collection, focused pytest, diagnostic coverage, Ruff, mypy,
public API or serializer regressions, production nonmutation, evidence-ID
uniqueness, and `git diff --check`.

The individual checks remain necessary, but their repeated manual assembly is a
candidate for a generated command manifest derived from explicit ownership and
supplied paths.

### Record synchronization

One bounded correction may require synchronized ownership, migration, progress,
queue, task, chain, completion, and parent-verification records. This is useful
external memory, but manual synchronization creates opportunities for stale
counts, stale next-item language, or conflicting active-item state.

A future tool could validate or generate derived synchronization while leaving
the authoritative human finding and queue transition explicit.

### Count reconciliation

The structural validator reports test functions, evidence owners, helpers,
parameterized functions, and static parameter cases. Pytest separately reports
expanded collected cases. These counts answer different questions, but repeated
manual reconciliation and explanation is avoidable.

A scoped result format could retain both count classes, label them explicitly,
and verify that all migration successors appear in actual collection.

### Aggregate consistency orchestration

The final P2-A03 consistency gate required structural validation plus separate
scripts or commands for unique IDs, prohibited test names, file-level Ruff
suppression, private helpers, ownership, migration completeness, pytest,
coverage, Ruff, mypy, production nonmutation, and diff cleanliness.

The checks should remain separate internally, but one supplied-path aggregate
entry point could produce one structured result without becoming a semantic
oracle or broad repository replay.

### Declarative enum coverage

`ArtifactLocationKind` and `ManifestState` have declaration-time enum members
but no executable method bodies owned by the classes. Coverage correctly reports
no missing class statements or branches, yet aggregate module percentages are
low because unrelated record classes are intentionally not run.

For such declarations, a scoped diagnostic should report class-body coverage as
`not_applicable` or “no executable body” rather than encouraging unrelated tests
to inflate module coverage.

Evidence:

- `p2-a04-artifact-location-kind-partial-correction.md`; and
- `p2-a04-manifest-state-partial-correction.md`.

### Exact migration schema and rationale placement

The structural validator requires the migration input to have exact
schema-version-1 keys. Adding rationale or genuinely-new-owner metadata directly
to that JSON causes deterministic rejection. Exact schema validation is useful,
but rationale then has to be duplicated or placed manually in a progress record.

A separately validated companion format could retain the exact migration map
while giving rationale and new-owner declarations one canonical location.

### Environment warning noise

Every focused `uv` command emitted a warning that the active `VIRTUAL_ENV` did
not match the project environment path. The commands still passed, but repeated
nonactionable warning text obscured concise validation output. Runner-level
environment normalization or one retained warning would improve signal without
changing test behavior.

## Proposed disposition

Record these items under inactive backlog proposal
`TEST-EVIDENCE-CONVENTIONS-2`. Any implementation requires separate activation,
writer ownership, focused fixtures, deterministic validation, and review. The
proposal is not a prerequisite for P2 and must not interrupt or retroactively
reinterpret the active file-by-file audit.

Potential implementation order, if later authorized:

1. validator/formatter interoperability fixtures;
2. unified scoped result and count reconciliation;
3. generated command manifests and aggregate entry point;
4. control-record synchronization validation;
5. declarative enum coverage classification;
6. migration-rationale companion schema; and
7. runner warning normalization.
