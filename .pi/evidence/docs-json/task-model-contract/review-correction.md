# HarnessTask model-contract review correction

Review record: `.pi/evidence/docs-json/task-model-contract/integration-review.md`

Correction-pass count: 1

Review status retained: failed

## Finding dispositions

Finding 1 disposition: corrected

Finding 1 correction: All 19 interfaces, the version-2 schema, projection profile, fixtures, and manifests are now explicitly project-local. Public imports are proposed from `ksdft2effmass.harness.pi.local`. The existing version-1 pilot schema remains supported, and no generic `WireRecordKind`, `HarnessWireRecord`, `harness/pi` schema, or generic manifest change is proposed.

Finding 1 verification: Exact ownership, path, resource-ID, and generic-wire exclusion assertions passed.

Finding 2 disposition: corrected

Finding 2 correction: `HTM-03-014`, `HTM-04-012`, and `HTM-06-015` now use `DOCUMENTATION_OWNED_CONTENT`. Every mapping with a `docs/` target now has the documentation-owned disposition, while canonical exclusions may be extracted as a secondary target.

Finding 2 verification: All 118 spans were rehashed; ordered contiguous coverage remains complete; no canonical mapping retains a `docs/` target.

Finding 3 disposition: corrected

Finding 3 correction: The unjustified `packet_id` was removed. `HarnessTaskMigrationReviewPacket` now has the sole field `request`, so equal validated requests produce equal immutable packet values without a hidden identity algorithm.

Finding 3 verification: Contract assertion confirmed the sole request field and absence of the former packet-ID field.

Finding 4 disposition: corrected

Finding 4 correction: The file-disposition recorder now requires exact equality between `human_decision.packet` and `packet.request.human_review_packet`. A closed four-row compatibility table maps `accepted`, `bounded_correction`, `rejected`, and `deferred` to the four migration dispositions. Generic response recording and bounded-correction scope remain owned by `HumanReviewDecisionRecorder`.

Finding 4 verification: All four exact compatibility rows and the packet-equality rule are present.

Finding 5 disposition: corrected

Finding 5 correction: The contract freezes the project-local version-2 schema path and ID, projection profile path and ID, fixture index, valid fixture paths and IDs, exact invalid-fixture naming rules and IDs, manifest and oracle-index surfaces, and explicit dependency relationships. SHA-256 identities are calculated only after implementation bytes exist. The dedicated local serializer/deserializer remain outside generic wire kinds.

Finding 5 verification: Required paths, IDs, fixture families, dependencies, and wire exclusions are present without fabricated content hashes.

Finding 6 disposition: corrected

Finding 6 correction: `HarnessTaskGraphValidator` now treats status as opaque and performs structural graph validation only. Existing explicit Task/chain relation validation retains lifecycle compatibility policy.

Finding 6 verification: The former completed-prerequisite rule is absent and the explicit no-lifecycle-policy statement is present.

Finding 7 disposition: corrected

Finding 7 correction: Compatibility now covers the existing version-1 pilot plus all six Markdown records before migration, then the increasing version-2 JSON set and decreasing six-to-zero Markdown set after each accepted file migration.

Finding 7 verification: The incorrect five-record phrase is absent and both exact population obligations are present.

## Result

Material findings remaining: 0

Deterministic correction verification: passed

Human acceptance: pending

Stage-2 activation: not authorized
