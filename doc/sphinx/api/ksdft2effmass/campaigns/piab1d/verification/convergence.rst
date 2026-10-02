PIAB1D convergence verification
===============================

Purpose and scope
-----------------

``Piab1dConvergenceResultsVerifier`` authenticates a version-one fixed-mode grid
refinement result and independently reconstructs six aggregate channels. It verifies
the represented centered second-order Dirichlet discretization for fixed mode indices.
It does not infer uniform spectral convergence from those fixed-mode observations.

Mathematical contract
---------------------

For :math:`N` interior points and unit dimensionless box length, the spacing is

.. math::
   :label: piab-convergence-spacing

   h_N=\frac{1}{N+1}.

With modal phase :math:`z_{n,N}=n\pi/[2(N+1)]`, the relative discrete energy error is

.. math::
   :label: piab-convergence-error

   \delta_{n,N}
   =1-\left(\frac{\sin z_{n,N}}{z_{n,N}}\right)^2.

For consecutive refinements, the observed order is

.. math::
   :label: piab-convergence-order

   p_n
   =\frac{\log(\delta_{n,N_a}/\delta_{n,N_b})}
          {\log(h_{N_a}/h_{N_b})}.

For fixed :math:`n`, the centered stencil is expected to approach order two. The
verifier checks only that each represented pairwise order agrees with the independently
reconstructed value. Monotonicity and proximity to order two are analysis questions.

Symbols, ordering, and channels
-------------------------------

:math:`N` and :math:`n` are positive integers; refinement dimensions and represented
mode inventories follow the strictly increasing input order; :math:`h_N`,
:math:`\delta_{n,N}`, and :math:`p_n` are finite dimensionless binary64 values. Counts
of refinements and reconstructed mode observations are derived from decoded collections.

The six channels cover grid spacing, relative energy error, discrete closed-form error,
zero consistent compression, the discarded-sector identity, and observed-order
reconstruction. Exact structural relations use zero tolerance. Numerical allowances
are version-one reproduction settings, not scientific-validation criteria.

Mappings, references, and evidence boundary
-------------------------------------------

The defining source is
``python/src/ksdft2effmass/campaigns/piab1d/verification/convergence.py``. The retained
input and result, protocol, verifier CLI, and checksum catalog are under
``calculations/research-monograph/particle-in-box/``. Maintained software evidence is in
``python/tests/software_verification/ksdft2effmass/campaigns/piab1d/``. Appendix D of the
research monograph owns the scientific-methodology narrative and cites John C.
Strikwerda, *Finite Difference Schemes and Partial Differential Equations*, second
edition, SIAM, 2004, DOI `10.1137/1.9780898717938
<https://doi.org/10.1137/1.9780898717938>`_.

Passing reports establish the stated numerical behavior on the retained finite grids.
They do not establish uniform spectral or operator convergence, identify a physical
potential, validate semiconductor physics, or quantify uncertainty.

API
---

.. currentmodule:: ksdft2effmass.campaigns.piab1d.verification.convergence

.. autoclass:: Piab1dConvergenceVerificationChannel
   :members:

.. autoclass:: Piab1dConvergenceResultsVerifier
   :members:
