VVUQ testing and evidence documentation
=======================================

The maintained test suite is an executable research-software evidence surface.
Tests must identify what they establish, how their oracle is obtained, and what
a pass does not establish.  This standard applies progressively when an object
or subsystem is migrated; it does not require a repository-wide mechanical
rewrite of stable tests.

Evidence classes
----------------

``software_verification``
   Checks an implemented software contract, such as public construction,
   invariants, behavior, error taxonomy, serialization, imports, or technical
   integration.  Values in an assertion do not by themselves make a test
   numerical verification.

``numerical_verification``
   Checks implementation of stated mathematics against a result derived
   independently of the production algorithm.  The evidence records units,
   scale regime, numerical representation, and an exact or tolerance-based
   acceptance rule.  It does not establish agreement with nature or with an
   independent physical reference.

``scientific_validation``
   Would compare a declared model and use case with independent reference
   evidence under a separately authorized validation protocol.  It is future
   work unless repository artifacts explicitly provide it.  Passing software
   or numerical tests must not be relabeled as scientific validation, and no
   marker or evidence-identifier family may be inferred for this absent class.

``uncertainty_quantification``
   Would identify and propagate uncertainty sources.  Error handling,
   parameterization, multiple scales, or tolerance testing alone is not
   uncertainty quantification.

Constructor and input-invariant tests are software verification.  Tests and
reports must explicitly exclude scientific validation and uncertainty
quantification when they have not been performed; the current maintained
operator-record and CPN evidence described below does not claim either
capability.

Stable evidence identifiers
---------------------------

Every migrated test receives an identifier that remains stable if files are
reorganized.  Existing identifier families combine the evidence class, an
object or subsystem abbreviation, and a three-digit sequence.  For example,
``SV-ORA-001`` identifies software-verification evidence for
``OperatorRecordResidualAnalyzer`` and ``NV-ORA-001`` identifies numerical
verification for the same object.  Migration preserves existing identifiers
and scientific meaning.  Identifiers for absent evidence classes must not be
created, and no new marker or family is implied by this convention.
Identifiers must be unique across the maintained test suite.

Unified executable-documentation grammar
----------------------------------------

The unified grammar applies when an evidence module is migrated.  It does not
silently rewrite or authorize changes to protected historical evidence.

Exact module headings
~~~~~~~~~~~~~~~~~~~~~

A migrated class-owned or artifact-owned module docstring contains the
following headings exactly once and in this order:

.. code-block:: text

   Evidence class and represented meaning
   Owned contract, oracle, and scope
   VVUQ and scientific exclusions

The first heading names the evidence class and, where applicable, distinguishes
the physical model, mathematical object, finite or numerical representation,
and software surface.  The second names the primary system under test (SUT),
the owned contract, the oracle source, and the included unit and scale regime.
The third states what pass and failure mean and excludes unsupported numerical
verification, scientific validation, uncertainty quantification, physical
correctness, and cross-language conformance.

Exact test and helper fields
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every migrated test-function docstring and nontrivial evidence-helper docstring
contains these seven fields exactly once and in this order, each with a nonempty
body:

.. code-block:: text

   Evidence ID
   Requirement
   Method
   Oracle
   Acceptance
   Interpretation
   Limitations

``Evidence ID`` gives one stable authoritative identifier.  A helper instead
names the evidence it supports and states that it owns no identifier.  A
parameterized test normally owns one identifier; an explicitly inventoried
same-stem inclusive range is permitted only with a one-to-one mapping from
parameters to identifiers.  ``Requirement`` states a public contract or
mathematical claim rather than restating an assertion.  ``Method`` identifies
public inputs, action, controlled fault, parameter regime, and warning policy.
``Oracle`` explains the independently known expected result.  ``Acceptance``
gives the exact result, exception, ordering, representation, or justified
inclusive tolerance or ULP rule.  ``Interpretation`` distinguishes plausible
implementation, fixture, oracle, environment, and contract defects.
``Limitations`` records excluded inputs, regimes, dependencies, physical
conclusions, scientific validation, uncertainty quantification, and
cross-language claims.  Evidence-specific requirements, oracles, acceptance
rules, and limitations remain authoritative rather than being replaced by
boilerplate.

Semantic test naming
~~~~~~~~~~~~~~~~~~~~

Migrated test functions use exactly
``test_<surface>__<facet>__<behavior>``.  ``<surface>`` is one of
``constructor``, ``field``, ``property``, ``method``, ``classmethod``,
``staticmethod``, ``protocol``, ``public_api``, ``artifact``, or ``workflow``;
the facet names the public operation or cohesive contract facet, and the
behavior states the expected observable outcome.  Segments are lowercase
snake case, evidence identifiers do not appear in function names, and a rename
requires a complete old-to-new pytest node-ID map.

Evidence ownership
~~~~~~~~~~~~~~~~~~

Class-owned evidence has one public DataObject, ResultObject, ActionObject,
Workflow, or error object as its sole primary SUT.  Collaborators only construct
inputs or expose public outcomes.  Cross-object behavior belongs to the
ActionObject or genuine production Workflow that owns the operation.  A public
schema, fixture family, import surface, dependency boundary, command, or
interoperability artifact instead owns artifact-integration evidence; a class or
technical Workflow must not be fabricated merely to provide an owner.  Helpers
own setup or assertion mechanics, no evidence identifier, and no independent
pass claim; they must not hide an oracle or scientific convention.  Protected
historical evidence remains inventoried and unchanged until a separate
migration is authorized.

Evidence filenames follow the owner.  A class-owned module is exactly
``test__<ClassName>.py`` and its case-sensitive stem, imported public class,
manifest owner, documentation, and ``SUT = <ClassName>`` assignment agree.  An
artifact- or boundary-owned module instead uses a descriptive lowercase
snake-case name that identifies the concrete artifact or both boundary sides;
``_to_`` is reserved for a directional relation.  Cross-object behavior is
owned by its genuine ActionObject or production Workflow, while technical
integration remains artifact- or boundary-owned and must not be assigned to an
invented Workflow.  Controlled renames preserve evidence identifiers,
assertions, fixtures, parameterization, and meaning, and update manifests,
replay paths, inventories, checksums, documentation, and one-to-one pytest node
maps together.  The exact grammar, approved ``workflow_cpn`` names, and review
rules are maintained in
``.pi/skills/document-python-research-software/references/test-evidence-documentation.md``.

Parameterization, representation, and independent oracles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parameterization is appropriate only when one requirement, method, oracle form,
acceptance rule, and interpretation cover a declared input partition.  Each
case receives a stable meaningful parameter ID rather than an ordinal.
Documentation states boundary values, signs, scales, canonicalization, warning
policy, excluded zeros, and the expected pass/fail partition.  Cases with
different requirements or failure meanings are separate tests.  Collection
count and evidence-owner count remain distinct and traceable.

Use exact equality for exact represented state, canonical text, deterministic
ordering, enum or error identity, and DataObject value semantics.  Do not weaken
an exact contract with approximate comparison.  Approximate comparisons require
an authorized mathematical or numerical contract and documentation of the norm,
tolerance, units, scale, boundary inclusivity, zero handling, and floating-point
representation.  A nonzero tiny reference uses a criterion that cannot accept
zero; exact mathematical zero is not merely an approximately small value.

An independent oracle is available without executing the behavior under test.
Acceptable sources include a public invariant, fixed schema, exact language
semantics, hand-derived analytical result, higher-precision or independently
implemented calculation, or approved external reference.  A production helper,
private method, production constant as the sole expected value, the same library
routine under different names, or agreement among reviews is not independent.
A production constant may select inputs only when its approved value is also
anchored independently.  Numerical-verification documentation states the
represented object, shape, dtype, units, scale regime, analytical result,
warning policy, and acceptance rule.

Controlled fault injection
--------------------------

Fault injection is permitted to exercise a documented public translation branch
that valid input cannot induce reliably.  A test must identify the controlled
dependency, why injection is needed, and the expected public error.  Such a test
verifies the owning ActionObject's boundary; it does not validate the controlled
dependency.  For example, an injected ``numpy.linalg.LinAlgError`` can verify
translation to ``LINEAR_ALGEBRA_FAILURE`` but cannot establish SVD accuracy.
Direct calls to private production methods are not an acceptable substitute for
public-boundary evidence.

StateSpace software evidence
----------------------------

``SV-SS-001`` through ``SV-SS-013`` verify the three owned facets of the
``StateSpace`` DataObject. Construction evidence covers public three-field
mapping; value-preserving canonicalization of Python integer and representative
NumPy ``int32``/``int64`` inputs to stored built-in ``int``; positive one and an
arbitrary-precision positive structural dimension; exact nonempty string
preservation without normalization; and absence of standalone serialization
APIs. Positivity is the only dimension-magnitude policy: construction imposes no
cap and allocates no vector or matrix.

Invariant evidence requires ``TypeError`` for Boolean, ``None``, floating,
numeric-string, byte, complex, and arbitrary-object dimensions, while zero and
negative admitted integer scalars raise ``ValueError``. ``identifier`` and
``kind`` are tested independently: representative non-string values raise
field-specific ``TypeError`` and the empty string raises field-specific
``ValueError``. The static constructor declaration includes the already admitted
Python and NumPy integer scalar families while the stored field remains
``dimension: int``. Boolean rejection is a runtime semantic refinement because
static integer typing cannot express that exclusion precisely.

Value-semantics evidence verifies exactly the stored fields ``identifier``,
``kind``, and ``dimension``; frozen slotted state without an instance
``__dict__``; and exact structural equality across every field. Hash behavior is
not specified. ``StateSpace`` has no independent wire format and is serialized
only as nested state by ``OperatorRecordJsonSerializer`` under the record's
schema-version-1 contract.

These are software-verification tests of synthetic finite metadata. Cross-object
agreement with basis ordering and matrix shape belongs to ``OperatorRecord``.
No numerical-verification evidence is assigned because ``StateSpace`` performs
no numerical algorithm. Passing does not establish a physical Hilbert space,
basis completeness, operator-domain correctness, matrix compatibility, DFT or
Wannier validity, scientific validation, uncertainty quantification, or Rust
conformance.

Basis software evidence
-----------------------

``SV-B-001`` through ``SV-B-018`` verify the construction, intrinsic invariants,
and exact value semantics of the ``Basis`` DataObject. Construction evidence
covers exact four-field mapping; tuple and list canonicalization to exact built-in
tuple storage; defensive ownership of mutable caller sequences; exact ordered-
label spelling and case preservation; representation of both exact Python Boolean
orthonormality states; and absence of standalone serialization APIs.

Invariant evidence rejects bare strings, bytes, unordered collections, mappings,
generators, scalar values, and arbitrary objects as ordering containers with
``TypeError``. Empty approved sequences raise ``ValueError``. Every label must be
a nonempty string and labels must be unique by exact case-sensitive equality.
Identifier and kind string semantics/nonemptiness are tested independently.
``orthonormal`` requires exact built-in ``bool``; integers and NumPy Booleans are
not coerced. The static constructor declaration exposes approved ordered-sequence
inputs while stored state remains ``ordering: tuple[str, ...]``. Bare strings
remain a documented runtime semantic rejection despite static sequence typing.

Value-semantics evidence verifies exactly ``identifier``, ``kind``, ``ordering``,
and ``orthonormal`` as frozen slotted state. Equality is exact across every field
and ordering-sensitive; no hash policy is specified. ``orthonormal=False`` is
valid Basis metadata, while ``OperatorRecord`` separately rejects it under the
schema-version-1 cross-object policy. Ordering-length agreement with StateSpace
and matrix dimension also belongs to ``OperatorRecord``. ``Basis`` is serialized
only as nested record state by ``OperatorRecordJsonSerializer``; no independent
Basis schema is approved.

These tests use abstract synthetic coordinate labels and perform no numerical
algorithm. No numerical-verification identifier is assigned. Passing does not
establish basis-vector existence, linear independence, completeness, numerical
orthogonality, StateSpace or matrix compatibility, gauge alignment, physical
equivalence, scientific validation, uncertainty quantification, or Rust
conformance.

Geometry software and numerical evidence
-----------------------------------------

``SV-G-001`` through ``SV-G-022`` verify the three software-owned facets of the
``Geometry`` DataObject. Construction evidence covers exact five-field mapping;
approved tuple/list nested-sequence and Python/NumPy integer/floating scalar
admission; canonical nested built-in tuple storage containing exact built-in
``float`` components; defensive ownership; exact metadata preservation; exact
row-order/sign representation; and absence of standalone serialization APIs.
Invariant evidence distinguishes wrong semantic container/scalar types
(``TypeError``) from wrong approved sequence shape, nonfinite components,
binary64 conversion overflow, and empty metadata values (``ValueError``). Value-
semantics evidence verifies frozen slotted state and exact structural equality
across every stored field without assigning a hash contract.

``NV-G-001`` through ``NV-G-009`` separately verify the intrinsic numerical
linear-independence policy. For

.. math::

   \rho(\mathbf C)=\frac{\sigma_{\min}(\mathbf C)}
                         {\sigma_{\max}(\mathbf C)},

``Geometry.LINEAR_INDEPENDENCE_RTOL`` publicly owns
:math:`r_{\mathrm{tol}}=10^{-12}` and construction accepts exactly when
:math:`\sigma_{\max}>0` and
:math:`\sigma_{\min}>r_{\mathrm{tol}}\sigma_{\max}`. Analytical evidence covers
a well-conditioned diagonal cell, exact duplicated-row dependence, skew and
left-handed triangular full-rank cells, the independently fixed public ``1e-12``
tolerance with ratios clearly below, exactly equal to, and clearly above the
strict threshold, both signs of finite normal uniform scales ``1e-200``, ``1``,
and ``1e200`` for accepted and rejected cells, and every row permutation of representative valid
and invalid cells. Expected decisions use diagonal singular values, exact row
relations, or triangular diagonal products rather than NumPy rank, SVD, or
determinant oracles. Every numerical construction promotes ``RuntimeWarning`` to
an error.

Geometry preserves explicit coordinate and length-unit strings and performs no
coordinate transformation, unit conversion, dimensional analysis, structure
relaxation, crystallographic validation, or physical-realism assessment. It need
not be orthogonal, normalized, cubic, or right-handed. Exact equality remains
ordering-sensitive even though the independence validity decision is row-
permutation invariant. ``OperatorRecordJsonSerializer`` alone owns nested record
serialization. Passing these tests establishes the documented Python software
contract and the tested binary64 independence decisions; it establishes no DFT
or Wannier accuracy, physical structure validity, scientific validation,
uncertainty quantification, or Rust conformance. Detailed traceability is in
:doc:`operator-record-geometry`.

``NV-G-001`` through ``NV-G-009`` are protected historical evidence and were
compared read-only with the unified convention, not migrated.  Their seven test
and helper fields, unique identifiers, numerical-verification marker,
meaningful signed-scale parameter IDs, analytical oracle independence, exact
representation rules, threshold boundaries, warning policy, interpretations,
and exclusions conform.  Their historical module headings and test names do
not use the new exact grammar.  Those structural differences are inventory
findings, not authorization to rename or redocument the accepted module.  The
comparison is not new validation, a tolerance-adequacy determination, or final
acceptance.

EnergyReference software evidence
---------------------------------

``SV-ER-001`` through ``SV-ER-012`` verify the construction, intrinsic
invariants, and exact value semantics of the ``EnergyReference`` DataObject.
Construction evidence covers the exact stored fields ``zero`` and ``unit``;
literal preservation of zero-convention and energy-unit strings across case,
spacing, punctuation, hyphenation, and spelling; exclusion of positional and
keyword numerical-offset constructor state; and absence of standalone
serialization APIs.

Invariant evidence tests ``zero`` and ``unit`` independently. ``None``,
Booleans, integers, floats, bytes, and arbitrary objects raise field-specific
``TypeError`` rather than being converted with ``str()``. The empty string has
the accepted semantic type but violates the nonempty invariant and raises
field-specific ``ValueError``. Accepted Python ``str`` instances are retained
unchanged. There is no trimming, case folding, normalization, registry lookup,
alias resolution, dimensional analysis, unit conversion, or physical
interpretation. Because trimming is absent, whitespace-only strings remain
nonempty metadata under the current contract.

Value-semantics evidence verifies frozen, slotted two-field state without an
instance ``__dict__`` and exact structural equality sensitive to every stored
string distinction. Hash behavior is not specified. Equality establishes exact
metadata identity rather than physical equivalence. Exact relational comparison
belongs to ``OperatorRecordCompatibilityAnalyzer``. Nested record JSON belongs
to ``OperatorRecordJsonSerializer``; malformed serializer payloads and the
historical forbidden ``energy_reference.value`` field remain on the serializer
evidence surface rather than being duplicated here.

These tests use synthetic textual metadata and are software verification only.
``EnergyReference`` owns no numerical algorithm, so numerical verification is
not applicable and no numerical-verification identifier is assigned. Passing
does not establish a physically suitable energy zero or unit, DFT or Wannier
validity, scientific validation, uncertainty quantification, or Rust
conformance. Detailed traceability is in
:doc:`operator-record-energy-reference`.

OperatorRecord DataObject software evidence
--------------------------------------------

``SV-OR-001`` through ``SV-OR-042`` verify five cohesive facets of the
``OperatorRecord`` DataObject: construction, matrix/cross-object invariants,
metadata/dependency invariants, defensive ownership, and exact value semantics.
The object stores exactly identifier, operator kind, canonical matrix,
StateSpace, Basis, Geometry, EnergyReference, and provenance.

Construction evidence admits nested tuple/list and exact NumPy-array matrices
containing approved Python/NumPy integer, floating, and complex scalars. It
verifies exact C-contiguous ``numpy.complex128`` canonical storage, public shape,
exact descriptive metadata preservation, general finite non-Hermitian admission,
and exclusion of Hermiticity, comparison, differencing, and serialization APIs.
Boolean, textual, null, and arbitrary scalar semantics raise ``TypeError``.
Rank, raggedness, squareness, finite real/imaginary components, and complex128
conversion range use ``ValueError``. Huge Python integer overflow is translated;
largest finite representative binary64 entries remain admitted without a norm
calculation.

Cross-object evidence requires matrix dimension, StateSpace dimension, and Basis
ordering length to agree. The record requires ``basis.orthonormal is True`` while
standalone Basis metadata may validly store ``False``. Exact public dependency
types are tested independently without invariant bypasses. Identifier and
operator-kind strings use independent ``TypeError``/``ValueError`` evidence.
Provenance accepts Mapping objects, including an explicit empty mapping, with
nonempty string keys and values. Non-Mapping iterables are not silently converted.

Ownership evidence verifies defensive copies from direct arrays, noncontiguous
views, and mutable dictionaries; canonical C-order storage from C, Fortran, and
strided inputs; matrix item-write and ``setflags(write=True)`` rejection; and
read-only Mapping exposure without requiring a public concrete mapping type. The
outer record remains frozen and slotted.

Equality evidence is exact across every stored field. Matrix equality is
complex-value and position sensitive with no tolerance; provenance uses mapping
content independent of insertion order. Unrelated-object comparison follows the
``NotImplemented`` protocol. ``OperatorRecord.__hash__ is None`` and no matrix or
provenance content hash is introduced.

These are software representation contracts. No Hermiticity residual,
compatibility rule, subtraction, residual norm, approximate comparison,
serializer payload, or round trip is duplicated. ``OperatorRecord`` performs no
scientific numerical algorithm, so numerical verification is not applicable and
no ``NV-OR`` evidence exists. Passing does not establish a physically valid
Hamiltonian, DFT/Wannier accuracy, scientific validation, uncertainty
quantification, or Rust conformance. Detailed traceability is in
:doc:`operator-record-data-object`.

HermiticityResult software evidence
-----------------------------------

``SV-HR-001`` through ``SV-HR-015`` verify the three cohesive owned facets of
``HermiticityResult``. Construction evidence covers exact mapping of residual
:math:`\varepsilon_{\mathrm H}`, tolerance :math:`\tau`, and common
``energy_unit``; accepted Python and NumPy integer/floating scalar-family
canonicalization to built-in ``float`` in both scalar positions; the exact
inclusive predicate ``residual <= tolerance`` including equality at zero;
exclusion of ``is_hermitian`` from constructor state; and absence of independent
serialization APIs.

Invariant evidence independently covers residual and tolerance semantic types,
finiteness including huge-integer conversion overflow, and nonnegativity. The
static constructor contract declares the already admitted Python and NumPy
integer/floating inputs while stored attributes remain built-in ``float``.
Because static integer typing cannot precisely exclude Boolean, Boolean rejection
remains an explicit runtime semantic refinement. Booleans, numeric strings,
bytes, complex values, and arbitrary objects raise
``TypeError`` rather than being coerced. NaN, infinities, and unrepresentable
integer conversions raise ``ValueError`` under field-specific finite-number
taxonomy; finite negatives raise ``ValueError``. Unit metadata must be a nonempty
Python string. Existing policy performs no trimming, normalization, registry
lookup, or conversion and does not impose an exact-built-in-string boundary.

Value-semantics evidence verifies exactly three dataclass fields, frozen slotted
state without an instance ``__dict__``, derived rather than stored
``is_hermitian``, and exact structural equality across every stored field. Hash
behavior is deliberately unspecified. ``OperatorRecordJsonSerializer``
serializes only ``OperatorRecord``; no ``HermiticityResult`` or retained-result
exception schema is approved.

These direct ResultObject tests use synthetic scalar state and do not invoke
``HermiticityAnalyzer`` or compute a matrix residual. Analyzer numerical
correctness, tolerance suitability, physical Hermiticity, DFT or Wannier
validity, scientific validation, uncertainty quantification, and Rust
conformance are not established. Detailed traceability is in
:doc:`operator-record-hermiticity`.

HermiticityAnalyzer separated evidence
---------------------------------------

``SV-HA-001`` through ``SV-HA-019`` are software-verification evidence for the
public ``HermiticityAnalyzer`` ActionObject. The ``configuration`` facet owns
explicit construction; tolerance scalar-family admission, canonicalization,
type, finiteness, conversion-overflow, and sign taxonomy; required unit typing
and nonemptiness; frozen/slotted state; and serialization exclusion. The
``contract`` facet owns independent ``execute()`` and ``require()`` input
boundaries, public Result construction, exact unit matching, unit-check-before-
arithmetic ordering, successful and failed requirement behavior, Analyzer-owned
tolerance policy, and structured nonfinite-residual failure. It uses exact-zero
or exact structural oracles and contains no independent approximate residual
metric oracle.

``NV-HA-001`` through ``NV-HA-005`` separately verify the numerical residual on
five analytical cases: exact Hermitian zero, complex :math:`\sqrt{26}`, real
nonsymmetric residual one, exact-zero preservation under a genuine exactly
representable unitary phase transformation, and the change from ``1`` to
:math:`1/\sqrt{3}` for the approved non-Hermitian discrete-Fourier basis case.
The expected values are derived without the production Analyzer, private
helpers, or replication of its NumPy residual expression. Exact zero requires
``actual == 0.0``. Normal nonzero values require

.. math::

   |x_{\mathrm{actual}}-x_{\mathrm{expected}}|
   \leq 64\epsilon_{\mathrm{mach}}|x_{\mathrm{expected}}|,

with zero excluded and the positive bound required to be smaller than the
expected magnitude. All numerical executions promote ``RuntimeWarning`` to an
error.

Hermiticity status is unitary invariant, but the chosen nonzero entrywise
maximum residual magnitude generally is not. These evidence classes therefore
remain distinct. Passing software evidence establishes the ActionObject contract
and failure taxonomy. Passing numerical evidence establishes only agreement with
five small normal-scale binary64 analytical cases. It does not establish a
scientifically appropriate tolerance, physical Hermiticity, basis/gauge
correctness, DFT or Wannier accuracy, model validation, uncertainty
quantification, arbitrary-dimension guarantees, or Rust conformance. Scientific
validation and uncertainty quantification have not been performed. Detailed
traceability is in :doc:`operator-record-hermiticity`.

HermiticityNumericalErrorCode software evidence
------------------------------------------------

``SV-HNEC-001`` through ``SV-HNEC-006`` verify the exact closed public enum
contract for ``HermiticityNumericalErrorCode``. Evidence covers the sole member
``NONFINITE_RESIDUAL = "nonfinite_residual"`` in declaration order, exact public-
registry alias absence, Python 3.14 ``StrEnum`` and ASCII lowercase snake-case
behavior, value/name lookup identity round trips, and exact ``ValueError`` versus
``KeyError`` invalid-lookup taxonomy.

``NONFINITE_RESIDUAL`` means ``HermiticityAnalyzer`` could not produce a finite
binary64 Hermiticity residual, including overflow while forming
:math:`H-H^\dagger` from individually finite entries. The Analyzer owns
production detection and emission; the enum performs no matrix operation or
finite check. Unit disagreement uses ``HermiticityUnitMismatchError`` and a
finite residual above tolerance uses ``HermiticityRequirementError``. Represented-
difference and residual-comparison numerical failures retain their separate
public code types.

These enum-contract tests are software verification of stable classification
vocabulary. Analyzer emission belongs to Analyzer software-verification evidence,
and residual accuracy belongs to numerical verification. ``StrEnum`` behavior
supports future conceptual Rust-enum mapping but approves no JSON, exception wire
format, Rust implementation, or Rust conformance. Physical Hermiticity,
scientific validation, and uncertainty quantification are not established.
Detailed traceability is in :doc:`operator-record-hermiticity`.

HermiticityNumericalError software evidence
--------------------------------------------

``SV-HNE-001`` through ``SV-HNE-007`` verify the cohesive direct-construction
contract for ``HermiticityNumericalError``. Evidence covers public ``ValueError``
hierarchy; complete current ``HermiticityNumericalErrorCode`` admission; exact
enum identity retention through the public ``reason`` field; positional and
``reason=`` keyword construction; semantic human-readable reason summarization;
``TypeError`` rejection of ``None``, Booleans, integer, one raw string, unrelated
enum member, and arbitrary object; additional free-form-detail exclusion; and
absence of independent serialization APIs.

``reason`` is a closed enum-backed category, not arbitrary prose. Raw strings are
not coerced, and no additional ``detail`` field is accepted. The approved public
structured field remains ``error.reason`` and is the authoritative machine-
readable category; the message is secondary human-readable text. Exact enum
vocabulary, aliases,
``StrEnum`` behavior, and lookups remain owned separately by ``SV-HNEC-001``
through ``SV-HNEC-006``.

``HermiticityAnalyzer`` owns production emission when a finite binary64 residual
cannot be produced. Direct exception evidence performs no matrix operation and
does not reproduce overflow. Unit disagreement and a finite residual exceeding
tolerance retain their separate exception types. No numerical-exception wire
format is approved; ``OperatorRecordJsonSerializer`` serializes only
``OperatorRecord``. Numerical correctness, overflow-handling correctness,
physical Hermiticity, scientific validation, uncertainty quantification, and
Rust conformance are not established. Detailed traceability is in
:doc:`operator-record-hermiticity`.

HermiticityUnitMismatchError software evidence
----------------------------------------------

``SV-HUME-001`` through ``SV-HUME-008`` verify the cohesive direct-construction
contract for ``HermiticityUnitMismatchError``. Evidence covers public
``ValueError`` hierarchy; exact retention of Analyzer-policy and record-metadata
unit strings in their ordered roles; semantic role-labeled diagnostics;
role-specific ``TypeError`` for wrong semantic types; role-specific ``ValueError``
for empty strings; ``ValueError`` for equal strings; case-sensitive exact
mismatch admission; free-form-reason exclusion; and absence of independent
serialization APIs.

The structured invariant is
:math:`u_{\mathrm{analyzer}}\ne u_{\mathrm{record}}`. Direct construction
requires two nonempty strings. It performs no trimming, case folding,
normalization, registry lookup, conversion, dimensional analysis, or physical-
unit validation. ``"eV"`` and ``"EV"`` therefore form a software mismatch,
without asserting physical inequivalence. The public fields—not parsed message
text—are authoritative.

``HermiticityAnalyzer`` separately owns production mismatch detection and
propagation. These direct exception tests construct no Analyzer,
``OperatorRecord``, matrix, tolerance, or residual. No exception wire format is
approved; ``OperatorRecordJsonSerializer`` serializes only ``OperatorRecord``.
This is software verification only. Numerical Hermiticity, unit suitability,
conversion-factor correctness, scientific validation, uncertainty
quantification, and Rust conformance are not established. Detailed traceability
is in :doc:`operator-record-hermiticity`.

HermiticityRequirementError software evidence
---------------------------------------------

``SV-HRE-001`` through ``SV-HRE-007`` verify the cohesive direct-construction
contract for ``HermiticityRequirementError``. Evidence covers public
``ValueError`` taxonomy, exact identity retention of one failed
``HermiticityResult``, stable semantic human-readable diagnostics, ``TypeError``
for representative wrong result types, ``ValueError`` for all correctly typed
successful states including ``residual == tolerance``, free-form-reason
exclusion, and absence of independent serialization APIs.

The retained Result is authoritative machine-readable evidence: residual
:math:`\varepsilon_{\mathrm H}`, tolerance :math:`\tau`, and energy unit remain
on ``error.result`` rather than being reconstructed or duplicated as exception
fields. ``HermiticityAnalyzer.require()`` owns production emission, while these
tests construct the exception directly to verify that it independently enforces
the strict failure invariant :math:`\varepsilon_{\mathrm H}>\tau`. The message
is secondary human-readable text and is not a parsing protocol.

This is software verification of in-memory exception structure and error
taxonomy. Matrix residual calculation, Analyzer execution and propagation, unit
mismatch, and nonfinite numerical behavior belong to their owning evidence
surfaces. No exception or retained-Result wire format is approved;
``OperatorRecordJsonSerializer`` serializes only ``OperatorRecord``. Numerical
verification of the Hermiticity residual, physical tolerance suitability,
physical Hermiticity, DFT or Wannier validity, model validity, scientific
validation, uncertainty quantification, and Rust conformance are not established.
Detailed traceability is in :doc:`operator-record-hermiticity`.

OperatorRecordComparisonResult software evidence
------------------------------------------------

``SV-ORCR-001`` through ``SV-ORCR-013`` verify direct construction and value
state for ``OperatorRecordComparisonResult``. The evidence covers valid public
fields, accepted NumPy scalar canonicalization, positive structural dimensions,
absence of unapproved serialization methods, identifiers and units, dimension
and residual-scalar admission, exact metric ordering, rejection of raw
roundoff-inconsistent state, huge-integer conversion taxonomy, immutable slotted
state, and exact structural equality.

These are software invariants. ``OperatorRecordResidualAnalyzer`` separately
owns metric computation, floating-point allowance, and permitted upward
canonicalization before constructing a result. The ResultObject contains no
physical acceptance threshold and has no approved JSON wire format. Numerical
verification is not applicable to direct ResultObject construction; scientific
validation and uncertainty quantification have not been performed. Hash behavior
is not specified by this evidence surface.

OperatorRecordCompatibilityMismatchCode software evidence
----------------------------------------------------------

``SV-OCMC-001`` through ``SV-OCMC-006`` verify the public enumeration contract
for ``OperatorRecordCompatibilityMismatchCode``. Evidence covers exact names,
stable values, canonical order, Python ``StrEnum`` and machine-string behavior,
name/value lookup round trips, unique values and absence of aliases, canonical
public descriptions, and exact invalid-lookup exception categories.

The independently written expected-contract table in the migrated cohesive test
module is not generated from the enum implementation. Enum order is public
because ``tuple(OperatorRecordCompatibilityMismatchCode)`` defines the canonical
compatibility-rule order used by compatibility results and analyzers. Values are
stable machine-readable ASCII snake-case strings; descriptions are human-facing
and must not replace those values in serialization or cross-language logic.
Reachability from independently valid record pairs and analyzer correctness
belong to ``OperatorRecordCompatibilityAnalyzer`` software-verification tests.
The evidence supports deterministic Python-to-other-language mapping but does
not establish existence or conformance of a Rust implementation. Scientific
validation and uncertainty quantification have not been performed.

OperatorRecordCompatibilityIssue software evidence
---------------------------------------------------

``SV-OCI-001`` through ``SV-OCI-007`` verify the public value-object contract for
``OperatorRecordCompatibilityIssue``. Evidence covers construction from a public
mismatch-code member, canonical description derivation for every public code,
rejection of non-code values and independently supplied free-form descriptions,
immutable slotted state, exact structural equality by code, and absence of
unsupported serialization APIs.

The Issue stores one authoritative ``OperatorRecordCompatibilityMismatchCode``
and derives ``description`` from that code; it cannot retain contradictory
free-form text. Exact description wording and enum-description uniqueness remain
owned by the mismatch-code contract under ``SV-OCMC-005`` rather than duplicated
here. Hash behavior is not specified by this evidence. The structure is
conceptually portable to a Rust value object with one enum field and a derived
description method, but Rust implementation and conformance are not established.
Mismatch reachability, analyzer correctness, actual operator compatibility,
scientific validation, and uncertainty quantification are not established.

OperatorRecordCompatibilityResult software evidence
----------------------------------------------------

``SV-ORCAR-001`` through ``SV-ORCAR-013`` verify direct construction,
invariants, and value semantics for ``OperatorRecordCompatibilityResult``.
Evidence covers compatible empty state; canonical single, multiple, and complete
Issue sequences; derivation of the full ``rules_applied`` tuple and
``is_compatible``; constructor exclusion of derived state; identifier taxonomy;
exact built-in tuple and public Issue element boundaries; duplicate-code and
canonical-order enforcement; immutable slotted state; exact structural equality;
and absence of unsupported serialization APIs.

The ResultObject stores only reference identifier, candidate identifier, and the
exact Issue tuple. Rule sequence and compatibility are derived. Exact mismatch-
code membership and order remain owned by ``SV-OCMC-001``; these ResultObject
tests verify derivation and structural admission without duplicating the full
enum table. No evidence fixture uses an Issue or Result as a set member or
dictionary key, and hash behavior is not specified. Rule execution and mismatch
reachability belong to ``OperatorRecordCompatibilityAnalyzer``. No independent
ResultObject wire format is approved. Rust conformance, scientific validation,
and uncertainty quantification have not been performed.

OperatorRecordCompatibilityAnalyzer software evidence
------------------------------------------------------

``SV-ORCA-001`` through ``SV-ORCA-019`` verify the public ActionObject contract
for ``OperatorRecordCompatibilityAnalyzer``. Evidence covers default public
construction; complete compatible audit results; independent variation of every
ignored identity, descriptive, and provenance field; reachability of every
public mismatch code from independently valid records; canonical deterministic
multiple-finding order; value-equivalent ``execute()`` and ``require()`` success;
structured incompatibility propagation; and independent reference/candidate type
boundaries for both public methods.

The matrix-dimension case intentionally also reports ordered-basis-label mismatch
because every valid record requires matrix dimension, state-space dimension, and
basis-ordering length to agree. The tests do not bypass frozen-object invariants
to claim independent dimension reachability. ``SV-ORCA-015`` uses the public enum
as the sole canonical-order owner and uses set equality only as a separate code-
membership coverage check. Exact ResultObject construction invariants remain
owned by ``SV-ORCAR-001`` through ``SV-ORCAR-013``.

The Analyzer evidence is software verification of exact representation metadata
for direct subtraction. It performs no numerical approximation and establishes
no physical equivalence, basis or gauge alignment, energy-zero alignment, unit
conversion, geometry transformation, equivalent DFT/Wannier provenance,
scientific validation, or uncertainty quantification. Detailed traceability is
in :doc:`operator-record-compatibility-analysis`.

IncompatibleOperatorRecordsError software evidence
--------------------------------------------------

``SV-IORE-001`` through ``SV-IORE-006`` verify the narrow direct-construction
contract for ``IncompatibleOperatorRecordsError``. Evidence covers public
``ValueError`` taxonomy, exact identity retention of the supplied incompatible
``OperatorRecordCompatibilityResult``, semantic human-readable mismatch-code
summarization, ``TypeError`` for representative wrong input types, ``ValueError``
for a correctly typed compatible Result, and absence of independent exception
serialization APIs.

The retained Result is authoritative machine-readable state containing reference
and candidate roles and the canonical ordered Issue tuple. Message checks do not
freeze incidental punctuation or duplicate canonical description evidence.
Analyzer propagation remains owned by ``SV-ORCA-017``; these tests construct the
exception directly. The exception has no approved JSON, dictionary, pickling, or
Rust wire contract.

This evidence verifies software failure-state structure only. It computes no
numerical norm and establishes no physical incompatibility, impossibility of a
future alignment or conversion, scientific validity of compatibility rules,
scientific validation, uncertainty quantification, or Rust conformance. Detailed
traceability is in :doc:`operator-record-compatibility-analysis`.

OperatorRecordDifferenceNumericalErrorCode software evidence
-------------------------------------------------------------

``SV-ORDNEC-001`` through ``SV-ORDNEC-006`` verify the exact closed public
enumeration contract for ``OperatorRecordDifferenceNumericalErrorCode``. The
evidence covers the sole member ``NONFINITE_DIFFERENCE`` with stable value
``nonfinite_difference``, deterministic one-member declaration order, explicit
alias absence through ``Enum.__members__``, Python 3.14 ``StrEnum`` behavior,
ASCII lowercase snake-case form, name/value lookup round trips, and exact
``ValueError`` versus ``KeyError`` invalid-lookup taxonomy.

The code categorizes a represented-difference failure owned by
``OperatorRecordDifferencer``: subtracting two individually finite, compatible
matrices produced a nonfinite entry in ``candidate - reference``. The enum itself
does not subtract matrices or detect nonfinite values. Differencer overflow
production evidence remains with the ActionObject, and exception construction
remains with ``OperatorRecordDifferenceNumericalError``. Residual-analysis
failures for nonfinite metrics, SVD failure, and metric-order violation retain a
separate taxonomy.

Stable string behavior supports future conceptual mapping to a Rust error enum,
but no Rust implementation or conformance is established. These are software-
verification tests of classification vocabulary, not numerical verification of
subtraction or evidence that a matrix operation is scientifically acceptable.
Scientific validation and uncertainty quantification have not been performed.
Detailed traceability is in :doc:`operator-record-difference`.

OperatorRecordDifferenceNumericalError software evidence
---------------------------------------------------------

``SV-ORDNE-001`` through ``SV-ORDNE-006`` verify the direct public exception
contract for ``OperatorRecordDifferenceNumericalError``. Evidence covers public
construction and ``ValueError`` taxonomy, complete current difference-code
admission, exact enum identity retention through ``error.code``, semantic human-
readable message content, representative invalid-code ``TypeError`` rejection,
free-form-reason exclusion, and absence of independent exception serialization
APIs.

The retained ``OperatorRecordDifferenceNumericalErrorCode`` member is the
authoritative machine-readable category. The message is secondary human-readable
text containing the stable code value and is not a parsing protocol. Raw strings
and unrelated enum members are rejected rather than coerced. The constructor
accepts no extra positional or keyword ``reason``, and a valid instance exposes
no ``reason`` attribute.

``OperatorRecordDifferencer`` separately owns production of the exception after
nonfinite represented subtraction and is not executed by this direct-construction
evidence. Residual-analysis codes ``NONFINITE_METRIC``,
``LINEAR_ALGEBRA_FAILURE``, and ``METRIC_ORDER_VIOLATION`` belong to a different
exception taxonomy. Schema version 1 serializes only ``OperatorRecord``; there is
no numerical-exception JSON schema or approved exception wire format.

This is software verification of in-memory exception structure and error
taxonomy, not numerical verification of subtraction accuracy. It establishes no
physical compatibility, scientific acceptability, scientific validation,
uncertainty quantification, Rust implementation, or Rust conformance. Detailed
traceability is in :doc:`operator-record-difference`.

OperatorRecordComparisonNumericalErrorCode software evidence
-------------------------------------------------------------

``SV-ORCNEC-001`` through ``SV-ORCNEC-006`` verify the exact closed public enum
contract for ``OperatorRecordComparisonNumericalErrorCode``. Evidence covers the
three-member sequence ``NONFINITE_METRIC = "nonfinite_metric"``,
``LINEAR_ALGEBRA_FAILURE = "linear_algebra_failure"``, and
``METRIC_ORDER_VIOLATION = "metric_order_violation"`` in declaration order;
explicit alias absence through ``Enum.__members__``; Python 3.14 ``StrEnum`` and
ASCII snake-case behavior; name/value lookup identity round trips; and exact
``ValueError`` versus ``KeyError`` invalid-lookup taxonomy.

Despite the retained historical type name, ``OperatorRecordResidualAnalyzer``
owns production emission of these residual-analysis categories.
``OperatorRecordComparator`` only propagates lower-layer exceptions. A nonfinite
represented subtraction belongs instead to
``OperatorRecordDifferenceNumericalErrorCode.NONFINITE_DIFFERENCE``.
``NONFINITE_METRIC`` covers a residual metric not representable as finite
binary64; ``LINEAR_ALGEBRA_FAILURE`` covers SVD failure or nonfinite singular
values; ``METRIC_ORDER_VIOLATION`` covers raw norm order defects larger than the
analyzer-owned allowance. Within-allowance differences are canonicalized rather
than reported as violations.

The enum evidence is software verification of stable classification vocabulary.
Production error translation remains under ``SV-ORA`` evidence, while residual-
metric accuracy and floating-point behavior remain under ``NV-ORA`` evidence.
No serialized exception format is approved. Rust mapping is conceptual only;
Rust implementation and conformance, scientific validation, and uncertainty
quantification have not been performed. Detailed traceability is in
:doc:`operator-record-residual-analyzer`.

OperatorRecordComparisonNumericalError software evidence
----------------------------------------------------------

``SV-ORCNE-001`` through ``SV-ORCNE-008`` verify the cohesive direct-
construction contract for ``OperatorRecordComparisonNumericalError``. Evidence
covers public ``ValueError`` hierarchy; complete admission of
``NONFINITE_METRIC``, ``LINEAR_ALGEBRA_FAILURE``, and
``METRIC_ORDER_VIOLATION``; exact enum identity retention through ``error.code``;
positional and ``code=`` keyword construction; semantic human-readable code
summaries; ``TypeError`` rejection of ``None``, Booleans, integer, every raw code
string, unrelated enum members, and arbitrary objects; continued absence and
keyword rejection of the former ``reason`` alias; arbitrary-detail exclusion;
and absence of independent serialization APIs.

``code`` is the sole authoritative structured category. The message is secondary
human-readable text containing the stable code value and is not a parsing
protocol. Raw strings are not coerced, no free-form ``detail`` field is accepted,
and ``OperatorRecordJsonSerializer`` serializes only ``OperatorRecord``. Exact
enum vocabulary, order, aliases, ``StrEnum`` behavior, and lookups remain owned
by ``SV-ORCNEC-001`` through ``SV-ORCNEC-006``.

Despite the historical ``Comparison`` name, ``OperatorRecordResidualAnalyzer``
owns production emission. ``OperatorRecordComparator`` may propagate this lower-
layer exception but does not create residual metrics or own the taxonomy. The
exception is distinct from ``OperatorRecordDifferenceNumericalError`` for
represented-subtraction failure, ``HermiticityNumericalError`` for nonfinite
Hermiticity residual production, and ``IncompatibleOperatorRecordsError`` for
exact metadata incompatibility.

Direct construction executes no norm, SVD, floating-point allowance,
canonicalization, Analyzer, or Workflow behavior. Production error emission
belongs to ``SV-ORA``, propagation belongs to ``SV-ORC``, and metric accuracy
belongs to ``NV-ORA``. Passing establishes the in-memory exception boundary, not
scientific acceptability of a residual. Scientific validation, uncertainty
quantification, and Rust conformance have not been performed; no exception wire
format is approved. Detailed traceability is in
:doc:`operator-record-residual-analyzer`.

OperatorRecordComparator Workflow software evidence
---------------------------------------------------

``SV-ORC-001`` through ``SV-ORC-007`` verify the genuine concrete production
Workflow ``OperatorRecordComparator``. Evidence covers default dependency
construction, identity retention for explicit dependencies, equality with
explicit differencer-then-residual-analyzer composition, field-specific
injection rejection, and unchanged propagation of representative structured
compatibility, subtraction, and residual-analysis failures.

The Workflow owns sequencing and dependency composition only. Compatibility
rules and signed subtraction belong to ``OperatorRecordDifferencer`` and its
compatibility dependency; norm algorithms, floating-point scaling, roundoff
allowance, and metric canonicalization belong to
``OperatorRecordResidualAnalyzer``. Independent norm accuracy remains under
``NV-ORA-001`` through ``NV-ORA-017``. The Workflow is not a technical-
integration owner or generic Workflow base class and introduces no physical
acceptance threshold. Scientific validation and uncertainty quantification have
not been performed.

OperatorRecordJsonSerializer and JSON-artifact software evidence
----------------------------------------------------------------

``SV-ORJS-001`` through ``SV-ORJS-018`` verify the serializer ActionObject across
five facets: public contract, deterministic fixed-field encoding, structural
JSON decoding, value semantics and invariant propagation, and exact round trips.
The exact round-trip corpus includes empty provenance, general non-Hermitian
complex matrices, extreme finite binary64 components, defensive ownership, and
operational immutability. Approximate comparisons are not used.

``SV-ORJSC-001`` through ``SV-ORJSC-003`` separately own the public draft-2020-12
JSON Schema: metamodel validity, conformance of actual serializer output and all
valid fixtures, and rejection of every golden invalid class expressible by the
schema. Runtime-only cross-field and numerical-structure constraints are stated
as exclusions rather than incorrectly attributed to JSON Schema.

``SV-ORJF-001`` through ``SV-ORJF-003`` separately own exact golden-file
inventory, deterministic valid-fixture interoperability, and exact-category
invalid-fixture rejection. These integration tests enumerate artifacts but do
not duplicate detailed runtime-facet assertions. The established ``jsonschema``
dependency is controlled as an independent validator; its own implementation is
not validated.

All three prefixes are software-verification evidence for synthetic records and
wire artifacts. Passing establishes no physical Hamiltonian validity, scientific
validation, uncertainty quantification, Rust implementation, or Python/Rust
conformance. Detailed traceability is in
:doc:`operator-record-json-serialization`.

CPN P1 class-ownership evidence
-------------------------------

``SV-CPN-001`` through ``SV-CPN-088`` cover the bounded project-owned CPN
contract. Eighty-eight test functions/evidence owners, collecting 91 parameter
cases, are partitioned into 32 class-owned ``test__ClassName.py`` modules under
the canonical workflow/CPN software-verification directory and five
artifact- or boundary-owned integration modules. The machine-readable manifest inventories
all 49 public exports, including 17 classified enum/marker exceptions. Detailed
ownership, commands, exclusions, and the resolved numeric-wire boundary are
recorded in :doc:`cpn-contract`.

The human-authorized controlled migration is complete for all 32 maintained
class-owned CPN modules and the five maintained artifact- or boundary-owned
integration modules.  Their 88 evidence owners retain ``SV-CPN-001`` through
``SV-CPN-088`` and now use the unified module/test/helper grammar and semantic
test names.  Complete one-to-one old/new pytest node mappings provide rename
traceability; for example, current nodes include
``test__CpnToken.py::test_field__iteration_index__rejects_boolean`` and
``test__workflow_cpn_python_public_api.py::test_artifact__public_api__exposes_approved_export_inventory``.
Protected historical modules remain unchanged.

This documentation and filename migration records structural ownership and
traceability only.  Path changes are not new evidence, semantic validation,
numerical verification, scientific validation, uncertainty quantification, or
final acceptance, and they do not establish persistence, adapter, or
cross-language behavior.

Traceability and review
-----------------------

Evidence identifiers connect public requirements, executable tests, Sphinx
summaries, and task records.  Detailed assertions remain in test modules;
Sphinx records the common standard and summarizes maintained numerical evidence.
Documentation and tests must remain synchronized as migration proceeds one
approved object or subsystem at a time.

Structural review checks exact heading and field occurrence/order, nonempty
field bodies, marker/prefix/hierarchy/owner agreement, identifier uniqueness,
helper nonownership, semantic name form, explicit primary SUT or artifact owner,
parameter IDs, node-ID mappings, and separation of evidence classes.  Semantic
review separately checks that requirements are public and non-tautological,
methods exercise public boundaries, oracles are genuinely independent,
acceptance follows exact-representation or justified-tolerance policy, and
units, shapes, scales, warnings, zeros, boundaries, interpretations, and
limitations are adequate.  It also checks that assertions, fixtures, schemas,
source, specification, and documentation preserve the same scientific and
public-contract meaning.

Structural tooling reports syntax and inventory conformance only.  It cannot
establish oracle independence, mathematical correctness, tolerance adequacy,
scientific validity, uncertainty-quantification adequacy, or human acceptance;
those require semantic review and, where protected, human authority.
