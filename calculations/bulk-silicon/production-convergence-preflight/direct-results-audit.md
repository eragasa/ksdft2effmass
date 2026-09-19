# Direct-results audit and provisional finite-setting analysis

**Status:** Provisional calculated and numerical-verification evidence from the
identified direct bootstrap execution. This audit does not accept convergence,
select a cutoff or mesh, establish an infinite-basis limit, classify the recurring
IEEE warning, provide scientific validation or uncertainty quantification, or
retrospectively represent the execution as a canonical `ScientificWorkflowRun`.

The human approved the direct-results-first strategy with the verbatim response
`yes`. The completed direct matrix is therefore audited before considering any new
execution. Re-execution solely to reproduce the matrix through the scientific
harness is not required.

## Retained execution boundary

- Absolute retained run root:
  `/Users/eugene/projects/ksdft2effmass-runs/bulk-silicon-production-convergence-20260813T021128Z`
- Portable historical descriptor:
  `ksdft2effmass-runs/bulk-silicon-production-convergence-20260813T021128Z`
- Descriptor SHA-256:
  `9d84848b4abb0db89e70fa8f6af2dc5f94b122d9574397e60398986638b91bb5`
- Boundary commit: `64de888ad54c1385941a0485433974342380094d`
- Observation commit: `e9c6a1453a6a9dfac8c13256d7d146f6b6ec1716`
- Executable: Quantum ESPRESSO `pw.x` 7.2 at
  `~/projects/q-e-qe-7.2/build/bin/pw.x`, SHA-256
  `6e8720e74cbafa7c7f07ee61ec6f5944c15d59bffa8ee8423fae14364f21c8ca`
- Runner: 4,292 bytes, SHA-256
  `5a193e4f1d93ffc309b7bdf3f9727372da436633a3f2fd262ebb6bf4692dde37`
- Ordered-input manifest: 1,732 bytes, SHA-256
  `cdb6a41cf266034dc7e7b3ed5f48006bbd7caef3ca815849919f1732934407be`
- Execution pseudopotential copy: 225,602 bytes, SHA-256
  `39822757f53f36e3bf3bfb779356152a8d3f21199c7db9dd5a931e5d18c45282`

The run receipts contain start `2026-08-13T13:14:44Z`, end
`2026-08-13T13:15:30Z`, and runner exit status `0`. The nine unique cases are
`C30`, `C36`, `C42`, `C48`, `C54`, `C60`, `K6`, `K10`, and `K12`. Logical mesh
candidate `K8` reuses the complete `C48` SCF and linked diagnostic NSCF and was not
rerun. Every unique case has one SCF and one linked diagnostic NSCF: 18 `pw.x`
invocations, all with one `JOB DONE.` marker and no retry. The primary text-output
identities are:

| Case | SCF output SHA-256 | Diagnostic NSCF output SHA-256 |
|---|---|---|
| C30 | `beea377403441fb3991da8bb43a8f11b4ceb0dfcb2f06169ac98413f4fcdf516` | `38cc66df4ade533892efe656fbb521f7b7883c9f05e2291f9570079af02bb965` |
| C36 | `d2ef0d6c8de145426fa038fff828e2014a8cc780bf0b9ebef66bb77baad47ce0` | `4a4df35f7f1149b3e9a4e860906fcb8b6f8e96fb79120a05856002e7a847086c` |
| C42 | `1919944412bbf2070bc52a5419190d8af86b318cea5e7b86a4d1680b574a6ad3` | `fb80b3cbbdc3ac7c5e3a26c6e66f8cd5d1cb5ae3177d4b20f2a17dd7b06f1c25` |
| C48 / K8 | `994c555388403256752b68b9f320dcf7ffb9917e7dcb7cb6e93d9a06153f65df` | `8c421ec24e43ed8eaf2244f2fa599163b1aacf70d92a648b024135e0abba7228` |
| C54 | `18a8a902232958e38d08d8ef341d121408ee1128d86b4454d9e90f63e8c2b258` | `ffe5115e2b5293835c7a299f9cc5ba1572af50663143e24366162eae4bd1396c` |
| C60 | `e00838526c557ff45a21a95b8e2c7579a4bafadeccf0657978d7c4fbc746d570` | `dfd49924642e80e271eef0219a6f89e2d4aa02d966bbeea6c9df600d3cdaac54` |
| K6 | `8d6aa55e564e469ca4e1d67bd82970f06595fc202800b498c2a1dab951d4316b` | `5fcc5d57bb41cc514fb145387511eb00696baf27fae74f290a22ec9c04f60eb3` |
| K10 | `9eb6d0d5693c3e1055bcc3feb376a07330fe23c0abdc4fb09760ec61d8a53920` | `f9350586d99c1022a892abb4733a00787cce9ebba1f0fee1e9525ab0ffbdca5b` |
| K12 | `72a024a0a625b4781e303a7a9b941aeafddd02a7ba281ea36418d1e399e5fd78` | `9aaaec778dcad5acfa64f8655dc7cf22a083477eb1b1a0e0b38dee2556cd2e98` |

The exact hashes for all 18 time/stderr files and five campaign receipts remain in
`execution-provenance.json`; the audit recomputed and matched them without copying
those files into this report.

## Audit procedure and integrity result

The audit was read-only:

1. parse the compact preflight, provenance, finite-setting analysis, disposition,
   and execution receipts;
2. compare all 18 external input copies byte-for-byte with their retained repository
   inputs and verify the runner, ordered-input manifest, and pseudopotential copy;
3. recompute SHA-256 and byte count for all 41 externally retained output, stderr,
   and campaign-receipt files listed by `execution-provenance.json`;
4. independently extract final SCF energy, pressure, stress tensor, iteration count,
   final estimated accuracy, diagnostic bands, wall time, maximum resident-set size,
   completion markers, and warning text from the retained text outputs;
5. independently reconstruct the band-4-at-$\Gamma$ alignment, direct gaps, two
   indirect gap probes, and all eight adjacent finite-setting comparisons; and
6. compare regular-file counts and aggregate byte counts for the 18 SCF/diagnostic
   scratch trees without reading or duplicating native wavefunction, density, or
   restart content.

All 41 retained output identities, all three compact boundary identities, all 18
input copies, all nine independently parsed case records, all eight independently
derived comparison rows, and all 18 scratch-tree metadata summaries agree with the
retained records. The run root contains 1,496 regular files in 43 directories and
occupies 161,744 KiB. Native scratch manifest
content hashes were not recomputed because those dense/restart bytes are not needed
to audit the reported convergence observables; their retained manifest identities
remain provenance rather than newly asserted authority.

## Extracted calculated observations

Energies are Rydberg per atom, pressure and the maximum absolute Cartesian stress
component are kilobar, final estimated SCF accuracy is Rydberg, band quantities are
electron volt, wall times are seconds, and peak resident-set size is bytes. The
stress tensors are hydrostatic to the printed 0.01-kbar precision; their full signed
components remain in `execution-provenance.json`.

| Case | $E$ (Ry/atom) | $P$ / max $|\sigma|$ (kbar) | SCF iterations | Final accuracy (Ry) | Direct gaps $\Gamma$, X, $\Delta_{0.85}$ (eV) | $\Gamma\to$X / $\Gamma\to\Delta_{0.85}$ probes (eV) | SCF / NSCF wall (s) | Peak RSS (B) |
|---|---:|---:|---:|---:|---|---|---|---:|
| C30 | -8.461848470 | 37.33 / 37.33 | 8 | $1.8\times10^{-12}$ | 2.5639, 3.5777, 3.3516 | 0.6730 / 0.5369 | 3.44 / 0.36 | 42,516,480 |
| C36 | -8.461947470 | 37.64 / 37.64 | 8 | $1.4\times10^{-12}$ | 2.5634, 3.5765, 3.3504 | 0.6727 / 0.5367 | 2.95 / 0.34 | 48,889,856 |
| C42 | -8.461966005 | 37.83 / 37.83 | 7 | $5.7\times10^{-11}$ | 2.5634, 3.5763, 3.3502 | 0.6727 / 0.5367 | 3.06 / 0.34 | 57,737,216 |
| C48 / K8 | -8.461968840 | 37.82 / 37.82 | 8 | $3.6\times10^{-13}$ | 2.5634, 3.5763, 3.3502 | 0.6727 / 0.5367 | 3.58 / 0.36 | 65,437,696 |
| C54 | -8.461973275 | 37.81 / 37.81 | 8 | $5.1\times10^{-13}$ | 2.5634, 3.5763, 3.3502 | 0.6727 / 0.5367 | 4.40 / 0.43 | 67,649,536 |
| C60 | -8.461975385 | 37.83 / 37.83 | 8 | $1.3\times10^{-13}$ | 2.5633, 3.5763, 3.3502 | 0.6727 / 0.5367 | 4.70 / 0.44 | 81,936,384 |
| K6 | -8.461965860 | 37.81 / 37.81 | 8 | $4.3\times10^{-12}$ | 2.5633, 3.5763, 3.3502 | 0.6726 / 0.5366 | 2.16 / 0.37 | 61,014,016 |
| K10 | -8.461968955 | 37.82 / 37.82 | 7 | $6.3\times10^{-11}$ | 2.5634, 3.5763, 3.3502 | 0.6727 / 0.5367 | 6.96 / 0.39 | 60,358,656 |
| K12 | -8.461968955 | 37.82 / 37.82 | 6 | $6.6\times10^{-11}$ | 2.5633, 3.5763, 3.3502 | 0.6726 / 0.5366 | 10.67 / 0.44 | 66,273,280 |

The band values are printed by QE to 0.0001 eV. Changes smaller than that printed
resolution are not inferred.

## Frozen criteria and disposition

The frozen adjacent-setting criteria are $10^{-5}$ Ry/atom for energy, 0.05 kbar
for pressure and each stress component, and 1.0 meV for aligned band-4/5 and gap
probes at retained printed precision.

| Comparison | $|\Delta E|$ (Ry/atom) | $|\Delta P|$ / max $|\Delta\sigma|$ (kbar) | Max band / gap-probe change (meV) | Criteria disposition |
|---|---:|---:|---:|---|
| C30→C36 | $9.90\times10^{-5}$ | 0.31 / 0.31 | 1.0 / 1.2 | Fails energy, pressure, stress, and gap-probe criteria |
| C36→C42 | $1.8535\times10^{-5}$ | 0.19 / 0.19 | 0.2 / 0.2 | Fails energy, pressure, and stress criteria |
| C42→C48 | $2.835\times10^{-6}$ | 0.01 / 0.01 | 0.0 / 0.0 | Meets all predefined finite-setting criteria |
| C48→C54 | $4.435\times10^{-6}$ | 0.01 / 0.01 | 0.0 / 0.0 | Meets all predefined finite-setting criteria |
| C54→C60 | $2.110\times10^{-6}$ | 0.02 / 0.02 | 0.1 / 0.1 | Meets all predefined finite-setting criteria |
| K6→K8 (C48) | $2.980\times10^{-6}$ | 0.01 / 0.01 | 0.1 / 0.1 | Meets all predefined finite-setting criteria |
| K8 (C48)→K10 | $1.15\times10^{-7}$ | 0.00 / 0.00 | 0.0 / 0.0 | Meets all predefined finite-setting criteria |
| K10→K12 | 0.0 | 0.00 / 0.00 | 0.1 / 0.1 | Meets all predefined finite-setting criteria |

This is finite-setting numerical-verification evidence only. No $E_*$ or $K_*$ is
selected, and no comparison bounds an infinite-basis error. The diagnostic points do
not locate the conduction valley or verify effective-mass curvature.

## Missing evidence and protected-execution disposition

No retained primary case, compact receipt, text output, identity, or required
observable is missing or corrupt. **No rerun of any of the 18 completed invocations
is needed for this audit or merely to obtain a canonical Petri-net representation.**

Two boundaries remain unresolved:

1. Every invocation emitted the same IEEE invalid/divide-by-zero/overflow/underflow
   flag report. It remains unresolved and unclassified; zero exit and `JOB DONE.` do
   not establish harmlessness.
2. The current Task completion rule requires a bounded cutoff--mesh interaction
   cross-check after a human selects provisional $E_*$ and $K_*$. No settings are
   selected here, so the exact missing mixed case or cases cannot yet be named.
   Such a cross-check would be new, separately authorized protected execution, not a
   rerun of a missing or corrupt primary case.

The next decision is human disposition of provisional settings and the warning, not
scientific-harness re-execution. Scientific-harness/Petri-net execution remains later
reproducibility and direct-versus-controlled comparison work.
