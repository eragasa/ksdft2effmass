# P2 — Provenance and external-tool capability records

Status: blocked; accepted P1 is satisfied, but accepted H5 and separate explicit P2 activation are still required

## Activation prerequisites

P2 requires all three conditions:

- `P1:human_accepted` (satisfied);
- `H5:human_accepted` (not satisfied);
- separate explicit human activation of P2 (not granted).

Acceptance of H5 must not launch P2. P3--P11 remain transitively blocked.

## Objective

Implement project-owned artifact/manifest records and narrowly shared external-tool lifecycle records for identity, specification, capability, installation, verification, immutable request/result, and structured failure.

Preserve `ArtifactReference`/`ArtifactLocation` separation. Durable tokens retain stable IDs and immutable payloads, never credentials, subprocess or scheduler handles, open files, mutable clients, closures, or SNAKES objects. QE/Wannier semantics remain concrete adapters; no plugin framework is authorized.

Completion requires implementation, tests, Markdown documentation, independent review, parent verification, and human acceptance.