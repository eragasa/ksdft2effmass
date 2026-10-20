# Implementation

`RealSymmetricOperatorReducer(request).reduce()` is the target signature. The frozen,
slotted action retains exactly one `RealSymmetricOperatorReductionRequest`; `reduce()`
accepts no arguments and returns one correlated result.

For basis matrix `Q`, the action constructs retained coordinates, projector, embedded
operator, and invariance residual. It may materialize the finite operator where required
by the declared result matrices. It does not call norm, comparison, fitting,
serialization, or plotting actions.

The source may depend on `ksdft2effmass.operators` types and NumPy. It must not import
model systems or outward composition owners.

Before implementation, the existing `OperatorCompression` overlap must be resolved.
The preferred implementation has one numerical kernel and no compatibility facade or
duplicate public behavior.

Target tests use small exact matrices and separately exercise trial and spectral
subspace nominal types. Model-specific tests remain outward evidence.
