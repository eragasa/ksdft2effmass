Scientific Workflow model
=========================

Use the package-level imports documented here.  These contracts represent
calculator-independent scientific composition; they do not invoke Tasks,
execute calculators, persist Workflow runs, or establish scientific validity.
Generic colored-Petri-net contracts remain under
:mod:`ksdft2effmass.petrinet.colored`.

Protocols
---------

.. currentmodule:: ksdft2effmass.workflows

.. autoclass:: ResultObject
   :members:

.. autoclass:: Task
   :members:

.. autoclass:: Workflow
   :members:

Identities and operation inputs
-------------------------------

.. autoclass:: ResultObjectIdentity
.. autoclass:: TaskDefinitionIdentity
.. autoclass:: TaskInstanceIdentity
.. autoclass:: WorkflowIdentity
.. autoclass:: WorkflowRunIdentity
.. autoclass:: TaskStartGateIdentity
.. autoclass:: TaskStartGateSetIdentity
.. autoclass:: TaskActivationIdentity
.. autoclass:: OperationIdentity
.. autoclass:: AttemptIdentity
.. autoclass:: TaskInputBinding
.. autoclass:: TaskExecutionContext

Composition and gates
---------------------

.. autoclass:: TaskStartGateSetMode
   :members:

.. autoclass:: TaskStartGate
.. autoclass:: TaskStartGateSet
   :members:
.. autoclass:: TaskInstance
.. autoclass:: WorkflowComposition

Activation selections
---------------------

``TaskActivationSelection`` is the public union of the three selection records
below.  Using separate records prevents gate-only fields from appearing on a
direct activation.

.. autoclass:: DirectTaskActivationSelection
.. autoclass:: AnyOfTaskActivationSelection
.. autoclass:: AllOfTaskActivationSelection
.. autoclass:: TaskGateSelection
.. autoclass:: TaskActivation
