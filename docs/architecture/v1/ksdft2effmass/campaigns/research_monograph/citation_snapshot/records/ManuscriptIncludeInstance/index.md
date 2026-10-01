# `ManuscriptIncludeInstance`

Immutable root or included-file occurrence in depth-first traversal order. It retains
parent file/instance IDs, child file ID/path, exact include-command span, per-parent
ordinal, and depth. Replay checks the root sentinel, earlier-parent topology,
contiguous per-parent ordinals, parent source bounds, and deterministic identity.
