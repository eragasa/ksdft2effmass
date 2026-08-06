# P2 — Provenance and external-tool capability records

Status: P2-HC02 Option-B test-evidence migration complete; open and blocked at renewed final human-acceptance checkpoint `P2-HC03`

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

Focused tests, collection, branch diagnostics, Ruff, mypy, Sphinx, P2 ownership/completion, checkpoint validation, H3 resources, skill capabilities, selected local route, protected hash nonmutation, dependency/lock nonmutation, and diff checks pass. P2 remains open and blocked at `.pi/checkpoints/P2-HC03-final-acceptance.json`. No R3/E3, H5, P3--P11, scientific/external execution, publication, or release is active.