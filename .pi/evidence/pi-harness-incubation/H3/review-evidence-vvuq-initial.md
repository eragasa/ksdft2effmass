# Independent H3 fixtures/evidence/VVUQ review

## Findings

### F1 — Material claim-boundary defect

`.pi/evidence/pi-harness-incubation/H3/validation-results.json:112` excludes only numerical verification **“beyond deterministic wire/hash behavior exercised by the validator.”** That wording leaves deterministic wire/hash behavior inside a numerical-verification claim. This conflicts with the accepted evidence grammar: numeric values or exact hashes used to check a software/wire contract remain software verification, and the local fixture index expressly says the `numerical_verification` label is classification input only and that no numerical result is claimed (`harness/local/fixtures/oracle-index.json:5`). It also conflicts with the same retained result's correct description of the 46 gates as software-verification gates (`validation-results.json:104`). H3 establishes structural/textual software verification only; it performs no numerical verification. The retained pre-review evidence therefore does not yet have a consistently correct software-verification-only boundary.

### F2 — Coverage weakness in the protected-debt classification oracle

The protected warning fixture records the expected classification `software_verification-only; no numerical/scientific claim` (`harness/local/fixtures/evidence-classification/cases.json:55-66`), but `evidence_oracle_gate` checks `expected.classification` only when status is `PASS` (`harness/pi/validation/validate_h3_resources.py:532-534`). The protected case has status `WARN`, so changing or deleting that claim-boundary value would not fail the completion validator. The WARN code/status behavior itself is exercised correctly; the classification/claim text is not enforced by that gate.

## Independently verified evidence

- **All 16 public schema pairs:** a separate Draft 2020-12/jsonschema run found zero errors for every valid fixture and at least one expected rejection for every invalid fixture. The closed ordered set is declared in `harness/pi/fixtures/fixture-index.json:3-20`; invalid causes covered role enum, lowercase digest, nonempty collections, UTC timestamp form, absolute path, positive line, scope enum, overlay policy, resource kind, termination policy, Boolean type, fixed issue severity, and result status/severity consistency. This agrees with the validator's closed-set requirement (`validate_h3_resources.py:155`).
- **DiagnosticPath:** independently checked the four required positive forms (regular file, directory-tree scope, `null`, and NFC Unicode) and all 19 indexed negatives: POSIX absolute; `.`/`..`; non-NFC; empty; empty/repeated/trailing segments; C0/C1 and U+2028; backslash; drive absolute/relative; device/UNC; leading `//`; and unpaired surrogate (`harness/pi/fixtures/diagnostic-path/oracle-index.json:5-121`). Exact valid spelling is retained. The `ValidationIssue.path` schema references `DiagnosticPath | null` (`harness/pi/schemas/records/validation-issue.schema.json`), consistent with the accepted H1 correction and H3 requirement (`.pi/tasks/pi-harness-incubation-H3-resources.md:31-35`).
- **Canonical vectors:** independently recomputed canonical bytes and SHA-256 for all 17 unique vectors. Vectors 001–016 correspond one-to-one, in the required spelling/order, to the 16 public record kinds; vector 017 preserves the exact NFC spelling `résultats/café.json` (`harness/pi/fixtures/canonical/canonical-json-vectors.json:122-143`). All members use integer/no-float data and ASCII member names, so the independently recomputed compact, sorted UTF-8 JSON plus one LF agrees with the declared RFC 8785 bytes for this corpus. These are fixture identities only, not future Python/Rust conformance.
- **Resolution oracles:** independently reviewed all 18 cases in `harness/pi/fixtures/resource-resolution/oracle-index.json:4-164`: missing dependency, duplicate ID/path, incompatible format/profile, generic-to-local dependency, extend-only overlay collisions, missing/not-found/not-file/hash/case errors, two successful generic/local resolutions, and symlink cases. The declarative outside-root symlink correctly yields `PIH.PATH.SYMLINK`, not escape, because H1 orders symlink rejection before resolved confinement; the disposable-only policy is explicit at line 166. The in-root symlink is likewise rejected. Expected values are anchored in the accepted H1 precedence rather than inferred from the validator output.
- **Software/numerical classification:** the six cases cover positive software and numerical labels, both cross-namespace negatives, undeclared marker rejection, and protected-gap WARN (`harness/local/fixtures/evidence-classification/cases.json:5-66`). The behavior is correct, subject to F2. These are classification tests only and supply no numerical result.
- **Protected local debt:** independently parsed the profile and actual Python tests. There are exactly 22 unique, strictly sorted entries, all under software verification; every named file and function exists. This agrees with the local extension's explicit debt statement (`harness/local/extensions/evidence-documentation.md:42-44`). They remain warnings, not assigned evidence or authorization to edit.
- **Ownership and separation:** the version-2 ownership preflight passed. Generic resources, local resources, fixtures, validator, documentation, and H3 evidence have six distinct writer roles and non-overlapping path scopes (`.pi/evidence/pi-harness-incubation/H3/task-ownership.json:8-41`). The evidence/VVUQ reviewer is read-only and separate from every writer (`task-ownership.json:44-54`).
- **Pre-review state:** the completion validator ran successfully with `H3 VALIDATION PASS`, 46 gates and 0 defects. This deterministic pass does not cure the independently identified retained-evidence claim defect.

## Commands run

- `python harness/pi/validation/validate_h3_resources.py` — PASS, 46 gates, 0 defects.
- `python .pi/task-ownership/validate_task_ownership.py --task H3 --chain .pi/chains/pi-harness-incubation.chain.json` — PASS.
- Independent Python/jsonschema validation of all 16 valid/invalid schema pairs — all 16 valid accepted and all 16 invalid rejected.
- Independent AST/profile inventory of protected debt — 22/22 unique and present.

## Limitations

This was a read-only review of textual fixtures, schemas, profiles, validator logic, ownership, and retained pre-review evidence. It did not execute H2, establish future Python or Rust conformance, perform scientific calculations, numerical verification, scientific validation, uncertainty quantification, or grant human acceptance/activation.

Review status: FAIL
