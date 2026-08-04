## FAIL — durable review-evidence inconsistency

### Material finding

The remand correction itself passes, but the checksummed independent-review artifacts were not updated:

- `.pi/evidence/class-owned-evidence-convention/review-architecture-vvuq-final.md:4-8`
- `.pi/evidence/class-owned-evidence-convention/review-integration-final.md:4-9`

Both still report the pre-remand **9-test CpnToken-only** scope and omit the three `FiringRequest` nodes. This conflicts with:

- the requirement to update independent review: `.pi/checkpoints/EVIDENCE-DOC-1-HC01-final-acceptance.json:44`
- the claim that remand re-reviews passed: `.pi/tasks/class-owned-evidence-documentation-convention.md:56`
- the current 12-test documentation: `docs/verification/testing-and-evidence.rst:925-935`

The stale artifacts are themselves included in the checksum catalog at `.pi/evidence/class-owned-evidence-convention/checksums.sha256:22-23`; checksum validity therefore proves file integrity, not current review coverage.

### Checks passed

- EVIDENCE-DOC-1 ownership preflight; reviewer assignment confirmed at `task-ownership.json:41-50`.
- EVIDENCE-DOC-1 completion validator: **2 modules, 12 tests, 12 IDs, 12 mappings, 96 inventoried modules**.
- P1 ownership preflight and validator: **32 class modules, 5 artifact modules, 49 exports, 88 IDs**.
- `FiringRequest` three-node names and one-to-one mappings: correct.
- Focused pilots: **12 passed**.
- Complete P1 test surface: **91 passed**.
- Executable AST comparison against `HEAD`: unchanged after removing test names/docstrings for both pilot modules.
- Evidence audit: `audit_errors=0`; 22 protected historical warnings unchanged.
- Both checksum catalogs: all entries valid.
- Checkpoint validator: 9 valid, 0 unresolved.
- Sphinx locked docs environment, warnings-as-errors: **33 pages, passed**.
- `git diff --check`: passed.
- Chain state: P1 human-accepted and closed; EVIDENCE-DOC-1 remand active; P2–P11 blocked (`chain.json:25-36`, `113-114`).
- Checkpoint B is durably resolved; final acceptance remains ungranted (`EVIDENCE-DOC-1-HC01-final-acceptance.json:41-50`).

No files edited. Human final acceptance remains blocked pending corrected durable independent-review evidence.