One-dimensional controlled parent models
=========================================

``ksdft2effmass.periodic1d`` provides two immutable toy-parent definitions used by
M1 and M2. Model records freeze identities, units, direct/reciprocal duality, and
Hermiticity; they do not execute calculations or choose retained subspaces.

Fourier parent
--------------

.. autoclass:: ksdft2effmass.periodic1d.Periodic1DFourierHamiltonianToyModel
   :members:
   :undoc-members:

Block-hopping parent
--------------------

.. autoclass:: ksdft2effmass.periodic1d.Periodic1DBlockHamiltonianToyModel
   :members:
   :undoc-members:
