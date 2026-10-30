# Authenticated producer bytes

These files preserve the exact producer-script bytes authenticated by the immutable
`script_sha256` fields in this unsealed execution's `execution.json`,
`verification/verification.json`, and `figures/rendering.json` records.

They are retained provenance, not the current executable source surface. The source
scripts at the calculation root have since changed with the analyzer → plain analysis →
recorder architecture and must not be substituted for the historical producer bytes or
used to rewrite this execution's authentication records.

SHA-256:

- `run_01_calculation.py`: `ed7efc16dc32100fbf3de413feaddbe20857d8adedf11f763590548022fba29b`
- `run_02_verification.py`: `997c89707333861c3172dff4f469b0762f2da1fd67942f424471d2a838a62ef6`
- `run_03_render.py`: `f3299287cde521c7297e53e6e483713148331375e4185245748585a1b2eeda46`

Hash agreement authenticates byte identity and integrity only. It does not establish
scientific validity, convergence, material relevance, publication acceptance, sealing,
or evidence promotion.
