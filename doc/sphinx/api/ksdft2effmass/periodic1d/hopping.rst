One-dimensional finite-hopping toy model
========================================

.. currentmodule:: ksdft2effmass.periodic1d

:class:`Periodic1DFiniteHoppingToyModel` is a nominal
:class:`~ksdft2effmass.periodic.Periodic1DModel` with the exact
:class:`~ksdft2effmass.periodic.PeriodicModelRole.TOY` role.  One configured instance
has a stable model identity, an ordered finite tuple of directed hopping blocks, an
exact energy-unit string, and an explicit pairwise Hermiticity tolerance.

For cell displacement :math:`R`, the blocks satisfy

.. math::

   H_R = H_{-R}^{\dagger}

under an inclusive absolute tolerance and zero relative tolerance.  Displacements are
unique, increasing, contiguous, and include zero.  Every block has one common nonzero
square orbital dimension.

The block constructor accepts NumPy arrays with integer, floating, or complex scalar
dtypes and stores an owned, C-contiguous, non-writeable ``complex128`` copy.  Boolean,
string, byte, and object arrays are rejected instead of being coerced into scientific
coefficients.

The model identifies a controlled scientific toy parent, not a represented Bloch-fiber
matrix or campaign.  Primitive-fiber and finite-supercell constructors remain separate
numerical Actions.  Structural and Hermiticity checks are software verification only;
they do not establish material realism, physical completeness, scientific validation,
or uncertainty quantification.

.. autoclass:: Periodic1DHoppingBlock
   :members:

.. autoclass:: Periodic1DFiniteHoppingToyModel
   :members:

Hopping construction routes
---------------------------

``BlockHoppingModel1D`` remains reusable coefficient data.  Its scientific meaning is
supplied by construction results: a complete centered finite-mesh Fourier transform is
a representation of an exact retained operator, while truncation and weighted fitting
construct separately identified effective models.  Coefficient values alone do not
select among these meanings.

:class:`Periodic1DCompleteHoppingRepresentationResult` owns the complete Fourier
construction route, including source and reconstruction diagnostics. It is distinct
from :class:`Periodic1DRetainedOperatorHoppingRepresentation`, documented in
:doc:`representations`, which binds an already retained complete hopping family to an
exact operator and gauge when a transform source need not be available.

.. autoclass:: Periodic1DCompleteHoppingRepresentationResult
   :members:

.. autoclass:: Periodic1DTruncatedHoppingEffectiveModelResult
   :members:

.. autoclass:: Periodic1DFittedHoppingEffectiveModelResult
   :members:
