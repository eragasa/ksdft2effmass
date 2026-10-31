# Accepted-S1 withheld-parent NSCF and frozen comparison

## Disposition

One explicitly authorized local QE 7.5 `pw.x` Davidson NSCF invocation completed with
return code zero. No retry occurred or remains authorized. The exact 408-point set is
candidate-conditioned, disjoint from the Gamma-origin `4 x 4 x 4` Wannier construction
mesh, and was frozen before observing direct-parent values.

The native occurrence is mechanically eligible for the frozen comparison:

- 408 k points and 12 bands were parsed from QEXSD;
- all eigenvalues and occupations are finite;
- QEXSD order agrees with the frozen manifest to
  `2.220446049250313e-16` in native coordinates;
- `JOB DONE` was present;
- no unconverged-eigenvalue warning was emitted; and
- the 411-file, 108,034,728-byte saved state was verified against its ProjectKoios
  manifest.

The native IEEE flags are retained as diagnostics. They do not block this occurrence
because native convergence succeeded, required values are finite, and no explicit
unconverged-eigenvalue or corruption diagnostic occurred.

## Scientific result

The provider-eligible rank-10 Wannier candidate is **not adequate for the frozen declared
SSSP-pilot intended use**. This does not invalidate its finite representation or change
its provider-eligible status.

| Frozen comparison | Observation | Target | Outcome |
|---|---:|---:|---|
| Indirect gap relative error | `14.5008943372%` | `<= 5%` | not met |
| Six valley-position displacements | `0.02120`--`0.03086 inverse angstrom` | `<= 0.0344650 inverse angstrom` | all met |
| Longitudinal mass relative errors | `4.74%`--`16.43%` | `<= 8%` each | two of six not met |
| Transverse mass relative errors | `31.997%`--`56.459%` | `<= 8%` each | none met |

The parent indirect gap is `0.6112467238614325 eV`; the candidate prediction is
`0.5226104822946773 eV`. On the prospectively declared, identical `0.002 inverse
angstrom` candidate-centered stencils, direct-parent longitudinal mass diagnostics are
approximately `0.962`--`0.976 m_e` and transverse diagnostics are approximately
`0.1925`--`0.2084 m_e`. Candidate transverse predictions are approximately
`0.2624`--`0.3037 m_e`. These are local same-stencil curvature comparisons; the parent
minimum locations themselves come from the separately declared joint quadratic fits.

The descriptive, non-gating injective spectral comparison has RMS error
`0.23706926309836587 eV`, maximum error `0.6955513330349543 eV`, and 95th-percentile
absolute error `0.6472639257309413 eV`.

The candidate predictions were reconstructed from the authenticated operator before
comparison. Their maximum energy discrepancy from the frozen characterization was
`1.4210854715202004e-14 eV`; the maximum reconstructed primary-curvature discrepancy
was below `8.0e-9 eV angstrom^2`.

## Consequence

This candidate must not be accepted as the full Wannier operator for the declared use,
and component-operator construction or Slater--Koster reduction must not proceed from it.
The result supports a prospectively declared construction-adequacy revision rather than
further optimizer tuning. Any revised mesh, rank, bands, windows, or projections define
a new scientific construction and require new preflight and calculator authorization.

## Retained identities

- QEXSD: `792898753c87d92328e6c511259c77c843c3ae59b212c1d8502b3e53563b8fb2`
- saved-state manifest: `8de35151ad55bca4658c472ec51ddd1468902e7ba6e6529d42c6df463f726d20`
- NSCF interpretation: `29d3c50f70b9faa0eed24acf5f0673d43eb666d1216327fdf74e53cdd6176b51`
- frozen validation result: `46f3716e20037187989863fccad9181402a7dc4f4b89e3c143527b10353c7aa6`
- external inventory: `7391a066e51defc7a138251b5d86117c80711d93b6446238b589dcb52ecfffd1`

Large native wavefunction files remain in the authenticated external occurrence root and
are not copied into Git. The retained external inventory covers 435 files totaling
210,171,760 bytes.
