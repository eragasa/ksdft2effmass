Plane-wave Kohn--Sham calculation records from QEXSD
====================================================

The bounded extraction path is:

.. code-block:: text

   explicit QEXSD bytes and source identity
   -> ParseQexsdDocument
   -> mechanically faithful QexsdDocument
   -> ConstructQexsdKohnShamPlaneWaveRecord
   -> immutable KohnShamPlaneWaveCalculationRecord
   -> canonical retained JSON

QEXSD parsing preserves raw source observations; QEXSD-owned construction maps
backend conventions into composed domain objects. Generic periodic geometry,
representation-neutral Kohn--Sham observations, plane-wave metadata, and
canonical serialization have separate owners. See the maintained
:download:`computational architecture <../computational/ksdft-pw-record-architecture.md>`.

Direct vectors and Cartesian atomic positions use bohr. Raw reciprocal vectors
and raw Cartesian k points are dimensionless coefficients with scale
``2pi_over_alat``; their physical values use bohr :sup:`-1`. For the retained
artifact, ``alat = 10.2 bohr`` and
:math:`A B_{\mathrm{physical}}^{\mathsf T}=2\pi I` under an absolute
componentwise residual bound of :math:`10^{-12}`. Eigenvalues and total energy
use hartree. Weights are explicitly marked as summing to two.

Spin-resolved arrays, energy reference, basis identity, retained subspace,
gauge, and phase convention remain unavailable. The record does not establish
convergence, numerical verification, scientific validation, UQ, or human
acceptance.

* :download:`Retained record <../../calculations/bulk-silicon/qe-example01-si-scf-davidson/ksdft-plane-wave-calculation-record.json>`
* :download:`Version-1 schema <../../specification/ksdft-plane-wave-calculation-record/v1/ksdft-plane-wave-calculation-record.schema.json>`
