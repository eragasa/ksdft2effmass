# Ragasa2026icmsep conference presentation

This directory contains a conference-oriented Beamer presentation derived from the v1
working manuscript. The main talk centers the active Wigner--Seitz shell deletion and
shell-scale fitting study. Slater--Koster appears only in backup material as a separate,
rank-deficient common-space route that was not fitted.

The deck preserves the manuscript's evidence hierarchy and claim boundaries:

- exact analytic rank-two statements remain separate from sampled calculations;
- silicon results remain producer-checked development evidence unless explicitly noted;
- the independent convention audit is not described as a reconstruction of the
  Hamiltonian calculations; and
- source-relative reduction fidelity is not described as silicon validation.

The slides reuse retained repository figures directly. They do not own or replace the
calculation records and do not authorize new QE, Wannier90, optimization, submission,
release, or archival operations.

## Build

From this directory:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error presentation.tex
```

The build uses Biber and the research-monograph bibliography at
`../../../../research-monograph/references.bib`. The reference backup includes the 63
entries selected as relevant to this talk's DFT, Wannier, alignment, reduction,
effective-mass, verification, and future-work context. `presentation.pdf` is a local
working rendering and is not a publication record.

## Current rendering

- Event: 4th International Conference on Materials Science and Engineering in the Philippines (ICMSEP 2026)
- Schedule and venue: 5--7 November 2026, Widus Hotel, Clark, Pampanga, Philippines
- Presenter: Eugene Joseph M. Ragasa, De La Salle University, Department of Physics
- Main talk: 33 slides, including title, section separators, implementation details, operator background, conclusion, and closing slide
- Main structure: Section I Introduction; Section II Scientific Software Implementation; Section III Rank-Two Periodic Theory; Section IV Rank-10 Silicon Case Study; Section V Conclusion
- Backup: 10 logical frames rendered as 21 pages, including the retained-dimension theorem and 12 reference pages
- Total: 54 rendered slides/pages
- PDF SHA-256: `25309791e9d8a8e5a1abb36221b8908c30eb36f37acc41128fe1662bc328ad30`
- Full-HD PNG export: `png-slides/slide-001.png` through `slide-054.png`
- Image-based PowerPoint export: `presentation.pptx`, 54 slides
- PowerPoint SHA-256: `fd9d4ae10870fb3084919d9fd57ad762027dbf5f4531acf4b5ada1b732b534dd`

The PowerPoint export uses one full-slide 1920-by-1080 PNG per page to preserve the
Beamer rendering exactly. Its text and diagrams are therefore not individually editable
PowerPoint objects.

The implementation-slide inventory reports 320,543 physical lines in Python files
beneath four selected `src` trees: optimization/numerics, PhysKit,
`projectkoios-simulations`, and `ksdft2effmass`. It excludes tests, documentation,
calculations, and generated artifacts. The simulations count is 36,971 lines from the
clean PW-DFT/Wannierization tranche at commit
`ec670681466f3ce0cc58db589d45c13a011f9b10`, whose package surfaces include the
optional SNAKES workflow topology and outward Quantum ESPRESSO and Wannier90
integrations. The formal
inventory uses the clean `projectkoios-formal` main tree at commit
`80145602d4d84e26a4c5ccd7bbd362618598e39b`: 24,870 physical lines beneath its
repository-owned Lean source tree and 956 proved theorem/lemma rows tracked by the
authoritative theorem manifest (858 theorems and 98 lemmas).
