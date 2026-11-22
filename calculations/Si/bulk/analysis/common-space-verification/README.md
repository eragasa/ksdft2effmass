# Retained independent common-space verification

## Authority and scope

The current human operator authorized the recommendation to execute independent
CSD1-V: authenticate the complete real evidence bundle, compute the existing
216-point Gram route, retain its independent result, and only then correlate the
original producer bytes. This is not authorization for CSD2/CSD3, HF gates, a new
window/successor, Quantum ESPRESSO, Wannier90, fits, commit or push.

**Run 002 passed numerical verification and producer correlation under the declared
source/finite-precision contract.** This is independent numerical reconstruction,
not an independent human review, physical/material validation, or production
qualification of the historical SSSP parent. The [adopted source interpretation](../../protocol/decisions/s30-state-identification.md)
and its lineage/backend-frame/rounding assumptions remain unchanged. Native and
nominal geometries are not declared equal; nominal dimensional diagnostics are
not relabeled. No off-mesh KS embedding is claimed.

## Actual result

The existing independent implementation reconstructed `B` using exact rational
arithmetic after the shared native parsing boundary and certified the Gram/eigen
route with binary64 eigensolver candidates and exact residual/frame bounds.
It did not import producer reconstruction, rank, vector, weight, comparison or
serialization implementations. The case runner imports only verifier/native-boundary
APIs. Producer numerical JSON was decoded only after the independent result existed.

All **216 points were conclusive**, with **214 resolved rank-ten points and two
resolved rank-nine points at indices 0 and 12**. The raw threshold remains the exact
binary64 value of `5.890206739032098e-7`; it was not replaced by a normalized gate.
Both deficient minimum directions have enclosed atomic/group weights. All 216
native/parse coverage checks and all 216 fixed retained-basis unitary controls passed.
Post-computation correlation reports **zero mismatches** against the actual
[producer run](../common-space-producer/).

Approximate displays of maxima over the retained exact rational bounds are:

| Quantity | Approximate maximum |
|---|---:|
| Native printing contribution | `9.384375299741157e-9` |
| Binary64 parsing contribution | `3.432720170340462e-15` |
| Eigenframe orthonormality defect | `5.757754269662233e-15` |
| Gram spectral error bound | `1.0117996239201401e-13` |
| Eigenpair residual bound | `2.9231467293745794e-14` |

These are dimensionless numerical bounds, not parent-solver, geometry, physical
fidelity or model-reduction error estimates. Exact endpoints are in the retained
JSON as reduced hexadecimal rational pairs. Hermiticity defect bounds are exactly
zero for the exactly formed Gram matrices. The scalar displays above are not new
verification tolerances or outward-rounded replacements for those endpoints.
Weights remain atomic-trial-coordinate diagnostics, not populations or physical Si4s
identification. Exact physical orthogonality at Gamma remains input-limited.

No arithmetic escalation was triggered. The non-arithmetic adapter issue described
below was repaired without changing inputs, arithmetic kernels, bounds or threshold.
The verified rank stop still forbids a resolved global rank-ten atomic alignment
from this unchanged source under the frozen gate; no fit or successor is activated.

## First attempt, explicit linkage repair, and replay

[Run 001](run-001/) completed and retained all 216 independent point results, but
post-computation correlation stopped with `producer request state space differs
from reviewed source contract`. Its [log](run-001/execution.log), independent result
and original manifest are preserved. The prior adapter source was recovered by
reversing only the verified linkage patch and authenticating the resulting bytes
against that original manifest: [exact prior source](run-001/comparison-adapter-before.py.txt),
SHA-256 `a6715bbd715423366c53fbb7124c57134eeef5821027834c85366bd0e8e1ef13`.
No correlation or pass was added to that attempt.

The adapter had compared **legacy human-readable request descriptions** directly to
**content-addressed declaration identifiers** in different wire fields. The repair
in `common_space/verification/producer_result.py` requires an explicit declaration
link for retained sources: matching review scope, the exact authenticated source-
assertion identity, effective geometry identifier and complete seven-module parser
binding. The declaration already binds both effective geometry/energy-reference IDs
and the exact reviewed request hash. Literal producer descriptions are then compared
to that authenticated request; dimensions, basis, spin, units, points, precision,
threshold and numerical comparisons remain exact or within the existing certified
intervals as appropriate. Missing or unequal links fail; unlinked descriptions are
not aliases. No historical request, assertion, result or protocol was rewritten.

[Run 002](run-002/) replayed the same numerical route into a fresh root with the
corrected adapter. The two independent JSON results are **byte-identical**. Its
independent record deliberately retains `independent-result-complete-pending-comparison`:
the separately written [correlation](run-002/producer-correlation.json) supplies the
subsequent outcome without rewriting that independent record.

A later additional launch at the same root was correctly rejected **before admission
or arithmetic**; its [rejected-repeat log](run-002/rejected-repeat.log) is retained.
That check replaced a scratch stdout redirect, so the [successful stdout](run-002/execution.log)
was recovered verbatim from this session's actual successful tool result. No other
writer or calculation was inferred from the existing root, and no third numerical
run or overwrite occurred.

## Identities and reproduction

| Artifact | SHA-256 |
|---|---|
| Independent JSON, both attempts | `3ed6f7bb54086ac8005acea8c34a9a47c475b14878618da4b5c6eaa01ac532ee` |
| Run 001 manifest | `c1e3900a531e53c275938448bd4c5db29e864f8a00060edd38056f9c882e1f93` |
| Run 002 manifest | `9db48ea644da434c60205542837a103669193fb23020067e5024fff3b61da3de` |
| Run 002 correlation | `c1979a548d41ddb3de81e398d5317972029d47fab1c6d30dae1d2405295b5d72` |
| Case runner | `af0e7d9d44ce4360b0f33ea84ea567cd52b76a48e31a4aefc704b9f41118b05e` |

Each independent JSON is 3700679 bytes of interval/residual/source metadata, not
wavefunctions or dense Hamiltonian output. Manifests bind its bytes and all verifier
module sources. The correlation binds the saved independent bytes/manifest and the
unchanged 189612-byte producer result, SHA-256
`761d58b83a43a9544ad2aae1872ef91cd4ef5387dbae9a6db169a32ee5498dd8`.

Observed runtime environment: local Python 3.14.6, NumPy 2.5.1, macOS arm64, and the
existing pinned Simulations native boundary. Dependencies/lockfile and HEAD
`dac209a60aec502ae05fe84abd0c5eca23d3b4df` are unchanged. The checkout remains dirty;
HEAD alone does not identify executed implementation bytes. Source hashes do not
attest historical calculator builds, a running process, scientific acceptance or
execution authority.

The [case runner](run_verification.py) composes existing APIs; it is not another
parser/verifier or a reusable package. It authenticates the nine real evidence roles,
all 16 adopted source paths, the adopted decision, and the exact shared ordered native
records. It never regenerates assertions/completion evidence. Its literal external
paths include the explicitly adopted EIG relocation, not a missing-path fallback.

After applicable authorization, from the repository root:

```console
PYTHONPATH=calculations/Si/bulk python/.venv/bin/python \
  calculations/Si/bulk/analysis/common-space-verification/run_verification.py --check-only

PYTHONPATH=calculations/Si/bulk python/.venv/bin/python \
  calculations/Si/bulk/analysis/common-space-verification/run_verification.py \
  --output-root /tmp/FRESH-common-space-verification
```

The first command authenticates/parses only. The second requires a nonexistent root
and computes the whole field before correlation. No transaction/hostile-filesystem
hardening, automatic source relocation, typed-result resumption, or permission is
provided. Failure may leave partial fresh artifacts; existing outputs are never replaced.

Checks: **160 affected tests** (66 arithmetic/error-bound, 45 correlation, 45 source/
protocol/independence, four retained-certificate contracts), strict mypy, Ruff and
Sphinx warnings-as-errors. Tests establish their named software/retained-byte behavior,
not physical validation. Original producer/checkpoint/statement/review/declaration,
protocol/request/S110, dependency and 67 archive identities are preserved.

**Next boundary: CSD2 retained symmetry-data diagnosis, not run here.** Geometric index
stars and the numerical rank diagnosis do not supply authenticated parent/trial/
Wannier symmetry actions, irreps or sector projectors. CSD3 and HF0–HF4 remain separate
prerequisites; no candidate window or successor has been selected.
