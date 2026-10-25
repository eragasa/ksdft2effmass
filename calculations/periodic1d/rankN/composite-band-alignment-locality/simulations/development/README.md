# Schema-free development simulation

`run_development.py` executes the complete finite rank/depth inventory through the canonical `HigherRankD1Calculator` and writes an ignored summary under `results/`.

`verify_analytic_controls.py` samples the declared isolation-energy and attack-angle formulas. It is a finite-grid sanity check, not the missing full-result verifier and not a proof.

From the repository root:

```bash
python/.venv/bin/python calculations/periodic1d/rankN/composite-band-alignment-locality/verify_analytic_controls.py
python/.venv/bin/python calculations/periodic1d/rankN/composite-band-alignment-locality/run_development.py
```

The complete producer can be resource intensive. Its output is replaceable development data and must not be promoted without strict schemas, independent verification, provenance, and separate authorization.
