QEXSD, periodic structures, sampling, and plane-wave records
=============================================================

The public interfaces are separated by ownership. Quantum ESPRESSO parsing, native
records, and the schema-version-1 aggregate adapter use
``ksdft2effmass.integration.quantum_espresso.qexsd``. Crystal geometry uses
``ksdft2effmass.structures.periodic``; electronic reciprocal-space sampling uses
``ksdft2effmass.electronic_structure``; representation-neutral Kohn--Sham
observations use ``ksdft2effmass.ksdft``; and plane-wave records and serialization
use ``ksdft2effmass.ksdft.pw``.

``ksdft2effmass.periodic`` temporarily re-exports the former public inventory for
source compatibility. New code uses the owning packages above.

QEXSD source and translation
----------------------------

.. currentmodule:: ksdft2effmass.integration.quantum_espresso.qexsd

.. autoclass:: QexsdSource
   :members:

.. autoclass:: QexsdDocument
   :members:

.. autoclass:: QuantumEspressoXsdDocumentParser
   :members:

The parser accepts exactly QEXSD ``23.03.10`` from the retained QE 7.2 artifact
and QEXSD ``25.05.21`` from the retained QE 7.5 smoke-test artifact under the QES
1.0 namespace. Other versions fail closed. This is mechanical native-value
support, not a claim that every document permitted by either upstream schema has
been exercised.

The schema-version-1 aggregate adapter remains integration-owned while downstream
integration adaptation is migrated.

.. currentmodule:: ksdft2effmass.integration.quantum_espresso.qexsd

.. autoclass:: ConstructQexsdKohnShamPlaneWaveRecord
   :members:

Periodic crystal geometry
-------------------------

.. currentmodule:: ksdft2effmass.structures.periodic

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

Electronic reciprocal-space sampling
------------------------------------

.. currentmodule:: ksdft2effmass.electronic_structure

.. autoclass:: KPointWeightNormalization
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
