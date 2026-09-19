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

## Boundaries

This recording alone authorizes only the managed state and bounded operations stated
in each applicable section above. It does not authorize public-contract breakage,
dependency changes, protected execution, scientific execution, scientific
interpretation, release activity, or automatic successor activation. The accepted
production-facts, callable/private-rules, and dependency-graph-views responses
authorize only their respective exact validated managed-closeout commits and
configured-upstream pushes. None authorizes successor activation.
