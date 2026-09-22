Development-harness validation
==============================

The validation API inspects one complete immutable ``HarnessState`` without changing
it. Each concrete domain validator returns the same identity-bearing
``ValidationResult`` contract. ``HarnessStateValidator`` composes only the explicit
ordered validator tuple supplied by its caller and additionally evaluates the
aggregate decision sequence and capability-to-resource closure. No registry,
default rule set, repair, authority resolution, persistence, projection, or successor
selection occurs.

A passing result establishes only the represented structural rules for the exact
normalized state identity. It does not establish pytest success, coding-standards
conformance for another subject, numerical verification, scientific validation,
uncertainty quantification, protected authority, or human acceptance. This API defines
no public serialization or wire format.

Results and rule identities
---------------------------

.. currentmodule:: ksdft2effmass.harness

.. autoclass:: ValidationApplicability
.. autoclass:: ValidationStatus
.. autoclass:: ValidationRuleIdentity
   :members:
.. autoclass:: ValidationFinding
   :members:
.. autoclass:: ValidationResult
   :members:
.. autoclass:: ActivationReferenceRequirement
.. autoclass:: DevelopmentTaskSelectionValidationPolicy

``ValidationResult.blocking`` is derived rather than caller-selected. A required
``fail``, ``error``, or ``not_run`` blocks its gate; an optional failure remains a
failed result but does not block by itself. Composite status precedence is ``error``,
then ``not_run``, then ``fail``, then ``pass`` across applicable children. Composite
results retain the complete child values and expose their exact identities through
``child_result_identities``.

Validators
----------

.. autoclass:: HarnessDomainValidator
   :members:
.. autoclass:: DevelopmentTaskSelectionValidator
   :members:
.. autoclass:: HarnessTaskGraphValidator
   :members:
.. autoclass:: HarnessCapabilityCatalogValidator
   :members:
.. autoclass:: HarnessResourceCatalogValidator
   :members:
.. autoclass:: HarnessEvidenceCatalogValidator
   :members:
.. autoclass:: HarnessStateValidator
   :members:

The evidence-catalog validator checks exact source paths, byte identities, and source
closure only. Evidence ownership, evidence identifiers, test semantics, and claim
classification remain with downstream coding-standards conformance.
