# P2 — Provenance and external-tool capability records

Status: blocked and inactive; accepted P1 is satisfied, but accepted H4 and separate explicit P2 activation are still required

## Activation prerequisites

P2 requires all three conditions:

- `P1:human_accepted` (satisfied);
- `H4:human_accepted` (not satisfied);
- `explicit_activation:P2` through a separate human decision (not granted).

These are the complete P2 prerequisites. H5 is optional extraction-readiness
work after H4 and is not a P2 prerequisite. Accepted H4 does not launch P2.
P3--P11 remain transitively blocked.

## Objective

Implement project-owned artifact/manifest records and narrowly shared external-tool lifecycle records for identity, specification, capability, installation, verification, immutable request/result, and structured failure.

Preserve `ArtifactReference`/`ArtifactLocation` separation. Durable tokens retain stable IDs and immutable payloads, never credentials, subprocess or scheduler handles, open files, mutable clients, closures, or SNAKES objects. QE/Wannier semantics remain concrete adapters; no plugin framework is authorized.

Completion requires implementation, tests, Markdown documentation, independent review, parent verification, and human acceptance.