# M4 migration rationale

M4 closes the 47 remaining inventory entries: 35 class-owned and 12 artifact-owned software-verification modules under the generic and local harness test hierarchy. The baseline contains 120 expanded pytest nodes. `m4-node-migration-map.json` preserves all 120 one-to-one; the focused multiline Evidence ID regression is the sole new node and is recorded separately.

The migration retains every pre-existing evidence identifier. The previously unowned H4/local tests now own `SV-HL-014` through `SV-HL-037`; the parser regression owns `SV-HARNESS-066`. These 25 new owners are listed in `m4-new-evidence-owners.json` and are not represented as migrated historical IDs.

Mechanical changes replace superseded module headings, blanket E501 suppression, hidden loop statements, unstable parameter IDs, vague or nonconforming names, and incomplete helper prose. Cohesive dynamic artifact inventories use named local case executors; they retain one artifact relation and one acceptance rule rather than claiming independently collected cases. Current route/completion evidence was corrected to the maintained local route and same-run count contract. Test-owned context helpers now state their assumptions and own no evidence result.

Production `AuditEvidenceIdentifiers` retains its pre-task `clean=False` behavior. Current maintained IDs are established by the structural validator and the authorized test-local cleaned-docstring audit described in the M3 diagnostic; M4 makes no production-parser correction claim. Profile namespace maxima and manifest identities were synchronized to the complete current inventory; the formerly protected-unowned classification fixture now represents its conforming owner. Historical H1-H4 reports and checksum evidence were not rewritten.

All M4 evidence is software verification. Passing does not establish numerical verification, scientific validation, UQ, physical correctness, portability, release readiness, or human acceptance.
