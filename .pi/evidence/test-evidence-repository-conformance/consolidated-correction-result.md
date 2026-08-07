# TEST-EVIDENCE-CONVENTIONS-2 consolidated correction result

Status: **correction implemented; deterministic gates pass except the separately reported wheel environment setup errors**.

Independent review input is retained verbatim at `consolidated-independent-review-fail.md`, copied from `.pi-subagents/artifacts/69659f6d_ksdft2effmass.ksdft2effmass-integration-reviewer_0_output.md`.

## Corrections

- **B1:** restored `python/src/ksdft2effmass/harness/pi/evidence.py` exactly to its pre-task `clean=False` behavior. Removed the dependent `SV-HARNESS-066` test and M4 new-node/new-owner claim. M4 now identifies the authorized structural validator plus test-local clean-docstring audit as the current-ID evidence and makes no production parser claim.
- **H1:** replaced exactly 105 generated/tautological function and nontrivial-helper blocks across the 21 reviewer-identified modules. A repeat search for the reviewed generated phrases returns no match.
- **H2:** broadened complete-equality/frozen recurrence recognition to contextual synonyms, added controlled synonym defects and unrelated-prose false-positive guards, and synchronized the durable fixture inventory. Added literal field inventories where field-complete claims remain. `OperatorRecordDifferenceResult` now explicitly inventories and exercises `compatibility_result`, `matrix`, and `energy_unit` for frozen state and exact equality. Narrower representative tests no longer claim complete state.
- **H3:** no backend-independent derivation supports the unchanged eight-ULP/64-epsilon thresholds for every scalar, scaled-Frobenius, and SVD path. Rather than invent one, retained only exact-zero `NV-ORA-017` in numerical verification and moved ten threshold-only nodes to the software-verification regression facet. `consolidated-correction-node-map.json` records the eleven-node closed mapping (ten moves plus exact-zero identity); `consolidated-correction-evidence-id-map.json` records predecessor `NV-ORA-007`--`016` to successor `SV-ORA-007`--`016`. Tolerances were not changed.
- Added the required explicit `--chain .pi/chains/test-evidence-repository-conformance.chain.json` ownership preflight to the active task and control record.

## Updated identities and counts

- discovered/inventoried modules: **183 / 183**;
- class-owned/artifact-owned: **156 / 27**;
- software/numerical verification: **179 / 4**;
- test functions / unique evidence owners: **1,020 / 1,020**;
- collected nodes: **2,568**;
- static parameter cases: **1,907**;
- structural findings: **0**;
- strict test-local ID audit: **1,020 occurrences, 1,020 unique IDs, 0 issues**;
- M1--M4 plus correction maps: unique and set-complete.

## Validation disposition

- ownership preflight with explicit chain: PASS;
- repository structural gate: PASS;
- strict test-local ID audit: PASS;
- focused correction pytest: PASS, 545 tests;
- validator recurrence pytest: PASS, 62 tests;
- full maintained pytest: 2,566 passed and 2 setup errors; both setup errors are the pre-existing wheel fixture environment boundary because `python/.venv` has no `pip`; no assertion failed;
- Ruff over all 183 inventoried modules and validator tests: PASS after the final one-line wrap correction;
- focused mypy over validators and 14 correction-sensitive modules: PASS, 16 source files;
- H3 resource gate: PASS, 58 gates and 0 defects;
- current local-route replay: PASS, 3 checks;
- migration reconciliation: PASS;
- production-source diff: empty after B1 reversion;
- staged files: none.

No scientific validation, UQ, physical correctness, release readiness, or human acceptance is established.

## Process note

One deterministic identifier-prefix replacement was executed through a short `python -c` command before the same operation was incorporated into the retained `consolidated_correction_h3.py` command. This did not widen mutation scope or change values/tolerances, but it did not follow the request's command-form preference against ad-hoc inline migration commands and is reported rather than concealed.
