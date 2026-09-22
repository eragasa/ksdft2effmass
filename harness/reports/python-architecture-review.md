# Python architecture inventory review

## Status and authority boundary

This is the first bounded evidence-gathering slice for managed Task
`python.architecture-refactor.inventory-and-policy`. It interprets the deterministic
inventory in `harness/reports/python-architecture-inventory.json`. It records human
acceptance of this bounded Phase 1 result but does not refactor source, change a
supported import, or establish scientific validation.

The verbatim human response to the Phase 1 recommendation was:

> recommendation authorized

This is normalized as **Option B**: supported imports are curated route by route at
deliberate package/subpackage boundaries; top-level implementation classes use
descriptive non-underscore names without becoming supported unless deliberately
exported and accepted; owner-local private mechanical methods remain permitted; and
cross-object private calls plus private ownership of public/scientific/numerical policy
are prohibited. Package imports cannot govern method visibility, so private methods
are not mechanically renamed into public members.

The verbatim human closeout response was:

> accepted and closeout authorized

This is normalized as human acceptance of the completed Phase 1 inventory, selected
Option B policy, candidate register, clean Sphinx dummy/HTML gates, and explicit
D4-D7 disposition. It authorizes managed administrative closeout only; it does not
authorize production refactoring, scientific validation, protected execution, release
activity, or successor activation.

The review is synchronized with these authorities:

- `AGENTS.md`;
- `docs/architecture/v2/index.md` and
  `docs/architecture/v2/repository-layout.md`;
- `docs/development/source-documentation.rst`;
- `.pi/skills/design-data-action-objects/references/data-action-architecture.md`; and
- `harness/intake/python-architecture-review-refactor.md`.

Architecture v2 is a partially implemented target. Therefore disagreement between a
static source signal and the v2 target is a migration-review signal, not automatically
a defect in the current implementation.

## Method and evidentiary limits

The retained typed generator
`.pi/task-ownership/generate_python_architecture_inventory.py` parses all 211
maintained `*.py` modules beneath `python/src/ksdft2effmass` with the Python 3.14
standard-library AST. It receives explicit repository, source, test, documentation,
Task, and output roots; its recursive JSON value union contains only exact scalar,
tuple, and string-keyed-dictionary containers, with no `Any`, generic `object`, erased
container, or non-entry-point module callable. Its SCC implementation and methodology
both identify the same Kosaraju-style forward-finish/reverse-graph two-pass algorithm.
The completion validator regenerates into an isolated temporary path and byte-compares
the canonical JSON before running the existing gates.

The inventory records per-file SHA-256 identities and an aggregate source-tree
identity, physical and AST spans, definitions, package exports and origins, static
imports, strongly connected components, private-call facts, route-decision inputs,
typed-wire debt, and nominal Protocol/ABC declarations. Tests and documentation are
scanned only as consumer evidence and are excluded from production metrics. Exact
algorithms and the reproduction command are in `methodology`; notably,
`from FACADE import NAME` produces both a facade edge and a `FACADE.NAME` submodule
edge when both resolve to maintained modules. The source identity is in
`source_identities.aggregate_sha256`.

The following are **observed evidence**:

- an exact source path, AST symbol, line/span, literal `__all__` entry, static import
  edge, explicit inheritance edge, consumer import, or source digest recorded by the
  inventory;
- an accepted documentation or test statement at a cited repository path; and
- an existing architecture ownership or dependency statement in Architecture v2.

The following remain **review signals**:

- a module, class, or method crossing a reporting threshold;
- an underscore-prefixed name;
- a syntactic export, deep import, or shared method name;
- a static cycle that contains package facades, `TYPE_CHECKING`, conditional, or local
  imports; and
- apparent responsibility clusters inferred from neighboring symbols.

These signals do not prove bad cohesion, unsupported API status, runtime cycles,
scientific error, or the correct extraction boundary. File size and underscore naming
are never treated as defects by themselves.

Option B settles the architecture policy, not the classification of every existing
route. Before implementation, each affected route still needs a bounded disposition
under its accepted contracts; any breaking change, public Protocol/ABC change, new
deterministic conformance threshold, serialization or scientific-contract change, or
package-ownership change retains its applicable human authority.

## Inventory interpretation

### Scale and concentration

`summary` records 90,700 physical lines, 971 top-level classes, 188 top-level
callables in 52 modules, 112 single-underscore top-level classes, and 563
single-underscore non-dunder methods. The inventory separately counts 645 Python
special methods so that `__post_init__`, `__init__`, and other language hooks are not
misclassified as private ownership.

The reporting thresholds are 500 module lines, 300 class-span lines, and 100
method-span lines. They produce 57 module, 38 class, and 105 method signals. The
highest concentrations are:

| Evidence | Lines | Interpretation |
|---|---:|---|
| `workflows/persistence.py` | 10,503 | Persistence records, validation, repository behavior, run serialization, and result-value serialization coexist. |
| `WorkflowRunSerializer` | 7,143 | `_encode` (2,232 lines) and `_decode` (4,024 lines) dominate the owner. This is a strong cohesion and wire-compatibility review signal, not proof of an allowable split. |
| `workflows/runs/records.py` | 3,358 | Forty-two records/enums cover attempts, result production, nested Workflow invocation, authority, dispatch, scientific decisions, and transitions. |
| `workflows/runs/replay.py` | 2,737 | Public replay values/action coexist with the 1,904-line `_WorkflowRunStructureValidator`. |
| `integration/quantum_espresso/effects.py` | 2,537 | Staging, workspace snapshots, native-output collection, and terminal-record publication form four visible capability clusters. |
| `harness/authority.py` | 2,165 | Authority values/actions coexist with 18 module-level callables and a private `_Serializer` inheritance owner. |

All exact spans and the remaining signals are in `long_owners`. A long immutable
record can still be cohesive; a short callable can still own misplaced policy.
Semantic responsibility, consumers, contracts, and verification determine whether a
future split is justified.

### Module-level callables

`top_level_callables` records 188 definitions: 137 underscore-prefixed and 51 without
an underscore. Fourteen `harness.cli.*.run` functions are identifiable external CLI
adapters. Those are plausible Python/packaging entry-point exceptions when their
bodies remain typed adaptation into explicit owners. The other definitions require
owner-by-owner classification. For example, `harness/authority.py` has 18 and
`harness/_contract.py` has 18; the count does not establish that each is dangling.

Architecture and source-documentation policy already require non-entry-point behavior
to live on a DataObject, ResultObject, ActionObject, serializer, Workflow, adapter, or
other explicit class owner. A future conformance rule should therefore report an exact
callable and its proposed owner or external hook. It must not ban every module-level
function mechanically or move trivial intrinsic checks into gratuitous ActionObjects.

### Classes and methods with private names

The 112 top-level class definitions in
`underscore_prefixed_top_level_classes` include substantial owners such as:

- `workflows.runs.replay._WorkflowRunStructureValidator` (1,904 lines);
- `harness._compiler_serialization._HarnessCompilerSerializer` (484 lines);
- `harness.pi.local.dbcontrol.ingestion._RepositoryControlIngestor` (484 lines); and
- `harness.pi.conformance.python.parser._PythonModuleFactExtractor` (409 lines).

They also include narrow exceptions, wire adapters, and implementation records. The
same spelling signal therefore covers materially different responsibilities.
Descriptive non-underscore class names can remain non-exported: package and
subpackage re-export policy, documentation, and accepted contracts determine support,
not an underscore alone.

Methods are different. Python package `__all__` controls star import names; it cannot
hide or export individual methods on an exported class. Renaming `_decode` to `decode`
on `WorkflowRunSerializer`, for example, makes a conventionally public attribute and
can affect documentation, typing, subclasses, mocks, and callers even when package
exports do not change. The inventory does not infer reflective use, but it now
separates statically resolved class-owner private calls from dynamic or aliased
receivers.

Selected Option B confirms the coherent narrower rule: private
scientific/numerical/public policy must not be the sole contract owner, cross-object
private-method calls are prohibited, and concise owner-local mechanical helpers remain
permissible. Top-level implementation owners receive descriptive non-underscore names
without becoming supported merely by naming. No mass private-method rename is
permitted.

#### Deterministic cross-owner private-call debt

`private_method_calls` records 16 statically resolvable cross-owner calls and no
unresolved receiver facts. All 16 are migration debt under the selected deterministic
cross-object prohibition. They include all reviewer examples:

- `harness/compiler.py:204,206`: `HarnessSourceFamilyContract.__post_init__` calls
  `HarnessLegacyDecisionBinding._require_path`;
- `harness/compiler.py:307`: `HarnessSourceIdentity.__post_init__` calls the same
  cross-owner method;
- `harness/pi/conformance/python/strict.py:295`:
  `PythonCodingStandardsAdapter.execute` calls
  `PythonCodingStandardsContract._object_annotation_exemptions`; and
- `workflows/control/dispatch.py:928`:
  `SimulationDispatchAdapterResult.__post_init__` calls
  `SimulationDispatchAdapter._outcome_agrees`.

The remaining original resolved facts are one ownership-validator call at
`harness/pi/conformance/python/ownership.py:297` and **seven** parser calls at
`harness/pi/conformance/python/parser.py:516,520,589,969,1010-1012`. The inspector
also resolves `PythonConformanceValidator()._execute` at
`harness/pi/local/control/generation.py:144` and the exact typed
`self._common_codec` dependency calls at `harness/pi/wire/resources.py:36,122`.
A future contract-preserving correction should prioritize the four
public-domain-owner groups:
(1) compiler path invariants, (2) strict-conformance exemptions, (3) dispatch outcome
agreement, then (4) conformance parser/ownership mechanics. Intrinsic invariants move
to their DataObject; reusable cross-object policy moves to a named ActionObject;
mechanical parser behavior receives one explicit parser owner. The exact source owner
must be verified in each bounded implementation, but no new human policy is needed to
stop one class calling another class's private method. If later syntax proves a
non-self receiver without recovering its exact owner, the inventory classifies it as
deterministic `cross_owner_owner_unresolved` debt rather than a discretionary signal.

### Package exports, supported imports, and deep imports

`package_exports` is a syntactic inventory, not a support decision. The top-level
`ksdft2effmass` package deliberately declares an empty `__all__`. Breadth is
concentrated at subpackage roots:

| Package | Literal `__all__` count |
|---|---:|
| `ksdft2effmass.workflows` | 230 |
| `ksdft2effmass.harness` | 135 |
| `ksdft2effmass.integration.quantum_espresso` | 134 |
| `ksdft2effmass.workflows.runs` | 116 |
| `ksdft2effmass.petrinet.colored` | 68 |
| `ksdft2effmass.harness.pi` | 54 |

The sum of effective star-export names over 35 package/subpackage roots is 985, with
duplicates possible across nested roots. This is breadth evidence, not a finding that
985 contracts are accepted or should remain at every route.

Existing accepted support evidence must retain precedence over naming heuristics.
Examples include the exact package routes described by `docs/api/operators.rst`,
`docs/api/provenance.md`, `docs/api/workflows.rst`,
`docs/concepts/sqlite-revision-store.rst`, and
`docs/architecture/migration/v1-to-v2/implementation/harness/decisions-authority.md`,
plus exact `__all__` verification in tests such as
`operators/test__OperatorRecord__construction.py`,
`provenance/test__public_api.py`, `harness/test__compiler_public_api.py`, and
`workflows/runs/test__public_api.py`. Conversely, accepted Task records explicitly
label some direct/private probe imports as private and revisable. Importability alone
must not silently promote them.

`consumer_imports` contains 196 imported-module groups. Under the documented lexical
rule, 164 groups are deep-module imports, with 483 source-consumer occurrences and
125 test-consumer occurrences. This over-approximates compatibility obligations:
internal imports, tests of private probes, and package-root imports have different
status. For example, six tests import `analysis._parameter_study`, while the accepted
parameter-study Task states that probe is private and not a stable public API.

Phase 1 supplies 16 representative C1-C10 rows in `proposed_route_matrix`, but the
four package-set rows are inventory context only and cannot govern an individual
export. `export_routes` is now the route-level decision input for all 985 syntactic
exports: each row records exact origin, exact static source/test consumers, exact
qualified-route or same-line from-import documentation evidence, exact accepted
support evidence when found, route-specific compatibility consequences, and
`unclassified_pending_bounded_option_b_application`. Bare-symbol matches are excluded;
absence of exact evidence is recorded as **unknown**, never unsupported. C7 consumers are
constrained by both source (`campaigns._plane_wave_study`) and target
(`petrinet.colored`), and C9 records the actual private deep route
`ksdft2effmass.analysis._parameter_study.ParameterStudyRefiner` rather than a
nonexistent package reexport. Option B governs each later true-route classification;
Phase 3 may only implement bounded accepted route dispositions and may not reopen the
architecture policy.

### Static dependencies and cycles

The maintained-source graph has 568 unique internal module edges and three strongly
connected components under the inventory's deliberately broad rule:

1. `harness.compiler` and `harness._compiler_serialization`;
2. `integration.quantum_espresso` and
   `integration.quantum_espresso.result_values`; and
3. a 15-module `harness.pi` component spanning validation, resource package facades,
   and wire modules.

These differ from the intake's preliminary no-cycle observation because this method
includes package `__init__` facades and imports inside `TYPE_CHECKING`, conditional,
function, and class bodies. The compiler reverse edge is type-checking-related;
`result_values.py` uses `from . import contracts/observation`, which creates a package
facade edge in this lexical model; the Harness component includes local imports used
to manage construction and wire boundaries. The SCCs are reproducible static signals,
not a claim of runtime import failure.

At component level the graph mostly reflects v2's inward directions, including
`integration → calculators/workflows/structures/electronic_structure/ksdft`,
`analysis → workflows`, `calculators → workflows`, and
`workflows → persistence/petrinet`. Two current direct edges deserve migration review
against the prospective diagram:

- `campaigns._bulk_silicon_production_convergence → petrinet.colored` and
  `campaigns._plane_wave_study → petrinet.colored`; and
- `workflows.observations → ksdft.pw`.

Architecture v2 is only partially implemented and its required-edge list is not stated
as an exhaustive ban on every unlisted edge. These edges therefore need semantic
ownership review, not automatic removal. No static edge from
`petrinet.colored → workflows` was observed.

### Existing Protocol and ABC relationships

`abstractions.definitions` records 14 Protocols and one ABC. The Protocols fall into
recognizable structural categories:

- domain roles: `workflows.model.ResultObject`, `Task`, and `Workflow`;
- data/source roles: the three `workflows.observations` protocols;
- operation ports: `PlaneWaveCalculator`, `AtomicRevisionStore`,
  `WorkflowRunRepository`, `WorkflowResultValueCodec`,
  `SimulationDispatchEntryCommitter`, `SimulationDispatchEffect`,
  `CodingStandardsAdapter`, and `HarnessDomainValidator`.

The only ABC is `analysis._parameter_study.ParameterStudyRefiner`, with abstract
`configuration_identity`, `refinement_identity`, and `execute`, and one explicit
subclass, `FiniteSequenceParameterStudyRefiner`. The accepted parameter-study Task
specifically records this nominal ABC, so the number of implementations is not a
license to replace it.

The AST can establish only explicit inheritance. It cannot prove structural Protocol
conformance or substitution needs. Existing Protocols appear aligned with structural
ports or roles, while the ABC expresses a nominal refinement family, but each public
change still requires consumer and compatibility evidence. Shared `execute`,
`serialize`, or `validate` names alone justify neither Protocol nor ABC.

### Harness authority typed-wire debt

`strict_typed_wire_debt` records 61 exact facts in `harness.authority` and
`harness._contract`: two `typing.Any` imports, 11 Any annotations, four
`cast(Any, ...)` calls, 35 generic-`object` annotations, and nine dictionaries or
mappings erased by Any/object (categories overlap where one annotation demonstrates
both debts). Representative controlling facts are:

- `harness/authority.py:1185,1416,2135,2161` — cast through Any;
- `harness/authority.py:1424-1434` — `_Serializer.execute(value: object)` and
  `_decode(...) -> Any`;
- `harness/authority.py:1440` — `dict[str, type[Any]]`;
- `harness/authority.py:1161,1400,2107,2138` — `dict[str, object]`; and
- `harness/_contract.py:19-200` — generic object, Any, and erased-dictionary parsing
  boundaries, including `dict[str, Any]` at lines 150, 151, and 168 and
  `dict[str, object]` at line 200.

This is typed software-architecture debt, not evidence that current wire bytes are
wrong. Any future C5 boundary must define an exact closed recursive representation
union (for example, null/Boolean/integer/real/string/list/string-keyed-map where the
accepted wire permits each member), parse it through typed conversion into closed
domain records, and remove cast-through-Any and erased dictionaries while preserving
accepted fields, error behavior, canonical bytes, and public imports. Merely moving
`_Serializer` would preserve the violation and is not an acceptable decomposition.

## Prioritized candidate register

Priorities rank review value and coupling risk, not defect severity. Future Task
boundaries below are proposals within already recorded phases; none is created or
activated here.

| ID / priority | Current owner, consumers, and contract | Verification surface | Exact managed overlap and authority consequence | Proposed future boundary |
|---|---|---|---|---|
| C1 / P0 | `workflows.persistence.WorkflowRunSerializer` (7,143 lines); consumed through the Workflow facade, dispatch, analysis/QE codecs, and atomic repository. Exact versioned bytes, failure ordering, imports, and `__module__` are compatibility surfaces. | Eleven `test__WorkflowRunSerializer*.py` modules; `test__WorkflowRunAtomicRepository.py`; **`test__WorkflowRunAtomicRepository__nested_history.py`**; Workflow persistence/API docs. | `migration.v2.workflows.persistence` is `closed_software_verified` but explicitly not human acceptance; `migration.v2.workflows.workflow-run` is `closed_human_accepted_pass`. Consume both results, treat the latter as accepted authority, and do not create a competing wire contract. | Phase 4 may decompose internal wire mechanics behind the unchanged serializer only after the exact route receives its bounded Option B disposition, with exact byte/failure/import compatibility. |
| C2 / P0 | `workflows.runs.replay._WorkflowRunStructureValidator` (1,904 lines); persistence calls it at `workflows/persistence.py:268,1617,1671,2246`, and replay calls it at `runs/replay.py:443`. Issue order and replay/persistence outcomes are observable. | `runs/replay/test__WorkflowRunReplayer.py`, transaction-validator/repository tests, and Workflow control tests. | Same two Workflow Tasks and statuses as C1. The accepted allocation in `workflows/persistence.md:213-222` places this private owner **inside `runs/replay.py`**, exposes `execute` to both callers, and says **there is no extra structural module**. | Default bounded work is in-place owner cleanup only, and only under the accepted private-owner policy. An extra module or changed structural/replay ownership is a separate human Architecture v2 decision, not default Phase 4 decomposition. |
| C3 / P0 | Package-set rows cover `workflows.__all__` (230), `harness.__all__` (135), QE `__all__` (134), and `workflows.runs.__all__` (116), but cannot govern individual names. All 985 individual `export_routes` carry exact origin/consumer/evidence/consequence/disposition fields. | Exact package-public-API tests, API/concept pages, and per-route evidence where an exact qualified/import form exists. | Workflow rows consume the two Workflow Tasks above; Harness consumes `migration.v2.harness.decisions-authority` (`closed_human_accepted_pass`); QE consumes the seven C4 Tasks below. Accepted results remain authority over their exact routes. | Inactive `python.architecture-refactor.public-import-boundaries` may, after activation, apply Option B route by route under accepted contracts; it cannot infer support from a package set or reopen the selected policy. |
| C4 / P1 | `integration.quantum_espresso.effects` (2,537 lines), with exact matrix rows for stager, snapshotter, output collector, and terminal publisher. Public exports, artifact/terminal representations, `__module__`, and execution boundaries must remain stable. | QE local-execution, executor, outcome-resolver, public-API, serialization, and artifact tests. | `migration.v2.integration.quantumespresso` is `planning` and grants no aggregate acceptance. `migration.v2.calculators.quantum-espresso-contracts` plus its boundary-decision, contract-verification, simulation/executor-bindings, and task-contract children are `closed_human_accepted_pass`; `quantumespresso.simulations.integration` is `completed` with human closeout. Consume accepted boundaries; do not reopen calculator/QE ownership or execution authority. | Phase 4 may propose capability-aligned modules only with unchanged ActionObject, artifact, execution, and route contracts; no scientific/execution setting changes. |
| C5 / P1 | `harness.authority` (18 callables, `_Serializer`) and `harness._contract`; 61 exact typed-wire debt facts. Harness public names and wire behavior are compatibility obligations. | Authority, decision, signature, serializer, strict-typing, and Harness public-API tests and accepted migration page. | `migration.v2.harness.decisions-authority` is `closed_human_accepted_pass`; its authority/wire result must be consumed, not redefined. | Phase 4 must introduce an exact closed representation union and typed conversion into closed records while preserving wire behavior/imports. Moving erased parsing is insufficient; Phase 5 may separately evaluate `_Serializer` inheritance. |
| C6 / P1 | 188 top-level callables; 14 CLI `run` hooks are exact framework-adapter candidates. Moving a callable can change imports even without behavior change. | Current callable tests plus future AST conformance fixtures. | `python.architecture-refactor.architecture-conformance` is `inactive`; it supplies no current implementation authority. Package-specific accepted Tasks remain authoritative for each callable's behavior. | Phase 2, only after activation, may implement the report-only inspector/ratchet with exact hook exceptions; migration remains package-owned Phase 4 work. |
| C7 / P1 | Three lexical SCCs and exact campaign→Petri-net / workflow→Kohn–Sham edges. Facade/type-only edges are not automatically runtime cycles. | Import smoke, dependency-direction, and package API tests. | `migration.v2.calculators.plane-wave-study-contracts` and `migration.v2.petrinet.colored.legacy-retirement` are `closed_human_accepted_pass`; `python.architecture-refactor.architecture-conformance` is inactive. Their accepted package semantics cannot be replaced by graph cleanup. | A separately activated Phase 2 may expose lexical/runtime/facade-excluded views. Phase 4 addresses an edge only after semantic ownership confirmation. |
| C8 / P2 | `workflows.runs.records` (3,358 lines, 42 records/enums); runs facade, replay, persistence, control, and QE consume it. Records participate in wire and `__module__` compatibility. | `workflows/runs/**`, serializer facets, control tests, Workflow API/concept docs. | `migration.v2.workflows.persistence` (`closed_software_verified`) and `migration.v2.workflows.workflow-run` (`closed_human_accepted_pass`) govern. The human-accepted WorkflowRun result is controlling. | Phase 4 may evaluate record families only after C1 and exact route dispositions under Option B, retaining accepted route/wire/module identity unless separately decided. |
| C9 / P2 | Fourteen Protocols, private deep route `ksdft2effmass.analysis._parameter_study.ParameterStudyRefiner`, and `_Serializer` inheritance. The ABC is not an `analysis` package reexport. Changes affect typing, runtime checks, construction, subclassing, imports, and module identity. | mypy, runtime-check, private-probe import, and concrete behavior tests; no stable public API is inferred. | `migration.v2.calculators.plane-wave-study-contracts`, `migration.v2.persistence.store`, `migration.v2.workflows.model`, and `migration.v2.workflows.control-ingress` are `closed_human_accepted_pass`; `python.architecture-refactor.abstraction-design` is inactive. Existing accepted abstractions and the private-probe limitation remain controlling. | After activation, Phase 5 may propose one exact compatibility disposition per family; shared method names remain insufficient. |
| C10 / policy gate | 112 private classes, 563 private methods, and 16 resolved prohibited cross-owner calls; no call remains in the discretionary unresolved bucket. Class exports and method visibility are distinct. | Exact call-site inventory and focused owner tests; cross-owner calls use the existing deterministic rule. | `migration.v2.harness.compiler`, `migration.v2.harness.conformance`, and `migration.v2.workflows.control-ingress` are each `closed_human_accepted_pass`. Compiler, parser/ownership/strict, and dispatch corrections must respectively consume those accepted results. Inactive architecture-conformance/module-decomposition phases grant no implementation authority. | Phase 2 may encode the selected Option B rule after activation. Phase 4 corrections remain bounded by package and accepted Task; descriptive class naming does not authorize exports or a repository-wide method rename. |

## Selected normative policy

The human-authorized Option B selection is now synchronized in `AGENTS.md`, the source
documentation standard, Architecture v2 repository layout, and strict-conformance
migration plan:

1. **Supported import classification.** Support requires a deliberate package or
   subpackage export, accepted contract evidence, and synchronized public
   documentation for the exact route. Importability, an underscore, `__all__`, or a
   maintained deep import is insufficient. An accepted route receives its own bounded
   compatibility disposition before removal or relocation.
2. **Non-exported named owners.** Top-level implementation classes use descriptive
   non-underscore names while remaining unsupported unless deliberately exported and
   accepted. A class name is not a package-surface decision.
3. **Method visibility.** Concise owner-local private mechanical methods remain
   permitted. Package exports cannot control method visibility, so private methods are
   not mechanically renamed. Cross-object private calls and private ownership of
   public, scientific, numerical, comparison, compatibility, or validation policy are
   prohibited.

The following inventory proposals remain non-normative migration design inputs:

4. **Callable conformance.** A future report-only inspector and ratchet can require
   each non-entry-point callable to cite an explicit owner while retaining exact typed
   framework hooks. Counts alone are not failures.
5. **Metric status.** Line count, fan-in/fan-out, export breadth, and naming remain
   prioritization signals until a separately accepted deterministic rule exists.
6. **Abstraction selection.** Composition remains preferred; Protocol or ABC changes
   require demonstrated substitution and compatibility evidence.
7. **Dependency graph views.** Concrete findings identify lexical,
   runtime-unconditional, or package-facade-excluded views rather than assuming one
   global graph interpretation.

## Resolved selection and remaining deferrals

- **D1 — resolved architecture policy:** Option B governs supported-import curation.
  The 985 individual export rows and exact non-export rows remain unclassified inputs
  for future bounded application. Each may later be preserved, deprecated, aliased,
  or explicitly retired under its accepted contracts; that disposition does not
  reopen Option B.
- **D2 — resolved class-naming policy:** Top-level implementation classes use
  descriptive non-underscore names but remain unsupported unless deliberately
  exported and accepted.
- **D3 — resolved method policy:** Owner-local private mechanical methods remain
  permitted; cross-object private calls and private public/scientific/numerical policy
  ownership are prohibited. Package exports do not control method visibility, and a
  blanket rename is not authorized.
- **D4 — deterministic metrics (deferred):** No enforceable size, coupling, or export
  threshold is selected.
- **D5 — graph semantics (deferred):** Each future finding identifies its applicable
  graph view; no repository-wide normative view is selected.
- **D6 — abstraction compatibility (deferred):** Existing accepted Protocols and
  `ParameterStudyRefiner` remain unchanged; later individual proposals retain their
  compatibility and human-decision requirements.
- **D7 — C2 architecture (conditional):** A separate Architecture v2 decision is
  required only if a future proposal adds an extra structural module or changes
  structural/replay ownership. In-place cleanup does not trigger D7.

Nothing here authorizes a production change, route reclassification, source move,
breaking change, or abstraction rewrite. Human acceptance applies to the bounded
Phase 1 result only; production work and successor activation remain separate.
