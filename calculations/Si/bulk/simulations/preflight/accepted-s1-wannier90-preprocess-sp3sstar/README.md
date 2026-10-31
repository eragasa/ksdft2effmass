# Accepted-S1 first Wannier90 preprocessing preflight

This directory retains the dry-run preflight for the first neighbor-topology
qualification candidate using the authenticated Davidson NSCF saved state.

The exact declaration uses:

- Wannier90 3.1.0, seed `silicon`;
- 12 parent bands and `num_wann = 10`;
- separate `Si:sp3` and `Si:l=0:r=2` declarations, producing four nodeless
  hybrids plus one nodal s-like trial projection per Si atom;
- the source-ordered unreduced `4 x 4 x 4` grid;
- outer window `[-5.85, 19.02] eV` in the native QE Kohn–Sham eigenvalue reference,
  enclosing all 12 Davidson-QEXSD bands;
- no frozen window;
- 100 localization iterations, `1.0e-10 angstrom^2` tolerance, and window 3;
- 200 disentanglement iterations, `1.0e-10 angstrom^2` tolerance, window 3, and
  mixing ratio 0.5; and
- `write_hr = .true.` for the later localization occurrence.

[`silicon.win`](silicon.win) was rendered and authenticated using the maintained
ProjectKoios `Wannier90PreprocessingInput.render()` and `.prepare()` surfaces. The
exact bound decision document is retained as
[`wannier-interface-decision.txt`](wannier-interface-decision.txt), SHA-256
`00ba0cb19789ff7349bf3b37784c4222eba758f90dd5be9d28c368763a892015`. No
calculator was executed.

## Projection correction

An initial unexecuted preparation used the compact spelling
`Si:sp3;l=0:r=2`. Source inspection established that Wannier90 applies the trailing
`:r=2` to every angular state on that line, which would make the hybrids nodal as well.
The superseded input and disposition are retained as
[`superseded-compact-projection.win`](superseded-compact-projection.win) and
[`preparation-attempts.json`](preparation-attempts.json). No calculator consumed it.

## Integration limitation

ProjectKoios revision `e146f3722e87ca2de2243421a94448cfa6e27037` supplies pure
rendering/preparation and bounded NNKP parsing, but not the planned first-party
preprocessing execution provider. The preflight therefore records this implementation
gap explicitly. Any authorized occurrence must still use the protected single-attempt
calculator executor, retain exact streams and outputs, and apply the maintained NNKP
parser and semantic checks.

The current PhysKit package exports the operational unit converter singleton while the
retained ProjectKoios tranche imports its former class name. Preflight used a local
runtime alias to that public singleton; neither dependency was modified.

## Authorization state

Status: **authorization consumed by one occurrence**.

Exactly one single-process `wannier90.x -pp silicon` invocation was performed with
zero retries. It returned zero, produced a bounded parseable `silicon.nnkp`, matched
the source lattice and ordered k points, and expanded the intended rank-10 projection
inventory. Compact evidence is retained under
[`../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-preprocess-sp3sstar/`](../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier90-preprocess-sp3sstar/).

This does not authorize `pw2wannier90.x`, localization, or any retry.
