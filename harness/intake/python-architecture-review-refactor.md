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

## Boundaries

This recording alone authorizes managed planning state only. It does not authorize
source refactoring, public-contract breakage, dependency changes, protected execution,
scientific execution, scientific interpretation, release activity, or automatic
successor activation. The later verbatim human response above authorizes only the
exact validated managed-closeout commit and configured-upstream push.
