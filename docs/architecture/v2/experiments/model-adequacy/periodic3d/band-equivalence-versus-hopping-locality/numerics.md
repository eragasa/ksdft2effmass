# Numerical method

## Representation conversion

The finite parent uses Kronecker lattice translations on `(C^N)^(tensor 3)` and a
four-dimensional orbital factor. A centered unitary tensor Fourier transform must
reproduce the complete direct sum of `4 x 4` Bloch fibers. The retained-frame isometry,
projector lift, inverse transform to `2 x 2` block-circulant Wannier/TB form, and
block/Fourier correlation are independently reconstructed using batched or matrix-free
operations rather than dense `4N^3 x 4N^3` allocation.

Hamiltonian subtraction requires explicit spaces, basis order, frame, gauge, energy
reference, units, and normalization. The full gauge supplies the covariant zero-residual
check; one cell-local global rotation supplies the restricted scientific residual.

## Finite Fourier semantics

Even tensor meshes use centered cyclic representatives
`{-N/2, ..., N/2-1}^3`. Ordinary-lattice conversion removes the union of three Nyquist
boundary planes. The union contains `N^3-(N-1)^3 = 3N^2-3N+1` unique blocks; plane
intersections and the corner are counted once.

## Support

Displacements form complete orbits under the 48-element cubic signed-permutation group;
distinct orbit multiplicity can be smaller when coordinates vanish or repeat. The
canonical representative sorts absolute coordinates in descending order. Orbits are
ordered by squared radius and canonical coordinates. Every attainable shell through the
cap is included, retained whole, and conjugate closed.

## Error and convergence

Parent--retained reconstruction, covariant equivalence, and restricted-alignment
residual remain separate before conversion or truncation. Cyclic conversion,
interpolation, deliberate truncation, and total errors remain separate on a disjoint
3-D mesh. Every field pair has reconstructed-Hamiltonian Frobenius maximum/RMS channels
and separate sorted-band maximum/RMS channels, with pointwise perturbation-bound checks.
Omitted block power is a locality diagnostic. First passing sampled
shells require construction- and evaluation-mesh stability.

The bounded matrix-free development ladder uses `N=8,16,32` and the odd `M=2N+1`
evaluation rule. Larger mesh proposals require renewed resource review. Exact caps, catalog-wide
convergence tolerances, and gap enclosures remain protocol gates, together with existence
of the declared global periodic frame. Wilson
and plaquette phases are sewing diagnostics, not topological claims.
