<!-- Generated from SQLite control state; do not edit. -->
# Reduce repository control-plane authority

[Task index](index.md) · [Previous](./harness-task-state-symlink-toctou-hardening.md) · [Next](./harness.extraction.md)

## Status

`closed_human_accepted_pass`: Human-accepted and closed with documented architectural limitations. Accepted claim: The bounded control-plane cleanup removed repository surfaces proven obsolete under the current architecture, eliminated unresolved dispositions, preserved operational behavior, and retained complete validation agreement. The repository is not claimed to have a minimal control plane. Further reduction requires a separately authorized later architectural change; no successor is activated.

## Objective

Reduce the live repository control plane to the minimum operational authority required for current and prospective work. Because the repository is pre-alpha, Git history is sufficient historical retention: unused compatibility, deprecated aliases, archived copies, resolved control records, and historical ceremony need not remain tracked merely to preserve old interfaces.

## Parent and prerequisites

- Depends on: `harness.simplify-2`

## Authority references

- AGENTS.md
- docs/development/agent-control-plane.rst
- harness/reports/control-plane-cleanup-inventory.json

## Authorized scope

- For every inspected surface, assign exactly one role from authority, runtime, projection, documentation, history, or cache and exactly one disposition from retain, delete, or unresolved. Unresolved is fail-closed: retain and report the surface, exclude it from deletion, and treat its presence as preventing final completion without manufacturing a human checkpoint unless an actual human-owned decision remains.
- Determine retention by reachability from explicit operational roots: applicable AGENTS.md; durable operational agents; retained skills; current and explicitly prospective Tasks; operational chains and current selection state; maintained user-facing commands; canonical resource profiles and manifests; authoritative schemas; current evidence authority; the control synchronization command; and the source-aware validation command.
- Analyze consumers through Python imports, public exports, CLI registrations, schema references, manifests and profiles, Task and chain references, documentation navigation, tests, declarative resource resolution, and generated-state inputs. A surface consumed only by obsolete, historical, or removable surfaces is not operational.
- Slice A — Authority and reachability: create the complete operational-root and reachability inventory without deleting files. Identify canonical authority sources, generated projections, historical-only records, obsolete compatibility clusters, unresolved dynamic or declarative consumers, and independently maintained duplicate representations.
- Slice B — Control-history removal: delete only completed or superseded control history; resolved or superseded checkpoints; closed historical chains; archived duplicates; historical ceremony retained only for old operation; reproducible generated duplicates; tracked caches; and temporary, replay, journal, staging, or backup artifacts proven deletable by Slice A. Do not create a replacement archive; Git history is the historical record.
- Slice C — Runtime and compatibility pruning: evaluate agents, skills, resources, schemas, fixtures, extensions, CLIs, harness modules, tests, and current documentation. Delete a runtime or compatibility surface only when it is unreachable from every operational root, has no supported public extension contract, is not dynamically or declaratively resolved, leaves no retained owner incomplete, migrates or removes associated tests and documentation with it, and focused plus repository-wide validation pass. Tests follow their retained behavioral owner and are not an independent numerical cleanup target.
- Retain one synchronization command, one source-aware validation command, and additional CLIs only for distinct maintained user operations; remove CLIs retained solely as wrappers and prohibit command-output parsing between maintained commands.
- Use one commit per completed slice. After all slices, regenerate through the sole synchronization command, run source-aware validation and all required focused and repository gates, obtain one consolidated read-only integration review, permit at most one bounded correction pass, and present one final human-acceptance decision.

## Completion criteria

- Slice A is committed with a complete operational-root and reachability inventory; every inspected surface has exactly one role and one disposition; no file deletion occurred in that slice; and all unresolved surfaces are retained, reported, excluded from deletion, and cleared before final completion.
- Only durable operational agent roles, retained skills with distinct operational capabilities, operational current or explicitly prospective Tasks and relationships, operational chains, and current selection state remain live.
- Slice B is committed after deleting only proven completed or superseded control history, resolved or superseded checkpoints, closed historical chains, archived duplicates, obsolete historical ceremony, reproducible generated duplicates, tracked caches, and temporary or replay artifacts; no replacement archive exists because Git preserves history.
- Current generated evidence projections remain only when reproducible by the maintained publisher, no tracked cache or temporary database, journal, staging, backup, or replay output remains, each control domain has one explicit authority source, and generated state has one maintained synchronization path.
- Slice C is committed after every deleted runtime or compatibility surface satisfies all six deletion conditions, every retained skill and resource has an operational-root-reachable consumer, every retained CLI provides a distinct maintained user operation, and associated tests and documentation follow their retained behavioral owner.
- Aliases, adapters, compatibility wrappers, schemas, fixtures, profiles, extensions, and control-plane documentation without an operational-root-reachable consumer or supported contract are removed, while unresolved dynamic and declarative consumers remain retained until resolved.
- Production harness modules and tests are evaluated by ownership, reachability, supported contracts, and behavior rather than numerical line, module, command, test, or file-count targets.
- Obsolete architecture may be deleted, but no replacement object architecture, framework, persistence model, plugin system, abstraction layer, public/private API redesign, behavioral rewrite, telemetry, or speculative extraction interface is introduced; later architectural candidates are recorded without implementation.
- Scientific production code, numerical-verification evidence, scientific-validation evidence, UQ evidence, simulation inputs or outputs, computational protocols, scientific schemas or fixtures, research documentation, and publication artifacts remain unchanged; stale control-plane references may be corrected without modifying those artifacts.
- After all three slice commits, maintained state is regenerated through the sole synchronization command; source-aware validation, affected tests, the complete configured suite, Ruff, mypy, Sphinx warnings-as-errors, resources, evidence conformance, Task and graph validation, and git diff --check pass; one consolidated read-only integration review completes; and at most one bounded correction pass is used before final human acceptance.

## Exclusions

- Do not create another archival layer before deleting the existing one; Git history is the historical retention boundary for this pre-alpha repository.
- Do not design or implement a replacement object architecture, new architectural framework, public/private API redesign, new persistence model, plugin system, new abstraction layer, telemetry, behavioral rewrite of retained components, or speculative extraction interface. Record discovered architectural improvements only as later candidates.
- Do not modify or delete scientific production code, numerical-verification evidence, scientific-validation evidence, UQ evidence, simulation inputs or outputs, computational protocols, scientific schemas or fixtures, research documentation, or publication artifacts. A control-plane reference does not bring the referenced scientific artifact into scope.
- Do not implement scientific or numerical behavior, execute simulations, add or change dependencies or lockfiles, perform release work, perform protected or external operations, or change scientific specifications, mathematical conventions, or physical settings.
- Do not create per-slice checkpoints or independent review loops, perform more than one consolidated correction pass, activate any other successor, or enable automatic successor activation.
- Do not treat structural simplification, reduced counts, passing tests, or reviewer agreement as scientific validation or final human acceptance.

## Historical source

No archived source.
