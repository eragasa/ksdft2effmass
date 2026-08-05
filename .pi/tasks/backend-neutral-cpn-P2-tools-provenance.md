# P2 — Provenance and external-tool capability records

Status: implementation complete; active and blocked at pending final human-acceptance checkpoint `P2-HC01`

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

## Completion boundary

Implementation, schema/fixtures, class-owned and artifact-owned software verification, maintained documentation, one consolidated independent review, one correction cycle, the ordinary R1 replay, the single replacement R2 replay, and parent verification are complete. The final root correction rejects single-backslash diagnostic paths; it is covered by focused and final deterministic checks but not a prohibited third replay. The full Python and mypy runs retain only the starting-revision H4/H2 harness baselines documented in parent verification. P2 is not closed or human-accepted and remains blocked at `.pi/checkpoints/P2-HC01-final-acceptance.json`.

H5, P3--P11, scientific/external execution, publication, and release remain inactive.