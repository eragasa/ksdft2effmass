Numerical-oracle qualification
==============================

A test oracle is a declared reference relation, value, dataset, or independent
evaluation route used to judge another result.  Calling a value ``expected`` or
``reference`` does not establish its correctness.  A claim-bearing oracle must be
qualified for its declared use before a consuming test can count as accepted
verification, validation, or uncertainty-quantification evidence.

The authoritative repository policy is
``docs/architecture/v2/documentation/numerical-oracle-qualification.md``.  This page
summarizes its contributor-facing contract.

Scope
-----

Qualification is required for analytic numerical references, manufactured solutions,
independent numerical evaluators, retained calculation references, literature or
empirical values, convergence references, and shared approximate-comparison values.
Direct exact software-contract assertions, such as an enum member or exact serialized
token, remain governed by their public contract and do not need a separate numerical
oracle record.

Qualification is bounded.  An analytically verified identity can support numerical
verification without supplying scientific validation.  An authenticated artifact can
establish byte identity without establishing convergence or physical adequacy.  A
successful oracle check never implies human acceptance.

Qualification record
--------------------

Each claim-bearing oracle entering qualification has a stable, versioned identity and a
machine-readable record beneath the applicable ``python/tests/**/resources/``
directory.  The record begins as a candidate; its existence does not qualify it.  The
record declares:

* oracle kind and evidence class;
* the exact bounded claim;
* authoritative equations, primary source, or retained-artifact identity;
* assumptions and validity domain;
* state space, basis, gauge or frame, normalization, geometry, ordering, energy
  reference, units, dtype, shape, and environment, each explicit or marked not
  applicable;
* comparator, norm, tolerance, and tolerance rationale;
* the production behavior and private kernels that the oracle must not reuse;
* exact class-qualified qualification and consumer test nodes;
* excluded claims; and
* conditions requiring suspension or a new oracle version.

A structural validator can establish that the record is complete and internally
referential.  It cannot establish that the underlying mathematics or scientific
reference is correct; qualification tests and semantic review provide that evidence.

Lifecycle dispositions
----------------------

The semantic qualification record does not contain mutable status.  A separate
append-only ``oracle-qualification-dispositions-v1.json`` ledger under the same explicit
resource owner records ``QUALIFIED``, ``SUSPENDED``, and ``RETIRED`` decisions.  Each
immutable entry binds:

* the oracle ID and qualification-record SHA-256 digest;
* the exact reviewed evidence revision;
* the versioned technical gate and its retained outcomes;
* independent reviewer identity, reviewed revision, outcome, and finding summary;
* named human authorization to adopt the repository disposition;
* transition reason, timestamp, and superseded decision.

The implementation and record are reviewed in a candidate revision.  A later
disposition-and-status proposal references that revision, avoiding recursive
self-reference, and changes only the disposition ledger and synchronized status pages.
For each oracle version, the validator requires at most one genesis, one linear chain,
at most one successor per decision, and exactly one terminal decision when the chain is
nonempty.  First decisions may be ``QUALIFIED`` or ``RETIRED``.  Requalification,
suspension, reinstatement, and retirement follow explicit transitions; ``RETIRED`` has
no successor.  The validator does not choose state by timestamp or file order.  A
content or evidence change invalidates the earlier digest/revision binding and returns
the changed oracle to ``Candidate`` until a new qualification proposal passes.

The versioned repository evidence gate and independent technical review are the
qualifying authority.  Human authorization adopts the technical disposition into the
repository; it is not human scientific acceptance, scientific validation, UQ,
publication authority, or protected-execution authority.

Qualification before consumption
--------------------------------

Qualification tests and consumer tests have separate responsibilities.

A qualification test examines the oracle without invoking the production object that
will later be judged.  Depending on the oracle, it can use direct substitution, exact
or limiting cases, higher precision, an independently assembled operator, a separately
authenticated artifact, or cross-implementation evidence.

A consumer test may apply a candidate or qualified oracle to the production result,
using only the declared domain and comparison rule.  Candidate and suspended consumers
are provisional diagnostics; only consumers of an effectively qualified oracle count
as accepted evidence.  Test execution order is not a dependency
mechanism.

The candidate gate validates record and existing-ledger structure, runs independent
qualification tests, runs consumers provisionally, validates documentation, and obtains
independent semantic review of the exact candidate revision.  After authorization, a
later disposition-and-status proposal binds that revision and record digest and updates
status pages consistently with the proposed outcome.  Its claims are not effective
merely because the commit exists.  The acceptance gate validates the unique linear
chain and allowed transition, verifies that only the ledger and status pages changed,
reruns qualification and consumer checks, and validates the proposed documentation.

Only the passing acceptance gate makes the proposed disposition and status effective
and makes qualified consumer results accepted evidence.  Failed
candidate or acceptance stages can aid debugging, but their consumer results cannot be
reported as qualified evidence.

Test-only ownership
-------------------

Reusable oracle behavior belongs under the applicable test ``resources/`` owner after
qualification.  It must not be added to ``python/src/ksdft2effmass/`` solely to make it
importable by tests.  A production evaluator is appropriate only when runtime users
need that capability independently, and it cannot be the sole oracle for itself.

Every maintained qualification or consumer module still follows the normal test rules:
one cohesive ``Test...`` class, explicit evidence-class marking, precise fixtures,
closed typing, and documentation of the represented mathematics and excluded claims.
The v1 design uses explicit artifact-owned modules and bounded record validation.  It
does not introduce a generic oracle engine, factory, plugin system, dynamic registry,
ambient discovery mechanism, or universal production abstraction.

Oracle status
-------------

``Candidate``
   No applicable terminal ``QUALIFIED`` decision binds the current record digest and
   evidence revision; consuming results are not accepted evidence.

``Qualified``
   The terminal disposition binds the current record digest and reviewed evidence
   revision to the passing versioned gate and independent technical review.

``Suspended``
   A check, authority, dependency, or applicability condition no longer holds.

``Retired``
   The oracle remains retained for provenance but has no active evidence consumers.

These are technical evidence states, not scientific or human acceptance decisions.

Row-036 pilot
-------------

The first pilot covers the period-:math:`2\pi` common-space comparison.  Its three
candidate analytic oracles are discrete-Fourier orthogonality, centered-difference
Bloch dispersion, and resolved sampled-cosine Fourier transfer in the bounded
:math:`M=1,N=7` no-wrap domain.  Map-column orthogonality and potential-transfer
aliasing remain separate claims.  Their formulas and bounded tolerances are documented,
but the versioned qualification records, independent qualification-test owner,
reviewed-revision dispositions, and candidate/acceptance gates are not yet implemented.  The production comparison remains implemented; its current numerical
tests are provisional evidence until that pilot is complete.

No calculator execution, dependency addition, scientific acceptance, publication, or
release is authorized by oracle qualification.
