# Right-handed fixed-cutoff silicon k-point campaign

## Status

**Superseded for downstream selection by the Gamma-centered campaign.** This shifted
campaign remains immutable evidence and must not be relabelled as Gamma-centered.

This directory retains compact evidence from four explicitly authorized local Quantum
ESPRESSO SCF occurrences. ProjectKoios completed and analyzed all four occurrences and
its declared 1 meV/atom neighboring-point policy reported convergence. That software
policy result is not, by itself, scientific acceptance of a mesh, executable, seed
structure, or downstream parent model.

The exact external evidence root remains:

```text
/Users/eugene/projects/ksdft2effmass/
  si-kpoint-sssp-qe75-right-handed-20261031T052927Z/
```

[`external-artifact-inventory.json`](external-artifact-inventory.json) authenticates
all 420 non-cache files retained there, including saved-state files that must not be
committed to this repository. The compact repository copy retains the campaign records,
driver, inputs, standard output, standard error, and execution records.

## Bound inputs

- ProjectKoios revision:
  `e146f3722e87ca2de2243421a94448cfa6e27037`;
- Quantum ESPRESSO 7.5 `pw.x`: 9,673,048 bytes, SHA-256
  `87aa72158e2c103c63fce1deca977dc42ff4ba344519a9662aadb96d33eab910`;
- SSSP 1.3.0 PBE efficiency `Si.pbe-n-rrkjus_psl.1.0.0.UPF`: 1,299,382
  bytes, SHA-256
  `ae3aefd0811f9499dbc4a72f1f9ae02ef4fc7f3568bf6f559b68668719c69e2b`;
- right-handed provisional structure `Si.PrimitiveUnitCell.RightHanded`: 692
  bytes, SHA-256
  `7bef37dfe20ce58a137de942ec1fa0aa50d6e7049b0265790f12171bc834529a`;
- wavefunction and density cutoffs: 48 and 384 Ry;
- shifted meshes: `(6,6,6)`, `(8,8,8)`, `(10,10,10)`, and `(12,12,12)`,
  each with shift `(1,1,1)`;
- fixed occupations, spatial symmetry, and time reversal; and
- one process per occurrence, no retries.

## Observations

| Mesh | Irreducible points | SCF iterations | Energy (eV/atom) |
| --- | ---: | ---: | ---: |
| `6 x 6 x 6` | 28 | 5 | -155.37559836358443 |
| `8 x 8 x 8` | 60 | 5 | -155.37564128954625 |
| `10 x 10 x 10` | 110 | 5 | -155.37564244603018 |
| `12 x 12 x 12` | 182 | 5 | -155.37564319434330 |

The final neighboring-point energy differences reported by ProjectKoios are
0.0011564839326183574 and 0.0007483131128083187 meV/atom. These are far below the
declared 1 meV/atom workflow threshold.

## Mesh selection by `kpoints_convergence_atol`

[`kpoint-selection.json`](kpoint-selection.json) applies the declared
`kpoints_convergence_atol = 1.0 meV/atom` with zero relative tolerance. It compares
each sampled per-atom energy with the densest sampled K12 reference and selects the
smallest passing mesh. The absolute K6-to-K12 difference is
0.04483075886696497 meV/atom, so the selected finite-grid cutoff is **K6**, not K8.
The ProjectKoios two-tail-increment assessment establishes that the sampled tail passes;
it is not the mesh-selection rule.

QE reported a positive unit-cell volume and did not repeat the earlier negative
lattice-determinant warning. It found 48 symmetry operations for every occurrence. The
generic `ibrav=0`-with-symmetry advisory remains because the provider-neutral input uses
explicit cell vectors.

[`handedness-comparison.json`](handedness-comparison.json) compares these energies with
the earlier left-handed run. The absolute right-minus-left differences are at most
0.000476199261356669 meV/atom. This is diagnostic evidence that the exact basis-order
change preserved the sampled physical calculation; it is not independent validation.

## Unresolved diagnostics

Every occurrence exited successfully, reached the declared SCF tolerance in five
iterations, produced finite energies, and then emitted the same four Fortran IEEE flags:
invalid, divide-by-zero, overflow, and underflow. The flags also occurred in the earlier
left-handed campaign, so correcting lattice handedness did not remove them. The retained
standard errors do not identify an originating routine or affected quantity.

Current disposition: the handedness defect is resolved, but the IEEE flags remain a
scientific-review limitation. No claim is made here that they are harmless. Acceptance
for a downstream parent calculation should either bind a documented QE/toolchain
explanation or obtain a comparison from an independently built calculator path.
