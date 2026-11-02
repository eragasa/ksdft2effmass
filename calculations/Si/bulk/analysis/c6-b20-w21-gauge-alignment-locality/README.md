# C6-B20-W21 gauge alignment and hopping locality

**Status:** producer-checked development analysis completed on 2026-11-02 and not
independently reconstructed. The retained run invoked no Quantum ESPRESSO or Wannier90
process and does not create a publication-qualified physics claim or release.

## Purpose

This directory owns the Hamiltonian-only application of the periodic-3D rank-N
alignment/locality framework to the authenticated, provider-eligible rank-10
`C6-B20-W21` silicon Wannier operator.

The calculation asks how a frozen momentum-dependent unitary acting inside the retained
rank-10 Wannier coordinates changes restricted alignment, finite Fourier-block locality,
and equal-accuracy finite-support requirements while preserving the complete represented
Hamiltonian spectrum.

The calculation is a controlled representation study on a DFT-derived finite operator.
It is not a claim that the source operator is an adequate production silicon model. The
revealed 408-point development comparison found that the source fails the declared gap
and effective-mass fidelity targets. That parent-fidelity result remains a separate
qualification layer rather than being hidden inside the gauge or truncation channels.

## Canonical sources

A frozen request must authenticate the applicable exact bytes from:

- [`../c6-b20-w21-untruncated-characterization/`](../c6-b20-w21-untruncated-characterization/)
  — S30 source identity, native HR/Wigner--Seitz reconstruction, units, energy
  reference, lattice, and structural checks;
- [`../c6-b20-w21-revealed-408-development/`](../c6-b20-w21-revealed-408-development/)
  — the revealed 408-point direct-parent development overlay;
- [`../construction-mesh-adequacy-recommendation/`](../construction-mesh-adequacy-recommendation/)
  — exact C6 construction coordinates and the unobserved 402-point confirmation
  boundary;
- [`../c6-b20-w21-spatial-truncation-design/`](../c6-b20-w21-spatial-truncation-design/),
  [`../c6-b20-w21-spatial-truncation-evaluation/`](../c6-b20-w21-spatial-truncation-evaluation/),
  and
  [`../c6-b20-w21-spatial-truncation-disposition/`](../c6-b20-w21-spatial-truncation-disposition/)
  — fixed-Wannier-gauge native Wigner--Seitz shell evidence retained only as a separate
  comparator; and
- the provider-eligible `C6-B20-W21` localization evidence under
  [`../../simulations/evidence/`](../../simulations/evidence/) — authenticated HR,
  `u`, `u_dis`, localization, and external-artifact identities.

The exact source digest inventory is frozen in [`request.json`](request.json). Paths
alone are not source authentication; `run_analysis.py` checked every declared byte size
and SHA-256 digest before parsing.

## Comparison boundary

The primary represented operator is the full untruncated Hamiltonian
`H_W(k)` in its declared rank-10 Wannier coordinates. This first calculation does not
add kinetic/non-kinetic component roles and does not infer atomic `sp3s*` semantics from
matrix rank.

The generic field analysis uses the retained coordinate space itself as the common
ambient comparison space. Identity coordinate frames represent the reference field; the
frozen attack acts on their right. Admission of the actual Wannier90 `u_dis` and `u`
artifacts remains an upstream S30/provider qualification and is not reinterpreted as an
off-mesh DFT frame.

The required alignment channels are:

1. identity comparison;
2. one momentum-independent global unitary;
3. pointwise complete-unitary polar recovery; and
4. the generating known-inverse oracle.

The oracle is an implementation control, not a fitted localization method and not a
competitor to Wannier90.

## Error channels

The calculation keeps these layers separate:

1. direct-parent representation error of complete `H_W` on the revealed 408-point
   inventory;
2. exact complete-field gauge equivalence within the represented rank-10 space;
3. cyclic-to-ordinary conversion consequences;
4. finite interpolation consequences;
5. deliberate complete-support truncation consequences; and
6. total finite-model consequences relative to the declared direct represented target.

Direct-parent values may be displayed only as a labeled development overlay. They must
not select the attack, support inventory, support-error curve projections, or future
acceptance thresholds. The frozen 402-point parent values remain forbidden inputs.

## Representation routes

Two real-space routes must not be conflated:

- the native Wannier90 HR/Wigner--Seitz representation authenticated by S30; and
- the centered finite-cyclic transform of sampled represented fields used by the
  periodic-3D framework, followed by explicit ordinary-lattice conversion.

Any cross-route comparison must declare the different representative and degeneracy
semantics. Native Wigner--Seitz blocks are not silently substituted for finite-cyclic
blocks, and the earlier S90/S100 shell inventory is not automatically reused for the
attacked representation.

## Maintained software boundary

Reusable field, attack, alignment, Fourier, locality, truncation, and verification
behavior belongs under:

```text
python/src/ksdft2effmass/periodic3d/rankN/
```

This calculation directory may authenticate source artifacts, construct immutable
requests, compose maintained actions, retain producer checks, and render explicitly
unverified development plots. Independent reconstruction is not required for this
version. It must not become a second reusable implementation.

The current development surfaces include:

- `Periodic3DRankNWannierFieldSource`;
- `Periodic3DRankNWannierFieldProducer`;
- `Periodic3DRankNGivensGaugeAttack`; and
- `Periodic3DRankNBandEquivalenceHoppingLocalityFieldAnalyzer`.

Their names and contracts are not frozen by this README. A retained calculation request
must bind the reviewed installed implementation identity used for that execution.

## Retained files

The authorized producer-only run retains:

```text
protocol.md
request.json
run_analysis.py
result.json
render_plots.py
render_pareto.py
figures/
executions/
```

`result.json` contains the complete plot-data contract, source identities, producer
checks, alignment results, shell curves, 125 displacement powers, and all 408 reference,
attacked, and matched-parent spectra. `figures/figure-manifest.json` checksum-binds the
original nine PDF and nine PNG renderings to the result and renderer.
`figures/pareto-figure-manifest.json` separately binds the corrected discrete Pareto
frontier that supersedes the original raw support-curve panel in the technical report.

The maximum complete-spectrum change under the attack was
`3.197442310920451e-14 eV`. Identity and global-unitary alignment left order-one frame
defects, while pointwise polar and known-inverse controls reduced them to approximately
`1.29e-15` and `5.06e-16`. These are internal represented-operator results, not a
validation of the silicon parent.

## Nonclaims

This owner does not establish:

- production-qualified or experimentally validated silicon physics;
- adequacy of the source Wannier operator for its failed intended-use targets;
- a converged construction-mesh limit;
- an accepted finite hopping support;
- atomic-orbital, site, sigma, pi, or Slater--Koster semantics;
- component-resolved `H/T/R` locality;
- a universal relationship between hopping power and spectral error; or
- authorization for calculator execution, any additional retained analysis,
  publication, or release.

## Authorization boundary

The 2026-11-02 no-calculator analysis and plot rendering were explicitly authorized in
the active operator session. Any additional retained run requires a new bounded
instruction. Any Quantum ESPRESSO or Wannier90 invocation remains a protected action
requiring separate explicit authorization.
