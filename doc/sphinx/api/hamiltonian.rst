Hamiltonian reduction API
=========================

The supported public import path for Hamiltonian records, retained spectral spaces,
reduction, reduction diagnostics, and decomposition is
``ksdft2effmass.hamiltonian``. Generic quantities and spectral decomposition are
imported directly from ``projectkoios.physkit``; KSD provides no compatibility layer.

.. currentmodule:: ksdft2effmass.hamiltonian

.. automodule:: ksdft2effmass.hamiltonian

Hamiltonian records
-------------------

.. autoclass:: Hamiltonian
   :members:

.. autoclass:: HermitianHamiltonian
   :members:

.. autoclass:: ReducedHamiltonian
   :members:

Spectral subspaces and reduction
--------------------------------

.. autoclass:: SpectralSubspace
   :members:

.. autoclass:: OrthogonalSpectralSubspace
   :members:

.. autoclass:: OrthogonalSpectralSubspaceSelectionRequest
   :members:

.. autoclass:: OrthogonalSpectralSubspaceSelector
   :members:

.. autoclass:: SpectralReduction
   :members:

.. autoclass:: OrthogonalHamiltonianBlockResult
   :members:

.. autoclass:: OrthogonalHamiltonianBlockRequest
   :members:

.. autoclass:: OrthogonalHamiltonianBlockAnalyzer
   :members:

Composable verification
-----------------------

Both verification values inherit the final generic dictionary and JSON boundaries.
They contain named, unit-bearing observations and do not own a model-specific
Hamiltonian constructor.

.. autoclass:: HamiltonianVerification
   :members:

.. autoclass:: SpectralReductionVerification
   :members:

Decomposition
-------------

.. autoclass:: HamiltonianDecomposition
   :members:
