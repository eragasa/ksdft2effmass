Periodic basis identities
=========================

The structured basis identity records exact matrix-coordinate order. They do not own
state-space identity, frame, gauge, embedding, geometry, energy reference, sewing, or
artifact provenance. Compatibility is exact, order-sensitive equality of the
dimensional concrete type and coordinate inventory; ``display_identifier`` is
descriptive only. ``PeriodicBasisInventory`` is a transient immutable composition
object: it maps explicitly declared retained ranks to structured identities but never
generates coordinates from rank.

.. currentmodule:: ksdft2effmass.periodic.operators.basis

.. autoclass:: PeriodicBasisFamily
   :members:

.. autoclass:: PeriodicBasisIdentity
   :members:

.. currentmodule:: ksdft2effmass.periodic.operators.basis_inventory

.. autoclass:: PeriodicBasisInventoryEntry
   :members:

.. autoclass:: PeriodicBasisInventory
   :members:

.. currentmodule:: ksdft2effmass.periodic.periodic1d.operators.basis

.. autoclass:: Periodic1DBasisIdentity
   :members:

.. currentmodule:: ksdft2effmass.periodic.periodic2d.operators.basis

.. autoclass:: Periodic2DBasisIdentity
   :members:

.. currentmodule:: ksdft2effmass.periodic.periodic3d.operators.basis

.. autoclass:: Periodic3DBasisIdentity
   :members:

.. currentmodule:: ksdft2effmass.periodic.operators.basis

.. autoclass:: LabeledComponentBasisCoordinate
   :members:

.. autoclass:: PlaneWaveBasisCoordinate
   :members:

.. autoclass:: WannierOrbitalBasisCoordinate
   :members:

.. autoclass:: SlaterKosterOrbital
   :members:

.. autoclass:: SlaterKosterOrbitalBasisCoordinate
   :members:
