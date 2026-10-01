# `CitationSnapshotError`

Structured fail-closed extraction exception containing a closed error code, optional
root-relative source path, optional zero-based UTF-8 byte offset, and sanitized
nonempty detail. It carries no source excerpt. Compiler failures return no partial
snapshot or Result.
