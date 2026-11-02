# Ragasa2026icmsep v1

## Purpose

This is a long-form working journal article titled **Band Equivalence, Hopping Locality, and Internal Fidelity of Reduced Wannier Hamiltonians: From Exact Rank-Two Geometry to a DFT-Derived Rank-10 Silicon Case Study**.

It combines:

1. the PIAB1D/QHO1D calibration hierarchy separating spectral compression, finite-matrix accuracy, finite spatial extent, and grid refinement;
2. the exact rank-two loss geometry, Bessel threshold law, residual/locality identity, and controlled range-inflation calculation from `Ragasa2026a`;
3. the source construction and evidence boundaries documented by `Ragasa2026d`;
4. the completed rank-10 silicon gauge/locality, literal shell, refitted shell, exact Parseval, dense-mesh, conduction-edge, and multiband-valence analyses;
5. one authorized accepted-S1 parent DFT band path with a full-source Wannier overlay; and
6. an explicit calculation inventory, error-channel matrix, checksum anchors, and claim/nonclaim register.

All theory, computational methodology, diagnostic figures, calculation inventories, and reproducibility material remain in the main article rather than being split into supplementary material. The silicon section records the retained DFT/Wannier construction, gauge circuit, Fourier and support conventions, shell-scale gradients and optimization, exact frozen coefficients, dense-mesh evaluation, valley search, finite-difference tensors, mass conventions, cluster transport, and multiband quadratic fitting.

## Status

Working synthesis only. It is not submission-ready and is not publication-qualified evidence.

- Analytic claims retain their explicit assumptions.
- Rank-two numerical surfaces retain their existing development/partial-verification status.
- Silicon analyses are producer-checked development evidence without independent reconstruction.
- The source Wannier model fails separate DFT-parent gap and electron-mass targets.
- Frozen 402-point confirmation values remain excluded.
- No physical HH/LH/split-off, acceptor, or SOC conclusion is made.
- One explicitly authorized local QE 7.5 fixed-density parent band-path run was performed; no Wannier90 execution or additional source construction was performed.
- The apparent `0.5226105 eV` versus `0.6892447 eV` gap discrepancy is resolved as two distinct candidate Hamiltonians compared with the same revealed DFT parent: the former is the earlier lower-energy-frozen `4^3`/12-band candidate, while the latter is the current `C6-B20-W21` source.

## Build

From this directory:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error manuscript.tex
```

The build uses `biber` through `latexmk`.

## Files

- `manuscript.tex` — complete journal-style source, including appendices;
- `references.bib` — bibliography;
- `manuscript.pdf` — rendered working manuscript;
- `evidence-allocation.md` — relationship to the existing paper program;
- `referee-response-1.md` — disposition and response to the first technical referee review.

Auxiliary LaTeX files are build products and are not evidence records.

## Current rendering

- Length: 50 pages
- PDF SHA-256: `3c0eb7ec2ef51f5a61d8a3119f1170215f6e8a3c470eecec34ba084eb5406f1e`

The PDF is a working synthesis artifact, not a sealed calculation result or publication record.
