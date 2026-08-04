## Review

**Verdict: FAIL**

- **Correct:** The contract remains non-implementation and correctly rejects workflow engines, dispatch/plugin frameworks, subprocess/Git mutation services, Graphify integration, and a third evidence-ownership kind (`contract-surface.md:5-14,100-109`).
- **Correct:** Resource paths, confinement, symlink rejection, explicit roots, and extension-only overlays are well bounded (`path-and-resource-resolution-contract.md:9-27,68-93,110-130`).
- **Correct:** Generic issue severity, duplicate keys, and total ordering are explicit (`issue-code-and-ordering-contract.md:40-64,74-109`).
- **Correct:** `docs/harness/ksdft2effmass.harness.02.md:3-14,224-230` accurately describes H1 as active, contract-only, and non-activating.

- **Blocker — RFC 8785 cannot preserve the declared integer domain:** `Version`, evidence range bounds, and occurrence lines permit integers through $2^{63}-1$ (`field-and-wire-contract.md:13,132,328`), while all public records require RFC 8785 canonicalization (`:34-46`). RFC 8785 number serialization uses the ECMAScript binary64 model. A concrete probe showed $2^{63}-1$ becoming `9223372036854776000`, so exact Python value equality, canonical bytes, and Python/Rust round trips cannot all hold. JSON integer bounds must be limited to an exactly representable domain or encoded differently.

- **Blocker — the exact public API omits types required by its own signatures:** The declared public surface (`contract-surface.md:16-64`) omits `WireRecordKind` and `HarnessWireRecord`, although callers must supply them to serialization actions (`:83-84`; `field-and-wire-contract.md:341-345`). It also omits the observable Python `HarnessInternalError` promised by action failures (`field-and-wire-contract.md:349-354`). Exporting these later would expand the supposedly closed API; not exporting `WireRecordKind` makes the decoder unusable.

- **Blocker — evidence policy remains insufficient for the demonstrated consumer:** `ProjectProfile` supplies only flat marker names, namespace tuples, and exact protected IDs (`field-and-wire-contract.md:132-135`), but does not define:
  1. how a tuple generates an evidence-ID string;
  2. which path/evidence class requires which marker and prefix; or
  3. how an unowned function is identified as a protected gap.

  The current auditor derives prefix and marker from the software/numerical path and records missing ownership as `(path, function)` with no evidence ID (`.pi/skills/audit_evidence_identifiers.py:45-55,218-259`). Its replay found the known 22 gaps as functions with no identifier. Therefore `protected_evidence_ids` cannot represent the demonstrated protected state, contrary to `AuditEvidenceIdentifiers` (`contract-surface.md:91`) and the correction claim (`review-corrections-round-1.md:16-20`).

- **Blocker — chain evaluation cannot distinguish an unknown prerequisite from an unsatisfied external prerequisite:** `TaskReference.prerequisite_ids` mixes task IDs and external-condition IDs (`field-and-wire-contract.md:255`), while `EvaluateChainState` receives only *satisfied* external IDs (`contract-surface.md:90`). An absent ID could therefore be either a typo requiring `PIH.CHAIN.PREREQUISITE_MISSING` or a valid but unsatisfied blocking condition. The current chain demonstrates this with `explicit_activation:H5` (`.pi/chains/pi-harness-incubation.chain.json:69-72`). Generic code cannot infer meaning from the colon because identifiers are explicitly opaque (`field-and-wire-contract.md:18-23`). Active/blocked/ready derivation is consequently not deterministic from the signature.

- **High — failure-code precedence is not complete:** Severity and sorting are fixed, but only checksum-entry/profile-identity precedence is specified (`issue-code-and-ordering-contract.md:49-64`). For example, `ValidateChecksumManifest` promises distinct invalid root, non-file, symlink, and malformed path failures (`contract-surface.md:92`), while the precedence section reserves its three checksum codes for entry comparison and otherwise refers to path/artifact codes during construction or resource resolution. Duplicate identifiers likewise have both generic and capability-specific codes without suppression rules. A complete condition-to-code/precedence table is still required.

- **High — local issue registration is unrepresentable:** The issue contract says a profile may register `LOCAL.<profile_id>.*` codes (`issue-code-and-ordering-contract.md:7-10`), and `ValidationIssue.code` must be registered (`field-and-wire-contract.md:298`). `ProjectProfile` contains no local code/severity registry (`:123-142`), generic code cannot interpret local codes, and direct `ValidationIssue` construction receives no profile. Local issues therefore cannot satisfy the intrinsic invariant without a prohibited ambient registry.

- **High — Rust mappings remain contradictory rather than exact:** `ValidationIssue.code` is mapped as “String/enum wrapper” and `path` as `Option<Path>` (`field-and-wire-contract.md:298-302`), while the exact Rust section says the code is an `Identifier` newtype and serialized paths use validated `ResourcePath` values (`:356-364,403-407`). `CheckpointRecord.record_paths` similarly says `Vec<Path>` (`:239`). `HarnessContractError` and `HarnessInternalError` have no defined variants or represented fields.

- **High — field-level demonstrated-consumer attestation is not established:** The matrix groups whole records rather than tracing each field and sometimes names prospective evidence:
  - `ArtifactIdentity.media_type` is attributed to checksum catalogs (`interface-decision-matrix.json:466-473`), but those catalogs contain only digest/path pairs (`.pi/evidence/pi-harness-incubation/H0/checksums.sha256:1-8`), and repository search found no non-H1 `media_type` consumer.
  - `ResourceManifest` field evidence includes the future H3 sequence rather than an exact current artifact (`interface-decision-matrix.json:483-489`).
  - Serialization results cite future H3 fixtures and future Python/Rust agreement (`:390-420`).
  - All operation-specific results are collapsed into one generic evidence group (`:582-590`).

  This does not satisfy the contract’s own field-level/current-consumer rule (`contract-surface.md:100-109`) and leaves speculative fields such as checksum manifest identity/version/root role unattested.

- **High — some record/result invariants remain non-exact:** `ArtifactIdentity.media_type` uses undefined “registered-style” syntax (`field-and-wire-contract.md:66`); checkpoint status/value contradiction rules have no truth table despite being promised by `ValidateCheckpointSet` (`contract-surface.md:89`); and `JsonSerializationResult.content_identity.media_type` is unspecified, allowing unequal results for identical canonical payloads (`field-and-wire-contract.md:66,330`).

### Residual risks

- H1 has no implementation, schemas, fixtures, or cross-language conformance tests; these findings are contract-level.
- H1 evidence is untracked and the maintained page is unstaged, so no durable reviewed artifact identity exists yet.
- The requested repository-root `plan.md` and `progress.md` were absent.
- The known 22 evidence-ID gaps remain protected migration debt; the current proposed profile cannot encode them.
- No files were edited or staged by this review.
