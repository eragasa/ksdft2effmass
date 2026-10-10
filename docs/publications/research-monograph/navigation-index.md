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

## Part I computational prerequisite sequence

1. `chapters/computational-quantities.tex` — quantities, units, coordinates,
   indexing, and metadata;
2. `chapters/finite-representations.tex` — vectors, bases, matrices, and finite
   representation contracts;
3. `chapters/hermitian-eigensystems.tex` — Hermitian spectral theory,
   characteristic equations, degeneracy, projectors, and eigensystem
   diagnostics;
4. `chapters/quantum-states-and-operators.tex` — quantum states, operators,
   Hamiltonians, and the one-dimensional particle in a box;
5. `chapters/particle-in-a-box-higher-dimensions.tex` — two- and
   three-dimensional boxes, tensor-product bases, Kronecker products, and
   sparse Kronecker sums;
6. `chapters/periodic-geometry.tex` — direct and reciprocal periodic geometry;
7. `chapters/bloch-periodic-finite-differences.tex` — Bloch seams and sparse
   finite-difference representations;
8. `chapters/projection-and-retained-spaces.tex` — projection, compression, and
   exact retained operators;
9. `chapters/isolated-band-fourier-reduction.tex` — one-dimensional Bloch
   fibers, isolated scalar bands, complete hopping transforms, finite-range
   truncation, direct fitting, and withheld evaluation;
10. `chapters/composite-band-gauge-alignment.tex` — composite Bloch frames, the
    Bloch--Wannier bridge, polar transport, reciprocal closure, Procrustes
    alignment, block hoppings, and gauge-dependent locality; and
11. `chapters/verification-and-evidence-vocabulary.tex` — bounded claims,
    verification, validation, uncertainty, and negative evidence.

## Part II model-adequacy sequence

1. `chapters/model-adequacy.tex` — the scientific motivation and distinction
   between exact retention and model-class approximation;
2. `chapters/operator-comparison.tex` — common-space identification, gauge,
   energy reference, represented differences, and residuals;
3. `chapters/admissible-sets-and-certificates.tex` — normalized spectral and
   operator losses, constrained alignment families, admissible-set
   intersections, common witnesses, quadratic geometry, and separation
   certificates; and
4. `chapters/evidence-for-model-adequacy.tex` — program-specific verification,
   validation, provenance, uncertainty, and claim discipline.

## Concept map

| Concept | Primary source | Supporting sources | Role in the manuscript |
|---|---|---|---|
| Computational quantity and metadata | `chapters/computational-quantities.tex` (`ch:training-computational-quantities`) | `chapters/finite-representations.tex`; `chapters/operator-comparison.tex` | Numbers, units, references, axis meanings, and operation-relative metadata |
| Fractional and Cartesian coordinates | `chapters/periodic-geometry.tex` (`ch:training-periodic-geometry`) | `chapters/computational-quantities.tex`; `chapters/bloch-periodic-finite-differences.tex` | Periodic coordinate map after general coordinate metadata |
| Vectors, bases, and matrices | `chapters/finite-representations.tex` (`ch:training-finite-representations`) | `chapters/quantum-states-and-operators.tex`; `chapters/operator-comparison.tex` | Finite coordinate representations |
| Hermitian eigensystems | `chapters/hermitian-eigensystems.tex` (`ch:training-hermitian-eigensystems`) | `chapters/quantum-states-and-operators.tex`; `chapters/particle-in-a-box-higher-dimensions.tex`; `chapters/projection-and-retained-spaces.tex` | Eigenpairs, spectral decomposition, Rayleigh quotients, degeneracy, projectors, coordinate freedoms, and numerical diagnostics |
| One-dimensional particle in a box | `chapters/quantum-states-and-operators.tex` (`ch:training-quantum-operators`) | `appendices/D-particle-in-a-box-residuals.tex` | Characteristic-equation solution, Born interpretation, and finite representation on $[a,b]$ |
| Differential characteristic equation | `chapters/quantum-states-and-operators.tex` | `chapters/hermitian-eigensystems.tex` | Converts a constant-coefficient operator polynomial into an algebraic root problem |
| Born rule | `chapters/quantum-states-and-operators.tex` | `appendices/A-notation-and-status.tex` | Position density and energy-outcome probabilities |
| Dirichlet Laplacian on an interval | `chapters/quantum-states-and-operators.tex` | `appendices/D-particle-in-a-box-residuals.tex` | Continuum operator, centered difference, and discrete sine eigensystem |
| Two- and three-dimensional particle in a box | `chapters/particle-in-a-box-higher-dimensions.tex` (`ch:training-particle-box-higher-dimensions`) | `chapters/quantum-states-and-operators.tex` | Separable continuum and finite box models |
| Kronecker product and Kronecker sum | `chapters/particle-in-a-box-higher-dimensions.tex` | `chapters/bloch-periodic-finite-differences.tex` | Separate coordinate actions, flattening order, and sparse multidimensional assembly |
| Gram metric | `chapters/periodic-geometry.tex` | `chapters/bloch-periodic-finite-differences.tex`; `appendices/H-two-dimensional-wannier-reduction.tex` | Intrinsic lengths, angles, and differential geometry |
| Embedded periodic plane | `chapters/periodic-geometry.tex` | `chapters/bloch-periodic-finite-differences.tex` | Distinguishes a full-column-rank $3\times2$ plane from a slab |
| Dual reciprocal basis | `chapters/periodic-geometry.tex` | `chapters/bulk-representations.tex` | Direct--reciprocal duality for square and rectangular bases |
| Metric scalar Laplacian | `chapters/bloch-periodic-finite-differences.tex` (`ch:training-bloch-finite-differences`) | `appendices/H-two-dimensional-wannier-reduction.tex` | Coordinate-aware geometric operator |
| Mixed finite differences | `chapters/bloch-periodic-finite-differences.tex` | `appendices/H-two-dimensional-wannier-reduction.tex` | Nonorthogonal-coordinate stencil |
| Bloch quotient seam | `chapters/bloch-periodic-finite-differences.tex` | `chapters/bulk-representations.tex` | Twisted periodic boundary convention |
| Model adequacy | `chapters/model-adequacy.tex` (`ch:operator-reduction-motivation`) | `chapters/admissible-sets-and-certificates.tex`; `chapters/evidence-for-model-adequacy.tex` | Governing scientific question |
| Candidate family and parameter domain | `chapters/admissible-sets-and-certificates.tex` (`ch:admissible-sets-certificates`) | `chapters/bulk-reduced-models.tex`; `appendices/G-one-dimensional-reduction.tex` | Separates model parameters, alignment variables, and numerical controls |
| Spectral and operator admissible sets | `chapters/admissible-sets-and-certificates.tex` | `chapters/operator-comparison.tex`; `chapters/bulk-reduced-models.tex` | Simultaneous thresholded criteria for one candidate |
| Common witness and separation certificate | `chapters/admissible-sets-and-certificates.tex` | `chapters/evidence-for-model-adequacy.tex`; `appendices/G-one-dimensional-reduction.tex` | Distinguishes existence evidence, global separation evidence, and failed search |
| Quadratic-loss geometry and threshold sensitivity | `chapters/admissible-sets-and-certificates.tex` | `chapters/evidence-for-model-adequacy.tex`; `appendices/G-one-dimensional-reduction.tex` | Ellipsoidal sublevel sets, finite alignment unions, metric dependence, and post-hoc sensitivity boundaries |
| Linear operator and domain | `chapters/quantum-states-and-operators.tex` (`ch:training-quantum-operators`) | `chapters/operator-comparison.tex`; `appendices/C-operator-spaces-compression-alignment.tex` | Mathematical definition and domain qualification |
| Dirac notation | `chapters/quantum-states-and-operators.tex` | `appendices/A-notation-and-status.tex` | Introductory state notation |
| Hamiltonian decomposition | `chapters/quantum-states-and-operators.tex` | `chapters/model-adequacy.tex`; `appendices/C-operator-spaces-compression-alignment.tex` | Operator decomposition before finite representation |
| Orthogonal projection | `chapters/projection-and-retained-spaces.tex` (`ch:training-projection-retained-spaces`) | `chapters/operator-comparison.tex`; `appendices/C-operator-spaces-compression-alignment.tex` | Retained-space construction |
| Position-space representation | `chapters/quantum-states-and-operators.tex` | `appendices/D-particle-in-a-box-residuals.tex` | Coordinate representation |
| PAW transformation | `chapters/model-adequacy.tex` | `chapters/bulk-representations.tex` | Explanatory contrast; not the active silicon parent |
| Spectral reconstruction | `chapters/projection-and-retained-spaces.tex` | `chapters/model-adequacy.tex`; `appendices/D-particle-in-a-box-residuals.tex` | Exact retained operator versus model-class approximation |
| State space | `chapters/quantum-states-and-operators.tex` | `chapters/projection-and-retained-spaces.tex`; `appendices/A-notation-and-status.tex`; `appendices/C-operator-spaces-compression-alignment.tex` | Operator and comparison prerequisite |
| Finite matrix representation | `chapters/finite-representations.tex` | `chapters/computational-quantities.tex`; `appendices/A-notation-and-status.tex` | Representation contract |
| Basis transformation and gauge | `chapters/finite-representations.tex` | `chapters/composite-band-gauge-alignment.tex`; `chapters/operator-comparison.tex`; `chapters/bulk-representations.tex`; `appendices/C-operator-spaces-compression-alignment.tex` | Generic coordinate freedom followed by periodic gauge constraints |
| Projection, localization, and truncation | `chapters/projection-and-retained-spaces.tex` | `chapters/isolated-band-fourier-reduction.tex`; `chapters/composite-band-gauge-alignment.tex`; `chapters/bulk-representations.tex`; `chapters/bulk-reduced-models.tex` | Distinct retained-space and approximation operations |
| Isolated Bloch band | `chapters/projection-and-retained-spaces.tex` | `chapters/isolated-band-fourier-reduction.tex`; `appendices/G-one-dimensional-reduction.tex` | Fiberwise rank-one retention separated from phase gauge and localization |
| Composite Bloch frame and projector | `chapters/composite-band-gauge-alignment.tex` (`ch:training-composite-band-gauge-alignment`) | `chapters/projection-and-retained-spaces.tex`; `appendices/G-one-dimensional-reduction.tex` | Higher-rank retained space separated from its gauge-dependent frame |
| Bloch--Wannier bridge | `chapters/composite-band-gauge-alignment.tex` | `chapters/bulk-representations.tex`; `appendices/G-one-dimensional-reduction.tex` | Derivation from a Bloch frame through a Wannier basis to matrix-valued hoppings |
| Polar frame transport and reciprocal closure | `chapters/composite-band-gauge-alignment.tex` | `chapters/bulk-representations.tex`; `appendices/G-one-dimensional-reduction.tex` | Neighbor-overlap conditioning, sewing, and closure holonomy without a topology claim |
| Pointwise and global Procrustes alignment | `chapters/composite-band-gauge-alignment.tex` | `chapters/operator-comparison.tex`; `chapters/bulk-representations.tex` | Exact controlled gauge recovery versus a restricted one-unitary family |
| Gauge-dependent block locality | `chapters/composite-band-gauge-alignment.tex` | `chapters/operator-comparison.tex`; `appendices/G-one-dimensional-reduction.tex` | Complete spectral covariance separated from gauge-sensitive truncation |
| Plane-wave Bloch fiber | `chapters/isolated-band-fourier-reduction.tex` (`ch:training-isolated-band-fourier-reduction`) | `chapters/bloch-periodic-finite-differences.tex`; `appendices/G-one-dimensional-reduction.tex` | Reciprocal-basis representation of a periodic cosine Hamiltonian |
| Complete hopping transform | `chapters/isolated-band-fourier-reduction.tex` | `appendices/G-one-dimensional-reduction.tex`; `chapters/bulk-reduced-models.tex` | Finite reciprocal-to-cell Fourier transform and inverse interpolation |
| Finite hopping range and Parseval diagnostic | `chapters/isolated-band-fourier-reduction.tex` | `appendices/G-one-dimensional-reduction.tex`; `chapters/evidence-for-model-adequacy.tex` | Omitted coefficients, training residuals, and transform-specific norm identity |
| Direct versus Fourier-mediated fitting | `chapters/isolated-band-fourier-reduction.tex` | `chapters/bulk-reduced-models.tex`; `appendices/G-one-dimensional-reduction.tex` | Conditional route equivalence under a matched uniform design |
| Training and staggered withheld reciprocal meshes | `chapters/isolated-band-fourier-reduction.tex` | `chapters/verification-and-evidence-vocabulary.tex`; `chapters/evidence-for-model-adequacy.tex` | Interpolation and evaluation roles without leakage |
| Energy reference | `chapters/operator-comparison.tex` | `chapters/bulk-representations.tex`; `appendices/I-impurity-effective-mass-models.tex` | Comparison prerequisite |
| Alignment | `chapters/operator-comparison.tex` | `chapters/bulk-representations.tex`; `chapters/impurity-operator-extraction.tex`; `appendices/C-operator-spaces-compression-alignment.tex` | Identified-space comparison |
| Operator residual | `chapters/operator-comparison.tex` | `appendices/B-hilbert-schmidt-and-frobenius.tex`; `appendices/D-particle-in-a-box-residuals.tex` | Comparison metric |
| Evidence classes | `chapters/verification-and-evidence-vocabulary.tex` (`ch:training-evidence-vocabulary`) | `chapters/evidence-for-model-adequacy.tex`; `chapters/preface.tex`; `appendices/A-notation-and-status.tex` | Foundational claim discipline |
| Software verification | `chapters/verification-and-evidence-vocabulary.tex` | `chapters/evidence-for-model-adequacy.tex`; `chapters/current-evidence-boundary.tex` | Contract evidence definition and program-specific application |
| Numerical verification | `chapters/verification-and-evidence-vocabulary.tex` | `chapters/evidence-for-model-adequacy.tex`; `chapters/first-principles-bulk-parent.tex` | Mathematical and convergence evidence |
| Scientific validation | `chapters/verification-and-evidence-vocabulary.tex` | `chapters/evidence-for-model-adequacy.tex`; `chapters/dopant-transferability.tex` | Independent-use evidence |
| Uncertainty quantification | `chapters/verification-and-evidence-vocabulary.tex` | `chapters/evidence-for-model-adequacy.tex`; `chapters/current-evidence-boundary.tex` | Uncertainty evidence boundary |
| Parent-model error | `chapters/preface.tex` | `chapters/bulk-reduced-models.tex`; `appendices/A-notation-and-status.tex` | Error category |
| Numerical error | `chapters/preface.tex` | `chapters/verification-and-evidence-vocabulary.tex`; `chapters/evidence-for-model-adequacy.tex`; `chapters/bulk-reduced-models.tex` | Error category |
| Model-reduction error | `chapters/preface.tex` | `chapters/bulk-reduced-models.tex`; `appendices/F-bulk-silicon-reduction-routes.tex` | Error category |
| Bulk-silicon program | `chapters/bulk-silicon-program.tex` (`ch:physical-problem`) | `chapters/first-principles-bulk-parent.tex` through `chapters/selecting-bulk-representation.tex` | First scientific program |
| First-principles bulk parent | `chapters/first-principles-bulk-parent.tex` (`ch:first-principles-parent`) | `chapters/current-evidence-boundary.tex` | Parent construction and current status |
| Pseudopotential identity | `chapters/first-principles-bulk-parent.tex` | `chapters/bulk-silicon-program.tex` | Numerical identity and provenance |
| Convergence | `chapters/first-principles-bulk-parent.tex` | `chapters/evidence-for-model-adequacy.tex` | Parent numerical verification |
| Bloch representation | `chapters/bulk-representations.tex` (`ch:representations-and-alignment`) | `appendices/G-one-dimensional-reduction.tex`; `appendices/H-two-dimensional-wannier-reduction.tex` | Periodic representation |
| Disentanglement | `chapters/bulk-representations.tex` | `appendices/F-bulk-silicon-reduction-routes.tex` | Retained-subspace construction |
| Wannier transformation | `chapters/bulk-representations.tex` | `appendices/F-bulk-silicon-reduction-routes.tex`; `appendices/G-one-dimensional-reduction.tex`; `appendices/H-two-dimensional-wannier-reduction.tex` | Localized representation |
| Wannier localization | `chapters/bulk-representations.tex` | `appendices/G-one-dimensional-reduction.tex`; `appendices/H-two-dimensional-wannier-reduction.tex` | Gauge selection, not reduction by itself |
| Bulk tight-binding hierarchy | `chapters/bulk-reduced-models.tex` (`ch:model-reduction`) | `appendices/F-bulk-silicon-reduction-routes.tex` | Bulk model classes |
| Direct reduction route | `chapters/bulk-reduced-models.tex` | `appendices/F-bulk-silicon-reduction-routes.tex` | KS-DFT-to-TB path |
| Wannier-mediated route | `chapters/bulk-reduced-models.tex` | `appendices/F-bulk-silicon-reduction-routes.tex` | KS-DFT-to-Wannier-to-TB path |
| Bulk-model selection | `chapters/selecting-bulk-representation.tex` | `chapters/current-evidence-boundary.tex` | Unresolved model-class decision |
| Doped-silicon program | `chapters/doped-silicon-program.tex` (`ch:doped-silicon-program`) | `chapters/impurity-operator-extraction.tex` through `chapters/dopant-transferability.tex` | Second scientific program |
| Substitutional phosphorus | `chapters/doped-silicon-program.tex` | `chapters/dopant-transferability.tex`; `appendices/I-impurity-effective-mass-models.tex`; `appendices/J-two-dimensional-defect-extraction.tex` | Donor branch |
| Substitutional boron | `chapters/doped-silicon-program.tex` | `chapters/dopant-transferability.tex`; `appendices/I-impurity-effective-mass-models.tex`; `appendices/J-two-dimensional-defect-extraction.tex` | Acceptor and transferability branch |
| Impurity-operator extraction | `chapters/impurity-operator-extraction.tex` (`ch:impurity-operator-extraction`) | `appendices/I-impurity-effective-mass-models.tex`; `appendices/J-two-dimensional-defect-extraction.tex` | Completed spin/1D controls and proposed 2D extension |
| Lattice impurity models | `chapters/lattice-impurity-models.tex` (`ch:lattice-impurity-models`) | `appendices/I-impurity-effective-mass-models.tex`; `appendices/J-two-dimensional-defect-extraction.tex` | Nested impurity model classes |
| Continuum effective-mass model | `chapters/continuum-effective-mass.tex` (`ch:continuum-effective-mass`) | `appendices/I-impurity-effective-mass-models.tex`; `appendices/J-two-dimensional-defect-extraction.tex`; `appendices/K-envelope-theory-luttinger-kohn-burt-ermoneit.tex` | Continuum reduction |
| Envelope-function theory | `appendices/K-envelope-theory-luttinger-kohn-burt-ermoneit.tex` (`app:envelope-theory`) | `chapters/model-adequacy.tex`; `chapters/continuum-effective-mass.tex`; `appendices/I-impurity-effective-mass-models.tex` | Equation extraction and project interpretation |
| Luttinger--Kohn model | `appendices/K-envelope-theory-luttinger-kohn-burt-ermoneit.tex` | `chapters/model-adequacy.tex`; `chapters/continuum-effective-mass.tex` | Bulk, multivalley, and degenerate-band envelope foundation |
| Burt envelope representation | `appendices/K-envelope-theory-luttinger-kohn-burt-ermoneit.tex` | `chapters/operator-comparison.tex`; `chapters/bulk-representations.tex` | Exact band-limited representation and controlled local reduction |
| Ermoneit multivalley theory | `appendices/K-envelope-theory-luttinger-kohn-burt-ermoneit.tex` | `chapters/continuum-effective-mass.tex`; `appendices/I-impurity-effective-mass-models.tex` | Valley-sector projectors, energy-reference invariance, and filtered-local approximation |
| Multivalley envelope equation | `appendices/K-envelope-theory-luttinger-kohn-burt-ermoneit.tex` | `chapters/continuum-effective-mass.tex`; `appendices/I-impurity-effective-mass-models.tex` | Phosphorus continuum foundation and limitation |
| Degenerate-band envelope equation | `appendices/K-envelope-theory-luttinger-kohn-burt-ermoneit.tex` | `chapters/doped-silicon-program.tex`; `chapters/continuum-effective-mass.tex` | Boron continuum foundation and spin--orbit qualification |
| Crossover radius | `chapters/continuum-effective-mass.tex` | `chapters/mathematics-of-reduction.tex` | Proposed atomistic-to-continuum criterion |
| Structured learning | `chapters/structured-learning.tex` (`ch:structured-learning`) | `chapters/dopant-transferability.tex` | Proposed model-class diagnostic |
| Dopant transferability | `chapters/dopant-transferability.tex` (`ch:dopant-transferability`) | `chapters/doped-silicon-program.tex` | Phosphorus-to-boron methodological test |
| Current evidence boundary | `chapters/current-evidence-boundary.tex` (`ch:results-and-limitations`) | `chapters/conclusions.tex` | Status inventory, not production scientific results |
| Proof architecture | `chapters/proof-architecture.tex` (`ch:proof-program`) | `chapters/mechanization-status.tex` | Proof-package organization |
| Finite-dimensional foundations | `chapters/finite-dimensional-foundations.tex` (`ch:finite-dimensional-foundations`) | `appendices/B-hilbert-schmidt-and-frobenius.tex`; `appendices/C-operator-spaces-compression-alignment.tex` | Exact operator identities |
| Excluded-space reduction | `chapters/mathematics-of-reduction.tex` (`ch:mathematics-of-reduction`) | `appendices/C-operator-spaces-compression-alignment.tex` | Analytical reduction claim |
| Operator-to-observable bounds | `chapters/mathematics-of-reduction.tex` | `appendices/I-impurity-effective-mass-models.tex` | Analytical bridge to declared observables |
| Mechanization status | `chapters/mechanization-status.tex` (`ch:mechanization-status`) | `chapters/current-evidence-boundary.tex` | Formal-proof evidence boundary |
| Notation and status | `appendices/A-notation-and-status.tex` | `chapters/preface.tex` | Reference appendix |
| Hilbert--Schmidt and Frobenius geometry | `appendices/B-hilbert-schmidt-and-frobenius.tex` | `chapters/finite-dimensional-foundations.tex` | Operator-space geometry |
| Particle-in-a-box residual diagnostic | `appendices/D-particle-in-a-box-residuals.tex` | `chapters/quantum-states-and-operators.tex`; `chapters/model-adequacy.tex` | Calculated finite-dimensional identifiability example, separate from the foundational derivation |
| Harmonic-oscillator diagnostic | `appendices/E-harmonic-oscillator-comparison.tex` | `chapters/model-adequacy.tex` | Completed illustrative numerical verification |
| One-dimensional periodic benchmark | `appendices/G-one-dimensional-reduction.tex` | `chapters/admissible-sets-and-certificates.tex`; `chapters/bulk-representations.tex`; `chapters/bulk-reduced-models.tex` | Historical reduction benchmarks plus the separately identified canonical M3 common-witness and separation-certificate result |
| Two-dimensional periodic benchmark | `appendices/H-two-dimensional-wannier-reduction.tex` | `chapters/bulk-representations.tex`; `chapters/bulk-reduced-models.tex` | Completed bounded numerical verification with a negative localization result |
| Controlled impurity-extraction benchmarks | `appendices/I-impurity-effective-mass-models.tex` (`app:impurity-model-classes`) | `chapters/impurity-operator-extraction.tex`; `chapters/current-evidence-boundary.tex` | Completed spin-space and one-dimensional synthetic verification |
| Two-dimensional defect-extraction program | `appendices/J-two-dimensional-defect-extraction.tex` (`app:two-dimensional-defect-extraction`) | `appendices/H-two-dimensional-wannier-reduction.tex`; `appendices/I-impurity-effective-mass-models.tex` | Active controlled synthetic task with no result; material transfer remains proposed |
| Candidate contemporary literature | `appendices/L-candidate-contemporary-literature.tex` (`app:candidate-contemporary-literature`) | `citation-audit.md`; `references.bib` | Prospective review queue; bibliography presence is not source acceptance |

## Navigation rules for agents

1. Start with the primary source listed above.
2. Follow its LaTeX label and explicit cross-references before searching for
   repeated terminology.
3. Use appendices for derivations and controlled examples, not as authority for
   scientific settings or completed results.
4. Check `chapters/current-evidence-boundary.tex` before describing a
   capability or numerical outcome as completed.
5. Consult the applicable owning specification, proof package, computational
   record, or provenance artifact before treating manuscript prose as a
   scientific or software contract.
