# Scientific interpretation

## Separation of objects

A mathematical operator, a finite matrix representation of that operator, and the history
by which one representation was derived are distinct objects. This package describes the
finite carrier, represented space, intended field role, and intrinsic representation
identity. It does not identify a derivation edge.

## Carriers

A Bloch matrix field is sampled on a finite momentum domain and is interpreted as

\[
H:K\longrightarrow \operatorname{End}(V).
\]

A cell-hopping field is indexed by a finite ordered translation inventory and is
interpreted as

\[
\widehat H:\Gamma\longrightarrow \operatorname{End}(V).
\]

The two carriers use different role enums. Momentum-domain roles distinguish ambient and
retained represented spaces. Translation-domain roles distinguish a complete declared
finite inventory from a support-truncated inventory. “Complete” never means complete over
an infinite lattice.

## Explicit interpretation

`RepresentationSpaceIdentity` composes state space, ordered basis, geometry, energy
reference, mathematical scalar-field identity, and coordinate-convention identity. Equal
array shape is not enough to establish a common space or basis.

Field class names state intended roles only. They do not establish Hermiticity,
idempotency, unitarity, isometry, periodicity, sewing, support completeness, Fourier
pairing, or reconstruction correctness.

## Exclusions

The package provides no physical-model law, eigensolver selection, gauge choice,
alignment policy, error threshold, evidence disposition, scientific decision, or formal
proof.
