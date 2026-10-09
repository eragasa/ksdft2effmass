Periodic-1D finite-difference fibers
=====================================

.. module:: ksdft2effmass.periodic1d.finite_differences

The grid stores the half-open order ``origin + j a/N`` for ``j = 0, ..., N-1``.
The finite-difference Action preserves the directed seam
``H[0,N-1] = -t exp(-2πik)`` and its conjugate reverse edge.  The sparse matrix is
a finite discretization of the qualified parent and does not establish mesh
convergence, scientific validation, or uncertainty quantification.

.. autoclass:: PeriodicUniformGrid1D
   :members:

.. autoclass:: PeriodicFiniteDifferenceFiberHamiltonian1DConstructor
   :members:

.. autoclass:: PeriodicFiniteDifferenceFiberHamiltonian1DResult
   :members:
