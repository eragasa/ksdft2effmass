# Scientific interpretation

A `TransformationIdentity` identifies one directed derivation edge between complete
representation-node identities. It records transformation kind, method identity, and an
explicit source/target and adjoint-orientation convention.

The kind enum distinguishes frame compression, gauge conjugation, alignment, finite
Fourier conversion, support truncation, and Fourier reconstruction. These are not
exclusive node roles. A retained Bloch node may participate in multiple derivation edges.

The identity is metadata. It is not an executed operation, numerical witness,
qualification result, evidence record, or formal proof.
