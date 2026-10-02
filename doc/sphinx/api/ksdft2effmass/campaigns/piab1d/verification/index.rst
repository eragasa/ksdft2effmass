PIAB1D independent verification
===============================

The PIAB1D verification package authenticates retained source identities and
independently reconstructs numerical results without importing the maintained
calculation Workflows, constructors, evaluators, serializers, or eigensolver
implementations under verification. Source identity, numerical agreement, and aggregate
disposition remain separate typed outcomes.

These verifiers concern controlled, dimensionless, finite particle-in-a-box
calculations. Passing reports establish only their stated software and numerical
verification checks. They do not establish semiconductor evidence, scientific
validation, transferability, or uncertainty quantification.

.. toctree::
   :maxdepth: 1

   decoder
   source
   core
   convergence
   eigenpair_sweep
   norm_sweep
   identifiability
