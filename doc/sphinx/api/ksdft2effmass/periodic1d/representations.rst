One-dimensional retained-operator representations
==================================================

.. currentmodule:: ksdft2effmass.periodic1d

An exact :class:`~ksdft2effmass.periodic.PeriodicRetainedOperator` is independent
of the finite basis and gauge used to represent it.
:class:`Periodic1DRetainedOperatorReciprocalRepresentation` binds that exact
operator to matrices on one complete reciprocal mesh, while
:class:`Periodic1DRetainedOperatorHoppingRepresentation` binds it to all
centered Born--von Karman hopping representatives for the same finite mesh.

Both records retain explicit ordered orthonormal basis, energy-reference,
representation-map, gauge, provenance, and canonical array-content identities. They
authenticate represented array bytes and validate retained labels, energy units and
zero, rank, and mesh compatibility. They do not choose or reconstruct a frame, assess
gauge quality, truncate coefficients, create an effective model, or establish
scientific validation or uncertainty quantification.

The hopping-family record is deliberately distinct from
:class:`Periodic1DCompleteHoppingRepresentationResult`. The latter is a construction
ResultObject that owns a complete reciprocal-to-hopping Fourier transform, including
its source, reconstructed samples, and numerical reconstruction diagnostics. By
contrast, :class:`Periodic1DRetainedOperatorHoppingRepresentation` binds an already
retained complete hopping family to an exact operator, basis, and gauge and
authenticates its coefficient bytes. It does not assert that a reciprocal source or
transform result is available. This distinction is required for the retained
composite rough-gauge hoppings, whose reciprocal matrices were not preserved.

.. autoclass:: Periodic1DRetainedOperatorReciprocalRepresentation
   :members:

.. autoclass:: Periodic1DRetainedOperatorHoppingRepresentation
   :members:
