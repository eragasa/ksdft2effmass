OperatorRecord represented-difference software verification
============================================================

Purpose and ownership
---------------------

``OperatorRecordDifferencer`` owns exact compatibility enforcement, the signed
represented subtraction

.. math::

   \Delta\mathbf H
   =
   \mathbf H_{\mathrm{candidate}}
   -
   \mathbf H_{\mathrm{reference}},

nonfinite-difference detection, and production of represented-difference
numerical errors.  The public
``OperatorRecordDifferenceNumericalErrorCode`` enum supplies the closed
classification vocabulary for those failures.  It does not perform subtraction,
detect nonfinite entries, or construct exceptions.  Exception construction is
owned separately by ``OperatorRecordDifferenceNumericalError``.

Closed numerical-error-code contract
------------------------------------

The exact public enum contains one member:

.. list-table:: Represented-difference numerical-error code
   :header-rows: 1

   * - Declaration order
     - Public member name
     - Stable machine-readable value
     - Meaning
   * - 1
     - ``NONFINITE_DIFFERENCE``
     - ``nonfinite_difference``
     - Subtraction of individually finite, compatible represented matrices
       produced at least one nonfinite entry in :math:`\Delta\mathbf H`.

The enum is a Python 3.14 ``StrEnum``.  Its value behaves as a string and is an
ASCII lowercase snake-case identifier.  Value lookup uses
``OperatorRecordDifferenceNumericalErrorCode(value)``; name lookup uses
``OperatorRecordDifferenceNumericalErrorCode[name]``.  Invalid values raise
``ValueError`` and invalid names raise ``KeyError`` under the standard Enum
lookup taxonomy.  No aliases, descriptions, free-form reasons, integer
discriminants, or serialization methods are part of this enum contract.

The stable member/value pair supports a future conceptual mapping to a Rust
error enum.  No Rust implementation or Python/Rust conformance evidence is
provided.

Structured exception contract
-----------------------------

``OperatorRecordDifferenceNumericalError`` is the public in-memory structured
``ValueError`` for represented-difference numerical failures. Its constructor
accepts exactly one ``OperatorRecordDifferenceNumericalErrorCode`` and retains
the exact supplied enum member by identity in ``error.code``. Every current enum
member is accepted; currently this is only ``NONFINITE_DIFFERENCE``.

The exception message identifies an operator-record difference numerical failure
and contains the stable code value. It is intended for humans and is secondary to
``error.code``; callers must not parse it as a machine protocol. Raw strings,
Booleans, ``None``, arbitrary objects, and members of unrelated enum classes are
rejected with ``TypeError`` rather than coerced. No positional or keyword free-
form ``reason`` is accepted, and a valid exception exposes no ``reason``
attribute.

The exception exposes no independent ``to_json``, ``to_dict``, ``serialize``,
``from_json``, ``from_dict``, or ``deserialize`` API. Schema version 1 applies
only to ``OperatorRecord``. Future Rust mapping is conceptual through the enum
category; no serialized exception format or Rust conformance exists.

Taxonomy separation
-------------------

``NONFINITE_DIFFERENCE`` belongs only to represented subtraction.  Residual
analysis owns distinct failures ``NONFINITE_METRIC``,
``LINEAR_ALGEBRA_FAILURE``, and ``METRIC_ORDER_VIOLATION`` through
``OperatorRecordComparisonNumericalErrorCode``. Difference and residual error
codes are not accepted interchangeably by their exception classes.

Executable evidence
-------------------

``SV-ORDNEC-001`` through ``SV-ORDNEC-006`` verify:

* the exact one-member sequence, name, value, and declaration order;
* explicit absence of aliases through the public ``Enum.__members__`` registry;
* Python 3.14 ``StrEnum`` and ASCII snake-case string behavior;
* value-based and name-based lookup round trips; and
* ``ValueError`` for an invalid value and ``KeyError`` for an invalid name.

The cohesive owner is
``python/tests/software_verification/ksdft2effmass/operators/``
``test__OperatorRecordDifferenceNumericalErrorCode.py``.  Differencer evidence
that subtraction overflow produces ``NONFINITE_DIFFERENCE`` remains with
``OperatorRecordDifferencer`` and is not duplicated by the enum-contract tests.
Direct exception evidence ``SV-ORDNE-001`` through ``SV-ORDNE-006`` verifies:

* public construction and ``ValueError`` taxonomy;
* complete current enum admission and exact code identity retention;
* semantic human-readable diagnostic content with ``error.code`` authoritative;
* ``TypeError`` rejection of raw strings, unrelated enums, and other invalid
  types;
* positional/keyword free-form-reason rejection and absence of ``reason``; and
* absence of independent exception serialization APIs.

Its cohesive owner is
``python/tests/software_verification/ksdft2effmass/operators/``
``test__OperatorRecordDifferenceNumericalError.py``. Actual production emission
of ``NONFINITE_DIFFERENCE`` remains with ``OperatorRecordDifferencer`` evidence
and is not duplicated by direct exception tests.

VVUQ and scientific boundary
----------------------------

The enum and exception evidence is software verification of classification
vocabulary and direct failure-state structure. It is not numerical verification
of matrix subtraction and does not establish that a particular subtraction is
numerically accurate or scientifically acceptable. It does not establish
physical compatibility of operators, residual-metric correctness, scientific
validation, uncertainty quantification, or Rust conformance. Scientific
validation and uncertainty quantification have not been performed for these
contracts.
