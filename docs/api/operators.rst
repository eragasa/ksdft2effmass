Operator records API
====================

The supported public import path for finite operator records is
``ksdft2effmass.operators``.  The classes below are documented from the
implemented public package; source docstrings own detailed field and method
contracts.  Internally, exact representation compatibility is implemented in
``operators.compatibility``, represented differences in ``operators.difference``,
residual analysis in ``operators.residuals``, and the comparison Workflow in
``operators.comparison``.  The comparison-related dependency direction is
``records.py -> compatibility.py -> difference.py -> residuals.py -> comparison.py``;
earlier layers do not import later layers.  Callers should continue to import
supported public objects from ``ksdft2effmass.operators``.

.. currentmodule:: ksdft2effmass.operators

.. automodule:: ksdft2effmass.operators

DataObjects and ResultObjects
-----------------------------

.. autoclass:: StateSpace
   :members:

.. autoclass:: Basis
   :members:

   The constructor accepts approved ordered sequences such as tuples and lists
   and defensively canonicalizes them to exact built-in tuple storage. Label order
   and spelling are semantic. ``orthonormal=False`` is valid Basis metadata;
   ``OperatorRecord`` separately requires an orthonormal basis under schema
   version 1. Basis vectors and overlap matrices are not stored, and no numerical
   orthogonality proof is performed. Basis has no standalone serialization API;
   it appears only as nested state through ``OperatorRecordJsonSerializer``.

.. autoclass:: Geometry
   :members:

   ``cell`` stores three row lattice vectors as an exact built-in tuple of three
   built-in three-float tuples. The constructor admits approved nested ordered
   sequences (including tuples and lists) with Python integer/floating and NumPy
   integer/floating scalar components, then defensively canonicalizes them.
   ``Geometry.LINEAR_INDEPENDENCE_RTOL`` publicly owns the dimensionless strict
   relative singular-value policy. Geometry preserves row order, signs, and all
   metadata strings exactly; it performs no unit conversion, coordinate
   transformation, crystallographic validation, or standalone serialization.
   Detailed software- and numerical-verification evidence is documented in
   :doc:`../verification/operator-record-geometry`.

.. autoclass:: EnergyReference
   :members:

   ``zero`` is an exact textual identifier for the energy-origin convention; it
   is not a numerical energy offset. ``unit`` is an exact textual energy-unit
   label. Both must be nonempty Python strings and are retained without trimming,
   normalization, interpretation, registry lookup, or conversion. Equality is
   exact structural equality, not physical equivalence. Compatibility belongs to
   ``OperatorRecordCompatibilityAnalyzer`` and nested JSON representation belongs
   to ``OperatorRecordJsonSerializer``; ``EnergyReference`` has no standalone
   serialization API. Detailed software-verification evidence is documented in
   :doc:`../verification/operator-record-energy-reference`.

.. autoclass:: OperatorRecord
   :members:
   :special-members: __eq__

   ``matrix`` represents :math:`\mathbf H\in\mathbb C^{N\times N}` in
   ``basis.ordering`` index order and uses ``energy_reference.unit`` and
   ``energy_reference.zero``. Approved nested tuple/list and exact NumPy-array
   inputs containing Python/NumPy integer, floating, or complex scalars are
   defensively canonicalized to exact C-contiguous ``numpy.complex128`` storage.
   The stored array is operationally non-writeable, including rejection of
   ``setflags(write=True)``. Provenance is defensively copied and exposed through
   a read-only ``Mapping``; an empty mapping is valid.

   Exact equality includes every stored field without tolerance, and the object
   is unhashable. General finite non-Hermitian matrices are admitted. Hermiticity,
   compatibility, differencing, residual analysis, comparison, alignment,
   conversion, and serialization remain separate ActionObject responsibilities.
   Detailed software-verification evidence is documented in
   :doc:`../verification/operator-record-data-object`.

.. autoclass:: HermiticityResult
   :members:

.. autoclass:: OperatorRecordCompatibilityMismatchCode
   :members:

.. autoclass:: OperatorRecordCompatibilityIssue
   :members:

.. autoclass:: OperatorRecordCompatibilityResult
   :members:
   :exclude-members: is_compatible, rules_applied

   .. attribute:: rules_applied
      :no-index:

      Complete canonical version-1 compatibility-rule sequence,
      ``tuple(OperatorRecordCompatibilityMismatchCode)``.

   .. attribute:: is_compatible
      :no-index:

      Derived compatibility status; true exactly when ``issues`` is empty.

.. autoclass:: OperatorRecordDifferenceResult
   :members:

   ``OperatorRecordDifferenceResult`` is intentionally unhashable:
   ``OperatorRecordDifferenceResult.__hash__ is None``. The object owns
   array-valued exact state and no safe exact hash is implemented.

.. autoclass:: OperatorRecordComparisonResult
   :members:

   All three residual fields use the common ``energy_unit`` and are stored as
   built-in finite non-negative Python ``float`` values. Accepted NumPy integer
   and floating scalars are canonicalized to built-in ``int`` and ``float``;
   Boolean values, numeric strings, complex scalars, nonfinite metrics, and
   negative metrics are rejected. Stored state must satisfy
   ``maximum_absolute_residual <= spectral_residual <= frobenius_residual``.

   Equality is exact structural equality over all public fields, not approximate
   numerical agreement or physical operator equivalence. Roundoff allowance and
   permitted metric canonicalization belong to
   ``OperatorRecordResidualAnalyzer`` before construction. This ResultObject has
   no approved ``to_json``, ``from_json``, ``to_dict``, ``from_dict``,
   ``serialize``, or ``deserialize`` contract; serialization requires a
   separately approved serializer ActionObject and wire-format specification.

Structured public exceptions
----------------------------

.. autoclass:: HermiticityUnitMismatchError
   :members:

.. autoclass:: HermiticityNumericalErrorCode
   :members:

.. autoclass:: HermiticityNumericalError
   :members:

.. autoclass:: HermiticityRequirementError
   :members:

.. autoclass:: IncompatibleOperatorRecordsError
   :members:
   :exclude-members: compatibility_result

   .. attribute:: compatibility_result
      :no-index:

      Structured ``OperatorRecordCompatibilityResult`` retained for public
      mismatch inspection.

.. autoclass:: OperatorRecordDifferenceNumericalErrorCode
   :members:

.. autoclass:: OperatorRecordDifferenceNumericalError
   :members:

.. autoclass:: OperatorRecordComparisonNumericalErrorCode
   :members:

.. autoclass:: OperatorRecordComparisonNumericalError
   :members:

ActionObjects
-------------

.. autoclass:: HermiticityAnalyzer
   :members:

.. autoclass:: OperatorRecordCompatibilityAnalyzer
   :members:
   :exclude-members: RULES_APPLIED

   .. attribute:: RULES_APPLIED
      :no-index:

      Class-owned canonical rule sequence equal to
      ``tuple(OperatorRecordCompatibilityMismatchCode)``.

.. autoclass:: OperatorRecordDifferencer
   :members:

.. autoclass:: OperatorRecordResidualAnalyzer
   :members:

.. autoclass:: OperatorRecordComparator
   :members:

   This genuine concrete production Workflow composes
   ``OperatorRecordDifferencer`` followed by ``OperatorRecordResidualAnalyzer``.
   It owns sequencing and dependency composition only; lower layers retain
   compatibility, subtraction, numerical, and structured-error policy. It is
   neither a technical-integration owner nor a generic Workflow base class.

.. autoclass:: OperatorRecordJsonSerializer
   :members:
   :exclude-members: SCHEMA_VERSION

   .. attribute:: SCHEMA_VERSION
      :no-index:

      Integer schema version emitted and accepted by this serializer. The only
      supported value is ``1``.

   The five runtime facets and the distinct public-schema and golden-fixture
   integration owners are documented in
   :doc:`../verification/operator-record-json-serialization`.
