<!-- Generated from SQLite control state; do not edit. -->
# Harness simplification round two

[Task index](index.md) · [Previous](./harness.simplification.round-2.sqlite-hybrid-cutover.md) · [Next](./harness.simplify-2.adapter-retirement.md)

## Status

`active`: coordinating parent restored after R2.4 completed; R2.5 is prerequisite-eligible but inactive, R2.6 and R2.7 remain inactive, and automatic successor activation remains disabled

## Objective

Simplify the maintained harness so that a maintainer can change one policy—Task persistence, evidence naming, resource resolution, or wire serialization—without editing an orchestration monolith or synchronizing unrelated representations.

## Parent and prerequisites

- Depends on: `harness.simplification.round-2.sqlite-hybrid-cutover`
- External prerequisite: `explicit_activation`

## Authority references

- AGENTS.md
- harness/intake/harness.simplify-2.md

## Authorized scope

- R2.1 — Decompose `python/src/ksdft2effmass/harness/pi/local/control.py` into private records, schema, ingestion, projections, deterministic SQL export, verification, and thin migration ownership while preserving the small public migration surface, existing public verification exports, SQLite schema and semantic identity, and deterministic projections.
- R2.2 — Audit and decompose project-local adapters by relocating all nine implementations into five contract-specific modules while preserving all nine public imports, all nine `execute` signatures, and the compatibility facade; no adapter was removed.
- R2.3 — Make evidence authority and `routine` versus `claim_bearing` profile semantics explicit, derive one immutable `PythonTestModuleModel` through one AST pass and independent evidence rules, prepare evidence inputs for full reconstruction, correct 13 private implementation-class ownership declarations without renumbering evidence IDs, and keep inventory and SQLite evidence rows as projections.
- R2.4 — Decompose resource records, manifest semantics, resolution, refresh or projection, and skill-resource closure, and prepare explicit resource inputs for the same full `HarnessControlMigrator` reconstruction without creating another database writer or synchronization framework.
- R2.5 — Decompose `python/src/ksdft2effmass/harness/pi/validation.py` into canonical JSON support and explicit domain codecs whose dispatch layer routes wire kinds without owning domain mappings or changing persistence ownership.
- R2.6 — Consolidate every maintained live CLI script and entry point under `python/src/cli/`, preserve historical command evidence, and expose one explicit synchronization surface that delegates complete database construction and publication to the existing `HarnessControlMigrator`; exact command spellings remain an implementation decision.
- R2.7 — Compose evidence, resource, Task, wire, and other validation results, extract one narrow private control-generation builder shared by the existing public migrator and verifier, compare complete candidate artifacts with maintained state without publication, retire replay and duplicated cross-domain gates, and return one structured maintained validation result.
- Use one maintained synchronization flow: authorized repository edit, then explicit control synchronization command, then `HarnessControlMigrator`, then staged complete SQLite reconstruction, then schema, relationship, and projection validation, then failure-safe publication of SQLite and generated projections.
- Keep `HarnessControlMigrator` responsible for reconstructing, validating, and publishing maintained control state, and keep `HarnessControlVerifier` responsible for nonmutating conformance checks; preserve their current public imports and execute signatures.
- At R2.7, establish the narrow private boundary `authoritative repository inputs → one private control-generation builder → complete candidate SQLite, SQL, manifest, and projection artifacts`. The implementation may use a private stateless builder and immutable result, but this Task neither creates nor freezes a public interface.
- `HarnessControlMigrator` uses the private builder, validates the complete candidate, and remains the sole publisher of maintained control artifacts. `HarnessControlVerifier` uses the same builder, compares the candidate with maintained artifacts, reports differences, performs no maintained writes, and removes temporary verification artifacts after success or failure. Verification must detect authoritative-source drift even when maintained SQLite and maintained SQL agree with each other.
- There is no migrator check mode, second construction algorithm, public builder Action, incremental updater, watcher, daemon, event-log authority, or second database writer. Preserve the current public imports and execute signatures of `HarnessControlMigrator` and `HarnessControlVerifier`. R2.3 through R2.6 continue using the existing migrator and introduce no other construction or publication path.
- R2.3 establishes canonical evidence inputs, R2.4 establishes canonical resource inputs, and existing canonical Task and graph inputs remain part of maintained control construction. R2.6's synchronization command supplies the canonical maintained input set. R2.7 makes the verifier derive that same set from repository-owned configuration.
- The verifier's source-aware guarantee applies to maintained canonical control state. Do not claim that `HarnessControlVerifier.execute(repository_root)` reproduces arbitrary noncanonical migration requests or alternate output locations, and preserve existing bounded compatibility behavior for nondefault `HarnessControlMigrationRequest` inputs unless separately authorized.
- Use one evidence-authority flow: Python test source and embedded declarations plus a versioned evidence policy or profile plus explicit predecessor or migration relationships produce one immutable derived `PythonTestModuleModel`, independent validation-rule results, and generated inventory, count, hash, SQLite-row, SQL-export, and documentation projections.
- Before any later authorization of incremental updating, measure full migration wall time, database size, projection count, rewritten-artifact count, synchronization frequency, and ordinary failure and recovery behavior. These measurements are diagnostics, do not activate telemetry, and leave incremental updating deferred unless full reconstruction is materially burdensome.
- Keep ordered execution unchanged and one child active at a time: R2.3 makes evidence authority and projections reconstructible; R2.4 does the same for resources; R2.5 decomposes wire validation without changing persistence ownership; R2.6 exposes one maintained synchronization command; and R2.7 composes repository validation and retires legacy routes.
- The active parent authorizes R2.3 through R2.7. After a child completes, the parent agent may explicitly transition to the next prerequisite-satisfied child without a separate human activation decision when no unresolved checkpoint, human-owned material choice, protected action, or unresolved material finding exists. Only one child may be active at a time; background activation is prohibited and `automatic_successor_activation` remains false.
- Internal implementation commits and deterministic child transitions require no separate checkpoint, acceptance packet, or human review cycle. Stop and report for actual ambiguity, public-contract choice, dependency decision, scientific decision, protected action, or unresolved material review finding. Retain one consolidated independent compatibility review at R2.7 before parent completion and final human acceptance.
- Treat every child as a complete vertical replacement of its owned subsystem: accepted end-state contract, implementation in isolation, complete affected-data migration, controlled parity, one cutover, and removal of the obsolete live path. Do not retain old and new operational authorities after cutover; temporary compatibility is permitted only when an accepted public contract requires it.
- Consolidate routine inspection, validation, projection, Task, and evidence operations behind a small maintained command surface backed by ActionObjects; every maintained live CLI script and entry point must live under `python/src/cli/` while reusable behavior remains with its owning ActionObjects under `python/src/ksdft2effmass/`, and routine repository inspection must not depend on executable wrappers outside `python/src/cli`, generated shell, or inline-Python fragments.
- Preserve `.pi` Tasks, chains, checkpoints, decisions, and evidence as history while moving remaining live structured operational authority under `harness/`; remove compatibility readers only after proving that no live consumer remains.
- Retire new proliferation of manually synchronized ownership, completion, verification, inventory, migration, review, transcript, and repeated chain-state copies; a Task, its graph relationships, lifecycle events, and referenced evidence should ordinarily suffice.
- Rationalize maintained harness agent and skill routing toward implementation, verification, documentation, and read-only integration-review roles with shared policy stored once, task-selected skills, exact assignment inputs and output contracts, and bounded scout-then-reviewer dispatch rather than duplicated prompt fragments or parallel deep reviews for routine inspection.
- Normalize maintained Python command examples and validation entry points on `python/.venv/bin/python` without adding or changing dependencies.
- Keep tracked control state in `harness/state/harness-control.sqlite3` and keep any future volatile observations in the ignored `.pi/cache/harness-observations.sqlite3`; this Task does not implement telemetry.

## Completion criteria

- The seven ordered child Tasks from `harness.simplify-2.control-decomposition` through `harness.simplify-2.validation-retirement`, including `harness.simplify-2.cli-consolidation`, are complete; each changed subdomain has an explicit owner and dependency direction, and orchestration layers contain coordination rather than domain mechanism.
- Existing public imports, ActionObject names and execute signatures, supported wire contracts, SQLite schema and semantic identity, deterministic SQL recovery, projection bytes, and compatibility behavior remain stable unless a separately resolved human decision explicitly authorizes a change.
- One maintained validation Action produces structured named checks, statuses, findings, and durations without invoking another CLI and parsing its output; one CLI renderer under `python/src/cli/` exposes the result, and no maintained live CLI script or entry point remains outside `python/src/cli`.
- The R2.7 private builder is the single owner of candidate control-generation mechanics; the migrator is the sole publisher, and the nonmutating verifier derives canonical maintained inputs, compares candidate SQLite, SQL, manifest, and projections with maintained artifacts, and removes temporary verification artifacts.
- Live structured control has one SQLite authority, one full database-construction and publication Action, deterministic generated projections, and no second maintained control model or writing path; legacy `.pi` material remains historical rather than operational authority.
- The explicit synchronization command delegates staged complete reconstruction, validation, and failure-safe publication to `HarnessControlMigrator`; no incremental SQL mutation, partial projection tracking, watcher authority, event-log authority, or second database writer exists.
- R2.3 through R2.7 have exact nonoverlapping ownership for evidence semantics and inputs, resource semantics and inputs, wire codecs, final CLI placement and synchronization exposure, and repository-wide validation composition respectively.
- A maintainer can change Task persistence, add, move, or remove a Python test, revise evidence naming, resolve resources, or change wire serialization without editing an unrelated orchestration monolith or manually synchronizing unrelated representations, generated inventories, counts, hashes, SQLite rows, or documentation projections.
- Focused tests, the complete maintained harness software-verification suite, Ruff, mypy, resource and evidence conformance, deterministic SQLite reconstruction, projection agreement, documentation validation, and dependency-lock nonmutation checks pass.
- One consolidated independent read-only compatibility review has no unresolved material findings after at most one consolidated correction pass.
- The Task concludes pending explicit human acceptance with `active_task` restored to null and no automatic successor, telemetry, production-source refactor, scientific work, or protected execution activated.

## Exclusions

- Do not refactor `operators/serialization.py`, `workflows/cpn/execution.py`, `provenance/serialization.py`, or other scientific/package-source modules in this Task; those require separate source-contract audits and separately activated Tasks.
- Do not split modules merely to reduce line counts. Split only where a subdomain has its own inputs, invariants, Action ownership, dependency direction, and focused tests; do not expose every internal codec or migration step as public API.
- Do not implement telemetry, observations collection, live instrumentation, session parsing, dashboards, tokens, costs, or effectiveness claims. Bounded measurements of full migration wall time, database size, projection count, rewritten artifacts, synchronization frequency, and ordinary failure and recovery behavior are diagnostics only and do not activate telemetry.
- Do not introduce incremental row-level updates, partial projection dependency tracking, another maintained SQLite database, another database writer or persistence framework, filesystem watchers or daemons, event-log authority, ambient repository discovery, a second control-generation algorithm, or a public builder Action. The R2.7 private builder may create temporary candidate artifacts for the migrator or verifier, but only `HarnessControlMigrator` may publish maintained state.
- Do not rewrite or delete retained historical `.pi` Tasks, chains, checkpoints, exact human decisions, evidence, provenance, or the historical scripts that record commands actually used. The `python/src/cli` location rule applies to maintained live command implementations, not retained historical evidence scripts; compatibility removal requires proven non-use and must preserve required historical traceability.
- Do not add or replace dependencies, change `python/uv.lock`, publish or extract a package, perform release actions, execute external or scientific calculations, change scientific settings or contracts, claim scientific validation or uncertainty quantification, or activate any successor automatically.

## Historical source

No archived source.
