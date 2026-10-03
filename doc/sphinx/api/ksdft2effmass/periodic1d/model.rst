One-dimensional periodic Fourier parent model
==============================================

.. currentmodule:: ksdft2effmass.periodic1d

:class:`Periodic1DFourierHamiltonianToyModel` identifies a complete untruncated
one-dimensional toy parent by composing a reusable Fourier potential with a positive
recoil-energy scale, stable state-space identity, primitive reciprocal-domain identity,
and configured model identity.  Its mathematical Bloch-fiber law is

.. math::

   H_{nm}(k) = E_G (k+n)^2\delta_{nm} + V_{n-m},

for reduced momentum :math:`k\in[-1/2,1/2]`.  The potential supplies the period and
Fourier energy convention; :math:`E_G` supplies the quadratic kinetic law.  Their
energy units must be compatible.

The parent is distinct from a finite plane-wave basis, sampled fiber matrix, retained
subspace, represented retained operator, or fitted effective model.  Its exact
:class:`~ksdft2effmass.periodic.PeriodicModelRole.TOY` role does not imply material
realism, scientific validation, or uncertainty quantification.

.. autoclass:: Periodic1DFourierHamiltonianToyModel
   :members:
