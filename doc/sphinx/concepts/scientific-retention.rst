Scientific retention
====================

``Retained`` has two different meanings in research software.  Scientific retention
selects a state space and operator content from a declared parent.  Evidence retention
preserves payloads, reports, checksums, or other historical artifacts.  The two must not
be represented by the same software type merely because both use the word
``retained``.

Four distinct objects
---------------------

The periodic scientific API separates four objects:

#. A :class:`~ksdft2effmass.periodic.PeriodicModel` identifies the modeled
   physical or mathematical system.
#. A :class:`~ksdft2effmass.periodic.PeriodicRetainedSubspace` identifies selected
   state space and its relation to the parent space.
#. A :class:`~ksdft2effmass.periodic.PeriodicRetainedOperator` identifies the exact
   operator whose domain and codomain are that retained space.
#. A :class:`~ksdft2effmass.periodic.PeriodicRepresentedRetainedOperator` binds the
   exact operator to one finite matrix representation and its coordinates.

These are not successive subclasses.  Explicit ActionObjects construct the relations
among them.

Projectors, frames, and gauges
------------------------------

For an orthogonal projector :math:`P`, the retained space is

.. math::

   \mathcal H^{(P)}=\operatorname{im}P.

An orthonormal frame :math:`F:\mathbb C^r\to\mathcal H` represents that space when

.. math::

   F^\dagger F=I_r,
   \qquad
   P=FF^\dagger.

For any unitary :math:`G\in U(r)`, the frame :math:`F'=FG` has the same projector:

.. math::

   F'F'^\dagger=P.

The frame and gauge therefore matter for matrix coordinates but do not, by themselves,
define a different retained subspace.  This is why the software records retained-space
identity separately from projector-or-frame record identity and represented gauge
identity.

Exact operators and matrices
----------------------------

The exact retained operator is

.. math::

   H^{(P)}=
   \left.PHP\right|_{\mathcal H^{(P)}}:
   \mathcal H^{(P)}\to\mathcal H^{(P)}.

It is not interchangeable with the ambient compression acting on the full parent
space.  It is also not interchangeable with its represented matrix

.. math::

   H^{(P)}_{ij}=\langle b_i|H^{(P)}|b_j\rangle.

Under a unitary basis change, the matrix changes covariantly as

.. math::

   \mathbf H^{(P)\prime}=G^\dagger\mathbf H^{(P)}G.

The public representation binding consequently requires exact retained-space identity,
dimension, basis ordering, energy unit, and scalar energy-zero agreement. It never
infers alignment from equal shape or equal eigenvalues.

Numerical compression boundary
------------------------------

For a finite real matrix :math:`H` and an orthonormal embedding :math:`Q`, the reusable
:class:`~ksdft2effmass.operators.OperatorCompression` Action computes

.. math::

   H_{\mathrm{coord}}=Q^T H Q,
   \qquad
   P=QQ^T,
   \qquad
   H_{\mathrm{ambient}}=PHP=QH_{\mathrm{coord}}Q^T.

The coordinate and ambient matrices encode the same compressed action on the selected
finite subspace but act on different declared spaces. If the selected subspace is
invariant, the coordinate matrix represents the exact restriction of that finite
operator. If it is not invariant, the matrix is a projected compression and its
eigenvalues are Ritz values. This operation is not energy-dependent downfolding and
does not include discarded-space resolvent corrections.

:class:`~ksdft2effmass.operators.OperatorCompressionResult` remains numerical evidence.
It carries no stable parent-model, parent-operator, retained-space, basis, gauge,
energy-zero, invariance, or provenance identity. A scientific retained operator must
attach those meanings explicitly; dimensions, matrix values, or a compression route do
not supply them by inference.

Stable references
-----------------

:class:`~ksdft2effmass.periodic.PeriodicOperatorReference` records stable identities
for the parent model, operator, and ambient state space together with exact periodic
spatial dimension.  The reference is not a Python model implementation, repository
root, path, URL, or loader.  Keeping resolution outside the scientific DataObject
prevents records from acquiring hidden filesystem, campaign, or execution behavior.

Selected-band definitions
-------------------------

:class:`~ksdft2effmass.periodic1d.Periodic1DSelectedBandRetentionDefinition` and
:class:`~ksdft2effmass.periodic2d.Periodic2DSelectedBandRetentionDefinition` compose a
reusable inclusive band-index interval with the general parent-qualified retention
definition.  The dimensional specializations require the exact parent dimension,
``SELECTED_BANDS`` construction kind, and equality between selected-band count and
retained rank.

These records declare what is selected and preserve ordered labels and stable parent,
operator, state-space, reciprocal-domain, construction, assumption, and provenance
identities.  They do not contain a projector, frame, represented operator, or finite
matrix and therefore do not by themselves identify a retained mathematical subspace.
Projection, disentanglement, basis transformation, and truncation remain separate
operations.

Construction boundary
---------------------

The public Actions bind already identified records:

* :class:`~ksdft2effmass.periodic.PeriodicRetainedSubspaceConstructor` binds a
  parent-qualified retention definition to retained-space metadata;
* :class:`~ksdft2effmass.periodic.PeriodicRetainedOperatorConstructor` binds the
  parent and retained domain/codomain to an exact restriction or compression; and
* :class:`~ksdft2effmass.periodic.PeriodicRepresentedRetainedOperatorConstructor`
  binds a compatible :class:`~ksdft2effmass.operators.OperatorRecord` to the exact
  retained operator.

These Actions do not compute eigenvectors, projectors, compressions, Fourier
transforms, gauge choices, or effective-model fits.  Existing numerical objects retain
those narrower meanings until a specialized later-phase Action composes them with the
scientific identities.

Approximation and evidence boundaries
-------------------------------------

Changing complete coordinates need not approximate the retained operator.  Truncating
hopping blocks or fitting a restricted model class does introduce an approximation and
must produce a separately identified effective model and reduction result.

Software construction checks establish only the documented type, identity, ordering,
and dimension contract.  They do not show that a retained subspace is physically
appropriate, that a numerical projector is accurate, that a gauge is smooth, or that
an effective model is scientifically valid.  Parent-model, numerical or discretization,
and model-reduction errors remain separate.

For the complete API, see :doc:`../api/ksdft2effmass/periodic/retention`.
