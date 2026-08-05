# P2 — Provenance and external-tool capability records

Status: open; `P2-HC01` resolved as Option B; one post-R2 bounded correction is active after the durable resolution push

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

P2 remains open during this bounded correction and will remain open pending renewed human acceptance after correction validation. H5, P3--P11, scientific/external execution, publication, and release remain inactive.