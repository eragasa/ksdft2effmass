# Paper 1 v3 calculation-parity checklist for Paper 2

## Scientific rule

Every scientifically applicable quantity in the Paper 1 v3 one-dimensional diagnostic
catalog must be recomputed independently for each Paper 2 family. Paper 1 tolerances and
conclusions do not transfer automatically. A one-dimensional quantity that has no
well-defined multidimensional counterpart must be identified as inapplicable with a
geometric or mathematical reason; it must not be omitted or assigned an artificial zero.

A checkbox may be marked complete only after the quantity's definition, units,
normalization, limiting interpretation, and independently reproduced value have been
reviewed. The checklist records scientific completeness, not scientific qualification.

## Notation

Let \(H^{\mathrm{ref}}(\mathbf k)\) and
\(H^{\mathrm{cmp}}(\mathbf k)\) denote the aligned reference and comparison
Hamiltonians on the declared retained state space. Their hopping blocks are
\(T^{\mathrm{ref}}_{\mathbf R}\) and
\(T^{\mathrm{cmp}}_{\mathbf R}\), with normalized block power
\(P^x_{\mathbf R}=\|T^x_{\mathbf R}\|_F^2/(2E_{\mathrm{ref}}^2)\) for
\(x\in\{\mathrm{ref},\mathrm{cmp}\}\). For a complete retained support
\(\mathcal S\), interpolation, deliberate truncation, and total errors are denoted by
\(\varepsilon^{\mathrm{int}}\), \(\varepsilon^{\mathrm{trunc}}\), and
\(\varepsilon^{\mathrm{tot}}\), respectively. Matrix-norm errors and sorted-band errors
remain distinct. \(E_{\mathrm{ref}}\) is the declared energy scale, \(\kappa\) is the
declared gauge-amplitude parameter, and all lattice radii are measured with the relevant
direct-lattice metric.

The checklist currently contains 110 obligations: 97 calculated quantities awaiting
independent parity review, three tolerance-dependent conclusions that remain unresolved,
two closure-phase quantities needing a defined multidimensional scalar reduction, and
eight literal one-dimensional quantities whose inapplicability must be confirmed.

## 1. Restricted global alignment

These checks concern the declared momentum-independent \(SO(2)\) alignment and positive
splitting scale. They must not be replaced by a momentum-dependent pointwise gauge.

- [ ] Evaluate the finite-mesh estimate of the maximum restricted correlation on the declared construction mesh. *(unitless)*
- [ ] Bound the change in the optimizing global rotation angle under amplitude refinement. *(unitless)*
- [ ] Recompute the maximum restricted correlation for every dimensional family. *(unitless)*
- [ ] Bound the refinement change in the maximum restricted correlation. *(unitless)*
- [ ] Evaluate the midpoint interpolation defect of the restricted correlation. *(unitless)*

## 2. Thresholds, scale optimization, refinement, and scientific dispositions

These checks distinguish the best positive splitting scale from the unit-scale problem
and keep numerical refinement separate from a scientific pass/fail conclusion.

- [ ] State the dimensionless tolerance used for each scientific decision; do not inherit the Paper 1 value without justification.
- [ ] Evaluate the endpoint minimum operator threshold divided by \(\sqrt{\kappa}\). *(unitless)*
- [ ] Evaluate the departure from the flat-parent residual--locality identity. *(unitless)*
- [ ] Evaluate the exact-spectrum joint operator threshold divided by \(\sqrt{\kappa}\). *(unitless)*
- [ ] Bound the largest refinement change among the final reported outcomes. *(unitless)*
- [ ] Bound the largest refinement change among invariants of the parent Hamiltonian. *(unitless)*
- [ ] Evaluate the midpoint defect of the joint threshold. *(in units of \(E_{\mathrm{ref}}\))*
- [ ] Separate interpolation error from the midpoint defect of the joint threshold. *(in units of \(E_{\mathrm{ref}}\))*
- [ ] Bound the largest refinement change among parent-model diagnostics. *(unitless)*
- [ ] Bound the largest refinement change in the operator or joint threshold. *(in units of \(E_{\mathrm{ref}}\))*
- [ ] Determine whether the momentum-resolved criterion passes, fails, or remains scientifically unresolved.
- [ ] Decide whether the optimized-scale result meets a frozen family-specific tolerance. *(currently unresolved because no tolerance is frozen)*
- [ ] Decide whether the unit-splitting-scale result meets a frozen family-specific tolerance. *(currently unresolved because no tolerance is frozen)*
- [ ] Recompute the positive splitting scale that minimizes the restricted-alignment residual. *(unitless)*
- [ ] Decide whether all required family-specific tolerances are satisfied simultaneously. *(currently unresolved because no tolerances are frozen)*

## 3. Frame transport, periodic closure, and sewing

These checks qualify the retained frame over the Brillouin torus. A rank-deficient
transport overlap invalidates closure and plaquette interpretation; an arbitrary unitary
completion must not be treated as physical evidence.

- [ ] Define and evaluate the first scalar reduction of the multidimensional closure-holonomy eigenphases. *(radians; reduction still to be defined)*
- [ ] Define and evaluate the second scalar reduction of the multidimensional closure-holonomy eigenphases. *(radians; reduction still to be defined)*
- [ ] Bound \(\|W^\dagger W-I\|\) for every closure holonomy \(W\). *(unitless)*
- [ ] Bound \(\|F(\mathbf k)^\dagger F(\mathbf k)-I\|\) over the sampled Brillouin zone. *(unitless)*
- [ ] Evaluate the maximum residual of the unitary Procrustes transport problem. *(unitless)*
- [ ] Record the singular-value cutoff used to declare a transport overlap rank deficient. *(unitless)*
- [ ] Bound the unitarity defect of every full-rank transport link. *(unitless)*
- [ ] Record the minimum singular value among all sampled transport overlaps. *(unitless)*
- [ ] Evaluate the defect in periodic closure of the transported frame. *(unitless)*

## 4. Fourier locality and omitted-weight accounting

For each representation, distinguish the non-onsite weight, the weight outside a chosen
complete physical-metric support, ordinary omitted modes, and Nyquist modes. Reference
and comparison quantities must be evaluated separately before taking their difference.

- [ ] Evaluate the comparison non-onsite power \(\sum_{\mathbf R\ne0}P^{\mathrm{cmp}}_{\mathbf R}\).
- [ ] Evaluate every shell-resolved comparison hopping-block power \(P^{\mathrm{cmp}}_{\mathbf R}\).
- [ ] Evaluate the normalized comparison tail \(\sum_{\mathbf R\notin\mathcal S}P^{\mathrm{cmp}}_{\mathbf R}\) outside each complete support \(\mathcal S\).
- [ ] Evaluate the comparison weight carried by Nyquist modes.
- [ ] Evaluate the comparison weight omitted from the ordinary lattice after cyclic-to-ordinary conversion.
- [ ] Evaluate the total omitted comparison weight, including ordinary and Nyquist contributions.
- [ ] Evaluate the endpoint excess of comparison non-onsite weight over reference non-onsite weight.
- [ ] Evaluate the excess non-onsite power \(\sum_{\mathbf R\ne0}(P^{\mathrm{cmp}}_{\mathbf R}-P^{\mathrm{ref}}_{\mathbf R})\).
- [ ] Bound the refinement change of every shell-resolved hopping-block power.
- [ ] Evaluate the amplitude-midpoint defect of every shell-resolved hopping-block power.
- [ ] Bound the refinement change of the integrated hopping weight.
- [ ] Evaluate the amplitude-midpoint defect of the non-onsite hopping weight.
- [ ] Evaluate the non-onsite power \(\sum_{\mathbf R\ne0}P_{\mathbf R}\) for the representation under study.
- [ ] Evaluate the normalized excess non-onsite power using the declared rank-two and energy normalization.
- [ ] Evaluate every normalized shell-resolved hopping-block power \(P_{\mathbf R}\).
- [ ] Evaluate the normalized tail \(\sum_{\mathbf R\notin\mathcal S}P_{\mathbf R}\) outside each complete support \(\mathcal S\).
- [ ] Evaluate the reference non-onsite power \(\sum_{\mathbf R\ne0}P^{\mathrm{ref}}_{\mathbf R}\).
- [ ] Evaluate every shell-resolved reference hopping-block power \(P^{\mathrm{ref}}_{\mathbf R}\).
- [ ] Evaluate the normalized reference tail \(\sum_{\mathbf R\notin\mathcal S}P^{\mathrm{ref}}_{\mathbf R}\) outside each complete support \(\mathcal S\).
- [ ] Evaluate the reference weight carried by Nyquist modes.
- [ ] Evaluate the reference weight omitted from the ordinary lattice after cyclic-to-ordinary conversion.
- [ ] Evaluate the total omitted reference weight, including ordinary and Nyquist contributions.

## 5. Numerical identities, reconstruction, and independent reproduction

These checks establish numerical consistency only. They do not establish convergence of
the scientific model or validate a material claim.

- [ ] Compare the principal result with an independently refined momentum quadrature. *(unitless relative defect)*
- [ ] Bound the change produced by the finer quadrature for every integrated quantity. *(unitless relative defect)*
- [ ] Bound the numerical defect in every analytic residual--locality identity. *(unitless)*
- [ ] Verify Parseval equality between momentum-space and hopping-space Frobenius weights. *(unitless relative defect)*
- [ ] Reconstruct \(H(\mathbf k)\) from the complete hopping blocks and bound the maximum reconstruction defect. *(unitless relative defect)*
- [ ] Bound \(\|H^{\mathrm{ref}}(\mathbf k)-H^{\mathrm{ref}}(\mathbf k)^\dagger\|\) over the sampled Brillouin zone. *(unitless relative defect)*
- [ ] Independently reproduce every primary numerical quantity and report the maximum normalized defect.
- [ ] Report the discrepancy between the primary calculation and the independent reconstruction without reusing the primary disposition.

## 6. Hamiltonian errors, operator thresholds, and first-passing supports

Matrix errors use the declared norm on the aligned retained Hamiltonians. Interpolation,
deliberate truncation, and their total consequence must remain separate. A first-passing
support requires the passing error and the error at the immediately preceding complete
support.

- [ ] Find the smallest complete support for which the comparison Hamiltonian satisfies the matrix-error tolerance.
- [ ] Report the comparison Hamiltonian error at that first-passing support.
- [ ] Report the comparison Hamiltonian error at the immediately preceding complete support.
- [ ] Evaluate \(\max_{\mathbf k}\varepsilon_{H,\mathrm{cmp}}^{\mathrm{int}}(\mathbf k)\).
- [ ] Evaluate \(\max_{\mathbf k}\varepsilon_{H,\mathrm{cmp}}^{\mathrm{tot}}(\mathbf k)\).
- [ ] Evaluate \(\max_{\mathbf k}\varepsilon_{H,\mathrm{cmp}}^{\mathrm{trunc}}(\mathbf k)\).
- [ ] Evaluate the Brillouin-zone RMS of \(\varepsilon_{H,\mathrm{cmp}}^{\mathrm{int}}\).
- [ ] Evaluate the Brillouin-zone RMS of \(\varepsilon_{H,\mathrm{cmp}}^{\mathrm{tot}}\).
- [ ] Evaluate the Brillouin-zone RMS of \(\varepsilon_{H,\mathrm{cmp}}^{\mathrm{trunc}}\).
- [ ] Confirm that the literal one-dimensional endpoint error at range zero has no unique multidimensional scalar-radius counterpart, or define one scientifically. *(currently inapplicable)*
- [ ] Confirm that the literal one-dimensional endpoint error at range sixteen has no unique multidimensional scalar-radius counterpart, or define one scientifically. *(currently inapplicable)*
- [ ] Confirm that the literal one-dimensional endpoint error at range eight has no unique multidimensional scalar-radius counterpart, or define one scientifically. *(currently inapplicable)*
- [ ] Evaluate the exact-spectrum joint operator threshold without replacing it by the optimized-scale threshold. *(in units of \(E_{\mathrm{ref}}\))*
- [ ] Evaluate \(\max_{\mathbf k}\varepsilon_H^{\mathrm{int}}(\mathbf k)\) for the representation under study.
- [ ] Evaluate the amplitude-midpoint defect of the minimum operator threshold. *(in units of \(E_{\mathrm{ref}}\))*
- [ ] Separate interpolation error from the amplitude-midpoint defect of the operator threshold. *(in units of \(E_{\mathrm{ref}}\))*
- [ ] Minimize the aligned operator residual over the allowed global rotation and positive splitting scale. *(in units of \(E_{\mathrm{ref}}\))*
- [ ] Divide the minimum operator threshold by \(\sqrt{\kappa}\) and examine its small-amplitude limit.
- [ ] Evaluate the normalized squared operator residual on the common retained state space.
- [ ] Find the smallest complete support for which the reference Hamiltonian satisfies the matrix-error tolerance.
- [ ] Report the reference Hamiltonian error at that first-passing support.
- [ ] Report the reference Hamiltonian error at the immediately preceding complete support.
- [ ] Evaluate \(\max_{\mathbf k}\varepsilon_{H,\mathrm{ref}}^{\mathrm{trunc}}(\mathbf k)\).
- [ ] Evaluate the Brillouin-zone RMS of \(\varepsilon_{H,\mathrm{ref}}^{\mathrm{trunc}}\).

## 7. Momentum, amplitude, and refinement resolution

Resolution counts document the discretization on which a quantity was evaluated; they
are not, by themselves, convergence evidence.

- [ ] Record the number and placement of gauge-amplitude nodes used in the analytic and numerical scans.
- [ ] Record the tensor dimensions and origin convention of the construction mesh.
- [ ] Record the tensor dimensions and shift of the independent evaluation mesh.
- [ ] Evaluate the minimum periodic separation between the construction mesh and the shifted evaluation mesh. *(unitless reduced reciprocal coordinate)*

## 8. Spectral errors and first-passing supports

Spectral errors compare sorted retained-band energies in units of
\(E_{\mathrm{ref}}\). They must remain distinct from matrix-norm errors because spectral
agreement alone does not establish operator equivalence or hopping locality.

- [ ] Find the smallest complete support for which the comparison bands satisfy the spectral-error tolerance.
- [ ] Report the comparison band error at that first-passing support.
- [ ] Report the comparison band error at the immediately preceding complete support.
- [ ] Evaluate the maximum comparison-band interpolation error over the evaluation mesh.
- [ ] Evaluate the maximum total comparison-band error over the evaluation mesh.
- [ ] Evaluate the maximum comparison-band truncation error over the evaluation mesh.
- [ ] Evaluate the Brillouin-zone RMS comparison-band interpolation error.
- [ ] Evaluate the Brillouin-zone RMS total comparison-band error.
- [ ] Evaluate the Brillouin-zone RMS comparison-band truncation error.
- [ ] Confirm that the literal one-dimensional endpoint band error at range zero has no unique multidimensional scalar-radius counterpart, or define one scientifically. *(currently inapplicable)*
- [ ] Confirm that the literal one-dimensional endpoint band error at range sixteen has no unique multidimensional scalar-radius counterpart, or define one scientifically. *(currently inapplicable)*
- [ ] Confirm that the literal one-dimensional endpoint band error at range eight has no unique multidimensional scalar-radius counterpart, or define one scientifically. *(currently inapplicable)*
- [ ] Evaluate the maximum normalized discrepancy between the pointwise reference and comparison band eigenvalues.
- [ ] Evaluate the maximum normalized discrepancy between the directly constructed reference and comparison band eigenvalues before Fourier interpolation or truncation.
- [ ] Evaluate the maximum band interpolation error for the representation under study.
- [ ] Confirm that a literal shared-node parent-eigenvalue comparison is unavailable when construction and evaluation meshes do not share nodes, or define a valid comparison. *(currently inapplicable)*
- [ ] Find the smallest complete support for which the reference bands satisfy the spectral-error tolerance.
- [ ] Report the reference band error at that first-passing support.
- [ ] Report the reference band error at the immediately preceding complete support.
- [ ] Evaluate the maximum reference-band truncation error over the evaluation mesh.
- [ ] Evaluate the Brillouin-zone RMS reference-band truncation error.

## 9. Retained-subspace qualification

The retained rank-two subspace must be identified and isolated before any aligned
Hamiltonian subtraction is interpreted.

- [ ] Confirm that a literal shared-node projector comparison is unavailable when construction and evaluation meshes do not share nodes, or define a valid projector comparison. *(currently inapplicable)*
- [ ] Evaluate the minimum sampled external spectral gap separating the retained rank-two subspace from the discarded states. *(in units of \(E_{\mathrm{ref}}\))*

## Completion condition

The checklist is complete only when every applicable box is supported by an
independently reproduced quantity for every Paper 2 family, every tolerance-dependent
conclusion has a frozen family-specific scientific rule, both closure-phase reductions
have a stated mathematical meaning, and every inapplicability statement has been
reviewed against the relevant geometry and meshes.
