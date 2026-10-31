# `C6-B20-W21` revealed-408 development comparison

## Purpose

This separately authorized S40 no-calculator analysis compares the structurally verified
full untruncated `C6-B20-W21` operator with the already revealed 408-point direct-parent
development evidence. It does not use or reveal the frozen 402-point confirmation
values.

## Frozen oracle-evaluation criteria

The comparison applies the unchanged development targets as parent-fidelity evaluation
criteria:

- indirect-gap relative error no greater than `5%`;
- valley-position displacement no greater than `3%` of Gamma--X, equal to
  `0.03446503626832577 inverse angstrom`; and
- relative error no greater than `8%` for every longitudinal and transverse principal
  electron mass.

These criteria do not use diagnostics available in a deployed reduction. Failure limits
physical-fidelity claims but does not invalidate provider eligibility, structural
reconstruction, or the full operator's role as the fixed controlled-reduction source.

## Comparison method

The analysis binds the exact S30 implementation and characterization result, the
retained revealed-parent validation result, the original 408-point manifest and
criteria, and the authenticated 408-point QEXSD.

- The candidate gap uses the S30 valley energies and the same full untruncated operator
  at Gamma.
- Parent valley locations and primary `0.002 inverse angstrom` Hessians are retained
  revealed-development observations from the frozen 408-point analysis.
- Candidate locations and primary Hessians are the S30 predictions frozen before this
  comparison.
- Valley displacement uses the minimum periodic Cartesian reciprocal displacement.
- Longitudinal directions are selected by signed cubic-axis overlap; transverse axes are
  matched by maximum mutual overlap, exactly as in the frozen parent-comparison method.
- A gauge-invariant injective rank-10-to-12 spectral match on all 408 points is retained
  as a non-gating diagnostic without fitted energy alignment.

No fitting, target-space change, spatial truncation, or model reduction occurs here.

## Run

From the repository root:

```text
PYTHONPATH=python/src:/Users/eugene/worktrees/projectkoios-simulations-pw-dft-wannierization-tranche-1/src/python \
  python/.venv/bin/python \
  calculations/Si/bulk/analysis/c6-b20-w21-revealed-408-development/run_analysis.py
```

The script writes `development-result.json` with KSD's
`TypedJsonMappingSerializer`.

## Result

The full untruncated operator fails the frozen development targets:

- indirect gap: `0.6892447449062074 eV` candidate versus
  `0.6112467238614325 eV` parent, `12.7605%` relative error against `5%`;
- all six valley positions pass, with displacements from
  `0.0190614` to `0.0213373 inverse angstrom` against
  `0.0344650 inverse angstrom`;
- all six longitudinal masses fail, with relative errors from `202.44%` to
  `218.21%` against `8%`;
- eleven of twelve transverse masses fail; the only pass is the `+z`
  `transverse_1` comparison at `7.0718%`; and
- the non-gating injective 408-point spectral residual has
  `0.737286 eV` maximum and `0.246196 eV` RMS error.

Disposition: **fails the parent-fidelity development criteria**. Provider eligibility
and S30 structural reconstruction remain valid. The result is development-oracle
evidence, not an operational rejection of the controlled reduction source. Spatial
truncation and Slater--Koster definitions may proceed only through their separate gated
stages using diagnostics available without the 402-point parent values. Those values
remain unobserved; no `C6-B30`, `C8`, `C12`, target-space change, or calculator
occurrence follows automatically.

| Artifact | SHA-256 |
|---|---|
| S40 corrected implementation | `c555f690fb0d6a7517bd61bcc3abee5acc30fc337e0bd3add358593f9b8f2952` |
| Initial linear-gate disposition | `fbd9ab474328323f43d03754d01a0a9be115ea30739c1a4ac65ca47767d99459` |
| Hidden-oracle role correction | `29e58f90c40ec428e12d087b4d6b6b70bfcd18d9c539bdcd9f17aa3dd36f333d` |
| Corrected S40 development result | `bb1a6d0fab5d08fecaa0d86cbfe00e8670e7f089e289c6fabc59c32c6f76991d` |
