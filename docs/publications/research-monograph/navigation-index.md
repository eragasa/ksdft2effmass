# Monograph navigation index

## Purpose and authority

This file is a source-navigation aid for humans and software agents. It does not
replace the table of contents, the back-of-book index, or the authoritative
scientific and computational records. Chapter and appendix prose remains
explanatory; applicable versioned files under `specification/`, computational
documentation, proof packages, and retained provenance records continue to own
their respective contracts and evidence.

The **Primary source** column identifies the manuscript location that owns the
main exposition. **Supporting sources** provide derivations, examples, or later
applications without redefining the primary discussion.

## Concept map

| Concept | Primary source | Supporting sources | Role in the manuscript |
|---|---|---|---|
| Model adequacy | `chapters/01-model-adequacy.tex` (`ch:operator-reduction-motivation`) | `chapters/03-evidence-for-model-adequacy.tex` | Governing scientific question |
| Linear operator and domain | `chapters/01-model-adequacy.tex`, Definition 1.1 | `chapters/02-operator-comparison.tex`; `appendices/C-operator-spaces-compression-alignment.tex` | Mathematical definition and qualification |
| Dirac notation | `chapters/01-model-adequacy.tex`, Definition 1.2 | `appendices/A-notation-and-status.tex` | Introductory notation |
| Hamiltonian decomposition | `chapters/01-model-adequacy.tex`, Definition 1.3 | `appendices/C-operator-spaces-compression-alignment.tex` | Operator decomposition |
| Orthogonal projection | `chapters/01-model-adequacy.tex`, Definition 1.4 | `chapters/02-operator-comparison.tex`; `appendices/C-operator-spaces-compression-alignment.tex` | Retained-space construction |
| Position-space representation | `chapters/01-model-adequacy.tex`, Definition 1.5 | `appendices/D-particle-in-a-box-residuals.tex` | Coordinate representation |
| PAW transformation | `chapters/01-model-adequacy.tex` | `chapters/06-bulk-representations.tex` | Explanatory contrast; not the active silicon parent |
| Spectral reconstruction | `chapters/01-model-adequacy.tex` | `appendices/D-particle-in-a-box-residuals.tex` | Controlled diagnostic |
| State space | `chapters/02-operator-comparison.tex` (`ch:mathematical-foundations`) | `appendices/A-notation-and-status.tex`; `appendices/C-operator-spaces-compression-alignment.tex` | Comparison prerequisite |
| Finite matrix representation | `chapters/02-operator-comparison.tex` | `appendices/A-notation-and-status.tex` | Representation contract |
| Basis and gauge | `chapters/02-operator-comparison.tex` | `chapters/06-bulk-representations.tex`; `appendices/C-operator-spaces-compression-alignment.tex` | Coordinate freedom and alignment prerequisite |
| Energy reference | `chapters/02-operator-comparison.tex` | `chapters/06-bulk-representations.tex`; `appendices/I-impurity-effective-mass-models.tex` | Comparison prerequisite |
| Alignment | `chapters/02-operator-comparison.tex` | `chapters/06-bulk-representations.tex`; `chapters/10-impurity-operator-extraction.tex`; `appendices/C-operator-spaces-compression-alignment.tex` | Identified-space comparison |
| Operator residual | `chapters/02-operator-comparison.tex` | `appendices/B-hilbert-schmidt-and-frobenius.tex`; `appendices/D-particle-in-a-box-residuals.tex` | Comparison metric |
| Evidence classes | `chapters/03-evidence-for-model-adequacy.tex` (`ch:verification-and-validation`) | `chapters/00-preface.tex`; `appendices/A-notation-and-status.tex` | Claim discipline |
| Software verification | `chapters/03-evidence-for-model-adequacy.tex` | `chapters/15-current-evidence-boundary.tex` | Software evidence |
| Numerical verification | `chapters/03-evidence-for-model-adequacy.tex` | `chapters/05-first-principles-bulk-parent.tex` | Mathematical and convergence evidence |
| Scientific validation | `chapters/03-evidence-for-model-adequacy.tex` | `chapters/14-dopant-transferability.tex` | Independent-use evidence |
| Uncertainty quantification | `chapters/03-evidence-for-model-adequacy.tex` | `chapters/15-current-evidence-boundary.tex` | Uncertainty evidence boundary |
| Parent-model error | `chapters/00-preface.tex` | `chapters/07-bulk-reduced-models.tex`; `appendices/A-notation-and-status.tex` | Error category |
| Numerical error | `chapters/00-preface.tex` | `chapters/03-evidence-for-model-adequacy.tex`; `chapters/07-bulk-reduced-models.tex` | Error category |
| Model-reduction error | `chapters/00-preface.tex` | `chapters/07-bulk-reduced-models.tex`; `appendices/F-bulk-silicon-reduction-routes.tex` | Error category |
| Bulk-silicon program | `chapters/04-bulk-silicon-program.tex` (`ch:physical-problem`) | `chapters/05-first-principles-bulk-parent.tex` through `chapters/08-selecting-bulk-representation.tex` | First scientific program |
| First-principles bulk parent | `chapters/05-first-principles-bulk-parent.tex` (`ch:first-principles-parent`) | `chapters/15-current-evidence-boundary.tex` | Parent construction and current status |
| Pseudopotential identity | `chapters/05-first-principles-bulk-parent.tex` | `chapters/04-bulk-silicon-program.tex` | Numerical identity and provenance |
| Convergence | `chapters/05-first-principles-bulk-parent.tex` | `chapters/03-evidence-for-model-adequacy.tex` | Parent numerical verification |
| Bloch representation | `chapters/06-bulk-representations.tex` (`ch:representations-and-alignment`) | `appendices/G-one-dimensional-reduction.tex`; `appendices/H-two-dimensional-wannier-reduction.tex` | Periodic representation |
| Disentanglement | `chapters/06-bulk-representations.tex` | `appendices/F-bulk-silicon-reduction-routes.tex` | Retained-subspace construction |
| Wannier transformation | `chapters/06-bulk-representations.tex` | `appendices/F-bulk-silicon-reduction-routes.tex`; `appendices/G-one-dimensional-reduction.tex`; `appendices/H-two-dimensional-wannier-reduction.tex` | Localized representation |
| Wannier localization | `chapters/06-bulk-representations.tex` | `appendices/G-one-dimensional-reduction.tex`; `appendices/H-two-dimensional-wannier-reduction.tex` | Gauge selection, not reduction by itself |
| Bulk tight-binding hierarchy | `chapters/07-bulk-reduced-models.tex` (`ch:model-reduction`) | `appendices/F-bulk-silicon-reduction-routes.tex` | Bulk model classes |
| Direct reduction route | `chapters/07-bulk-reduced-models.tex` | `appendices/F-bulk-silicon-reduction-routes.tex` | KS-DFT-to-TB path |
| Wannier-mediated route | `chapters/07-bulk-reduced-models.tex` | `appendices/F-bulk-silicon-reduction-routes.tex` | KS-DFT-to-Wannier-to-TB path |
| Bulk-model selection | `chapters/08-selecting-bulk-representation.tex` | `chapters/15-current-evidence-boundary.tex` | Unresolved model-class decision |
| Doped-silicon program | `chapters/09-doped-silicon-program.tex` (`ch:doped-silicon-program`) | `chapters/10-impurity-operator-extraction.tex` through `chapters/14-dopant-transferability.tex` | Second scientific program |
| Substitutional phosphorus | `chapters/09-doped-silicon-program.tex` | `chapters/14-dopant-transferability.tex`; `appendices/I-impurity-effective-mass-models.tex` | Donor branch |
| Substitutional boron | `chapters/09-doped-silicon-program.tex` | `chapters/14-dopant-transferability.tex`; `appendices/I-impurity-effective-mass-models.tex` | Acceptor and transferability branch |
| Impurity-operator extraction | `chapters/10-impurity-operator-extraction.tex` (`ch:impurity-operator-extraction`) | `appendices/I-impurity-effective-mass-models.tex` | Aligned pristine--doped difference |
| Lattice impurity models | `chapters/11-lattice-impurity-models.tex` (`ch:lattice-impurity-models`) | `appendices/I-impurity-effective-mass-models.tex` | Nested impurity model classes |
| Continuum effective-mass model | `chapters/12-continuum-effective-mass.tex` (`ch:continuum-effective-mass`) | `appendices/I-impurity-effective-mass-models.tex`; `appendices/J-envelope-theory-luttinger-khon-burt-ermoneit.tex` | Continuum reduction |
| Envelope-function theory | `appendices/J-envelope-theory-luttinger-khon-burt-ermoneit.tex` (`app:envelope-theory`) | `chapters/01-model-adequacy.tex`; `chapters/12-continuum-effective-mass.tex`; `appendices/I-impurity-effective-mass-models.tex` | Equation extraction and project interpretation |
| Luttinger--Kohn model | `appendices/J-envelope-theory-luttinger-khon-burt-ermoneit.tex` | `chapters/01-model-adequacy.tex`; `chapters/12-continuum-effective-mass.tex` | Bulk, multivalley, and degenerate-band envelope foundation |
| Burt envelope representation | `appendices/J-envelope-theory-luttinger-khon-burt-ermoneit.tex` | `chapters/02-operator-comparison.tex`; `chapters/06-bulk-representations.tex` | Exact band-limited representation and controlled local reduction |
| Ermoneit multivalley theory | `appendices/J-envelope-theory-luttinger-khon-burt-ermoneit.tex` | `chapters/12-continuum-effective-mass.tex`; `appendices/I-impurity-effective-mass-models.tex` | Valley-sector projectors, energy-reference invariance, and filtered-local approximation |
| Multivalley envelope equation | `appendices/J-envelope-theory-luttinger-khon-burt-ermoneit.tex` | `chapters/12-continuum-effective-mass.tex`; `appendices/I-impurity-effective-mass-models.tex` | Phosphorus continuum foundation and limitation |
| Degenerate-band envelope equation | `appendices/J-envelope-theory-luttinger-khon-burt-ermoneit.tex` | `chapters/09-doped-silicon-program.tex`; `chapters/12-continuum-effective-mass.tex` | Boron continuum foundation and spin--orbit qualification |
| Crossover radius | `chapters/12-continuum-effective-mass.tex` | `chapters/18-mathematics-of-reduction.tex` | Proposed atomistic-to-continuum criterion |
| Structured learning | `chapters/13-structured-learning.tex` (`ch:structured-learning`) | `chapters/14-dopant-transferability.tex` | Proposed model-class diagnostic |
| Dopant transferability | `chapters/14-dopant-transferability.tex` (`ch:dopant-transferability`) | `chapters/09-doped-silicon-program.tex` | Phosphorus-to-boron methodological test |
| Current evidence boundary | `chapters/15-current-evidence-boundary.tex` (`ch:results-and-limitations`) | `chapters/20-conclusions.tex` | Status inventory, not production scientific results |
| Proof architecture | `chapters/16-proof-architecture.tex` (`ch:proof-program`) | `chapters/19-mechanization-status.tex` | Proof-package organization |
| Finite-dimensional foundations | `chapters/17-finite-dimensional-foundations.tex` (`ch:finite-dimensional-foundations`) | `appendices/B-hilbert-schmidt-and-frobenius.tex`; `appendices/C-operator-spaces-compression-alignment.tex` | Exact operator identities |
| Excluded-space reduction | `chapters/18-mathematics-of-reduction.tex` (`ch:mathematics-of-reduction`) | `appendices/C-operator-spaces-compression-alignment.tex` | Analytical reduction claim |
| Operator-to-observable bounds | `chapters/18-mathematics-of-reduction.tex` | `appendices/I-impurity-effective-mass-models.tex` | Analytical bridge to declared observables |
| Mechanization status | `chapters/19-mechanization-status.tex` (`ch:mechanization-status`) | `chapters/15-current-evidence-boundary.tex` | Formal-proof evidence boundary |
| Notation and status | `appendices/A-notation-and-status.tex` | `chapters/00-preface.tex` | Reference appendix |
| Hilbert--Schmidt and Frobenius geometry | `appendices/B-hilbert-schmidt-and-frobenius.tex` | `chapters/17-finite-dimensional-foundations.tex` | Operator-space geometry |
| Particle-in-a-box diagnostic | `appendices/D-particle-in-a-box-residuals.tex` | `chapters/01-model-adequacy.tex` | Illustrative example only |
| Harmonic-oscillator diagnostic | `appendices/E-harmonic-oscillator-comparison.tex` | `chapters/01-model-adequacy.tex` | Proposed controlled numerical experiment |
| One-dimensional warmup | `appendices/G-one-dimensional-reduction.tex` | `chapters/06-bulk-representations.tex`; `chapters/07-bulk-reduced-models.tex` | Proposed analytical and numerical warmup |
| Two-dimensional warmup | `appendices/H-two-dimensional-wannier-reduction.tex` | `chapters/06-bulk-representations.tex`; `chapters/07-bulk-reduced-models.tex` | Proposed analytical and numerical warmup |
| Candidate contemporary literature | `appendices/K-candidate-contemporary-literature.tex` (`app:candidate-contemporary-literature`) | `citation-audit.md`; `references.bib` | Prospective review queue; bibliography presence is not source acceptance |

## Navigation rules for agents

1. Start with the primary source listed above.
2. Follow its LaTeX label and explicit cross-references before searching for
   repeated terminology.
3. Use appendices for derivations and controlled examples, not as authority for
   scientific settings or completed results.
4. Check `chapters/15-current-evidence-boundary.tex` before describing a
   capability or numerical outcome as completed.
5. Consult the applicable owning specification, proof package, computational
   record, or provenance artifact before treating manuscript prose as a
   scientific or software contract.
