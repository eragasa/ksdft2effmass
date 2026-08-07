# M3 operator evidence migration rationale

M3 migrated the complete 59-module operator inventory selected from the maintained-test inventory: 52 class-owned software-verification modules, four class-owned numerical-verification modules, three artifact-owned integration modules, and the class-owned `OperatorRecordComparator` Workflow included in the 52. The operator fixture support module was migrated with the tests but is not a collected evidence owner.

Before mutation, M3 durably captured 920 exact pytest node IDs and SHA-256 identities in `m3-historical-node-inventory.json`. `m3-node-migration-map.json` maps every historical node to exactly one unique successor. Three artifact filenames were canonicalized to lowercase artifact-owned names. Semantic test names now identify constructor, field, property, method, protocol, artifact, public-API, or workflow surfaces.

The migration preserved all historical evidence identifiers, public calls, represented mathematics, literal expected values, exception classes/messages, exact comparisons, numerical tolerances and ULP bounds, units, warning-as-error policy, fixtures, and assertions. Thirty-nine additional collected nodes expose cases formerly hidden in loops or split wrong-type, unknown-value, threshold, constructor/field, schema/runtime, and warning-policy partitions. They are listed separately in `m3-new-split-nodes.json` and do not appear as historical successors.

Thirty-six new evidence owners were necessary: 22 formerly unowned public tests and 14 new cohesive split owners. Their durable identifiers and rationales are recorded in `m3-new-evidence-owners.json`. No historical evidence record was rewritten.
