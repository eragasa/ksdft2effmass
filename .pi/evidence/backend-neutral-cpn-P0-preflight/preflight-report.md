# P0 SNAKES/MyST packaging and capability preflight

## Status

**Recommendation: `CONDITIONAL_PASS`.** The accepted CPN and Markdown
architecture is technically feasible in the tested repository-supported
environment. Required CPN construction, colored-token, multiset, guard,
binding, arc-expression, firing, retry/history, provenance-join, marking
inspection, and bounded reachability behaviors executed successfully. A
representative MyST/Sphinx build also passed with warnings treated as errors.

The conditions are bounded but require human decisions:

1. SNAKES 0.9.33 has no declared Python requirement or version-specific Python
   classifiers even though installation, import, and required behavior passed on
   CPython 3.14.6. Adopt only a bounded tested version line with CI probes.
2. SNAKES license metadata is incomplete and internally nonspecific: core
   metadata has no SPDX expression, installed license files contain LGPL v3
   text, while the upstream README grants LGPL 2.1-or-later. This report records
   facts and makes no legal conclusion. Redistribution treatment requires human
   acceptance and, if necessary, legal review.
3. The SNAKES `gv` plugin loads, composes DOT, and is optional, but Python 3.14
   reports deprecated `codecs.open`; warnings-as-errors therefore requires an
   upstream or bounded compatibility correction before rendering is required.
   The system `dot` executable was unavailable, so actual rendering was not
   tested.
4. MyST is viable with `dollarmath`, but enabling it currently collects Markdown
   throughout `docs/`; the broad disposable build does not pass warnings as
   errors. A separate task must choose an explicit maintained-source collection
   or correction policy, repair three user-guide directory links and all sources
   in that chosen collection, pass a maintained `-W` build, and replace rather
   than duplicate the current RST download navigation.
5. Maintained dependency declarations and Sphinx configuration remain unchanged
   until the human checkpoint is resolved and a separate packaging/configuration
   task is authorized.

This is software/tooling capability evidence, not numerical verification,
scientific validation, uncertainty quantification, or proof of the future
project CPN contract.

## Preconditions and scope containment

At launch, `CPN-HC01` and the CPN skill-capability audit were human-accepted,
all persisted checkpoints were resolved, no prior task was active, and the
existing P0 record was the authoritative owner. P0 was set as the only active
task. P1--P11 remain blocked and unauthorized.

No production source or maintained production test changed. No dependency or
lockfile changed. No QE, ABINIT, Wannier90, scheduler, MPI, cloud, cluster, or
scientific executable ran. No project CPN runtime or persistence implementation
was created. `cpnpy` and SimPN were neither installed nor adopted. The separate
22-test evidence-ID debt remains inactive.

## Isolated environment

Only one repository-supported Python version was available:

| Item | Tested value |
|---|---|
| OS | macOS 26.5.1 |
| Architecture | arm64 |
| Python | CPython 3.14.6 |
| Interpreter used to create venv | `/opt/homebrew/bin/python3.14` |
| Repository constraint | `>=3.14` |
| pip | 26.2, upgraded only inside the disposable venv |
| Package source | PyPI simple index |
| Sphinx | 9.1.0 |

CPython 3.12 was installed on the host but is below the repository requirement
and was not presented as a supported test. No Python 3.15 interpreter was
available. Therefore the oldest and newest supported interpreters actually
available were the same CPython 3.14.6 interpreter; no other version is claimed
tested.

The environment was created under a safely checked `mktemp` path outside the
repository. Package caches were disabled. The venv, pip report, build trees,
HTML, doctrees, and attempted Graphviz outputs are disposable and are not
retained in the repository.

## Package identity and dependency footprint

### SNAKES

- canonical distribution: `SNAKES`;
- import: `snakes`;
- tested version: 0.9.33, released 2024-06-03;
- source: PyPI sdist, SHA-256
  `af8c3046bfedf3e088b6bf37d451ad6aeeb79716f68a6253e44ddbd1c7e250f3`;
- local wheel build: succeeded but the transient wheel was not retained and its
  nondeterministic build digest is not an adoption identity;
- declared direct/optional dependencies: none;
- declared Python requirement: absent;
- upstream project: <https://codeberg.org/fpom/snakes> (legacy GitHub repository
  now says it moved to Codeberg);
- documentation: <https://snakes.ibisc.univ-evry.fr/>;
- maintenance snapshot: release/current tree last updated 2024-06-03; no future
  maintenance guarantee is inferred.

The upstream tutorial generically claims Python 2.5 and later, including Python
3, but this does not establish 3.14 support. Package metadata also does not
establish it. The distinct evidence is: sdist installation succeeded, import
succeeded with warnings promoted to errors, and the required synthetic behavior
executed on CPython 3.14.6.

### MyST Parser

- canonical distribution: `myst-parser`;
- import/Sphinx extension: `myst_parser`;
- tested version: 5.1.0, wheel released 2026-05-13;
- wheel SHA-256:
  `9c91c52b3cdb4d94a6506e4fab4e2f296c7623a0da0dcbe6de1565c3dad67a8a`;
- Python requirement: `>=3.11`, with an explicit Python 3.14 classifier;
- direct dependencies: `docutils>=0.20,<0.23`, Jinja2,
  `markdown-it-py~=4.2`, `mdit-py-plugins>=0.6.1,~=0.6`, PyYAML, and
  `sphinx>=8,<10`;
- optional groups: code-style, linkify, RTD, testing, and testing-docutils;
- project: <https://github.com/executablebooks/MyST-Parser>;
- documentation: <https://myst-parser.readthedocs.io/>;
- PyPI development classifier: Beta.

The resolved environment contained 29 distributions including pip. The exact
inventory is in `package-metadata.json`.

## License facts and bounded recommendation

MyST 5.1.0 ships the MIT license. SNAKES core metadata exposes only a generic
LGPL classifier and no license expression. Its installed 0.9.33 distribution
contains LGPL v3 text in `LICENCE.md` and `COPYING`; the upstream README says
LGPL 2.1-or-later. This difference may be consistent with the “or later” grant,
but P0 does not make that legal determination.

For an Apache-2.0 project, the bounded technical/distribution recommendation is
to keep SNAKES as a separately installed optional dependency, do not copy,
modify, vendor, statically combine, or bundle SNAKES into project artifacts,
preserve required notices and license texts when redistribution occurs, and
ensure users can replace the compatible library version. Apache project code
would remain separately licensed. Whether a particular wheel, application
bundle, container, or other combined distribution satisfies all LGPL
obligations is a protected legal/redistribution question and remains at the
human checkpoint.

## SNAKES API and colored-token behavior

The retained script used the installed public API:

```python
from snakes.data import Substitution
from snakes.nets import (
    Expression, Marking, PetriNet, Place, StateGraph,
    Transition, Variable, tAll,
)
from snakes.typing import Instance
```

It exercised `PetriNet`, `add_place`, `add_transition`, `add_input`,
`add_output`, `transition`, `Transition.modes`, `Transition.enabled`,
`Transition.fire`, `get_marking`, `set_marking`, place-token inspection, and
`StateGraph.build`, iteration, markings, successors, and completion.

Synthetic immutable frozen dataclass payloads represented tool capability,
execution request/result, failure, retry authorization, and provenance identity.
Strings, integers, tuples, and frozen dataclasses were accepted in an
unrestricted heterogeneous place. Equal frozen values had value equality and
equal multiset lookup. Two equal failure tokens retained multiplicity two; nine
distinct values coexisted in one place. A list token failed with `TypeError`
because multiset keys must be hashable. Separately, a place constrained with
`Instance(SyntheticToken)` accepted the intended frozen payload and rejected a
hashable string with `ValueError: forbidden token`, demonstrating actual color
checking rather than only structured-value carriage.

### Guards, bindings, firing, and errors

A three-input authorization transition bound request, capability, and
authorization tokens; a pure Boolean guard compared immutable capability IDs;
an output expression constructed a distinct immutable result. One enabled mode
was enumerated and fired. A separate two-token transition produced two enabled
bindings on repeated inspection; sorting their immutable value representations
produced the same canonical sequence. SNAKES' own mode order is not adopted as a
durable contract, so future deterministic selection remains project-owned. Guard mismatch and missing input both produced an
empty mode list. A supplied invalid substitution returned `False` from
`enabled()` and `fire()` raised `ValueError: transition not enabled for ...`.
No guard performed I/O, dynamic backend import, process invocation, scheduler
contact, mutation, or another side effect.

SNAKES expressions are arbitrary Python evaluations, so purity is policy, not an
engine security property. Upstream documentation also warns that expressions
may be evaluated repeatedly and side effects produce incorrect behavior. P1/P3
must preserve the accepted pure-guard and external two-phase execution boundary.

### Failure, retry, and history

The synthetic retry transition required matching parent identity and the next
attempt number. It consumed a failure and authorization, explicitly re-emitted
the unchanged failure into a history place, and created a new request with
attempt identity `run-1:attempt-2`. The prior failed attempt remained
inspectable and retry was disabled without authorization. History is therefore
representable but is not automatic persistence.

### Provenance-compatible join

Matching parent, manifest, and protocol-version identifiers enabled one join
mode. Independently mismatched parent, manifest, and protocol identifiers each
produced zero modes. Two branch completion values alone were insufficient. This
establishes runtime feasibility only; future scientific representation
compatibility remains project-owned.

## Marking inspection and persistence feasibility

SNAKES markings expose per-place multisets and explicit multiplicities. The
preflight extracted a neutral disposable record with place identifier, token
type identifier, token payload, and multiplicity. Project-owned persistence is
feasible with these conditions:

- do not treat engine iteration order as durable;
- canonical-sort records;
- use explicit versioned type registries and project-owned encoders/decoders;
- do not reconstruct from Python qualified names alone;
- add schema/model version, correlation, provenance, lineage, and retry/history
  outside SNAKES;
- reject unsupported arbitrary objects;
- never use pickle for live nets or arbitrary Python values.

Successful in-memory token use is not serialization evidence. No project
persistence format was implemented.

## Reachability and plugin inventory

`snakes.nets.StateGraph` is core, not plugin-provided. It completely enumerated
a bounded four-marking counter net and identified the final marking as having no
successors. There is no demonstrated dedicated dead-transition detector; after
complete bounded exploration, unused edge transition labels can be inspected to
infer dead transitions. `StateGraph` does not detect unboundedness and may
explore forever, so only explicitly bounded/restricted use is recommended. P0
does not claim model checking or scientific workflow verification.

Installed plugins were `bound`, `clusters`, `gv`, `hello`, `labels`, `let`,
`modules`, `ops`, `pids`, `pos`, `query`, `status`, and `synchro`. No plugin is
required by the accepted architecture beyond optional `gv`; core
`StateGraph` covers the preflight reachability case. The documented load call
was verified:

```python
snakes.plugins.load("gv", "snakes.nets")
```

The plugin builds a generated extended module/subclass composition and
automatically loads `clusters` and `pos`. Plugin order, generated names, and
class composition must remain isolated in a future adapter to avoid import/name
conflicts. No unrelated plugin was enabled.

## Graphviz

The `gv` plugin imported and produced DOT text without system Graphviz. It
invokes `dot` directly and does not require a separate Python `graphviz`
distribution. System `dot` was absent; discovery/version and SVG rendering were
therefore `NOT_AVAILABLE`. Normal rendering raised `FileNotFoundError`. On
Python 3.14, `gv` also emits `DeprecationWarning` for `codecs.open`, which fails
under warnings-as-errors before process discovery.

Graphviz remains optional. Plugin rendering is `CONDITIONAL_PASS` pending a
bounded compatibility correction and a separate environment with `dot`. DOT,
SVG, PNG, and other diagrams are derived views and cannot be authoritative
workflow state.

## MyST/Sphinx and Obsidian-compatible source

`myst_parser` imported on Python 3.14.6. A disposable mixed project built with
Sphinx 9.1.0, MyST 5.1.0, `-W --keep-going`, and:

```python
extensions = ["myst_parser"]
myst_enable_extensions = ["dollarmath"]
myst_heading_anchors = 3
```

The build verified headings, fenced Python, `$...$`, `$$...$$`, relative links,
a MyST `{toctree}` fence, Markdown-to-Markdown references, an RST index linking
to Markdown, Unicode scientific symbols, a table, nested fences, and raw inline
HTML. Generated HTML assertions passed and no warning was emitted. The source
remains portable for Obsidian-style authoring, but Obsidian itself was not run.
The minimal build does not prove every repository Markdown page compatible.
Adding `myst_parser` to the current `docs/conf.py` would register Markdown
throughout `docs/`, not only pages placed in a toctree; the retained broad build
therefore fails. The later configuration task must define the intended collected
source set (or correct all collected Markdown) and produce a maintained
warnings-as-errors pass before enabling MyST.

### Maintained user-guide audit

The 13 Markdown user-guide pages contain two `$$` delimiters, two lines with
inline dollar mathematics, five fenced blocks (ten opening/closing fence lines),
one Python and four text fences, 12 table rows, and no Mermaid, nested/long
fence, or raw-HTML match. All 33 local links exist on disk.

Three index links target directories (`../architecture/`, `../computational/`,
`../research/`). A broad disposable MyST collection reports them as missing
cross-reference targets. They need bounded changes to concrete index documents
before warnings-as-errors direct rendering. The broad collection also exposed
Mermaid lexer and existing cross-reference warnings outside the requested
user-guide scope. P0 does not silently suppress them or claim a maintained MyST
pass; collection/exclusion policy and any broader corrections belong to the
human-authorized packaging/configuration task.

The current RST index has 17 download-only links for user-guide/architecture
Markdown. After MyST is enabled, direct toctree navigation should replace those
entries where appropriate to prevent duplicates. Deliberate source-download
links may remain separately if desired. Enabling MyST changes these files from
download-only assets to collected documents; it does not require duplicate RST
copies.

## Dependency placement analysis

| Candidate | Assessment |
|---|---|
| SNAKES as core runtime | Not recommended: operator-record and other non-workflow users do not need the engine; it broadens the LGPL and source-build footprint. |
| SNAKES as optional workflow extra | **Recommended:** future workflow CLI/runtime users opt in; neutral APIs remain SNAKES-free; license and build boundaries remain visible. |
| SNAKES as development-only | Not sufficient for a future production CPN runtime, though development/CI may install the workflow extra. |
| MyST as general development dependency | Viable but broader than necessary for contributors who do not build docs. |
| MyST as optional documentation extra | **Recommended:** extend the existing `docs` extra; wheel/runtime users do not receive documentation tooling. |

Recommended declaration ranges for a separately approved task are
`SNAKES>=0.9.33,<0.10` in a `workflow` extra and
`myst-parser>=5.1,<6` in the existing `docs` extra, with the lockfile retaining
the exact tested artifacts. Because only 0.9.33/5.1.0 were tested, upgrades
within those ranges still require CI capability/build probes. MyST constrains
Sphinx to `>=8,<10`; the documentation declaration should state that compatible
range explicitly rather than relying on transitive resolution. Optional system
Graphviz should remain outside wheel metadata and be documented/probed only
where rendering is requested.

The workflow extra should not cause neutral operator or scientific DataObjects
to import or expose SNAKES. A future production CLI that executes CPNs can
require the extra and fail with a project-owned actionable missing-capability
result. Reproducibility requires source hashes/lock entries and Python 3.14 CI.
No dependency declaration or lockfile was changed by P0.

## Repository tooling and packaging compatibility

Disposable tooling checks used pytest 9.1.1, mypy 2.3.0, Ruff 0.16.1, and
`build` 1.5.0. A disposable pytest SNAKES construction/mode/firing test passed.
The retained evidence scripts pass the repository Ruff format/lint policy.
SNAKES 0.9.33 has no `py.typed` marker or stubs; a disposable typed adapter
smoke passed only by explicitly suppressing `import-untyped` and isolating the
engine as `Any`. Static typing is therefore `CONDITIONAL_PASS`: a future adapter
must own this narrow untyped boundary and must not leak SNAKES types into neutral
APIs.

The repository Python project built a wheel in the disposable directory,
installed without dependencies into a second clean temporary venv, imported,
and exposed the expected metadata. Mandatory requirements remained NumPy/SciPy;
SNAKES and MyST were absent. The generated wheel and environments were removed.
The compact command/result evidence is `tooling-smoke.json`.

## Capability matrix summary

Of 24 required capability records:

- 16 are `PASS`;
- 7 are `CONDITIONAL_PASS`, including protected placement/license decisions;
- 1 is `NOT_AVAILABLE` (optional system Graphviz);
- none is `FAIL`.

The authoritative per-capability statuses, evidence paths, exact environment,
limitations, corrections, and blocking/optional classification are in
`capability-matrix.json`. The matrix validator also rejects missing status,
invalid status, absent artifact, duplicate capability, and mismatched
environment probes.

## Independent read-only reviews

Seven required lanes and focused correction re-reviews were completed:

1. SNAKES API/Python evidence: passed after one low wording correction that now
   distinguishes runtime Python-version compatibility from absent declarations.
2. Colored-token/guard/marking/retry/join semantics: initial findings required a
   constrained color checker and repeated canonical two-mode inspection; the
   corrected evidence passed focused re-review.
3. Persistence/reachability claims: passed, with bounded-exploration and
   project-owned registry/encoder residual risks retained.
4. SNAKES/Graphviz packaging and license facts: replacement review returned
   `CONDITIONAL_PASS` with no blocker; LGPL/redistribution remains correctly
   human-gated and no legal conclusion is made.
5. MyST/Sphinx/Obsidian compatibility: initial findings corrected raw-HTML
   scanning, rendered assertions, and maintained-collection claims. Focused
   follow-up verified the exact nested-fence assertion; its only finding was the
   expected stale checksum after an evidence edit, corrected by regenerating and
   validating the final checksum manifest.
6. Dependency placement: passed; exact pin versus bounded range remains an
   explicit human tradeoff, with bounded ranges plus exact lock artifacts
   recommended.
7. Final control-plane/scope integration: initial findings required chain/state,
   checkpoint, tooling, wheel, and Sphinx-claim corrections; corrected
   integration re-review passed.

Reviews are advisory findings. Deterministic commands own software gates, parent
verification owns evidence completeness, and only the human can accept P0 or
authorize maintained packaging/configuration.

## Post-preflight human decision

No material CPN semantic requirement failed, so engine reconsideration is not
recommended. On 2026-08-03 the human PI selected Option A at `P0-HC01`, accepted
P0 as `CONDITIONAL_PASS`, and closed it. The human authorized only bounded P0A
packaging/configuration. Existing P1 is the project-owned CPN contract rather
than the packaging successor and remains blocked with P2--P11.

For project governance the human records the explicit upstream SNAKES grant as
`LGPL-2.1-or-later` while retaining the observed fact that the distributed
license file contains LGPLv3 text. This is not a general legal conclusion. P0A
must add an accurate third-party notice and must not vendor, copy, modify,
redistribute, or bundle SNAKES. Any such future distribution action requires a
new human license checkpoint. Runtime, persistence, untrusted-expression,
bounded-`StateGraph`, optional-Graphviz, explicit-MyST-collection, and maintained
warnings-as-errors boundaries remain in force.
