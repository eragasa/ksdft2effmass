# Periodic multiband calculation program

This directory is the publication-independent planning and aggregation layer for periodic multiband calculations. Its primary purpose is to collect the salient, source-traceable results of dimension- and rank-specific calculation owners without transferring their identities or evidence status.

It is not a second implementation owner. Reusable algorithms remain under `python/src/ksdft2effmass/`; simulation entrypoints, verification, generated outputs, and retained runs remain with the individual calculation roots.

## Calculation map

| Spatial dimension | Retained rank | Current owner | Status |
|---|---:|---|---|
| 1-D | 1 | [`periodic1d/rank1/fourier-locality/`](../../periodic1d/rank1/fourier-locality/) | Pre-execution model-family-compatible scalar null-control design; no implementation or result |
| 1-D | 2 | [`periodic1d/rank2/band-equivalence-locality/`](../../periodic1d/rank2/band-equivalence-locality/) | Extracted development calculation; no retained successor run |
| 2-D | 2 | [`periodic2d/rank2/orthogonal/band-equivalence-locality/`](../../periodic2d/rank2/orthogonal/band-equivalence-locality/) | Bounded orthogonal development calculation |
| 2-D | 2 | [`periodic2d/rank2/nonorthogonal/band-equivalence-locality/`](../../periodic2d/rank2/nonorthogonal/band-equivalence-locality/) | Bounded nonorthogonal development calculation |
| 2-D | 2 | [`periodic2d/rank2/strain-locality/`](../../periodic2d/rank2/strain-locality/) | Bounded synthetic-strain development controls |
| 3-D | 2 | [`periodic3d/rank2/orthogonal/band-equivalence-locality/`](../../periodic3d/rank2/orthogonal/band-equivalence-locality/) | Bounded orthogonal development calculation |
| 3-D | 2 | [`periodic3d/rank2/nonorthogonal/band-equivalence-locality/`](../../periodic3d/rank2/nonorthogonal/band-equivalence-locality/) | Bounded nonorthogonal development calculation |
| 3-D | 2 | [`periodic3d/rank2/strain-locality/`](../../periodic3d/rank2/strain-locality/) | Bounded synthetic-strain development controls |
| 1-D | 3, 4, 8, 16 | [`periodic1d/rankN/composite-band-alignment-locality/`](../../periodic1d/rankN/composite-band-alignment-locality/) | Schema-free development calculation; no retained run |
| 2-D | greater than 2 | None | Prospective |
| 3-D | greater than 2 | None | Prospective |

The current cross-family rank-two comparison is owned by [`band-equivalence-dimensional-comparison/`](../../band-equivalence-dimensional-comparison/). This planning layer may summarize that output but does not replace it.

The retained [`Mathieu1D`](../../mathieu1d/) calculation remains a related scalar periodic-potential benchmark. It is not the model-family-compatible rank-one control and is not relabeled or replaced by this plan.

## Computational-experiment difficulty ladder

The levels below describe increasing model, geometry, alignment, verification, and resource complexity. They do **not** rank scientific importance or evidence maturity. A retained lower-level calculation can have stronger evidence than an unexecuted higher-level design.

### Level 0 --- structural and analytic null controls

- [`periodic1d/rank1/fourier-locality/`](../../periodic1d/rank1/fourier-locality/) --- planned compatible scalar control. It will test Fourier interpolation and truncation while recording that scalar phase conjugation cannot alter the represented Hamiltonian. No numerical model or run exists yet.

### Level 1 --- scalar single-band periodic reduction

- [`mathieu1d/`](../../mathieu1d/) --- retained one-dimensional Mathieu single-band Fourier reduction with strict schemas and producer-independent package verification. It is a related benchmark, not part of the compatible rank ladder.
- [`ICMSEP2026/conference/paper_1/isolated-band/`](../../ICMSEP2026/conference/paper_1/isolated-band/) --- retained controlled isolated-band reconstruction, truncation, fitting-route, and withheld-mesh predecessor.

### Level 2 --- one-dimensional rank-two alignment and locality

- [`periodic1d/rank2/band-equivalence-locality/`](../../periodic1d/rank2/band-equivalence-locality/) --- active four-state parent with a rank-two retained representation, smooth momentum-dependent rotations, and hopping-locality diagnostics.
- [`ICMSEP2026/conference/paper_1/multiband-alignment/`](../../ICMSEP2026/conference/paper_1/multiband-alignment/) --- retained rank-two synthetic alignment and matrix-valued hopping predecessor.
- [`ICMSEP2026/conference/paper_1/constrained-admissible-sets/`](../../ICMSEP2026/conference/paper_1/constrained-admissible-sets/) --- retained finite alignment-family witness and separation calculation.

### Level 3 --- multidimensional rank-two orthogonal controls

- [`periodic2d/rank2/orthogonal/band-equivalence-locality/`](../../periodic2d/rank2/orthogonal/band-equivalence-locality/) --- bounded square-lattice three-mesh development calculation.
- [`periodic3d/rank2/orthogonal/band-equivalence-locality/`](../../periodic3d/rank2/orthogonal/band-equivalence-locality/) --- bounded simple-cubic three-mesh development calculation; retained rank remains two.

### Level 4 --- basis-aware, strain, and cross-family rank-two analysis

- [`periodic2d/rank2/nonorthogonal/band-equivalence-locality/`](../../periodic2d/rank2/nonorthogonal/band-equivalence-locality/) --- triangular-Bravais/honeycomb-basis controlled development calculation.
- [`periodic3d/rank2/nonorthogonal/band-equivalence-locality/`](../../periodic3d/rank2/nonorthogonal/band-equivalence-locality/) --- FCC-Bravais/diamond-basis controlled development calculation.
- [`periodic2d/rank2/strain-locality/`](../../periodic2d/rank2/strain-locality/) --- two-dimensional rhombic geometry, frozen-response, prescribed-response, and scan controls.
- [`periodic3d/rank2/strain-locality/`](../../periodic3d/rank2/strain-locality/) --- three-dimensional Bain-path geometry, response, and scan controls.
- [`band-equivalence-dimensional-comparison/`](../../band-equivalence-dimensional-comparison/) --- aggregation of compatible rank-two family definitions into tolerance and shell--scale comparisons.

### Level 5 --- one-dimensional higher-rank non-Abelian controls

- [`periodic1d/rankN/composite-band-alignment-locality/`](../../periodic1d/rankN/composite-band-alignment-locality/) --- calculation-owned schema-free development composition for ranks 3, 4, 8, and 16; rotation depths 1, 2, 4, and 8; and no-alignment, global, pointwise, and known-inverse controls. Strict serialization, a full independent verifier, and retained evidence remain absent.

### Level 6 --- higher-rank multidimensional controls

- **Periodic 2-D higher rank** --- prospective; no calculation root, implementation, or result.
- **Periodic 3-D higher rank** --- prospective; no calculation root, implementation, or result.

### Level 7 --- external-code and material-facing reductions

- [`research-monograph/periodic-1d/`](../../research-monograph/periodic-1d/) --- retained periodic one-dimensional controlled reductions and Wannier90 attempts used only as historical integration precursors.
- [`Si/bulk/`](../../Si/bulk/) --- canonical planning and aggregation owner for bulk-parent qualification, the prospective Wannier bridge, and joint spectral/operator reduction. Historical tutorial, reference, smoke-comparison, and provisional convergence records remain under [`bulk-silicon/`](../../bulk-silicon/); neither location establishes an accepted parent or material validation.

## Contents

- [`development-plan.md`](development-plan.md) gives the staged multiband program in plain language.
- [`analysis/README.md`](analysis/README.md) defines the aggregation boundary.
- [`analysis/salient-results.md`](analysis/salient-results.md) records the currently supportable cross-project summary and its evidence classifications.

## Evidence rule

Aggregation never upgrades evidence. A development result remains development evidence; a retained result keeps its original package identity; an analytic certificate does not become numerical validation; and an absent result remains absent. Every quantitative entry must link to its calculation-owned source or be marked as unavailable.
