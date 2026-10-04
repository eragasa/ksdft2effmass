One-dimensional selected-band retention
=======================================

.. currentmodule:: ksdft2effmass.periodic1d

:class:`Periodic1DSelectedBandRetentionDefinition` composes a reusable
``ContiguousBandSelection`` with the general parent-qualified
:class:`~ksdft2effmass.periodic.PeriodicRetentionDefinition`.

The inclusive ascending band interval supplies ordered parent-band indices.  The
general definition supplies parent model, parent operator, ambient state space,
retained-space identity, reciprocal domain, construction-record identity,
assumptions, and provenance.  The retained-state labels correspond elementwise to the
ascending selected indices.

Construction requires an exact one-dimensional parent, the
``SELECTED_BANDS`` retention kind, and equality between retained rank and selected band
count.  It does not inspect eigenvalues, establish band isolation, construct a
projector or frame, choose a gauge, or create a retained operator.

:class:`Periodic1DRetainedBandGroupDefinition` adds one stable group identity while
preserving the complete parent-qualified selected-band definition.  Its convenience
properties expose the same ordered interval and rank without duplicating scientific
identity.

:class:`Periodic1DBandFrameRetainedSubspace` binds ordered reciprocal-path frames
and endpoint sewing data to the scientific retained space while preserving the
frame's gauge dependence.  Rank and ambient dimension must agree exactly.  Its
``frame_content_sha256`` reauthenticates the ordered frame matrices canonicalized as
little-endian complex128 in reciprocal-point, ambient-basis, retained-state C order;
the mesh and sewing map are outside that digest scope.  This represented-content
digest is not mathematical retained-space identity.

:class:`Periodic1DOrthogonalSpectralRetainedSubspace` separately binds an
``OrthogonalSpectralSubspace`` numerical embedding to a parent-qualified scientific
retained space.  Its retained and ambient dimensions must agree exactly; the numerical
eigenvectors do not supply parent or reciprocal-domain identity by themselves.

These objects are scientific retention definitions and represented retained-space data,
not campaign definitions or encoded
document.  Its synthetic tests are software verification only and establish no
numerical verification, physical adequacy, scientific validation, or uncertainty
quantification.

.. autoclass:: Periodic1DSelectedBandRetentionDefinition
   :members:

.. autoclass:: Periodic1DRetainedBandGroupDefinition
   :members:

.. autoclass:: Periodic1DOrthogonalSpectralRetainedSubspace
   :members:

.. autoclass:: Periodic1DBandFrameRetainedSubspace
   :members:
