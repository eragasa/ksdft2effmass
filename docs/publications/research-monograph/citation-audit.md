# Complete citation audit

## Editorial status

This is a prospective source-discovery audit, not a literature review. The
candidate articles and books have not all been read. Every recommendation must
remain unresolved until the relevant source is read and its support for the
exact local claim is checked. The corresponding manuscript prompts are shown as
red **Prospective citation note** boxes. The 21 candidate records originally
reported below as missing have since been copied provisionally into
`references.bib` so each displayed key can carry a rendered citation. The
individual status lines preserve the audit-time baseline and do not indicate
that metadata or claim support has been accepted.

## Scope and method

This audit covers the Preface, Chapters 1–20, and Appendices A–I. Appendices
C–I are the material formerly organized as Technical Notes. Every TeX source
was reviewed against `references.bib`; all 62 existing citation-key occurrences
were reconciled, representing all 45 bibliography entries. No unresolved or
misspelled existing key was found.

The findings below are intended to avoid indiscriminate citation prompts:
project-specific definitions, proposed workflows, exact derivations supplied in
the manuscript, and explicit nonclaims were not flagged merely because they
lack external citations. This selectivity does not upgrade the recommendations
from prospective notes to verified source judgments. Approximate line
numbers refer to the audited source state and may move during later editing.

**Location:** `docs/publications/research-monograph/chapters/00-preface.tex`, approximately lines 164–168, “Program scope.”

**Passage / claim:** A neutral periodic dopant supercell must not be silently reinterpreted as an isolated or ionized impurity.

**Why a citation is needed:** This is a substantive defect-physics distinction involving charge state, boundary conditions, and finite-supercell interpretation, not merely an editorial convention. A standard point-defect review would support the warning.

**Recommended citation(s):**
- Christoph Freysoldt, Blazej Grabowski, Tilmann Hickel, Jörg Neugebauer, Georg Kresse, Anderson Janotti, and Chris G. Van de Walle, *First-Principles Calculations for Point Defects in Solids*, 2014
- Bibliographic key if already present: `freysoldt2014`
- Status: PRESENT IN BIBLIOGRAPHY

**Priority:** Medium

---

**Location:** `docs/publications/research-monograph/appendices/J-envelope-theory-luttinger-khon-burt-ermoneit.tex`, with the motivating pointer in `chapters/01-model-adequacy.tex`, “Project motivation and significance.”

**Passage / claim:** Band curvature near an extremum leads to the effective-mass kinetic operator, while a controlled envelope theory additionally requires a state-space map and treatment of band truncation, gauge, valleys, and spatial coarse-graining.

**Why a citation is needed:** This is the foundational technical transition on which the chapter’s motivation rests. The opening textbook footnote is too remote and general to document the specific envelope-function derivation and its limitations. Primary effective-mass work and dedicated envelope-function analyses are already available in the bibliography.

**Recommended citation(s):**
- J. M. Luttinger and W. Kohn, *Motion of Electrons and Holes in Perturbed Periodic Fields*, 1955
- Bibliographic key if already present: `luttingerKohn1955`
- Status: PRESENT IN BIBLIOGRAPHY

- M. G. Burt, *The Justification for Applying the Effective-Mass Approximation to Microstructures*, 1992
- Bibliographic key if already present: `burt1992`
- Status: PRESENT IN BIBLIOGRAPHY

- M. G. Burt, *Fundamentals of Envelope Function Theory for Electronic States and Photonic Modes in Nanostructures*, 1999
- Bibliographic key if already present: `burt1999`
- Status: PRESENT IN BIBLIOGRAPHY

- L. Ermoneit, A. Thayil, T. Koprucki, and M. Kantner, *Exact Multivalley Envelope Function Theory of Valley Splitting in Si/SiGe Nanostructures*, 2026
- Bibliographic key if already present: `ermoneit2026`
- Status: PRESENT IN BIBLIOGRAPHY

**Resolution update:** Resolved for the four identified sources. The supplied
copies of Luttinger and Kohn (1955), Burt (1992, 1999), and Ermoneit et al.
(2026) have been read in full. Appendix~J, titled *Envelope Theory: Luttinger
Khon, Burt, and Ermoneit*, now extracts the specific source equations for the
band-edge basis, exact band-limited envelope representation, nonlocal and local
multiband equations, dominant-envelope elimination, interface conditions,
operator ordering, out-of-zone solutions, valley-sector projection,
energy-reference invariance, and observable reconstruction. Chapter~1 retains only a motivating
cross-reference. These papers still do not establish modern Wannier
disentanglement, independently generated pristine--doped alignment, or the
project's proposed continuum crossover.

**Priority:** High

---

**Location:** `docs/publications/research-monograph/chapters/01-model-adequacy.tex`, approximately lines 324–352, “Project motivation and significance,” retained entangled bands, projection/disentanglement, and Bloch-gauge discussion.

**Passage / claim:** A smooth retained family for entangled bands may require projection or disentanglement, and Bloch-gauge changes alter matrix coordinates without changing the represented abstract operator or spectrum.

**Why a citation is needed:** Disentanglement and momentum-dependent Wannier gauge freedom are established technical features of Wannier construction. These claims should be tied directly to the primary disentanglement paper and the established review rather than left under the chapter’s general solid-state citations.

**Recommended citation(s):**
- Ivo Souza, Nicola Marzari, and David Vanderbilt, *Maximally Localized Wannier Functions for Entangled Energy Bands*, 2001
- Bibliographic key if already present: `souza2001`
- Status: PRESENT IN BIBLIOGRAPHY

- Nicola Marzari, Arash A. Mostofi, Jonathan R. Yates, Ivo Souza, and David Vanderbilt, *Maximally Localized Wannier Functions: Theory and Applications*, 2012
- Bibliographic key if already present: `marzari2012`
- Status: PRESENT IN BIBLIOGRAPHY

**Priority:** Medium

---

**Location:** `docs/publications/research-monograph/chapters/01-model-adequacy.tex`, approximately lines 619–642, “Central hypothesis,” norm-resolvent convergence equation.

**Passage / claim:** Norm-resolvent convergence, using identification maps between changing retained spaces and the continuum space, is proposed as one possible continuum criterion.

**Why a citation is needed:** The project-specific choice is explicitly provisional and does not itself require precedent, but the established mathematical meaning and implications of norm-resolvent convergence should be anchored to an operator-theory source.

**Recommended citation(s):**
- Gerald Teschl, *Mathematical Methods in Quantum Mechanics: With Applications to Schrödinger Operators*, 2014
- Bibliographic key if already present: `teschl2014`
- Status: PRESENT IN BIBLIOGRAPHY

**Priority:** Low

---

**Location:** `docs/publications/research-monograph/chapters/01-model-adequacy.tex`, approximately lines 650–660, “Relation to Hilbert’s sixth problem.”

**Passage / claim:** Hilbert’s sixth problem is characterized as calling for rigorous formulations of physical theories and justification of limiting relations between microscopic and continuum descriptions.

**Why a citation is needed:** This is a historical characterization of a named primary source. The monograph should cite Hilbert’s published problem statement rather than relying on an uncited paraphrase.

**Recommended citation(s):**
- David Hilbert, *Mathematical Problems*, 1902
- Bibliographic key if already present: none
- Status: MISSING FROM BIBLIOGRAPHY
- If missing, complete BibTeX

```bibtex
@article{hilbert1902,
  author  = {Hilbert, David},
  title   = {Mathematical Problems},
  journal = {Bulletin of the American Mathematical Society},
  volume  = {8},
  number  = {10},
  pages   = {437--479},
  year    = {1902},
  doi     = {10.1090/S0002-9904-1902-00923-3},
  note    = {Translated by Mary Winston Newson}
}
```

**Priority:** Medium

---

**Location:** `docs/publications/research-monograph/chapters/02-operator-comparison.tex`, approximately lines 100–104, “Basis transformations and gauge.”

**Passage / claim:** Momentum-dependent unitary freedom changes the Wannier basis; localization selects or optimizes a gauge; equal band energies do not determine Wannier functions or a distinguished alignment between calculations.

**Why a citation is needed:** The finite-dimensional basis-change equation is self-contained, but its specialization to Bloch/Wannier gauge and localization is a domain-specific result. Direct citations would distinguish established Wannier theory from the chapter’s proposed alignment framework.

**Recommended citation(s):**
- Nicola Marzari, Arash A. Mostofi, Jonathan R. Yates, Ivo Souza, and David Vanderbilt, *Maximally Localized Wannier Functions: Theory and Applications*, 2012
- Bibliographic key if already present: `marzari2012`
- Status: PRESENT IN BIBLIOGRAPHY

- Ivo Souza, Nicola Marzari, and David Vanderbilt, *Maximally Localized Wannier Functions for Entangled Energy Bands*, 2001
- Bibliographic key if already present: `souza2001`
- Status: PRESENT IN BIBLIOGRAPHY

**Priority:** Medium

---

**Location:** `docs/publications/research-monograph/chapters/02-operator-comparison.tex`, approximately lines 163–171, “Energy references.”

**Passage / claim:** A band-edge plotting reference and an electrostatic estimator used to align pristine and doped supercells are not automatically the same convention; a common scalar energy zero is required before bulk–dopant subtraction.

**Why a citation is needed:** The algebraic effect of adding a scalar identity is self-contained, but electrostatic alignment across defect supercells is a specialized methodological issue with established primary and review literature. Citation is especially important because energy alignment is a stop condition for the proposed impurity subtraction.

**Recommended citation(s):**
- Christoph Freysoldt, Jörg Neugebauer, and Chris G. Van de Walle, *Fully Ab Initio Finite-Size Corrections for Charged-Defect Supercell Calculations*, 2009
- Bibliographic key if already present: `freysoldt2009`
- Status: PRESENT IN BIBLIOGRAPHY

- Christoph Freysoldt, Blazej Grabowski, Tilmann Hickel, Jörg Neugebauer, Georg Kresse, Anderson Janotti, and Chris G. Van de Walle, *First-Principles Calculations for Point Defects in Solids*, 2014
- Bibliographic key if already present: `freysoldt2014`
- Status: PRESENT IN BIBLIOGRAPHY

**Priority:** High

---

**Location:** `docs/publications/research-monograph/chapters/03-evidence-for-model-adequacy.tex`, approximately lines 37–68 and 210–232, “Evidence classes” and “Uncertainty quantification.”

**Passage / claim:** The chapter distinguishes mathematical proof, software verification, numerical verification, scientific validation, and uncertainty quantification, and states that these evidence classes do not imply one another.

**Why a citation is needed:** This taxonomy is central to the monograph and overlaps established verification, validation, and UQ terminology. The project may refine the categories, but an authoritative source should identify the external methodological foundation and make project-specific extensions visible.

**Recommended citation(s):**
- National Research Council, *Assessing the Reliability of Complex Models: Mathematical and Statistical Foundations of Verification, Validation, and Uncertainty Quantification*, 2012
- Bibliographic key if already present: none
- Status: MISSING FROM BIBLIOGRAPHY
- If missing, complete BibTeX

```bibtex
@book{nationalResearchCouncil2012,
  author    = {{National Research Council}},
  title     = {Assessing the Reliability of Complex Models: Mathematical and
               Statistical Foundations of Verification, Validation, and
               Uncertainty Quantification},
  publisher = {The National Academies Press},
  address   = {Washington, DC},
  year      = {2012},
  doi       = {10.17226/13395},
  url       = {https://doi.org/10.17226/13395}
}
```

**Priority:** High

---

**Location:** `docs/publications/research-monograph/chapters/03-evidence-for-model-adequacy.tex`, approximately lines 191–203, “Scientific validation.”

**Passage / claim:** The PBE Kohn–Sham parent disagrees with the experimental silicon gap, and that discrepancy must be classified as parent-model error rather than reduction error.

**Why a citation is needed:** The error attribution is well reasoned, but the asserted silicon-specific disagreement is an external factual claim. It needs both a PBE silicon benchmark and an experimental or evaluated silicon reference. The exact Kohn–Sham gap literature explains why Kohn–Sham eigenvalue gaps and physical fundamental gaps require care, but does not alone establish the numerical discrepancy for the project’s settings.

**Recommended citation(s):**
- Jochen Paier, Martijn Marsman, Kerstin Hummer, Georg Kresse, Iann C. Gerber, and János G. Ángyán, *Screened Hybrid Density Functionals Applied to Solids*, 2006
- Bibliographic key if already present: none
- Status: MISSING FROM BIBLIOGRAPHY
- If missing, complete BibTeX

```bibtex
@article{paier2006,
  author  = {Paier, Jochen and Marsman, Martijn and Hummer, Kerstin and
             Kresse, Georg and Gerber, Iann C. and
             {\'A}ngy{\'a}n, J{\'a}nos G.},
  title   = {Screened Hybrid Density Functionals Applied to Solids},
  journal = {The Journal of Chemical Physics},
  volume  = {124},
  number  = {15},
  pages   = {154709},
  year    = {2006},
  doi     = {10.1063/1.2187006}
}
```

- Peter Y. Yu and Manuel Cardona, *Fundamentals of Semiconductors: Physics and Materials Properties*, 2010
- Bibliographic key if already present: `yuCardona2010`
- Status: PRESENT IN BIBLIOGRAPHY

- John P. Perdew and Mel Levy, *Physical Content of the Exact Kohn–Sham Orbital Energies: Band Gaps and Derivative Discontinuities*, 1983
- Bibliographic key if already present: `perdewLevy1983`
- Status: PRESENT IN BIBLIOGRAPHY

- L. J. Sham and M. Schlüter, *Density-Functional Theory of the Energy Gap*, 1983
- Bibliographic key if already present: `shamSchluter1983`
- Status: PRESENT IN BIBLIOGRAPHY

**Priority:** High

---

**Location:** `docs/publications/research-monograph/chapters/03-evidence-for-model-adequacy.tex`, approximately lines 205–208, “Scientific validation.”

**Passage / claim:** Dopant validation references must match charge state, periodic versus isolated setting, spin/SOC branch, band-edge reference, and observable; a neutral periodic P:Si calculation cannot directly validate an isolated ionized-donor potential.

**Why a citation is needed:** This is a domain-specific constraint on defect-model interpretation. The charge-state and periodic-supercell distinctions are supported by the established point-defect literature and are consequential for what validation claim is permitted.

**Recommended citation(s):**
- Christoph Freysoldt, Blazej Grabowski, Tilmann Hickel, Jörg Neugebauer, Georg Kresse, Anderson Janotti, and Chris G. Van de Walle, *First-Principles Calculations for Point Defects in Solids*, 2014
- Bibliographic key if already present: `freysoldt2014`
- Status: PRESENT IN BIBLIOGRAPHY

**Priority:** High

---

**Location:** `docs/publications/research-monograph/chapters/03-evidence-for-model-adequacy.tex`, approximately lines 241–247, “Training, validation, and leakage.”

**Passage / claim:** Withheld validation data must not affect parameter selection, model-class expansion, stopping rules, or tolerance adjustment; redesign after a validation failure requires a new untouched validation design.

**Why a citation is needed:** This is a strong and appropriate methodological rule, but it invokes the established problem of model-selection bias and validation leakage. A primary methodological reference would distinguish accepted statistical rationale from repository-specific process policy.

**Recommended citation(s):**
- Gavin C. Cawley and Nicola L. C. Talbot, *On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation*, 2010
- Bibliographic key if already present: none
- Status: MISSING FROM BIBLIOGRAPHY
- If missing, complete BibTeX

```bibtex
@article{cawley2010,
  author  = {Cawley, Gavin C. and Talbot, Nicola L. C.},
  title   = {On Over-fitting in Model Selection and Subsequent Selection Bias
             in Performance Evaluation},
  journal = {Journal of Machine Learning Research},
  volume  = {11},
  pages   = {2079--2107},
  year    = {2010},
  url     = {https://www.jmlr.org/papers/v11/cawley10a.html}
}
```

**Priority:** Medium

---

**Location:** `docs/publications/research-monograph/chapters/03-evidence-for-model-adequacy.tex`, approximately lines 257–277, “Provenance and reproducibility.”

**Passage / claim:** Reproducibility is relative to retained identities and declared conditions, with a minimum record including input identities, code and executable versions, settings, commands, environment, checksums, metrics, outcomes, and artifact locations.

**Why a citation is needed:** The precise minimum list may remain project policy, but its framing as reproducible computational research should be connected to established reproducibility guidance. The citation would support the general principle without implying that the external source dictates every project-specific field.

**Recommended citation(s):**
- Geir Kjetil Sandve, Anton Nekrutenko, James Taylor, and Eivind Hovig, *Ten Simple Rules for Reproducible Computational Research*, 2013
- Bibliographic key if already present: none
- Status: MISSING FROM BIBLIOGRAPHY
- If missing, complete BibTeX

```bibtex
@article{sandve2013,
  author  = {Sandve, Geir Kjetil and Nekrutenko, Anton and Taylor, James and
             Hovig, Eivind},
  title   = {Ten Simple Rules for Reproducible Computational Research},
  journal = {PLOS Computational Biology},
  volume  = {9},
  number  = {10},
  pages   = {e1003285},
  year    = {2013},
  doi     = {10.1371/journal.pcbi.1003285},
  url     = {https://doi.org/10.1371/journal.pcbi.1003285}
}
```

**Priority:** Medium

---

**Location:** `docs/publications/research-monograph/chapters/04-bulk-silicon-program.tex`, approximately lines 30–35, “The parent description,” and lines 110–111, “Interpretive limits.”

**Passage / claim:** Kohn–Sham eigenvalues are not the complete many-body excitation spectrum, and a Kohn–Sham band gap is not an exact quasiparticle gap.

**Why a citation is needed:** This is a central scientific limitation of the parent model, not merely a project convention. The nearby Hohenberg–Kohn and Kohn–Sham citations establish DFT and the Kohn–Sham equations, but do not adequately support the specific gap and derivative-discontinuity qualification. Suitable primary references already exist in the bibliography but are not cited at either occurrence.

**Recommended citation(s):**
- John P. Perdew and Mel Levy, *Physical Content of the Exact Kohn–Sham Orbital Energies: Band Gaps and Derivative Discontinuities*, 1983
  - Bibliographic key if already present: `perdewLevy1983`
  - Status: PRESENT IN BIBLIOGRAPHY
- L. J. Sham and M. Schlüter, *Density-Functional Theory of the Energy Gap*, 1983
  - Bibliographic key if already present: `shamSchluter1983`
  - Status: PRESENT IN BIBLIOGRAPHY

**Priority:** High

---

**Location:** `docs/publications/research-monograph/chapters/04-bulk-silicon-program.tex`, approximately line 110, “Interpretive limits.”

**Passage / claim:** “A finite periodic supercell is not an isolated impurity.”

**Why a citation is needed:** The statement is correct but underpins later finite-size and defect-model limitations. A defect-supercell review should support the distinction between an isolated defect and the periodically repeated numerical model. The recommended review is already present in the bibliography.

**Recommended citation(s):**
- Christoph Freysoldt, Blazej Grabowski, Tilmann Hickel, Jörg Neugebauer, Georg Kresse, Anderson Janotti, and Chris G. Van de Walle, *First-Principles Calculations for Point Defects in Solids*, 2014
  - Bibliographic key if already present: `freysoldt2014`
  - Status: PRESENT IN BIBLIOGRAPHY

**Priority:** Medium

---

**Location:** `docs/publications/research-monograph/chapters/05-first-principles-bulk-parent.tex`, approximately lines 38–45, “External-program boundary.”

**Passage / claim:** Quantum ESPRESSO is assigned responsibility for current SCF, NSCF, band-path, and lattice-optimization calculations, with `pw.x` identified as the relevant executable.

**Why a citation is needed:** `giannozzi2009` is a valid foundational citation, but it is weak as the sole reference for a current software boundary and capability statement. The later publisher paper documents the expanded, modern Quantum ESPRESSO suite and is normally cited alongside the 2009 paper. The existing citation should be retained rather than replaced.

**Recommended citation(s):**
- Paolo Giannozzi et al., *Quantum ESPRESSO: A Modular and Open-Source Software Project for Quantum Simulations of Materials*, 2009
  - Bibliographic key if already present: `giannozzi2009`
  - Status: PRESENT IN BIBLIOGRAPHY
- Paolo Giannozzi et al., *Advanced Capabilities for Materials Modelling with Quantum ESPRESSO*, 2017
  - Bibliographic key if already present: none (proposed key: `giannozzi2017`)
  - Status: MISSING FROM BIBLIOGRAPHY
  - If missing, complete BibTeX:

```bibtex
@article{giannozzi2017,
  author  = {Giannozzi, Paolo and others},
  title   = {Advanced Capabilities for Materials Modelling with {Quantum ESPRESSO}},
  journal = {Journal of Physics: Condensed Matter},
  volume  = {29},
  number  = {46},
  pages   = {465901},
  year    = {2017},
  doi     = {10.1088/1361-648X/aa8f79}
}
```

**Priority:** Low

---

**Location:** `docs/publications/research-monograph/chapters/05-first-principles-bulk-parent.tex`, approximately lines 69–72, “Pseudopotential identity.”

**Passage / claim:** PseudoDojo cutoff hints are expressed in Hartree, while Quantum ESPRESSO interprets `ecutwfc` in Rydberg.

**Why a citation is needed:** This exact unit distinction is software- and interface-specific and can cause a factor-of-two input error. The PseudoDojo paper supports the pseudopotential-table context, but the exact `pw.x` input unit should be tied to the official primary software documentation rather than inferred from the general Quantum ESPRESSO journal paper.

**Recommended citation(s):**
- M. J. van Setten et al., *The PseudoDojo: Training and Grading a 85 Element Optimized Norm-Conserving Pseudopotential Table*, 2018
  - Bibliographic key if already present: `vansetten2018`
  - Status: PRESENT IN BIBLIOGRAPHY
- Quantum ESPRESSO Foundation, *pw.x: Input Description*, n.d.
  - Bibliographic key if already present: none (proposed key: `quantumEspressoPwInput`)
  - Status: MISSING FROM BIBLIOGRAPHY
  - If missing, complete BibTeX:

```bibtex
@manual{quantumEspressoPwInput,
  author       = {{Quantum ESPRESSO Foundation}},
  organization = {Quantum ESPRESSO Foundation},
  title        = {{pw.x}: Input Description},
  url          = {https://www.quantum-espresso.org/Doc/INPUT_PW.html},
  note         = {Official online input reference; record the consulted
                  software/documentation version and access date at editorial freeze}
}
```

**Priority:** Medium

---

**Location:** `docs/publications/research-monograph/chapters/06-bulk-representations.tex`, approximately lines 108–128, “Wannier transformation,” especially the equation defining the composite-band Wannier functions.

**Passage / claim:** A composite retained subspace is transformed using a momentum-dependent matrix \(U(\mathbf k)\in U(M)\), and changing that unitary frame changes individual Wannier functions while preserving the subspace projector.

**Why a citation is needed:** `wannier1937` is the correct foundational citation for Wannier functions, but it is not sufficient by itself for the modern composite-band, matrix-valued gauge formulation used in the displayed equation. The primary generalized-Wannier paper should accompany it; the later review already in the bibliography may also be retained for broader context.

**Recommended citation(s):**
- Gregory H. Wannier, *The Structure of Electronic Excitation Levels in Insulating Crystals*, 1937
  - Bibliographic key if already present: `wannier1937`
  - Status: PRESENT IN BIBLIOGRAPHY
- Nicola Marzari and David Vanderbilt, *Maximally Localized Generalized Wannier Functions for Composite Energy Bands*, 1997
  - Bibliographic key if already present: none (proposed key: `marzari1997`)
  - Status: MISSING FROM BIBLIOGRAPHY
  - If missing, complete BibTeX:

```bibtex
@article{marzari1997,
  author  = {Marzari, Nicola and Vanderbilt, David},
  title   = {Maximally Localized Generalized Wannier Functions for Composite
             Energy Bands},
  journal = {Physical Review B},
  volume  = {56},
  number  = {20},
  pages   = {12847--12865},
  year    = {1997},
  doi     = {10.1103/PhysRevB.56.12847}
}
```
- Nicola Marzari, Arash A. Mostofi, Jonathan R. Yates, Ivo Souza, and David Vanderbilt, *Maximally Localized Wannier Functions: Theory and Applications*, 2012
  - Bibliographic key if already present: `marzari2012`
  - Status: PRESENT IN BIBLIOGRAPHY

**Priority:** Medium

---

**Location:** `docs/publications/research-monograph/chapters/06-bulk-representations.tex`, approximately lines 130–137, “Wannier transformation.”

**Passage / claim:** In the PAW formalism, transformation from auxiliary states to all-electron states contributes augmentation terms to Wannier overlap matrix elements.

**Why a citation is needed:** `rostgaard2009` directly addresses the asserted derivation, so the citation is not incorrect. It is, however, a non-peer-reviewed technical report and is weak as the sole authority for the underlying PAW transformation. Pairing it with Blöchl’s primary, peer-reviewed PAW paper would distinguish support for the PAW formalism from support for the specialized Wannier-overlap derivation.

**Recommended citation(s):**
- Carsten Rostgaard, *The Projector Augmented-Wave Method*, 2009
  - Bibliographic key if already present: `rostgaard2009`
  - Status: PRESENT IN BIBLIOGRAPHY
- Peter E. Blöchl, *Projector Augmented-Wave Method*, 1994
  - Bibliographic key if already present: `blochl1994paw`
  - Status: PRESENT IN BIBLIOGRAPHY

**Priority:** Low

---

**Location:** `docs/publications/research-monograph/chapters/06-bulk-representations.tex`, approximately lines 144–146, “Localization.”

**Passage / claim:** “Spatial localization depends on the regularity of the selected Bloch frame over the Brillouin zone.”

**Why a citation is needed:** `kohn1959` is foundational but has narrower historical scope than the surrounding three-dimensional, composite-subspace discussion. A modern primary result treating exponential localization and the associated topological conditions in higher-dimensional insulators would prevent the sentence from appearing to extend Kohn’s result without qualification.

**Recommended citation(s):**
- Walter Kohn, *Analytic Properties of Bloch Waves and Wannier Functions*, 1959
  - Bibliographic key if already present: `kohn1959`
  - Status: PRESENT IN BIBLIOGRAPHY
- Christian Brouder, Gianluca Panati, Matteo Calandra, Christophe Mourougane, and Nicola Marzari, *Exponential Localization of Wannier Functions in Insulators*, 2007
  - Bibliographic key if already present: none (proposed key: `brouder2007`)
  - Status: MISSING FROM BIBLIOGRAPHY
  - If missing, complete BibTeX:

```bibtex
@article{brouder2007,
  author  = {Brouder, Christian and Panati, Gianluca and Calandra, Matteo and
             Mourougane, Christophe and Marzari, Nicola},
  title   = {Exponential Localization of Wannier Functions in Insulators},
  journal = {Physical Review Letters},
  volume  = {98},
  number  = {4},
  pages   = {046402},
  year    = {2007},
  doi     = {10.1103/PhysRevLett.98.046402}
}
```

**Priority:** Medium

---

**Location:** `docs/publications/research-monograph/chapters/06-bulk-representations.tex`, approximately lines 266–269, “Subspace diagnostics,” immediately after the principal-angle equation.

**Passage / claim:** A “polar or orthogonal-Procrustes construction” can supply a unitary coordinate identification.

**Why a citation is needed:** `higham1986` appropriately supports computation of the polar decomposition, but it is not the primary source for the orthogonal Procrustes problem named in the same claim. The Procrustes-specific statement should have its own primary reference.

**Recommended citation(s):**
- Nicholas J. Higham, *Computing the Polar Decomposition—with Applications*, 1986
  - Bibliographic key if already present: `higham1986`
  - Status: PRESENT IN BIBLIOGRAPHY
- Peter H. Schönemann, *A Generalized Solution of the Orthogonal Procrustes Problem*, 1966
  - Bibliographic key if already present: none (proposed key: `schonemann1966`)
  - Status: MISSING FROM BIBLIOGRAPHY
  - If missing, complete BibTeX:

```bibtex
@article{schonemann1966,
  author  = {Sch{\"o}nemann, Peter H.},
  title   = {A Generalized Solution of the Orthogonal Procrustes Problem},
  journal = {Psychometrika},
  volume  = {31},
  number  = {1},
  pages   = {1--10},
  year    = {1966},
  doi     = {10.1007/BF02289451}
}
```

**Priority:** Medium

---

**Location:** `docs/publications/research-monograph/chapters/09-doped-silicon-program.tex`, approximately lines 56–58, Section “Substitutional phosphorus”

**Passage / claim:** “Each finite supercell represents a periodic dopant array. An isolated-donor interpretation requires supercell-size evidence rather than the presence of a single substituted atom in the simulation cell.”

**Why a citation is needed:** This is an established methodological limitation of periodic point-defect supercell calculations, not merely a project convention. An authoritative defect-calculation review should support the finite-size and periodic-image warning.

**Recommended citation(s):**
- Christoph Freysoldt, Blazej Grabowski, Tilmann Hickel, Jörg Neugebauer, Georg Kresse, Anderson Janotti, and Chris G. Van de Walle, *First-Principles Calculations for Point Defects in Solids*, 2014
- Bibliographic key if already present: `freysoldt2014`
- Status: PRESENT IN BIBLIOGRAPHY

**Priority:** Medium

---

**Location:** `docs/publications/research-monograph/chapters/09-doped-silicon-program.tex`, approximately lines 66–78, Section “Substitutional boron”

**Passage / claim:** The boron branch is treated as an acceptor problem whose final continuum treatment must preserve the spin–orbit-coupled valence manifold.

**Why a citation is needed:** The exact computational branch is an internal specification, but its physical motivation—the multicomponent, spin–orbit-coupled valence-band structure of shallow acceptors—should be tied to the foundational acceptor literature. The recommended source supports that background; it should not be represented as independently mandating this project’s precise DFT implementation.

**Recommended citation(s):**
- Alfonso Baldereschi and Nunzio O. Lipari, *Spherical Model of Shallow Acceptor States in Semiconductors*, 1973
- Bibliographic key if already present: none
- Status: MISSING FROM BIBLIOGRAPHY
- If missing, complete BibTeX

```bibtex
@article{baldereschiLipari1973,
  author  = {Baldereschi, A. and Lipari, N. O.},
  title   = {Spherical Model of Shallow Acceptor States in Semiconductors},
  journal = {Physical Review B},
  volume  = {8},
  pages   = {2697--2709},
  year    = {1973},
  doi     = {10.1103/PhysRevB.8.2697}
}
```

**Priority:** Medium

---

**Location:** `docs/publications/research-monograph/chapters/09-doped-silicon-program.tex`, approximately lines 94–99, Section “Interpretive limits”

**Passage / claim:** “A Kohn--Sham band gap is not an exact quasiparticle gap.”

**Why a citation is needed:** This is a substantive statement about the interpretation of Kohn–Sham eigenvalue gaps and the derivative discontinuity. The bibliography already contains the two primary 1983 papers normally used to support it.

**Recommended citation(s):**
- John P. Perdew and Mel Levy, *Physical Content of the Exact Kohn–Sham Orbital Energies: Band Gaps and Derivative Discontinuities*, 1983
- Bibliographic key if already present: `perdewLevy1983`
- Status: PRESENT IN BIBLIOGRAPHY
- L. J. Sham and M. Schlüter, *Density-Functional Theory of the Energy Gap*, 1983
- Bibliographic key if already present: `shamSchluter1983`
- Status: PRESENT IN BIBLIOGRAPHY

**Priority:** High

---

**Location:** `docs/publications/research-monograph/chapters/12-continuum-effective-mass.tex`, approximately lines 16–20, Section “Continuum effective-mass reduction”

**Passage / claim:** The continuum stage uses a multivalley donor solver for phosphorus, a multiband acceptor solver for boron, and screened-Coulomb and central-cell impurity model families.

**Why a citation is needed:** These are material-specific descendants of established envelope-function, silicon-donor, and shallow-acceptor theories. The project-specific solver and model-selection contracts remain proposed work, but the physical model classes require foundational attribution.

**Recommended citation(s):**
- J. M. Luttinger and Walter Kohn, *Motion of Electrons and Holes in Perturbed Periodic Fields*, 1955
- Bibliographic key if already present: `luttingerKohn1955`
- Status: PRESENT IN BIBLIOGRAPHY
- Walter Kohn and J. M. Luttinger, *Theory of Donor States in Silicon*, 1955
- Bibliographic key if already present: none
- Status: MISSING FROM BIBLIOGRAPHY
- If missing, complete BibTeX

```bibtex
@article{kohnLuttinger1955donor,
  author  = {Kohn, Walter and Luttinger, J. M.},
  title   = {Theory of Donor States in Silicon},
  journal = {Physical Review},
  volume  = {98},
  pages   = {915--922},
  year    = {1955},
  doi     = {10.1103/PhysRev.98.915}
}
```

- Alfonso Baldereschi and Nunzio O. Lipari, *Spherical Model of Shallow Acceptor States in Semiconductors*, 1973
- Bibliographic key if already present: none
- Status: MISSING FROM BIBLIOGRAPHY
- If missing, complete BibTeX

```bibtex
@article{baldereschiLipari1973,
  author  = {Baldereschi, A. and Lipari, N. O.},
  title   = {Spherical Model of Shallow Acceptor States in Semiconductors},
  journal = {Physical Review B},
  volume  = {8},
  pages   = {2697--2709},
  year    = {1973},
  doi     = {10.1103/PhysRevB.8.2697}
}
```

**Priority:** High

---

**Location:** `docs/publications/research-monograph/chapters/13-structured-learning.tex`, approximately lines 10–14, opening discussion

**Passage / claim:** “Kohn--Sham DFT supplies a parent one-particle operator.”

**Why a citation is needed:** This invokes a named foundational formalism. Although DFT is presumably introduced earlier in the monograph, local attribution here would make the structured-learning chapter’s parent-model premise traceable.

**Recommended citation(s):**
- Walter Kohn and Lu Jeu Sham, *Self-Consistent Equations Including Exchange and Correlation Effects*, 1965
- Bibliographic key if already present: `kohn1965`
- Status: PRESENT IN BIBLIOGRAPHY

**Priority:** Low

---

**Location:** `docs/publications/research-monograph/chapters/13-structured-learning.tex`, approximately lines 206–215, Section “A learned reference for the continuum crossover,” unnumbered screened-Coulomb equation

**Passage / claim:** A screened Coulomb donor term is assigned the asymptotic form
\(V_{\rm EMT}(r)\sim-e^2/(4\pi\epsilon_0\epsilon_r r)\).

**Why a citation is needed:** The electrostatic expression is standard, but its use as the asymptotic impurity term in silicon multivalley donor effective-mass theory is a specific physical-model claim. The classic silicon-donor source directly anchors that context.

**Recommended citation(s):**
- Walter Kohn and J. M. Luttinger, *Theory of Donor States in Silicon*, 1955
- Bibliographic key if already present: none
- Status: MISSING FROM BIBLIOGRAPHY
- If missing, complete BibTeX

```bibtex
@article{kohnLuttinger1955donor,
  author  = {Kohn, Walter and Luttinger, J. M.},
  title   = {Theory of Donor States in Silicon},
  journal = {Physical Review},
  volume  = {98},
  pages   = {915--922},
  year    = {1955},
  doi     = {10.1103/PhysRev.98.915}
}
```

**Priority:** High

---

**Location:** `docs/publications/research-monograph/chapters/13-structured-learning.tex`, approximately lines 402–406, Section “A staged computational progression,” Level 1

**Passage / claim:** “Use fixed stencils or a linear Slater--Koster or tight-binding parameterization…”

**Why a citation is needed:** Slater–Koster is a named parameterization and should cite its primary source. The appropriate entry is already present.

**Recommended citation(s):**
- J. C. Slater and G. F. Koster, *Simplified LCAO Method for the Periodic Potential Problem*, 1954
- Bibliographic key if already present: `slater1954`
- Status: PRESENT IN BIBLIOGRAPHY

**Priority:** Medium

---

**Location:** `docs/publications/research-monograph/chapters/15-current-evidence-boundary.tex`, approximately lines 100–106, Section “Direct PBE bootstrap observations”

**Passage / claim:** “A separately retained PBE/PseudoDojo bootstrap campaign executed nine SCF and nine linked NSCF Quantum ESPRESSO invocations.”

**Why a citation is needed:** Internal records must substantiate the execution count and outcomes, but the named exchange-correlation approximation, pseudopotential library, and electronic-structure software also require their standard scholarly citations. These references establish the methods and software, not the claimed execution history.

**Recommended citation(s):**
- John P. Perdew, Kieron Burke, and Matthias Ernzerhof, *Generalized Gradient Approximation Made Simple*, 1996
- Bibliographic key if already present: `perdew1996`
- Status: PRESENT IN BIBLIOGRAPHY
- M. J. van Setten et al., *The PseudoDojo: Training and Grading a 85 Element Optimized Norm-Conserving Pseudopotential Table*, 2018
- Bibliographic key if already present: `vansetten2018`
- Status: PRESENT IN BIBLIOGRAPHY
- Paolo Giannozzi et al., *QUANTUM ESPRESSO: A Modular and Open-Source Software Project for Quantum Simulations of Materials*, 2009
- Bibliographic key if already present: `giannozzi2009`
- Status: PRESENT IN BIBLIOGRAPHY

**Priority:** High

---

**Location:** `docs/publications/research-monograph/chapters/15-current-evidence-boundary.tex`, approximately lines 151–156, Section “Present limitations,” Subsection “Parent calculation”

**Passage / claim:** “The selected PBE parent will also retain parent-model limitations relative to experiment even after numerical convergence.”

**Why a citation is needed:** This externally testable statement is too broad without identifying the affected observable. If it refers to the electronic gap discussed elsewhere, the derivative-discontinuity literature supports a narrowed claim. Those papers do not substantiate every possible PBE-versus-experiment discrepancy, so the sentence should not use them to imply a universal limitation.

**Recommended citation(s):**
- John P. Perdew and Mel Levy, *Physical Content of the Exact Kohn–Sham Orbital Energies: Band Gaps and Derivative Discontinuities*, 1983
- Bibliographic key if already present: `perdewLevy1983`
- Status: PRESENT IN BIBLIOGRAPHY
- L. J. Sham and M. Schlüter, *Density-Functional Theory of the Energy Gap*, 1983
- Bibliographic key if already present: `shamSchluter1983`
- Status: PRESENT IN BIBLIOGRAPHY

**Priority:** Medium

---

**Location:** `chapters/16-proof-architecture.tex`, §“Proof-package graph,” lines 44–46; `chapters/17-finite-dimensional-foundations.tex`, §“Finite-dimensional retained frames,” lines 43–47; and `chapters/19-mechanization-status.tex`, §“Mechanization status,” lines 10–12 and 24–40.

**Passage / claim:** The proof program is targeted independently in Lean, Isabelle, and Rocq; the checked trial specifically uses Lean 4 and mathlib.

**Why a citation is needed:** These systems and the mathematical library are central research infrastructure in this part of the monograph, but none has a scholarly system citation. Such citations identify the systems and their proof foundations. They would not, by themselves, substantiate the repository-specific claims that a target is checked or unencoded; those claims still require internal provenance.

**Recommended citation(s):**
- Leonardo de Moura and Sebastian Ullrich, “The Lean 4 Theorem Prover and Programming Language,” 2021
- Bibliographic key if already present: not present; proposed key: `demouraUllrich2021`
- Status: MISSING FROM BIBLIOGRAPHY
- If missing, complete BibTeX

```bibtex
@inproceedings{demouraUllrich2021,
  author    = {de Moura, Leonardo and Ullrich, Sebastian},
  title     = {The {Lean 4} Theorem Prover and Programming Language},
  booktitle = {Automated Deduction---CADE 28},
  series    = {Lecture Notes in Computer Science},
  volume    = {12699},
  pages     = {625--635},
  publisher = {Springer},
  address   = {Cham},
  year      = {2021},
  doi       = {10.1007/978-3-030-79876-5_37}
}
```

- The mathlib Community, “The Lean Mathematical Library,” 2020
- Bibliographic key if already present: not present; proposed key: `mathlib2020`
- Status: MISSING FROM BIBLIOGRAPHY
- If missing, complete BibTeX

```bibtex
@inproceedings{mathlib2020,
  author    = {{The mathlib Community}},
  title     = {The {Lean} Mathematical Library},
  booktitle = {Proceedings of the 9th ACM SIGPLAN International Conference on Certified Programs and Proofs},
  pages     = {367--381},
  publisher = {Association for Computing Machinery},
  address   = {New York, NY, USA},
  year      = {2020},
  doi       = {10.1145/3372885.3373824}
}
```

- Tobias Nipkow, Lawrence C. Paulson, and Markus Wenzel, *Isabelle/HOL: A Proof Assistant for Higher-Order Logic*, 2002
- Bibliographic key if already present: not present; proposed key: `nipkowPaulsonWenzel2002`
- Status: MISSING FROM BIBLIOGRAPHY
- If missing, complete BibTeX

```bibtex
@book{nipkowPaulsonWenzel2002,
  author    = {Nipkow, Tobias and Paulson, Lawrence C. and Wenzel, Markus},
  title     = {{Isabelle/HOL}: A Proof Assistant for Higher-Order Logic},
  series    = {Lecture Notes in Computer Science},
  volume    = {2283},
  publisher = {Springer},
  address   = {Berlin and Heidelberg},
  year      = {2002},
  doi       = {10.1007/3-540-45949-9}
}
```

- Yves Bertot and Pierre Castéran, *Interactive Theorem Proving and Program Development: Coq’Art: The Calculus of Inductive Constructions*, 2004
- Bibliographic key if already present: not present; proposed key: `bertotCasteran2004`
- Status: MISSING FROM BIBLIOGRAPHY
- If missing, complete BibTeX

```bibtex
@book{bertotCasteran2004,
  author    = {Bertot, Yves and Cast{\'e}ran, Pierre},
  title     = {Interactive Theorem Proving and Program Development:
               {Coq'Art}: The Calculus of Inductive Constructions},
  series    = {Texts in Theoretical Computer Science. An EATCS Series},
  publisher = {Springer},
  address   = {Berlin and Heidelberg},
  year      = {2004},
  doi       = {10.1007/978-3-662-07964-5}
}
```

**Priority:** Medium

---

**Location:** `chapters/18-mathematics-of-reduction.tex`, §“Crossover and operator-to-observable bounds,” lines 66–70, following the definition of $r_{c,d}(\tau)$.

**Passage / claim:** “The assumption $\eta_d(R)\to0$ as $R\to\infty$ is an asymptotic-locality hypothesis, not a consequence established by general Kohn--Sham DFT.”

**Why a citation is needed:** This is an important scientific scope claim about what general Kohn–Sham DFT does not establish. It should be placed against the primary literature on nearsightedness, which proves or motivates locality only for particular quantities and under conditions that do not automatically imply decay of the defined atomistic-minus-continuum discrepancy. The citation should accompany the existing cautious wording, not be presented as a proof of that negative claim.

**Recommended citation(s):**
- Emil Prodan and Walter Kohn, “Nearsightedness of Electronic Matter,” 2005
- Bibliographic key if already present: not present; proposed key: `prodanKohn2005`
- Status: MISSING FROM BIBLIOGRAPHY
- If missing, complete BibTeX

```bibtex
@article{prodanKohn2005,
  author  = {Prodan, Emil and Kohn, Walter},
  title   = {Nearsightedness of Electronic Matter},
  journal = {Proceedings of the National Academy of Sciences},
  volume  = {102},
  number  = {33},
  pages   = {11635--11638},
  year    = {2005},
  doi     = {10.1073/pnas.0505436102}
}
```

**Priority:** High

---

**Location:** `chapters/18-mathematics-of-reduction.tex`, §“Crossover and operator-to-observable bounds,” lines 72–79, immediately before and alongside the `davis1970` citation.

**Passage / claim:** “Standard perturbation theory motivates spectral-distance bounds controlled by $\|E\|$. Invariant-subspace rotation can be controlled by a Davis--Kahan-type estimate…”

**Why a citation is needed:** `davis1970` correctly supports the invariant-subspace rotation statement, but it is not an adequate general citation for the preceding, broader claim about spectral variation for self-adjoint operators. A standard operator-perturbation source should be added, particularly because the text explicitly leaves the finite- versus infinite-dimensional setting to the proposed proof obligation.

**Recommended citation(s):**
- Tosio Kato, *Perturbation Theory for Linear Operators*, 1995
- Bibliographic key if already present: not present; proposed key: `kato1995`
- Status: MISSING FROM BIBLIOGRAPHY
- If missing, complete BibTeX

```bibtex
@book{kato1995,
  author    = {Kato, Tosio},
  title     = {Perturbation Theory for Linear Operators},
  edition   = {2},
  series    = {Classics in Mathematics},
  publisher = {Springer},
  address   = {Berlin and Heidelberg},
  year      = {1995},
  doi       = {10.1007/978-3-642-66282-9}
}
```

**Priority:** Medium

---

**Location:** `chapters/18-mathematics-of-reduction.tex`, §“Compatibility and certified incompatibility,” lines 121–125.

**Passage / claim:** Certification requires a valid global lower bound, potentially obtained from “analytic estimates, interval methods, branch-and-bound, exhaustive certified reduction, or an applicable validated convex relaxation.”

**Why a citation is needed:** The logical point that failure of a local optimizer is not a global certificate is sound, but the subsequent list invokes established validated-global-optimization methodologies without a source. A primary review covering complete search, interval bounds, branch-and-bound, and constraint-based certification would ground these examples. It should not be read as asserting that every listed technique is already applicable to this project’s model space.

**Recommended citation(s):**
- Arnold Neumaier, “Complete Search in Continuous Global Optimization and Constraint Satisfaction,” 2004
- Bibliographic key if already present: not present; proposed key: `neumaier2004`
- Status: MISSING FROM BIBLIOGRAPHY
- If missing, complete BibTeX

```bibtex
@article{neumaier2004,
  author  = {Neumaier, Arnold},
  title   = {Complete Search in Continuous Global Optimization and Constraint Satisfaction},
  journal = {Acta Numerica},
  volume  = {13},
  pages   = {271--369},
  year    = {2004},
  doi     = {10.1017/S0962492904000194}
}
```

**Priority:** Medium

---

**Location:** `docs/publications/research-monograph/appendices/A-notation-and-status.tex`, approximately line 159, section “Excluded-space and continuum notation,” definition of \(H_{\mathrm{eff}}(E)\).

**Passage / claim:** “Energy-dependent Feshbach effective operator in the retained \(P\) space.”

**Why a citation is needed:** This invokes an eponymous projection-operator construction rather than defining purely monograph-specific notation. A citation to Feshbach’s primary work would establish the origin and intended meaning of the term.

**Recommended citation(s):**
- Herman Feshbach, “Unified Theory of Nuclear Reactions,” 1958
- Bibliographic key if already present: `feshbach1958`
- Status: PRESENT IN BIBLIOGRAPHY

**Priority:** Low

---

**Location:** `docs/publications/research-monograph/appendices/B-hilbert-schmidt-and-frobenius.tex`, approximately lines 216–234, section “Domains and the particle in a box,” including the displayed domain \(H^2(0,L)\cap H_0^1(0,L)\).

**Passage / claim:** A differential expression does not alone specify a quantum operator; the real-line kinetic operator and finite-interval Dirichlet realization are different operators because their domains differ.

**Why a citation is needed:** Operator domains and self-adjoint realizations are central, non-elementary premises of the appendix’s interpretation of particle-in-a-box residuals. The parallel discussion in Appendix C is cited, but this standalone section is not.

**Recommended citation(s):**
- Gerald Teschl, *Mathematical Methods in Quantum Mechanics: With Applications to Schrödinger Operators*, 2014
- Bibliographic key if already present: `teschl2014`
- Status: PRESENT IN BIBLIOGRAPHY

**Priority:** Medium

---

**Location:** `docs/publications/research-monograph/appendices/B-hilbert-schmidt-and-frobenius.tex`, approximately lines 256–277, section “Infinite-dimensional qualification,” definition of \(\mathcal L_2(\mathcal H)\).

**Passage / claim:** The bounded operators on an infinite-dimensional Hilbert space do not form a Hilbert space under the Hilbert–Schmidt inner product; one instead uses the Hilbert–Schmidt class, and finite-rank operators belong to that class.

**Why a citation is needed:** This is a substantive operator-ideal result rather than an elementary finite-matrix identity. Appendix C cites Simon for the same qualification, so the uncited presentation here should use the same authoritative source.

**Recommended citation(s):**
- Barry Simon, *Trace Ideals and Their Applications*, 2005
- Bibliographic key if already present: `simon2005`
- Status: PRESENT IN BIBLIOGRAPHY

**Priority:** Medium

---

**Location:** `docs/publications/research-monograph/appendices/C-operator-spaces-compression-alignment.tex`, approximately lines 130–140, section “Compression and downfolding,” displayed equation defining \(\hat H_{\mathrm{down}}(E)\).

**Passage / claim:** “A Feshbach–Löwdin construction gives the energy-dependent operator … whenever the reduced resolvent exists,” currently cited only to `lowdin1982`.

**Why a citation is needed:** The existing Löwdin citation is relevant and should remain, but it only partially supports the compound “Feshbach–Löwdin” attribution. Adding Feshbach’s primary projection-formalism paper would make the attribution complete. This is a weak-justification issue, not an incorrect citation.

**Recommended citation(s):**
- Herman Feshbach, “Unified Theory of Nuclear Reactions,” 1958
- Bibliographic key if already present: `feshbach1958`
- Status: PRESENT IN BIBLIOGRAPHY

**Priority:** Low

---

**Location:** `docs/publications/research-monograph/appendices/E-harmonic-oscillator-comparison.tex`, approximately lines 15–31 and 48–112, sections “Question addressed by the experiment” and “Exact retained ladder Hamiltonian,” including the equations for \(\hat H_{\mathrm{QHO}}\), ladder-state actions, \(E_n\), and the finite-ladder commutator.

**Passage / claim:** The exact one-dimensional harmonic-oscillator ladder representation, oscillator length, number-state actions, energy spectrum, and its retained finite-dimensional restriction.

**Why a citation is needed:** These equations provide the external textbook foundation for the proposed experiment and its reference operator. Appendix E currently contains no external citations at all. Although standard, the collection should be anchored to a recognized quantum-mechanics source.

**Recommended citation(s):**
- Ramamurti Shankar, *Principles of Quantum Mechanics*, 1994
- Bibliographic key if already present: `shankar1994`
- Status: PRESENT IN BIBLIOGRAPHY

**Priority:** Medium

---

**Location:** `docs/publications/research-monograph/appendices/E-harmonic-oscillator-comparison.tex`, approximately lines 196–210, section “Map from ladder states to a spatial representation,” equation defining \(\mathbf J_{X,h}^{(K)}=\mathbf S_{X,h}^{(K)}(\mathbf G_{X,h}^{(K)})^{-1/2}\).

**Passage / claim:** The inverse-square-root construction is described as a “symmetrically orthonormalized injection” and asserted to produce orthonormal columns.

**Why a citation is needed:** The identity is directly checkable, but the construction is a recognized polar/inverse-square-root orthonormalization method whose numerical interpretation depends on positive definiteness and conditioning. A primary numerical linear-algebra reference would provide method provenance.

**Recommended citation(s):**
- Nicholas J. Higham, “Computing the Polar Decomposition—with Applications,” 1986
- Bibliographic key if already present: `higham1986`
- Status: PRESENT IN BIBLIOGRAPHY

**Priority:** Low

---

**Location:** `docs/publications/research-monograph/appendices/F-bulk-silicon-reduction-routes.tex`, approximately lines 57–145, especially section “From the retained KS operator to a Wannier representation,” equations defining \(\mathbf J_{\mathrm W}\), \(\mathbf H_{\mathrm W}(\mathbf k)\), and \(\mathbf H_{\mathrm W}(\mathbf R)\).

**Passage / claim:** Disentanglement selects a retained subspace; localization selects a gauge within that subspace; localization alone does not discard rank or hopping blocks; real-space truncation is a separate approximation.

**Why a citation is needed:** These are established and important distinctions from modern Wannier theory, not merely notation introduced by the appendix. Appendix F currently has no citations at all. The existing review and primary disentanglement paper directly support the claims.

**Recommended citation(s):**
- Nicola Marzari, Arash A. Mostofi, Jonathan R. Yates, Ivo Souza, and David Vanderbilt, “Maximally Localized Wannier Functions: Theory and Applications,” 2012
- Bibliographic key if already present: `marzari2012`
- Status: PRESENT IN BIBLIOGRAPHY

- Ivo Souza, Nicola Marzari, and David Vanderbilt, “Maximally Localized Wannier Functions for Entangled Energy Bands,” 2001
- Bibliographic key if already present: `souza2001`
- Status: PRESENT IN BIBLIOGRAPHY

**Priority:** Medium

---

**Location:** `docs/publications/research-monograph/appendices/F-bulk-silicon-reduction-routes.tex`, approximately lines 18, 147–173, 405–406, and 448–466; section “Tight-binding model class” and the proposed bulk experiment.

**Passage / claim:** The target is an orthogonal \(sp^3s^\ast\) silicon tight-binding hierarchy whose model class includes a declared Slater–Koster structure and neighbor-shell restrictions.

**Why a citation is needed:** “Slater–Koster” and the semiconductor \(sp^3s^\ast\) construction refer to identifiable historical model frameworks. Citing their foundational sources would establish what scientific model lineage the proposed hierarchy invokes without implying that any particular published parameter set has been adopted.

**Recommended citation(s):**
- J. C. Slater and G. F. Koster, “Simplified LCAO Method for the Periodic Potential Problem,” 1954
- Bibliographic key if already present: `slater1954`
- Status: PRESENT IN BIBLIOGRAPHY

- P. Vogl, H. P. Hjalmarson, and J. D. Dow, “A Semi-Empirical Tight-Binding Theory of the Electronic Structure of Semiconductors,” 1983
- Bibliographic key if already present: `vogl1983`
- Status: PRESENT IN BIBLIOGRAPHY

**Priority:** Medium

---

**Location:** `docs/publications/research-monograph/appendices/G-one-dimensional-reduction.tex`, approximately lines 307–351, section “Mathieu and Floquet formulation,” equations defining \(A\), \(q\), and the Floquet exponent \(\nu\).

**Passage / claim:** The cosine Schrödinger problem is converted to the Mathieu equation, Bloch periodicity becomes a Floquet condition, and Mathieu characteristic values can provide an independent reference for selected bands.

**Why a citation is needed:** The algebraic substitution is shown, but the named Mathieu/Floquet theory and use of characteristic-value branches as reference data require a source documenting their conventions. This is especially important because the text correctly warns that branch ordering and characteristic-value conventions differ.

**Recommended citation(s):**
- N. W. McLachlan, *Theory and Application of Mathieu Functions*, 1947
- Status: MISSING FROM BIBLIOGRAPHY
- If missing, complete BibTeX

```bibtex
@book{mclachlan1947,
  author    = {McLachlan, N. W.},
  title     = {Theory and Application of Mathieu Functions},
  publisher = {Clarendon Press},
  address   = {Oxford},
  year      = {1947}
}
```

**Priority:** Medium

---

**Location:** `docs/publications/research-monograph/appendices/H-two-dimensional-wannier-reduction.tex`, approximately lines 355–390, section “Direct two-dimensional gauge construction.”

**Passage / claim:** Polar or singular-value decompositions provide neighboring unitary transport maps; overlap singular values diagnose subspace mismatch; Wilson loops around reciprocal cycles and plaquettes diagnose closure holonomy; locally optimal rotations need not give a globally periodic localized frame.

**Why a citation is needed:** This paragraph presents a recognizable gauge-transport methodology and numerical matrix construction. The existing bibliography already contains appropriate sources, but neither is cited here.

**Recommended citation(s):**
- Nicola Marzari, Arash A. Mostofi, Jonathan R. Yates, Ivo Souza, and David Vanderbilt, “Maximally Localized Wannier Functions: Theory and Applications,” 2012
- Bibliographic key if already present: `marzari2012`
- Status: PRESENT IN BIBLIOGRAPHY

- Nicholas J. Higham, “Computing the Polar Decomposition—with Applications,” 1986
- Bibliographic key if already present: `higham1986`
- Status: PRESENT IN BIBLIOGRAPHY

**Priority:** Medium

---

**Location:** `docs/publications/research-monograph/appendices/H-two-dimensional-wannier-reduction.tex`, approximately lines 393–416, section “Topology and the localization boundary,” especially the displayed Chern-number equation and the following paragraph.

**Passage / claim:** A nonzero first Chern number obstructs a globally smooth periodic frame and a complete set of exponentially localized Wannier functions spanning the retained subspace.

**Why a citation is needed:** This is a substantive mathematical theorem central to the appendix’s stopping condition. It should be supported by a primary proof rather than left uncited.

**Recommended citation(s):**
- Christian Brouder, Gianluca Panati, Matteo Calandra, Christophe Mourougane, and Nicola Marzari, “Exponential Localization of Wannier Functions in Insulators,” 2007
- Status: MISSING FROM BIBLIOGRAPHY
- If missing, complete BibTeX

```bibtex
@article{brouder2007,
  author  = {Brouder, Christian and Panati, Gianluca and Calandra, Matteo and
             Mourougane, Christophe and Marzari, Nicola},
  title   = {Exponential Localization of Wannier Functions in Insulators},
  journal = {Physical Review Letters},
  volume  = {98},
  number  = {4},
  pages   = {046402},
  year    = {2007},
  doi     = {10.1103/PhysRevLett.98.046402}
}
```

**Priority:** High

---

**Location:** `docs/publications/research-monograph/appendices/I-impurity-effective-mass-models.tex`, approximately lines 22–27, section “Physical objective.”

**Passage / claim:** “The parent description is a self-consistent Kohn–Sham calculation in the Born–Oppenheimer fixed-ion framework~\cite{hohenberg1964,kohn1965}.”

**Why a citation is needed:** The existing Hohenberg–Kohn and Kohn–Sham papers correctly support density-functional and Kohn–Sham theory, but they are weakly justified as support for the separate Born–Oppenheimer attribution. Either the citation placement should make clear that they support “Kohn–Sham,” or a source for the Born–Oppenheimer approximation should be added.

**Recommended citation(s):**
- Max Born and Robert Oppenheimer, “Zur Quantentheorie der Molekeln,” 1927
- Status: MISSING FROM BIBLIOGRAPHY
- If missing, complete BibTeX

```bibtex
@article{bornOppenheimer1927,
  author  = {Born, Max and Oppenheimer, Robert},
  title   = {Zur Quantentheorie der Molekeln},
  journal = {Annalen der Physik},
  volume  = {389},
  number  = {20},
  pages   = {457--484},
  year    = {1927},
  doi     = {10.1002/andp.19273892002}
}
```

- Pierre Hohenberg and Walter Kohn, “Inhomogeneous Electron Gas,” 1964
- Bibliographic key if already present: `hohenberg1964`
- Status: PRESENT IN BIBLIOGRAPHY

- Walter Kohn and Lu Jeu Sham, “Self-Consistent Equations Including Exchange and Correlation Effects,” 1965
- Bibliographic key if already present: `kohn1965`
- Status: PRESENT IN BIBLIOGRAPHY

**Priority:** Medium

---

**Location:** `docs/publications/research-monograph/appendices/I-impurity-effective-mass-models.tex`, approximately lines 76–87, section “Pristine silicon reference.”

**Passage / claim:** The bulk pilot compares a silicon band-edge subspace with a constrained orthogonal \(sp^3s^\ast\) Slater–Koster hierarchy.

**Why a citation is needed:** This invokes two established model constructions but supplies no citation. The references would identify the intended historical framework while leaving the appendix’s own model-class restrictions authoritative.

**Recommended citation(s):**
- J. C. Slater and G. F. Koster, “Simplified LCAO Method for the Periodic Potential Problem,” 1954
- Bibliographic key if already present: `slater1954`
- Status: PRESENT IN BIBLIOGRAPHY

- P. Vogl, H. P. Hjalmarson, and J. D. Dow, “A Semi-Empirical Tight-Binding Theory of the Electronic Structure of Semiconductors,” 1983
- Bibliographic key if already present: `vogl1983`
- Status: PRESENT IN BIBLIOGRAPHY

**Priority:** Medium

---

**Location:** `docs/publications/research-monograph/appendices/I-impurity-effective-mass-models.tex`, approximately lines 353–373, section “Dopant branches and validation.”

**Passage / claim:** The phosphorus and boron neutral-supercell branches have different electron counts and spin requirements; final boron acceptor and valence-manifold claims require spin–orbit-coupled spinor treatment; finite supercells represent periodic dopant arrays, so isolated-dopant conclusions require size and shape convergence.

**Why a citation is needed:** The electron counts follow from the declared substitutions, but the importance of the spin–orbit-coupled silicon valence manifold and the finite-supercell limitation are external semiconductor and defect-methodology claims. The references currently appear only for the subsequent charged-defect sentence, leaving the broader claims unsupported.

**Recommended citation(s):**
- J. M. Luttinger and W. Kohn, “Motion of Electrons and Holes in Perturbed Periodic Fields,” 1955
- Bibliographic key if already present: `luttingerKohn1955`
- Status: PRESENT IN BIBLIOGRAPHY

- Peter Y. Yu and Manuel Cardona, *Fundamentals of Semiconductors: Physics and Materials Properties*, 2010
- Bibliographic key if already present: `yuCardona2010`
- Status: PRESENT IN BIBLIOGRAPHY

- Christoph Freysoldt, Blazej Grabowski, Tilmann Hickel, Jörg Neugebauer, Georg Kresse, Anderson Janotti, and Chris G. Van de Walle, “First-Principles Calculations for Point Defects in Solids,” 2014
- Bibliographic key if already present: `freysoldt2014`
- Status: PRESENT IN BIBLIOGRAPHY

**Priority:** Medium


## Summary

- **Total locations flagged:** 47
- **Priority:** 12 high, 28 medium, 7 low
- **Existing citation keys checked at audit time:** 45 unique keys
- **Prospective bibliography entries added after the audit:** 21 unique entries
- **Conclusive incorrect existing citations:** 0
- **Existing citations needing stronger attachment or supplementation:** 6 locations

### Prospectively added bibliography entries

The complete provisional BibTeX for each entry appears in the applicable
finding above. Each requires source and metadata verification before the
editorial note is resolved.

1. `hilbert1902`
2. `nationalResearchCouncil2012`
3. `paier2006`
4. `cawley2010`
5. `sandve2013`
6. `giannozzi2017`
7. `quantumEspressoPwInput`
8. `marzari1997`
9. `brouder2007`
10. `schonemann1966`
11. `baldereschiLipari1973`
12. `kohnLuttinger1955donor`
13. `demouraUllrich2021`
14. `mathlib2020`
15. `nipkowPaulsonWenzel2002`
16. `bertotCasteran2004`
17. `prodanKohn2005`
18. `kato1995`
19. `neumaier2004`
20. `mclachlan1947`
21. `bornOppenheimer1927`

### Systematic gaps

1. **Effective-mass foundations.** The opening effective-mass derivation and the
   phosphorus/boron continuum models need direct attribution to Luttinger–Kohn,
   Kohn–Luttinger, Burt, and Baldereschi–Lipari rather than relying only on a
   remote textbook footnote.
2. **Modern Wannier theory.** Composite-band gauges, disentanglement,
   higher-dimensional localization, topology, and route comparisons are
   unevenly cited. The Marzari–Vanderbilt, Souza–Marzari–Vanderbilt, and Brouder
   references are the principal missing anchors.
3. **Defect-supercell interpretation.** Periodic-image, charge-state, energy
   alignment, and isolated-defect caveats recur in several chapters; the
   existing Freysoldt references should be attached consistently.
4. **Evidence methodology.** The verification/validation/UQ taxonomy,
   validation leakage rule, and reproducibility guidance currently lack
   methodological sources.
5. **Formal-method infrastructure.** Lean, mathlib, Isabelle, and Rocq/Coq are
   named as proof backends without scholarly system references. Repository-local
   proof status still requires internal evidence in addition to those citations.
6. **Structured learning.** The chapter is mostly a project-specific proposed
   framework, so it was not broadly over-cited. Named Kohn–Sham, Slater–Koster,
   and silicon-donor model claims still need local attribution.
7. **Appendix coverage.** Appendix F has no citations despite relying on Wannier
   and tight-binding lineages; Appendix E needs a quantum-harmonic-oscillator
   anchor; Appendix H contains an uncited Chern/Wannier obstruction theorem.
8. **Software documentation.** The foundational Quantum ESPRESSO paper is
   present, but current capability and exact input-unit claims should also use
   the 2017 suite paper and a versioned official `pw.x` input reference.

### Existing citations requiring attention

- `giannozzi2009` is correct but incomplete as the sole source for current
  Quantum ESPRESSO capabilities; supplement it with `giannozzi2017`.
- `rostgaard2009` directly supports the PAW Wannier-overlap derivation but is an
  arXiv tutorial; pair it with the existing primary `blochl1994paw` citation.
- `kohn1959` is foundational but too narrow by itself for the manuscript's
  multidimensional/topological localization claim; supplement it with
  `brouder2007`.
- `higham1986` supports polar decomposition but is not the primary orthogonal
  Procrustes citation; supplement it with `schonemann1966`.
- `lowdin1982` supports the Löwdin side of the compound “Feshbach–Löwdin”
  attribution; add the existing `feshbach1958` citation at that occurrence.
- `hohenberg1964,kohn1965` support DFT and Kohn–Sham theory, not the separate
  Born–Oppenheimer attribution in Appendix I; add `bornOppenheimer1927` or
  move the existing citations to the narrower clause they actually support.

No existing citation was conclusively found to be false. The future-dated
`ermoneit2026` entry was independently resolved to the Physical Review B
publisher page, and the supplied paper has now been read in full. Its exact
valley-sector projection, nonlocal potential kernel, and energy-reference
invariance analysis support the cited locality claim.

### Internal evidence and navigation issues

Scholarly citations cannot substantiate repository-specific claims such as exact
execution counts, accepted task status, prover success, absence of `sorry` or
`admit`, or retained artifact identity. Those statements need durable internal
provenance references.

The audit also found stale “Note 5” and “Note 6” prose references in Appendices H
and I. These should become LaTeX cross-references to Appendices G and H. They are
navigation defects rather than bibliography defects.

### Sections with no additional citation finding

After complete review, no genuine additional external citation requirement was
identified in Chapters 7, 8, 10, 11, 14, or 20, or in Appendix D. Their uncited
material is principally project-specific policy, proposed work, explicit
mathematical derivation, or synthesis already supported at its primary location.

## Verification note

Publisher or primary-source pages were spot-checked for the principal missing
references, including Marzari–Vanderbilt, Brouder et al., Baldereschi–Lipari,
Kohn–Luttinger, Lean 4, Isabelle/HOL, Coq’Art, Kato, Neumaier, the National
Research Council report, and Sandve et al. Continuously updated documentation
such as the Quantum ESPRESSO `pw.x` manual still requires a version and access
date at editorial freeze. Any bibliography import should receive a final
publisher-metadata check before being treated as authoritative.
