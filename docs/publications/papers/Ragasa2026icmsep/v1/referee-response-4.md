# Response to technical review 4 — Discussion, Conclusions, and appendices

## Review disposition

- **Review outcome:** `CHANGES_REQUIRED`
- **Operator request:** `NONE`
- **Manuscript status:** discussion, conclusions, and appendix exposition revised; independent reconstruction and public archival packaging remain publication blockers

The review is accepted. The revisions tighten evidentiary hierarchy and derivation detail
without adding physics, changing frozen models, accessing the excluded 402-point set, or
performing new QE, Wannier90, silicon, optimization, or band-edge calculations.

## Responses and revisions

### 1. Unequal evidentiary status of the conclusions

**Disposition:** `NO_ACTION_REQUIRED` after revision

The Conclusions now open by distinguishing exact restricted-family statements from
bounded dispersive and rank-10 numerical demonstrations. They state explicitly that the
material-derived results remain subject to independent reconstruction.

Conclusion 4 retains the producer-checked qualification and “observed support-error
frontiers.” The final paragraph identifies H-shell-16 as a 371-of-383 near-full-support
reduction rather than a compact model.

### 2. Controlled finite-range conclusion

**Disposition:** `NO_ACTION_REQUIRED` after revision

Conclusion 3 now states the exact demonstrated result: in the declared controlled
dispersive rank-two example, the spectrum-preserving representation change raises the
first passing cutoff from 4 to 10 at the sampled target `10^-8 E_ref`. It explicitly
denies a universal monotonic gauge–range law.

### 3. Derivative and internal-operator fidelity

**Disposition:** `NO_ACTION_REQUIRED` after revision

Section 7.5 now separates three channels:

- errors in band values;
- errors in local second derivatives; and
- errors in the matrix-valued internal structure of a nearly degenerate subspace.

It states that the latter two are not controlled by the reported global spectral RMS
without additional regularity and error-control assumptions.

### 4. Evidence maturity and scope

**Disposition:** `NO_ACTION_REQUIRED` after revision

Section 7.9 now distinguishes complete-scope execution from independent
reconstruction. Full producer coverage is not independent reconstruction, and
independent reconstruction of a subset does not verify the unexamined inventory.

A condensed main-text evidence table now reports result class, evidence type,
verification status, and permitted claim. The complete calculation inventory remains in
the article appendix because it is an essential provenance and lifecycle boundary for
this synthesis; it was not moved out of the manuscript.

### 5. Rank-two derivation appendix

**Disposition:** `NO_ACTION_REQUIRED` after revision

Appendix A now:

1. declares normalized Brillouin-zone measure and the Fourier-coefficient convention;
2. shows that the zero block lies in the real traceless coefficient plane;
3. constructs the best onsite rotation and scale explicitly;
4. identifies `lambda_* = ||B_0||_F / ||D||_F = mu_max`; and
5. states the normalization `kappa = ||D||_F^2 / (2 E_ref^2)` used to recover the main theorem.

### 6. Numerical precision

**Disposition:** `NO_ACTION_REQUIRED` after revision

Appendix C now states that narrative values are rounded for readability while appendix
digits identify retained machine-readable records and are not uncertainty estimates.

### 7. Analysis-procedure appendix

**Disposition:** `NO_ACTION_REQUIRED` after revision

Appendix D is renamed **Analysis Procedures and Reproducibility Record**. It explicitly
denies that the appendix alone is a complete reproduction package.

The conduction search procedure now records the signed-sector partition, eight coarse
starts plus the source coordinate, band identity, ±0.12 Å⁻¹ Cartesian box, iteration and
tolerance settings, signed-axis rejection rule, and lowest-successful-candidate
selection.

### 8. Error-channel appendix

**Disposition:** `NO_ACTION_REQUIRED`

The complete error-channel table remains unchanged because it is one of the manuscript's
central scientific boundaries. A condensed six-channel separation already appears in
the silicon methodology, and the new evidence table makes the verification hierarchy
visible in the main Discussion.

### 9. Artifact hashes and eventual archive

**Disposition:** `MUST_FIX` before publication

Appendix F now states explicitly that hashes are audit anchors, not reproducibility
artifacts. Publication requires an archive containing the referenced files, manifests,
source identities, execution records, dependency resolution, and artifact relationships.
The final PDF plus digest list is insufficient.

No release, archive, DOI, or publication action is authorized by this manuscript edit.

### 10. Parent-gap lineage

**Disposition:** `NO_ACTION_REQUIRED`

The provenance question is already resolved in the main text:

- `0.5226105 eV` belongs to the earlier lower-energy-frozen `4^3`/12-band candidate;
- `0.6892447 eV` belongs to the current `C6-B20-W21` source; and
- both were compared with the same revealed DFT parent.

The manuscript uses the latter value only for the current source and does not combine
candidate lineages.

### 11. Remaining publication blockers

**Disposition:** `MUST_FIX`

Before submission-qualified numerical claims:

1. independently reconstruct the complete rank-two finite-range result;
2. independently reconstruct the rank-10 gauge/Fourier/support calculations;
3. independently reproduce the frozen fidelity and band-edge analyses; and
4. create the exact public reproduction archive and environment record.

These tasks must preserve the frozen attacks, models, searches, thresholds, and source
identities. More physics or another model family is not the next priority.
