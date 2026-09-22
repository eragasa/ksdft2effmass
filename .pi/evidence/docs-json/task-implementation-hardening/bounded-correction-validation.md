# Stage-2A bounded-correction validation

Status: PASS for the requested software-verification boundary, pending explicit human acceptance at the renewed checkpoint.

Claim boundary: These results establish only the declared software contracts and exact repository-state checks. They do not establish migration semantics, scientific validity, human authority, or human acceptance.

## Starting state and authority

- Fetched `origin/dev`; local `dev`, `origin/dev`, and `FETCH_HEAD` were exactly `a577ebb1865fde2af7560be3c087018f32c1afd7` with ahead/behind `0/0`.
- The starting working tree was clean.
- Stage 2A was awaiting human implementation acceptance at the prior pending checkpoint.
- The current human instruction selected its bounded-correction option and authorized only this correction.
- Stage 2B remained `blocked_on_task_implementation_hardening`; no real Task migration, candidate for a selected Task, migration packet, or Stage-2B activation occurred.

## Root cause of the prior broad-test result

The tracked source at `a577ebb` used two unparenthesized multi-exception clauses. The prior broad test did not fail because the project interpreter was Python 3.14.6, where PEP 758 makes `except UnicodeDecodeError, SyntaxError:` valid grammar. Ruff configured for Python 3.14 also accepted and reformatted toward that spelling.

The requested alternatives were checked explicitly:

- **Dirty working tree:** the old validation record did not retain enough immutable evidence to prove that its test run used a clean tree, so its wording was not a reproducible committed-tree claim. No evidence of a dirty corrected copy explains the pass; the matching Python 3.14 bytecode header records the tracked source size and timestamp.
- **Stale or installed package:** not the cause. The project virtual environment resolves `ksdft2effmass` to this repository's `python/src/ksdft2effmass/__init__.py`.
- **Different revision:** not the cause. The same spelling existed before `a577ebb` in the tracked evidence module.
- **Another import boundary:** not the cause. Maintained tests import `ksdft2effmass.harness.pi.evidence.identifiers` directly.

The exact root cause was therefore interpreter grammar, compounded by an evidence gap: the previous record did not prove a clean committed checkout and imported package path. Both exception clauses now use explicit tuples. `# fmt: skip` retains the requested tuple spelling because Ruff targeting Python 3.14 would otherwise remove the parentheses.

## Packet-binding correction

`HarnessTaskMigrationReviewPacketPreparer` still recomputes canonical Task JSON, rendering, comparison, complete source coverage, exact mapping spans, and opaque blocks. It now additionally constructs the one exact immutable `HumanReviewObservation` tuple that the generic packet must contain and requires exact generic findings and limitations agreement.

The observations deterministically bind:

1. source SHA-256 identity and byte count;
2. candidate Task ID, canonical-JSON SHA-256 identity, and byte count;
3. every source mapping field and the complete unmapped-span account;
4. rendered-document SHA-256 identity and byte count;
5. comparison source/rendered identities, status, differences, and unmapped spans;
6. each documentation-owned mapping and exact block identity with preservation status; and
7. all applicable comparison limitations.

Observation detail is canonical JSON text created from these exact runtime values. Preparation requires the exact source/rendered target path tuple and source revision. Empty, incomplete, altered, stale, or candidate-unrelated packets fail closed. This adds no serialized field and does not change the accepted 16-field `HarnessTask` wire contract.

`HarnessTaskMigrationFileDispositionRecorder` now invokes the public `HarnessTaskMigrationReviewPacketPreparer` on the packet's retained request and requires equality with the prepared result before checking decision binding or disposition compatibility. A directly constructed but inconsistent packet therefore cannot be dispositioned. No token, registry, private constructor, persistence, identity authentication, natural-language interpretation, file mutation, or activation machinery was added.

## Representative example

The example is now explicitly a **manually supplied HarnessTask serialization-and-rendering example**. It does not claim Markdown-to-JSON extraction and adds no parser. It separately demonstrates:

- manually supplied `HarnessTask` to canonical JSON;
- `HarnessTask` plus documentation content plus projection profile to rendered Markdown; and
- source Markdown plus rendered Markdown plus accepted mappings to exact byte-structural comparison.

The source remains `40ada86450912593bb5554de6b6536011eadce13eaa103ecfe4754846d088fd9`. The corrected candidate JSON is `4f660787561789952d49df747e0fcdbe0fe1a9faf7e0aa9b51e566e5cfdc3bfc`; rendered Markdown is `a404ce5c5c0d75df3dedc600193461137f00fce7c867e246567fa96f5eaf872a`; and the exact difference is `insert:source[0:0]->rendered[0:183]`. The opaque source paragraph is unchanged.

## Changed paths

- `.pi/chains/harness-simplification.chain.json`
- `.pi/checkpoints/harness.simplification.docs-json.task-implementation-hardening.implementation-acceptance.json`
- `.pi/checkpoints/harness.simplification.docs-json.task-implementation-hardening.corrected-implementation-acceptance.json`
- `.pi/evidence/docs-json/task-implementation-hardening/bounded-correction-validation.md`
- `.pi/evidence/docs-json/task-implementation-hardening/hardening-decisions.md`
- `.pi/evidence/docs-json/task-implementation-hardening/implementation-acceptance-packet.md`
- `.pi/evidence/docs-json/task-implementation-hardening/representative-example/manifest.json`
- `.pi/evidence/docs-json/task-implementation-hardening/representative-example/rendered.md`
- `.pi/evidence/docs-json/task-implementation-hardening/representative-example/source-to-rendered.diff`
- `.pi/evidence/docs-json/task-implementation-hardening/representative-example/task.json`
- `.pi/evidence/python-conformance/module-inventory.json`
- `harness/tasks/harness.simplification.docs-json.task-implementation-hardening.json`
- `docs/api/harness-task.rst`
- `docs/harness/ksdft2effmass.harness.002.001.012.md`
- `python/src/ksdft2effmass/harness/pi/evidence/identifiers.py`
- `python/src/ksdft2effmass/harness/pi/local/task_model.py`
- `python/tests/software_verification/ksdft2effmass/harness/pi/local/task_model_examples.py`
- `python/tests/software_verification/ksdft2effmass/harness/pi/local/test__HarnessTaskMigrationFileDispositionRecorder.py`
- `python/tests/software_verification/ksdft2effmass/harness/pi/local/test__HarnessTaskMigrationReviewPacketPreparer.py`

No dependency, lockfile, schema, fixture, profile, public export, or six selected Markdown Task changed.

## Deterministic results

- `py_compile` over every Python file under `python/src/ksdft2effmass/harness/pi`: PASS.
- Focused Stage-2A ownership set: PASS, 87 tests.
- Packet preparer, disposition recorder, and cross-surface contract subset: PASS, 43 tests.
- Direct TaskStateInspector and TaskRecordAdapter compatibility: PASS, 12 tests; the Stage-2A cross-surface set also retains Markdown/v1/v2 compatibility coverage.
- Focused mypy over changed production and evidence helpers/modules: PASS, zero issues.
- Maintained Stage-2A Python conformance: PASS, 23 modules, 63 evidence owners, zero findings.
- Repository maintained-evidence conformance: PASS, 241 modules, 2,937 collected nodes, zero findings.
- Local harness resource/profile validation: PASS, zero issues.
- Ruff format and lint over affected Python: PASS.
- Sphinx HTML build with warnings as errors: PASS.
- `git diff --check`: PASS.
- Checkpoint validation: PASS.
- Six authoritative Markdown Task identities: PASS, byte-identical to the accepted inventory and 20,074 bytes total.
- Stage 2B inactivity: PASS.

## Clean committed-tree proof

The resulting correction commit was checked from a separate detached Git worktree with no tracked or untracked changes. The validation ran from that worktree's `python/` directory with `PYTHONPATH=<isolated-worktree>/python/src` and printed both:

- `ksdft2effmass.__file__ = <isolated-worktree>/python/src/ksdft2effmass/__init__.py`; and
- `ksdft2effmass.harness.pi.evidence.identifiers.__file__ = <isolated-worktree>/python/src/ksdft2effmass/harness/pi/evidence/identifiers.py`.

That isolated committed tree passed package `py_compile`, focused Stage-2A tests, packet-binding negative evidence, adapter/TaskStateInspector compatibility, maintained evidence validation, Ruff format/lint, focused mypy, resource/profile validation, Sphinx warnings-as-errors, whitespace checks, six-source identity checks, and Stage-2B inactivity checks. No pass is attributed to another installation or a dirty checkout.

## Review and residual limits

The original independent review remains unchanged: two high, one medium, and one low finding were accepted and dispositioned in its one correction pass. The present correction used no intercom, other session, repeated reviewer, or replay loop, so there is no new independent-review result to imply acceptance.

The tuple syntax correction is a clarity and reproducibility correction under the Python 3.14 project policy; it does not add older-Python support. Packet observations prove exact runtime binding only and do not prove the semantic correctness of a future candidate or human acceptance. The renewed checkpoint remains pending, all six Markdown Tasks remain authoritative, and Stage 2B remains inactive.
