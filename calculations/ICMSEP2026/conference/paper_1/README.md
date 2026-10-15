# ICMSEP 2026 Conference Paper 1 controlled calculation

This directory retains the direct low-dimensional admissible-set demonstration,
separately scoped M1/M2/M3 child packages used by Conference Paper 1, and draft
plans for additional controlled studies.

## Evidence class

The parent result is **controlled illustrative numerical verification** for a
synthetic one-dimensional scalar Hamiltonian. M1--M3 remain synthetic. The
`silicon-wannier-kinetic-preview/` child is instead a bounded publication
extraction from a read-only analysis of the official Wannier90 3.1.0 silicon
tutorial setting. It is not production silicon validation, and creating the
preview executed no protected electronic-structure calculator.

## Files

- `input.json` — frozen parent, candidate class, losses, thresholds, roles, and figure settings;
- `protocol.md` — mathematical and evidentiary contract;
- `run.py` — result and figure constructor;
- `result.json` — retained machine-readable outcomes and certificate data;
- `verify_result.py` — independent reconstruction that does not import `run.py`;
- `boundaries.csv` — figure boundary samples, not the source of the certificate;
- `admissible-sets.png` — publication figure;
- `report.md` — bounded human-readable findings;
- `software.json` — repository and runtime identities; and
- `SHA256SUMS` — identities of the retained direct-demonstration files;
- `isolated-band/` — prospectively frozen M1 isolated-band evidence; and
- `multiband-alignment/` — prospectively frozen M2 rank-two alignment and locality evidence;
- `constrained-admissible-sets/` — prospectively frozen M3 witness-and-certificate evidence; and
- `constrained-admissible-sets-threshold-sensitivity/` — explicitly post-hoc analytic sensitivity reanalysis of the sealed M3 quadratics;
- `hopping-shell-hierarchy/` — draft, unexecuted plan for a certified nested two-dimensional hopping-shell hierarchy intended to replace the generic 2D summary figure if later frozen, executed, and accepted; and
- `silicon-wannier-kinetic-preview/` — bounded original-tutorial-file correlation, executed Wannier90 input diff, source JSON, finite-mesh truncation figure, and checksums for the preliminary material-facing preview.

## Reproduce and verify

From the repository root:

```bash
python/.venv/bin/python calculations/ICMSEP2026/conference/paper_1/run.py
python/.venv/bin/python calculations/ICMSEP2026/conference/paper_1/verify_result.py
```

The retained outcomes are:

- an exact common witness for the complete-mesh objective; and
- a certified separated case with
  $0.452\leq\delta^\ast\leq0.500$ for the restricted-training objective.

Both statements are relative to the frozen model class, thresholds, alignment family,
and finite domains.
