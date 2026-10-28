# Configuration numerics

## Exact parent input

The parent input consists of two four-by-four integer matrices and one positive common
denominator. The onsite numerator must be exactly symmetric. The positive-cell hopping
need not be symmetric because the calculation constructs its negative-cell partner by
conjugate transpose before forming each Hermitian parent Hamiltonian.

No floating matrix is stored in the configuration. The analyzer owns conversion to
binary64 `ComplexMatrixQuantity` values and the `HermitianHamiltonian` boundary.

## Finite inventories

Construction mesh sizes are positive, even, unique, and strictly increasing. The
production size is the largest declared size. Support radii are nonnegative, unique, and
strictly increasing, and every ordinary support excludes the smallest mesh's cyclic
Nyquist representative.

The evaluation rule stores a positive size and a proper positive rational stagger.
Construction/evaluation disjointness is checked exactly with `fractions.Fraction`, not by
binary64 proximity.

## Scalar admission

Integer controls require built-in `int`; booleans and NumPy integer subclasses reject.
Threshold and consistency controls require finite nonnegative built-in `float` values.
Threshold values are calculation inputs, while comparison directions remain fixed
algorithm behavior.

## Serialization

The typed mapping enumerates every field explicitly. Decoding requires exact field
identity and exact tuple/scalar container types before invoking the same constructor
invariants. No reflected dataclass-field inventory defines the wire.
