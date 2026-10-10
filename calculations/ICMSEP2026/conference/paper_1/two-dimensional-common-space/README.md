# M4 two-dimensional common-space comparison

This directory contains the **draft, unexecuted protocol** for M4. It specifies
a local synthetic comparison of two-dimensional plane-wave and finite-difference
Hamiltonians after explicit transport to a common finite state space.

## Current status

- Protocol: drafted, not frozen.
- Input: deterministically generated from `configuration.toml`.
- Implementation gate: blocked; the maintained square-cell comparator must be
  generalized to the declared nonorthogonal geometry and strict M4 document
  contracts must be implemented.
- Calculation: not executed.
- Scientific result: none.

The square cases are historical regression/reconciliation controls. The skew
cases are prospective synthetic numerical-verification cases. Neither is
material validation.

## Files

- `configuration.toml`: editable protocol controls.
- `build_input.py`: strict deterministic input generator.
- `input.json`: generated canonical input.
- `protocol.md`: mathematical, computational, verification, and claim contract.

Regenerate or check the canonical input from the repository root:

```bash
python/.venv/bin/python \
  calculations/ICMSEP2026/conference/paper_1/two-dimensional-common-space/build_input.py
python/.venv/bin/python \
  calculations/ICMSEP2026/conference/paper_1/two-dimensional-common-space/build_input.py \
  --check
```

These commands only parse local configuration, verify identities of retained
repository files, and write/check `input.json`. They do not execute M4 or any
external calculator.

Do not create `protocol-freeze.json` or run a confirmatory calculation until the
implementation gate in `protocol.md` is satisfied and reviewed.
