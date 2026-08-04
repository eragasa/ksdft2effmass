# Final H3 architecture / Rust / resource-contract re-review

## Verdict

No material architecture, generic/local dependency, schema/resource-identity, DiagnosticPath, or intended-Rust finding remains against the accepted H1/H3 contract. All three findings from the initial architecture review are closed.

## Initial-finding closure

1. **Schema and semantic boundary — closed.** `ResourceManifest` now encodes the `generic -> null` / `local -> Identifier` conditional (`harness/pi/schemas/records/resource-manifest.schema.json:53-80`), and `ProjectProfile` encodes paired null/non-null local manifest identity and version (`harness/pi/schemas/records/project-profile.schema.json:276-301`). The retained oracle fixes exactly seven negative cases: four schema rejections and three schema-accepted cross-value cases rejected by `DeserializeJsonRecord` as `PIH.WIRE.INVALID_VALUE` (`harness/pi/fixtures/semantic-invariants/oracle-index.json:3-83`). The affected record-schema descriptions explicitly assign non-portable cross-value checks to semantic validation (`harness/pi/schemas/records/resource-reference.schema.json:6,35-41`; `task-reference.schema.json:6,20-31`; `chain-view.schema.json:6,25-39`). Independent probes reproduced the 4-reject/3-accept boundary, verified all three semantic rejection predicates, and freshly mutated manifest, profile, and DiagnosticPath values; all expected structural mutations were rejected.

2. **Generic filename policy — closed.** The generic grammar delegates module placement and filename policy to an explicit local profile/extension and neither selects nor validates them (`harness/pi/skills/document-research-python/references/test-evidence-documentation.md:138-140`). The concrete convention remains solely local (`harness/local/extensions/evidence-documentation.md:23-35`). This conforms to H1's exclusion of universal filename rules.

3. **Neutral generic fixtures — closed.** The directory DiagnosticPath is now the neutral lexical spelling `tests/verification/directory-scope` (`harness/pi/fixtures/diagnostic-path/oracle-index.json:9-12`), while the generic profile fixture uses neutral `example.*`, `VX-*`, and `verification_*` values (`harness/pi/fixtures/valid/project-profile.json:2-77`). Canonical vectors identify only neutral future-consumer targets, including `intended Rust` (`harness/pi/fixtures/canonical/canonical-json-vectors.json:3-7`), cover the closed 16-record wire set plus the NFC DiagnosticPath spelling vector, and retain canonical JSON plus one LF and SHA-256 identities.

## Architecture and identity checks

- Generic and local manifests preserve extension-only direction: the local manifest extends `pih.generic.resources`; local resources may depend on generic IDs; no generic resource depends on a local identity. The generic tree leakage gate scans every file under `harness/pi/`, including fixtures and validator source (`harness/pi/validation/validate_h3_resources.py:595-630`), and passed.
- Independent SHA-256 replay matched the acceptance-index identities exactly: generic manifest `8a681a17ab9920b64c78ec76c3d8bb08d20924e6222cc5f9fcafdd6065f3b183`, local manifest `cb5556f1a2d924cb11094da99bfba8832a93edace99cd612db9d924db1577f98`, local profile `68c9fa503d7e53973bf4daa679e841268e25f0b546c84fa2536dc94c1f69a295`, and validator `db86f2adb546a27a068719b4886066985a91865564bc55cb9eb7757699687ae8` (`.pi/evidence/pi-harness-incubation/H3/acceptance-index.json`). All 23 generic and 3 local resource byte hashes also passed manifest replay.
- `ValidationIssue.path` remains `DiagnosticPath | null`, distinct from `ResourcePath` and `OwnershipScopePath` (`harness/pi/schemas/records/validation-issue.schema.json:104-113`; `harness/pi/schemas/records/common.schema.json:32-47`). Valid file/directory/null/NFC and the required invalid lexical families are retained.
- The canonical corpus is suitable for the accepted future Python/intended-Rust agreement boundary. It introduces no platform path, dynamic registry, Rust-only wire discriminator, float, or implementation dependency. No Rust implementation is claimed by H3.

## Commands and independent probes

- `python harness/pi/validation/validate_h3_resources.py` — PASS, 46 gates, 0 defects.
- `python .pi/task-ownership/validate_task_ownership.py --task H3 --chain .pi/chains/pi-harness-incubation.chain.json` — PASS.
- Independent Draft 2020-12 mutation probe — PASS: four schema-level negative cases rejected; three cross-value cases structurally accepted and independently confirmed intrinsically invalid with the exact retained semantic oracle; fresh manifest/profile/DiagnosticPath mutations rejected.
- Disposable-copy resource-byte mutation — PASS: changing the generic skill bytes made the validator exit 1 and report the exact manifest SHA-256 mismatch; repository files were not changed.
- Independent SHA-256 replay and generic-tree local-literal scan — PASS for the accepted identities and dependency/leakage boundary.

## Limitations

This was a read-only review of the current uncommitted H3 candidate. No future Python or Rust codec exists, so cross-language round trips and validated Rust newtypes/actions were not executable; the vectors establish intended portable inputs, not implementation conformance. No numerical/scientific validation, uncertainty quantification, human acceptance, successor activation, or protected execution is established by these software-verification checks.

Review status: PASS
