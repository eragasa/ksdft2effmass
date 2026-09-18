# Claim-to-source applicability matrix

This matrix records what each methodological precedent can and cannot support.
Access labels and source identities are defined in `source-register.md`.
“Benchmark mismatch” is not a criticism of the source; it prevents importing a
result into a different operator, state space, scaling regime, or finite-volume
problem.

## Finite-rank and weak-binding sources

### KS54 — Koster and Slater (1954) — abstract-level support

- **Operator class:** impurity-modified crystal difference equation expressed
  through Wannier-function coefficients.
- **Dimension:** crystalline setting; no dimension-specific theorem is assigned
  from the available abstract.
- **Scaling parameter:** none used in the retained claim.
- **State-space identification:** host and impurity amplitudes are represented in
  a Wannier/LCAO description.
- **Spectral regime:** impurity levels relative to host bands.
- **Defect assumptions:** a crystal Hamiltonian changed by an impurity.
- **Finite-volume assumptions:** not assigned from abstract-level access.
- **Supported conclusion:** host Green-function/difference-equation methods are a
  classical precedent for resolving impurity levels in a localized basis.
- **Benchmark mismatch:** the source does not support this project's exact
  finite-supercell rank-one secular equation, numerical tolerances, alignment
  protocol, or independent implementation. Detailed formula attribution is
  withheld because full text was not lawfully inspected.

### S76 — Simon (1976) — full text

- **Operator class:** continuum Schrödinger operators of the form
  $-\Delta+\lambda V$.
- **Dimension:** one and two spatial dimensions.
- **Scaling parameter:** weak coupling $\lambda\downarrow0$.
- **State-space identification:** a fixed $L^2(\mathbb R^d)$ space; no changing
  lattice/continuum identification.
- **Spectral regime:** eigenvalues below the continuum threshold.
- **Defect assumptions:** integrability and sign/moment hypotheses on $V$ that
  differ by dimension.
- **Finite-volume assumptions:** infinite domain.
- **Supported conclusion:** weak attractive perturbations in one and two
  dimensions have dimension-specific bound-state existence and threshold
  asymptotics.
- **Benchmark mismatch:** the analytical-oracle exercise uses a finite periodic
  two-orbital lattice and a rank-one represented defect; its finite-size roots
  are not Simon's continuum weak-coupling asymptotics.

### P10 — Parzygnat, Lee, Avniel, and Johnson (2010) — full text

- **Operator class:** periodic continuum Schrödinger operator plus a localized
  multiplication defect.
- **Dimension:** one- and two-dimensional localization, including localization
  in selected directions of higher-dimensional periodic systems.
- **Scaling parameter:** arbitrarily weak defect strength under sufficient sign
  and depth conditions.
- **State-space identification:** one continuum periodic operator and its
  defect-perturbed counterpart on a common space.
- **Spectral regime:** below the ground-state edge and inside spectral gaps;
  degenerate edge sectors are treated through finite matrices.
- **Defect assumptions:** sufficiently localized, mostly negative or mostly
  positive defect with conditions tied to the relevant Bloch edge and gap.
- **Finite-volume assumptions:** infinite periodic medium, not a finite
  supercell sequence.
- **Supported conclusion:** sufficient conditions exist for weak-defect
  localization in low-dimensional periodic media and for multiple states at
  degenerate edges.
- **Benchmark mismatch:** this is an existence result, not an alignment,
  operator-extraction, route-commutativity, or finite-volume error analysis.

## Band-edge and continuum-limit sources

### HW11 — Hoefer and Weinstein (2011) — full text

- **Operator class:**
  $H_\varepsilon=-\Delta+V(x)+\varepsilon^2Q(\varepsilon x)$ with periodic
  $V$ and localized $Q$.
- **Dimension:** $d\geq1$ under stated hypotheses.
- **Scaling parameter:** $\varepsilon\downarrow0$, jointly weakening and
  widening the defect.
- **State-space identification:** continuum Floquet--Bloch decomposition and a
  multiscale identification with a homogenized envelope operator.
- **Spectral regime:** discrete eigenvalues bifurcating from a periodic band edge
  into a gap.
- **Defect assumptions:** localized, slowly varying scaled defect and a suitable
  band edge/effective-mass structure.
- **Finite-volume assumptions:** infinite domain.
- **Supported conclusion:** the bifurcating eigenvalue and mode are governed to
  controlled order by a homogenized effective-mass operator.
- **Benchmark mismatch:** profile broadening at fixed lattice spacing and the
  benchmark's represented-lattice scaling are not automatically the
  $\varepsilon^2Q(\varepsilon x)$ limit.

### DVW15 — Duchêne, Vukićević, and Weinstein (2015) — full text

- **Operator class:** one-dimensional periodic continuum Schrödinger operator
  plus $\lambda V(x)$.
- **Dimension:** one.
- **Scaling parameter:** weak localized defect strength $\lambda\downarrow0$;
  the envelope length grows as the defect eigenvalue approaches a band edge.
- **State-space identification:** Gelfand--Bloch transform and
  Lyapunov--Schmidt reduction from the periodic operator to a near-edge
  envelope equation.
- **Spectral regime:** discrete modes emerging into gaps from nondegenerate band
  edges.
- **Defect assumptions:** localized weak defect with a sign condition involving
  the edge Bloch mode and curvature.
- **Finite-volume assumptions:** infinite domain.
- **Supported conclusion:** near-edge defect modes have a Bloch-carrier times
  homogenized-envelope structure with controlled eigenvalue/eigenfunction
  approximations.
- **Benchmark mismatch:** the synthetic continuum study freezes a represented
  finite operator and tests numerical criteria; it does not verify this
  weak-coupling theorem's hypotheses or asymptotic expansion.

### NT21 — Nakamura and Tadano (2021) — full text

- **Operator class:** standard discrete Schrödinger operators on $h\mathbb Z^d$
  and a continuum Schrödinger operator on $L^2(\mathbb R^d)$.
- **Dimension:** $d\geq1$ for the square-lattice construction.
- **Scaling parameter:** lattice mesh $h\downarrow0$.
- **State-space identification:** explicit sampling/synthesis maps $P_h$ and
  $P_h^*$ satisfying Fourier-support and orthonormality conditions.
- **Spectral regime:** norm-resolvent convergence, with consequences for
  spectral projections and spectra away from boundaries.
- **Defect assumptions:** real potential satisfying the paper's continuity,
  lower-bound, and relative-variation hypotheses.
- **Finite-volume assumptions:** infinite discrete and continuum spaces.
- **Supported conclusion:** after explicit identification, the discrete
  resolvents converge in norm to the continuum resolvent under the stated
  assumptions.
- **Benchmark mismatch:** the represented two-orbital band parent, finite
  periodic box, scaled dispersion, and defect family are not the paper's
  nearest-neighbor square-lattice operator. The bounded numerical pass is not a
  norm-resolvent theorem.

### KLH11 — König, Lee, and Hammer (2011) — full text

- **Operator class:** continuum few-body Schrödinger bound states with
  finite-range interactions in a periodic cubic box.
- **Dimension:** three spatial dimensions, with angular-momentum sectors.
- **Scaling parameter:** box length $L\to\infty$ relative to interaction range
  and inverse binding momentum.
- **State-space identification:** finite periodic-box states compared with the
  infinite-volume bound state through image overlaps.
- **Spectral regime:** isolated bound-state energy shifts.
- **Defect assumptions:** finite-range interaction and an asymptotic bound-state
  tail; the derivation is not a crystalline impurity theorem.
- **Finite-volume assumptions:** cubic periodic volume; leading corrections are
  exponentially small in the binding momentum times $L$ and depend on angular
  momentum.
- **Supported conclusion:** periodic images shift bound-state energies in a
  structured, asymptotically exponential way.
- **Benchmark mismatch:** the one-dimensional multiorbital lattice and its
  defect-derived bands do not inherit the paper's coefficients, angular
  dependence, or correction formula. The source motivates separate image
  diagnostics only.

## Semiconductor effective-mass sources

### KL55 — Kohn and Luttinger (1955) — browser-rendered full-text inspection

- **Operator class:** multivalley effective-mass description of substitutional
  donor states in silicon.
- **Dimension:** three-dimensional silicon.
- **Scaling parameter:** separation between a slowly varying donor envelope and
  lattice-periodic Bloch structure; no project-specific refinement sequence is
  inferred.
- **State-space identification:** donor states are expanded through conduction
  valleys and their Bloch factors with coupled envelopes.
- **Spectral regime:** shallow donor bound states near conduction-band minima.
- **Defect assumptions:** substitutional donor in silicon within the stated
  effective-mass and impurity-potential approximations.
- **Finite-volume assumptions:** isolated-donor theory rather than a periodic
  supercell convergence study.
- **Supported conclusion:** silicon donor theory is intrinsically multivalley;
  a scalar one-valley envelope is not the complete classical model.
- **Benchmark mismatch:** the source does not justify the synthetic one-
  dimensional parent, a Wannier Hamiltonian subtraction, a material crossover,
  or the benchmark's operator criteria.

### G15 — Gamble et al. (2015) — full text

- **Operator class:** coupled six-valley Shindo--Nara effective-mass equations
  with silicon Bloch functions and a fitted donor central-cell correction.
- **Dimension:** three-dimensional silicon.
- **Scaling parameter:** variational envelope basis/refinement and donor-pair
  separation, not a lattice-spacing continuum limit.
- **State-space identification:** multivalley envelope functions mapped through
  full Bloch factors; comparisons are made with atomistic tight binding.
- **Spectral regime:** phosphorus donor energies, wavefunctions, and donor-pair
  tunnel coupling.
- **Defect assumptions:** a model central-cell correction is required; the work
  finds a tetrahedral correction necessary for the targeted spectrum.
- **Finite-volume assumptions:** donor calculations and pair placements, not the
  benchmark's periodic-image sequence.
- **Supported conclusion:** multivalley structure and atomically sensitive
  central-cell physics materially affect silicon-donor observables; effective
  mass theory can agree with atomistic calculations when these ingredients are
  treated explicitly.
- **Benchmark mismatch:** agreement in that calibrated model does not validate a
  first-principles impurity operator, prove a general continuum crossover, or
  select this project's model class.

## Wannier defect-operator and finite-size sources

### BVK11 — Berlijn, Volja, and Ku (2011) — full text

- **Operator class:** configuration-dependent Wannier effective Hamiltonian
  expanded in one- and higher-impurity contributions extracted from pristine
  and impurity supercells.
- **Dimension:** material-specific three-dimensional electronic structure with
  a layered host.
- **Scaling parameter:** impurity concentration/configuration and supercell
  partitioning; no continuum scale.
- **State-space identification:** the normal-cell and supercell Hamiltonians
  must be represented in the same Wannier basis; projected Wannier functions
  are used to promote consistency.
- **Spectral regime:** configuration-averaged spectral functions and disorder
  broadening.
- **Defect assumptions:** impurity contributions can be partitioned from their
  periodic images and truncated to low-order cluster effects for the use case.
- **Finite-volume assumptions:** impurity effects are extracted in supercells
  and embedded in larger configurations; artificial supercell boundaries are
  explicitly relevant.
- **Supported conclusion:** localized-basis Hamiltonian differences and
  supercell-to-large-system embedding are established tools for disorder
  modeling, and a common Wannier basis is a prerequisite.
- **Benchmark mismatch:** the objective is disorder averaging, not blind map
  identifiability, fail-closed compatibility, model-class adequacy, or
  continuum crossover.

### CM11 — Corsetti and Mostofi (2011) — full text

- **Operator class:** plane-wave DFT supercells for charged and neutral silicon
  vacancies, with localized Wannier functions used for potential alignment and
  bonding analysis.
- **Dimension:** three-dimensional silicon.
- **Scaling parameter:** supercell size/geometry and Brillouin-zone sampling.
- **State-space identification:** bulk-like localized Wannier onsite elements in
  defect and bulk supercells are matched to estimate the scalar potential
  offset.
- **Spectral regime:** formation energies, charge-transition levels, defect
  levels, and bonding.
- **Defect assumptions:** silicon vacancy charge states with periodic boundary
  conditions and relaxed structures.
- **Finite-volume assumptions:** elastic, electrostatic, orthogonality, and
  image effects vary with supercell size and sampling.
- **Supported conclusion:** energy-reference alignment and system-size/sampling
  convergence are distinct requirements in defect supercells; MLWF onsite
  elements can provide a localized alignment probe when equivalent functions
  can be matched.
- **Benchmark mismatch:** the source does not infer a full unitary map or define
  the benchmark's operator-, route-, and projector-level stopping rules.

### LP19 — Lihm and Park (2019) — full text

- **Operator class:** independently generated MLWF tight-binding models that
  share an overlapping region and are stitched into a larger model.
- **Dimension:** demonstrated for three-dimensional surface systems; the method
  is formulated for localized tight-binding models.
- **Scaling parameter:** overlap-region/model thickness and iterative correction
  convergence, not a physical continuum limit.
- **State-space identification:** orbital pairing/permutation, spin-axis
  rotation, phase correction, potential alignment, or a unitary correction
  obtained by minimizing overlapping Hamiltonian-element differences.
- **Spectral regime:** boundary/interface artifacts and stitched-model bands.
- **Defect assumptions:** common-region atomic structures and corresponding
  localized orbitals must be sufficiently similar for stitching.
- **Finite-volume assumptions:** the overlap region must be bulk-like and
  hopping truncation must support the principal-layer construction.
- **Supported conclusion:** independently generated Wannier models are not
  automatically in a common basis; orbital, spin, phase, and energy alignment
  are operational requirements, and Hamiltonian matching is a practical
  correction route.
- **Benchmark mismatch:** this is not a blind-identifiability theorem, does not
  supply the benchmark's anchor conditioning/principal-angle thresholds, and
  does not prove uniqueness outside the observed overlap.

### LPZB20 — Lu, Park, Zhou, and Bernardi (2020) — full text

- **Operator class:** electron--defect perturbation-potential matrix elements
  transformed between Bloch and Wannier representations by a generalized
  double Fourier transform.
- **Dimension:** demonstrated for three-dimensional silicon and copper.
- **Scaling parameter:** coarse/fine Brillouin-zone grids and spatial truncation
  of neutral-defect matrix elements.
- **State-space identification:** primitive-cell Bloch states and MLWFs are
  connected by explicit unitary matrices; the defect perturbation is obtained
  from pristine/defect Kohn--Sham potentials with a scalar potential alignment.
- **Spectral regime:** elastic defect scattering, relaxation times, mobility,
  and resistivity.
- **Defect assumptions:** neutral vacancies in the demonstrated calculations;
  rapid Wannier-space decay is used for interpolation.
- **Finite-volume assumptions:** a defect supercell supplies the perturbation;
  the coarse grid fixes a Wigner--Seitz range, and convergence is checked
  against direct matrix elements.
- **Supported conclusion:** first-principles defect-potential differences,
  energy alignment, and localized-basis interpolation are established for
  electron--defect scattering.
- **Benchmark mismatch:** the goal is scattering interpolation rather than a
  bound-state model hierarchy, hidden clean/defect gauge inference, or
  independent subtraction-route commutativity.

### KM26 — Kang and Muechler (2026) — full-text preprint

- **Operator class:** host Wannier tight-binding supercell modified by onsite
  parameters taken from a small relaxed defect-like unit cell; hoppings are
  left unchanged in the present protocol.
- **Dimension:** demonstrated for two- and three-dimensional materials.
- **Scaling parameter:** supercell replication and candidate-defect screening;
  no continuum limit.
- **State-space identification:** corresponding localized orbitals and the
  substitution site are assumed/matched across host and defect-like unit-cell
  models.
- **Spectral regime:** number, degeneracy, and shallow/deep character of in-gap
  states.
- **Defect assumptions:** rapid qualitative prescreening for substitutional
  defects under an onsite-only approximation.
- **Finite-volume assumptions:** a replicated host supercell approximates the
  isolated defect; the paper does not replace full supercell validation.
- **Supported conclusion:** an onsite-only localized model can be useful as a
  screening class and has explicit failure domains involving vacancies,
  charge redistribution, and spin polarization.
- **Benchmark mismatch:** the preprint does not extract the full aligned defect
  operator or test whether nonlocal hopping, spin, route, or continuum
  residuals invalidate the onsite class. It is contemporary context, not an
  established historical precedent.

### SXT26 — Shi et al. (2026) — full-text preprint

- **Operator class:** clean and defect DFT/Wannier Hamiltonians embedded as a
  defect patch in a finite-box projected Bogoliubov--de Gennes calculation.
- **Dimension:** two-dimensional iron-chalcogenide defect/vortex models.
- **Scaling parameter:** finite-box size, projected energy cutoff, and
  defect--vortex separation; no semiconductor continuum limit.
- **State-space identification:** Hungarian site/orbital assignment followed by
  a dense unitary Procrustes alignment; the same fixed rotation is applied to
  all defect positions. A PAW-derived cross-overlap and generalized metric are
  retained because the clean and defect basis sets are not mutually
  orthonormal.
- **Spectral regime:** superconducting vortex-core spectra and finite-box
  pinning free-energy differences.
- **Defect assumptions:** point-defect patches in FeSe/FeTe with a clean
  exterior, calibrated superconducting background, and residual boundary
  mismatch checked a posteriori.
- **Finite-volume assumptions:** a four-configuration subtraction is used to
  cancel common finite-box backgrounds; a buffered reference remains inside
  the same box.
- **Supported conclusion:** explicit assignment, unitary alignment, nontrivial
  overlap metrics, and residual boundary diagnostics are independently used in
  a recent first-principles clean/defect Wannier workflow.
- **Benchmark mismatch:** this recent preprint addresses superconducting vortex
  pinning, not semiconductor effective-mass reduction. It does not establish
  the benchmark's blind-map identifiability, undercomplete-sector gauge
  freedom, structured stops, independent real/fiber route comparison, or
  continuum criteria. Its preprint status prevents treating it as peer-reviewed
  validation.

## Matrix-level conclusion

No checked source combines all of the benchmark's represented-space
compatibility audit, withheld-map recovery, undercomplete identifiability,
energy-reference inference, model-class residual hierarchy, independent
real/fiber route commutativity, finite-rank resolvent oracle, finite-volume
ledger, and separated continuum-refinement axes. That bounded observation
supports describing the exercise as an integrated diagnostic synthesis. It does
not establish that no such combination exists outside the declared search, and
it does not support priority or novelty in any individual component.
