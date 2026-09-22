# Control-plane cleanup intake

## Human request

> let's do a control plane clean up, plan a task with immediate priority, but not active to do this, this should include an audit of AGENTS.md, skills, prompts, and all control plane surfaces. start first with the inventory

## Revised activation instruction

The human subsequently accepted and closed `harness.simplify-2`, revised this Task,
and explicitly required separate activation. `harness.control-plane-cleanup` is now
active. Automatic successor activation remains disabled, no other successor is
active, and cleanup implementation must not begin until the corrected Task and its
generated documentation agree.

## Objective and historical boundary

The objective is authority reduction, not arbitrary file-count reduction. The live
control plane should contain only the minimum operational authority required for
current and prospective work. This repository is pre-alpha, and Git history is
sufficient historical retention. Unused live compatibility, deprecated aliases,
archived copies, resolved control records, and historical ceremony do not need to
remain tracked merely to preserve old interfaces. No replacement archival layer is
to be created.

## Role, disposition, and reachability

Every inspected surface receives exactly one role—`authority`, `runtime`,
`projection`, `documentation`, `history`, or `cache`—and exactly one disposition—
`retain`, `delete`, or `unresolved`. Unresolved is fail-closed: the surface is
retained, reported, and excluded from deletion. An unresolved surface blocks final
completion but requires a human checkpoint only when an actual human-owned decision
remains.

Retention is determined by reachability from explicit operational roots rather than
by any consumer. Roots are applicable `AGENTS.md`, durable operational agents,
retained skills, current and explicitly prospective Tasks, operational chains and
current selection state, maintained user-facing commands, canonical resource
profiles and manifests, authoritative schemas, current evidence authority, the
control synchronization command, and the source-aware validation command.

Consumer analysis covers Python imports, public exports, CLI registrations, schema
references, manifests and profiles, Task and chain references, documentation
navigation, tests, declarative resource resolution, and generated-state inputs. A
surface consumed only by obsolete, historical, or removable surfaces is not
operational.

## Three bounded slices

1. **Authority and reachability:** build and commit the complete operational-root and
   reachability inventory without deleting files.
2. **Control-history removal:** remove only control history, resolved decisions,
   closed chains, archives, historical ceremony, reproducible generated duplicates,
   caches, and temporary or replay artifacts proven deletable by Slice A. Create no
   replacement archive.
3. **Runtime and compatibility pruning:** remove a runtime or compatibility surface
   only when it is unreachable from every operational root, has no supported public
   extension contract, is not dynamically or declaratively resolved, leaves no
   retained owner incomplete, carries its tests and documentation disposition with
   it, and passes focused and repository-wide validation.

Tests follow their retained behavioral owner and are not an independent numerical
cleanup target. Use one commit per completed slice, no per-slice checkpoints, one
consolidated read-only integration review after all slices, and at most one bounded
correction pass before one final human-acceptance decision.

## CLI and architecture boundaries

Retain one synchronization command, one source-aware validation command, and
additional commands only for distinct maintained user operations. No CLI remains
solely as another CLI's wrapper, and maintained commands do not parse one another's
output.

The Task may delete obsolete architecture but may not design or implement a
replacement architecture, framework, API redesign, persistence model, plugin system,
abstraction layer, telemetry, behavioral rewrite of retained components, or
speculative extraction interface. Discovered architectural improvements become
later candidates only.

## Scientific and protected boundaries

Do not modify or delete scientific production code; numerical-verification,
scientific-validation, or UQ evidence; simulation inputs or outputs; computational
protocols; scientific schemas or fixtures; research documentation; or publication
artifacts. A control-plane reference does not bring a scientific artifact into
scope, although a stale control-plane reference may be corrected without modifying
the referenced artifact.

No dependency or lockfile change, protected or external action, release work,
scientific implementation, simulation, or automatic successor activation is
authorized.
