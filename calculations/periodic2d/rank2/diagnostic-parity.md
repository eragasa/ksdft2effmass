# Periodic 2-D rank-two diagnostic parity

This catalog accounts for every scientific diagnostic family exposed by the maintained
periodic-1D embedded-subspace/rank-two donor. It maps those diagnostics to the
periodic-2D rank-two owner without copying one-dimensional coefficients, meshes,
cutoffs, scalar Nyquist rules, or conclusions.

Public periodic-2D rank-two requests, analyses, capability actions, lifecycle records,
and visualization contracts are owned under `ksdft2effmass.periodic2d.rank2`. Common
finite-periodic arithmetic remains implemented under
`ksdft2effmass.band_equivalence_hopping_locality`. The calculation
children select family-specific geometry, controls, execution identity, and evidence
status.
This catalog describes installed software and retained fields; it is not a calculated
result or an authorization to execute a producer.

## Parent and retained-subspace qualification

| Periodic-1D diagnostic | Periodic-2D rank-two diagnostic | Two-dimensional disposition |
|---|---|---|
| Minimum external isolation gap | `minimum_sampled_external_gap` and `continuous_external_gap_lower_bound` | The sampled value and analytic lower bound remain separate. |
| Retained-seed overlap | `minimum_seed_overlap` | Retained as a subspace-identification diagnostic. |
| Parent Hermiticity | `maximum_parent_hermiticity_defect` | Retained before any retained-space comparison. |
| Parent eigensystem reconstruction | `maximum_eigensystem_reconstruction_defect` | Retained independently of projector and Fourier reconstruction. |
| Frame orthonormality | `maximum_frame_orthonormality_defect` | Retained on the tensor mesh. |
| Projector reconstruction | `maximum_projector_reconstruction_defect` | Retained separately from frame orthonormality. |
| Parent/retained lifting reconstruction | `maximum_parent_retained_reconstruction_defect` | Retained after identifying the retained space. |
| Parent Fourier reconstruction | `maximum_parent_fourier_reconstruction_defect` | Uses the canonical tensor-product transform. |
| Reciprocal-period frame closure | `maximum_periodic_frame_closure_defect` | Checked along every primitive reciprocal direction. |

These fields are present for every `(case, parent_scale, amplitude)` point. Repeated
parent-only values are retained deliberately so that each point is independently
interpretable after stored-byte admission.

## Frame transport and topology

The periodic-1D primitive-link and closed-loop diagnostics specialize in two dimensions
as follows:

- `minimum_sampled_transport_singular_value`;
- `maximum_transport_procrustes_residual`;
- `maximum_transport_squared_residual_roundoff_cutoff`;
- `maximum_transport_unitarity_defect`;
- `maximum_transport_rank_cutoff`;
- `transport_rank_deficient_link_count`;
- `transport_closure_and_plaquette_applicable` and its stable inapplicability reason;
- `maximum_absolute_closure_holonomy_phases` for the primitive cycles;
- `maximum_closure_holonomy_unitarity_defect`; and
- `maximum_plaquette_holonomy_phase`.

A rank-deficient link makes closure and plaquette diagnostics inapplicable. Missing
values are represented by `None` with the typed reason; they are never replaced by
numerical zeros. The plaquette channel is a genuine periodic-2D addition and has no
one-dimensional counterpart.

## Representation equivalence and restricted alignment

`BandEquivalenceHoppingLocalityRepresentationEquivalenceAnalysis` retains the complete
rank-two comparison channel:

- spatial dimension and retained rank;
- maximum direct ordered-band defect (`maximum_direct_band_defect`);
- maximum covariant operator defect (`maximum_covariant_defect`);
- alignment applicability and inapplicability reason;
- restricted global rotation angle and degeneracy disposition;
- splitting scale;
- finite-mesh maximum correlation;
- analytic flat-parent correlation, its controlled remainder bound, and the finite
  quadrature defect;
- minimum operator threshold;
- exact-spectrum joint operator threshold;
- both thresholds divided by the square root of the splitting scale; and
- normalized squared operator residual (`normalized_squared_operator_residual`).

This is the two-dimensional owner of the donor's band defect, harmonic-correlation,
restricted-angle, threshold, and loss-reconstruction diagnostics. The periodic-1D
`PeriodicHarmonicMaximum` object is not copied: the two-dimensional restricted rotation
is solved for the declared tensor field and retains an explicit degeneracy disposition.

The generic `BandEquivalenceHoppingLocalityLoss` supplements this rank-two point channel with
weighted operator and ordered-spectrum losses normalized by `2 E_ref^2`. It binds the
sample shape and weights, retained-space and basis identifiers, gauge/geometry
identification, energy unit, and positive normalization. Its independent reference uses
scalar matrix-element sums and independently ordered Hermitian eigenvalues. Historical
square execution bytes predate this loss record and remain unchanged.

## Fourier, Nyquist, and locality diagnostics

Every point retains:

- reference and comparison Fourier reconstruction defects;
- reference and comparison Parseval defects;
- reference and comparison twisted tensor-Nyquist defects
  (`reference_twisted_nyquist_defect` and `comparison_twisted_nyquist_defect`);
- reference and comparison ordinary-lattice Hermiticity defects;
- reference and comparison interpolation error channels;
- total, onsite, and nononsite normalized powers for both representations;
- excess and splitting-normalized excess nonzero hopping weight;
- the flat-parent identity departure when applicable;
- reference and comparison Nyquist powers;
- the flat residual-tail identity defect when applicable; and
- minimum and maximum physical basis distances when basis offsets are present.

The donor's displacement-resolved hopping powers become complete physical-metric-shell
powers. `BandEquivalenceHoppingLocalityShellAnalysis` retains, for every complete shell:

- shell index and cumulative retained-block count;
- reference and comparison truncation-only Hamiltonian and ordered-band maximum/RMS
  errors;
- reference and comparison total Hamiltonian and ordered-band maximum/RMS errors;
- reference and comparison shell power;
- ordinary and total omitted powers; and
- reference and comparison truncation Parseval defects
  (`reference_truncation_parseval_defect` and
  `comparison_truncation_parseval_defect`).

Tensor Nyquist classes replace the periodic-1D negative-Nyquist endpoint rule. Complete
physical-metric shells replace absolute integer cutoffs. Equal-radius displacements are
never split.

## Support-selection diagnostics

For each declared tolerance, `BandEquivalenceHoppingLocalityFirstPassingDecision` retains the
minimum stored complete shell for all four support questions:

1. reference ordered-band error;
2. comparison ordered-band error;
3. reference Hamiltonian error; and
4. comparison Hamiltonian error.

Each decision retains the passing error and preceding-shell error. A missing passing
shell remains `None` at the declared cap and means unresolved, not impossible. The
selection is checked through the reusable `RealSpaceSupportTruncationToleranceSelector`;
independent verification reconstructs shell powers and stored decision identities
without treating the production selector as an oracle.

## Parent-family diagnostics

The donor's separate parent-hopping family becomes the ordered `parent_scales` axis in
each periodic-2D request. Every parent scale receives the full qualification, transport,
representation-equivalence, Fourier, shell, and support-decision inventory above.
Cross-scale conclusions are family-owned: square and triangular/honeycomb controls do
not share a conclusion merely because they use the same scale coordinate.

## Amplitude diagnostics

The donor's correlation, operator-threshold, joint-threshold, nonzero-hopping-weight,
and hopping-block-power interpolation channels are retained by
`BandEquivalenceHoppingLocalityAmplitudeMidpointAnalysis`. It records:

- applicability and a typed inapplicability reason;
- endpoint minimum normalized operator threshold;
- maximum correlation midpoint defect (`maximum_correlation_midpoint_defect`);
- maximum operator-threshold midpoint defect;
- maximum joint-threshold midpoint defect;
- maximum nonzero-hopping-weight midpoint defect; and
- maximum hopping-block-power midpoint defect.

For each declared flat-parent resolution level,
`BandEquivalenceHoppingLocalityFlatAmplitudeResolutionAnalysis` additionally retains the number
of intervals and nodes and the operator/joint midpoint defects. The current periodic-2D
requests use a prospectively declared bounded resolution ladder. The periodic-1D
adaptive midpoint/quarter-point stopping algorithm and its numerical thresholds are not
silently transferred: periodic-2D retains the same diagnostic channels but does not
claim the donor's `converged`, level-cap, or sample-cap outcome.

## Momentum-refinement diagnostics

`BandEquivalenceHoppingLocalityRefinementPair` retains all transferable adjacent-mesh channels:

- maximum parent-diagnostic change;
- maximum final parent-invariant change;
- maximum correlation change;
- maximum operator/joint-threshold change;
- maximum nonzero-hopping-weight change;
- maximum shell/block-power change;
- maximum restricted-angle change;
- maximum direct-band-defect change;
- maximum reconstruction-defect change;
- maximum Parseval-defect change;
- maximum first-passing outcome change;
- first-passing-disposition stability; and
- transport closure/plaquette applicability stability.

The record also carries the donor's shared-node eigenvalue/projector diagnostic names,
but explicitly marks them inapplicable. The current half-step Monkhorst--Pack doubling
meshes have no shared nodes, so `maximum_shared_parent_eigenvalue_defect` and
`maximum_shared_projector_defect` are `None` with a stable reason. No family-wide
channel tolerances were prospectively frozen; therefore `within_draft_tolerances` and
the aggregate pass fields are `None`, and the momentum disposition is `unresolved`
rather than `converged`.

## Geometry diagnostics added by periodic 2-D

The periodic-2D specialization also retains diagnostics that are absent or trivial in
one dimension:

- metric-covariance defects under declared lattice probes;
- construction/evaluation tensor-mesh minimum separation;
- physical basis-distance ranges;
- closure and plaquette applicability; and
- plaquette holonomy phase.

These additions do not alter the donor quantities or authorize cross-family
identification.

## Independent verification and retained projection

The direct verifier admits exact stored result bytes and independently reconstructs:

- stored algebraic identities;
- parent fields and retained ordered bands;
- reference/comparison shell powers, omitted powers, and Nyquist powers; and
- the authenticated visualization-data projection.

The generic quadratic-loss verifier separately compares production and scalar-reference
operator and spectral losses at `1.0e-10`. SHA-256 authenticates byte identity only;
neither hash agreement nor passing software tests establish physical validation,
continuum convergence, or publication evidence.

## Strain-family extension

The `strain-locality/` child is not a nominal parent-scale family. Its development
records extend the catalog with geometry, response, witness, scan-envelope, and
transition-bracketing diagnostics. Those values remain separate from the square and
triangular/honeycomb result graphs and currently lack a direct byte-owning lifecycle.

## Availability boundary

This inventory closes diagnostic-name and ownership accounting against the periodic-1D
rank-two donor. It does not assert numerical parity between dimensions. Producing new
periodic-2D numerical rows, retaining new loss or refinement-assessment artifacts, or
creating a new execution still requires a new execution identity and explicit human
authorization.
