QEXSD, periodic geometry, and plane-wave Kohn--Sham records
===========================================================

The public interfaces are separated by ownership. Quantum ESPRESSO parsing and
translation use ``ksdft2effmass.io.quantum_espresso.qexsd``; generic geometry
uses ``ksdft2effmass.periodic``; representation-neutral Kohn--Sham observations
use ``ksdft2effmass.ksdft``; and plane-wave records and serialization use
``ksdft2effmass.ksdft.pw``.

QEXSD source and translation
----------------------------

.. currentmodule:: ksdft2effmass.io.quantum_espresso.qexsd

.. autoclass:: QexsdSource
   :members:

.. autoclass:: QexsdDocument
   :members:

.. autoclass:: ParseQexsdDocument
   :members:

.. autoclass:: ConstructQexsdKohnShamPlaneWaveRecord
   :members:

Periodic geometry
-----------------

.. currentmodule:: ksdft2effmass.periodic

.. autoclass:: DirectLattice
.. autoclass:: ReciprocalLattice
.. autoclass:: PeriodicStructure
.. autoclass:: KPointSampling

Kohn--Sham and plane-wave records
---------------------------------

.. currentmodule:: ksdft2effmass.ksdft

.. autoclass:: KohnShamSpectralObservations
.. autoclass:: TotalEnergyObservation

.. currentmodule:: ksdft2effmass.ksdft.pw

.. autoclass:: KohnShamPlaneWaveCalculationRecord
.. autoclass:: KohnShamPlaneWaveCalculationRecordJsonSerializer
   :members:
