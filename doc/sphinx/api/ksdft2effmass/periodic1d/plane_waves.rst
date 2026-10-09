Periodic-1D plane-wave fibers
=============================

.. module:: ksdft2effmass.periodic1d.plane_waves

These records construct and retain one finite Galerkin representation of a
parent-qualified periodic-1D Fourier Hamiltonian.  Matrix order is exactly the
order of ``PlaneWaveBasis1D.reciprocal_indices``.  The finite matrix is not the
untruncated parent operator, and software checks do not establish basis
convergence or scientific validation.

.. autoclass:: PlaneWaveFiberHamiltonian1DConstructor
   :members:

.. autoclass:: PlaneWaveFiberHamiltonian1DResult
   :members:
