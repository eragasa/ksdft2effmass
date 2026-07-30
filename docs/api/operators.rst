Operator records API
====================

The supported public import path for finite operator records is
``ksdft2effmass.operators``.  The classes below are documented from the
implemented public package; source docstrings own detailed field and method
contracts.

.. currentmodule:: ksdft2effmass.operators

.. automodule:: ksdft2effmass.operators

DataObjects and ResultObjects
-----------------------------

.. autoclass:: StateSpace
   :members:

.. autoclass:: Basis
   :members:

.. autoclass:: Geometry
   :members:

.. autoclass:: EnergyReference
   :members:

.. autoclass:: OperatorRecord
   :members:
   :special-members: __eq__

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

.. autoclass:: OperatorRecordComparisonResult
   :members:

Structured public exceptions
----------------------------

.. autoclass:: HermiticityUnitMismatchError
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

.. autoclass:: OperatorRecordComparator
   :members:

.. autoclass:: OperatorRecordJsonSerializer
   :members:
   :exclude-members: SCHEMA_VERSION

   .. attribute:: SCHEMA_VERSION
      :no-index:

      Integer schema version emitted and accepted by this serializer. The only
      supported value is ``1``.
