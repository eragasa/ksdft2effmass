# P1 — Project-owned CPN contract

Status: closed as human-accepted `PASS` through `P1-HC03` on 2026-08-04; no successor launched

## Authority

The human PI accepted P0A as `PASS`, required its checkpoint closeout to remain
separate from successor launch, and then explicitly authorized this P1 task as
the first production-code task after successful P0A closeout validation. That
validation passed. P2--P11 remain blocked and unauthorized.

## Objective

Deliver an executable, backend-neutral, project-owned Colored Petri Net (CPN)
contract in production source with focused tests. Define language-neutral
project-owned token colors, places, transitions, arcs/inscriptions, pure guards,
multiset markings, scope-explicit outcomes/terminal states, structured errors,
and Rust-translatable persistence fields.

The contract must encode

$$
\mathcal N=(P,T,A,\Sigma,C,G,E,I),
$$

multiple tokens, synchronization, retries, recovery, repeated transition
execution and cyclic net execution, authorizations, provenance, and parent-child
lineage. Repeated execution does not imply automatic `iteration_index`
advancement: version 1 performs no arithmetic, and the index is explicitly
supplied or copied routing data. It must not expose or
inherit from SNAKES classes, reduce markings to Booleans, serialize lambdas, or
create a multi-engine framework.

## Task-specific ownership and launch preflight

The fail-closed ownership declaration is
`.pi/evidence/backend-neutral-cpn-P1-contract/task-ownership.json`. It assigns
separate implementation, test, and documentation writers, independent
architecture and integration reviewers, the public-export inventory source,
exact class-module policy, explicit exceptions, non-class gate ownership, and
the required completion validator.

The controlling chain must run

```bash
python .pi/task-ownership/validate_task_ownership.py --task P1
```

before implementation or resumed corrective implementation. A missing or
invalid ownership manifest blocks launch. The declared test-ownership validator
must pass before independent review. Passing either control-plane validator is
administrative/software-evidence validation only; it did not resolve the former
numeric checkpoints and does not grant P1 acceptance or P2--P11 authorization.

## Authorized implementation scope

- production Python source under `python/src/ksdft2effmass/workflows/cpn/`;
- immutable DataObjects/ResultObjects for the neutral contract and explicit
  ActionObjects for contract validation and executable marking/transition
  behavior owned by P1;
- fixed, deterministic, Rust-translatable public contract fields and enums;
- focused software-verification tests under the maintained VVUQ hierarchy;
- language-neutral schemas and valid/invalid fixtures required to expose the
  contract independently of Python;
- Markdown concept/API documentation and Sphinx navigation for implemented
  behavior;
- public package imports, source documentation, read-only review, parent
  verification, and final human-acceptance evidence.

## Exclusions

P1 must not implement or begin:

- a SNAKES engine adapter or any other engine adapter;
- authoritative marking persistence, a persistence repository, or pickle;
- external-tool execution, scheduler/subprocess behavior, QE, ABINIT, or
  Wannier90 integration;
- a concrete scientific workflow or backend/scientific payload model;
- P2 provenance/tool-capability objects or any P2--P11 task scope;
- untrusted expression evaluation, dynamically supplied Python callables, or
  serialized lambdas.

The neutral contract may represent durable persistence fields and explicit
request/result, authorization, retry, provenance, and lineage identifiers, but
must not perform their later-task storage or external execution.

## Required evidence and acceptance gates

- production contract source is executable and importable without SNAKES;
- markings preserve token multiplicity and deterministic token identity/order;
- transition enablement and firing cover multiple inputs, synchronization,
  pure declarative guards/inscriptions, token consumption, and token production;
- retry, failure/recovery, repeated and cyclic firing, authorization, provenance,
  and parent-child lineage states are representable without Boolean completion
  collapse; `iteration_index` is explicitly supplied or copied and is not
  advanced arithmetically by the version-1 expression language;
- accepted/rejected/failed/blocked outcomes carry explicit scope and terminality;
- invalid definitions, markings, bindings, and firings produce documented
  structured errors;
- public Python types, language-neutral schemas, fixtures, tests, documentation,
  and intended Rust mappings agree;
- no production module imports SNAKES and no SNAKES runtime object enters the
  public contract or durable fields;
- focused software-verification tests, formatter, linter, type checker, public
  import smoke test, fixture/schema validation, and Sphinx warnings-as-errors
  pass;
- independent architecture, test/documentation, and integration reviews have no
  unresolved material findings;
- parent verification confirms scope containment and keeps P2--P11 and
  production/scientific execution blocked;
- a new human final-acceptance checkpoint is required to close P1.

Passing P1 gates is software-verification and contract-conformance evidence. It
is not numerical verification, scientific validation, uncertainty
quantification, SNAKES-adapter verification, persistence verification, or
scientific-execution authorization.

## Implementation progress

The sole-writer implementation produced the authorized neutral production
package, focused software-verification and integration tests, version-1 schemas
and synthetic fixtures, public API/concept/verification documentation, and exact
Sphinx navigation/configuration additions. The implementation supports complete
multiset markings, pure declarative guards and inscriptions, deterministic
binding enumeration, read/consume/output firing, synchronization, explicit
retry/recovery/iteration routing state, scoped outcomes, and structured errors
without SNAKES or later-task objects. Repeated firing copies explicitly supplied
iteration routing data; it does not compute `current + 1`.

Implementation and the deterministic correction passes are complete but P1
remains open. Retained initial and correction reviews record the discovered
findings and their disposition. Final pre-checkpoint architecture and integration
re-reviews identified two protected public-contract blockers: tagged `REAL` wire
canonicalization and fixed integer width/overflow semantics. The human PI later
resolved them through `P1-HC01` Option A and `P1-HC02` Option B; the bounded
numeric correction and focused evidence are now implemented pending final review,
parent verification, and separate human acceptance.

## Deterministic test-ownership and completeness corrections

While the numeric decision remains blocked, the human authorized two bounded
nonnumeric corrections. The first replaced six combined workflow modules with
one-class object modules and temporarily moved eight package/schema/fixture/
import/isolation gates to a deterministic evidence script. Historical reviews
and their old paths/counts remain unchanged and explicitly superseded.

The later completeness correction restores `SV-CPN-023` and
`SV-CPN-027`--`SV-CPN-033` to five artifact-owned integration modules under
ordinary pytest. The one-class rule applies only to object-level modules. The
maintained surface now contains 32 exact one-class modules, five artifact-owned
modules, 88 test functions/evidence IDs (`SV-CPN-001`--`SV-CPN-088`), and 91
collected parameter cases. Eighteen public constructor-invariant owners gained
dedicated modules (`SV-CPN-040`--`SV-CPN-057`); deterministic missing branches
for nine existing owners gained `SV-CPN-058`--`SV-CPN-079`; resolved numeric
contract evidence occupies `SV-CPN-080`--`SV-CPN-088`.

The ownership manifest records current owners and complete predecessor mappings,
including old pytest -> temporary deterministic gate -> restored pytest nodes.
`test-completeness-matrix.json` classifies `SV-CPN-040`--`SV-CPN-079` as
`DETERMINISTIC_NOW` and `SV-CPN-080`--`SV-CPN-088` as resolved by
`P1-HC01` Option A plus `P1-HC02` Option B. No numeric test branch remains blocked
by those resolved checkpoints.
`contract_gates.py` now invokes the artifact pytest modules and is not their
authoritative implementation. The ownership validator audits, but does not
replace, maintained pytest evidence.

The earlier nonnumeric ownership correction did not change production behavior,
schemas, fixtures, dependencies, or the then-unresolved numeric contract. The
later separately authorized numeric correction owns those bounded surfaces.
Passing either evidence set does not grant P1 acceptance or authorize P2--P11.

## Nonnumeric iteration-semantics correction

The human PI clarified that repeated transition execution and cyclic CPN
execution are independent of automatic index advancement. The version-1
expression language has no arithmetic operation and does not compute
`iteration_index = current + 1`; `iteration_index` is explicitly supplied or
copied routing data and may repeat while marking revision advances. Tests and
maintained documentation now make that distinction explicit. Any future
automatic advancement requires ownership by a future ActionObject or a
separately authorized expression-language revision.

The closed P0A replay retains its accepted historical expectations. Its failure
against later authorized P1 documentation pages is expectation drift between
snapshots, not a P1 failure. Accepted P0A evidence remains unchanged; exact
replay requires the corresponding historical tree, while present-tree execution
must report the drift separately.

## Resolved numeric-contract checkpoint

The human PI selected Option A for `P1-HC01` on 2026-08-04. The authorized
version-1 contract uses IEEE-754 binary64 `REAL` canonicalization and signed i64
`ContractValue` integer bounds. The later `P1-HC02` decision narrows every
expression-visible nonnegative control field to `[0, 2^63 - 1]`, with matching
JSON-Schema limits and structured revision overflow at `2^63 - 1`.
The correction may now update the assigned production, test, schema/fixture,
documentation, and evidence surfaces, followed by independent review and parent
verification.

The implementation writer completed a safe partial subset, then discovered that
expression-visible upper-u64 controls could not pass through signed
`ContractValue.INTEGER`. The human PI resolved `P1-HC02` as Option B: all P1 v1
expression-visible controls—including revisions and iteration indices—are
bounded to `2^63 - 1`, and structured revision overflow occurs at that maximum.
No unsigned `ContractValue` kind is added. If P2 later needs true u64 artifact
sizes or counters, it may introduce explicitly typed fields under separate P2
authority.

The human PI granted final P1 acceptance as Option A through `P1-HC03` on
2026-08-04 after final reviews and parent verification passed. P1 is closed as
human-accepted `PASS`. This acceptance does not automatically launch P2 and does
not authorize arithmetic
`iteration_index` advancement, SNAKES adaptation, persistence, P2--P11,
production/scientific execution, or any external calculation.

## Post-close documentation-governance maintenance

`EVIDENCE-DOC-1` is separately authorized bounded maintenance of the reusable
test-evidence documentation convention. Resolved `EVIDENCE-DOC-1-HC02` Option B
extends the pilots to all 32 class-owned modules and 78 evidence owners in the
P1 CPN workflow test directory, with complete helper documentation and function-
node traceability. This structural migration does not reopen P1, alter
`P1-HC01`--`P1-HC03`, or change any P1 production, schema, fixture, assertion,
tolerance, or scientific meaning. The architecture-reviewed artifact follow-up
uses five exact descriptive `workflow_cpn` filenames with synchronized test
ownership, node maps, control-plane gate replay paths, completeness records, and
migration inventory. Old filenames retained in accepted P1 reviews and explicit
predecessor mappings are historical. `SV-CPN-028` remains one accepted
conjunctive nonnumeric Python/JSON boundary agreement with no split or new IDs;
numeric agreement remains separately owned by `SV-CPN-087` and `SV-CPN-088`.
The EVIDENCE-DOC-1 completion gate now recognizes the manifest-declared
artifact-owned versus boundary-owned integration contracts. The two verification-documentation pages and both current checksum catalogs
are synchronized with the migrated filenames and complete current module
surface. Obsolete integration paths remain only in accepted historical reviews,
baselines, or explicit predecessor mappings. P1 remains closed as human-accepted
`PASS`; this maintenance still requires
independent semantic review and human final acceptance and does not launch
P2--P11.
