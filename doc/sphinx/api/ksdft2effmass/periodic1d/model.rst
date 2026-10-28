One-dimensional controlled parent model
========================================

``ksdft2effmass.periodic1d`` provisionally retains the immutable block-hopping toy
parent used by M2 and M3. The record freezes identity, units, and Hermiticity; it does
not execute calculations or choose retained subspaces. The former Fourier toy-parent
record was removed with the legacy M1 isolated-band surface. The direct rank-one control
declares its exact parent through
:class:`~ksdft2effmass.periodic1d.fourier_locality.Periodic1DFourierLocalityConfiguration`.

Block-hopping parent
--------------------

.. autoclass:: ksdft2effmass.periodic1d.Periodic1DBlockHamiltonianToyModel
   :members:
   :undoc-members:
