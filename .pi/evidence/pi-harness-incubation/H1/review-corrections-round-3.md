# H1 bounded correction round 3

The correction-2 review outputs are retained unchanged. This final semantic
correction resolves their remaining contract inconsistencies.

1. Added `PIH.WIRE.INVALID_VALUE` for correctly typed wire values that violate a
   closed intrinsic invariant, and added `PIH.CHAIN.ACTIVATION_UNEXPECTED`.
   Removed stale media-type and all local-code ambiguity. Expanded the
   action/code precedence table.
2. Bound generic and optional local manifests by exact profile ID/version plus
   explicit action-input SHA-256 identity of RFC 8785 canonical JSON plus LF.
   Resolution verifies all three independently without creating a circular
   local-manifest/profile hash.
3. Defined the exact chain-evaluation truth algorithm for task/external
   prerequisites, active status, structurally ready state, explicit activation,
   unresolved linked checkpoints, and the permitted overlap of active/blocked at
   a checkpoint.
4. Reconciled `ChecksumManifest` everywhere to its minimal entries-only shape
   with the root supplied explicitly; corrected the current catalog count to six.
5. Added `HarnessContractError` to the support/portability surface and corrected
   remaining raw Rust `u64`, identifier, and path table mappings.
6. Clarified that the maintained page describes `H1-HC01` prospectively until
   the checkpoint is created after reviews and validation.

The correction-2 integration reviewer reported the tracked activation evidence
file as absent. Parent verification confirms
`.pi/evidence/pi-harness-incubation/H1/activation.json` exists, is tracked in
commit `29eef9b5ed894d528d905f4556a905804983e305`, parses as JSON, and matches the
chain activation. The reviewer observation is retained but is factually
superseded; no contract edit was required.

H1 remains proposed and no successor is activated.
