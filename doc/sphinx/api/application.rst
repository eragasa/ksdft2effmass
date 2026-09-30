Application result-value composition
====================================

This provisional package exposes only explicit seven-family result-codec composition,
not the separately planned application composition root, configuration resolver,
database defaults or execution service. See
:doc:`../concepts/workflow-run-persistence` for exact wire and evidence limits.

Three named immutable dependencies are supplied explicitly::

    from ksdft2effmass.analysis import QuantityOfInterestResultValueSerializer
    from ksdft2effmass.application import ApplicationResultValueSerializer
    from ksdft2effmass.integration.quantum_espresso import (
        QuantumEspressoResultValueSerializer,
    )
    from ksdft2effmass.workflows import WorkflowResultValueSerializer

    qe = QuantumEspressoResultValueSerializer()
    codec = ApplicationResultValueSerializer(
        workflow_codec=WorkflowResultValueSerializer(source_codec=qe),
        quantum_espresso_codec=qe,
        quantity_of_interest_codec=QuantityOfInterestResultValueSerializer(),
    )

The Workflow source dependency must be an exact QE serializer. Independently created
instances of that stateless immutable codec are equivalent; Python object identity
is not part of the wire contract. Dependencies must be the exact supported frozen
serializers, not subclasses or arbitrary mutable ports; wrong types raise
``TypeError``. Explicit
branches route two Workflow, three QE and two scalar classes and their version-one
concrete type labels. Owning codecs retain complete payloads and closed failure
records. Unknown concrete types/versions remain incompatible. No registry, discovery,
dynamic imports, native I/O, scientific transformations or store selection occurs.

.. currentmodule:: ksdft2effmass.application

.. autoclass:: ApplicationResultValueSerializer
   :members:
