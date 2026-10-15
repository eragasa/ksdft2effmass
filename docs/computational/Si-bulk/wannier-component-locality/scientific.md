# Scientific definition

## Campaign identity

The primary campaign identifier is **Si-VC**:

- **Si**: pristine diamond-structure silicon;
- **V**: the occupied valence manifold is retained; and
- **C**: low conduction states needed for the indirect gap, conduction valleys,
  and electron effective masses are retained.

The exact retained rank is deliberately absent from the identifier. A
rank-ten target is a paper-program candidate, not an accepted result. Only an
accepted ten-function branch may use the qualified record label **Si-VC10**.

A rank-four occupied-valence branch is **Si-V**. It is a qualification and
subspace-sensitivity control. It cannot satisfy the headline band-edge target
because it omits the low conduction states.

## Physical branch

The production parent is prospectively fixed to:

- pristine two-atom primitive diamond silicon;
- PBE;
- the scalar-relativistic PseudoDojo standard-table ONCV silicon
  pseudopotential with decompressed SHA-256
  `39822757f53f36e3bf3bfb779356152a8d3f21199c7db9dd5a931e5d18c45282`;
- four valence electrons per silicon atom;
- non-spin-polarized, non-SOC calculations;
- a zero-pressure PBE-relaxed lattice accepted under Task `02.01.04`; and
- mutually compatible, exactly identified `pw.x`, `pw2wannier90.x`, and
  `wannier90.x` builds and environments.

The historical `Si.pbe-n-van.UPF`, 25-Ry, rank-four, \(4^3\)-Wannier tutorial
branch is preliminary evidence only. It is neither an Si-VC parent nor a
production convergence point. Physical valence-hole masses would require a
separate SOC/spinor decision and are outside this branch.

## Preliminary motivation, not production evidence

The bounded [silicon Wannier-kinetic preview](../../../../calculations/ICMSEP2026/conference/paper_1/silicon-wannier-kinetic-preview/README.md)
uses official Wannier90 3.1.0 `examples/example11` inputs and tutorial-scale
settings: the ultrasoft `Si.pbe-n-van.UPF`, `ecutwfc = 25 Ry`, an unshifted
\(10^3\) SCF mesh, twelve parent bands, four retained Wannier functions, a
\(4^3\) Wannier mesh, and 6.5-eV window ceilings.

For its finite represented operator, the reciprocal decomposition defect is
about \(1.52\times10^{-15}\) eV and the native-`hr.dat` discrepancy is about
\(1.28\times10^{-5}\) eV. Retaining 57 of 64 blocks permits maximum ordered-
eigenvalue errors of approximately 0.0207, 0.0843, and 0.0636 eV for
\(H^W\), \(T^W\), and \(R^W\), respectively. Across the twelve nonzero finite
shell radii, the kinetic and remainder shell maxima exceed the total-Hamiltonian
shell maximum at eleven radii; their reported ratios span approximately
1.24--2.67.

These observations motivate component-resolved locality tests. They do not
establish production convergence, an Si-VC subspace, validated effective masses,
infinite-lattice decay, asymptotic localization, or a material-level
compressibility ordering.

## Bounded material question

For one accepted retained subspace and declared Wannier-gauge construction,
write

\[
H^W(\mathbf{k})=T^W(\mathbf{k})+R^W(\mathbf{k}).
\]

The campaign asks whether \(H^W\) is more compressible than both represented
components on a prospectively fixed physical-radius and operator-error domain.
No ordering is assumed.

The strongest admissible positive claim is:

> Within the identified PBE/ONCV Kohn--Sham parent, accepted Si-VC subspace,
> declared Wannier construction, tested numerical settings, and preregistered
> physical-radius domain, the total represented Hamiltonian requires less
> real-space support than both represented components at the declared operator
> error levels.

This is not an experimental validation, an infinite-lattice decay theorem, or a
claim that \(R^W\) is a continuous scalar potential. The finite represented
remainder may include represented local, nonlocal-pseudopotential, Hartree,
exchange-correlation, and other parent-Hamiltonian contributions.

## Subspace and gauge conditions

Component locality is gauge dependent. Every candidate must retain:

- parent-band inventory and scalar energy reference;
- inner- and outer-window membership at every source point;
- projectability and retained-subspace projector diagnostics;
- projections and their physical interpretation;
- disentanglement and localization objectives and stopping records;
- Wannier centers, spreads, symmetry diagnostics, and boundary-sewing defects;
- initialization and optimizer-basin identities; and
- common-space principal-angle and aligned-frame diagnostics across numerical
  settings.

Candidate selection uses parent-band, projector, interpolation, center, spread,
symmetry, and optimizer-basin evidence. It must not consume component-tail or
compressibility outcomes. At least one independently initialized accepted
candidate is required as a robustness guard. If accepted gauges reverse the
component ordering, the conclusion is inconclusive or must be narrowed to a
named gauge construction.

Si-V and Si-VC remain distinct token and evidence families. A favorable Si-V
control cannot be relabeled as the Si-VC production candidate.

## Claim dispositions

For each preregistered tolerance \(\tau\), define support-radius differences

\[
D_T(\tau)=r_T(\tau)-r_H(\tau),
\qquad
D_R(\tau)=r_R(\tau)-r_H(\tau).
\]

The strongest disposition requires positive \(D_T\) and \(D_R\) throughout the
predeclared tolerance/radius domain for every accepted mesh, parent-setting
guard, and gauge guard, with margins larger than observed finite-setting
variation. Tail diagnostics must not contradict the direct-error result.

Allowed dispositions are:

- `stable-total-more-compressible`;
- `gauge-or-subspace-conditional`;
- `numerically-inconclusive`;
- `no-supported-ordering`; or
- `reversed-ordering`.

A smooth interpolated band diagram, successful interface, small Wannier spreads,
or one favorable truncation radius cannot by itself produce the first
disposition.

## Scientific decisions

The scientific topology stops at explicit human gates:

- **H1 — prerequisite disposition:** numerical-warning disposition, exact
  executable/build family, cutoff/SCF-mesh coordinate plan, and zero-pressure
  acceptance policy.
- **H2 — subspace and construction freeze:** rank, parent bands, projections,
  windows and exclusions, uniform mesh sequence, gauge/initialization policy,
  random seeds, optimizer-basin rule, and candidate-selection thresholds.
- **H3 — confirmatory-analysis freeze:** physical radii, pair-symmetric mask,
  operator tolerances, evaluation grids, normalization, direct/tail comparison
  rules, allowed dispositions, and sealed construction and withheld roles.

These decisions freeze prospective inputs. They do not authorize calculator
execution or accept a scientific outcome.
