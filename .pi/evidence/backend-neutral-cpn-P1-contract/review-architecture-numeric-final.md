**PASS**

- Ownership preflight passed for P1.
- `tokens.py` REAL constructor accepts exact built-in `int`/`float`, canonicalizes through binary64 `float`, and rejects overflow or nonfinite results.
- `cpn-contract.schema.json` uses:
  - integer branch bounded inclusively by
    \(L=2^{1024}-2^{970}-1\);
  - general-number branch bounded inclusively by maximum finite binary64
    \(M=2^{1024}-2^{971}\).
- Therefore integer-valued REAL accepts `M+1` and `L`, while `L+1` is rejected; noninteger numbers cannot exceed \(M\).
- `SV-CPN-087` states and exercises these boundaries, including both signs and strict JSON rejection of nonfinite constants.
- Numeric paragraphs in the specification README and concept/API/verification documentation consistently state the same contract.
- Strict JSON excludes `NaN`, `Infinity`, and `-Infinity`; direct in-memory validator behavior for `nan` is explicitly outside the wire contract.

No files were edited. The checksum verification was not rerun.
