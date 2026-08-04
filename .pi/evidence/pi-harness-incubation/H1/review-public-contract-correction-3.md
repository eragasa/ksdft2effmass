# FAIL

## Review
- **Correct:** Chain-state truth table is internally coherent, including activation handling and active/blocked overlap (`field-and-wire-contract.md:291-323`).
- **Blocker:** `contract-surface.md:92` requires an unregistered serializer input to return `FAIL`, while `contract-surface.md:83-85` permits `TypeError` for wrong argument types and `issue-code-and-ordering-contract.md:80` provides no diagnostic assignment for an object outside the closed union. The observable API behavior remains contradictory.
- **Blocker:** `ValidateSkillResources` promises forbidden-overlay findings and accepts manifest identities (`contract-surface.md:102`), but its diagnostic allocation omits manifest/overlay codes (`issue-code-and-ordering-contract.md:90`). Using a skill code would violate the prohibition against repurposing unrelated codes (`issue-code-and-ordering-contract.md:36-40`).
- **Blocker:** `HarnessContractError` appears in the exact Python public API (`contract-surface.md:16,50-57`) but is defined and owned only as a Rust constructor error (`field-and-wire-contract.md:399-410`; `interface-decision-matrix.json:469-476`). Its Python export status is unresolved.
- **Blocker:** Consumer traceability for `HarnessContractError` cites only a Rust-mapping requirement, not a current consumer (`interface-decision-matrix.json:469-476,687-692`), contradicting the current-consumer rule (`contract-surface.md:109-118`).
- **Note:** Review was restricted to the six requested artifacts; referenced external consumers were not independently verified.
