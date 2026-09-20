# Python architecture review and refactor

## Human request

Create one parent managed software Task for a comprehensive Python architecture
review and refactor. Its immediate children are substantive phases. More narrowly
scoped descendants of those phase Tasks will be determined later from the review;
this recording does not speculate about or activate those future Tasks.

The requested direction is to:

- break up large files and classes along cohesive module and submodule boundaries;
- improve conformance with the repository's DataObject, ResultObject, ActionObject,
  serializer, Workflow, typing, documentation, and dependency-direction rules;
- remove dangling module-level behavior;
- eliminate private class and method ownership in favor of explicit named owners,
  while controlling the supported public API through deliberate package and
  subpackage imports rather than re-exporting every defined class;
- strengthen separation of concerns; and
- identify justified abstract-class candidates without creating nominal hierarchy
  solely to label otherwise unrelated classes.

## Resolved Phase 1 policy selection

The verbatim human response was:

> recommendation authorized

This response is normalized as **Option B**. Supported Python imports are curated route
by route through deliberate package/subpackage exports backed by accepted contract
evidence and synchronized public documentation; importability or `__all__` alone does
not establish support. Top-level implementation classes use descriptive
non-underscore names but remain unsupported unless deliberately exported and accepted.
Concise owner-local private mechanical methods remain permitted. Cross-object private
calls and private ownership of public, scientific, or numerical policy are prohibited.
Package imports cannot control method visibility, so private methods are not
mechanically renamed into public members.

The selected architecture policy does not itself classify any current route or
authorize a breaking change. Existing broad facades, private top-level classes, and
cross-object calls remain bounded migration inputs. Exact route dispositions are
future applications of Option B under the applicable accepted contracts and activated
Task; they do not reopen the Option B architecture choice.

## Human acceptance and closeout

The verbatim human acceptance response was:

> accepted and closeout authorized

This response is normalized as human acceptance of the completed Phase 1 inventory,
selected Option B policy, candidate register, clean Sphinx dummy/HTML gates, and
reported deferrals and limitations. It also authorizes the managed administrative
closeout commit and configured-upstream push required by repository policy. It does
not accept or authorize production refactoring, scientific validation, protected
execution, release activity, or successor activation.

## Immediate disposition

Phase 1 is human-accepted and closed through the authorized administrative closeout.
The parent and five successor phase Tasks remain inactive and require separate
explicit activation. No production implementation is started, and no successor or
future descendant is activated automatically.

This task tree does not supersede accepted Architecture v2 package ownership,
existing managed Tasks, accepted public or wire contracts, or retained evidence. A
future phase must identify overlaps and consume accepted results rather than create a
second authority for the same behavior.

## Preliminary inventory

A read-only AST inventory identified the following review signals:

- `python/src/ksdft2effmass/workflows/persistence.py` has 10,503 lines, including a
  7,143-line `WorkflowRunSerializer`;
- `workflows/runs/records.py`, `workflows/runs/replay.py`, and
  `integration/quantum_espresso/effects.py` each exceed 2,500 lines;
- maintained source contains 188 module-level callables across 52 modules, including
  exact command and framework entry points that require separate classification;
- maintained source contains 112 underscore-prefixed top-level classes and many
  owner-local private methods requiring semantic classification rather than blind
  renaming;
- several package roots expose more than one hundred names; and
- the static maintained-source module graph showed no import cycle in the initial
  scan.

These observations are prioritization inputs, not conformance findings or proof that a
particular split is correct. Phase 1 owns the reproducible inventory, policy decisions,
and review criteria.

## Phase structure

1. **Inventory and policy** — establish the reproducible architecture inventory,
   supported-import contract, compatibility posture, exact callable/private-owner
   policy, separation criteria, and abstraction criteria.
2. **Architecture conformance** — implement explicit-input production-source
   architecture inspection and a controlled migration ratchet without automatic
   rewriting.
3. **Public import boundaries** — establish deliberate package/subpackage supported
   imports and migrate over-broad export surfaces under explicit compatibility
   decisions.
4. **Module decomposition** — split overloaded modules and classes by cohesive domain
   responsibility and move behavior to its proper explicit owner.
5. **Abstraction design** — evaluate demonstrated polymorphism and introduce, retain,
   replace, or reject Protocol and abstract-class boundaries with contract evidence.
6. **Aggregate verification** — verify the complete accepted refactor, documentation,
   public imports, typing, architecture rules, and residual limitations.

Each phase may later receive package-, module-, or contract-specific child Tasks only
after its exact decomposition is supported by current evidence and separately recorded.
Parent-child relationships express containment; prerequisite fields express only the
ordered phase results required by later work.

## Selected policy consequences and remaining deferrals

- Route compatibility is applied individually under Option B. A later bounded route
  classification may preserve, deprecate, alias, or explicitly retire an exact route;
  package-set evidence cannot decide for every member.
- Descriptive non-underscore names are the target for top-level implementation
  classes, without exporting them automatically.
- Owner-local private mechanical methods may remain private. Cross-object private
  calls are prohibited, as is private ownership of public/scientific/numerical policy.
  Package exports cannot control method visibility, and blanket private-method rename
  is not authorized.
- D4 remains deferred: no deterministic size, coupling, fan-in/fan-out, or export
  threshold is selected.
- D5 remains deferred: a future concrete graph finding must identify its lexical,
  runtime-unconditional, or facade-excluded view.
- D6 remains deferred: abstraction changes still require demonstrated substitution and
  their own compatibility evidence.
- D7 remains conditional: it arises only if a future proposal moves the structural
  validator to an extra module or changes structural/replay ownership.

## Phase 2 planning and decomposition

An adversarial review recommended activating Phase 2 only for managed planning and
recording four inactive implementation slices. The exact human response was:

> recommendation authorized

The selected slice DAG is:

1. `production-facts`, which also names the accepted Phase 1 Task as its prerequisite;
2. `callable-private-rules` and `dependency-graph-views`, each dependent only on
   `production-facts`; and
3. `ratchet-integration`, dependent on both rule slices.

This planning activation narrows supported-export agreement to neutral syntactic facts
or agreement with an explicitly supplied accepted route contract. All 985 route
support dispositions remain unclassified and Phase 3-owned. Every future candidate
rule must be identified as deterministic enforcement, deterministic structural
observation, or a review-only signal. Semantic ownership of public, scientific,
numerical, comparison, compatibility, or validation policy is review-only absent
explicit semantic metadata. The accepted version-one `python.test-evidence` subject
is preserved; future production inspection is a sibling subject/profile, not a
mutation of that contract.

### Phase 2 planning acceptance

The human was asked exactly:

> Do you accept the Phase 2 planning/decomposition result? Acceptance will not activate an implementation slice.

The exact human response was:

> yes

This response is normalized as acceptance of the bounded Phase 2
planning/decomposition result. Phase 2 remains selected with status `planning`. The
architecture parent, all four implementation children, and Phases 3-6 remain
inactive. This acceptance does not activate implementation, authorize production
source or test changes, authorize export, dependency, wire, or public-contract
mutation, authorize staging, commit, or push, or establish software verification,
numerical verification, scientific validation, or uncertainty quantification. A
next child-activation decision remains separate.

### Production-facts child activation

The exact subsequent human response was:

> recommendation authorized

This response activates only
`python.architecture-refactor.architecture-conformance.production-facts` with bounded
implementation authority for its declared source, tests, controlled resources,
architecture documentation, ownership, activation, and generated projection paths.
The child supplies explicit-input immutable neutral Python production-source facts as
a sibling of the accepted `python.test-evidence` contract. Under the repository's
single-active-Task invariant, Phase 2 is deferred between children while this child is
separately selected and explicitly authorized for ongoing bounded implementation with
Task status `planning`. The exact selection receipt remains authority for this managed
operation rather than implying inactivity or completion. The parent is not closed, the
other three children and Phases 3-6 remain inactive, and automatic successor
activation is false. This activation does not authorize policy findings, ambient
source discovery, source repair, package exports, accepted version-one behavior
changes, dependencies, wire or supported public contracts, scientific code,
protected execution, publication edits, staging, commit, push, human acceptance,
numerical verification, scientific validation, or uncertainty quantification.

### Production-facts acceptance and managed closeout

The human was asked exactly:

> Do you accept this result and authorize managed administrative closeout? Closeout will commit and push only this slice, leave siblings inactive, and exclude the manuscript modification.

The exact human response was:

> accepted and authorized

This response is normalized as human acceptance of the bounded production-facts
software-verification result and authorization of one validated managed administrative
closeout commit and configured-upstream push for only the accepted ownership boundary.
The accepted result establishes explicit-input neutral Python syntax facts,
deterministic represented failures and ordering, preserved accepted version-one
conformance behavior, maintained software-verification evidence, documentation
agreement, and deterministic Harness projections. It does not establish runtime
semantic completeness, architecture-policy findings, numerical verification,
scientific validation, uncertainty quantification, protected execution authority,
release status, or successor authority. The known repository-wide mypy
duplicate-conftest limitation remains in unchanged unrelated files; affected strict
mypy passes.

The production-facts child is `closed_human_accepted_pass`. Task selection is cleared,
Phase 2 remains `deferred_between_children` and not closed, the other three children
and Phases 3-6 remain inactive, and automatic successor activation remains false. The
closeout explicitly excludes the unrelated manuscript modification.

### Callable/private-rules child activation

The exact subsequent human response was:

> recommendation authorized

This response selects only
`python.architecture-refactor.architecture-conformance.callable-private-rules` with
receipt
`human-selection.python.architecture-refactor.architecture-conformance.callable-private-rules`
and authorizes ongoing bounded implementation of its declared explicit-input rule
scope. The child remains `planning` because the unrelated research Task retains the
sole durable `active` status. Phase 2 remains `deferred_between_children`,
production-facts remains closed, dependency-graph-views and ratchet-integration remain
inactive, Phases 3-6 remain inactive, and automatic successor activation is false.

The implementation may consume immutable accepted production facts, explicit exact
hook exceptions, and controlled maintained fixtures. It may produce only neutral
read-only violations, structural observations, and review-only signals. This
activation does not authorize source repair, route or export disposition, dependency
graph decisions, accepted production-facts changes, dependency or wire changes,
scientific claims, staging, commit, push, human acceptance, or successor activation.

### Callable/private-rules acceptance and managed closeout

The human was asked exactly:

> Do you accept python.architecture-refactor.architecture-conformance.callable-private-rules and authorize managed administrative closeout (mark closed, validate, commit, push, and verify the remote commit), without activating a successor?

The exact human response was:

> yes

This response is normalized as human acceptance of the bounded callable/private-rules
software-verification result and authorization of one validated managed administrative
closeout commit and configured-upstream push for only the accepted ownership boundary.
The accepted result establishes canonical callable/private rule classifications, exact
framework-hook exceptions, deterministic dangling-callable and top-level
underscore-class findings, conservative private-call observations under accepted v1
facts, maintained software-verification evidence, documentation agreement, and
deterministic Harness projections. It does not establish non-self receiver binding,
general non-call private-attribute coverage, runtime dispatch completeness, semantic
ownership completeness, numerical verification, scientific validation, uncertainty
quantification, protected execution authority, release status, or successor authority.
The known repository-wide mypy duplicate-conftest limitation remains in unchanged
unrelated files; affected strict mypy passes.

The callable/private-rules child is `closed_human_accepted_pass`. Task selection is
cleared, Phase 2 remains `deferred_between_children` and not closed,
production-facts remains closed, dependency-graph-views and ratchet-integration remain
inactive, Phases 3-6 remain inactive, and automatic successor activation remains
false. The closeout explicitly excludes the unrelated manuscript modification.

### Dependency-graph-views child activation

The exact subsequent human response was:

> recommendation authorized

This response selects only
`python.architecture-refactor.architecture-conformance.dependency-graph-views` with
receipt
`human-selection.python.architecture-refactor.architecture-conformance.dependency-graph-views`
and authorizes ongoing bounded implementation of its declared explicit-input graph
scope. The child remains `planning` because the unrelated research Task retains the
sole durable `active` status. Phase 2 remains `deferred_between_children`,
production-facts and callable-private-rules remain closed, ratchet-integration remains
inactive, Phases 3-6 remain inactive, and automatic successor activation is false.

The implementation may consume immutable accepted production facts and explicit
accepted dependency contracts. It may derive only separately identified lexical,
runtime-unconditional, and package-facade-excluded dependency views with deterministic
strongly connected components and exact edge provenance. This activation does not
authorize a universal graph interpretation, source repair, route or export disposition,
dependency changes, accepted prerequisite changes, wire or public-contract changes,
scientific claims, staging, commit, push, human acceptance, or successor activation.

### Dependency-graph-views acceptance and managed closeout

The human was asked exactly:

> Do you accept python.architecture-refactor.architecture-conformance.dependency-graph-views and authorize managed administrative closeout—mark closed, validate, commit, push, and verify the remote commit—without activating a successor?

The exact human response was:

> accepted and closeout authorized

This response is normalized as human acceptance of the bounded dependency-graph-views
software-verification result and authorization of one validated managed administrative
closeout commit and configured-upstream push for only the accepted ownership boundary.
The accepted result establishes three explicitly identified syntax-derived graph views,
exact source-edge provenance, deterministic strongly connected components, fail-closed
exact-edge dependency-contract handling, maintained software-verification evidence,
documentation agreement, and deterministic Harness projections. It does not establish
runtime import success, a universal dependency meaning, large/deep-graph scalability,
numerical verification, scientific validation, uncertainty quantification, protected
execution authority, release status, or successor authority.

The dependency-graph-views child is `closed_human_accepted_pass`. Task selection is
cleared, Phase 2 remains `deferred_between_children` and not closed, production-facts
and callable-private-rules remain closed, ratchet-integration remains inactive, Phases
3-6 remain inactive, and automatic successor activation remains false. The closeout
explicitly excludes the unrelated manuscript modification.

### Ratchet-integration child activation

The exact subsequent human response was:

> recommendation authorized

This response selects only
`python.architecture-refactor.architecture-conformance.ratchet-integration` with
receipt
`human-selection.python.architecture-refactor.architecture-conformance.ratchet-integration`
and authorizes ongoing bounded implementation of its declared production-conformance
ratchet scope. The child remains `planning` because the unrelated research Task
retains the sole durable `active` status. Phase 2 remains
`deferred_between_children`; production-facts, callable-private-rules, and
dependency-graph-views remain closed; Phases 3-6 remain inactive; and automatic
successor activation is false.

The implementation may consume the three accepted Phase 2 prerequisite capabilities,
an explicit versioned production policy/profile, and an immutable content-identified
inherited baseline. It may provide bounded deterministic CLI/report integration that
keeps inherited findings visible and rejects newly introduced deterministic
violations. This activation does not authorize mutable or permanent waivers, route
support classification, source repair, exports, dependency changes, accepted
prerequisite changes, wire or public-contract changes, scientific claims, staging,
commit, push, human acceptance, Phase 3 activation, or successor activation.

The bounded implementation adds the distinct version-one production policy and
ratchet profile, exact content-identified configuration and inherited baseline,
aggregate composition of all four Phase 2 slices, and a bounded explicit-input CLI
report. Inherited deterministic findings remain visible historical comparison inputs;
they are not approvals or waivers. Newly introduced deterministic violations fail.
Identity, profile, configuration, baseline, and ambiguous-duplicate mismatches fail
closed. Maintained tests and validators establish only bounded structural software
verification. This provisional implementation does not change the child status from
`planning`, human-accept or close Phase 2d or Phase 2, classify support routes, repair
source, or activate Phase 3 or any successor.

### Ratchet-integration acceptance and managed closeout

The human was asked exactly:

> Do you accept python.architecture-refactor.architecture-conformance.ratchet-integration and authorize managed administrative closeout—mark it closed, run only lightweight closeout-state/projection checks, commit, push, and verify the remote commit—without activating Phase 3 or any successor?

The exact human response was:

> accept and closeout authorized

This response is normalized as human acceptance of the bounded Phase 2d structural
software-verification result and authorization of one validated managed administrative
closeout commit and configured-upstream push for only the accepted ownership boundary.
The accepted result establishes a distinct versioned production policy/profile, exact
content-identified configuration and inherited baseline inputs, visible non-waiving
inherited findings, fail-closed new deterministic violations, bounded deterministic
CLI/report behavior, and aggregate verification of all four Phase 2 slices. It does
not establish repository-wide architecture conformance, runtime semantic completeness,
route support dispositions, scientific validation, uncertainty quantification,
protected execution authority, release status, Phase 2 parent acceptance, or
successor authority.

The ratchet-integration child is `closed_human_accepted_pass`. Task selection is
cleared, Phase 2 remains `deferred_between_children` and not closed, all four children
are closed, Phases 3-6 remain inactive, and automatic successor activation remains
false. The closeout explicitly excludes the unrelated manuscript modification.

### Phase 2 aggregate closeout review selection

The exact subsequent human response was:

> recommendation authorized

This response selects only the Phase 2 parent
`python.architecture-refactor.architecture-conformance` with receipt
`human-selection.python.architecture-refactor.architecture-conformance` and status
`planning` for bounded aggregate closeout review of its four already accepted
children. It authorizes only parent, selection, intake, ownership-validator, and
generated-state reconciliation plus lightweight aggregate status, projection, Harness,
formatting, typing, and whitespace checks. It does not reopen or rerun child
implementation, authorize new source or evidence behavior, human-accept or close Phase
2, or activate Phase 3 or any successor. All four children remain closed, Phases 3-6
remain inactive, and automatic successor activation is false.

### Phase 2 aggregate acceptance and managed closeout

The human was asked exactly:

> Do you accept python.architecture-refactor.architecture-conformance and authorize managed administrative closeout—mark Phase 2 closed, run lightweight closeout-state/projection checks, commit, push, and verify the remote commit—without activating Phase 3 or any successor?

The exact human response was:

> yes

This response is normalized as human acceptance of the bounded Phase 2 aggregate
result and authorization of one validated managed administrative closeout commit and
configured-upstream push for only the accepted ownership boundary. Phase 2 and all
four children are `closed_human_accepted_pass`; task selection is cleared; Phases 3-6
remain inactive; and automatic successor activation remains false. The accepted result
establishes only the bounded Phase 2 production-source architecture-conformance
contracts and their software-verification evidence. It does not establish broader
repository-wide architecture conformance, runtime semantic completeness, route support
dispositions, scientific validation, release status, or successor authority. The
closeout explicitly excludes the unrelated manuscript modification.

### Phase 3 adversarial planning selection

The exact subsequent human response was:

> recommendation authorized under an adverserial planning

This response selects `python.architecture-refactor.public-import-boundaries` with
receipt `human-selection.python.architecture-refactor.public-import-boundaries` and
status `planning` after its accepted Phase 2 prerequisite. It authorizes bounded
read-only inspection of the accepted route inventory, package exports, maintained
import consumers, documentation, compatibility evidence, and Phase 2 conformance
contracts; adversarial challenge of planning assumptions and proposed boundaries; and
reconciliation of the Phase 3 Task, intake, ownership, planning validator, generated
projections, and narrowly scoped planning artifacts. It does not classify a route by
inference, change production source, tests, exports, supported APIs, dependencies, or
documentation contracts, activate an implementation child or successor, provide human
acceptance, or authorize commit or push. Package-specific implementation children
remain deferred until the adversarial plan is reviewed and explicitly accepted;
automatic successor activation remains false.

#### Phase 3 adversarial planning result

Read-only workflow `34351631-3be1-45b3-9c9b-be6f7db1a369` produced an initial
architecture plan, an independent assumption and policy challenge, an independent
integration and compatibility challenge, and a corrected synthesis. Both initial
reviews reported `CHANGES_REQUIRED`. The synthesis corrected every evidence-backed
`MUST_FIX` finding and reports `NO_BLOCKING_FINDINGS`; its sole
`SAFE_TO_DEFER` item is installed-wheel PEP 561 typing, which is excluded from the
Phase 3 claim unless separately decided.

The corrected maintained plan is
`harness/reports/python-public-import-boundaries-plan.md`. It:

- preserves the 985 Phase 1 route records as immutable predecessor lineage rather
  than treating them as an exhaustive accessible-namespace inventory;
- adds separately keyed neutral facts for non-`__all__` package bindings, deep routes,
  maintained consumers, documentation, and proposed new routes;
- separates support status from compatibility disposition;
- gives all 35 package surfaces and all ten zero-route boundaries explicit ownership;
- separates a neutral current-fact foundation, 21 cohesive route-disposition units,
  file-level mutation partitioning, conditional implementation, and aggregate
  verification; and
- restricts dependency claims to accepted contracts for exact named graph views.

Only
`python.architecture-refactor.public-import-boundaries.current-fact-foundation` is
recorded now, with status `inactive`. The 21 disposition units, mutation partition,
conditional implementation children, and aggregate verifier remain proposed planning
units rather than activated Tasks. This preserves the rule against speculative
successor activation and permits the neutral prerequisite to refresh the stale
consumer and whole-source facts before exact later Task boundaries are recorded.

#### Phase 3 plan acceptance and F0 activation

The human was offered this recommendation:

> accept the corrected plan, close out and push this planning boundary, then activate F0 only

with the exact suggested response:

> Accept the corrected Phase 3 plan, authorize its validated managed planning closeout commit and push, and activate F0 only. Keep D1–D21, M1, all implementation children, V1, and automatic successor activation inactive.

The exact human response was:

> recommendation authorized

This response is normalized as acceptance of the corrected bounded Phase 3
adversarial plan, authorization of one validated managed planning closeout commit and
configured-upstream push for its exact boundary, and separate implementation
activation of only
`python.architecture-refactor.public-import-boundaries.current-fact-foundation`.
The Phase 3 parent moves to `deferred_between_children`; F0 is selected with status
`planning`; D1–D21, M1, all implementation children, V1, Phase 4, and automatic
successor activation remain inactive. This acceptance does not classify any route,
decide compatibility, accept an F0 result, authorize F0 result closeout, or establish
numerical verification, scientific validation, uncertainty quantification, release,
or publication status. The planning closeout excludes the unrelated manuscript
modification.

#### F0 provisional implementation result

The selected F0 implementation provides:

- `foundation-selection.tsv`, an authored explicit selection of 1,064 inputs;
- `foundation-inputs.json`, the canonical content-identified input manifest;
- `foundation.json`, the deterministic neutral current-fact report;
- a standard-library-only task-local generator with no repository, current-directory,
  or Git discovery; and
- a validator that reproduces both JSON artifacts, rejects a changed selected-input
  identity, verifies tracked first-party Python selection coverage, and runs the
  applicable structural gates.

The provisional foundation retains 985 predecessor routes, 35 package surfaces, all
ten zero-route surfaces, 3,742 maintained first-party import observations, 738 imports
of non-initializer modules, 246 documentation citations, 469 raw unadjudicated
authority citations, six exact accepted Phase 2 lineage inputs, 216 current
production-fact outputs, all three named dependency-graph views, 430 separately keyed
supplemental candidates, and 35 fresh-interpreter package observations. Four runtime
observations represent `ModuleNotFoundError` instead of attributes because the
selected environment lacks already-declared optional or development packages:
`ksdft2effmass.harness.pi.local`, `.local.control`, and `.local.dbcontrol` lack
`jsonschema`, while `ksdft2effmass.operators` lacks `numpy`. No dependency is added or
installed. These failures are explicit bounded environment observations, not support
or compatibility conclusions.

The generator and report do not classify a route, modify an initializer or consumer,
create a production parser, alter the accepted Phase 1 inventory, or extend Phase 2
claims. F0 remains selected with status `planning`; the provisional result is not
human accepted, its closeout is not authorized, and no disposition unit is active.

##### F0 independent review and authorized correction

Independent workflow `057f50f4-0dd4-4b95-9cd2-949f747d7b60` performed architecture
and integration reviews. Both reviewers reported `CHANGES_REQUIRED`. Their
nonduplicated blockers were incomplete authority/Phase 2 and public-documentation
inputs, an insufficiently closed and independently validated report shape, malformed
and unresolved initializer origins, unbound runtime environment and nonmutation,
missing accepted Phase 1 identity anchoring, output/input aliasing, and an inaccurate
neutral-claim sentence. Existing fixture-placement debt was `SAFE_TO_DEFER` because F0
only inventories it.

The human was asked:

> Authorize one bounded F0 correction pass followed by focused architecture and integration re-review?

and responded exactly:

> recommendation authorized

The bounded correction:

- minimizes each predecessor row to an exact closed neutral shape and validates the
  complete report schema and cross-view counts independently;
- anchors the accepted Phase 1 inventory to SHA-256
  `fb180c5d8aa9ecd33a319d03a5795ab24343d9b2b553acac580ec452b5795c7e` and its
  accepted closeout commit, then checks all 35 initializer identities;
- resolves relative syntactic import targets absolutely, resolves every star binding
  to its accepted defining origin, and rejects unsupported `__all__` mutation or an
  unresolved star origin;
- includes all tracked API, concept, user-guide, verification, migration, and source-
  documentation pages under the accepted selection rule, occurrence columns, raw
  unadjudicated authority terms, and six identified accepted Phase 2 fact/view inputs;
- binds runtime observations to the interpreter bytes, implementation/version, and
  installed-distribution inventory; uses isolated no-bytecode probes in temporary
  directories; and rechecks all selected bytes afterward;
- rejects output/input aliases, preserves a pre-existing output on failure, and uses
  same-directory atomic replacement on success; and
- states accurately that inherited neutral fields and supplemental unknown states are
  retained while no new support conclusion or compatibility decision is adjudicated.

No dependency was installed, no source/API/documentation contract was changed, and no
route was classified. The corrected result awaited focused re-review; F0 remained
selected with status `planning`, closeout was not authorized, and no successor was
active.

##### F0 focused re-review and final authorized correction

Focused workflow `80ce73c9-9984-4d56-9990-0f02fb1f4173` returned
`CHANGES_REQUIRED`. It confirmed that documentation coverage, Phase 1 anchoring,
absolute import targets, output aliasing and atomicity, neutral claims, and runtime
isolation/nonmutation were corrected. Remaining deterministic blockers were absent
actual Phase 2 result instances, insufficiently closed recursive JSON and nested
cross-view validation, nontransitive defining origins, indirect or aliased `__all__`
mutation, and—under the stricter architecture reading—missing content identities for
runtime-loaded files.

The human authorized the recommendation for one final bounded correction pass and
focused architecture/integration re-review with the exact response:

> recommendation authorized

The final bounded correction:

- converts every generated report view through frozen closed records and serializes
  only those records, with exact nested variants and summary/cross-view invariants;
- executes the accepted Phase 2 production-source inspector on all 216 selected
  production modules and the accepted dependency analyzer for the lexical,
  runtime-unconditional, and package-facade-excluded views, retaining exact source
  identities without extending their claims;
- retains syntactic import targets while resolving first-party re-export chains to
  terminal defining origins and failing on cycles or missing bindings;
- rejects indirect `globals()`/`vars()` and aliased `__all__` access, with independent
  positive and negative probes;
- strictly rejects duplicate JSON keys and representative malformed accepted-anchor,
  runtime-variant, zero-surface, summary, and Phase 2 count mutations; and
- binds every runtime observation to content identities for all loaded file-backed
  modules while retaining isolated no-bytecode temporary-directory execution and
  selected-input nonmutation checks.

No dependency was installed and no route was classified. The result then underwent
the separately authorized focused re-review; F0 remained in `planning`, closeout was
not authorized, and no successor was active.

##### F0 adversarial remediation decomposition

Final focused workflow `c211e942-663c-4ede-941b-144b5ef7801b` still reported
`CHANGES_REQUIRED`: the closed domain and cross-view gate remained incomplete,
unrepresented `__all__` escapes remained, unreadable file-backed runtime modules could
still be omitted, and generated domain values still crossed builder boundaries as
recursive JSON representations.

The human requested that the remaining work be broken into a task list resolved by an
adversarial process. Read-only workflow `26bc43fb-bd8d-43f2-8116-85ad0b3103cc`
produced an initial decomposition, an independent assumption challenge, an independent
integration challenge, and the corrected finite synthesis maintained at
`harness/reports/python-public-import-foundation-remediation-plan.md`. The synthesis
reports `NO_BLOCKING_FINDINGS` and defines six serial children:

1. `closed-domain-contract`;
2. `typed-domain-construction`;
3. `initializer-acquisition-closure`;
4. `runtime-file-completeness`;
5. `adversarial-validation`; and
6. `aggregate-verification`.

The corrected sequence gives each remaining blocker exactly one correction owner,
reserves maintained malformed-state and fixed-boundary regression evidence for C5,
and permits only one final read-only architecture/integration round in C6. It also
moves the sole implementation-time generated-pair refresh after all three selected
task tools reach final bytes. There is no automatic repair or review loop.

The human was offered the exact recommendation to accept this corrected finite
decomposition and authorize one validated managed planning closeout that records C1-C6
and their schema-v2 ownership manifests as inactive children, commits and pushes only
that planning boundary, and keeps every child and successor inactive until separately
selected. The exact response was:

> recommendation authorized

This response is normalized as acceptance of the corrected finite F0 remediation
decomposition and authorization of that exact managed planning closeout. C1-C6 were
recorded inactive and required separate selection. No F0 result was human accepted,
and D1-D21, M1, I*, V1, Phase 4, and automatic successor activation remained
inactive. The unrelated manuscript modification remained excluded.

##### C1 closed-domain-contract selection

After the planning closeout was pushed and remotely verified, the human was asked to
authorize quiescing the F0 parent writer, moving F0 to `deferred_between_children`,
and selecting and activating only
`python.architecture-refactor.public-import-boundaries.current-fact-foundation.closed-domain-contract`,
while keeping C2-C6 and every Phase 3 successor inactive. The exact response was:

> recommendatio authorized

The response is unambiguous in context and is normalized as authorization of that
C1-only transition and bounded implementation. F0 is deferred between children; C1
alone is selected with status `planning`; C2-C6, D1-D21, M1, I*, V1, Phase 4, and
automatic successor activation remain inactive. This does not accept a C1 result,
authorize C2, or permit a route, dependency, public-contract, scientific, release, or
publication decision.

##### C1 acceptance and managed closeout

C1 implemented the closed immutable task-internal foundation domain and its cohesive
cross-view validation. Independent workflows
`82cc9aaf-c9cb-4472-b39e-81adad92b9ea` and
`36be95ec-7339-4ebf-90de-ee35fb04a700` reported deterministic defects in record-local
closure, exact package/star and lineage relations, canonical collections, and
serializer ownership. The human separately authorized the bounded correction
recommendations. The final recommendation authorized one strictly bounded correction
of the remaining deterministic findings, local C1 gates, and reporting without another
broad review loop.

The final result uses frozen closed records with exact discriminants and owner-local
invariants, canonical duplicate-free collections, exact accepted-inventory and
production-input identities, exact Phase 2 lineage categories and content identities,
serializer-owned runtime-environment identity, and one cohesive cross-view ActionObject
with independent mutual-reachability SCC validation. Canonical version-one represented
bytes are preserved. The completion gate passes Ruff, formatting, strict mypy for the
model and typed probe, direct-construction checks, and 26 adversarial malformed-state
probes. Ownership and whitespace checks also pass. These checks establish only the
bounded task-internal structural software contract; C2-C6 retain their separately
assigned acquisition, typed construction, runtime completeness, maintained generated
refresh, and aggregate verification responsibilities.

The exact human response was:

> acceptance and closeout authorized

This response is normalized as human acceptance of C1 and authorization of one
validated managed administrative closeout commit and configured-upstream push for only
the accepted C1 and administrative state boundary. C1 is
`closed_human_accepted_pass`; F0 remains `deferred_between_children`; task selection is
cleared; C2-C6, D1-D21, M1, I*, V1, Phase 4, and automatic successor activation remain
inactive. The maintained F0 generated pair is not refreshed, no route support or
compatibility disposition is made, and the unrelated manuscript modification remains
excluded.

## Boundaries

This recording alone authorizes only the managed state and bounded operations stated
in each applicable section above. It does not authorize public-contract breakage,
dependency changes, protected execution, scientific execution, scientific
interpretation, release activity, or automatic successor activation. The accepted
production-facts, callable/private-rules, dependency-graph-views,
ratchet-integration, Phase 2 aggregate, and Phase 3 planning responses authorize only
their respective exact validated managed-closeout commits and configured-upstream
pushes. The Phase 3 response additionally activates only F0. None authorizes D1–D21,
M1, a production or documentation-contract implementation child, V1, Phase 4, or any
automatic successor activation.
