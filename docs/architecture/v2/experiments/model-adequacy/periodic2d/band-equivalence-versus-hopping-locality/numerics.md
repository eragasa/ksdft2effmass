# Numerical method

## Representation conversion

The finite parent uses Kronecker lattice translations on `(C^N)^(tensor 2)` and a
four-dimensional orbital factor. A centered unitary tensor Fourier transform must
reproduce the complete direct sum of `4 x 4` Bloch fibers. The retained-frame isometry,
projector lift, inverse transform to `2 x 2` block-circulant Wannier/TB form, and
block/Fourier correlation are independently reconstructed. Dense `4N^2 x 4N^2`
allocation is not required.

Hamiltonian subtraction is permitted only after the spaces, basis order, frame, gauge,
energy reference, units, and normalization are explicit. The full gauge supplies the
covariant zero-residual check; one cell-local global rotation supplies the restricted
scientific residual.

## Finite Fourier semantics

Even tensor meshes use centered cyclic representatives
`{-N/2, ..., N/2-1}^2`. Ordinary-lattice conversion removes the union of the two
Nyquist boundary lines, containing `2N-1` unique blocks. Conversion power remains
separate from deliberate truncation.

## Support

Displacements form complete square signed-permutation orbits with canonical
representative `(max(|R_x|,|R_y|), min(|R_x|,|R_y|))`. Orbits are ordered by squared
radius and coordinates. The inventory includes every attainable squared-radius shell
through its cap. Support prefixes retain whole orbits and remain conjugate closed.

## Error channels

The action first keeps parent--retained reconstruction, covariant equivalence, and
restricted-alignment residual separate. It then keeps cyclic conversion, interpolation,
deliberate truncation, and total errors separate on a disjoint mesh. Each field pair has maximum and RMS reconstructed-Hamiltonian Frobenius
errors and separate maximum and RMS sorted-band errors. Pointwise eigenvalue differences
must satisfy the operator/Frobenius perturbation bound. Omitted block power is not a
spectral-error bound. First passing sampled shells must survive construction- and
evaluation-mesh refinement or remain `unresolved`.

Exact meshes, shell caps, tolerances, conservative gap enclosures, and existence of the
declared global periodic frame remain protocol gates. Wilson and plaquette phases are
sewing diagnostics, not topological claims.
