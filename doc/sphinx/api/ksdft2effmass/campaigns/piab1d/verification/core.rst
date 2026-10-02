PIAB1D core-result verification
===============================

Purpose and scope
-----------------

``Piab1dResultsVerifier`` authenticates and independently reconstructs the
version-one core PIAB1D residual result. The represented continuum operator acts on
:math:`L^2(0,L)` with a Dirichlet domain; the finite Hamiltonian is an :math:`N\times N`
real symmetric matrix; and the retained coordinate Hamiltonian is an :math:`M\times M`
matrix. The verifier does not identify matrices acting on different spaces.

Mathematical contract
---------------------

For grid spacing :math:`h=L/(N+1)`, the finite Hamiltonian is

.. math::
   :label: piab-core-finite-hamiltonian

   \mathbf H_h
   = \frac{\hbar^2}{2mh^2}
     \operatorname{tridiag}(-1,2,-1).

If :math:`\boldsymbol\Phi_M` contains the lowest :math:`M` orthonormal discrete
eigenvectors, then

.. math::
   :label: piab-core-projector

   \mathbf P_M=\boldsymbol\Phi_M\boldsymbol\Phi_M^{\mathsf T},
   \qquad \mathbf P_M^2=\mathbf P_M,

and the full-space and retained-coordinate representations are

.. math::
   :label: piab-core-representations

   \mathbf H_h^{(P_M)}=\mathbf P_M\mathbf H_h\mathbf P_M,
   \qquad
   \mathbf H_{\mathrm{red}}
   =\boldsymbol\Phi_M^{\mathsf T}\mathbf H_h\boldsymbol\Phi_M.

The consistently compressed residual is zero, while unmatched compression retains the
discarded sector

.. math::
   :label: piab-core-discarded-sector

   \mathbf P_M\mathbf H_h\mathbf P_M-\mathbf H_h
   =-\mathbf Q_M\mathbf H_h\mathbf Q_M,
   \qquad \mathbf Q_M=\mathbf I-\mathbf P_M.

A nonzero discarded sector is required only when :math:`M<N`. Full retention is valid
and is not required to manufacture a discarded component.

Symbols and conventions
-----------------------

:math:`L`, :math:`m`, and :math:`\hbar` are positive dimensionless parameters;
:math:`N` and :math:`M` are positive integer dimensions with :math:`M\leq N`;
:math:`\boldsymbol\Phi_M` has shape :math:`N\times M`; :math:`\mathbf P_M` and
:math:`\mathbf H_h` have shape :math:`N\times N`; and
:math:`\mathbf H_{\mathrm{red}}` has shape :math:`M\times M`. Matrix comparisons use
explicit Frobenius, spectral, entrywise, or relative conventions recorded by each
channel. All retained numerical arrays are finite binary64 values.

Verification and provenance
---------------------------

The verifier reconstructs 15 numerical channels covering the finite Hamiltonian,
closed-form spectra, retained basis, projector, embeddings, compression identities,
discarded sector, and boundary-realization difference. Source authentication uses the
shared PIAB1D source module and remains separate from numerical reconstruction.

The owning protocol is
``calculations/research-monograph/particle-in-box/protocol.md``; the retained payload is
``result.json``; maintained evidence is
``python/tests/software_verification/ksdft2effmass/campaigns/piab1d/test__Piab1dResultsVerifier.py``;
and scientific methodology is in
``docs/publications/research-monograph/appendices/D-particle-in-a-box-residuals.tex``.
Appendix D provides verified citations for the finite-difference and boundary-domain
background. The software thresholds and historical-runner admission are
repository-derived version-one policy.

Passing channels establish software and numerical verification for the represented
finite calculation only. They do not identify a physical effective potential, establish
continuum operator convergence, validate semiconductor physics, or quantify
uncertainty.

API
---

.. currentmodule:: ksdft2effmass.campaigns.piab1d.verification.core

.. autoclass:: Piab1dNumericalVerificationChannel
   :members:

.. autoclass:: Piab1dResultsVerifier
   :members:
