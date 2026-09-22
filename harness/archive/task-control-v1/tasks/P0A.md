# P0A — SNAKES/MyST packaging and documentation configuration

Status: closed; human-accepted `PASS` through resolved `P0A-HC01` on 2026-08-03

## Authority

The human PI accepted P0 as `CONDITIONAL_PASS` and authorized this separate,
bounded packaging/configuration successor. Existing P1 is the project-owned CPN
contract, not this packaging task, and remains blocked with P2--P11. P0A must
stop for its own human acceptance and must not launch P1 or another task.

The durable decision and preserved human response are in
`.pi/checkpoints/P0-HC01-packaging-license-and-configuration.json`.

## Objective

Adopt only the accepted dependency declarations and documentation configuration,
retain exact lock artifacts and hashes, add an accurate third-party notice, and
verify installation and maintained documentation behavior without implementing
the production CPN runtime.

## Authorized changes

- add `SNAKES>=0.9.33,<0.10` only to an optional `workflow` extra;
- keep SNAKES outside core and development-only dependency sets;
- add `myst-parser>=5.1,<6` to the documentation extra;
- constrain the documentation environment to `Sphinx>=8,<10`;
- refresh the established lockfile while preserving exact resolved artifacts and
  hashes;
- keep system Graphviz optional and outside Python wheel metadata;
- add a third-party dependency notice identifying SNAKES, its copyright holder,
  upstream location, version range, and upstream `LGPL-2.1-or-later`
  declaration;
- retain the observed fact that the distributed SNAKES license file contains
  LGPLv3 text;
- define explicit MyST source collection and navigation behavior without
  indiscriminately collecting every Markdown file under `docs/`;
- correct or explicitly exclude existing directory links and duplicate RST/MyST
  navigation within the selected maintained documentation scope;
- add only focused installation/configuration verification needed for this task.

## License and redistribution boundary

This is a project packaging decision, not a general legal conclusion. P0A may
depend on an independently installed SNAKES package but must not:

- vendor or embed SNAKES source;
- copy SNAKES implementation code into project-owned modules;
- modify or redistribute a SNAKES fork;
- bundle SNAKES into a standalone executable, application bundle, or container
  intended for distribution;
- imply that SNAKES is covered by the project's Apache-2.0 license.

Any future vendoring, modification, fork distribution, or bundled
binary/container distribution requires a new human license checkpoint.

## Runtime and scientific boundaries

SNAKES remains replaceable behind a project-owned boundary. Project records,
schemas, identifiers, persistence, provenance, retry semantics, and canonical
ordering remain backend-neutral. Pickle is prohibited for authoritative
persistence. Arbitrary Python expressions and untrusted guard text must not be
evaluated. Pure project-owned guards remain policy; SNAKES is not a security
sandbox. `StateGraph` supports only bounded reachability enumeration. Graphviz
output remains optional, derived, and nonauthoritative.

P0A must not implement the production CPN runtime, public CPN contract, marking
persistence, scientific token payloads, backend integration, or another CPN
backend. It must not change scientific operator behavior or launch QE, ABINIT,
Wannier90, scheduler, remote, or other scientific calculations.

## Required evidence and gates

- dependency extras contain exactly the authorized ranges and placement;
- the lock records exact selected artifacts and hashes;
- clean installation/import probes cover the core installation, `workflow`
  extra, and `docs` extra as applicable;
- the third-party notice matches retained upstream package evidence and does not
  imply Apache-2.0 coverage;
- explicit MyST collection/navigation behavior is documented;
- the selected maintained documentation build passes Sphinx with warnings as
  errors;
- affected link and duplicate-navigation checks pass;
- focused formatter, linter, package-build, and import checks pass;
- no production CPN/scientific source or test implementation is introduced;
- independent read-only license/packaging, documentation, and integration
  reviews report no unresolved material finding;
- parent verification confirms scope containment and checkpoint state;
- human final acceptance closes P0A before any later task may launch.

Passing these gates is packaging/configuration software evidence only. It is not
production CPN verification, numerical verification, scientific validation,
uncertainty quantification, or authorization for scientific execution.

## Implementation result

The authorized declarations and configuration are implemented:

- `SNAKES>=0.9.33,<0.10` occurs only in the optional `workflow` extra;
- `myst-parser>=5.1,<6` and `sphinx>=8,<10` occur only in `docs`;
- the uv lock resolves SNAKES 0.9.33, MyST 5.1.0, and Sphinx 9.1.0 with
  registry artifact hashes;
- Graphviz remains absent from wheel metadata;
- `THIRD_PARTY_NOTICES.md` records the binding SNAKES license and distribution
  treatment;
- Sphinx collects all maintained RST and only the 13 Markdown user-guide pages;
- one explicit user-guide toctree replaces duplicate user-guide downloads;
- directory and excluded-Markdown links use concrete repository source targets.

Isolated core, workflow-extra, docs-extra, project-wheel, Sphinx 9.1.0, and
lower-range Sphinx 8.2.3 checks passed. Ruff, mypy, and all 921 repository tests
passed. Detailed reproducible evidence is retained under
`.pi/evidence/backend-neutral-cpn-P0A-packaging-configuration/`.

## Deterministic corrections

- `P0A-001`: `uv tree --extra` is unsupported by uv 0.11.25. Locked whole-tree
  inspection and independent project/wheel metadata assertions replaced it.
- `P0A-002`: the initial evidence Ruff run found two long hash literals and
  stopped before returning to the repository root. The constants were split,
  Ruff passed, and both evidence scripts reran from the correct root.
- `P0A-003`: tooling review found authoritative verifier gates used removable
  Python `assert` statements and the command manifest used undefined shell
  variables/prose placeholders. All gates now raise unconditional failures, an
  optimized-mode malformed-input probe passes, and `run_verification.sh`
  provides one exact self-cleaning replay command.
- `P0A-004`: packaging, documentation, and integration review found stale
  pre-adoption status prose plus an unsynchronized chain dependency flag. The
  computational registry, repository docs index, user-guide status text, and
  chain now distinguish declared optional dependencies from the still-absent
  production CPN runtime.
- `P0A-005`: correction re-review found the replay depended on an ignored local
  `.venv`, could mutate `python/.venv`, and left setuptools `python/build/`
  output. The generated build output was removed. The replay now builds from a
  disposable source copy and directs every uv environment under its trapped
  temporary root; no repository virtual environment or build tree is used.
- `P0A-006`: documentation re-review found one remaining prospective P0 engine-
  reconsideration sentence. It now records the completed P0 result and requires
  separate authorization for any future comparison or reopening.
- `P0A-007`: final tooling review found uv's download cache still defaulted
  outside the temporary replay root. The replay now sets `UV_CACHE_DIR` under
  the trapped root. Final documentation review also identified three minor
  completed-P0/current-task phrases; those records now distinguish accepted P0,
  active packaging-only P0A, and future separately authorized work.
- `P0A-008`: the final replay review found unqualified `python3` commands could
  resolve through a repository virtual environment on `PATH`. Replay now creates
  a dedicated Python 3.14 evidence environment under the trapped root and uses
  its absolute interpreter for every evidence and malformed-input command.

These corrections did not change the approved ranges, license treatment,
documentation scope, production code, tests, or scientific meaning.

## Read-only review result

The required packaging/license, documentation, tooling, and integration lanes
passed after deterministic corrections `P0A-003`--`P0A-008`. Review confirmed
optional-extra isolation, exact lock identities, notice accuracy, absence of
bundled SNAKES/Graphviz content, bounded MyST discovery, complete user-guide
navigation, maintained Sphinx 8/9 warnings-as-errors builds, unconditional
evidence gates, clean-checkout replay, synchronized control-plane state, and no
production/scientific implementation. Structured results and residual risks are
retained in `review-results.json`.

Parent verification passed artifact regeneration, dependency/configuration/
notice/link assertions, lock validation, checkpoint and chain assertions,
production-scope and generated-output scans, JSON/shell checks, no-staged-file
verification, and `git diff --check`. The exact full isolated replay passed and
left no repository build/cache/environment output.

## Final human acceptance and closeout

The human PI selected Option A at `P0A-HC01` on 2026-08-03 and accepted P0A as
`PASS` without corrective work. The dependency placement, lockfile,
documentation collection policy, third-party notice, redistribution boundary,
validation evidence, and recorded non-blocking residual limitations are
human-accepted.

P0A is closed. Its checkpoint resolution did not launch P1. The same human
message separately authorized P1 activation only after P0A closeout validation
passed; that activation is recorded independently in the P1 task and chain
records. No production CPN implementation, SNAKES adapter, persistence,
workflow execution, or scientific execution was produced by P0A.
