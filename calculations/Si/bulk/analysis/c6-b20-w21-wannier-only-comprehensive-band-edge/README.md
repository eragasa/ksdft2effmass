# Comprehensive non-SOC Wannier band-edge analysis

## Status

This directory retains an authorized, producer-checked development analysis of
the full `C6-B20-W21` rank-10 Wannier Hamiltonian and the frozen
`H-shell-05`, `H-shell-10`, and `H-shell-16` reduced models. No model was
refitted. No Quantum ESPRESSO or Wannier90 process was invoked. The work has
not received an independent reconstruction and is not publication-qualified
validation.

The source is scalar-relativistic and non-SOC. The valence results therefore
describe a three-band orbital manifold. They are not physical silicon
heavy-hole, light-hole, or split-off parameters and do not support acceptor
claims.

## Why this amendment was necessary

The preceding fidelity ladder characterized the indirect gap, six conduction
valleys, electron curvature, and principal electron masses. It did not examine
the valence-edge manifold. That omission matters: shell reduction can preserve
global spectral RMS while splitting or rotating the nearly degenerate
three-band valence cluster at Gamma.

A Hessian of each independently ordered valence band is not a valid general
solution at a degeneracy. Ordered branches can exchange identity and are not
analytic at Gamma. This study therefore retains both:

1. an explicit ordered-branch diagnostic, which exposes the failure of that
   convention; and
2. a degeneracy-aware three-band quadratic represented Hamiltonian, which is
   the primary non-SOC valence-curvature result.

## Frozen inputs

The request authenticates the final Wannier-only fidelity-ladder request,
producer, and result, plus the untruncated characterization. It reconstructs
the same four frozen Hamiltonians in the same rank-10 Wannier basis. Identity
alignment is used for same-gauge operator comparisons. The full source remains
a represented Wannier Hamiltonian that fails declared DFT-parent gap and
mass-adequacy criteria; source-relative preservation is not silicon validation.

## Methods

### Conduction valleys

The final valley coordinates from the preceding ladder are retained. For each
of the six valleys and each model, the Cartesian band-4 Hessian and gradient
are recomputed with central-difference steps of `0.001`, `0.002`, `0.005`, and
`0.01 inverse-angstrom`. The `0.002 inverse-angstrom` result is the primary
reported tensor. The analysis retains:

- the full inverse-mass and mass tensors;
- principal curvatures, axes, and masses;
- the one-valley density-of-states mass convention
  `(m1 m2 m3)^(1/3)`;
- the one-valley conductivity-mass convention
  `3 / (1/m1 + 1/m2 + 1/m3)`;
- the six-valley density-of-states convention
  `[sum_v (m1_v m2_v m3_v)^(1/2)]^(2/3)`; and
- the equal-population inverse-tensor average and its scalar conductivity-mass
  convention.

These are geometric summaries of the represented curvatures. No scattering,
carrier-density, finite-temperature transport, or physical DOS calculation is
claimed.

### Gamma valence cluster

Bands 1, 2, and 3 in zero-based ordering define the valence cluster. The result
records its energies, centroid, splitting, overlap singular values, projector
distance, and principal angles relative to the full-source cluster in the
common Wannier basis.

### Ordered-branch diagnostic

For `[100]`, `[110]`, and `[111]`, the three ordered cluster eigenvalues are
sampled symmetrically about Gamma. Even quartic fits are performed over
`0.005`, `0.01`, and `0.02 inverse-angstrom` half-windows. The resulting
apparent masses are retained only as a diagnostic of branch-ordering and
fit-window sensitivity. Missing points in the sensitivity figure denote a
positive fitted curvature rather than a silently clipped value.

### Degeneracy-aware multiband fit

At each displaced point, the three-band eigenspace is polar-transported to the
model's Gamma cluster. The `+q` and `-q` represented Hamiltonians are averaged,
and the matrix field is fitted to

```text
H_eff(q) = H_eff(0)
         + q_x^2 B_xx + q_y^2 B_yy + q_z^2 B_zz
         + 2 q_x q_y B_xy + 2 q_x q_z B_xz + 2 q_y q_z B_yz.
```

Thirteen unoriented rays and four positive radii per ray are used at each fit
window. Directional curvature channels are the eigenvalues of twice the
direction-contracted quadratic coefficient matrix. Negative channels are
reported as apparent non-SOC hole masses. The six candidate coefficient
matrices are polar-aligned to the source Gamma cluster before their joint
Frobenius error is evaluated.

For a reduced model whose `H_eff(0)` is already split, curvature-channel
eigenvalues describe the quadratic multiband operator; they are not Hessians
of independently nondegenerate branches.

### Additional checks

The study also evaluates:

- minimum direct gaps at Gamma and at six conventional X and eight
  conventional L points;
- equivalent-point gap spreads as a cubic-symmetry diagnostic; and
- ordered-band minima, maxima, bandwidths, VBM, CBM, and indirect gap on the
  independent Gamma-origin `32^3` mesh.

## Results

### Valence-cluster integrity

| Model | Gamma three-band splitting | Maximum source-cluster principal angle |
|---|---:|---:|
| Full source | 0.02495 meV | approximately 0 degrees |
| H-shell-05 | 102.175 meV | 1.856 degrees |
| H-shell-10 | 54.806 meV | 0.925 degrees |
| H-shell-16 | 2.496 meV | 0.0420 degrees |

The moderate reductions retain a recognizable three-dimensional subspace but
do not retain its internal near-degeneracy. Subspace fidelity alone is
therefore insufficient for valence-edge fidelity.

The independently ordered source branches are not stable mass objects. The
source upper branch is not hole-like in every fit window for any of the three
directions, and finite ordered-branch masses can change by up to about 75.5%
with the fit window. `H-shell-05` and `H-shell-10` look much more stable under
that invalid convention primarily because their large artificial Gamma
splittings remove the source degeneracy.

### Degeneracy-aware non-SOC curvature channels

At the primary `0.01 inverse-angstrom` window, the full-source apparent channel
masses in electron-mass units are:

| Direction | Channel 1 | Channel 2 | Channel 3 |
|---|---:|---:|---:|
| `[100]` | 0.1411 | 0.2771 | 0.3015 |
| `[110]` | 0.09690 | 0.3119 | 2.923 |
| `[111]` | 0.08770 | 0.6971 | 0.7722 |

These are eigenchannels of a non-SOC three-band quadratic operator, not HH,
LH, or split-off masses.

| Model | Aligned quadratic-coefficient error | Maximum channel-mass change |
|---|---:|---:|
| H-shell-05 | 9.54% | 38.9% |
| H-shell-10 | 5.88% | 19.7% |
| H-shell-16 | 0.279% | 4.53% |

The largest changes occur in the weak-curvature, large-mass channels. The
quadratic coefficient fits are numerically stable: changing the fit window
from `0.01` to `0.005` or `0.02 inverse-angstrom` changes the joint coefficient
field by at most about 0.41% among the four models. Primary fit residuals are
approximately `5-6e-7 eV` RMS.

### Conduction-mass summaries

| Model | Six-valley DOS-mass convention | Change from source | Conductivity-mass convention | Change from source |
|---|---:|---:|---:|---:|
| Full source | 1.4764 | — | 0.25063 | — |
| H-shell-05 | 1.2272 | 16.9% | 0.30188 | 20.4% |
| H-shell-10 | 1.1384 | 22.9% | 0.23335 | 6.90% |
| H-shell-16 | 1.4715 | 0.333% | 0.25058 | 0.0216% |

The maximum principal-mass spread across the four finite-difference steps is
below about 0.172% for every model. The much larger H-shell-05 and H-shell-10
source-relative changes are therefore not controlled by the selected stencil.

### High-symmetry and dense-mesh checks

Relative to the source Gamma direct gap of `2.55542 eV`, H-shell-05 and
H-shell-10 shift the gap by about `-41.8` and `-42.0 meV`; H-shell-16 shifts it
by about `-1.00 meV`.

Equivalent-point direct-gap spreads are:

| Model | X spread | L spread |
|---|---:|---:|
| Full source | 0.00366 meV | 0.0239 meV |
| H-shell-05 | 150.1 meV | 68.7 meV |
| H-shell-10 | 36.7 meV | 63.9 meV |
| H-shell-16 | 0.427 meV | 2.97 meV |

Thus the moderate fitted shell reductions also amplify residual
cubic-equivalence violations. On the `32^3` mesh, all four VBMs remain at
Gamma. The maximum ordered-band bandwidth change is about `354 meV` for
H-shell-05, `81.1 meV` for H-shell-10, and `3.14 meV` for H-shell-16.

## Interpretation

The expanded analysis strengthens the fidelity-ladder conclusion:

- H-shell-05 and H-shell-10 are not adequate band-edge reductions even when
  their global spectral errors appear moderate. They strongly split the
  valence manifold, change multiband curvature channels, alter derived electron
  masses, and amplify symmetry-equivalent gap differences.
- H-shell-16 remains close to the full Wannier source across electron tensors,
  the valence quadratic operator, direct gaps, and bandwidths, although its
  `2.50 meV` Gamma splitting is still roughly two orders of magnitude above the
  source splitting.
- A single hole mass tensor cannot be extracted from these non-SOC data without
  imposing an invalid ordered-band convention. The retained matrix-valued
  quadratic operator is the appropriate source-relative object.
- An SOC calculation would be needed only to promote this into physical
  silicon HH/LH/split-off or acceptor analysis. It is not needed for the
  present Wannier-compression diagnosis.

## Retained artifacts

- `request.json`: frozen scope and authenticated input identities.
- `run_analysis.py`: electron tensors, cluster/projector diagnostics,
  ordered-branch diagnostics, high-symmetry checks, and dense-mesh analysis.
- `result.json`: machine-readable primary result.
- `run_multiband_analysis.py`: degeneracy-aware three-band quadratic fit.
- `multiband-result.json`: machine-readable multiband result.
- `render_results.py`: primary figure renderer.
- `render_multiband.py`: multiband figure renderer.
- `render_figures_v2.py`: retained version-2 layout composition.
- `render_figures_v3.py`: strict-typing, no-overwrite layout-only composition of the
  two retained renderers.
- `plot-data.json`: machine-readable directional dispersion curves.
- `figures/`: original PDF and PNG renderings.
- `figures-v2/`: first layout-only successor separating legends from titles and
  increasing panel spacing.
- `figures-v3/`: strict-typing successor used by the manuscript; no Hamiltonian or
  scientific analysis was rerun.

The calculation scripts and retained outputs are no-overwrite artifacts.
