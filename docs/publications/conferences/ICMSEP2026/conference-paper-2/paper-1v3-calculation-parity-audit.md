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

The checklist contains 110 completed development-parity dispositions: five
restricted-alignment checks, 15 threshold/refinement/disposition checks, nine
frame/transport/closure checks, 22 Fourier-locality and omitted-weight checks, eight
numerical-identity checks, 24 Hamiltonian-error checks, four mesh/amplitude-resolution
checks, 21 spectral-error checks, and two retained-subspace checks. The three inherited
tolerance-dependent conclusions are explicitly inapplicable because the synthetic study
characterizes a decision landscape and defines no acceptance test; their numerical
requirements remain calculated coordinates rather than pass/fail outcomes. There are no
outstanding literal one-dimensional applicability determinations. A completed box records a definition and
an independent development reconstruction; it does not confer scientific qualification.
For the completed alignment checks, direct finite-mesh correlations agree with the
applicable Bessel-product or constrained zero-mode comparators in bounded square,
cubic, triangular, and FCC controls, and the refinement angle, correlation, and
midpoint reductions were reconstructed directly from adjacent levels. For the completed
closure checks, the ordered link products and their phase reductions were reconstructed
independently in bounded two- and three-dimensional frames. Full-rank transport singular
values, Procrustes residuals, applied rank cutoffs, link-unitarity defects,
closure-unitarity defects, frame orthonormality, and periodic frame closure were
likewise reconstructed from the parent projectors and neighbor overlaps rather than
accepted from the reported reductions. The positive-scale minimum and unit-scale
exact-spectrum residuals were evaluated directly from the aligned matrices, while their
normalized thresholds, midpoint defects, and refinement changes were reconstructed
separately. For the completed Fourier checks, independent explicit finite sums rebuilt
the square, simple-cubic, triangular, and FCC construction fields, hopping blocks,
reconstructions, shell powers, ordinary omitted powers, Nyquist powers, and error
channels without calling the production Fourier transform or evaluator. The bounded
pointwise discrepancies and the independently reconstructed refinement and midpoint
reductions agreed within an absolute tolerance of \(5\times10^{-13}\). The added
error-channel parity tranche independently rebuilt normalized Hamiltonian and sorted-band
interpolation, truncation, and total errors on every complete metric shell, then selected
the first-passing shell and its immediately preceding error without calling the
production decision routine. The deliberately loose value \(10^{-1}\) exercises the
first-passing development calculation only; it is not a frozen family-specific
scientific tolerance. The same oracle checked the \(N=6\) half-step construction mesh,
the independently shifted \(M=7\) evaluation mesh, their strictly positive torus
separation, direct band covariance, Parseval and reconstruction defects, Hamiltonian
Hermiticity, and the sampled external rank-two isolation gap. The literal one-dimensional
range-zero endpoint has the unique onsite-shell replacement \(s=0\). Literal ranges 8
and 16 have no family-independent multidimensional replacement because complete support
is ordered by each family's scaled direct-lattice metric; all available complete shells
and first-passing shells are retained instead. Positive construction--evaluation mesh
separation also makes literal shared-node eigenvalue and projector comparisons
inapplicable rather than zero. Independent \(N=8\) and \(N=16\) quadratures bounded
the largest normalized change among the enumerated integrated alignment and Fourier
power channels by \(10^{-5}\) in this development control. Direct closed-form
second-harmonic maximization separately reproduced the optimized positive-scale and
unit-scale thresholds, normalized squared residual, midpoint defects, and sampled
small-amplitude behavior. Flat residual--locality identities were independently
reconstructed where the flat parent has nonzero retained splitting; the bipartite
flat-parent controls instead retain explicit zero-splitting inapplicability.

## 1. Restricted global alignment

These checks concern the declared momentum-independent \(SO(2)\) alignment and positive
splitting scale. They must not be replaced by a momentum-dependent pointwise gauge.

- [x] Evaluate the finite-mesh estimate of the maximum restricted correlation on the declared construction mesh. *(unitless)*
- [x] Bound the change in the optimizing global rotation angle under amplitude refinement. *(unitless)*
- [x] Recompute the maximum restricted correlation for every dimensional family. *(unitless)*
- [x] Bound the refinement change in the maximum restricted correlation. *(unitless)*
- [x] Evaluate the midpoint interpolation defect of the restricted correlation. *(unitless)*

## 2. Thresholds, scale optimization, refinement, and scientific dispositions

These checks distinguish the best positive splitting scale from the unit-scale problem
and keep numerical refinement separate from a scientific pass/fail conclusion.

- [x] State the dimensionless tolerance used for each scientific decision; do not inherit the Paper 1 value without justification.
- [x] Evaluate the endpoint minimum operator threshold divided by \(\sqrt{\kappa}\). *(unitless)*
- [x] Evaluate the departure from the flat-parent residual--locality identity. *(unitless)*
- [x] Evaluate the exact-spectrum joint operator threshold divided by \(\sqrt{\kappa}\). *(unitless)*
- [x] Bound the largest refinement change among the final reported outcomes. *(unitless)*
- [x] Bound the largest refinement change among invariants of the parent Hamiltonian. *(unitless)*
- [x] Evaluate the midpoint defect of the joint threshold. *(in units of \(E_{\mathrm{ref}}\))*
- [x] Separate interpolation error from the midpoint defect of the joint threshold. *(in units of \(E_{\mathrm{ref}}\))*
- [x] Bound the largest refinement change among parent-model diagnostics. *(unitless)*
- [x] Bound the largest refinement change in the operator or joint threshold. *(in units of \(E_{\mathrm{ref}}\))*
- [x] Determine whether the momentum-resolved criterion passes, fails, or remains scientifically unresolved.
- [x] Decide whether the optimized-scale result meets a frozen family-specific tolerance. *(inapplicable: the synthetic decision-landscape study defines no acceptance test; the optimized-scale requirement remains a calculated objective coordinate)*
- [x] Decide whether the unit-splitting-scale result meets a frozen family-specific tolerance. *(inapplicable: the synthetic decision-landscape study defines no acceptance test; the unit-scale requirement remains a calculated objective coordinate)*
- [x] Recompute the parent splitting power \(\kappa\) and the optimal nonnegative comparison multiplier \(\lambda_\ast=\max(0,\mu_{\max})\). *(unitless)*
- [x] Decide whether all required family-specific tolerances are satisfied simultaneously. *(inapplicable: simultaneous pass/fail classification is replaced by sampled nondominance among retained-block, Hamiltonian-error, and sorted-band-error objectives)*

## 3. Frame transport, periodic closure, and sewing

These checks qualify the retained frame over the Brillouin torus. A rank-deficient
transport overlap invalidates closure and plaquette interpretation; an arbitrary unitary
completion must not be treated as physical evidence.

- [x] Evaluate \(\Phi_0=\max_{\alpha,\mathbf k_\perp}|\phi_{\alpha,0}(\mathbf k_\perp)|\), where \(\phi_{\alpha,0}\) is the lower ordered principal eigenphase of the full-rank closure holonomy around reciprocal direction \(\alpha\). *(radians)*
- [x] Evaluate \(\Phi_1=\max_{\alpha,\mathbf k_\perp}|\phi_{\alpha,1}(\mathbf k_\perp)|\), where \(\phi_{\alpha,1}\) is the upper ordered principal eigenphase of the same closure holonomy. *(radians)*
- [x] Bound \(\|W^\dagger W-I\|\) for every closure holonomy \(W\). *(unitless)*
- [x] Bound \(\|F(\mathbf k)^\dagger F(\mathbf k)-I\|\) over the sampled Brillouin zone. *(unitless)*
- [x] Evaluate the maximum residual of the unitary Procrustes transport problem. *(unitless)*
- [x] Record the singular-value cutoff used to declare a transport overlap rank deficient. *(unitless)*
- [x] Bound the unitarity defect of every full-rank transport link. *(unitless)*
- [x] Record the minimum singular value among all sampled transport overlaps. *(unitless)*
- [x] Evaluate the defect in periodic closure of the transported frame. *(unitless)*

## 4. Fourier locality and omitted-weight accounting

For each representation, distinguish the non-onsite weight, the weight outside a chosen
complete physical-metric support, ordinary omitted modes, and Nyquist modes. Reference
and comparison quantities must be evaluated separately before taking their difference.
The bounded parity reconstruction uses rank two and \(E_{\mathrm{ref}}=1\), so each
reported block power is dimensionless. Ordinary omitted power excludes the removed
Nyquist boundary and tends to zero when the complete support contains every ordinary
mode; total omitted power is the ordinary omitted power plus the separately reported
Nyquist power. Refinement checks use \(N=4,8,16\), while the independent shifted-mesh
point check uses \(N=6\) and \(M=7\). These sizes establish development parity only,
not convergence or a retained scientific result.

- [x] Evaluate the comparison non-onsite power \(\sum_{\mathbf R\ne0}P^{\mathrm{cmp}}_{\mathbf R}\).
- [x] Evaluate every shell-resolved comparison hopping-block power \(P^{\mathrm{cmp}}_{\mathbf R}\).
- [x] Evaluate the normalized comparison tail \(\sum_{\mathbf R\notin\mathcal S}P^{\mathrm{cmp}}_{\mathbf R}\) outside each complete support \(\mathcal S\).
- [x] Evaluate the comparison weight carried by Nyquist modes.
- [x] Evaluate the comparison weight omitted from the ordinary lattice after cyclic-to-ordinary conversion.
- [x] Evaluate the total omitted comparison weight, including ordinary and Nyquist contributions.
- [x] Evaluate the endpoint excess of comparison non-onsite weight over reference non-onsite weight.
- [x] Evaluate the excess non-onsite power \(\sum_{\mathbf R\ne0}(P^{\mathrm{cmp}}_{\mathbf R}-P^{\mathrm{ref}}_{\mathbf R})\).
- [x] Bound the refinement change of every shell-resolved hopping-block power.
- [x] Evaluate the amplitude-midpoint defect of every shell-resolved hopping-block power.
- [x] Bound the refinement change of the integrated hopping weight.
- [x] Evaluate the amplitude-midpoint defect of the non-onsite hopping weight.
- [x] Evaluate the non-onsite power \(\sum_{\mathbf R\ne0}P_{\mathbf R}\) for the representation under study.
- [x] Evaluate the normalized excess non-onsite power using the declared rank-two and energy normalization.
- [x] Evaluate every normalized shell-resolved hopping-block power \(P_{\mathbf R}\).
- [x] Evaluate the normalized tail \(\sum_{\mathbf R\notin\mathcal S}P_{\mathbf R}\) outside each complete support \(\mathcal S\).
- [x] Evaluate the reference non-onsite power \(\sum_{\mathbf R\ne0}P^{\mathrm{ref}}_{\mathbf R}\).
- [x] Evaluate every shell-resolved reference hopping-block power \(P^{\mathrm{ref}}_{\mathbf R}\).
- [x] Evaluate the normalized reference tail \(\sum_{\mathbf R\notin\mathcal S}P^{\mathrm{ref}}_{\mathbf R}\) outside each complete support \(\mathcal S\).
- [x] Evaluate the reference weight carried by Nyquist modes.
- [x] Evaluate the reference weight omitted from the ordinary lattice after cyclic-to-ordinary conversion.
- [x] Evaluate the total omitted reference weight, including ordinary and Nyquist contributions.

## 5. Numerical identities, reconstruction, and independent reproduction

These checks establish numerical consistency only. They do not establish convergence of
the scientific model or validate a material claim.

- [x] Compare the principal result with an independently refined momentum quadrature. *(unitless relative defect)*
- [x] Bound the change produced by the finer quadrature for every integrated quantity. *(unitless relative defect)*
- [x] Bound the numerical defect in every applicable analytic residual--locality identity and retain explicit zero-splitting inapplicability. *(unitless)*
- [x] Verify Parseval equality between momentum-space and hopping-space Frobenius weights. *(unitless relative defect)*
- [x] Reconstruct \(H(\mathbf k)\) from the complete hopping blocks and bound the maximum reconstruction defect. *(unitless relative defect)*
- [x] Bound \(\|H^{\mathrm{ref}}(\mathbf k)-H^{\mathrm{ref}}(\mathbf k)^\dagger\|\) over the sampled Brillouin zone. *(unitless relative defect)*
- [x] Independently reproduce every primary numerical quantity and report the maximum normalized defect.
- [x] Report the discrepancy between the primary calculation and the independent reconstruction without reusing the primary disposition.

## 6. Hamiltonian errors, operator thresholds, and first-passing supports

Matrix errors use the declared norm on the aligned retained Hamiltonians. Interpolation,
deliberate truncation, and their total consequence must remain separate. A first-passing
support requires the passing error and the error at the immediately preceding complete
support.

- [x] Find the smallest complete support for which the comparison Hamiltonian satisfies the matrix-error tolerance.
- [x] Report the comparison Hamiltonian error at that first-passing support.
- [x] Report the comparison Hamiltonian error at the immediately preceding complete support.
- [x] Evaluate \(\max_{\mathbf k}\varepsilon_{H,\mathrm{cmp}}^{\mathrm{int}}(\mathbf k)\).
- [x] Evaluate \(\max_{\mathbf k}\varepsilon_{H,\mathrm{cmp}}^{\mathrm{tot}}(\mathbf k)\).
- [x] Evaluate \(\max_{\mathbf k}\varepsilon_{H,\mathrm{cmp}}^{\mathrm{trunc}}(\mathbf k)\).
- [x] Evaluate the Brillouin-zone RMS of \(\varepsilon_{H,\mathrm{cmp}}^{\mathrm{int}}\).
- [x] Evaluate the Brillouin-zone RMS of \(\varepsilon_{H,\mathrm{cmp}}^{\mathrm{tot}}\).
- [x] Evaluate the Brillouin-zone RMS of \(\varepsilon_{H,\mathrm{cmp}}^{\mathrm{trunc}}\).
- [x] Resolve the literal one-dimensional endpoint error at range zero by evaluating the unique multidimensional onsite-only complete shell \(s=0\).
- [x] Confirm that the literal one-dimensional endpoint error at range sixteen has no unique multidimensional scalar-radius counterpart. *(inapplicable: family metrics give no common range-16 support)*
- [x] Confirm that the literal one-dimensional endpoint error at range eight has no unique multidimensional scalar-radius counterpart. *(inapplicable: family metrics give no common range-8 support)*
- [x] Evaluate the exact-spectrum joint operator threshold without replacing it by the optimized-scale threshold. *(in units of \(E_{\mathrm{ref}}\))*
- [x] Evaluate \(\max_{\mathbf k}\varepsilon_H^{\mathrm{int}}(\mathbf k)\) for the representation under study.
- [x] Evaluate the amplitude-midpoint defect of the minimum operator threshold. *(in units of \(E_{\mathrm{ref}}\))*
- [x] Separate interpolation error from the amplitude-midpoint defect of the operator threshold. *(in units of \(E_{\mathrm{ref}}\))*
- [x] Minimize the aligned operator residual over the allowed global rotation and positive splitting scale. *(in units of \(E_{\mathrm{ref}}\))*
- [x] Divide the minimum operator threshold by \(\sqrt{\kappa}\) and examine its sampled small-amplitude limit.
- [x] Evaluate the normalized squared operator residual on the common retained state space.
- [x] Find the smallest complete support for which the reference Hamiltonian satisfies the matrix-error tolerance.
- [x] Report the reference Hamiltonian error at that first-passing support.
- [x] Report the reference Hamiltonian error at the immediately preceding complete support.
- [x] Evaluate \(\max_{\mathbf k}\varepsilon_{H,\mathrm{ref}}^{\mathrm{trunc}}(\mathbf k)\).
- [x] Evaluate the Brillouin-zone RMS of \(\varepsilon_{H,\mathrm{ref}}^{\mathrm{trunc}}\).

## 7. Momentum, amplitude, and refinement resolution

Resolution counts document the discretization on which a quantity was evaluated; they
are not, by themselves, convergence evidence.

- [x] Record the number and placement of gauge-amplitude nodes used in the analytic and numerical scans.
- [x] Record the tensor dimensions and origin convention of the construction mesh.
- [x] Record the tensor dimensions and shift of the independent evaluation mesh.
- [x] Evaluate the minimum periodic separation between the construction mesh and the shifted evaluation mesh. *(unitless reduced reciprocal coordinate)*

## 8. Spectral errors and first-passing supports

Spectral errors compare sorted retained-band energies in units of
\(E_{\mathrm{ref}}\). They must remain distinct from matrix-norm errors because spectral
agreement alone does not establish operator equivalence or hopping locality.

- [x] Find the smallest complete support for which the comparison bands satisfy the spectral-error tolerance.
- [x] Report the comparison band error at that first-passing support.
- [x] Report the comparison band error at the immediately preceding complete support.
- [x] Evaluate the maximum comparison-band interpolation error over the evaluation mesh.
- [x] Evaluate the maximum total comparison-band error over the evaluation mesh.
- [x] Evaluate the maximum comparison-band truncation error over the evaluation mesh.
- [x] Evaluate the Brillouin-zone RMS comparison-band interpolation error.
- [x] Evaluate the Brillouin-zone RMS total comparison-band error.
- [x] Evaluate the Brillouin-zone RMS comparison-band truncation error.
- [x] Resolve the literal one-dimensional endpoint band error at range zero by evaluating the unique multidimensional onsite-only complete shell \(s=0\).
- [x] Confirm that the literal one-dimensional endpoint band error at range sixteen has no unique multidimensional scalar-radius counterpart. *(inapplicable: family metrics give no common range-16 support)*
- [x] Confirm that the literal one-dimensional endpoint band error at range eight has no unique multidimensional scalar-radius counterpart. *(inapplicable: family metrics give no common range-8 support)*
- [x] Evaluate the maximum normalized discrepancy between the pointwise reference and comparison band eigenvalues.
- [x] Evaluate the maximum normalized discrepancy between the directly constructed reference and comparison band eigenvalues before Fourier interpolation or truncation.
- [x] Evaluate the maximum band interpolation error for the representation under study.
- [x] Confirm that a literal shared-node parent-eigenvalue comparison is unavailable because the independently evaluated construction--evaluation torus separation is positive. *(inapplicable)*
- [x] Find the smallest complete support for which the reference bands satisfy the spectral-error tolerance.
- [x] Report the reference band error at that first-passing support.
- [x] Report the reference band error at the immediately preceding complete support.
- [x] Evaluate the maximum reference-band truncation error over the evaluation mesh.
- [x] Evaluate the Brillouin-zone RMS reference-band truncation error.

## 9. Retained-subspace qualification

The retained rank-two subspace must be identified and isolated before any aligned
Hamiltonian subtraction is interpreted.

- [x] Confirm that a literal shared-node projector comparison is unavailable because the independently evaluated construction--evaluation torus separation is positive. *(inapplicable)*
- [x] Evaluate the minimum sampled external spectral gap separating the retained rank-two subspace from the discarded states. *(in units of \(E_{\mathrm{ref}}\))*

## Completion condition

The checklist is complete when every applicable box is supported by an independently
reproduced quantity for every Paper 2 family, every inherited tolerance-dependent
conclusion has either a frozen family-specific scientific rule or an explicit
non-acceptance disposition, both closure-phase reductions have a stated mathematical
meaning, and every inapplicability statement has been reviewed against the relevant
geometry and meshes.
