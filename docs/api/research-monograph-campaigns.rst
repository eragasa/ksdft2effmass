Research-monograph campaigns
=============================

``ksdft2effmass.campaigns.research_monograph`` contains public composition and
retained-format contracts for the project's research-monograph calculations.  These
campaign objects bind exact study controls to reusable analysis contracts.  They do
not own generic scientific algorithms, grant protected execution authority, or decide
scientific acceptance.  Campaign implementation classes and methods are public and
use no underscore-prefixed implementation names; Python-required special methods are
the only exception.

Harmonic-oscillator study
-------------------------

The Appendix E campaign deserializes its closed version-one input, evaluates the
ordered Cartesian product of interval half-width, grid spacing, and retained
dimension, and serializes the resulting comparisons with explicit source identities.
The retained historical result remains bound to its original runner identity.  Newly
authored records bind the current public model-system and campaign implementation
sources; this does not relabel historical evidence.

.. currentmodule:: ksdft2effmass.campaigns.research_monograph

.. autoclass:: HarmonicOscillatorStudyDefinition
   :members:

.. autoclass:: HarmonicOscillatorStudyResult
   :members:

.. autoclass:: HarmonicOscillatorStudyInputDeserializer
   :members:

.. autoclass:: HarmonicOscillatorStudyEvaluator
   :members:

.. autoclass:: HarmonicOscillatorStudyResultSerializer
   :members:

.. autoclass:: HarmonicOscillatorResultVerifier
   :members:

Particle-in-a-box residual study
--------------------------------

The Appendix D core residual campaign deserializes its retained version-one input,
composes the public one-dimensional box and represented-operator contracts, preserves
the historical numerical JSON payload, and verifies retained or newly authored
provenance without importing the implementation under verification. Public Workflows
also own the convergence, higher-eigenpair, norm, and identifiability campaigns while
calculation-directory runners and verifiers remain thin CLI adapters.

.. autoclass:: ParticleInBoxStudyDefinition
   :members:

.. autoclass:: ParticleInBoxResidualStudyResult
   :members:

.. autoclass:: ParticleInBoxStudyInputDeserializer
   :members:

.. autoclass:: ParticleInBoxResidualStudyEvaluator
   :members:

.. autoclass:: ParticleInBoxStudyResultSerializer
   :members:

.. autoclass:: ParticleInBoxResultVerifier
   :members:

.. autoclass:: ParticleInBoxConvergenceWorkflow
   :members:

.. autoclass:: ParticleInBoxConvergenceVerifier
   :members:

.. autoclass:: ParticleInBoxEigenpairSweepWorkflow
   :members:

.. autoclass:: ParticleInBoxEigenpairSweepVerifier
   :members:

.. autoclass:: ParticleInBoxNormSweepWorkflow
   :members:

.. autoclass:: ParticleInBoxNormSweepVerifier
   :members:

.. autoclass:: RetainedModelClassFitResult
   :members:

.. autoclass:: RetainedModelClassFitter
   :members:

.. autoclass:: ParticleInBoxIdentifiabilityWorkflow
   :members:

.. autoclass:: ParticleInBoxIdentifiabilityVerifier
   :members:
