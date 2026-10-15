# Conference Paper 1, version 2

This directory contains the compact prose revision of Conference Paper 1 requested from
`model_class_expressivity_submission_edit.pdf`.

## Contents

- `manuscript.tex` is the editable, standalone LaTeX source.
- `manuscript.pdf` is a generated local build and is excluded by the repository's PDF
  ignore rule.
- The main paper and supplementary methods are combined in one document.
- Figures are consumed from the repository-owned calculation packages rather than copied
  into a second evidence tree.

## Source correlation

The user-provided prose reference has SHA-256
`872a69c87ef39d0ef1e7d25f97900286e017416c70abae63e88322877519db3a`.
The editable source was reconstructed from the accompanying
`model_class_expressivity_with_silicon_revised.tex` and synchronized to the prose
reference. The reference's substantive changes relative to that source were retained:

1. the shorter feasibility-focused abstract;
2. explicit reciprocal alignment and Fourier transformation for momentum-dependent
   identifications;
3. an explicit statement that a finite operator comparison does not certify omitted-tail
   locality; and
4. the distinction between spectral/operator admissibility and a separate locality or
   structural constraint.


The silicon section also includes the retained component-resolved shell-norm plot. It
shows larger kinetic than non-kinetic-remainder block norms at every nonzero canonical
radius of the finite tutorial mesh. The manuscript does not promote this observation to
a claim of slower infinite-lattice kinetic decay or identify the remainder as a scalar
potential.

The scientific scope remains bounded. Synthetic calculations establish controlled
software and numerical behavior only. The silicon material-facing preview is a read-only,
tutorial-scale finite-mesh truncation result; it does not establish production
convergence, material validation, effective masses, or a silicon expressivity
certificate. No Quantum ESPRESSO or Wannier90 calculation was run to prepare this
version.

## Build

From this directory:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error manuscript.tex
```

Before submission, replace the acknowledgment placeholder and supply an authorized
release identifier, exact source revision, and public archival record if applicable.
