# Scientific interpretation

The source and target are complete `RepresentationIdentity` values. `kind` is an explicit
`RepresentationTransformationKind` enum member, and `orientation` states the directed
convention.

Intrinsic validation enforces the Phase 1 role transitions: ambient-to-retained frame
compression, retained Bloch gauge/alignment edges, retained-Bloch-to-complete-cell
Fourier conversion, complete-to-truncated support restriction, and cell-to-retained
reconstruction.

The identity does not prove that a map exists, was applied correctly, is dimensionally
compatible, preserves spectra, or meets a scientific admissibility criterion.
