# P3 — SNAKES net construction and project-owned persistence

Status: blocked by accepted P1 and P2

## Objective

Implement the selected SNAKES adapter behind the accepted project CPN contract and deterministic project-owned durable marking persistence.

Persistence records workflow schema/model IDs, multisets of typed token payloads, provenance, parent-child lineage, request/result correlation, and retry/failure history. Live-net pickle, arbitrary Python pickle, serialized lambdas, credentials, external clients, and Graphviz-as-authority are prohibited. Logical subnet composition must not assume an unverified hierarchical SNAKES API.

Completion requires implementation, tests, Markdown documentation, independent review, parent verification, and human acceptance.