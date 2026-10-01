# `ResearchMonographCitationSnapshotIntegrityValidator`

Public ActionObject owning complete owner-result acceptance. `request_identity()`
derives the root-independent durable request ID. `execute(snapshot, request_id)`
checks all public limits (including ASCII ``[A-Za-z0-9._-]{1,200}`` keys),
canonical constants, source/include lineage, record IDs and relationships, locators,
marker links, bibliography bindings, and closure sets, then
returns `citation-result:<64 lowercase hex>` over the complete length-framed
projection. `validate_aggregate_source_size()` and
`validate_canonical_projection_size()` expose the exact 100,000,000-byte source and
20,000,000-byte pre-hash projection boundaries.
