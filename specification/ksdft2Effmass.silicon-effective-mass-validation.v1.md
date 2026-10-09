# Silicon effective-mass validation specification v1

Task: `ksdft2Effmass.computational.02.02.02`

Artifact: `SiliconEffectiveMassValidationSpecification-v1`

Status: **protocol frozen; no effective-mass result accepted**

Scope: the scalar-relativistic, non-spin-polarized, non-SOC pristine-silicon bulk
pilot frozen by
[`PhysicalSpecification-v1`](ksdft2Effmass.physical-specification.v1.md) and
[`NumericalSpecification-v1`](ksdft2Effmass.numerical-specification.v1.md).

This specification defines the evidence required to report longitudinal and
transverse conduction-electron effective masses relative to the selected PBE
Kohn–Sham parent. It does not authorize a Quantum ESPRESSO or Wannier90 execution,
select final numerical settings, report a calculated mass, validate agreement with
experiment, or extend the accepted observable set to physical valence-hole masses.

## Authority and claim boundary

The physical specification owns the parent model: diamond silicon, PBE, the selected
PseudoDojo PBE standard-table ONCV silicon pseudopotential, the PBE-relaxed production
lattice constant, and the scalar-relativistic non-SOC bulk-pilot branch. The numerical
specification owns the candidate refinement protocols and the frozen downstream
stability tolerances.

This specification owns:

- identification of the conduction-valley observable;
- the Cartesian Hessian and inverse-mass conventions;
- separation of parent, interpolation, reduction, and local-derivative evidence;
- training and withheld-validation boundaries;
- acceptance logic for an effective-mass result; and
- the minimum retained record needed to reconstruct the claim.

It does not alter pseudopotentials, exchange–correlation approximations, crystal
geometry, cutoffs, meshes, Wannier windows, projections, or tolerances. Any such
change follows the authority and protected-action rules of the owning specification
and calculation task.

Passing this protocol establishes a numerically stable result for the selected
Kohn–Sham parent. It does not establish exact quasiparticle or experimental silicon
masses. Comparison with experiment or higher-level theory is external validation and
must retain parent-model discrepancy separately.

## Accepted observable and deferred observables

### Immediate accepted target

The v1 bulk-pilot target is the nondegenerate conduction minimum on each explicitly
identified silicon $\Delta$-valley branch. The accepted observables are:

1. the Cartesian reciprocal coordinate $\mathbf{k}_\nu$ of the local minimum;
2. the Cartesian energy Hessian at that minimum;
3. the longitudinal electron effective mass;
4. the two transverse principal electron effective masses before any symmetry-based
   averaging; and
5. the transverse-plane splitting and axis-alignment defects used to test the expected
   valley symmetry.

The six-valley relationship is a physical symmetry statement that must be represented
by explicit reciprocal coordinates and maps. A shared label, filename, spectrum,
dimension, or apparent degeneracy is not sufficient to identify equivalent valleys.

### Valence and spin–orbit boundary

The scalar-relativistic non-SOC $\Gamma$ valence manifold may be retained as a
method-development multiband calculation. A degenerate manifold is described by its
projected matrix-valued quadratic tensor, not by independently differentiated scalar
bands through the degeneracy.

Physical heavy-hole, light-hole, split-off, acceptor, or spin–orbit-coupled valence
claims are outside this v1 observable set. They require a separately accepted fully
relativistic spinor/SOC bulk branch compatible with the final B:Si parent defined by
the physical specification. The non-SOC electron pilot is not blocked by that later
branch.

## State spaces and comparison routes

Every mass record must name the state space and route that produced it.

### Parent Kohn–Sham route

The primary reference is the selected parent Kohn–Sham conduction band evaluated from
direct Quantum ESPRESSO results around an identified valley. The band must be
nondegenerate and isolated throughout the declared local neighborhood. Pointwise
energy order alone is not a band-tracking rule; continuity must be established by an
explicit state-overlap, projector, symmetry, or other reviewed identity witness.

### Wannier interpolation route

A Wannier-interpolated result is a distinct represented-operator route. It may be
compared with the parent only after source identity, retained frame, energy reference,
reciprocal coordinates, and target subspace are correlated. Its training mesh and
withheld direct-DFT validation points must be distinct.

### Reduced-model route

A tight-binding or other reduced model is a further route. Its mass discrepancy is a
model-reduction error only after the parent and any intervening Wannier representation
have separately passed their own numerical and interpolation gates. A matching matrix
dimension or spectrum does not establish state-space identity.

No discrepancy may be silently reassigned between these routes.

## Reciprocal and mass conventions

Let $\mathbf{k}$ be a Cartesian reciprocal wavevector with physical inverse-length
units. Reduced crystal coordinates may be retained as source coordinates, but every
derivative record must include the declared direct and reciprocal lattice bases and
the exact map to Cartesian coordinates.

For a nondegenerate band $E_\nu(\mathbf{k})$ with a local minimum at
$\mathbf{k}_\nu$, define

$$
\mathbf{g}_\nu
=
\left.\nabla_{\mathbf{k}}E_\nu(\mathbf{k})\right|_{\mathbf{k}_\nu},
\qquad
\mathbf{K}_\nu
=
\left.\nabla_{\mathbf{k}}\nabla_{\mathbf{k}}E_\nu(\mathbf{k})
\right|_{\mathbf{k}_\nu}.
$$

The inverse effective-mass tensor is

$$
\mathbf{M}_\nu^{-1}=\frac{1}{\hbar^2}\mathbf{K}_\nu.
$$

The value and authority of $\hbar$ and every unit-conversion factor are
provenance-bearing inputs. If $E$ is represented in energy units and $\mathbf{k}$ in
inverse-length units, then $\mathbf{K}_\nu$ has energy-times-length-squared units.
Accepted masses must be retained in a physical mass unit and as a dimensionless ratio
to the explicitly identified electron rest mass $m_e$; the value and authority of
$m_e$ are retained inputs rather than implicit library defaults. Public numeric APIs
must not accept booleans or numeric strings as mass, energy, coordinate, or tolerance
values.

Let $\widehat{\mathbf{e}}_{\parallel,\nu}$ be the explicitly declared unit Cartesian
valley axis and let $\mathbf{P}_{\perp,\nu}=\mathbf{I}-
\widehat{\mathbf{e}}_{\parallel,\nu}
\widehat{\mathbf{e}}_{\parallel,\nu}^{\mathsf T}$. The longitudinal inverse mass is

$$
m_{\parallel,\nu}^{-1}
=
\widehat{\mathbf{e}}_{\parallel,\nu}^{\mathsf T}
\mathbf{M}_\nu^{-1}
\widehat{\mathbf{e}}_{\parallel,\nu}.
$$

The two transverse inverse masses are the two nonzero principal values of
$\mathbf{P}_{\perp,\nu}\mathbf{M}_\nu^{-1}\mathbf{P}_{\perp,\nu}$ restricted to the
transverse plane. Both values must be retained before an optional symmetry average.
The record must also retain the longitudinal–transverse coupling norm, the difference
between the two transverse values, and the angle between the Hessian principal axis
and the declared valley axis.

A conduction minimum requires a stationary point and a positive-definite Cartesian
Hessian within the declared numerical resolution. A negative or unresolved principal
curvature is a failed or inconclusive minimum assessment, not an electron mass.

## Valley-location protocol

For every explicitly listed valley:

1. Use an accepted SCF density from the frozen parent branch.
2. Use a declared coarse path or reciprocal neighborhood only to bracket a candidate
   minimum.
3. Refine the candidate using direct local NSCF samples in a declared Cartesian
   neighborhood.
4. Keep the valley-location sample set separate from the final withheld validation
   points.
5. Record the minimization or fitting model, polynomial order when applicable,
   included and excluded points, coordinate scaling, residuals, and conditioning.
6. Check the full Cartesian gradient at the reported point; a one-dimensional line
   minimum alone does not establish a three-dimensional stationary point.
7. Check that the target state remains nondegenerate and identity-tracked throughout
   the accepted neighborhood.
8. Repeat with at least one refined neighborhood or smaller stencil.

The valley-position acceptance tolerance is the `0.002` fractional-path-coordinate
stability rule frozen by `NumericalSpecification-v1`. Cartesian residual and
conditioning diagnostics must also be reported; passing the fractional-coordinate
rule does not excuse a nonstationary or ill-conditioned fit.

## Effective-mass extraction protocol

The primary mass extraction must use direct parent eigenvalues in a local Cartesian
sampling design that determines all independent Hessian components. A symmetry line
alone is insufficient for the full tensor.

The retained extraction record must include:

- the exact center and offsets in reduced and Cartesian coordinates;
- the stencil or fit family and polynomial order;
- the local radius or radii;
- energy and coordinate units;
- band-identity witnesses;
- the design-matrix singular values or an equivalent conditioning diagnostic;
- fitted gradient, Hessian, residuals, and covariance or resampling information where
  defined;
- ordered Hessian and inverse-mass principal values and axes; and
- the result from at least one smaller-radius or finer local sampling design.

Analytic derivatives from a represented operator may be used as an independent route,
but they do not replace the direct-parent extraction gate. Centered finite differences
or an independently constructed local fit must check derivative signs, Cartesian
transformations, $\hbar^2$ factors, and units.

The longitudinal and transverse masses must each change by no more than `0.5%` under
the accepted refinement and guard comparison, as frozen by
`NumericalSpecification-v1`. The inverse-mass tensor comparison should also report

$$
\varepsilon_{M^*}
=
\frac{\left\|\mathbf{M}_{\mathrm{candidate}}^{-1}
-\mathbf{M}_{\mathrm{reference}}^{-1}\right\|_{\mathrm F}}
{\left\|\mathbf{M}_{\mathrm{reference}}^{-1}\right\|_{\mathrm F}}.
$$

The scalar `0.5%` rules remain the acceptance criteria for the v1 longitudinal and
transverse observables. The tensor error, principal-axis changes, residuals, and
conditioning are retained diagnostics and can make an otherwise scalar-passing result
inconclusive if they expose band mixing, a nonstationary point, or an unstable fit.

## Convergence and error separation

### Parent-model discrepancy

Exchange–correlation approximation, pseudopotential family, relativistic treatment,
and crystal structure define the parent physical model. Differences produced by
changing them are parent-model discrepancies, not numerical convergence errors. They
must not be combined with the numerical error budget without a separately defined
model-uncertainty construction.

### Parent numerical/discretization evidence

The parent gate consumes the accepted cutoff, charge-density cutoff, SCF mesh,
lattice, eigensolver, and tolerance records owned by Stage 02. At minimum, the mass
campaign must compare the accepted candidate with the next-higher retained guard for
the indirect gap, valley location, longitudinal mass, transverse masses, and withheld
band energies. One-variable-at-a-time tables and any required cutoff–mesh interaction
check remain separate evidence.

Finite-setting stability demonstrates only stability over the tested settings. It is
not an infinite-basis error bound unless an explicit asymptotic argument is supplied.

### Local sampling and derivative evidence

Valley-location uncertainty, stencil-radius sensitivity, fit residuals, conditioning,
and derivative-route disagreement form the local extraction error record. Pointwise
energy tolerances alone are insufficient because second derivatives amplify energy
errors by an inverse squared length scale.

### Wannier interpolation evidence

For each withheld parent point in the accepted local valley neighborhood, retain:

- parent and Wannier energies in a correlated state space;
- energy residuals;
- state/projector identity diagnostics;
- valley-coordinate discrepancy;
- Cartesian Hessian and inverse-mass-tensor discrepancy; and
- dependence on the uniform Wannier mesh.

The frozen `1 meV` withheld-energy rule applies to numerical changes at fixed
withheld points; it is not automatically a parent-to-Wannier accuracy threshold. The
longitudinal and transverse Wannier masses must satisfy the frozen `0.5%`
relative-change rule under Wannier-mesh refinement. Separate parent-to-Wannier energy
and mass accuracy thresholds must be declared before window, projection, or mesh
selection; numerical-convergence tolerances must not be silently repurposed as
route-accuracy thresholds.

### Model-reduction evidence

For each declared reduced model, retain its band, valley, Hessian, inverse-mass, and
principal-axis discrepancies relative to the accepted upstream reference. Rank,
windows, projections, truncation, and fitting changes are model-reduction axes and
must not be reported as parent DFT convergence.

### Error budget

The final record must report, without automatic aggregation:

1. parent-model discrepancy or declared unassessed parent-model limitation;
2. parent numerical/discretization stability;
3. valley-location and local derivative-extraction sensitivity;
4. Wannier interpolation discrepancy, when that route is used;
5. reduced-model discrepancy, when that route is used; and
6. external-validation discrepancy, when literature, experiment, or another method is
   compared.

A combined uncertainty may be reported only when its statistical or deterministic
combination rule and assumptions are explicitly defined. Otherwise the components
remain separate bounds, sensitivities, or discrepancies.

## Training and withheld validation sets

Every fitted or localized representation must declare its training set before results
are evaluated. Withheld validation points must not be used to choose windows,
projections, fit order, fitting weights, local radius, or model parameters.

A validation point may test more than one route only when its source identity and
state-space correspondence are explicit. Reusing a training point under another
filename does not create independent validation evidence.

The final record must include complete ordered manifests for both sets and state any
symmetry expansion applied to either set.

## Required retained artifacts

The `Bulk validation record` produced by `02.02.02` must contain or bind:

- the accepted physical and numerical specification versions;
- exact executable, pseudopotential, input, parent-state, environment, and software
  identities;
- explicit valley coordinates, axes, and symmetry maps;
- ordered training, fit, guard, and withheld-validation manifests;
- parent eigenvalues and state-identity observations used for location and curvature;
- fit/stencil definitions, conditioning, residuals, gradients, Hessians, masses, and
  unit conversions;
- all accepted and rejected convergence points;
- separate parent, derivative, interpolation, reduction, and external-comparison
  diagnostics;
- machine-readable acceptance results for every frozen tolerance;
- retained stdout and compact native-output bindings; and
- an explicit limitations and claim-status statement.

Large wavefunction, charge-density, restart, scratch, and dense-matrix data remain
external. Their authoritative manifests, software versions, compact inputs, and
necessary checksums must be retained.

## Concrete software record boundary

The first software implementation should use concrete immutable domain records rather
than a generic campaign engine. The intended responsibilities are:

- `SiliconConductionValleyTarget`: explicit valley identity, coordinate branch,
  Cartesian longitudinal axis, parent-model identity, and band-identity contract;
- `SiliconEffectiveMassSamplingDesign`: ordered Cartesian offsets, training/withheld
  roles, fit family, order, radius, and units;
- `SiliconEffectiveMassConvergencePoint`: one fully identified numerical setting and
  its valley, Hessian, and mass observations;
- `SiliconEffectiveMassConvergenceSeries`: one controlled convergence axis with
  ordered points and a declared guard;
- `SiliconEffectiveMassErrorBudget`: separate parent, derivative, interpolation,
  reduction, and external-comparison components; and
- `SiliconEffectiveMassAcceptanceAssessment`: the explicit frozen-tolerance outcomes
  and bounded claim status.

Reusable nondegenerate Cartesian Hessian and tensor-to-mass mathematics may belong to
`ksdft2effmass.solid_state` after the inexpensive demonstrations below. Campaign
identity, manifests, convergence-axis policy, and acceptance decisions remain owned by
`ksdft2effmass` and must not move into calculator or provider integrations.

## Inexpensive demonstrations required before production extraction

Before accepting production effective-mass software, demonstrate:

1. a one-dimensional analytic band with a known scalar curvature and mass;
2. a two-dimensional anisotropic valley rotated relative to the coordinate axes, with
   known principal masses and nonzero off-diagonal Hessian entries; and
3. a three-dimensional degenerate multiband model showing that directional curvature
   matrices are not independent scalar-band mass tensors.

These are synthetic software/numerical verification problems. Passing them does not
validate silicon or authorize production calculations.

## Acceptance states

An effective-mass assessment has exactly one scientific status:

- `ACCEPTED_FOR_SELECTED_PARENT`: every required artifact and correlation is present;
  the target is a stationary, nondegenerate local minimum; the parent numerical,
  local-extraction, longitudinal-mass, transverse-mass, guard, and withheld-point gates
  pass; and every limitation is retained.
- `NOT_ACCEPTED`: at least one required gate fails with sufficient evidence to make
  that determination.
- `INCONCLUSIVE`: required evidence is absent, corrupted, conflicting, or too
  ill-conditioned to determine acceptance.

These statuses classify the bounded scientific assessment only. They do not authorize
execution, commit, publication, release, or promotion.

## Current retained four-Wannier analysis

The retained four-Wannier QE→Wannier90 analysis is useful method-development evidence
for same-frame operator construction, Wigner–Seitz interpolation, analytic Cartesian
derivatives, and a degenerate $\Gamma$ quadratic model. It does not satisfy this
specification because:

- it uses a $4\times4\times4$ reciprocal mesh without mass-convergence evidence;
- it does not locate and validate the indirect $\Delta$ conduction minimum;
- it does not supply direct-parent Cartesian mass stencils and withheld validation
  points;
- it does not establish retained-rank, window, projection, or Wannier-mesh mass
  convergence;
- its ultrasoft silicon pseudopotential is not the frozen PseudoDojo ONCV
  pseudopotential of the accepted bulk-pilot branch; and
- production-lineage authentication remains deferred.

It must remain a separate content-bound finite represented-model result. Its
curvatures cannot be promoted into a convergence point of the accepted bulk-pilot mass
campaign by relabeling.

## Execution and review gate

Before any protected production execution, report the exact executable and identity,
input system, physical branch, pseudopotential, candidate settings, invocation count,
expected compact and large outputs, anticipated runtime, memory, and storage, and the
failure/stop policy. Obtain explicit human authorization for that bounded execution.

Before a final effective-mass claim, obtain an independent review that checks state
identity, Cartesian conventions, $\hbar^2$ and unit conversion, extrema, Hessian
conditioning, convergence evidence, error separation, provenance, and claim language.

## Explicit non-results

- No new Quantum ESPRESSO or Wannier90 calculation was run.
- No effective mass, valley location, convergence setting, Wannier window, projection,
  retained rank, or uncertainty value is reported.
- No literature or experimental value is adopted as a calculated result or acceptance
  target.
- No current curvature branch is converted into a silicon effective mass.
- No valence-hole or SOC effective-mass result is accepted by this v1 protocol.
