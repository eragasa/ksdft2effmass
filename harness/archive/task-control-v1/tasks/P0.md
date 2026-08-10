# P0 — SNAKES and documentation-tooling preflight

Status: closed; human-accepted as `CONDITIONAL_PASS` through resolved `P0-HC01` on 2026-08-03

## Launch authority and bounded ownership

The human PI explicitly launched this existing authoritative P0 record on
2026-08-03. Preconditions were verified at launch: the CPN architecture and CPN
skill-capability audit are human-accepted; all persisted checkpoints are
resolved; no prior task is active; and P1--P11 remain blocked and unauthorized.
No duplicate P0 record was created.

The pi parent is the sole writer and control-plane owner. Focused read-only
owners are assigned to the architecture, documentation, integration-review, and
independent reviewer agents. Deterministic package/API probes, capability-matrix
validation, checksums, Ruff, Sphinx, checkpoint validation, and repository-scope
checks remain tool-owned evidence under the accepted skill-capability audit.

## Objective

Verify before dependency adoption that SNAKES is technically, legally, and operationally usable with the repository's supported Python and tooling. Also verify the exact MyST dependency/configuration needed to collect Markdown-first documentation in Sphinx.

## Required evidence

- Python 3.14 installation, import, and basic execution;
- authoritative package identity, source, license metadata, dependency footprint, and packaging compatibility;
- token values, guards, variable binding, input/output inscriptions, multiple tokens and markings, deterministic enabled-transition inspection, and failure behavior;
- state-space/reachability and Graphviz support only if later tasks require them;
- safe separation between project persistence and live SNAKES objects;
- compatibility with Ruff, mypy, pytest, Sphinx, and repository packaging;
- MyST package/license/version/configuration compatibility for mathematics, fenced code, relative links, Obsidian-compatible Markdown, and Sphinx warnings-as-errors;
- comparative cpnpy/SimPN notes only as needed to explain nonselection, without reopening SNAKES absent material failure.

Do not build production workflow modules or add dependencies before the preflight evidence and human acceptance. Escalate only a material technical, legal, Python-version, packaging, or semantics failure. Completion requires evidence, documentation, independent review, parent verification, and human acceptance.

## Active-task boundary

P0 owns disposable SNAKES/MyST/Sphinx/Graphviz capability, package, license,
Python-version, dependency-footprint, documentation-syntax, and placement
preflight only. Retained evidence belongs under
`.pi/evidence/backend-neutral-cpn-P0-preflight/`. Disposable environments and
generated outputs remain outside the repository.

P0 does not implement production CPN or test modules, persistence, scientific
payloads, backend integration, or calculations. It does not install or adopt
`cpnpy` or SimPN. The separate 22-test evidence-ID migration debt remains
inactive. P1--P11 are blocked and unauthorized and may not be launched by P0.

## Preflight result

Overall recommendation: `CONDITIONAL_PASS` on CPython 3.14.6, macOS 26.5.1
arm64. SNAKES 0.9.33 installed from the hashed PyPI sdist, imported, and passed
bounded construction, constrained colored-token, multiset, guard, binding, arc,
firing, retry/history, provenance-join, neutral-extraction, and bounded
reachability probes. MyST 5.1.0 with Sphinx 9.1.0 passed a representative mixed
RST/Markdown warnings-as-errors build. No material CPN requirement failed, so
engine reconsideration is not recommended.

Conditions are recorded in
`.pi/evidence/backend-neutral-cpn-P0-preflight/capability-matrix.json` and the
full `preflight-report.md`: SNAKES lacks declared Python-version metadata and
type information; neutral persistence requires project-owned registries and
canonical encoders; SNAKES Graphviz rendering uses deprecated `codecs.open` and
system `dot` was unavailable; SNAKES LGPL metadata/text requires a protected
redistribution decision; and maintained MyST activation requires an explicit
collection/correction policy plus a successful maintained warnings-as-errors
build.

The recommended future placement is SNAKES in an optional `workflow` extra,
MyST in the existing `docs` extra, and system Graphviz as optional. No maintained
dependency, lockfile, or Sphinx configuration changed in P0.

## Deterministic corrections

- `P0-001`: Graphviz negative rendering initially stopped at Python 3.14's
  `codecs.open` deprecation. The probe now records that warning separately from
  missing `dot`, and plugin rendering is `CONDITIONAL_PASS`.
- `P0-002`: The first representative MyST page used a Mermaid fence and failed
  warnings-as-errors without a lexer. Mermaid was removed from the required
  minimal fixture and retained as an explicit maintained-source audit concern.
- `P0-003`: The Markdown fence scanner allowed language matching across lines.
  The regex was bounded and evidence rerun.
- `P0-004`: Independent review found that unrestricted `tAll` demonstrated only
  structured carriage. A constrained `Instance(SyntheticToken)` positive and
  hashable wrong-color rejection probe was added.
- `P0-005`: Independent review found that one-mode selection did not establish
  deterministic inspectability. A repeated two-mode probe and project-owned
  canonical sorting evidence were added; engine order remains nonauthoritative.
- `P0-006`: Markdown raw-HTML scanning misclassified angle-bracket URL syntax
  after dependency-catalog edits and used an unconditional observation. The
  scanner now recognizes actual element syntax, derives the observation from
  the count, and the audit was rerun.
- `P0-007`: Representative nested-fence/raw-HTML assertions checked only text.
  They now check expected rendered HTML classes/elements.
- `P0-008`: Review identified missing pytest, mypy, and repository-wheel
  evidence. Disposable pytest, an explicitly isolated untyped mypy boundary,
  and clean wheel build/install/import/metadata probes were added.
- `P0-009`: Active-task state was synchronized across the authoritative chain,
  control-plane, computational, research, architecture, and user-guide records.
- `P0-010`: MyST claims were narrowed: the representative build passes, while
  current broad maintained Markdown collection does not. A later task must own
  collection/correction policy and a maintained `-W` pass.
- `P0-011`: Re-review found the nested-fence HTML assertion could match
  surrounding prose. It now requires the rendered Markdown code-block class,
  escaped inner fence, highlighted `print`, and encoded nested string.
- `P0-012`: Re-review found transient locally built wheel digests were not
  independently reproducible after disposable artifacts were removed. Those
  digests were removed as adoption identities; the authoritative PyPI source
  hashes remain retained.

## Read-only review result

The required seven lanes covered SNAKES API/Python evidence; colored-token,
guard, marking, retry, and join semantics; persistence/reachability; packaging,
Graphviz, and license facts; MyST/Sphinx/Obsidian compatibility; dependency
placement; and control-plane/scope integration. Initial semantic, documentation,
tooling, and integration findings produced corrections `P0-004`--`P0-012`.
Focused semantic and integration re-reviews passed. Packaging/license review was
`CONDITIONAL_PASS` with no technical blocker and retained the protected human
decision. Documentation re-review verified the corrected scanner and claim
boundary; focused nested-fence verification was repeated after the final
assertion correction. Reviews remain advisory and do not replace deterministic
gates or human acceptance.

## Final human acceptance and closeout

The human PI selected Option A at `P0-HC01` on 2026-08-03 and accepted P0 as
`CONDITIONAL_PASS`. The accepted result establishes sufficient technical
viability for SNAKES 0.9.33 and MyST Parser 5.1.0 in the tested CPython 3.14.6
environment. It does not establish production CPN behavior, numerical or
scientific validity, uncertainty quantification, or authorization for scientific
execution.

The human decision records upstream SNAKES licensing as
`LGPL-2.1-or-later` for project governance while retaining the observed fact
that the distributed license file contains LGPLv3 text. This is a project
packaging decision, not a general legal conclusion. The decision also preserves
backend-neutral records and persistence, prohibits authoritative pickle and
untrusted expression evaluation, bounds `StateGraph` claims to reachability
enumeration, and keeps Graphviz derived and optional.

P0 is closed. Its objective, retained capability evidence, package metadata,
validation results, limitations, deterministic corrections, and review outcomes
are recorded above and under
`.pi/evidence/backend-neutral-cpn-P0-preflight/`. No maintained dependency,
lockfile, production source, production test, or scientific result was changed
by P0.

The only active successor is the separately bounded P0A packaging/configuration
task in `.pi/tasks/backend-neutral-cpn-P0A-packaging-configuration.md`. Existing
P1 is the project-owned CPN contract rather than the packaging task and remains
blocked with P2--P11. P0A may not launch P1 or perform production/scientific
execution.