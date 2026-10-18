# Post-sequence general-lattice-vector extension

## Purpose

This topic records the reusable capability considered after the four concrete
isotropic/anisotropic experiments establish stable source contracts.

- Prerequisite: [dimensionality and anisotropy ladder](../../../experiments/model-adequacy/dimensional-anisotropy-ladder.md).
- Target dimensions: intrinsic periodic dimension two and three.
- Target input: caller-supplied full-rank lattice vectors with explicit units and orientation.
- Current status: architecture direction only; no API, module, class, or arbitrary-lattice claim.

## Lattice construction

For periodic dimension `p` and direct-basis matrix `A`, the columns of `A` define the
physical lattice and its Gram matrix.

- Require full column rank.
- Define `G = A^T A`.
- Require `G` to be positive definite under the reviewed rank policy.
- Define the reciprocal dual `B = 2 pi A (A^T A)^(-1)`.
- Verify `B^T A = 2 pi I`.
- Reduce to `B = 2 pi A^(-T)` for a square full-rank three-dimensional basis.

## Fourier coordinates

Reduced-coordinate Fourier algebra remains separate from physical-distance geometry.

- Use integer lattice coordinates `n` in `Z^p`.
- Use reduced reciprocal coordinates `q` with `k = B q`.
- Verify `k . (A n) = 2 pi q . n`.
- Construct Fourier phases from reduced coordinates and integer representatives.
- Compute physical lengths and angles through `G` rather than integer norms.

## Two-dimensional method

The two-dimensional capability must preserve whether the lattice is intrinsic or
embedded in a higher-dimensional ambient space.

- Accept a reviewed full-rank intrinsic `2 x 2` basis.
- Accept a reviewed full-column-rank embedded-plane `3 x 2` basis.
- Preserve the induced metric, plane orientation, projector, and reciprocal dual.
- Reject reinterpretation of an embedded plane as a three-dimensional periodic cell.
- Test square, rectangular, and at least one oblique finite case.

## Three-dimensional method

The three-dimensional capability must preserve a full-rank `3 x 3` direct basis and its
orientation.

- Record determinant sign and volume convention.
- Record rank and conditioning diagnostics.
- Construct reciprocal dual and metric deterministically.
- Test cubic, orthorhombic, and at least one triclinic finite case.
- Reject zero-volume and numerically singular inputs under a frozen policy.

## Symmetry construction

Lattice geometry alone does not establish the symmetry of the represented Hamiltonian.

- Declare each finite integer action `S` in `GL(p,Z)`.
- Verify the metric condition `S^T G S = G` within the declared arithmetic policy.
- Verify that the parent model admits the same action.
- Construct complete deterministic representative orbits.
- Include Hermitian closure under `n -> -n`.
- Do not merge coefficients solely because physical lengths agree.

## Support construction

General lattice vectors do not supply a universal hopping-shell hierarchy.

- Each experiment declares its finite integer representative domain.
- Each experiment declares support nesting and scientific meaning.
- Physical distance is computed from the lattice metric.
- Symmetry multiplicity is computed from the accepted model action.
- Candidate coordinates remain experiment-owned.

## Numerical verification

A finite adversarial case inventory must precede a general-support claim.

- Verify direct/reciprocal duality.
- Verify reduced-phase invariance.
- Verify metric lengths and angles.
- Verify orbit coverage and canonical ordering.
- Test near-singular and orientation-reversing bases.
- Test coordinate permutations and symmetry mismatches.
- Compare specialized square, cubic, rectangular, and orthorhombic routes with the general route.

## Ownership

The capability must reuse existing geometry and numerical owners rather than duplicate
them in KSD.

- PhysKit owns reusable lattice basis, reciprocal dual, metric, embedding, and finite-periodic geometry primitives.
- A reviewed numerical owner may own dimension-bounded Fourier assembly and reconstruction.
- Optimization owns reviewed unit-free fitting and constrained-geometry kernels.
- KSD experiments own scientific symmetry acceptance, support meaning, channels, thresholds, evidence, and interpretation.

## Extraction gate

Source extraction begins when the next concrete experiment identifies owner-neutral
behavior whose semantic owner can define a complete contract. KSD must not implement the
same generic mechanism merely to manufacture a second example.

- Inventory the exact behavior required by the current sequence stage.
- Review existing PhysKit and Numerics contracts before proposing new primitives.
- Select exact rank, condition, unit, orientation, and canonicalization policies.
- Create source module architecture only when a reusable module is selected.
- Extract the smallest complete owner contract before adding a competing KSD implementation; later stages may broaden it.
- Concentrate detailed equations, algorithms, tolerances, failures, and references under the implementing `ClassName`.
- Keep experiment schemas and dispositions local because they own scientific evidence and interpretation, not because repeated implementations are absent.

## References and provenance

The equations above are project-applied finite-lattice coordinate identities; no new
external algorithm implementation is selected by this topic.

- PhysKit revision `7157dcedd0d220673d443c1c025e35a6fd1ffa7a` is the live
  pinned KSD-compatible owner revision for nonorthogonal 2-D/3-D finite-periodic
  lattice primitives. Earlier owner reviews audited this lineage at
  `949d106bc98975a18ad86d6fa84092ef0c68298e` and
  `2cede347e4beeb39f06ca096c15b7a76de276953`; current KSD dependency tests qualify
  the exact consumed surface rather than treating those historical reviews as a
  transferable scientific validation.
- [Periodic-2D package architecture](../../periodic/periodic2d/index.md) records the current embedded-plane and inverse-metric contracts.
- [Periodic-3D package architecture](../../periodic/periodic3d/index.md) records the three-dimensional ownership boundary.
- Future class pages must cite primary sources and exact owner documentation for any adopted decomposition, interval, or lattice-reduction algorithm.

## Interpretation

General lattice-vector support is geometry and numerical capability rather than a
material model.

- It does not define silicon, graphene, or another crystal.
- It does not infer orbital, valley, spin, gauge, or parent-calculation semantics.
- It does not establish completeness over all lattices from a finite test inventory.
- It does not authorize protected computation or scientific validation claims.
