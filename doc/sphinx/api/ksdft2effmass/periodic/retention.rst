Periodic scientific retention
=============================

.. currentmodule:: ksdft2effmass.periodic

Purpose and ownership
---------------------

The phase-four retention API separates a modeled periodic system, a retained
mathematical state space, an exact operator on that space, and one finite matrix
representation.  These objects are related by explicit construction rather than
inheritance.

The usual path is:

.. code-block:: text

   PeriodicOperatorReference + PeriodicRetentionDefinition
       -> PeriodicRetainedSubspaceConstructor
       -> PeriodicRetainedSubspace
       -> PeriodicRetainedOperatorConstructor
       -> PeriodicRetainedOperator
       -> PeriodicRepresentedRetainedOperatorConstructor
       -> PeriodicRepresentedRetainedOperator

Parent models and operators are referenced by stable identity.  The API does not
embed arbitrary model implementations, resolve identities, load files, execute
calculations, compute projectors, choose gauges, align spaces, convert units, shift
energy zeros, truncate couplings, or fit effective models.

Mathematical distinction
------------------------

For an orthogonal projector :math:`P` acting on the parent space
:math:`\mathcal H`, the retained space is

.. math::

   \mathcal H^{(P)}=\operatorname{im}P.

The exact retained operator is

.. math::

   H^{(P)}=
   \left.PHP\right|_{\mathcal H^{(P)}}:
   \mathcal H^{(P)}\longrightarrow\mathcal H^{(P)}.

This differs from the ambient compression ``P H P`` considered as an operator on
the full parent space.  For an ordered orthonormal retained basis
:math:`(|b_i\rangle)`, the finite coordinates are

.. math::

   H^{(P)}_{ij}=\langle b_i|H^{(P)}|b_j\rangle.

A unitary frame change can change these coordinates without changing the retained
space or exact operator.  Consequently, equal dimensions or spectra do not establish
basis or gauge alignment.

Representation binding
----------------------

:class:`PeriodicRepresentedRetainedOperator` composes an exact retained operator with
an :class:`~ksdft2effmass.operators.OperatorRecord`.  Construction requires exact
agreement of:

* retained and represented state-space identity;
* retained rank, matrix dimension, and state-space dimension;
* ordered retained labels and represented basis ordering; and
* exact energy unit and scalar energy-zero convention.

The ``OperatorRecord`` continues to own matrix entries, basis, geometry, energy
reference, and represented provenance.  The binding adds the exact retained-operator,
representation-map, and gauge identities without copying those fields.

Exact agreement is a software binding precondition.  It is not unit conversion,
energy alignment, gauge alignment, physical equivalence, numerical verification, or
scientific validation.  Incompatible construction fails rather than reordering,
padding, truncating, converting, shifting, or inferring an alignment.

Evidence boundary
-----------------

Construction tests use synthetic records and provide software verification of type,
identity, ordering, and dimension behavior.  They do not verify projector
orthogonality, subspace isolation, gauge smoothness, exact numerical compression,
material realism, scientific validation, or uncertainty quantification.

Preserved campaign payloads are encoded documents, not scientific retained spaces or
operators.  Truncation and fitting construct approximate effective models and remain
outside this API.

Public API
----------

.. autoclass:: PeriodicRetentionKind
   :members:

.. autoclass:: PeriodicRetainedOperatorConstructionKind
   :members:

.. autoclass:: PeriodicHermiticityStatus
   :members:

.. autoclass:: PeriodicOperatorReference
   :members:

.. autoclass:: PeriodicRetentionDefinition
   :members:

.. autoclass:: PeriodicRetainedSubspace
   :members:

.. autoclass:: PeriodicRetainedSubspaceConstructor
   :members:

.. autoclass:: PeriodicRetainedOperator
   :members:

.. autoclass:: PeriodicRetainedOperatorConstructor
   :members:

.. autoclass:: PeriodicRepresentedRetainedOperator
   :members:

.. autoclass:: PeriodicRepresentedRetainedOperatorConstructor
   :members:
