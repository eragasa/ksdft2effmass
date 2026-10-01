# `ResearchMonographCitationSnapshotRequest`

Immutable execution request containing one absolute repository root bounded to 4096
UTF-8 bytes. The manuscript and bibliography paths are fixed and not caller-selected.
Its `request_id` identifies the operation and relative contract paths but deliberately
excludes the machine-local absolute root.
