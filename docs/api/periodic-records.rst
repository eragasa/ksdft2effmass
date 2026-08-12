QEXSD and periodic calculation records
======================================

Use the public ``ksdft2effmass.periodic`` import path. QEXSD parsing is not
semantic periodic-record construction.

.. currentmodule:: ksdft2effmass.periodic

Native source and parsing
-------------------------

.. autoclass:: QexsdSource
   :members:

.. autoclass:: QexsdDocument
   :members:

.. autoclass:: ParseQexsdDocument
   :members:

Semantic record and serialization
---------------------------------

.. autoclass:: UnavailableReason
   :members:

.. autoclass:: PeriodicCalculationRecord
   :members:

.. autoclass:: ConstructPeriodicCalculationRecord
   :members:

.. autoclass:: PeriodicCalculationRecordJsonSerializer
   :members:
