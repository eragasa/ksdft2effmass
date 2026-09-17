# Blind alignment of matched one-dimensional defect spaces

## Abstract

A deterministic synthetic inverse problem tests whether hidden translation, orbital, spin-frame, and scalar energy-reference maps can be recovered before subtracting matched one-dimensional pristine and defect Hamiltonians. Full-rank spinless and spinor controls recover the authored maps modulo one global phase with Frobenius defects below $1.42\times10^{-14}$ and recover planted defect operators below $9.33\times10^{-15}\,E_G$. A controlled unitary perturbation of the anchor cross-covariance produces correspondingly graded map, extraction, model-class, spectral, and wavefunction errors without conflating those metrics. An undercomplete anchor identifies a 16-dimensional sector of a 32-dimensional represented space: two admissible full completions disagree by $9.92\times10^{-1}\,E_G$ as full operators but by only $7.73\times10^{-16}\,E_G$ after compression to the identified sector. Ill-conditioning, incompatible retained subspaces, unequal rank, incompatible spin space, and a missing energy anchor stop structurally. Neighboring diagnostics locate the conditioning, principal-angle, and energy-rank boundaries and demonstrate that rank and spin mismatches require explicit common-space constructions rather than forced fits. These are software and numerical verification results for synthetic data, not material validation.

## Question

The accepted known-map defect benchmark established that aligned subtraction recovers planted represented impurity operators. It did not establish whether the required coordinate and energy-reference maps can be inferred from observations without supplying the authored map. This follow-on asks:

1. when is the hidden map identifiable from a declared anchor cross-covariance;
2. what is recoverable when the anchors are rank deficient;
3. how does controlled anchor error propagate into distinct downstream metrics; and
4. which incompatibilities must prevent subtraction rather than be forced into a fit?

## Methods

The study reuses the immutable 16-cell, two-orbital composite parent and the planted onsite orbital and spin-mixing controls from the accepted defect benchmark. Candidate operators are authored by applying the inherited nontrivial translation, orbital permutation, orbital rotation, orbital phases, site phases, spin-frame rotation where applicable, and a scalar shift of $0.137\,E_G$.

The inference action receives reference and candidate operators, an anchor cross-covariance, retained-subspace overlap information, an exterior energy-anchor projector, spin labels, and a partial-alignment permission flag. It does not receive the authored map, shift, or defect. A truncated SVD supplies the polar partial isometry. The shift is estimated from the aligned exterior sector before subtraction. Oracle data enter only after inference, when map and extraction errors are evaluated.

Full-rank recovery is assessed modulo one global complex phase. In the undercomplete control, only the declared reference sector and its compressed operator are assessed; the complement is treated as an explicit gauge freedom. The full methods and stopping rules are frozen in `protocol.md`.

## Results

### Exact identifiable controls

The 32-dimensional spinless control has anchor condition number $1.43$. Its phase-quotiented map defect is $9.68\times10^{-15}$, scalar-shift error is $5.55\times10^{-17}\,E_G$, extraction defect is $5.54\times10^{-15}\,E_G$, and maximum active eigenvalue defect is $2.47\times10^{-15}\,E_G$. The lowest-state fidelity is numerically one.

The 64-dimensional spinor control has anchor condition number $1.54$. Its map defect is $1.41\times10^{-14}$, scalar-shift error is $5.55\times10^{-17}\,E_G$, extraction defect is $9.32\times10^{-15}\,E_G$, and maximum active eigenvalue defect is $3.30\times10^{-15}\,E_G$. The lowest-state fidelity is $0.9999999999999984$.

The planted onsite-class residuals are $2.23\times10^{-16}\,E_G$ and $2.03\times10^{-16}\,E_G$ for the spinless and spinor controls. Their extracted onsite-class residuals are $5.54\times10^{-15}\,E_G$ and $8.92\times10^{-15}\,E_G$. Model-class adequacy is therefore recorded separately from coordinate-map and direct extraction errors.

### Controlled anchor noise

The well-conditioned noise sweep perturbs only the unitary factor of the synthetic anchor cross-covariance. At $10^{-2}$ rad, the phase-quotiented map defect is $2.78\times10^{-2}$, the extraction defect is $1.62\times10^{-2}\,E_G$, the extracted onsite-model residual is $1.61\times10^{-2}\,E_G$, the maximum active eigenvalue defect is $6.81\times10^{-3}\,E_G$, and the lowest-state fidelity is $0.999931$. The inferred scalar-shift error remains $5.79\times10^{-6}\,E_G$ because it is estimated separately from the exterior sector.

The sweep demonstrates controlled error propagation for this authored family. It is not a statistical noise model, UQ result, or material tolerance study.

### Gauge-equivalent undercomplete anchors

The undercomplete control retains 16 nonzero singular directions in a 32-dimensional space. The inferred partial map agrees with the authored partial map to $9.06\times10^{-16}$ in Frobenius norm and the compressed planted operator is recovered to $7.37\times10^{-16}\,E_G$.

A second unitary completion acts only on the 16-dimensional null complement. The two full extracted operators disagree by $9.92\times10^{-1}\,E_G$, whereas their disagreement after compression to the identified sector is $7.73\times10^{-16}\,E_G$; the two partial maps agree there to $1.08\times10^{-15}$. Thus the full map and full operator are non-identifiable, while the declared compressed sector is numerically stable. This is the benchmark's explicit degeneracy result.

### Structured stopping

Five invalid observations return no alignment map, energy shift, or extracted operator:

| Control | Structured issue |
|---|---|
| minimum anchor singular value $10^{-8}$ and condition number $10^8$ | `BLIND_ALIGNMENT.ANCHOR_ILL_CONDITIONED` |
| retained-subspace principal angle $0.6$ rad | `BLIND_ALIGNMENT.SUBSPACE_ANGLE_EXCEEDED` |
| unequal represented ranks | `BLIND_ALIGNMENT.RANK_MISMATCH` |
| spinless/spinor mismatch | `BLIND_ALIGNMENT.SPIN_MISMATCH` |
| zero exterior energy-anchor rank | `BLIND_ALIGNMENT.ENERGY_ANCHOR_INSUFFICIENT` |

These are rejected comparisons, not large residuals from nominal extraction.

## Debugging the five stops

The retained negative controls were not weakened. Each was paired with neighboring or explicitly reconciled observations.

For conditioning, a fixed additive anchor perturbation of spectral norm $10^{-10}$ was applied while the smallest anchor singular value was reduced. At condition number $5.00\times10^5$, the map and extraction defects have grown to $2.64\times10^{-6}$ and $1.22\times10^{-6}\,E_G$. The next point has condition number $1.25\times10^6$ and stops, followed by the $10^7$ and $10^8$ controls. Thus the diagnostic exposes pre-threshold amplification without treating a stopped case as a large nominal residual.

For retained-subspace compatibility, only reference direction 31 carries the swept principal angle. Angles through $0.34$ rad remain admissible, while $0.36$ and $0.60$ rad stop against the frozen $0.35$-rad rule. The threshold is a declared synthetic protocol boundary, not a material acceptance criterion.

The unequal-rank case remains invalid as a full unitary comparison. After explicitly declaring a $32\times31$ rectangular partial isometry, its common-sector map and zero-operator extraction defects are $9.92\times10^{-15}$ and $6.58\times10^{-15}\,E_G$. The zero target has a 31-dimensional lowest eigenspace, so an individual lowest-state fidelity is undefined; the eigenspace-projector defect is $7.28\times10^{-15}$.

The spinless--spinor comparison likewise remains invalid directly. An explicit spin lift gives the common 64-dimensional spinor space and reproduces the full-rank spinor map and extraction defects, $1.41\times10^{-14}$ and $9.32\times10^{-15}\,E_G$. Conversely, the planted spin-mixing defect has spin-independent restriction residual $7.97\times10^{-2}\,E_G$, so no lossless spinless restriction exists for that control.

Finally, exterior energy-anchor ranks zero through three stop. Rank four now passes exactly under the declared rule, with shift error $-2.78\times10^{-17}\,E_G$ and extraction defect $7.59\times10^{-15}\,E_G$; ranks eight and 22 also pass. This diagnostic exposed and corrected a numerical-boundary defect in the initial implementation: energy-anchor rank is now computed by singular-value numerical rank rather than compared through a floating-point trace. The trace remains only the shift-averaging weight. Rank four is a robustness requirement of this protocol, not a universal identifiability theorem.

## Independent verification

The verifier independently reconstructs the parent Hamiltonian, hidden maps, defects, observations, polar maps, scalar shift, extracted operators, gauge-completion contrast, matrix digests, structured stops, all five diagnostic families, the rectangular partial isometry, and the spin-lift comparison without importing the runner. It reproduces every retained numerical field within the declared floating-point comparison rule.

## Interpretation

The exercise distinguishes three outcomes:

1. full identifiability, where the map is recovered modulo a declared global phase;
2. partial identifiability, where only an identified sector and compressed operator may be compared; and
3. incompatibility, where subtraction must not occur.

The benchmark also shows why alignment quality cannot be represented by one downstream eigenvalue or fidelity. Map, shift, extraction, model-class, spectral, and state-vector diagnostics respond differently even in this controlled setting.

## Limitations

All observations, maps, and defects are synthetic. The anchor cross-covariance and retained-subspace overlap are authored observables, not outputs from an independent electronic-structure calculation. The partial case establishes only compressed-sector recovery and does not identify the anchor-null complement. Nothing here validates silicon, phosphorus, boron, DFT, Wannierization, continuum reduction, transferability, uncertainty estimates, or a public alignment API.
