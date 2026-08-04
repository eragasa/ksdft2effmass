## Review

**Verdict: FAIL**

- **Correct:** DataObject, ActionObject, ResultObject, support-type, and Rust action boundaries are explicitly separated (`contract-surface.md:20-77`; `field-and-wire-contract.md:333-428`).
- **Correct:** Explicit roots, lexical/resolved confinement, symlink rejection, extension-only overlays, and prohibition of ambient discovery are coherent (`path-and-resource-resolution-contract.md:7-93,100-144`).
- **Correct:** Capability primary owners, generic-to-local dependency direction, exclusions, and the blocked `H3 → H2 → H4` sequence are consistent (`contract-surface.md:119-168`; `h3-h2-ownership-plan.json:5-23`).

- **Blocker — closed diagnostic contract cannot represent all promised malformed inputs:** `DeserializeJsonRecord` promises structured `FAIL` for every invariant failure (`contract-surface.md:91-93`), but the closed registry has no general invalid-value code (`issue-code-and-ordering-contract.md:19-34`). For example, `ProjectProfile.overlay_policy` accepts only `extend_only` (`field-and-wire-contract.md:128`); another string has the correct JSON/Python type but violates the invariant, matching neither `PIH.WIRE.INVALID_TYPE` nor a registered profile condition. The contract forbids squeezing unregistered conditions into unrelated codes and forbids generic local codes (`issue-code-and-ordering-contract.md:7-15,36-39`). Conversely, `PIH.ARTIFACT.MEDIA_TYPE_INVALID` remains registered (`:26`) although `ArtifactIdentity` explicitly has no media-type field (`field-and-wire-contract.md:71-76`). The closed Python/Rust failure protocol is therefore incomplete and internally stale.

- **Blocker — manifest revision/content is not bound by the profile or action inputs:** `ResourceManifest` carries a meaningful `manifest_version` (`field-and-wire-contract.md:103-108`), but `ProjectProfile` names only manifest IDs (`:126-127`). `ResolveResource` receives no expected manifest version or manifest byte identity and checks only those IDs/base relation (`path-and-resource-resolution-contract.md:100-113`). This contradicts the claim that manifest compatibility is independently checked (`:132-150`) and the rule that resource-entry changes advance the manifest version (`version-boundaries.md:53-55`). Two structurally valid manifests with the same ID but different revisions—or different contents under the same ID/version—cannot be distinguished against profile policy.

- **Blocker — `EvaluateChainState` does not define its derived facts:** The action promises deterministic active, blocked, and ready tuples (`contract-surface.md:98`; `field-and-wire-contract.md:341`), but no truth table defines whether these derive from declared status, prerequisite satisfaction, explicit activation, checkpoints, or combinations thereof. In particular, the result for a task declared blocked whose prerequisites are satisfied, or a structurally ready task awaiting required activation, is unspecified. The role of the `checkpoints` argument in derivation is also undefined. Python and Rust could therefore produce different valid-looking outputs from identical inputs.

- **High — checksum decision evidence contradicts the corrected exact fields:** The decision matrix still defines `ChecksumManifest` as “versioned” and “bound to an explicit root role” (`interface-decision-matrix.json:158-167`), while its own field trace says entries plus `schema_version` only (`:589-593`) and the field contract explicitly excludes catalog version and root-role fields (`field-and-wire-contract.md:289-300`). H3 schema authors would face conflicting H1 authority.

### Residual risks

- H1 remains proposal-only; no schemas, fixtures, implementation, or cross-language conformance evidence exists.
- All H1 contract artifacts remain untracked, so this review attests only the inspected worktree snapshot.
- Successor manifests and agent records remain intentionally absent and require separate activation/preflight.
- Repository-root `plan.md` and `progress.md` were absent.
- No files were edited or staged by this review.
