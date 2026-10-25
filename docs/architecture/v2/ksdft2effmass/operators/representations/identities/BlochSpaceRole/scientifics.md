# Scientific interpretation

`BlochSpaceRole.ambient` identifies a Bloch node intended to act on the declared parent
represented space. `BlochSpaceRole.retained` identifies a Bloch node intended to act on a
declared retained represented space.

Gauge conjugation, alignment, and Fourier reconstruction are not Bloch space roles. They
are derivation edges. A node may remain `BlochSpaceRole.retained` while carrying all three
kinds of incoming or outgoing transformation history.
