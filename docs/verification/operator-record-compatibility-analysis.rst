OperatorRecord compatibility-analysis software verification
============================================================

Purpose and scope
-----------------

``OperatorRecordCompatibilityAnalyzer`` is an ActionObject that audits whether
two independently valid finite ``OperatorRecord`` matrices already use the same
representation metadata required for direct subtraction.  This is a strict
software precondition for forming

.. math::

   \Delta\mathbf H
   =
   \mathbf H_{\mathrm{candidate}}
   -
   \mathbf H_{\mathrm{reference}}.

Compatibility is exact rather than approximate.  The analyzer does not align
bases or gauges, align energy zeros, convert units, transform geometry, compare
provenance, or establish physical equivalence.

Compatibility-critical fields and rule evidence
-------------------------------------------------

The analyzer compares every critical field and reports all findings in canonical
order.  ``SV-ORCA-004`` through ``SV-ORCA-014`` construct both inputs as
independently valid records and establish reachability of every public mismatch
code.

.. list-table:: Compatibility-rule reachability
   :header-rows: 1

   * - Evidence ID
     - Public mismatch code
     - Compatibility-critical field
   * - ``SV-ORCA-004``
     - ``MATRIX_DIMENSION_MISMATCH``
     - Matrix dimension
   * - ``SV-ORCA-005``
     - ``STATE_SPACE_KIND_MISMATCH``
     - State-space kind
   * - ``SV-ORCA-006``
     - ``OPERATOR_KIND_MISMATCH``
     - Operator kind
   * - ``SV-ORCA-007``
     - ``ORDERED_BASIS_LABELS_MISMATCH``
     - Ordered basis-label tuple
   * - ``SV-ORCA-008``
     - ``BASIS_KIND_MISMATCH``
     - Basis kind
   * - ``SV-ORCA-009``
     - ``LATTICE_VECTORS_MISMATCH``
     - Row lattice vectors
   * - ``SV-ORCA-010``
     - ``BOUNDARY_CONDITIONS_MISMATCH``
     - Boundary-condition convention
   * - ``SV-ORCA-011``
     - ``COORDINATE_CONVENTION_MISMATCH``
     - Coordinate convention
   * - ``SV-ORCA-012``
     - ``GEOMETRY_LENGTH_UNIT_MISMATCH``
     - Geometry length unit
   * - ``SV-ORCA-013``
     - ``ENERGY_UNIT_MISMATCH``
     - Matrix energy unit
   * - ``SV-ORCA-014``
     - ``ENERGY_ZERO_CONVENTION_MISMATCH``
     - Applied energy-zero convention

Matrix-dimension coupling
-------------------------

The matrix-dimension finding is intentionally coupled to the ordered-label
finding.  Every valid record satisfies

.. math::

   \operatorname{dim}(\mathbf H)
   =
   \texttt{StateSpace.dimension}
   =
   \operatorname{len}(\texttt{Basis.ordering}).

Consequently, an independently valid candidate with a different matrix dimension
must also have a basis-label sequence of different length.  ``SV-ORCA-004``
therefore expects, in order,
``MATRIX_DIMENSION_MISMATCH`` and
``ORDERED_BASIS_LABELS_MISMATCH``.  The evidence does not fabricate invalid
records or claim that matrix-dimension mismatch is independently isolatable
under current intrinsic invariants.

Ignored identity, descriptive, and provenance fields
-----------------------------------------------------

``SV-ORCA-003`` independently varies these ignored fields while keeping every
compatibility-critical field equal:

* ``OperatorRecord.identifier``;
* ``StateSpace.identifier``;
* ``Basis.identifier``;
* ``Geometry.system``;
* ``OperatorRecord.provenance``.

Ignoring these fields means only that they do not prevent direct matrix
subtraction under the current software contract.  It does not establish that the
records describe the same physical system, have equivalent DFT or Wannier
provenance, or are scientifically acceptable to subtract.

Deterministic audit ordering
----------------------------

``tuple(OperatorRecordCompatibilityMismatchCode)`` owns the complete canonical
rule order.  ``execute()`` evaluates every rule and reports findings in that
order.  ``SV-ORCA-015`` reaches the complete mismatch sequence with two
independently valid records and compares the ordered issue-code tuple directly
to the enum tuple.  A separate set equality checks coverage only; no set or
dictionary determines public issue order.

``execute()`` and ``require()``
-------------------------------

``execute(reference, candidate)`` returns an
``OperatorRecordCompatibilityResult`` for both compatible and incompatible
pairs.  The result retains reference and candidate identifiers as role-specific
audit context, exposes the complete ``rules_applied`` sequence, and reports an
empty issue tuple exactly when compatible.

``require(reference, candidate)`` performs the same complete audit.  It returns
a value-equivalent compatible result on success.  On failure it raises
``IncompatibleOperatorRecordsError`` whose public ``compatibility_result``
retains the complete audit, exact issue codes, and input roles.  Callers should
inspect this structured result rather than parse exception text.

Structured incompatibility exception evidence
---------------------------------------------

``SV-IORE-001`` through ``SV-IORE-006`` verify
``IncompatibleOperatorRecordsError`` independently of Analyzer execution. The
exception is a public ``ValueError`` subtype for an already-incompatible
``OperatorRecordCompatibilityResult``. It retains the exact supplied Result by
identity so callers can inspect the original reference and candidate roles and
the canonical ordered Issue tuple without reconstruction.

The retained ``compatibility_result`` is authoritative machine-readable audit
state. ``str(error)`` is only a human-readable summary stating incompatibility
and listing retained mismatch codes in Issue order. Evidence checks that semantic
content without promoting punctuation or separators into a new public formatting
contract. Canonical mismatch names, values, descriptions, and Analyzer
reachability remain owned by their existing evidence surfaces rather than being
duplicated here.

Direct construction rejects a value that is not an
``OperatorRecordCompatibilityResult`` with ``TypeError`` and a diagnostic naming
``compatibility_result``. A correctly typed but compatible Result violates the
exception-state invariant and is rejected with ``ValueError`` indicating that an
incompatible result is required. ``OperatorRecordCompatibilityAnalyzer.require()``
constructs and propagates this exception after its complete audit; that
propagation is owned by ``SV-ORCA-017``, while ``SV-IORE`` evidence verifies the
exception's direct contract.

The exception has no independent ``to_json``, ``to_dict``, ``serialize``,
``from_json``, ``from_dict``, or ``deserialize`` API. It retains an in-memory
audit only. Exception, compatibility-result, and comparison-result serialization
are outside the schema-version-1 ``OperatorRecord`` wire contract.

An incompatibility finding means that records fail the current exact direct-
representation contract. It does not prove that physical Hamiltonians are
fundamentally incompatible or that basis alignment, gauge alignment, energy-zero
alignment, unit conversion, geometry transformation, or another scientifically
justified identification map could not make them comparable. This is software
verification, not numerical verification or scientific validation. No numerical
norm, uncertainty model, uncertainty propagation, UQ result, or Rust exception
conformance is established.

Evidence interpretation and exclusions
---------------------------------------

``SV-ORCA-001`` through ``SV-ORCA-019`` are software-verification evidence for
public construction, audit-result creation, exact field ownership, mismatch
reachability, deterministic ordering, structured enforcement, and public input
types.  The synthetic finite matrices do not come from DFT, Wannierization,
experiment, or impurity extraction.

This evidence is not numerical verification because it evaluates no numerical
approximation, convergence, scaling, or conditioning.  Scientific validation
has not been performed: passing does not prove physical equivalence, basis or
gauge alignment, energy-zero alignment, equivalent provenance, or acceptable
scientific subtraction.  Uncertainty quantification has not been performed: no
uncertainty sources, distributions, intervals, or propagation procedure are
part of this audit.

Architecture integration ownership
----------------------------------

The analyzer object tests do not inspect internal module locations or parse
production source.  The narrowly scoped technical integration test
``test__OperatorComparisonDependencyDirection.py`` owns executable evidence for
the package direction
``records -> compatibility -> difference -> residuals -> comparison``.  That
package-topology check is separate from Analyzer behavior.
