Operator records API
====================

The supported public import path for finite operator records is
``ksdft2effmass.operators``.  The classes below are documented from the
implemented public package; source docstrings remain owned by the implementation
stage.

.. currentmodule:: ksdft2effmass.operators

.. automodule:: ksdft2effmass.operators

DataObjects and ResultObjects
-----------------------------

.. autoclass:: StateSpace
   :members:
   :undoc-members:

.. autoclass:: Basis
   :members:
   :undoc-members:

.. autoclass:: Geometry
   :members:
   :undoc-members:

.. autoclass:: EnergyReference
   :members:
   :undoc-members:

.. autoclass:: OperatorRecord
   :members:
   :undoc-members:
   :special-members: __eq__

.. autoclass:: HermiticityResult
   :members:
   :undoc-members:

ActionObjects
-------------

.. autoclass:: HermiticityAnalyzer
   :members:
   :undoc-members:

.. autoclass:: OperatorRecordJsonSerializer
   :members:
   :undoc-members:
   :exclude-members: SCHEMA_VERSION
