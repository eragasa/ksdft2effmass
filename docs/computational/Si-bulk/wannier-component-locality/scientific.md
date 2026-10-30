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

The authoritative physical and numerical specifications together with the
[pseudopotential-library decision](../../../../specification/dft-pseudopotential-library/v1/index.md)
fix the campaign parent to:

- pristine two-atom primitive diamond silicon;
- PBE;
- PseudoDojo ONCVPSP v0.5, PBE, scalar-relativistic, stringent-table silicon
  in native UPF2 form, whose exact source entry, artifact bytes, and checksums
  must be acquired and accepted before execution;
- four valence electrons per silicon atom; and
- non-spin-polarized, non-SOC calculations.

Before execution, the campaign must additionally consume a zero-pressure
PBE-relaxed lattice accepted under Task `02.01.04` and mutually compatible,
exactly identified `pw.x`, `pw2wannier90.x`, and `wannier90.x` builds and
environments. Their values and identities are not selected by this page.

The earlier standard-table ONCV artifact with decompressed SHA-256
`39822757f53f36e3bf3bfb779356152a8d3f21199c7db9dd5a931e5d18c45282`
is a historical parent/comparator only and is not the v0.5/stringent production
artifact. The historical `Si.pbe-n-van.UPF`, 25-Ry, rank-four,
\(4^3\)-Wannier tutorial branch is preliminary evidence only. Neither is an
Si-VC production parent or production convergence point. Physical valence-hole
masses would require a separate SOC/spinor decision and are outside this branch.

## Preliminary motivation, not production evidence

A separate local retained-candidate package uses official Wannier90 3.1.0
`examples/example11` inputs and tutorial-scale settings to exercise a finite
represented \(H^W=T^W+R^W\) decomposition and real-space truncation diagnostics.
That package and its exact numerical observations are outside this documentation
candidate and have not yet completed their own provenance and evidence review.
They are therefore not quoted or promoted here.

The only admissible motivation at this stage is qualitative: cancellation in a
represented total Hamiltonian can make component-resolved locality differ from
total-Hamiltonian locality, so the ordering should be tested prospectively rather
than assumed. A later update may cite exact preview values only after the compact
package, external-output correlations, checksums, and evidence language are
separately retained and reviewed. A tutorial preview cannot establish production
convergence, an Si-VC subspace, validated effective masses, infinite-lattice
decay, asymptotic localization, or a material-level compressibility ordering.

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
  executable/build family, exact provisional seed structure, coupled-cutoff/k-point
  coordinate and selection plan, zero-pressure structural policy, fresh-confirmation
  stencil, and bounded re-relax/reconfirm budget.
- **H2 — subspace and construction freeze:** rank, parent bands, projections,
  windows and exclusions, uniform mesh sequence, gauge/initialization policy,
  random seeds, optimizer-basin rule, and candidate-selection thresholds.
- **H3 — confirmatory-analysis freeze:** physical radii, pair-symmetric mask,
  operator tolerances, evaluation grids, normalization, direct/tail comparison
  rules, allowed dispositions, and sealed construction and withheld roles.

These decisions freeze prospective inputs. They do not authorize calculator
execution or accept a scientific outcome.
