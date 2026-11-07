# Numerical behavior

Construction requires an exact `RepresentationTransformationKind`, exact source and
target `RepresentationIdentity` instances, and nonempty exact strings for edge identity,
method, and orientation. The role-transition helper admits only the combinations encoded
for the six enum members.

No matrix dimension, mesh equality, basis equality, coordinate convention, support
subset, Fourier pairing, residual, or tolerance is checked. The factory performs the
same exact nominal checks before delegating to the immutable identity constructor.
