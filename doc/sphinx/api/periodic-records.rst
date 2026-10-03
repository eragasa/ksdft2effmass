QEXSD, periodic structures, sampling, and plane-wave records
=============================================================

The public interfaces are separated by ownership. Quantum ESPRESSO parsing, native
records, and the schema-version-1 aggregate adapter use
``ksdft2effmass.integration.quantum_espresso.qexsd``. Crystal geometry uses
``ksdft2effmass.structures.periodic``; electronic reciprocal-space sampling uses
``ksdft2effmass.electronic_structure``; representation-neutral Kohn--Sham
observations use ``ksdft2effmass.ksdft``; and plane-wave records and serialization
use ``ksdft2effmass.ksdft.pw``.

``ksdft2effmass.periodic`` owns the nominal one- through three-dimensional scientific-
model hierarchy, scientific-retention records and construction Actions, and explicit
toy-model catalogs. ``ksdft2effmass.periodic1d`` owns canonical one-dimensional
scientific definitions, beginning with parent-qualified selected-band retention. The
root periodic package temporarily also re-exports the former geometry and sampling
inventory for source compatibility; new geometry and sampling code uses the owning
packages above.

Periodic scientific models
--------------------------

The scientific-model hierarchy is independent of campaigns and numerical execution.
Its exact dimensions and explicit model roles provide the common membership boundary
for later model catalogs and compatible-observation comparisons.

.. toctree::
   :maxdepth: 1

   ksdft2effmass/periodic/model
   ksdft2effmass/periodic/retention
   ksdft2effmass/periodic/catalog
   ksdft2effmass/periodic1d/hopping
   ksdft2effmass/periodic1d/model
   ksdft2effmass/periodic1d/retention

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
