# V2-ISSUE-010: Package dependency graph consistency

**Severity:** High

**Scope:** Architecture v2 package boundaries

## Conflict

The v2 system overview shows runtime/control-flow arrows from scientific workflow to calculators and from analysis back to workflow. The normative repository layout instead requires calculator implementations to depend on generic scientific-workflow contracts and gives inconsistent direction for scientific-analysis contracts. Runtime orchestration and static imports are not clearly distinguished.

## Affected contracts

- `index.md` — *System overview*
- `repository-layout.md` — *Dependency direction*
- `principles.md` — *Calculator independence*

## Required resolution

Define one normative static import graph and label runtime/control-flow diagrams separately. If generic executor and analysis result/protocol contracts are workflow-owned, state `calculators → workflow.scientific` and `analysis → workflow.scientific` consistently while preserving runtime dispatch through injected implementations.

## Acceptance condition

Every required and forbidden package edge is consistent across diagrams, prose, and future dependency-validator policy.
