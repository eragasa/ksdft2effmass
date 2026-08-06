# P2-TOOLS-DECOMPOSITION-1 parent verification

Status: **PASS_DURABLE_BOUNDARY_PENDING_COMMIT_AND_P2_HC05_HUMAN_ACCEPTANCE**

Starting revision: `fc2e8fc3ceb9336e9b6e94e8583271da5877488b` (`HEAD == origin/dev` after `git fetch origin dev`). P2 remained open with sole pending checkpoint `P2-HC04`; P3, H5, protected execution, publication, and release were inactive. The selected maintained route was `local` and its two checks passed.

## Public and source boundary

Documentation supports exactly `ksdft2effmass.provenance`, not the former implementation path `ksdft2effmass.provenance.tools`; `tools.py` was removed rather than retained as a facade. `external_tools.py` owns the four declaration types, `tool_observations.py` owns the three observation types, and `external_execution.py` owns its three enums, three records, and internal outcome alias. The three leaf modules do not import actions or serialization. The static graph is acyclic.

All 32 package exports are unchanged. Baseline/current inspection found unchanged constructor signatures, enum names/order/values, dataclass fields, frozen behavior, and slots for every package class; only the expected defining-module origins changed. `actions.py`, `serialization.py`, and `__init__.py` changed only import/type/export wiring. Strict version-1 discriminators and field mappings are unchanged. `_require_text`, `_require_identifier`, `_require_version`, `_require_sha256`, `_require_identifier_tuple`, and `_require_root_relative_path` were removed without replacement helper functions/classes; each moved record directly owns intrinsic validation.

## Skills and evidence

The repository-local `develop-python-test-evidence` skill/profile selected was `AUTHORIZED_TEST_EVIDENCE_WRITE`; the repository-local `document-python-research-software` profile selected was `AUTHORIZED_DOCS_WRITE`. These selection facts are separate from validator outcomes. The exact generic-validator command and complete JSON output are preserved in `tools-decomposition-test-evidence-implementation.md`.

The exact 13 class-owned software-verification modules contain 85 test functions/evidence owners, 145 collected cases, and no helpers. Twenty-four historical nodes retain IDs `SV-PROV-024` through `045`, `074`, and `078` through a complete one-to-one map. The 121 genuinely new nodes use owner-specific IDs `SV-PROV-176` through `236`. Structural validation returned PASS with zero findings. It did not establish oracle independence, semantic completeness, scientific validity, UQ, or human acceptance; those claim boundaries were separately reviewed.

## Deterministic validation

- Import graph: seven modules, acyclic; declaration/observation/execution leaves have no provenance imports.
- Exact 13 modules: `145 passed`; complete provenance class-owned directory: `493 passed`; five focused integration modules: `144 passed`.
- Diagnostic branch coverage: `external_tools.py` 89% with 7 uncovered statements/partial branches; `tool_observations.py` 75% with 23; `external_execution.py` 75% with 48. These gaps are reported rather than hidden with meaningless tests.
- Ruff format/lint: PASS. Focused mypy: PASS, 40 files. Sphinx `-W`: PASS, 45 sources.
- Package export identity and baseline shape: PASS. Strict serialization, canonical JSON vectors, valid/invalid fixture behavior: PASS.
- Schema/fixtures: 45 files unchanged, aggregate SHA-256 `d0c6e4d849ec51e6c01d4cdb9255b3612720b7d6c706d9b6f84d32249108d453`.
- `python/pyproject.toml`, `python/uv.lock`, and `package-lock.json` retained SHA-256 `5d631881...`, `186504b6...`, and `a5e07678...` respectively.
- Clean wheel: exactly seven provenance Python modules, no `tools.py`; clean temporary installation and all 32 public imports passed. Generated build output was removed.
- Task ownership, current P2 completion, skill capability, checkpoint, selected local harness route, and `git diff --check`: PASS.
- The historical actions-correction validator's old `__init__.py` byte-hash guard is inapplicable to this newly authorized import wiring, as judged by the sole reviewer. Its historical baseline and R1/R2 were not rewritten; no R3/E3 was created.

## Review and correction

The sole independent reviewer returned one medium finding: `SV-PROV-226` called the internal `ExternalExecutionOutcome` alias public. The single consolidated correction pass removed that unsupported public claim and documented the alias as an internal collaborator with no separate owner while retaining the explicit human-required result/failure alias assertion and unchanged package exports. All affected deterministic gates were rerun and passed. No second review occurred.

The two artifact-owned integration evidence modules for import direction and wheel content were mechanically synchronized by the parent integration owner because the former expected inventories required `tools.py`; the reviewer judged both changes necessary, in scope, and nonsemantic.

Unrelated working-tree paths remain unstaged and excluded. P2-HC04 is superseded without human acceptance; renewed final acceptance is pending at P2-HC05. P2 remains open and unaccepted. No successor, protected execution, publication, or release was activated. Software verification establishes none of external-tool availability, execution validity, numerical verification, scientific validation, UQ, physical correctness, provenance truth, publication readiness, release readiness, or human acceptance.
