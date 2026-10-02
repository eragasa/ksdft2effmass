# Scientific retention: spaces, operators, and representations

## Manuscript meaning

In the research monograph, **retained** has a scientific meaning. It identifies the
state space and operator content kept by a declared projection, band selection,
disentanglement, or related reduction. It does not mean merely that a file was saved.

The governing distinctions are developed in:

- [Chapter 1, model adequacy](../../../../publications/research-monograph/chapters/01-model-adequacy.tex),
  which distinguishes an exact retained operator from an approximate effective model;
- [Appendix A, notation and status](../../../../publications/research-monograph/appendices/A-notation-and-status.tex),
  which defines the retained subspace, projector, frames, and interspace maps;
- [Appendix C, operator spaces, compression, and alignment](../../../../publications/research-monograph/appendices/C-operator-spaces-compression-alignment.tex),
  which distinguishes the parent operator, retained operator, and finite matrix
  representation; and
- [Appendix G, one-dimensional reduction](../../../../publications/research-monograph/appendices/G-one-dimensional-reduction.tex),
  which states that a lattice model approximates a retained Bloch operator or its
  dispersion rather than the original scalar potential directly.

This architecture preserves those distinctions in software. It does not replace the
mathematical definitions in the manuscript or an applicable versioned specification.

## Required object separation

The scientific path contains distinct objects:

```text
PeriodicModel
     |
     v
parent operator on an identified state space
     |
     +-- retention definition and projector/frame
     v
PeriodicRetainedSubspace
     |
     v
PeriodicRetainedOperator
     |
     +-- declared basis and representation map
     v
represented retained operator
     |
     +-- approximation or fit in a prescribed class
     v
EffectivePeriodicModel
```

The arrows are typed constructions or identifications, not inheritance claims.
Specifically:

- `PeriodicModel` identifies the modeled physical or mathematical periodic system.
- A retention definition identifies what is kept and how it is selected. Depending on
  the method, it records a spectral index set, energy window, projector, selected-band
  family, disentangled frame, or another explicitly specified construction.
- `PeriodicRetainedSubspace` represents the selected state space and its relationship
  to the parent space.
- `PeriodicRetainedOperator` represents the exact restriction or compression on that
  retained space. It is an operator, not a physical-model subclass.
- A represented retained operator is a finite matrix together with its basis, ordering,
  geometry, units, gauge, energy reference, and representation map. The matrix is not
  interchangeable with the abstract retained operator.
- An effective periodic model is an element of a prescribed approximate model class on
  an identified space. It is not identical to the exact retained operator merely
  because both have the same finite dimension or spectrum.

## Retention classification is metadata, not the object

A future closed retention-kind value may distinguish constructions such as spectral
restriction, selected-band retention, or a disentangled retained subspace. Such a
value classifies the construction only. A generic `RetainedType` cannot replace the
retained-space identity, parent relationship, projector or frame, rank, domain and
codomain, or operator data.

Retention is also not the same axis as `PeriodicModelRole`. `TOY` and
`MATERIAL_REFERENCE` state the evidentiary role of a scientific model. Either role may
participate in a retention construction.

## Required retained-space identity

A retained-space record must make the following information explicit when applicable:

- parent model and parent operator identities;
- ambient and retained state-space identities;
- spatial dimension;
- selection or construction method and its parameters;
- retained rank and ordered band, orbital, or frame identities;
- projector or orthonormal frame identity;
- reciprocal mesh or continuous-domain convention;
- spin and internal-degree-of-freedom conventions; and
- provenance needed to reproduce the selection.

Equal rank is not retained-space compatibility. Comparisons between independently
constructed retained spaces require an explicit identification or alignment result.

## Required retained-operator identity

A retained-operator record must identify its retained domain and codomain, parent
operator, restriction or compression construction, units, energy reference, and
Hermiticity status. A Bloch-family record also identifies reciprocal coordinates,
mesh or domain, band or frame ordering, gauge convention, and reciprocal-boundary
sewing convention.

Pristine and defect retained operators are not subtracted until an owning alignment
Action supplies a common space and records the direction of transport. Parent-model,
retained-subspace, representation, and model-class approximation errors remain
separate.

## Evidence retention is a different meaning

The repository also retains files, payloads, checksums, reports, and results as
historical evidence. That preservation meaning must be qualified as **retained
evidence**, **retained artifact**, **retained result**, or **encoded campaign
document**. It must not be used to classify a byte container as a scientific retained
space or operator.

Current classes under campaign `model/retained/` paths that contain only
`input_payload` and `result_payload` bytes are encoded campaign-document records. They
are not implementations of `PeriodicRetainedSubspace`, `PeriodicRetainedOperator`, or
`PeriodicModel`, regardless of their historical `...CampaignModel` names. Migration
will rename and relocate those records while preserving their exact bytes and
provenance.
