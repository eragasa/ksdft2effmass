# Calculation workflow

This package owns the bounded, calculation-specific rank-N D1 workflow. It fixes the current finite rank ladder (`3`, `4`, `8`, `16`), depth ladder, channel inventory, meshes, supports, diagnostic records, qualification logic, and schema-free development composition.

It is not part of the installed `ksdft2effmass` library API. Reusable matrix-field diagnostics and numerical operations remain with their canonical library owners. The root entrypoints adapt files and command-line execution to this workflow.

Current status: schema-free development implementation. Strict serialization, producer-independent full-result verification, retained-run composition, and production-evidence status are not implemented.
