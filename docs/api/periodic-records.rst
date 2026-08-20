QEXSD, periodic geometry, and plane-wave Kohn--Sham records
===========================================================

The public interfaces are separated by ownership. Canonical Quantum ESPRESSO
parsing and native records use
``ksdft2effmass.integration.quantumespresso.qexsd``; the historical
``ksdft2effmass.io.quantum_espresso.qexsd`` path retains compatibility forwarding
and the schema-version-1 aggregate adapter. Generic geometry uses
``ksdft2effmass.periodic``; representation-neutral Kohn--Sham observations
use ``ksdft2effmass.ksdft``; and plane-wave records and serialization use
``ksdft2effmass.ksdft.pw``.

QEXSD source and translation
----------------------------

.. currentmodule:: ksdft2effmass.integration.quantumespresso.qexsd

.. autoclass:: QexsdSource
   :members:

.. autoclass:: QexsdDocument
   :members:

.. autoclass:: QexsdDocumentParser
   :members:

The schema-version-1 compatibility adapter remains under the historical import
path while downstream integration adaptation is migrated.

.. currentmodule:: ksdft2effmass.io.quantum_espresso.qexsd

.. autoclass:: ConstructQexsdKohnShamPlaneWaveRecord
   :members:

Periodic geometry
-----------------

.. currentmodule:: ksdft2effmass.periodic

.. autoclass:: UnitSystem
   :members:

.. autoclass:: PhysicalDimension
   :members:

.. autoclass:: LengthUnit
   :members:

.. autoclass:: InverseLengthUnit
   :members:

.. autoclass:: CoordinateConvention
   :members:

.. autoclass:: ReciprocalScaleConvention
   :members:

.. autoclass:: KPointWeightNormalization
   :members:

.. autoclass:: DirectLattice
   :members:

.. autoclass:: ReciprocalLattice
   :members:

.. autoclass:: ReciprocalLatticeCompatibilityValidator
   :members:

.. autoclass:: AtomicSpecies
   :members:

.. autoclass:: PeriodicSite
   :members:

.. autoclass:: PeriodicStructure
   :members:

.. autoclass:: KPointSampling
   :members:

Kohn--Sham and plane-wave records
---------------------------------

.. currentmodule:: ksdft2effmass.ksdft

.. autoclass:: EnergyUnit
   :members:

.. autoclass:: Availability
   :members:

.. autoclass:: KohnShamSpectralObservations
   :members:

.. autoclass:: TotalEnergyObservation
   :members:

.. currentmodule:: ksdft2effmass.ksdft.pw

.. autoclass:: KohnShamPlaneWaveCalculationRecord
   :members:

.. autoclass:: KohnShamPlaneWaveCalculationRecordValidator
   :members:

.. autoclass:: KohnShamPlaneWaveCalculationRecordJsonSerializer
   :members:
