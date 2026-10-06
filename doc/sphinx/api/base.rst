Package-wide data-object bases
==============================

``ksdft2effmass.base`` supplies the thin package-wide structural and functional
hierarchy used by provisional workflow v2.  The hierarchy owns no scientific
algorithm, workflow policy, persistence, discovery, serialization, or external
effect.  Constructors and intrinsic invariant checks remain data-object behavior;
material operations use immutable requests, concrete actionizers, and immutable
results.

Thin public hierarchy
---------------------

.. currentmodule:: ksdft2effmass.base

.. autoclass:: DataObject
   :members:
.. autoclass:: DataObjectModel
   :members:
.. autoclass:: DataObjectActionRequest
   :members:
.. autoclass:: DataObjectActionResult
   :members:
.. autoclass:: DataObjectActionizer
   :members:

Nominal data-object specializations
-----------------------------------

.. currentmodule:: ksdft2effmass.base.data_object

.. autoclass:: AbstractDataObject
   :members:

.. currentmodule:: ksdft2effmass.base.immutable

.. autoclass:: AbstractImmutableDataObject
   :members:

.. currentmodule:: ksdft2effmass.base.identity

.. autoclass:: AbstractIdentity
   :members:

.. currentmodule:: ksdft2effmass.base.validation

.. autoclass:: AbstractValidation
   :members:

.. currentmodule:: ksdft2effmass.base.derivation

.. autoclass:: AbstractDerivation
   :members:

Configurable actionizers
------------------------

.. currentmodule:: ksdft2effmass.base.actionizer.configuration

.. autoclass:: AbstractActionConfiguration
   :members:

.. currentmodule:: ksdft2effmass.base.actionizer.request

.. autoclass:: ConfigurableDataObjectActionRequest
   :members:

.. currentmodule:: ksdft2effmass.base.actionizer.configurable

.. autoclass:: ConfigurableDataObjectActionizer
   :members:
