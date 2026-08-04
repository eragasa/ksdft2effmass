# P2 — Provenance and external-tool capability records

Status: blocked by accepted P1

## Objective

Implement project-owned artifact/manifest records and narrowly shared external-tool lifecycle records for identity, specification, capability, installation, verification, immutable request/result, and structured failure.

Preserve `ArtifactReference`/`ArtifactLocation` separation. Durable tokens retain stable IDs and immutable payloads, never credentials, subprocess or scheduler handles, open files, mutable clients, closures, or SNAKES objects. QE/Wannier semantics remain concrete adapters; no plugin framework is authorized.

Completion requires implementation, tests, Markdown documentation, independent review, parent verification, and human acceptance.