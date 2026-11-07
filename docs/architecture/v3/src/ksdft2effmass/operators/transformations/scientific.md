# Scientific interpretation

## Directed derivation identity

A transformation identity describes a directed edge between complete representation
identities. It records an explicit transformation kind, method identity, orientation
text, source identity, and target identity. It neither stores transformed matrices nor
asserts that an operation was executed.

The implemented kinds distinguish:

- frame compression \(F^\dagger H F\);
- gauge conjugation;
- alignment;
- finite Fourier conversion;
- support truncation; and
- Fourier reconstruction.

These are derivation kinds rather than node roles. Compression remains distinct from
projector formation \(F F^\dagger\) and from restriction to an invariant subspace.
Fourier conversion, truncation, and reconstruction remain distinct edges.

## Nominal computation

Every future concrete request, Action, and result must expose one exact
`RepresentationTransformationKind`. Kind agreement identifies the intended operation
family only. It does not prove dimensional compatibility, witness validity, numerical
correctness, property preservation, qualification, scientific validity, or theorem
applicability.

## Current role-transition scope

The implemented edge identity admits the KSD transitions encoded in source:
ambient-to-retained frame compression, retained-to-retained gauge conjugation or
alignment, retained-Bloch to complete-declared cell hopping, complete-declared to
support-truncated cell hopping, and cell-hopping to retained-Bloch reconstruction.
These are current KSD contracts, not claims of universal mathematical coverage.
