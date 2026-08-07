# M1 migration rationale

## Scope

Profile: `AUTHORIZED_TEST_EVIDENCE_WRITE`. The controlled batch contains 39 modules: the package-root artifact, 32 class-owned provenance modules, and 6 artifact-owned provenance integration modules. Operator, CPN, and harness test modules are excluded.

## Node preservation

`m1-node-migration-map.json` records all 1,252 baseline collected nodes one-to-one. Collection after migration is 1,266 nodes. The 14-node increase is separately enumerated in `m1-new-split-nodes.json`; none is represented as a migrated historical node.

## Semantic corrections

- `CapabilityKind` unknown-string construction and integer wrong-semantic-type construction were split into cohesive owners. `SV-PROV-177` remains with the unknown accepted-type partition; `SV-PROV-402` identifies the newly independent wrong-type owner.
- `RunManifest` frozen-state evidence now exercises all eight declared public fields through `FROZEN_FIELDS`. Equality evidence now independently varies all eight fields through `EQUALITY_FIELDS` while keeping every constructed terminal state valid. Fourteen additional collected field partitions result.
- Fixture case IDs retain their original paths and expected outcomes while naming scalar and extra-member defects without falsely combining unknown-value and wrong-type evidence semantics.
- Artifact module openings now agree exactly with their structured artifact ownership.
- `VerificationObservation` now declares complete frozen/equality field inventories matching its existing per-field cases.
- The package-root import test now has artifact-owned module/test documentation, a semantic public-API surface, and stable evidence ID `SV-PACKAGE-001`.
- The local project profile authorizes the existing `SV-PROV` namespace and the new package-root namespace; its resource-manifest digest is synchronized.

Assertions, fixture files, production behavior, existing evidence IDs, expected values, and tolerances were otherwise preserved.
