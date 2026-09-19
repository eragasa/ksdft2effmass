# Adversarial review of the initial solid-state implementation

## Scope

This review challenges the initial public `ksdft2effmass.solid_state` records and
actions. It covers dimensional closure, Bravais classification, direct/reciprocal
lattices, finite integer geometry, boundary twists, scalar lattice models, localized
perturbations, and integral lattice operations. It does not review an unimplemented
Hamiltonian constructor or a calculated finite-domain result.

## Findings and dispositions

| Attack | Disposition | Implemented boundary |
|---|---|---|
| A broad solid-state aggregate could duplicate atomic crystal geometry. | Addressed | `DirectLattice*D` and `ReciprocalLattice*D` explicitly represent reduced lattice-model translation coordinates. There is no implicit `PeriodicStructure` adapter. |
| A generic coordinate tuple could admit zero, four, or mixed dimensions. | Addressed | Dimensioned records accept only exact one-, two-, or three-component tuple unions and reject Boolean integers. |
| A supposedly generic indexer could retain hidden 2D axis order. | Addressed | Exact tests cover terminal 1D, 2D, and 3D indices under last-axis-fastest ordering and inverse resolution. |
| Negative periodic coordinates could receive truncating rather than Euclidean quotients. | Addressed | `PeriodicImageResolver` uses positive-extent `divmod`; the retained 3D adverse case checks negative crossings. |
| Twist lifts and quotient representatives could collapse into one value. | Addressed | They are separate DataObjects; reduction returns the representative and integer quotient. |
| Twist meshes could silently become weighted k-point sampling. | Addressed | Boundary twists carry no weights or reciprocal scale, and documentation forbids implicit conversion. |
| `P/C/I/F` alone could omit a Bravais lattice. | Corrected | `BravaisCentering` also includes `R`, which is required for the rhombohedral Bravais lattice. |
| Factored systems and centerings could admit nonexistent combinations. | Addressed | Bravais DataObjects admit exactly 1, 5, and 14 standard combinations; prohibited square C, tetragonal F, and rhombohedral P cases are tested. |
| Base-centered `A/B/C` settings could be mixed without a coordinate convention. | Addressed with explicit limitation | Version one uses canonical `C`; `A` or `B` settings require an explicit transformation before construction. |
| A primitive basis could be mislabeled with conventional-cell centering. | Residual documentation risk | Centering is documented as conventional-cell metadata. No metric classifier currently infers centering from primitive basis vectors. |
| Composing `Lattice*D` could be mistaken for proof of reciprocal duality. | Addressed | Composition validates types only; `LatticeDualityAnalyzer` separately checks $AB^{\mathsf T}=2\pi I$ with an explicit caller tolerance. |
| Duality could compare incompatible length scales numerically. | Addressed | Reciprocal components are converted to the inverse of the direct unit before residual evaluation. |
| Exact nonzero determinants could admit severely ill-conditioned bases. | Residual, intentionally bounded | DataObjects reject exact singularity only. No conditioning threshold is invented; a future caller-toleranced metric/conditioning analyzer requires a separate contract. |
| Lattice system labels could claim metric compatibility without evidence. | Addressed | Bravais records validate allowed labels only. Tolerance-dependent metric classification remains unimplemented and unclaimed. |
| Scalar records could predeclare unsupported multi-orbital behavior through erased arrays. | Addressed | Hopping and localized terms are scalar records with exact real/imaginary components. Multi-orbital, spin, and composite contracts remain deferred. |
| The implementation could silently densify twisted operators. | Not applicable yet | Sparse complex supercell construction is not implemented. It remains blocked on an explicit complex sparse represented-operator boundary. |
| New source could be mistaken for migrated historical calculation identity. | Addressed | Accepted Stage C artifacts and historical implementation identities are unchanged. The new package has only software-verification evidence. |

## Verification evidence

The initial artifact-owned software-verification module contains ten evidence owners.
It checks public exports, dimensional indexing, negative periodic images, twist
reduction and mesh order, scalar model inventories, 3D transformations, dimensional
rejections, all Bravais combinations, direct--reciprocal duality, and dimension-specific
lattice composition.

The non-wheel Python suite passes with 4,845 tests and three externally gated skips.
Strict mypy passes for 248 source files. Focused Ruff, evidence conformance, checkpoint,
Harness, task-state, and projection checks pass. The Sphinx build introduces no new
warnings; it remains nonzero under `-W` because of the three pre-existing missing
research references recorded by project status.

These checks establish software contracts only. They do not establish numerical
verification of a finite Hamiltonian, scientific validity, material relevance,
uncertainty quantification, or execution authority.

## Outcome

**Technical review outcome: NO_BLOCKING_FINDINGS_FOR_THE_INITIAL_RECORD_SLICE.**

Before twisted-supercell construction, the next design must resolve an immutable
complex sparse represented-operator contract without weakening existing real sparse
quantities or densifying pre-diagonalization operators. Before Bravais metric
classification, it must define conventional-cell settings, metric invariants, and
caller-owned tolerances explicitly.
