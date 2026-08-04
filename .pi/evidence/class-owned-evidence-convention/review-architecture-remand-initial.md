# EVIDENCE-DOC-1 review: **FAIL**

The code/documentation correction itself passes, but durable review evidence is stale.

## Passing findings

- Ownership preflight passed; manifest assigns this architecture/VVUQ reviewer.
- Completion validator passed: 2 modules, 12 tests, 12 IDs, 12 node mappings, 96 inventoried modules.
- `FiringRequest` module:
  - exact required headings and seven per-test fields;
  - semantic names following `test_<surface>__<facet>__<behavior>`;
  - sole primary SUT is `FiringRequest`;
  - `TransitionBinding` is only a constructor collaborator;
  - all three oracles independently derive from public invariants and Python error taxonomy;
  - stable IDs `SV-CPN-037`, `068`, and `069`;
  - 3 tests passed and exactly 3 nodes collected.
- Normalized AST comparison against `HEAD`, removing only module/test docstrings and test names: identical. Executable bodies, assertions, exception checks, fixtures, parameterization, production behavior, and tolerances are unchanged.
- Node map, ownership manifest, migration inventory, and documentation agree.
- P1 ownership audit passed: 32 class modules, 5 artifact modules, 49 exports, 88 IDs.
- Checkpoints: 9 valid, 0 unresolved; chain JSON valid.
- P1 remains closed as human-accepted PASS; P2–P11 and production/scientific execution remain blocked.
- Both checksum inventories passed: 26 EVIDENCE-DOC-1 entries and 116 P1 entries.
- Evidence audit: 0 errors; 22 known protected historical warnings.
- `git diff --check` passed.

## Blocking finding

The checksummed durable final-review records still describe the pre-remand, CpnToken-only state:

- `.pi/evidence/class-owned-evidence-convention/review-architecture-vvuq-final.md:4-7` reports 9 tests/mappings and only focused `CpnToken`.
- `.pi/evidence/class-owned-evidence-convention/review-integration-final.md:4-9` likewise reports 9 tests and does not review `FiringRequest`.

This contradicts the claimed post-remand re-review completion at `.pi/tasks/class-owned-evidence-documentation-convention.md:54-56`. Checksums establish byte integrity, not semantic currency.

**Required deterministic correction:** durably record the consolidated post-remand reviews, regenerate affected checksums, and replay validation. No scientific or API decision is required.

**Mutation summary:** no edits performed.