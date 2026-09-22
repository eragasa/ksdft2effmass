# Phase 3 public-import boundaries: corrected bounded recommendation

> **Status:** Read-only planning evidence. This document does not classify a route,
> accept a compatibility change, activate a child, edit source/tests/documentation,
> authorize implementation, or establish human acceptance.

## Evidence basis

The synthesis checked the draft and both reviews against the controlling repository
surfaces:

- `AGENTS.md`, `docs/architecture/v2/repository-layout.md`, and
  `docs/development/source-documentation.rst` establish accepted Option B: support is
  route-specific and requires a deliberate package/subpackage export, accepted
  contract evidence, and synchronized public documentation. Importability,
  descriptive naming, deep use, and `__all__` membership are insufficient.
- `tasks/software/python.architecture-refactor.public-import-boundaries.json` remains
  `planning`, has `explicit_activation_required: true`, requires maintained source,
  tests, examples, documentation, deep consumers, compatibility, import, wheel,
  typing, Sphinx, Harness, and projection evidence, and grants no implementation or
  successor authority.
- The accepted Phase 1 inventory contains 985 distinct `export_routes` over 35 package
  initializers. All 985 have
  `support_status = unknown_no_exact_accepted_support_evidence` and
  `compatibility_disposition = unclassified_pending_bounded_option_b_application`.
  Unknown is not unsupported. The Phase 1 report explicitly says both those rows and
  exact non-export rows remain unclassified Phase 3 inputs.
- The 35 current initializers are byte-identical to their accepted Phase 1 identities,
  so the 985 predecessor route keys remain the mandatory predecessor route set. The
  present source tree has 216 Python modules and aggregate SHA-256
  `35a13b6e15ac33dae08a56d0a8f40c739fdf3b8a52e3db7ac35eade2ee7d1819`, rather
  than the accepted snapshot's 211 modules and
  `63a8a74bb641746f54f1b041147fa65b552751760a9db11ab64bebcc7fbc8fe6`.
  The five added modules are Phase 2 Harness/conformance modules; the older
  `harness/cli/main.py` also changed. Consumer and whole-source evidence must
  therefore be refreshed.
- There are ten zero-route surfaces. Three declare literal empty `__all__` values:
  `ksdft2effmass`, `ksdft2effmass.petrinet`, and
  `ksdft2effmass.harness.pi.local.dbcontrol`. Seven are only effectively empty under
  the Phase 1 AST fallback: `calculators`, `calculators.dft`, `campaigns`,
  `integration`, `harness.pi.dbcontrol`, `harness.pi.local.control`, and
  `harness.pi.wire`.
- Current accessible names exceed `__all__`. For example,
  `harness.pi.resources` explicitly binds `_confined_file`, and `harness.pi` binds
  `TypeAlias` and private cycle-resolution modules without exporting them. These are
  accessibility facts, not support conclusions.
- The Phase 1 consumer report covered source/test roots only. Current maintained
  consumers also include examples and repository Harness checks, including private
  analysis/Workflow imports in
  `examples/tutorials/silicon-bands/scripts/compare_retained_observations.py`, QE
  facade imports in `examples/tutorials/silicon-scf/qe/reconstruct_silicon_scf.py`,
  and CLI/local imports in `harness/pi/validation/*.py`.
- Existing files demonstrate shared mutation surfaces. The Workflow control and runs
  public-API tests each assert both a leaf facade and the Workflow root;
  `docs/api/periodic-records.rst` spans geometry, sampling, Kohn--Sham, plane-wave,
  and QEXSD APIs; and `docs/api/harness-control.rst` spans Harness root, generic Pi,
  Python conformance, and local composition.
- Accepted Phase 2 production facts are explicit-input, immutable syntax facts and do
  not emit support findings. Accepted graph capability provides separately identified
  lexical, runtime-unconditional, and facade-excluded views; it enforces an edge only
  against an explicitly supplied accepted contract for that exact view. It is not a
  universal runtime or repository conformance proof.
- `harness.pi.conformance.python` intentionally rebinds five public owners'
  `__module__`. Route work must preserve object identity, global lookup, and applicable
  pickle/wire behavior, not merely the `__module__` string.
- `python/pyproject.toml` packages `ksdft2effmass*`, but no `py.typed` marker or stub
  package exists. Source-tree mypy evidence therefore does not establish downstream
  installed-wheel typing.

The branch is `dev`. The working tree already contains Phase 3 control-record changes
and an unrelated manuscript modification. This review changed neither repository
state nor those files and ran no tests, imports, builds, external calculations,
commits, or pushes.

## Corrected decomposition

The smallest defensible decomposition separates neutral evidence, route decisions,
file mutation ownership, conditional implementation, and aggregate verification.
The proposed task-internal machine outputs below use a closed, versioned canonical
JSON representation. They are regenerated Phase 3 evidence, not a public package wire
format or a backward-compatibility promise. This plan introduces no production
parser/serializer. If a Python reader is later proposed, it requires separate
authority and must convert exact `bytes` through a typed parser into closed immutable
records; no `Any`, `cast(Any, ...)`, generic `object`, erased dictionary boundary, or
caller-origin trust classification is permitted.

Let `R = harness/reports/public-import-boundaries/phase3` denote the proposed output
folder if the plan is later accepted and the applicable child is activated.

### F0 — Current fact foundation

**Exact inputs**

1. The accepted Phase 1 inventory and review, including the exact 985 predecessor
   route keys and their identities.
2. An explicit content-identified manifest of all 216 current production modules and
   all 35 initializers.
3. An explicit content-identified manifest of maintained first-party Python consumers,
   including `python/src`, `python/tests`, `examples`, repository Harness checks, and
   any other tracked first-party Python path found before execution; no ambient-current-
   directory discovery.
4. Content-identified public API/concept/migration documentation and applicable
   accepted Task/decision records.
5. Accepted Phase 2 production-fact and named dependency-view outputs, without
   extending their semantic claims.

**Exact output:** `R/foundation.json`, containing separate typed views for:

- the immutable 985-row predecessor table;
- all 35 package surfaces, literal-`__all__` declaration state, effective star names,
  initializer bindings, and defining origins;
- maintained source/test/example/Harness/documentation consumers;
- deep implementation imports;
- fresh-interpreter runtime package-attribute observations, explicitly labeled as a
  bounded runtime view rather than an exhaustive language guarantee;
- raw authority/documentation citations with `unknown` and `ambiguous` represented as
  data; and
- separately keyed supplemental candidates for non-`__all__` bindings, relevant deep
  routes, and proposed new routes. Supplemental records never alter or replace a
  predecessor key.

**Gate:** exactly 985 unique predecessor keys, all 35 initializers, all ten zero-route
surfaces, exact content identities, no duplicate record key, complete input manifest,
and deterministic serialization. Fail on unreadable input, parse failure, unresolved
mechanical origin, dynamic/unrepresentable `__all__`, or identity mismatch. Do **not**
fail merely because support authority is absent or ambiguous; record that state and
leave adjudication to a disposition child. F0 edits no initializer, consumer, API
page, or disposition.

### D1–D21 — Disposition units

Every disposition unit reads `R/foundation.json` plus the exact accepted contracts and
public documentation cited for its rows. Its sole output is the listed JSON matrix; it
edits no Python or public documentation. Each predecessor route receives two
orthogonal results:

1. **Support:** `supported`, `unsupported`, or `unresolved`, with exact accepted
   authority and synchronized documentation references. Absence of evidence yields
   `unresolved`, never `unsupported`.
2. **Compatibility:** `preserve`, `deprecate`, `alias`, `retire`, or `unresolved`, with
   independent fields for `__all__` membership, explicit package binding, deep-route
   behavior, replacement, warning behavior, identity/`__module__`/global lookup,
   duration or retirement condition, consumer migration, and specified failure.

A proposed new supported route is a supplemental route record; it does not rewrite the
985-row lineage. “Alias” alone is not a support state. Removing a name from `__all__`
does not by itself retire explicit package access or a deep route.

| ID | Exact surfaces | Predecessor rows | Decision prerequisite | Exact output |
|---|---|---:|---|---|
| D1 | `electronic_structure`, `structures`, `periodic` | 28 | F0 | `R/geometry-sampling.json` |
| D2 | `ksdft`, `ksdft.pw` | 10 | D1 | `R/ksdft.json` |
| D3 | `operators` | 26 | F0 | `R/operators.json` |
| D4 | `units` | 21 | F0 | `R/units.json` |
| D5 | `provenance` | 32 | F0 | `R/provenance.json` |
| D6 | `persistence` | 11 | F0 | `R/persistence.json` |
| D7 | `petrinet.colored` | 68 | F0 | `R/petrinet-colored.json` |
| D8 | `workflows.control` | 37 | D6, D7 | `R/workflows-control.json` |
| D9 | `workflows.runs` | 116 | D6, D7 | `R/workflows-runs.json` |
| D10 | `workflows` | 230 | D8, D9 | `R/workflows-root.json` |
| D11 | `analysis` | 19 | D1–D4, D10 as cited by exact routes | `R/analysis.json` |
| D12 | `calculators.dft.pw` | 18 | D1, D2, D4 as cited by exact routes | `R/calculator-pw.json` |
| D13 | `integration.quantum_espresso`, `.qexsd` | 138 | D1, D2, D4, D10, D12 | `R/quantum-espresso.json` |
| D14 | `application` | 1 | D10, D11, D13 | `R/application.json` |
| D15 | `harness.pi.resources` | 9 | F0 | `R/harness-pi-resources.json` |
| D16 | `harness.pi.conformance`, `.conformance.python` | 6 | F0 | `R/harness-pi-conformance.json` |
| D17 | `harness.pi` | 54 | D15, D16 | `R/harness-pi.json` |
| D18 | `harness.pi.local` | 25 | D15–D17 | `R/harness-pi-local.json` |
| D19 | `harness.cli` | 1 | D18 | `R/harness-cli.json` |
| D20 | `harness` | 135 | D16 and exact accepted Harness contracts | `R/harness-root.json` |
| D21 | all ten zero-route surfaces listed above | 0 | F0 | `R/zero-boundaries.json` |

The 20 nonzero units are disjoint and sum to exactly **985**. D21 supplies decision
ownership that cardinality cannot detect. Its matrix records `declares_all`
separately from effective emptiness and decides whether each accepted negative
boundary requires a literal empty `__all__`.

**Disposition gate for each unit:** exact row and surface cardinality; no foreign route
key; defining-origin and initializer identity agreement with F0; raw consumer,
documentation, and authority evidence retained; both outcome dimensions populated;
and every non-preserve or newly supported proposal accompanied by an exact decision
packet. A unit may produce unresolved proposals for review, but it cannot close as an
accepted disposition until every unresolved human-owned item in that unit is decided.
Accepted exact route inventories are preserved deterministically unless a separately
authorized proposal changes them. A test using “approved” or “accepted” is verification
evidence only until its durable authority is traced.

### M1 — File-level mutation partition

M1 begins only after the applicable D outputs are accepted. It does not alter source.

**Exact inputs:** `R/foundation.json` and all accepted D1–D21 matrices.

**Exact output:** `R/mutation-plan.json`, mapping every required changed file to
exactly one inactive implementation child, its accepted route decisions, predecessors,
verification targets, and rollback boundary. It also records a no-change result for
accepted cohorts requiring no mutation.

**Gate:** every proposed changed path occurs once; no two writers own the same file;
every source, consumer, test, evidence mapping, fixture, migration record, and
Sphinx page affected by a route change has an owner; initializer ownership follows the
route cohort; dependency order is acyclic; and every implementation child is cohesive
and independently revertible. M1 must stop if a shared file has no single outward
owner. It may create a serial integration owner; it may not duplicate assertions or
silently split an evidence identity.

### I* — Conditional implementation children

No I child exists or is active now. M1 may instantiate one only when an accepted
matrix requires mutation. Each child receives one accepted route matrix and the exact,
non-overlapping path set from `R/mutation-plan.json`; its output is exactly the new
contents of those paths plus its recorded software-verification result. A no-change
matrix gets no implementation child.

An implementation child may change only its assigned initializers, necessary import
wiring, assigned consumers, assigned tests/evidence mappings, and assigned API/concept/
migration documentation. It may not change scientific/numerical meaning, serializer or
persistence meaning, wire bytes/tags/failure order, method visibility, execution
settings, dependencies, or unrelated domain behavior. Breaking, deprecation, alias,
retirement, or newly supported behavior requires its accepted human route decision
before activation.

**Implementation gate:** exact accepted support and compatibility behavior; source-tree
and isolated-wheel imports for all affected routes; wheel origin and metadata; required
installation profile/extras; object identity, `__module__`, global lookup and pickle
where applicable; signatures, protocols, exceptions, and enums; exact wire/schema/
round-trip/failure-order evidence where applicable; targeted pytest; affected strict
mypy; Ruff check/format; Sphinx dummy and HTML builds with warnings as errors; and the
accepted non-waiving production-conformance ratchet. Graph evidence states only that,
for each named view, no observed edge violates an explicitly supplied accepted
contract for that exact edge and view. Import/wheel smoke is reported separately and
neither claim is universal runtime conformance.

### V1 — Aggregate verification

**Exact inputs:** `R/foundation.json`, all accepted D matrices,
`R/mutation-plan.json`, and the exact resulting states/evidence of every instantiated I
child.

**Exact output:** `R/aggregate-verification.json` plus its deterministic human-readable
summary.

**Gate:** all 985 predecessor route keys occur exactly once with accepted support and
compatibility results and exact lineage; every supplemental candidate is explicitly
resolved without being promoted from syntax; all 35 surfaces and ten negative
boundaries are checked; duplicate names at different routes retain separate outcomes;
final `__all__`, explicit package binding, deep-route, warning, identity, and failure
behavior match each accepted matrix; maintained source, tests, examples, Harness
checks, and docs reconcile; no implementation-only descriptive owner is documented as
supported; all M1 path ownership is disjoint; the full configured Python software-
verification suite, package build/install smoke, source-tree typing, Sphinx,
Harness/projection reconstruction, ratchet, and whitespace gates pass or an exact
limitation is reported. V1 verifies; it cannot invent or repair a disposition.

## Dependency DAG

Arrows below mean **decision or evidence prerequisites**, not asserted runtime import
semantics. M1 must refine implementation ordering from exact accepted changes and
named Phase 2 graph views.

```text
Accepted Phase 1 Option B + accepted Phase 2 bounded capabilities
                              |
                              v
                        F0 foundation
                              |
       +----------------------+--------------------------+
       |                      |                          |
       v                      v                          v
 D1 geometry             D3/D4/D5                  D6 persistence
       |                 operators/units/               + D7 Petri net
       v                 provenance                     |
 D2 Kohn--Sham                                          +--> D8 control --+
       |                                                +--> D9 runs -----+--> D10 Workflow root
       +----------------------+------------------------------+              |
                              |                                             +--> D11 analysis
                              +--> D12 calculator PW                         |
                                      \                                    |
                                       +----------> D13 QE <----------------+
                                                         |
                                            D11 + D10 + D13
                                                         v
                                                   D14 application

 F0 --> D15 resources ----+
 F0 --> D16 conformance --+--> D17 generic Pi --> D18 local --> D19 CLI
            +-----------------------------------------------> D20 Harness root
 F0 -------------------------------------------------------> D21 zero boundaries

 all accepted D1-D21 --> M1 exact file partition --> conditional serial/parallel I*
                                                       |
                                                       v
                                                   V1 aggregate
```

Where a D11 or D12 route does not actually cite one of the conservative prerequisites,
M1 may omit that implementation edge. It may not invent a dependency contract from a
lexical edge.

## Route-disposition method

1. **Freeze lineage, not conclusions.** Preserve every one of the 985 Phase 1 route
   keys and its predecessor identity. Refresh current facts alongside it. Never mutate
   historical Phase 1 evidence.
2. **Inventory three different observables.** Record separately (a) effective star
   membership, (b) explicit/fresh-process package attributes, and (c) documented,
   accepted supported routes. A deep implementation path is a fourth relevant
   compatibility observable. None implies another.
3. **Add supplemental records.** Non-`__all__` bindings, relevant deep routes, and a
   proposed new supported route receive separately keyed records. “No unaccepted extra
   export” means: no final star member beyond its accepted star disposition, no
   package binding or deep behavior outside its compatibility disposition, and no
   route described as supported without accepted support evidence and synchronized
   docs. It does not mean that Python can make unsupported implementation modules
   physically unimportable.
4. **Trace authority.** For every route, distinguish raw tests/docs/consumers from an
   accepted Task, decision, specification, or public contract. Preserve exact accepted
   inventories deterministically. Record contradictory or missing authority as
   unresolved.
5. **Decide support and compatibility independently.** A supported route can be
   preserved, deprecated, aliased, or retired only as its accepted decision permits;
   an unsupported route may remain importable for internal ownership. Unknown cannot
   be converted into unsupported or retirement.
6. **Document exact public behavior.** A supported route requires a synchronized API
   reference/concept entry. Deprecation/alias/retirement requires migration text,
   replacement, duration or retirement condition, warnings and failures. Internal
   consumers may retain owner-local deep imports where dependency direction, typing,
   or cycle avoidance requires them.
7. **Protect represented contracts.** Before a re-export changes, check object
   identity, `__module__`, global lookup/pickle, signatures, wire tags/bytes,
   exceptions, serializer failure order, units, and scientific representation. Phase
   3 does not reinterpret basis, gauge, energy reference, geometry, or validation
   meaning.

## Future ownership boundaries

No writer is assigned or active. If later activated, ownership is file-exclusive:

| Future owner | Exclusive mutation surface |
|---|---|
| F0 | Only `R/foundation.json`; no production module, initializer, test, or public API page. The report records its exact reproduction procedure and input identities. |
| D1–D21 | Only that unit's exact `R/*.json` matrix. Disposition writers are read-only with respect to production, tests, and docs. |
| M1 | Only `R/mutation-plan.json`. |
| Cohort implementation owner | Initializer(s) for that cohort, necessary same-cohort import wiring, and files assigned exclusively by M1. |
| Workflow root integration owner | `workflows/__init__.py`; the existing control/runs public-API modules that jointly assert leaf and root behavior; shared Workflow API/migration pages. Leaf owners must not edit those shared tests. |
| Periodic/QEXSD API integration owner | `docs/api/periodic-records.rst` after D1, D2, and D13; scientific leaf owners must not edit this shared page concurrently. |
| Harness API integration owner | `docs/api/harness-control.rst` after D15–D20; Harness leaf owners must not edit this shared page concurrently. |
| Analysis example integration owner | `examples/tutorials/silicon-bands/scripts/compare_retained_observations.py` after D10/D11 decisions. |
| QE example integration owner | `examples/tutorials/silicon-scf/qe/reconstruct_silicon_scf.py` after D13. |
| CLI/local integration owner | Repository Harness validation consumers that jointly import `harness.cli` and `harness.pi.local`. |
| Application composition owner | Cross-domain campaign/application consumers, including any file combining analysis, calculator, Workflow, Petri-net, or unit imports. |
| V1 | Only aggregate evidence outputs; no repairs. |

M1 must enumerate the exact paths rather than granting these owners broad globs. Any
newly discovered shared file goes to one serial outward-integration owner; it is not
shared between leaf writers. Existing pytest evidence identities remain with their
single owner. If a split is genuinely necessary, M1 records predecessor mappings and
prohibits duplicated assertions.

## Gates and claim boundaries

| Gate | Establishes | Does not establish |
|---|---|---|
| F0 identity/cardinality/schema gate | Complete bounded current fact views and immutable 985-row lineage | Route support, compatibility authority, runtime completeness |
| Per-D authority/disposition gate | A reviewable or accepted exact route matrix | Implementation correctness or human acceptance by reviewer agreement |
| M1 ownership gate | Non-overlapping, acyclic future mutation allocation | Correct route policy or source behavior |
| Per-I software gates | Agreement with the accepted route and compatibility contract under tested source/wheel conditions | Universal runtime behavior, numerical verification, scientific validation, UQ, release status |
| Named dependency-view checks | No observed edge violates the supplied accepted contract for that exact view | Universal dependency meaning or runtime import success |
| V1 aggregate gate | Integrated software-verification coverage for accepted Phase 3 scope | External-user census, protected-execution authority, release, or final human acceptance |

Installed-wheel typing is explicitly outside the Phase 3 claim unless the human later
accepts a PEP 561 packaging contract. Wheel import behavior and source-tree typing
remain required and separately reported.

## Accepted, deferred, and human-decision items

### Already accepted and preserved

- Option B route-specific support policy, descriptive unsupported implementation-owner
  names, and the separation of package export from method visibility.
- The 985-row Phase 1 predecessor inventory as required lineage, together with exact
  non-export inputs; not as 985 accepted supported APIs.
- Phase 2 explicit-input syntax facts, exact callable/hook rules, named dependency
  views, and the content-identified non-waiving ratchet, with their existing claim
  limits.
- Existing accepted scientific, wire, persistence, Workflow, Harness, QE, and package
  ownership contracts. Phase 3 may consume but not reinterpret them.

### Deterministic corrections accepted into this recommendation

- Add the missing top-level package and all ten zero-route boundaries to explicit
  decision ownership.
- Keep all 985 predecessor records while adding separately keyed binding, deep-route,
  consumer, documentation, and proposed-new-route records.
- Split support status from compatibility disposition.
- Split the former broad Pi Harness family into resources, conformance/Python, generic
  Pi, local composition, and CLI units, with Harness root separate.
- Make F0 a neutral task-internal derived fact report; record ambiguous authority
  rather than adjudicating it.
- Insert M1 file-level mutation partitioning before any writer and assign known shared
  files to serial integration owners.
- Restrict dependency claims to exact accepted contracts in named graph views.

### Deferred without blocking this plan

- PEP 561 installed-package typing (`py.typed` or stubs). This is a separate public
  packaging decision if downstream typing support is requested.
- Phase 4 module decomposition, callable ownership migration, abstraction redesign,
  broad deep-import cleanup, and scientific/numerical policy changes.
- Claims about unknown third-party consumers, reflective access, downstream pickle,
  subclassing, or mocking. These remain compatibility uncertainty, not evidence of
  safety.

### Genuine later human decisions

No new architecture checkpoint is justified now: Option B is already selected, and
all review corrections above follow deterministically from accepted contracts. A
human public-contract decision is required later only for an exact route/batch whose
complete packet leaves materially different defensible outcomes—for example:

- stabilizing a syntactic route as newly supported;
- retiring or relocating a supported or compatibility-observable route;
- selecting deprecation duration/retirement conditions;
- accepting an alias with observable identity and failure behavior; or
- changing one of the 14 temporary `periodic` compatibility routes.

Where durable authority already fixes an exact inventory, preservation is a
correction, not a new choice. Missing evidence remains unresolved and stops that unit;
it does not manufacture a choice or authorize removal.

## Adversarial findings disposition

| Finding | Source | FindingDisposition | Resolution and disagreement handling |
|---|---|---|---|
| Top-level package omitted; ten zero boundaries lacked complete ownership | Both reviews | `MUST_FIX` | D21 owns all ten, including `ksdft2effmass`; it distinguishes three literal and seven implicit empty inventories. Both reviews agree. |
| The 985 rows were treated as exhaustive | Both reviews | `MUST_FIX` | They remain mandatory immutable predecessor lineage, while F0 adds separately keyed package-binding, runtime-view, deep-route, maintained consumer, docs, and new-route candidates. This resolves the apparent wording difference between “keep 985 unchanged” and “not exhaustive”: unchanged lineage is not an exhaustive namespace universe. |
| Maintained examples and repository Harness consumers were omitted | Integration review | `MUST_FIX` | F0 explicitly inventories all content-identified maintained first-party Python consumers, including examples and Harness checks. |
| Support and compatibility were collapsed | Assumption review | `MUST_FIX` | Every route gets orthogonal support and compatibility records with exact observable fields. |
| Generic Pi Harness family was not cohesive/reversible | Assumption review | `MUST_FIX` | D15–D19 split resources, conformance/Python, generic Pi, local composition, and CLI; D20 keeps Harness root separate. |
| Neutral ledger introduced an implicit wire decision and adjudicated ambiguity | Assumption review | `MUST_FIX` | F0 is a versioned task-internal regenerated evidence format, not a public/persistent API; its closed generation schema rejects representation errors while unknown/ambiguous authority remains data for D units; no production parser is introduced. |
| Aggregate “no forbidden dependency” exceeded accepted graph semantics | Assumption review | `MUST_FIX` | Per-I and V1 claims are limited to explicitly supplied accepted contracts for exact named views; import smoke is separate. |
| Implementation ownership overlapped on shared tests/docs/consumers | Integration review | `MUST_FIX` | M1 is a prerequisite; known Workflow, periodic/QEXSD, Harness, examples, and application shared files have one serial integration owner. |
| Installed-wheel typing was overstated | Integration review | `SAFE_TO_DEFER` | Phase 3 claims source typing and wheel imports/metadata only. PEP 561 support is deferred to a separate human packaging decision if requested. |

**ReviewOutcome: NO_BLOCKING_FINDINGS**

The two original reviews correctly required changes. This synthesis incorporates every
`MUST_FIX`; the sole `SAFE_TO_DEFER` item is explicitly excluded from the claim. This
outcome evaluates the corrected plan only and is not human acceptance or software
verification of an implementation.

**OperatorRequest: NONE**

## Exact recommended next human action

Review and, if satisfactory, respond exactly:

> `Accept the corrected Phase 3 public-import-boundaries plan and authorize activation of F0 only. Keep D1-D21, M1, all implementation children, V1, and automatic successor activation inactive.`

That action would authorize only the neutral current-fact foundation. It would not
classify any route, accept a compatibility disposition, authorize production/API/doc
mutation, or authorize commit, push, protected execution, release, or successor work.
