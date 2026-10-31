# Withheld-parent tolerance authority review

## Question

Which observations can decide whether the provider-eligible Wannier operator is
adequate for its declared use, without inventing thresholds from the candidate's own
behavior?

## Authority findings

The physical specification requires the non-SOC bulk pilot to retain the indirect
Kohn--Sham gap, conduction-valley position, longitudinal electron effective mass,
transverse electron effective mass, and withheld-point band errors. It does not assign
numerical tolerances.

The ICMSEP2026 publication program prospectively states spectral targets of:

- `5%` for the indirect gap;
- `3%` of the Gamma--X reciprocal distance for the conduction-valley position; and
- `8%` for each electron effective mass.

Those targets are tied to the declared bulk-silicon reduction use. They therefore give
an intended-use basis for the parent-versus-Wannier gap, valley, and mass comparisons.
This is a necessary screen, not an arbitrary fractional allocation of an additive error
budget: any later Slater--Koster reduction must be compared directly with its parent
under separately bound criteria. Passing the Wannier screen does not reserve or certify
a reduction-error allowance.

The target source anticipates the final PseudoDojo branch, whereas this occurrence is
the separately identified SSSP pilot. Applying the spectral targets here does not
satisfy the PseudoDojo or independent-toolchain gates. The targets are not claims that
the operator is intrinsically right or wrong. Exceeding one means only that the
candidate is inadequate for this declared pilot use under that target.

No reviewed source in the active calculation assigns a maximum or RMS tolerance to the
complete withheld spectrum. The rank-10 candidate and rank-12 parent are not the same
finite representation, so their descriptive comparison uses gauge-invariant injective
spectral matching and never subtracts unaligned operators. Those residuals must be
reported without a binary disposition. They cannot be converted into a new threshold
after observing the parent values.

## Adopted prospective criteria

Before any direct-parent values are observed, this preflight binds:

| Quantity | Metric | Intended-use target |
|---|---|---:|
| Indirect gap | absolute relative parent/Wannier error | `<= 5%` |
| Valley position | Cartesian reciprocal displacement of matched minima | `<= 3%` of Gamma--X |
| Longitudinal mass | absolute relative error at every matched valley | `<= 8%` |
| Each transverse mass | absolute relative error at every matched valley | `<= 8%` |

For the accepted relaxed lattice parameter `5.469182093640207 angstrom`, the Gamma--X
distance is `1.1488345422775257 inverse angstrom`; the position target is therefore
`0.03446503626832577 inverse angstrom`.

The parent valley location uses a joint quadratic fit on Cartesian reciprocal points at
radii no greater than `0.010 inverse angstrom` around each frozen candidate center. The
gating mass comparison uses parent and candidate three-dimensional fits on the identical
`0.002 inverse angstrom` stencil, matching the primary scale already frozen in the
candidate characterization. Fits at `0.005` and `0.010 inverse angstrom` remain
sensitivity observations. Longitudinal and transverse masses are assigned by
principal-direction overlap with the matched signed cubic valley axis, and the full
tensor and coordinate basis remain reported.

Injectively matched spectral residuals, valley-energy spreads, local gradients, fit
residuals, condition numbers, and stencil sensitivity remain mandatory reported
observations but are non-gating until a separate authority supplies a prospective
intended-use target. The indirect-gap comparison uses the authenticated existing
Gamma-point parent VBM as a construction-point support datum; only its conduction
minimum is newly withheld.

## Inconclusive outcomes

The comparison is inconclusive rather than failed if the sampled domain does not
contain the matched parent minimum, the local fit is rank deficient or unsuitable, the
conduction band cannot be tracked, required eigenvalues are nonfinite or unconverged,
or a relative metric has a zero denominator.

These criteria do not authorize `pw.x`. They become applicable only to the exact
withheld set and exact input bound by this preflight.
