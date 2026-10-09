# Numerical-oracle qualification standard

## Purpose and authority

This standard governs claim-bearing oracles used by maintained software-verification,
numerical-verification, scientific-validation, and uncertainty-quantification tests.
An oracle is a declared reference relation, value, dataset, or independent evaluation
route against which a quantity under test is compared. An oracle is evidence input; it
is not made trustworthy merely because a test calls it an oracle or because the test
passes.

This page owns repository evidence policy for oracle qualification. It does not replace:

- mathematical and physical definitions in `specification/`;
- scientific assumptions in `docs/research/`;
- computational provenance in `docs/computational/` and `calculations/`;
- test ownership and documentation rules in the
  [architecture documentation standard](index.md); or
- domain-specific acceptance authority.

Qualification establishes that an oracle is fit for one explicitly bounded evidence
claim. It does not establish scientific validation, uncertainty quantification, human
acceptance, or unrestricted reuse.

## Scope

A qualification record is required before maintained evidence relies on any
claim-bearing:

- analytic or algebraic numerical reference;
- manufactured solution;
- independently implemented numerical evaluator;
- cross-implementation conformance reference;
- retained calculation or encoded artifact used as an expected result;
- literature, benchmark, or empirical value;
- convergence-rate or asymptotic reference; or
- shared approximate-comparison reference.

A separate numerical-oracle record is not required for a direct exact software-contract
assertion whose authority is already the public contract, such as an enum member, field
name, exact exception type, immutable byte string, or declared serialization token.
Those assertions still require normal source, test, and provenance documentation.
Calling a fixture `expected`, `reference`, or `golden` does not decide its category.

## Evidence categories and qualification routes

| Oracle kind | Minimum qualification route | Evidence that remains separate |
|---|---|---|
| Exact analytic identity | Authoritative definition or complete repository derivation, assumptions, domain, special or limiting cases, implementation independence, and finite-precision analysis | Scientific validation, UQ, and human acceptance |
| Manufactured solution | Governing equation, independent substitution or residual check, boundary/initial conditions, units, represented space, and discretization boundary | Physical adequacy of the manufactured case |
| Numerical reference implementation | Independent algorithm or implementation, verification against analytic, higher-precision, or converged evidence, conditioning and convergence limits, and dependency audit | Validation of the physical parent model |
| Retained calculation or artifact | Authenticated bytes, producing route, software/input identity, decoding contract, relevant convergence status, and interpretation boundary | Conclusions not present in the retained evidence |
| Literature, benchmark, or empirical value | Primary source, pinpoint locator, units and convention alignment, uncertainty or tolerance, intended-use match, and license/provenance | Transfer to a different material, model, or regime |
| Asymptotic or convergence reference | Stated limit, refinement variable, expected order, pre-asymptotic exclusions, norm, fit procedure, and precision floor | Convergence outside the tested family |

An oracle may require more than one route. For example, a retained DFT value can require
artifact authentication, numerical convergence evidence, and scientific applicability.
Hashes establish byte identity only.

## Qualification contract

Every claim-bearing oracle entering qualification has one immutable, versioned identity
and a machine-readable record beneath the applicable `python/tests/**/resources/`
directory. The record begins as a candidate and does not become qualified merely by
existing. The future v1 record must contain at least:

| Field | Required meaning |
|---|---|
| `schema_version` | Qualification-record schema version |
| `oracle_id` | Stable semantic identity ending in an explicit oracle version |
| `kind` | Closed oracle kind from the accepted schema |
| `evidence_class` | Exact evidence class for which use is qualified |
| `claim` | One bounded statement supplied to consumer tests |
| `authoritative_definition` | Specification, equation IDs, primary source, or retained-artifact identity |
| `implementation` | Test-only evaluator/test node, or explicit `not_applicable` for a literal identity |
| `assumptions` | Mathematical, physical, representation, and provenance assumptions |
| `representation_contract` | State space, basis, gauge or frame, normalization, geometry, ordering, energy reference, and units, each explicit or `not_applicable` |
| `validity_domain` | Inputs, parameter range, dtype, shape, software/backend environment, and other applicability limits |
| `comparator` | Equality, residual, norm, interval, or other declared comparison |
| `tolerance` | Absolute/relative tolerance and scale, or explicit exact comparison |
| `tolerance_rationale` | Truncation, conditioning, roundoff, source uncertainty, or other bounded reason |
| `independence_boundary` | Production symbols, private kernels, artifacts, or routes the oracle must not reuse |
| `qualification_evidence` | Exact class-qualified tests and retained records that qualify the oracle |
| `consumers` | Exact maintained test modules or nodes that rely on the oracle |
| `excluded_claims` | Conclusions the oracle cannot support |
| `change_policy` | Conditions requiring a new oracle version or suspended use |

The qualification record owns the oracle's semantic definition and applicability. It
does not carry mutable lifecycle status or a manually asserted scientific-acceptance
boolean. A passing structural validator proves record conformance, not semantic
correctness. A lifecycle-ready validator must accept both an empty candidate ledger and
schema-valid nonempty disposition chains. Claim-bearing consumer docstrings must also be
lifecycle-neutral rather than asserting the candidate ledger's temporary contents. The
candidate revision therefore freezes both validator and consumer content before the
later proposal, rather than changing test logic or consumer documentation together with
a technical disposition.

## Immutable technical dispositions

Lifecycle governance uses a separate append-only disposition ledger beneath the same
explicit test-resource owner. The v1 ledger is
`oracle-qualification-dispositions-v1.json`; it is not a runtime registry. Each entry is
an immutable technical decision containing:

| Field | Required meaning |
|---|---|
| `decision_id` | Stable unique technical-disposition identity |
| `oracle_id` | Exact semantic oracle version governed by the decision |
| `qualification_record_sha256` | Digest of the reviewed qualification-record bytes; a digest establishes content identity only |
| `evidence_revision` | Exact Git revision containing the reviewed record, qualification tests, validator, and consumer bindings |
| `technical_outcome` | `QUALIFIED`, `SUSPENDED`, or `RETIRED` |
| `qualification_authority` | Exact repository evidence-gate version whose prerequisites were applied |
| `gate_evidence` | Commands or retained gate artifacts and their outcomes |
| `independent_review` | Reviewer identity, reviewed revision, review outcome, and durable finding disposition summary |
| `repository_authorization` | Named human authorization to adopt this technical disposition into the repository |
| `transition_reason` | Evidence-backed reason for qualification, suspension, or retirement |
| `supersedes_decision_id` | Previous decision in the same oracle-version chain, or explicit `not_applicable` for the first decision |
| `decided_at` | RFC 3339 decision timestamp |

The record and qualification implementation are reviewed at `evidence_revision`. A
subsequent disposition-and-status proposal commit appends the decision referencing that
already reviewed revision; it cannot refer recursively to its own commit. The proposal
may change only the applicable disposition ledger and synchronized status documentation;
it does not change the bound record, authority, qualification tests, or consumers.

For each `oracle_id`, the disposition ledger preserves earlier entries and forms either
no chain or exactly one linear chain:

- there is at most one genesis entry with `supersedes_decision_id` equal to
  `not_applicable`;
- every non-genesis entry names the immediately preceding decision for the same
  `oracle_id`;
- each decision has at most one successor;
- a nonempty chain has exactly one terminal decision overall; and
- no entry may succeed a `RETIRED` decision.

The first disposition may be `QUALIFIED` or `RETIRED`. Allowed successors are
`QUALIFIED -> QUALIFIED` for reviewed requalification of the same semantic version,
`QUALIFIED -> SUSPENDED`, `QUALIFIED -> RETIRED`, `SUSPENDED -> QUALIFIED`, and
`SUSPENDED -> RETIRED`. A first `SUSPENDED` decision, `SUSPENDED -> SUSPENDED`, and all
successors to `RETIRED` are invalid. The validator enforces these rules without choosing
by timestamp or file order.

When no applicable terminal `QUALIFIED` decision exists for the current qualification-
record digest and evidence revision, the oracle is a `Candidate`, `Suspended`, or
`Retired` according to the terminal decision and content binding. A superseding decision
changes technical state without changing the oracle's mathematical identity. Any change
to the definition, formula, convention, representation contract, authority,
implementation, comparison rule, tolerance, or qualification evidence invalidates the
old digest/revision binding and returns the changed oracle to `Candidate` until a new
`QUALIFIED` decision is proposed and its acceptance gate passes. A meaning-preserving
editorial correction may retain the oracle version, but still needs review and a new
disposition bound to the new record digest.

The qualifying authority is the versioned repository evidence gate plus its independent
technical review. Human authorization permits the repository change and disposition
adoption; it is not scientific validation, uncertainty quantification, human scientific
acceptance, publication authority, or permission for protected execution.

## Qualification tests and consumer tests

Qualification evidence and consumer evidence have different owners.

A qualification test establishes the reference itself without invoking the production
object whose behavior will later be judged. It may check a derivation by direct
substitution, exact or limiting cases, higher precision, an independently assembled
operator, a separately authenticated artifact, or cross-implementation agreement.
Its module is artifact-owned, uses one cohesive `Test...` class, and resides beside the
consumer family rather than in a detached global test bucket.

A consumer test may apply a candidate or qualified oracle to the production object. It
records the `oracle_id`, comparator, tolerance, validity domain, and current technical
state in its documentation or mapped resource. Candidate and suspended consumers are
provisional diagnostics only; their results count as accepted evidence only when the
current oracle is qualified by a passing acceptance gate. A consumer does not silently
extend the oracle beyond its recorded domain.

Shared test-only evaluation behavior may live beneath the applicable test `resources/`
owner after its own qualification. It must not be moved into
`python/src/ksdft2effmass/` solely to make tests import it. Production source may own a
similar capability only when runtime users independently require that capability; such
a production evaluator cannot be the sole independent oracle for itself.

The v1 implementation uses ordinary artifact-owned test modules, explicit resource
paths, and bounded record validation. It must not introduce a generic oracle engine,
factory, plugin system, dynamic registry, ambient discovery mechanism, or universal
production abstraction. A validation command may inspect only the explicitly declared
records in its bounded invocation; it does not discover or dispatch oracle behavior.

## Independence and regress prevention

Oracle qualification is not an infinite chain of self-comparison. The chain terminates
at one or more explicit authorities:

- an exact mathematical derivation;
- direct substitution into a governing equation;
- an authenticated independently produced artifact;
- a primary external measurement or benchmark; or
- a separately implemented and demonstrably converged numerical route.

The qualification record must identify that terminating authority. It must not infer
identity, frame, gauge, normalization, units, provenance, or compatibility from names,
array shapes, ranks, spectra, or matching output.

Qualification code must not call the system under test, copy its private evaluation
kernel, or decode expected values through the serializer under examination. Use of
NumPy, SciPy, Python, operating-system arithmetic, or external scientific software is
an explicit trusted dependency with a recorded environment and relevant limitation;
those dependencies are not silently treated as infallible.

## Tolerances and finite precision

A tolerance belongs to the oracle-consumer comparison contract, not to convenience.
Documentation states:

1. the compared quantity and units;
2. comparator and norm;
3. absolute and relative components;
4. reference scale and zero-reference behavior;
5. truncation, discretization, conditioning, roundoff, or source uncertainty included;
6. parameter and dtype domain for which the tolerance was established; and
7. conditions that invalidate the tolerance.

A fixed small-case floating-point bound is not a convergence threshold, scientific
acceptance criterion, or uncertainty interval. Qualification must fail closed when the
reference or comparison leaves its representable numeric range.

## Technical status

Oracle status is derived from the semantic record and its explicit disposition chain;
it is technical evidence state, not human acceptance:

| Status | Meaning |
|---|---|
| `Candidate` | No applicable terminal `QUALIFIED` decision exists for the current record digest and evidence revision; consumer evidence must not be accepted. |
| `Qualified` | The terminal disposition binds the current record digest and reviewed evidence revision to a passing versioned gate and independent technical review. |
| `Suspended` | A superseding disposition records that a qualification check, authority, dependency, or applicability condition no longer holds; consumers cannot supply accepted evidence. |
| `Retired` | A superseding disposition permanently closes active use of this oracle version; retained records and earlier decisions remain for provenance. |

## Gate ordering

Qualification uses two explicit gates so a decision never refers recursively to the
commit that contains it.

The **candidate gate** runs in this dependency order:

1. validate qualification-record and existing disposition-ledger structure, paths,
   identifiers, content bindings, supersession chains, and class-qualified pytest nodes;
2. run oracle-qualification tests without the production target under judgment;
3. run consumer software/numerical/VVUQ tests as provisional evidence;
4. build synchronized documentation and validate links; and
5. obtain independent semantic review of that exact candidate revision.

After human repository-change authorization, a later **disposition-and-status proposal**
commit appends a decision bound to the reviewed candidate revision and record digest and
updates status documentation consistently with the proposed outcome. Those status
claims are not effective merely because the commit exists. The **acceptance gate** then:

1. verifies the disposition, exactly one genesis, linear no-fork supersession, allowed
   transitions, and exactly one terminal decision for the oracle version;
2. verifies that only the explicit disposition ledger and status-document paths changed
   from the bound candidate revision, while qualification, consumer, and authority
   content remained unchanged;
3. reruns the qualification and consumer checks at the proposal commit; and
4. validates the proposed status documentation and links.

Only a passing acceptance gate makes the proposed disposition and synchronized status
claims effective and makes qualified consumer results accepted evidence. A failed
proposal remains ineffective and must be corrected or superseded; it cannot be cited as
qualification. Test
collection order is not dependency control. When a candidate or acceptance stage fails,
consumer tests may still aid debugging, but their results cannot be reported as
qualified verification or validation evidence.

## Documentation and mapping

Every consuming architecture testing page identifies:

- oracle ID and kind;
- authoritative definition;
- qualification test or retained record;
- consumer test node;
- comparator, tolerance, environment, and validity domain; and
- excluded claims.

The relevant ownership JSON continues to own test-module classification. Oracle
qualification receives a separate record rather than overloading class ownership,
because test ownership and reference adequacy answer different questions.
Sphinx development documentation explains this policy to contributors; domain pages
explain the actual oracle.

## Row-036 pilot and transition

`PERIODIC-XWALK-036` is the first pilot. Its existing tests consume three separately
documented analytic oracle records:

1. period-$2\pi$ discrete-Fourier orthogonality, including two-sided unitarity for
   $M=2$, $N=5$ and the separately bounded column-isometry diagnostics for the
   rectangular $M=1,N=5$ and $M=1,N=7$ consumers;
2. the centered-difference Bloch dispersion for the declared free and cosine small-grid
   cases; and
3. exact sampled cosine Fourier-transfer blocks in the bounded no-wrap domain
   $M=1$, $N=7$.

The third claim uses the same finite root-of-unity identity as the first but is not the
same oracle: map-column orthogonality does not establish absence of pairwise potential-
transfer aliasing.

Their formulas, assumptions, comparators, tolerances, and excluded scientific claims
are documented and have received bounded technical review. The pilot now has
versioned machine-readable qualification records, local schemas, an artifact-owned
independent qualification-test module, bounded structural/content/dependency checks,
exact consumer bindings, a passing candidate gate, and three proposed genesis
`QUALIFIED` dispositions bound to reviewed evidence revision
`f37e5d722f8c9007d8ea55c06e808c9c73bf775d`. The dispositions do not validate their own
scientific meaning. Row 036 is proposed as **Ready for gate**. Under this policy, the
dispositions, status, and bounded numerical-verification evidence become effective only
if the exact disposition-and-status proposal commit passes the acceptance gate.

The documentation-first implementation sequence is:

1. **Complete:** accept and review this policy and synchronized Sphinx/domain documentation;
2. **Complete:** define the v1 qualification-record and disposition-ledger schemas and row-036 semantic records;
3. **Complete:** add artifact-owned qualification tests independent of the comparator;
4. **Complete:** add bounded structural, reviewed-record content-binding, supersession-chain, and dependency-direction validation that supports both candidate and disposition states;
5. **Complete for the candidate stage:** bind consumer nodes to candidate oracle IDs and implement the candidate gate;
6. **Complete:** create and independently review corrected candidate revision `f37e5d722f8c9007d8ea55c06e808c9c73bf775d` containing the lifecycle-ready validator and status-neutral consumer documentation;
7. **Complete in this proposal:** append three genesis `QUALIFIED` decisions bound to that reviewed revision and propose restoration of `Ready for gate`; and
8. **Acceptance condition:** treat `Ready for gate` and the numerical evidence as effective only if the exact proposal commit passes the acceptance gate.

This transition does not invalidate row 036's production algebra or software-contract
tests. It limits the present interpretation of its numerical tests.

## Limitations

This page documents the target policy. The machine-readable schemas, bounded validator,
candidate gate, and proposed dispositions are implemented only for the explicit row-036
pilot. Their effect remains conditional on the exact proposal acceptance gate; no
ordered repository-wide CI gate or repository-wide oracle inventory is implemented.
Existing numerical and scientific tests outside the
row-036 pilot require later inventory and migration; absence from the pilot is not
evidence that their oracles are qualified. No calculator execution, dependency addition, scientific
acceptance, or publication is authorized by this policy.
