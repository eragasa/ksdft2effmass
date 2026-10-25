# Scientific interpretation

The enum classifies derivation edges:

- `frame_compression` records `F† H F` from an ambient represented space to a retained
  represented space; it is not projector construction `P = F F†` and is a restriction
  only when a separately stated invariance hypothesis applies;
- `gauge_conjugation` records an internal-coordinate conjugation;
- `alignment` records a corrective transformation under a declared admissible family;
- `finite_fourier_conversion` changes from a momentum-domain Bloch carrier to a
  translation-domain cell-hopping carrier;
- `support_truncation` restricts the declared coefficient inventory; and
- `fourier_reconstruction` changes back to a momentum-domain Bloch carrier.

A retained Bloch node may have several of these edge kinds in its derivation history.
Therefore none is an exclusive Bloch node state.
