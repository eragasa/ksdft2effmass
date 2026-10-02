# Periodic2d capability-parity gate

## Status and boundary

This record defines the non-defect capability gate that must be completed before
additional periodic2d defect-campaign work. It is an implementation and documentation
map, not a calculated result, scientific validation claim, or authorization to rerun
Wannier90 or another external program.

The canonical software spelling is `periodic2d`. Historical experiment identifiers
and provenance strings are evidence and are not silently rewritten merely to normalize
current package naming.

No new work under `campaigns.periodic2d.defects` or the retained
`impurity-defect-2d` campaign belongs to this gate. Existing defect material remains
unchanged while the parent periodic2d capabilities are brought to parity.

## PhysKit dependency boundary

The current human instruction authorizes periodic2d lattice work to use the reusable
Project Koios PhysKit lattice owners. Before this slice, this branch had no PhysKit
package dependency and the cosine model left its square-cell duality implicit. The
new dependency is `projectkoios-physkit` pinned to revision
`0f17e84d421ebdae5d55d06f807db64d6b408262`. Periodic2d imports
`DirectLattice2D` and `ReciprocalLattice2D` from
`projectkoios.physkit.periodic.lattice`; it does not introduce another campaign-local
direct or reciprocal lattice type.

PhysKit owns the primitive-basis convention. With direct primitive vectors stored as
columns of $A$, it constructs

$$
B = 2\pi A^{-\mathsf T}, \qquad A^{\mathsf T}B=2\pi I.
$$

The retained cosine model fixes $A=2\pi I$ and therefore $B=I$. Its reduced momentum
$\boldsymbol\kappa$ and reciprocal integer pair $\mathbf n$ produce the Cartesian
wave vector $B(\boldsymbol\kappa+\mathbf n)$ and kinetic diagonal
$\lVert B(\boldsymbol\kappa+\mathbf n)\rVert^2$. This recovers the retained scalar
formula without treating reduced coordinates as Cartesian coordinates by accident.
No retained numerical payload or historical provenance identifier changes.

PhysKit also owns `TwistedSupercellOperatorConstructor` for sparse scalar hopping
operators on a `FinitePeriodicDomain` with a declared boundary-twist lift. That
constructor is the required owner for the later real-space parent-operator and hopping
parity slices. It is not interchangeable with a continuum plane-wave constructor:
`TwistedSupercellOperatorConstructor` consumes a finite hopping inventory rather than
Fourier coefficients of a continuum operator.

The pinned PhysKit revision contains `PlaneWaveBlochHamiltonian1D` but no corresponding
two-dimensional owner. By current human instruction, this repository temporarily owns
`PlaneWaveBlochHamiltonian2DConstructor` under
`ksdft2effmass.analysis.model_systems.periodic2d`. It uses PhysKit lattice objects,
the same two-pi dual convention, a finite conjugate-symmetric Fourier inventory, and
explicit represented-space metadata. The periodic2d cosine campaign now adapts its
coefficients into that reusable Action instead of assembling its own plane-wave
matrix. The class is isolated from campaign provenance and acceptance policy so it can
be migrated to PhysKit later without moving ksdft-specific policy.

## Meaning of parity

Parity means equivalent scientific and software coverage where a two-dimensional
analogue is mathematically applicable. It does not require identical source files or
pretend that a one-dimensional scalar phase, a two-dimensional Chern invariant, and a
composite-band Wilson loop are interchangeable.

| Capability | Periodic1d coverage | Current periodic2d coverage | Required periodic2d disposition |
|---|---|---|---|
| Periodic potential model | Typed finite Fourier potential | Typed cosine potential with separable and coupled terms | Retain typed owner; document coefficient and unit conventions |
| Plane-wave representation | Typed basis, sewing, fiber constructor, and represented result | Request exposes `p`-outer, `q`-inner indices and dimension; the model uses PhysKit direct/reciprocal lattices; centered half-open meshes retain wrapped-neighbor translations; explicit nonunitary maps sew both positive reciprocal directions; results retain exact requests | Use these owners in later typed campaign and serialization extraction without conflating mesh wrapping and finite-basis truncation |
| Finite-difference representation | Typed periodic grid and twisted fiber constructor | Request exposes `x`-outer, `y`-inner ordering, spacing, dimension, and Bloch seam phases; result retains the exact request; a typed comparator transports the grid operator into the plane-wave common space and records threshold-free disagreement | Preserve the explicit transport in later campaign extraction and keep discretization error distinct from other error classes |
| Isolated-band campaign | Definition, calculation Workflow, typed results, serialization, correlation, and independent verification | Input, calculation, retained model, correlation, and verification concentrated in `run.isolated` | Split owned records and wire mechanics; preserve retained version-one bytes |
| Stress/adverse controls | Amplitude, shape, mesh/isolation, gauge-covariance, and route-assumption cases | No equivalent campaign | Add dimension-appropriate parent, anisotropy, mesh, gauge, and route controls without using expected trends as verification oracles |
| Composite subspace | Typed isolation, gauge, Wilson, hopping, route, serialization, and verified Workflow results | Rank-three projected-gauge calculation, correlation, and verification | Add typed composite result hierarchy and explicit unavailable-channel reporting |
| Gauge transport and alignment | Scalar transport, composite polar transport, pointwise alignment, and gauge comparisons | Numerical behavior is embedded in campaign calculators and reconstructors | Introduce cohesive typed Actions and Results with explicit overlap and closure preconditions |
| Reciprocal-to-hopping transform | Complete transform, inverse interpolation, truncation, fitting routes, Parseval, and locality diagnostics | Scalar and block transforms appear inside retained campaigns | Introduce reusable complete-transform and separate truncation/fitting result owners |
| Route reconciliation | Transform, complete least-squares, weighted, and incomplete routes remain distinct | Route comparisons are campaign-local | Add typed route identities and comparisons; never pool incompatible errors |
| Wilson and topology diagnostics | Wilson phases for composite groups | Chern, Wilson, and phase-sweep campaigns exist | Preserve as additional 2D coverage; expose gauge-invariant typed results without treating expected topology as an oracle |
| Effective mass | Scalar curvature diagnostics | Two-dimensional curvature tensor appears in retained calculations | Add typed tensor result with declared reciprocal coordinates, energy unit, and finite-difference step |
| Wannier90 boundary | Typed native adapters, preparation, retained observations, and verified Workflows | Balanced, study, and optimizer-basin retained campaigns | Reuse integration-owned native adapters; keep optimizer behavior and campaign policy outside generic periodic owners |
| Serialization | Closed input/result serializers and strict decoding | Repeated campaign-local JSON mechanics | Add shared periodic2d wire mechanics and campaign-owned versioned serializers without generic untyped containers |
| Tests | Class-owned software and numerical evidence across model, campaign, serializer, and verification owners | Strong retained-campaign coverage but limited granular owner coverage | Add class-owned evidence for every new public owner and independent numerical oracles where claims require them |
| Documentation | API, concept, architecture, equations, conventions, evidence limits, and citations | Campaign overview and retained reports exist | Add complete API and concept documentation with direct method references |

The existing periodic2d topology and optimizer studies are additional capabilities.
They do not substitute for the missing stress, typed-result, serialization, alignment,
hopping-transform, or route-comparison coverage.

## Current implementation progress

The first foundation slice now makes the represented-space identity inspectable rather
than leaving it implicit in constructor loops:

- `Periodic2DPlaneWaveBasis` owns reciprocal indices, ordering, cutoff, and represented
  dimension, while PhysKit `DirectLattice2D` and `ReciprocalLattice2D` own primitive
  lattice geometry and the two-pi dual convention;
- `Periodic2DUniformCellGrid` owns site indices, ordering, period, spacing, and
  represented dimension, and finite-difference requests combine that grid with
  positive-direction seam phases;
- the reusable `PlaneWaveBlochHamiltonian2DConstructor` owns the two-dimensional
  Fourier-operator construction pending later PhysKit migration, and the cosine
  campaign delegates its plane-wave matrix to that Action;
- `CenteredUniformReciprocalMesh2D` owns uniform half-open sampling and deterministic
  first-outer, second-inner ordering, while typed neighbor results retain exact integer
  reciprocal translations at positive-direction boundary wraps;
- `PlaneWaveReciprocalSewing2DConstructor` owns the two independent positive primitive
  coefficient shifts and explicitly truncates coefficients leaving the finite basis
  instead of wrapping them;
- representation-specific immutable results retain the exact request and reject matrix
  dimensions incompatible with its basis or grid; the plane-wave result also retains
  the checked maximum direct--reciprocal duality residual;
- `Periodic2DCommonSpaceOperatorComparator` constructs the normalized plane-wave grid
  map, transports the finite-difference operator, and retains the exact difference,
  isometry defect, Frobenius error, and maximum-entry error without assigning an
  acceptance status;
- public numerical inputs reject booleans, strings, and NumPy scalar substitutes rather
  than coercing them; and
- each affected public owner has class-owned software-verification coverage and Sphinx
  API or concept documentation.

The represented-identity, reciprocal-mesh, finite plane-wave sewing, and transported
common-space portions of implementation step 2 are now explicit. Their later use in
versioned campaign serializers remains open, and no stress or defect capability is
activated by these slices.

## Implementation order

1. Freeze the capability and reference inventory in this record.
2. Complete plane-wave, finite-difference, reciprocal-mesh, and represented-result
   contracts.
3. Separate isolated-band definitions, results, serialization, calculation,
   correlation, and verification ownership.
4. Add the periodic2d stress/adverse-control campaign.
5. Complete composite-subspace typed results and gauge/alignment contracts.
6. Complete scalar and block hopping transforms, truncation, fitting routes, Parseval,
   withheld-mesh diagnostics, and route reconciliation.
7. Integrate effective-mass tensors, Wilson loops, Chern diagnostics, and Wannier90
   adapters through those owners.
8. Complete class-owned tests, retained adapters, checksums, API documentation, concept
   documentation, and reference auditing.
9. Run the periodic2d parity gate before any new defect-campaign implementation.

## Documentation acceptance

Every implemented technique must document:

- the physical model, mathematical operator, represented state space, and finite matrix;
- basis ordering, gauge, reciprocal coordinates, energy reference, units, and geometry;
- equations and the numerical approximation actually used;
- input invariants, failure behavior, and output interpretation;
- software verification, numerical verification, scientific validation, and uncertainty
  exclusions separately; and
- direct references attached to the technique they support.

Reference lists use short entries with a DOI or ISBN. Original method papers and
official software papers or manuals are preferred. Reviews may provide context but do
not replace the direct reference for an implemented algorithm.

## Direct technique references

- Bloch, F., “Über die Quantenmechanik der Elektronen in Kristallgittern,” *Z. Phys.* **52**, 555–600 (1929). DOI: `10.1007/BF01339455`.
- Wannier, G. H., “The Structure of Electronic Excitation Levels in Insulating Crystals,” *Phys. Rev.* **52**, 191–197 (1937). DOI: `10.1103/PhysRev.52.191`.
- Luttinger, J. M. and Kohn, W., “Motion of Electrons and Holes in Perturbed Periodic Fields,” *Phys. Rev.* **97**, 869–883 (1955). DOI: `10.1103/PhysRev.97.869`.
- Schönemann, P. H., “A Generalized Solution of the Orthogonal Procrustes Problem,” *Psychometrika* **31**, 1–10 (1966). DOI: `10.1007/BF02289451`.
- Higham, N. J., “Computing the Polar Decomposition—with Applications,” *SIAM J. Sci. Stat. Comput.* **7**, 1160–1174 (1986). DOI: `10.1137/0907079`.
- Chelikowsky, J. R., Troullier, N. and Saad, Y., “Finite-Difference-Pseudopotential Method: Electronic Structure Calculations without a Basis,” *Phys. Rev. Lett.* **72**, 1240–1243 (1994). DOI: `10.1103/PhysRevLett.72.1240`.
- Marzari, N. and Vanderbilt, D., “Maximally Localized Generalized Wannier Functions for Composite Energy Bands,” *Phys. Rev. B* **56**, 12847–12865 (1997). DOI: `10.1103/PhysRevB.56.12847`.
- Souza, I., Marzari, N. and Vanderbilt, D., “Maximally Localized Wannier Functions for Entangled Energy Bands,” *Phys. Rev. B* **65**, 035109 (2001). DOI: `10.1103/PhysRevB.65.035109`.
- Fukui, T., Hatsugai, Y. and Suzuki, H., “Chern Numbers in Discretized Brillouin Zone,” *J. Phys. Soc. Jpn.* **74**, 1674–1677 (2005). DOI: `10.1143/JPSJ.74.1674`.
- Yates, J. R., Wang, X., Vanderbilt, D. and Souza, I., “Spectral and Fermi Surface Properties from Wannier Interpolation,” *Phys. Rev. B* **75**, 195121 (2007). DOI: `10.1103/PhysRevB.75.195121`.
- Brouder, C., Panati, G., Calandra, M., Mourougane, C. and Marzari, N., “Exponential Localization of Wannier Functions in Insulators,” *Phys. Rev. Lett.* **98**, 046402 (2007). DOI: `10.1103/PhysRevLett.98.046402`.
- Mostofi, A. A. et al., “wannier90: A Tool for Obtaining Maximally-Localised Wannier Functions,” *Comput. Phys. Commun.* **178**, 685–699 (2008). DOI: `10.1016/j.cpc.2007.11.016`.
- Slater, J. C. and Koster, G. F., “Simplified LCAO Method for the Periodic Potential Problem,” *Phys. Rev.* **94**, 1498–1524 (1954). DOI: `10.1103/PhysRev.94.1498`.
- Niu, Q., Thouless, D. J. and Wu, Y.-S., “Quantized Hall Conductance as a Topological Invariant,” *Phys. Rev. B* **31**, 3372–3377 (1985). DOI: `10.1103/PhysRevB.31.3372`.
- Soluyanov, A. A. and Vanderbilt, D., “Computing Topological Invariants without Inversion Symmetry,” *Phys. Rev. B* **83**, 235401 (2011). DOI: `10.1103/PhysRevB.83.235401`.

These references support techniques, not retained numerical values or material claims.
Any later reference addition must be checked against the publisher or DOI metadata
before it enters maintained documentation.
