# Retained CSD1 producer checkpoint

## Authority and scope

The current human operator authorized the recommendation to complete/test the
missing calculation-local point inventory, authenticate the adopted source inputs,
and execute the unchanged 216-point no-calculator reconstruction. A subsequent
“continue” continued that work. This authorization does **not** include independent
CSD1-V execution, CSD2/CSD3, HF gates, a successor/window selection, calculators,
fits, commit, or push. The unchanged development request remains data, not execution
permission. This README does not authorize another execution.

The producer consumed the [adopted complete-S30 identification](../../protocol/decisions/s30-state-identification.md)
and the existing [source-state declaration](../wannier-window-remedy/source-state-assertions.json).
The complete fixed HR/WSvec model and its native retained-space interpretation on
216 source indices remain distinct from the nominal-geometry dimensional diagnostics.
All 16 explicitly adopted source paths plus the decision/declaration matched their
identities; the seven-module shared native boundary matched exact dimensions and all
216 declared coordinate presentations before products. The producer then used its
own direct SVD implementation, not verifier arithmetic or S110's calculation code.

## Actual producer result

[Run 001](run-001/) completed and retained all 216 point records:

- **214 resolved rank-ten points; two resolved rank-nine points**, at indices 0
  (Gamma) and 12 `(0,1/3,0)` in construction-index notation.
- Raw nominal minima: `5.361015757842935e-13` and `2.018656234207826e-7`.
  The frozen raw threshold remains **`5.890206739032098e-7`**; no normalized gate,
  pseudoinverse, rank reduction, deleted direction or window change was used.
- The native-bound comparison and retained-subspace unitary-invariance control passed
  the existing producer criteria. This is producer agreement with the retained S110
  comparison, **not independent numerical verification** or physical validation.
- Disposition remains `blocked-orbital-alignment-rank-deficient-no-fit`.

The [point inventory](run-001/point-inventory.json) contains all **48 geometric
operations**, their complete 216-index permutations, and **16 disjoint index orbits**.
For the adopted executed cell `D=c*P`, each Cartesian signed permutation `R` gives
`M=P^-1 R P` and `Q=M^-T`. Exact integer arithmetic checks lattice preservation,
direct/reciprocal duality, and the identical-Si motif `{0,tau}`, `tau=(1/4,1/4,1/4)`,
with the required translation either zero or `tau`. This is not a claim that QE's
sampling metadata supplies electronic symmetry representations.

Gamma's index star is `{0}`. The index-12 geometric star is
`{2,4,12,24,72,86,144,172}`; **only index 12 fails the raw gate in that star**.
Each member's actual producer diagnostics is retained, without assuming rank invariance.
This nonuniform index-star pattern does not establish physical symmetry breaking,
an irrep, or a symmetry-sector mismatch.

These are **geometric construction-index relations**, using `Q*n modulo 6`, not
asserted exact physical-k equivalences of rounded native presentations. The original
native coordinate floats are retained unchanged. Each operation records its maximum
printed/binary64 coordinate-component residual as an exact hexadecimal rational;
the largest observed value is about `1.000000082740371e-10`. It is not rounded away,
compared against a borrowed gate, or declared a physical-k error bound. No Bloch,
trial, or Wannier action, nonsymmorphic phase, character or sector projector is supplied.
The completion receipt's inventory flag means exhaustive enumeration at this stated
index-domain scope, **not CSD2 symmetry authentication**.

## Retained artifacts and continuation

The five core files total **400643 bytes**:

| Artifact | SHA-256 |
|---|---|
| [result.json](run-001/result.json) | `761d58b83a43a9544ad2aae1872ef91cd4ef5387dbae9a6db169a32ee5498dd8` |
| [point-inventory.json](run-001/point-inventory.json) | `fd23080496ee077e967631a1cf4258301f4efc41d045557a03365d8bcaed19c7` |
| [producer-completion.json](run-001/producer-completion.json) | `0d03312dea85e6881fa432ee15f402ab9d0011e9312bfff749dcf2dc9d28c452` |

The [manifest](run-001/manifest.json) binds the core output bytes, unchanged request,
entrypoint and all three producer implementation modules. The
[human-readable transcript](run-001/human-readable-summary.txt) reports the stages.
Completion was persisted only after the actual result and inventory files existed
and matched their produced bytes. Saved checksums and copied star rows were checked
against the actual deliverables. This is integrity checking, not a second numerical route.
No manually normalized replacement for the original producer schema was introduced.

The shared local [native-input boundary](../../common_space/verification/native_inputs.py)
remained unchanged at SHA-256
`4757593fd187445031de13a07aa47779761033f52c4e60961ec4f80d19fde6a9`.
This shares authentication/parsing/immutable records only, not verifier arithmetic.

The run used local `.venv` Python **3.14.6**, NumPy **2.5.1**, and the pinned
`projectkoios-simulations==0.1.0.dev0` native boundary on macOS arm64. These runtime
versions were observed in the same environment immediately after execution; they do
not attest historical QE/Wannier executable builds. Dependencies and lockfile were
not changed. HEAD remains `dac209a60aec502ae05fe84abd0c5eca23d3b4df`; the checkout is
**dirty**, so HEAD alone does not identify executed code. Individual manifest module
hashes identify its actual uncommitted implementation bytes.

Affected software checks: **123 tests**, strict mypy, Ruff and Sphinx warnings-as-errors.
These include synthetic geometry/group-closure checks, actual synthetic producer JSON
adaptation, independent-verification software contracts and four saved-result contracts.
An earlier broad common-space suite exceeded its 180-second command window; a subsequent
combined run exposed the now-fixed synthetic-route regression before also timing out.
The affected suites were rerun successfully after that fix; no full-suite pass is claimed.

**Subsequent checkpoint:** the separately authorized [independent CSD1-V run](../common-space-verification/)
now authenticates the complete real bundle and verifies/correlates all 216 points under
the declared source/uncertainty contract. This producer's artifacts remain unchanged.
CSD2 electronic symmetry diagnosis is the next boundary, not run; CSD3 and later gates
remain stopped.
Native-input uncertainty and modeled-backend assumptions retain their adopted meanings;
this result does not establish exact physical orthogonality at Gamma or production
qualification of the historical SSSP parent.

## Reproduction recipe

After applicable authorization, with all explicitly bound source paths and manifest
implementation hashes available, use a **fresh** output root:

```console
PYTHONPATH=calculations/Si/bulk python/.venv/bin/python \
  calculations/Si/bulk/analysis/c6-b20-w21-slater-koster-definition-fit/run_common_space_diagnosis.py \
  --request calculations/Si/bulk/analysis/c6-b20-w21-slater-koster-definition-fit/common-space-diagnosis-request.json \
  --source-declaration calculations/Si/bulk/analysis/wannier-window-remedy/source-state-assertions.json \
  --output-root /tmp/FRESH-csd1-producer-root
```

The case-specific external paths remain literal. The EIG copy is the explicitly
adopted relocation, not a silent fallback for the absent historical S30 relative path.
No general portability, transactional persistence, hostile-filesystem hardening or
replayability of the old S30 script is claimed; partial failed fresh outputs may remain.
