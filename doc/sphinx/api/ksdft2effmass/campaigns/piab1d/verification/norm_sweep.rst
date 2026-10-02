PIAB1D norm-sweep verification
==============================

Purpose
-------

``Piab1dNormSweepResultsVerifier`` reconstructs the finite-matrix norms recorded by the
version-one norm sweep. It verifies each grid independently. Changes in a norm across
grid sizes are data for later analysis, not verification conditions.

Mathematics
-----------

For ``N`` interior points, interval length :math:`L`, spacing
:math:`h=L/(N+1)`, and the current dimensionless values :math:`m=\hbar=1`, define

.. math::

   a = \frac{1}{2h^2},
   \qquad
   E_n = 4a\sin^2\!\left(\frac{n\pi}{2(N+1)}\right).

The Dirichlet Hamiltonian norms are

.. math::

   \lVert H\rVert_F = a\sqrt{6N-2},
   \qquad
   \lVert H\rVert_2 = E_N,
   \qquad
   \lVert H\rVert_{\max}=2a.

The endpoint-link boundary residual has norms

.. math::

   \lVert R_b\rVert_F=\sqrt{2}a,
   \qquad
   \lVert R_b\rVert_2=\lVert R_b\rVert_{\max}=a.

For retained dimension ``r``, the discarded spectral sector has

.. math::

   \lVert R_d\rVert_F
   = \left(\sum_{n=r+1}^{N}E_n^2\right)^{1/2},
   \qquad
   \lVert R_d\rVert_2=E_N.

All quantities are dimensionless in this controlled calculation. Raw norms retain the
:math:`h^{-2}` finite-difference scale and must not be compared across dimensions as if
they acted on one fixed state space.

Checks and tolerances
---------------------

The report checks grid inventory, spacing, Hamiltonian norms, zero consistent-
compression residuals, boundary-residual norms, and discarded-sector norms. Reported
binary64 norms use the retained verifier's explicit relative-plus-absolute envelopes:
``2e-13`` relative, ``2e-12`` absolute for Hamiltonian and boundary norms, and
``2e-11`` absolute for discarded-sector norms. These are version-one reproduction
settings, not uncertainty estimates.

The retained algebraic residual values are decoded as finite nonnegative data, but this
result file does not retain eigenvectors from which an independent verifier could
reconstruct them. They therefore do not determine verification success.

Usage
-----

.. code-block:: python

   from pathlib import Path
   from ksdft2effmass.campaigns.piab1d import Piab1dNormSweepResultsVerifier

   report = Piab1dNormSweepResultsVerifier().execute(
       Path("calculations/research-monograph/particle-in-box/norm-sweep-result.json"),
       Path("."),
   )
   assert report.passes

Implementation, evidence, and limits
------------------------------------

The implementation is
``python/src/ksdft2effmass/campaigns/piab1d/verification/norm_sweep.py``. Tests and
retained inputs are under the corresponding PIAB1D test and calculation directories.
A passing report verifies the listed finite identities and recorded source files. It
does not establish continuum convergence, physical identifiability, semiconductor
validity, or uncertainty bounds.

API
---

.. currentmodule:: ksdft2effmass.campaigns.piab1d.verification.norm_sweep

.. autoclass:: Piab1dNormSweepVerificationChannel
   :members:

.. autoclass:: Piab1dNormSweepResultsVerifier
   :members:
