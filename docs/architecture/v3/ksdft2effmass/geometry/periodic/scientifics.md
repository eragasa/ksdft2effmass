# Periodic geometry scientific interpretation

## Geometry is not a represented calculation

A periodic lattice geometry identifies an ordered primitive translation basis and its
physical length convention. It does not identify atoms, orbitals, a Hamiltonian, a
finite supercell, a reciprocal mesh, a numerical basis, a real-space kernel, or a
calculated material property.

An integer lattice displacement is a dimensionless coefficient tuple. A direct-lattice
displacement is the physical length vector obtained after those coefficients act on one
exact direct lattice. The two values are related but not interchangeable.

## Direct and reciprocal lattice displacements

For one declared geometry,

\[
\mathbf R_{\mathbf n}=A\mathbf n
\]

is a `DirectLatticeDisplacement`, while

\[
\mathbf G_{\mathbf m}=B\mathbf m
\]

is a `ReciprocalLatticeDisplacement`. Both use integer coefficients, but they belong to
different physical spaces and have different units. The direct value has length units;
the reciprocal value has inverse-length units.

A reciprocal-lattice displacement represents an integer reciprocal shift. It must not be
used as the name for a general reciprocal-space vector with real basis coefficients.

## Reciprocal coordinates and reciprocal-space vectors

A `ReciprocalLatticeCoordinate` is a dimensionless real coefficient tuple in an ordered
reciprocal primitive basis. A `ReciprocalSpaceVector` is the corresponding physical
inverse-length vector obtained only after correlating those coefficients with one
geometry:

\[
\mathbf k_{\mathbf q}=B\mathbf q.
\]

This neutral geometry value is not named `BlochWavevector`. Bloch terminology begins
only when a separate periodic-state owner correlates the reciprocal-space value with a
fiber, band index, energy, wavefunction, basis, or gauge.

The distinction preserves the difference between:

- reciprocal primitive-basis coefficients;
- physical reciprocal-space components;
- an integer reciprocal-lattice displacement;
- a selected reciprocal-quotient representative;
- a labeled point on a reciprocal path;
- a member of an ordered reciprocal mesh; and
- a periodic-fiber state space attached to that point.

None of those later meanings may be inferred from a bare tuple or physical vector.

## Reciprocal quotient and periodic-state interpretation

Periodic-state theory may identify reciprocal-space vectors modulo reciprocal-lattice
displacements only together with the applicable basis, sewing, and gauge conventions.
The core coordinate value therefore does not silently replace \(\mathbf q\) by a
preferred representative of \(\mathbf q+\mathbb Z^d\).

Representative selection is a distinct operation. A future representative owner must
declare its domain, such as centered half-open or unit half-open, and its endpoint
policy. Reciprocal paths and meshes additionally own point order, labels, weights,
adjacency, and sampling identity.

## Consumer boundaries

`ksdft2effmass.geometry.periodic` owns no real-space kernel term, hopping coefficient,
periodic fiber, eigenstate, energy, or wavefunction.

A real-space-kernel owner may use an integer displacement as a coefficient index and may
request the corresponding direct-lattice displacement when a physical distance is
needed. A periodic-state owner may correlate a reciprocal-lattice coordinate and
reciprocal-space vector with a represented state space. An ordered basis-embedding owner
may correlate intracell retained-state or MLWF centers with the geometry so that a
locality analyzer can derive
\(A(\mathbf n+\mathbf s_\beta-\mathbf s_\alpha)\). Geometry does not own the state
identifiers, center-to-matrix-index correlation, Wannier provenance, coefficient power,
or locality interpretation. Those consumers depend on geometry; geometry does not
depend on them.

## Coordinate recovery is not representative selection

The inverse operation from a physical reciprocal-space vector to reciprocal coordinates
is numerical basis recovery. It uses the geometry already bound to the source vector,
recovers coefficients, reconstructs the physical vector, and reports a residual. It
does not:

- select a reciprocal-quotient representative;
- claim exact equality after floating-point inversion;
- infer a reciprocal path or mesh point;
- establish gauge equivalence;
- verify a periodic sewing relation; or
- establish scientific validity.

A tolerance-bearing verifier may assess numerical consistency. A representative selector
may subsequently apply a declared reciprocal-lattice quotient convention. Those are
peer operations with different scientific meanings.

## Provider and KSD ownership

PhysKit owns reusable numerical lattice primitives, its current `LatticeDisplacement`
integer record, physical quantities, unit conversion, and metric derivation. KSD uses
the scientific term `IntegerLatticeDisplacement` but does not duplicate or alias the
provider class.

KSD values compose PhysKit values without subclassing them. Legacy KSD-local lattice
records may be projected into the new geometry through explicit dimension-owned
migration operations. Such projection does not rewrite retained bytes or transfer
legacy duality and Bravais-verification claims implicitly.

## Excluded claims

Construction of these values establishes software-level dimensional, unit, finiteness,
and correlation invariants only. It does not establish:

- correctness of a crystal structure;
- convergence of a reciprocal mesh;
- correctness of a DFT or Wannier calculation;
- adequacy of a reduced Hamiltonian;
- smoothness or periodicity of a gauge;
- locality of kernel or hopping coefficients; or
- scientific validation against experiment.
