# Implementation

`SpectralReduction(hamiltonian=..., spectral_subspace=...)` eagerly constructs one
correlated result. Its `reduced_hamiltonian` property returns that exact
`ReducedHamiltonian` by identity.

Construction retains the exact parent and subspace objects, delegates the two
coordinate transformations to the subspace, and applies no acceptance tolerance.

`OrthogonalSpectralSubspace` performs sparse parent multiplication without an implicit
dense-parent conversion. It materializes the reduced and embedded matrices because
both are declared result representations.

There is one reduction implementation. The superseded `OperatorCompression`, its
result record, and the prospective request/reducer hierarchy are removed rather than
retained as compatibility APIs.
