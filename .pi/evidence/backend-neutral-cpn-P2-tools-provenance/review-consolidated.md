# Consolidated P2 review: **FAIL**

One bounded consolidated correction cycle is required. No files were edited, no external/scientific tools were run, and no successor/checkpoint was activated.

## Control-plane preflight

- Ownership preflight: **PASS**
  - Manifest assigns this reviewer at `.pi/evidence/backend-neutral-cpn-P2-tools-provenance/task-ownership.json:45-50`.
- Completion validator: **PASS**
  - 33 exports, 25 class-owned modules, 35 fixtures, one schema.
- Local harness route: **PASS**, selected route `local`.
- Checkpoints: **PASS**, 22 valid, zero unresolved.
- P2 remains active; H5 and P3–P11 remain inactive/blocked.
- Manifest version 2 does not enable `evidence-branches-v1`; branch-profile review is therefore not applicable.

## Findings

### HIGH — Credential exclusion is claimed but not enforced

The accepted architecture prohibits credentials in durable tokens (`docs/architecture/colored-petri-net-workflows.md:171-173`). Public documentation repeats that categorical guarantee at:

- `docs/api/provenance.md:92-97`
- `docs/concepts/provenance-and-artifacts.md:49-53`
- `docs/user-guide/external-tool-lifecycle.md:55-58`

However, durable records accept unrestricted nonempty text:

- manifest arguments: `python/src/ksdft2effmass/provenance/records.py:395-400`
- environment values: `records.py:335-341`
- verification detail: `python/src/ksdft2effmass/provenance/tools.py:228-236`
- failure message: `tools.py:367-375`

For example, an argument vector can contain `("--password", "secret")`. Rejecting credential-like environment *names* does not prevent credentials in values or other text.

Evidence also overstates this boundary: `test__ExternalExecutionRequest.py:102-145` checks only field names, while `test__EnvironmentObservation.py:60-61` explicitly excludes value classification.

This requires a public-contract decision on the enforceable sanitized-text/admission boundary before correction.

### HIGH — Runtime, schema, tests, and RFC 3339 claims are inconsistent

1. `RunManifest` accepts impossible dates such as `2026-02-31T12:00:00Z`. Its regex validates only numeric ranges at `records.py:29-32`, although errors claim RFC 3339 at `records.py:413-424`.
2. The maintained test explicitly excludes calendar validity at `test__RunManifest.py:117-134`, while API documentation calls the values UTC timestamps at `docs/api/provenance.md:17`.
3. The schema accepts runtime-invalid states:
   - credential-like environment names: schema `:370-397`, runtime rejection `records.py:335-341`;
   - non-NFC common text: schema examples `:476-479`, `:684-687`, and `:1003-1006`, versus runtime NFC enforcement `records.py:42-52`;
   - inconsistent `ExecutionCorrelationResult` status/issues: schema `:398-443`, runtime `actions.py:173-197`;
   - inconsistent artifact-verification status and represented equality: schema `:37-87`, runtime `actions.py:80-92`.

This conflicts with the synchronization requirement in `docs/development/source-documentation.rst:104-117` and the claimed strict schema/runtime contract.

### MEDIUM — Private validators cross module ownership boundaries

`records.py:42-108` defines module-private generic field validators. They are imported across modules by:

- `tools.py:13-19`
- `actions.py:8`

The architecture permits module-private helpers **within** their owning module and requires intrinsic validation to remain owner-local (`.pi/skills/design-data-action-objects/references/data-action-architecture.md:65-77`). The corrective policy explicitly prohibits module-level field validators and prefers limited owner-local duplication (`.../data-action-architecture.md:81-93`).

### MEDIUM — Maintained documentation contradicts active P2 state and MyST inventory

Current maintained pages still say no successor launched and P2 remains blocked:

- `docs/user-guide/installation.md:13`
- `docs/user-guide/external-dependencies.md:182`
- `docs/api/workflows-cpn.md:123-129`
- `docs/concepts/cpn-contract.md:126-135`
- `docs/verification/cpn-contract.rst:174-182`
- `docs/user-guide/colored-petri-nets.md:35-40`
- `docs/user-guide/dft-backends.md:38-43`

The MyST catalog also says 13 user-guide pages at:

- `docs/user-guide/installation.md:19`
- `docs/user-guide/external-dependencies.md:177`

The explicit toctree now contains 14 pages (`docs/index.rst:79-92`). Because these stale files are outside the documentation writer’s current owned paths (`task-ownership.json:33-42`), correction ownership must be expanded before edits.

### MEDIUM — Public source documentation and enum policy are incomplete

String-valued public enums use `Enum`, for example:

- `tools.py:22-61`
- `actions.py:19-37`
- `records.py:111-143`

Repository policy requires `enum.StrEnum` for string-valued public enums (`docs/development/source-documentation.rst:124-132`). Several enum and error docstrings also provide only a one-line summary without documenting members or full behavior, contrary to the public-object requirement at `source-documentation.rst:23-32`.

## Evidence inventory

- **`records.py`**: reference/location separation, frozen ownership, u64, digest, lexical path, deterministic tuples, lineage and lifecycle separation otherwise conform; timestamp and credential findings remain.
- **`tools.py`**: installation versus verification, request/result/failure forms, authorization ID, immutable outcomes, retries-as-new-requests, and scientific-acceptance exclusions are represented; credential admission remains unresolved.
- **`actions.py`**: exact artifact verification and deterministic request/outcome correlation are correctly separated from I/O and scientific interpretation.
- **`serialization.py` / schema / fixtures**: duplicate keys, BOM, unknown keys, floats/non-finite values, surrogates, booleans/numeric-string u64, canonical LF JSON, paths, and fixture round trips pass; schema/runtime relational gaps remain.
- **Public API and wheel**: exact module inventory, exports, clean wheel import, and specification packaging pass.
- **Tests**: 75 unique `SV-PROV-001`–`SV-PROV-075` identifiers; exact headings/fields, ownership, semantic names, software-verification classification, and VVUQ exclusions pass structurally. The credential and timestamp gaps prevent semantic evidence completeness.
- **Dependency direction**: static imports are acyclic and isolated from DFT/QE/SNAKES/harness/runtime clients. Documentation correctly distinguishes static acyclicity from stateful CPN semantics.
- **CPN boundaries**: pure guards, two-phase execution, retained failures/retries, common-parent joins, and accepted-marking distinctions remain documented without claiming a scientific DAG.

## Commands run

- Ownership validator: **PASS**
- P2 completion validator: **PASS**
- Focused P2 pytest: **75 passed**
- Affected Ruff check and format check: **PASS**, 36 files formatted
- Affected mypy: **PASS**, no issues in 36 files
- Sphinx 9.1.0/MyST 5.1.0 with `-W --keep-going`: **PASS**, 45 sources
- Local-route validation: **PASS**
- Checkpoint dry-run validation: **PASS**, zero unresolved
- `git diff --check`: **PASS**
- Evidence-ID/grammar audit: 75 identifiers, all unique and contiguous
- Targeted runtime/schema probes reproduced the impossible-date and schema/runtime inconsistencies.

The supplied full-suite and full-mypy baseline results were not rerun.

## Replay and residual risk

P2-R1/E1 reports PASS and its recorded input-set hash still matches with zero catalog mismatches. The later provenance test-package marker is not included in the R1 inventory. After correction, the single permitted replacement replay should bind that marker and all corrected artifacts.

**Required next step:** one consolidated correction cycle, followed by the permitted replacement replay and final verification. Credential/sanitization semantics and any resulting public API or serialization change remain human-owned.