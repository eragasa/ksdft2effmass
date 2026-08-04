# Final H1 architecture review — FAIL

## Findings

1. **BLOCKER — task-ownership review preflight fails.**
   `python .pi/task-ownership/validate_task_ownership.py --task H1` failed with:

   > `task ownership preflight failed: expected exactly one chain task 'H1'`

   `.pi/chains/pi-harness-incubation.chain.json:45-48` identifies H1 but names no ownership manifest. Consequently, no validated manifest assigns `ksdft2effmass.ksdft2effmass-architecture` as an independent reviewer. This blocks attested production-task planning review under the architecture-agent control-plane contract. The absence is intentional for contract-only H1, but the present review includes the production ownership plan for H3/H2/H4.

2. **BLOCKER — complete explicit policy data remains unresolved for local issue codes.**
   `.pi/evidence/pi-harness-incubation/H1/issue-code-and-ordering-contract.md:9-10,35-38,49-54` permits profiles to register local codes and gives them observable severity semantics. However, `ProjectProfile` has no local issue-code registry or code-to-severity mapping among its complete fields at `.pi/evidence/pi-harness-incubation/H1/field-and-wire-contract.md:123-142`. Meanwhile, `ValidationIssue.code` requires a registered code (`:298`) and the Rust contract says “the registry validates it” (`:356-358`).
   The contract therefore does not specify how Python or Rust validates a profile-owned local code. Human authority must either:
   - add complete immutable local-code registration data and validation rules; or
   - remove local-code registration from the generic H1 contract and leave local diagnostics entirely outside it.

## Prior architecture findings

| Required correction | Result | Evidence |
|---|---|---|
| Ownership scope type | Resolved | `OwnershipScopePath` and `OwnershipScope` file/tree semantics: `field-and-wire-contract.md:12,177-188`; confinement: `path-and-resource-resolution-contract.md:25-39`. |
| Complete explicit policy data | **Not resolved** | Operational resource, skill, evidence, and lifecycle fields were added at `field-and-wire-contract.md:129-142`, but local issue-code registration remains absent as described above. |
| Named serialization/results | Resolved | `contract-surface.md:37-64,83-84`; concrete results at `field-and-wire-contract.md:319-345`. |
| Normalized agent view | Resolved | `AgentDescriptorView` at `field-and-wire-contract.md:189-197`; generic validator consumes normalized agents in `contract-surface.md:88`. |
| Closed integer versions | Resolved | `field-and-wire-contract.md:13`; `version-boundaries.md:42-48,62-72`. |
| Capability ownership | Resolved | One-primary capability matrix and explicit dependency direction: `contract-surface.md:111-141`; scientific/domain behavior is excluded rather than assigned to local harness Python. |
| DataObject/ActionObject/Rust boundary | Resolved | Exact public object categories in `contract-surface.md:20-64`; explicit Rust newtypes, structs, errors, bytes/paths, and action signatures in `field-and-wire-contract.md:347-405`. |

The H4 ownership, exact handoff paths, H3 schema owner, documentation status, and H2 local-Python ambiguity identified by the initial integration review were corrected in `h3-h2-ownership-plan.json:79-146,213-271,315-468`, `docs/harness/ksdft2effmass.harness.00.md:9-16`, and `.pi/tasks/pi-harness-incubation-H2-python-core.md:5-8`.

## Residual risks

- All H1 evidence files remain untracked; this verdict attests the inspected working-tree snapshot, not a committed/checksummed contract identity.
- H1 remains proposal-only: no H3 schemas/fixtures, H2 implementation, or executable software-verification evidence exists.
- Future H3/H2/H4 agent records and task manifests do not yet exist and must pass their own preflight before launch.
- H1-HC01 human acceptance remains required. This review does not accept the public API, serialization contract, architecture, or successor activation.
- No numerical verification, scientific validation, or UQ applies to this contract-only task.

## Inspection and validation

Inspected all 15 current H1 evidence files, retained initial reviews and correction record, both requested harness pages, H1/H2 task records, both controlling chains, the architecture agent record, and the authoritative DataObject/ActionObject skill/reference.

No files were edited or staged.
