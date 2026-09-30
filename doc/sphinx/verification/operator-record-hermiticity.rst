OperatorRecord Hermiticity software verification
=================================================

This page records focused software-verification evidence for the direct public
contracts of ``HermiticityUnitMismatchError``,
``HermiticityNumericalErrorCode``, ``HermiticityNumericalError``, and
``HermiticityRequirementError`` and places
that evidence within the larger
Hermiticity subsystem. It does not independently verify the numerical residual
algorithm or establish physical Hermiticity.

Hermiticity objects and ownership
---------------------------------

``HermiticityUnitMismatchError``
   Structured ``ValueError`` retaining the Analyzer-policy unit and record-
   metadata unit in separate ordered fields when those strings differ exactly.
   It performs no analysis or conversion.

``HermiticityNumericalErrorCode``
   Closed Python 3.14 ``StrEnum`` vocabulary for Analyzer-owned numerical
   failure classification. It performs no matrix operation or detection.

``HermiticityNumericalError``
   Structured ``ValueError`` retaining one exact
   ``HermiticityNumericalErrorCode`` through the public ``reason`` field.

``HermiticityResult``
   Immutable structured analysis result retaining residual
   :math:`\varepsilon_{\mathrm H}`, tolerance :math:`\tau`, and their common
   ``energy_unit``. Its public ``is_hermitian`` property is the authoritative
   interpretation of those stored values.

``HermiticityRequirementError``
   Structured ``ValueError`` enforcement failure retaining the exact failed
   ``HermiticityResult`` through ``error.result``. Its message is a secondary
   human-readable diagnostic, not a machine-parsing protocol.

``HermiticityAnalyzer.require()``
   Production ActionObject operation that executes the analysis, returns a
   successful Result, or raises ``HermiticityRequirementError`` with the failed
   Result. Direct exception tests do not invoke this operation; they verify that
   the exception independently protects its own invariant.

HermiticityResult software contract
-----------------------------------

``HermiticityResult`` is a frozen, slotted ResultObject with exactly three stored
fields:

``residual``
   The non-negative finite binary64 Hermiticity residual
   :math:`\varepsilon_{\mathrm H}`.

``tolerance``
   The non-negative finite binary64 acceptance tolerance :math:`\tau` recorded
   for the analysis.

``energy_unit``
   The nonempty Python string naming the common energy unit of both stored
   scalars.

The mathematical residual represented by the first field is

.. math::

   \varepsilon_{\mathrm H}
   =
   \max_{i,j}\left|H_{ij}-H_{ji}^{*}\right|.

Direct ResultObject construction does not compute this expression and stores no
matrix or ``OperatorRecord``. The declared constructor input contract includes
Python integer and floating scalars and NumPy integer and floating scalars for
both ``residual`` and ``tolerance``; each is canonicalized to a built-in stored
``float``. Because Python static integer typing includes Boolean values, Boolean
rejection is an explicit runtime semantic refinement rather than a precisely
expressible static exclusion. Booleans, numeric
strings, bytes, complex values, and arbitrary objects raise ``TypeError`` with a
field-specific real-number diagnostic. NaN, infinities, and accepted integers
that overflow binary64 conversion raise ``ValueError`` under the field-specific
finite-number taxonomy; raw ``OverflowError`` is not exposed. Finite negative
values raise ``ValueError``. The energy unit follows the existing
``isinstance(value, str)`` policy: non-strings raise ``TypeError`` and the empty
string raises ``ValueError``. No trimming, normalization, case folding, unit
registry, or conversion is performed; a whitespace-only string remains nonempty
under this policy.

``is_hermitian`` is derived rather than stored:

.. math::

   \texttt{is\_hermitian}
   \iff
   \varepsilon_{\mathrm H}\leq\tau.

The boundary is inclusive, including exact ``0.0 <= 0.0``, and uses direct
comparison of the stored binary64 values rather than approximate comparison.
Callers cannot supply ``is_hermitian`` as positional or keyword constructor
state. Exact structural equality compares all three stored fields; it is not
approximate equality or scientific equivalence. The object has no instance
``__dict__`` and ordinary assignment to any stored field is rejected. Hash
behavior is not part of this evidence contract.

``SV-HR-001`` through ``SV-HR-015`` verify construction and field mapping,
accepted scalar-family canonicalization, the inclusive predicate, derived-field
constructor exclusion, serialization exclusion, independent residual and
tolerance type/finiteness/sign taxonomy, energy-unit typing and nonemptiness,
frozen slotted state, and exact structural equality. The cohesive facets are
``test__HermiticityResult__construction.py``,
``test__HermiticityResult__invariants.py``, and
``test__HermiticityResult__value_semantics.py`` under the target software-
verification hierarchy, each marked only ``software_verification``.

The ResultObject contains no Analyzer policy beyond the recorded tolerance, unit
conversion, scientific acceptance criterion, physical provenance, or independent
serialization behavior. ``OperatorRecordJsonSerializer`` serializes only
``OperatorRecord``; no ResultObject, retained-result exception, or numerical-
exception wire format is approved. ``HermiticityAnalyzer`` separately owns
matrix residual computation, tolerance application, unit matching, and production
Result construction. Structured Hermiticity exceptions separately own their
failure states. ResultObject tests therefore provide software verification only:
they do not establish Analyzer numerical correctness, appropriateness of
:math:`\tau`, physical Hermiticity, DFT or Wannier validity, scientific
validation, uncertainty quantification, or Rust conformance.

HermiticityAnalyzer software and numerical evidence
----------------------------------------------------

For a stored matrix :math:`H`, ``HermiticityAnalyzer`` returns

.. code-block:: python

   HermiticityResult(
       residual=epsilon_H,
       tolerance=tau,
       energy_unit=u,
   )

where

.. math::

   \varepsilon_{\mathrm H}
   =
   \max_{i,j}\left|H_{ij}-H_{ji}^{*}\right|,

and ``is_hermitian`` is true exactly when
:math:`\varepsilon_{\mathrm H}\leq\tau`. The Analyzer owns :math:`\tau`; it is
not stored on ``OperatorRecord`` and this evidence does not determine a
scientifically appropriate tolerance. The required unit contract is exact:

.. math::

   u_{\mathrm{analyzer}}=u_{\mathrm{record}}.

No trimming, normalization, registry lookup, or unit conversion is performed.
Unit agreement is checked before residual arithmetic. A mismatch raises
``HermiticityUnitMismatchError`` with the Analyzer and record unit roles
retained. A finite residual above tolerance causes ``require()`` to raise
``HermiticityRequirementError`` retaining the failed Result. Nonfinite residual
formation raises ``HermiticityNumericalError`` with exact reason
``NONFINITE_RESIDUAL``. Overflow-focused evidence promotes ``RuntimeWarning`` to
an error and requires the structured exception rather than a leaked NumPy
warning.

``SV-HA-001`` through ``SV-HA-010`` verify explicit configuration, Python and
NumPy integer/floating tolerance admission and built-in-float canonicalization,
invalid semantic types, nonfinite and conversion-overflow rejection, negative
rejection, required explicit unit, unit typing and nonemptiness, frozen/slotted
state, and serialization exclusion. ``SV-HA-011`` through ``SV-HA-019`` verify
the independent ``execute()`` and ``require()`` input boundaries, public Result
construction, exact unit mismatch and unit-before-arithmetic ordering,
``require()`` success and structured failure, Analyzer-owned tolerance policy,
and structured warning-free nonfinite-residual failure. These are owned by the
``configuration`` and ``contract`` software-verification modules and are marked
only ``software_verification``.

``NV-HA-001`` through ``NV-HA-005`` provide separate numerical verification:

* an exactly Hermitian complex matrix gives exact residual ``0.0``;
* ``[[1, 2+i], [3+4i, 4]]`` gives :math:`\sqrt{26}` because the upper
  residual is :math:`-1+5i`;
* ``[[1, 2], [3, 4]]`` gives residual ``1``;
* a genuine similarity :math:`U^\dagger H U` using an exactly representable
  diagonal-phase unitary preserves exact zero; and
* the approved non-Hermitian matrix has residual ``1`` before a discrete-Fourier
  basis change and :math:`1/\sqrt{3}` afterward.

Hermiticity itself is invariant under unitary basis transformations: exact zero
remains zero under the exact unitary case. The nonzero entrywise maximum
residual is generally not unitarily invariant, so its magnitude can change with
basis without changing zero-versus-nonzero Hermiticity status.

Exact analytical zero is accepted only by ``actual == 0.0``. For the small
normal-scale nonzero analytical cases, acceptance is

.. math::

   |x_{\mathrm{actual}}-x_{\mathrm{expected}}|
   \leq
   64\epsilon_{\mathrm{mach}}|x_{\mathrm{expected}}|,

with actual, expected, and allowed error required to be nonzero and the allowed
error required to be smaller than the expected magnitude. This local binary64
criterion is not a production tolerance policy, scientific acceptance policy,
or arbitrary-dimension forward-error theorem. Every numerical Analyzer
execution treats ``RuntimeWarning`` as an error.

Passing ``SV-HA`` establishes public ActionObject behavior and structured failure
taxonomy. Passing ``NV-HA`` establishes agreement with five small analytical
matrix cases under the stated binary64 criterion. Neither establishes physical
Hermiticity of DFT output, basis or gauge correctness, DFT or Wannier accuracy,
model validation, scientific appropriateness of :math:`\tau`, uncertainty
quantification, arbitrary-dimension guarantees, or Rust conformance. Scientific
validation and uncertainty quantification have not been performed.

Unit-mismatch invariant
-----------------------

The Analyzer tolerance policy declares one energy-unit string
:math:`u_{\mathrm{analyzer}}`. ``OperatorRecord.energy_reference.unit`` supplies
the represented matrix and residual metadata string :math:`u_{\mathrm{record}}`.
``HermiticityAnalyzer`` owns production detection before residual calculation.
It raises ``HermiticityUnitMismatchError`` exactly when

.. math::

   u_{\mathrm{analyzer}} \ne u_{\mathrm{record}}.

The exception constructor independently requires two nonempty strings and
rejects equal strings. A wrong semantic type raises ``TypeError`` with the
invalid role; an empty or equal correctly typed string state raises
``ValueError``. Comparison is exact and case-sensitive. Thus ``"eV"`` and
``"EV"`` form a software mismatch, while ``"eV"`` and ``"eV"`` cannot form a
mismatch exception. This says nothing about whether differently cased strings
name physically distinct units.

The constructor retains the roles without swapping them:
``error.analyzer_energy_unit`` is the Analyzer-policy string and
``error.record_energy_unit`` is the record-metadata string. Exact disagreement
prevents applying the Analyzer tolerance to the represented residual without a
separately approved conversion. No trimming, normalization, case folding, unit
registry, conversion factor, dimensional analysis, or physical-unit validation
is performed.

The human-readable message identifies both labeled roles and values, but the two
fields are authoritative programmatic state. No free-form ``reason`` is accepted
or exposed. The exception has no JSON, dictionary, serializer, or deserializer
API; ``OperatorRecordJsonSerializer`` serializes only ``OperatorRecord``. No unit-
mismatch exception wire format or Rust conformance implementation is approved.

``SV-HUME-001`` through ``SV-HUME-008`` verify direct construction and hierarchy,
ordered role retention, semantic diagnostic content, wrong-type rejection,
empty-string rejection, equal-string rejection and case-sensitive mismatch,
free-form-reason exclusion, and serialization exclusion. Their cohesive owner is
``python/tests/software_verification/ksdft2effmass/operators/test__HermiticityUnitMismatchError.py``
and carries only the ``software_verification`` marker. Analyzer detection and
propagation remain in the Analyzer's own evidence surface.

Closed numerical-error code
---------------------------

The exact public enumeration contract is one member in declaration order:

.. code-block:: python

   class HermiticityNumericalErrorCode(StrEnum):
       NONFINITE_RESIDUAL = "nonfinite_residual"

``NONFINITE_RESIDUAL`` means that ``HermiticityAnalyzer`` could not produce a
finite binary64 value for

.. math::

   \varepsilon_{\mathrm H}
   =
   \max_{i,j}\left|H_{ij}-H_{ji}^{*}\right|.

Stored matrix entries can each be finite while forming :math:`H-H^\dagger`
overflows. The Analyzer owns production detection and emission. The enum owns
only the stable category vocabulary; it performs no subtraction, maximum
reduction, finite check, or exception construction.

The public registry contains exactly the declared name ``NONFINITE_RESIDUAL``
and no aliases. As a Python 3.14 ``StrEnum``, the member is also a string,
``str(code)`` is ``"nonfinite_residual"``, value lookup uses
``HermiticityNumericalErrorCode("nonfinite_residual")``, and name lookup uses
``HermiticityNumericalErrorCode["NONFINITE_RESIDUAL"]``. The stable value is an
ASCII lowercase snake-case identifier. This in-memory behavior supports a future
conceptual Rust-enum mapping but establishes no Rust implementation, conformance,
or serialized numerical-exception format.

This code is distinct from unit disagreement
(``HermiticityUnitMismatchError``), a finite residual exceeding tolerance
(``HermiticityRequirementError``), nonfinite represented subtraction
(``OperatorRecordDifferenceNumericalErrorCode.NONFINITE_DIFFERENCE``), and
residual-comparison numerical failures
(``OperatorRecordComparisonNumericalErrorCode``). A nonfinite residual is a
software/numerical failure, not evidence that the physical Hamiltonian is non-
Hermitian.

``SV-HNEC-001`` through ``SV-HNEC-006`` verify exact member sequence and value,
no aliases, Python 3.14 ``StrEnum`` behavior, value and name lookup identity, and
``ValueError`` versus ``KeyError`` invalid-lookup taxonomy. Their cohesive owner
is
``python/tests/software_verification/ksdft2effmass/operators/test__HermiticityNumericalErrorCode.py``.
These enum-contract tests are software verification. Analyzer emission remains
Analyzer software-verification evidence, while residual accuracy belongs to
numerical verification. Scientific validation and uncertainty quantification
are not established.

Structured numerical exception
------------------------------

``HermiticityNumericalError(reason)`` is a public ``ValueError`` whose sole
structured constructor field is ``reason``. The constructor accepts exactly a
``HermiticityNumericalErrorCode`` member, either positionally or through the
``reason=`` keyword, and retains the exact enum object by identity. Raw strings,
Booleans, integers, unrelated enum members, and arbitrary objects raise
``TypeError`` rather than being coerced.

The approved public structured field remains ``reason``. Here ``reason`` is a
closed machine-readable category, not free-form prose. No additional
positional or keyword ``detail`` is accepted or exposed. The human-readable
message identifies a Hermiticity numerical failure and includes the stable enum
value, but ``error.reason`` is authoritative and callers need not parse the
message.

``HermiticityAnalyzer`` owns production emission when it cannot produce a finite
residual. Direct exception tests do not invoke the Analyzer or reproduce matrix
overflow. Unit disagreement remains ``HermiticityUnitMismatchError``; a finite
residual exceeding tolerance remains ``HermiticityRequirementError``. A
``HermiticityNumericalError`` means a finite residual result could not be
represented, not that a finite residual was calculated and found too large.

No numerical-exception JSON or dictionary format is approved.
``OperatorRecordJsonSerializer`` serializes only ``OperatorRecord``. ``StrEnum``
string compatibility does not create a wire contract. A future Rust mapping
would use a closed error enum, but no Rust serialization, implementation, or
conformance evidence exists.

``SV-HNE-001`` through ``SV-HNE-007`` verify direct construction and
``ValueError`` hierarchy, complete enum admission and exact reason identity,
positional/keyword forms, semantic diagnostics, invalid-type rejection, extra-
detail exclusion, and serialization exclusion. Their cohesive owner is
``python/tests/software_verification/ksdft2effmass/operators/test__HermiticityNumericalError.py``.
The enum vocabulary remains owned by ``SV-HNEC-001`` through ``SV-HNEC-006``;
Analyzer emission remains Analyzer software-verification evidence, and residual
accuracy/overflow behavior remain numerical-verification scope. Scientific
validation and uncertainty quantification are not established.

Criterion and equality boundary
-------------------------------

For a fixed represented matrix :math:`H`, the Analyzer defines

.. math::

   \varepsilon_{\mathrm H}
   =
   \max_{i,j}\left|H_{ij}-H_{ji}^{*}\right|.

Residual and tolerance have the Result's explicit energy unit. Acceptance is
inclusive:

.. math::

   \varepsilon_{\mathrm H}\leq\tau.

The requirement exception therefore represents only the strict failure state

.. math::

   \varepsilon_{\mathrm H}>\tau.

In particular, :math:`\varepsilon_{\mathrm H}=\tau` is successful and the
exception constructor rejects such a Result with ``ValueError``. The constructor
does not recompute the criterion, convert units, or duplicate residual,
tolerance, or unit as exception fields; it uses the existing public
``result.is_hermitian`` property and retains the exact failed Result by identity.

Structured exception contract
-----------------------------

The constructor accepts exactly one ``HermiticityResult``. A wrong semantic type
raises ``TypeError``. A correctly typed but successful Result raises
``ValueError`` because it would create contradictory failure state. The
exception itself remains a ``ValueError`` subtype.

No positional or keyword free-form ``reason`` is accepted, and a valid exception
has no public ``reason`` attribute. Callers inspect ``error.result`` for
programmatic residual, tolerance, unit, and success state rather than parsing
``str(error)``. The accepted message contract promises the semantic statement
that the operator matrix is not Hermitian within tolerance; incidental
punctuation, capitalization, float formatting, and separators are not frozen by
this evidence.

No exception wire format is approved. ``HermiticityRequirementError`` exposes no
``to_json``, ``to_dict``, ``serialize``, ``from_json``, ``from_dict``, or
``deserialize`` API. ``OperatorRecordJsonSerializer`` serializes only
``OperatorRecord`` under schema version 1. The retained ``HermiticityResult`` has
no approved JSON schema in this task. Future Rust error mapping remains
conceptual; no Rust implementation or conformance is established.

Executable evidence
-------------------

``SV-HRE-001`` through ``SV-HRE-007`` verify, respectively:

* public construction and ``ValueError``/``Exception`` taxonomy;
* exact failed-Result identity retention and access to retained values;
* stable semantic human-readable failure summary;
* ``TypeError`` rejection of representative wrong result types;
* ``ValueError`` rejection of successful Results, including equality;
* exclusion of positional and keyword free-form reasons; and
* absence of independent exception serialization APIs.

The cohesive owner is
``python/tests/software_verification/ksdft2effmass/operators/test__HermiticityRequirementError.py``
and carries only the ``software_verification`` marker. Analyzer execution,
requirement propagation, matrix residual calculation, unit mismatch, and
nonfinite numerical failures remain in their owning Hermiticity test surfaces.

VVUQ boundaries
---------------

This direct exception evidence is software verification. It verifies public
construction, structured failure-state invariants, identity retention,
diagnostics, and error taxonomy.

It is not numerical verification of :math:`\varepsilon_{\mathrm H}` and does not
verify that a tolerance is suitable for a physical problem. It uses synthetic
scalar Result values without a matrix, DFT record, Wannier representation, or
physical operator. It establishes no DFT or Wannier validity, model validity,
physical Hermiticity, scientific validation, or uncertainty quantification.
Rust conformance has not been performed.
