# C6-B20-W21 independent numerical-convention audit

This calculation-local audit addresses two implementation-level checks raised during
continued manuscript review without invoking the silicon producer calculators.

1. It independently recomputes the single-valley and six-valley density-of-states and
   equal-population conductivity-mass conventions from the retained primary mass and
   inverse-mass tensors.
2. It reconstructs the complete size-six centered-cyclic displacement inventory and
   the exact cyclic-to-ordinary selection ledger, then checks the retained 125-mode
   ordinary inventory, FCC metric labels, physical radii, and displacement powers.

The script imports no `ksdft2effmass` producer or verifier. It consumes only authenticated
retained JSON results and uses direct NumPy linear algebra plus integer enumeration.

This is an **independent convention and inventory audit**, not a complete independent
reconstruction of the silicon Hamiltonians. In particular, the historical gauge result
does not retain the 216 cyclic coefficient matrices, so this package does not
independently reconstruct their values or the power carried by the 91 removed Nyquist
records. Complete rank-10 Fourier reconstruction remains a publication blocker.

Run from `python/` into a fresh directory:

```bash
uv run python \
  ../calculations/Si/bulk/analysis/c6-b20-w21-independent-convention-audit/run_audit.py \
  --output-root /tmp/c6-b20-w21-independent-convention-audit
```

The script refuses to overwrite any retained output.
