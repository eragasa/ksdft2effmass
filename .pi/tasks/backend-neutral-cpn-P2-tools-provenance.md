# P2 — Provenance and external-tool capability records

Status: `P2-A00`--`P2-A05` are `audited_and_cleared`; `P2-A06` is next but not started; P2 remains open and unaccepted after resolved `P2-HC06`

Activation authority: the current human instruction titled **P2 — Activate and implement provenance and external-tool capability records**. The durable activation, reconciled version-1 choices, starting revision, local-route preflight, and inactive successor scope are recorded in `.pi/evidence/backend-neutral-cpn-P2-tools-provenance/activation.json`. The ownership declaration is `.pi/evidence/backend-neutral-cpn-P2-tools-provenance/task-ownership.json`.

## Activation prerequisites

P2 required all three conditions, now satisfied:

- `P1:human_accepted` through resolved `P1-HC03`;
- `H4:human_accepted` through the resolved H4 closeout and maintained local-route proof;
- `explicit_activation:P2` through the current human instruction and durable activation record.

H5 remains optional, inactive, and not a P2 prerequisite. P3--P11 remain blocked and inactive. Scientific execution, external-tool execution, publication, and release remain unauthorized.

## Objective

Implement project-owned artifact/manifest records and narrowly shared external-tool lifecycle records for identity, specification, capability, installation, verification, immutable request/result, and structured failure.

Preserve `ArtifactReference`/`ArtifactLocation` separation. Durable tokens retain stable IDs and immutable payloads, never credentials, subprocess or scheduler handles, open files, mutable clients, closures, or SNAKES objects. QE/Wannier semantics remain concrete adapters; no plugin framework is authorized.

Completion requires implementation, tests, Markdown documentation, independent review, parent verification, one bounded ordinary replay, and human acceptance.

## Version-1 reconciliation

P2 uses an immutable `ArtifactLocation` DataObject because the current human objective explicitly requires the record and maintained provenance documentation already presents it. Artifact byte sizes use the unsigned 64-bit range. Strict JSON input rejects duplicate and unknown keys, BOMs, malformed Unicode, non-finite values, booleans as integers, and numeric strings. Canonical output is compact sorted-key UTF-8 JSON followed by one LF; P2 has no floating-point fields. Project-owned artifact logical paths and diagnostic paths follow the accepted H1/H2 root-relative NFC POSIX lexical contract without importing harness types. Locations use explicit root-relative values or opaque approved external-location descriptors and never discover a root or current working directory implicitly.

These bounded choices implement the accepted architecture without importing harness, CPN, SNAKES, backend, scheduler, subprocess-client, or mutable-client objects into durable payloads. They do not authorize storage I/O, external execution, QE or Wannier90 adapters, scientific interpretation, numerical acceptance, scientific validation, or UQ.

## Option-B bounded correction

The human PI resolved `P2-HC01` as Option B on 2026-08-05 and authorized exactly one post-R2 bounded correction of `python/src/ksdft2effmass/provenance/records.py` and its directly owned verification surface. The correction removes dangling module-level validator callables, places intrinsic invariants visibly in the seven owning records, rejects direct `RunManifest` self-dependency, completes the seven class-owned evidence modules, adds the corresponding schema/runtime invalid fixture, and synchronizes directly affected provenance documentation. Separate implementation and verification writers and one targeted independent reviewer are required; at most one small correction pass may address a material review finding.

R1 and R2 remain immutable historical evidence. No R3/E3 is authorized. The corrected current boundary is covered by deterministic validation and targeted review, followed by a renewed final P2 human-acceptance checkpoint, commit, and push.

## Completion boundary

The Option-B correction is complete. Current-boundary deterministic validation passes, including focused software verification, schema/runtime fixture agreement, branch-coverage diagnostics, Ruff, mypy, Sphinx warnings-as-errors, P2 completion and ownership, checkpoint validation, the maintained local harness route, dependency/lockfile nonmutation, and unrelated-work preservation. The single targeted reviewer confirmed the substantive correction and returned one inapplicable lower-authority heading finding plus one source-docstring finding; the latter was corrected in the sole small correction pass and revalidated. No second general review or R3/E3 was performed.

P2-HC02 was resolved as Option B on 2026-08-06. The human authorized one test-evidence-only migration using the accepted `develop-python-test-evidence` skill with `AUTHORIZED_TEST_EVIDENCE_WRITE`: seven `records.py` class-owned modules and the directly related fixture/runtime artifact-owned module, plus their explicit ownership, complete one-to-one pytest node migration map, completeness inventory, directly affected test-evidence documentation, review/completion records, and renewed `P2-HC03` checkpoint.

Production source, public behavior, schemas, fixtures, serialization, dependencies, lockfiles, scientific meaning, R1/R2, and P2 successors remain unchanged. Existing evidence IDs and assertions are preserved except for mechanical splitting needed to give each test one correctly named public surface. No R3/E3 is authorized. H5, P3--P11, scientific/external execution, publication, and release remain inactive.

## P2-HC02 test-evidence migration completion

The eight supplied modules now satisfy the accepted structural convention with explicit seven-class/one-artifact software-verification ownership, complete one-to-one historical node migration, semantic parameter IDs, visible documented helpers, cohesive public surfaces, truthful seven-field documentation, and separated schema/runtime/serialization evidence. All historical IDs remain unrenumbered; distinct split owners use `SV-PROV-104` through `SV-PROV-142`.

One targeted reviewer returned material semantic findings. The sole writer completed one consolidated correction pass. All applicable findings were corrected and parent-confirmed; the proposed four-property split was inapplicable because the human instruction explicitly permits one cohesive delegation-map owner. No second reviewer cycle occurred.

Focused tests, collection, branch diagnostics, Ruff, mypy, Sphinx, P2 ownership/completion, checkpoint validation, H3 resources, skill capabilities, selected local route, protected hash nonmutation, dependency/lock nonmutation, and diff checks pass. P2 remained open at `.pi/checkpoints/P2-HC03-final-acceptance.json` until the current human instruction authorized one further bounded correction of `python/src/ksdft2effmass/provenance/actions.py`, seven class-owned action/result/enum test modules, three directly affected maintained documentation pages, and their current-boundary evidence/control records. Separate source, test-evidence, and documentation writers plus one targeted read-only reviewer are required. The parent owns integration, validation, checkpoint state, and durable commits.

The correction removes `_require_identifier` and `_require_sha256`, moves intrinsic validation directly into owning `__post_init__`/`execute` methods, preserves public behavior and signatures, migrates the seven class-owned test surfaces under `develop-python-test-evidence`, and documents the public operation/claim boundaries under `document-python-research-software`. Production outside `actions.py`, exports, schemas, fixtures, serialization, dependencies, locks, external-tool lifecycle meaning, and scientific meaning remain protected. R1/R2 stay immutable; no replay is authorized.

Implementation, test-evidence migration, documentation, one targeted review, one consolidated correction pass, and parent deterministic validation are complete. `actions.py` has no private validation helpers or replacement private machinery; seven class-owned modules and their complete migration records pass the accepted test-evidence convention. Public exports/signatures/vocabularies, schemas/fixtures, serialization, dependencies/locks, and successor state are unchanged.

The correction is durable at `4bd5a607dda238475322e32207897512a73e20a0` and matches `origin/dev`. `P2-HC03` was superseded without resolution; renewed final acceptance is pending at `.pi/checkpoints/P2-HC04-final-acceptance.json`.

No R3/E3, H5, P3--P11, scientific/external execution, publication, or release is active.

## P2 tools lifecycle-ownership decomposition

The current human instruction authorized `P2-TOOLS-DECOMPOSITION-1` while P2 remained open. Documentation inspection established that only `ksdft2effmass.provenance` is a supported import path; `ksdft2effmass.provenance.tools` had no supported module-path contract. The former implementation module was therefore removed and replaced by `external_tools.py`, `tool_observations.py`, and `external_execution.py`, with package, action, and serializer import wiring updated without changing the accepted package export inventory or version-1 wire mapping.

Every moved record now directly validates intrinsic fields in its own `__post_init__`; the six former private validators and replacement private machinery are absent. The exact 13 class-owned software-verification modules, complete one-to-one historical node migration, owner-specific new evidence inventory, maintained documentation, import/wheel artifact synchronization, and current P2 completion validator are durable. The sole targeted reviewer returned one internal-alias wording/ownership finding. One consolidated correction pass removed the unsupported public-alias wording while retaining the human-required internal alias assertion and unchanged package exports. No second review occurred.

Deterministic structural validation, 493 provenance cases, 144 focused integration cases, diagnostic per-module branch coverage, Ruff, mypy, Sphinx warnings-as-errors, public shape comparison, strict serialization/schema/fixture agreement, clean wheel build/install, ownership/completion/skill/checkpoint/local-route gates, protected nonmutation, and diff checks pass. `P2-HC04` was superseded without acceptance; renewed final acceptance is pending at `P2-HC05`. P2 remains open and unaccepted. No R3/E3, H5, P3--P11, protected execution, publication, or release is active.

## Ordered provenance audit queue

The current human instruction records one authoritative audit queue at `.pi/evidence/backend-neutral-cpn-P2-tools-provenance/provenance-audit-queue.json`. It contains exactly P2-A00--P2-A11, permits only one mutable item at a time, distinguishes deterministic structural validation from semantic review, and requires every item to reach `audited_and_cleared` before P2 may be accepted. P2-A00 (`actions.py`) and P2-A01 (`external_tools.py`) are cleared. P2-A02 (`tool_observations.py`) is also `audited_and_cleared`: production remained byte-identical; three class-owned modules now cover every authoritative identifier, version, digest, evidence-member, equality, frozen-state, enum-surface, taxonomy, and lifecycle partition. Deterministic validation passed, and the sole targeted review's two bounded findings were corrected in one consolidated pass. The durable correction revision is `379c491e41752bebda5d7cb6324eb6c820223609`.

`P2-HC06` was resolved as Option A and the ordered P2-A03 file audits are complete. The three enum, request, result, failure, and internal outcome-alias evidence surfaces passed their bounded deterministic checks. Consolidated ownership contains six class-owned modules and one artifact-owned module; 405 aggregate cases pass with complete diagnostic statement and branch coverage of `external_execution.py`. P2-A03 is `audited_and_cleared`. Within P2-A04, `ArtifactLocationKind` now has a dedicated class-owned module, and `SV-PROV-011` moved from `test__ArtifactLocation.py` to its correct enum owner with the complete version-1 enum contract. Deterministic validation passed. The `ManifestState` module is explicitly class-owned, preserves `SV-PROV-075`, and covers the complete version-1 lifecycle enum contract. `LineageKind` now has a dedicated class-owned module, preserves moved `SV-PROV-019`, and leaves `SV-PROV-133` with `LineageRelation`. The three enum corrections and aggregate deterministic consistency check passed. P2-A04 is `audited_and_cleared`.

The completed human P2-A05 audit authorized one bounded serialization correction. `_DuplicateKeyError` was removed, `_strict_object` now raises `ProvenanceJsonError` directly, and the other explicit record-mapping helpers, signatures, exports, and version-1 wire semantics remain unchanged. `SV-PROV-057` moved exactly once from the error module to the serializer's malformed-syntax translation owner; `SV-PROV-056` and `SV-PROV-058`--`SV-PROV-061` remain unrenumbered. New strict-input and unsupported-record owners use `SV-PROV-378`--`SV-PROV-393`. Two class-owned modules contain 22 evidence owners, no helpers, and 24 collected cases. Structural validation, focused tests, 100% diagnostic statement and branch coverage, fixture/wire regressions, Ruff, mypy, public API, protected nonmutation, and control-plane checks pass. P2-A05 is `audited_and_cleared`; P2-A06 is next but was not started. P2-A06 remains pending read-only audit; P2-A07--P2-A11 remain pending artifact audits. Recording or clearing an audit item does not authorize P2 acceptance, activate P3/H5, authorize external or scientific execution, or establish numerical verification, scientific validation, UQ, provenance truth, publication readiness, or release readiness.