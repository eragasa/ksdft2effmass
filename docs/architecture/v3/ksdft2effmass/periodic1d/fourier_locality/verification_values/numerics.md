# Independent-verification-value numerics

The independent route directly assembles each `4 x 4` parent matrix from the frozen
rational coefficients and complex phases. It uses a Hermitian eigensolver only for the
two lowest ordered values.

Fourier coefficients and inverse candidates are calculated from explicit dense phase
matrices rather than production transform objects. Truncations use direct support masks.
Equal-weight direct fits use an independently assembled Hermitian real design and
`numpy.linalg.lstsq`.

Maximum, root-mean-square, omitted-norm, Parseval, route, gap, dominance, passage, and
refinement values are reconstructed from explicit formulas. Every inventory is regenerated
from the configuration rather than copied from the subject result.

The independent route uses binary64 and the same declared finite problem. It is
algorithmically independent, not an arbitrary-precision or interval oracle.
