Canonical units and conversions
===============================

The authoritative unit inventory, conversion factors, source identities,
numerical policy, and provenance requirements are defined by
:doc:`../architecture/v2/ksdft2effmass/units`.  This API is an in-memory typed
boundary only; it does not rewrite native records or define a conversion-result
wire format.

Compatibility
-------------

The prior public ``PlaneWaveEnergyUnit`` enum and two-argument
``PlaneWaveEnergyCutoff(value, unit)`` constructor are replaced by a canonical
``UnitScalar`` in electron volts passed as
``PlaneWaveEnergyCutoff(quantity)``.  No compatibility alias or implicit native-unit
conversion is supplied.

.. currentmodule:: ksdft2effmass.units

Scalar and unit records
-----------------------

.. autoclass:: PhysicalDimension
.. autoclass:: UnitIdentity
.. autoclass:: UnitScalar

Canonical inventory, definitions, and authority
------------------------------------------------

.. autodata:: METAL_UNIT_INVENTORY
   :annotation: MetalUnitInventory

   Exact versioned canonical LAMMPS ``metal`` dimensional inventory and pinned
   LAMMPS-document provenance.

.. autodata:: METAL_UNIT_CONVERSION_CATALOG
   :annotation: MetalUnitConversionCatalog

   Exact ordered native-to-canonical definitions authorized for in-memory
   conversion.
.. autoclass:: MetalUnitInventory
.. autoclass:: ContentIdentity
.. autoclass:: AuthorityReference
.. autoclass:: MetalUnitConversionAuthority
.. autoclass:: NumericalPolicy
.. autoclass:: MetalUnitConversionDefinition
.. autoclass:: MetalUnitConversionCatalog

Requests, results, and conversion
---------------------------------

.. autoclass:: MetalUnitConversionSourceCorrelation
.. autoclass:: MetalUnitConversionRequest
.. autoclass:: MetalUnitConversionOutcome
.. autoclass:: MetalUnitConversionFailureCode
.. autoclass:: MetalUnitConversionLimitation
.. autoclass:: MetalUnitConversionSuccess
.. autoclass:: MetalUnitConversionFailure
.. autodata:: MetalUnitConversionResult
   :annotation: MetalUnitConversionSuccess | MetalUnitConversionFailure

   Closed in-memory result alias.  No serialized wire representation is defined.
.. autoclass:: MetalQuantityConverter
