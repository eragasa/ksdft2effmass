# M3 constrained admissible sets

This retained package evaluates two threshold pairs for a compact two-parameter
family of rank-two represented Hamiltonians. It composes the frozen M2
multiband-alignment input and uses only a finite family of one-global real
rotations.

`configuration.toml` is the human-readable scientific configuration.
`build_input.py` verifies the referenced M2 input digest and materializes the
self-contained canonical `input.json`. Run

```console
python build_input.py --check
```

to verify that correlation without rewriting retained input.

The prospectively frozen procedure is in `protocol.md`; its pre-execution seal
is `protocol-freeze.json`. After execution, `run.py` produces the result,
library-verification summary, figure data, figure, report, and software record.
`verify_result.py` independently reconstructs the finite protocol without
importing producer Actions and writes `standalone-verification.json`.
`source.sha256` binds the exact implementation inputs, and `SHA256SUMS` binds
the retained package bytes. The numbered amendment chain records every
post-freeze correction; amendment 9 records adversarial verifier hardening that
changed neither the scientific controls nor the retained numerical result.

Training and evaluation roles are strictly separated. The inherited 257-point
staggered evaluation mesh uses the M2 offset `1/(N+1)` and is disjoint from the
64-point training mesh. Evaluation values cannot alter models, frames,
thresholds, witnesses, certificates, ranges, or dispositions.

The calculation is local and synthetic. Passing verification establishes
bounded software and numerical behavior for the frozen finite protocol only.
It is not material validation, uncertainty quantification, continuum
convergence, proof for arbitrary nonconvex alignment families, or scientific
acceptance. SHA-256 identifies bytes and does not establish chronology.
