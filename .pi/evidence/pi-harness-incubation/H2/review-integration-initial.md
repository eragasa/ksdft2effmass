# Initial integration review

- **Result:** FAIL
- **Run:** `dcf7a711-4e3f-4905-a8e1-0b5830ffac2d`
- **Reviewer:** `ksdft2effmass-harness-python-integration-reviewer`
- **Source:** `.pi-subagents/artifacts/dcf7a711-4e3f-4905-a8e1-0b5830ffac2d_ksdft2effmass.ksdft2effmass-harness-python-integration-reviewer_2_output.md`
- **Mutation:** read-only; no repository edits or staging.

## Findings

1. **HIGH:** wire serialization/deserialization used reflection and a class registry contrary to the accepted fixed-union contract (`validation.py:291-328,383-428` at review time).
2. **MEDIUM:** generic source used a prohibited dynamic absolute project import in `resources.py:471-473`.
3. **MEDIUM:** H2 fixture paths depended on repository-root cwd. Repo-root Python tests passed 1057, while `cd python && pytest -q` produced 20 failures and 1037 passes.
4. **MEDIUM:** the completion validator suppressed `E501`; configured full Ruff reported 332 pre-existing line-length failures while the focused validator subset passed.

## Commands observed

- `uv run --isolated --offline --locked --project python --extra dev --extra docs python python/tests/software_verification/ksdft2effmass/harness/pi/validate_h2_completion.py` — **PASS**, 39 modules and 45 evidence IDs.
- `source .venv/bin/activate && python -m pytest -q python/tests` — **PASS**, 1057 tests.
- `source .venv/bin/activate && cd python && python -m pytest -q` — **FAIL**, 20 failed/1037 passed.
- `source .venv/bin/activate && python -m ruff check python/src python/tests` — **FAIL**, 332 `E501` findings.
- `uv run --isolated --offline --locked --project python --extra docs sphinx-build -W -b html docs <temp-output>` — **PASS**, 42 sources.
- Offline wheel build/install/import from a temporary neutral cwd — **PASS**; all ten harness modules packaged and 41 public names imported.
- `python .pi/checkpoints/validate_checkpoints.py && git diff --check` — **PASS**.
- Dependency/lock checksum comparison and `git diff --cached --quiet` — **PASS**.

Residuals were filesystem TOCTOU limits, CPython 3.14/macOS-only packaging coverage, and absent executable Rust conformance. No numerical-verification, scientific-validation, or UQ claim was made.
