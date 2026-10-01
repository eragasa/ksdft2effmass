PIAB1D retained-space identifiability verification
==================================================

Purpose
-------

``Piab1dIdentifiabilityResultsVerifier`` reconstructs the finite retained-space
arithmetic in the version-one identifiability study. The study writes two decompositions
of the same reduced Hamiltonian and fits one illustrative shift to four declared matrix
classes. Verification checks those equations; it does not decide which class is a
physical model.

Mathematics
-----------

Let :math:`H_r` be the retained Hamiltonian and :math:`S` the illustrative real
symmetric shift. The two represented decompositions are

.. math::

   H_r = T_{\mathrm{physical}} + V_{\mathrm{physical}},
   \qquad V_{\mathrm{physical}}=0,

and

.. math::

   H_r = T_{\mathrm{shifted}} + V_{\mathrm{shifted}},
   \qquad V_{\mathrm{shifted}}=S.

For each declared model class :math:`\mathcal{M}`, the retained best fit
:math:`S_{\mathcal{M}}` and unexplained residual
:math:`R_{\mathcal{M}}=S-S_{\mathcal{M}}` are reconstructed directly. The checked model
classes are scalar identity, diagonal in the retained basis, real symmetric
tridiagonal, and arbitrary real symmetric matrices. The reported scalar diagnostic is
:math:`\lVert R_{\mathcal{M}}\rVert_F`.

Algorithm and tolerances
------------------------

The verifier checks matrix dimensions, symmetry of :math:`S`, both decomposition sums,
potential assignments, exact model-class inventory, best-fit matrices, residual
matrices, and residual Frobenius norms. The maximum antisymmetric entry of the retained
Hamiltonian uses ``5e-15`` because that matrix was formed by a binary64 basis
transformation. Decomposition sums use ``2e-14``; reported Frobenius norms use
``2e-15``. Exact constructed matrices use zero tolerance.

Residual ordering is intentionally not a verification condition. Comparing or ranking
model classes is analysis. A smaller algebraic residual does not by itself establish
physical identifiability.

The source report also checks the retained parent ``result.json`` identity in addition
to the study input and historical runner identity.

Usage
-----

.. code-block:: python

   from pathlib import Path
   from ksdft2effmass.campaigns.piab1d import (
       Piab1dIdentifiabilityResultsVerifier,
   )

   report = Piab1dIdentifiabilityResultsVerifier().execute(
       Path(
           "calculations/research-monograph/particle-in-box/"
           "identifiability-result.json"
       ),
       Path("."),
   )
   assert report.passes

Implementation, evidence, and limits
------------------------------------

The implementation is
``python/src/ksdft2effmass/campaigns/piab1d/verification/identifiability.py``. Tests and
retained inputs are under the corresponding PIAB1D test and calculation directories.
The shift is illustrative and has no assigned physical meaning. Results depend on the
retained basis, selected matrix classes, and Frobenius metric. A passing report does not
validate a material model or prove physical identifiability.

API
---

.. currentmodule:: ksdft2effmass.campaigns.piab1d.verification.identifiability

.. autoclass:: Piab1dIdentifiabilityVerificationChannel
   :members:

.. autoclass:: Piab1dIdentifiabilityResultsVerifier
   :members:
