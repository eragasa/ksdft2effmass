# QE example01 silicon Davidson bands result

**Status:** Calculated tutorial result awaiting human review. This is not a
production reference, numerical verification, or scientific validation.

Exactly one authorized local single-process invocation ran in the isolated
external workspace. It started at `2026-08-12T22:45:01.138515Z`, ended at
`2026-08-12T22:45:01.595653Z`, and exited with status 0. Shell wall time was
0.457126 s. QE reported 0.17 s CPU and 0.21 s wall time.

The stdout contains both `End of band structure calculation` and `JOB DONE.`.
It contains 28 ordered k-point blocks with eight printed eigenvalues each. QE
reported `ethr = 1.25E-08` and an average 17.4 diagonalization iterations.

External stream identities:

- stdout: 12,252 bytes, SHA-256
  `69c016287b8ae4875491f4a522cb72d05a4f0466bc6dada5b7bb6b94c749d99f`;
- stderr: 139 bytes, SHA-256
  `f382ec8367e667a70bf57907b4d4298dc573e3a6569c53218739fdb92f87b99e`.

Stderr contains the exact warning:

```text
Note: The following floating-point exceptions are signalling: IEEE_INVALID_FLAG IEEE_DIVIDE_BY_ZERO IEEE_OVERFLOW_FLAG IEEE_UNDERFLOW_FLAG
```

This record does not classify the warning as harmless or fatal. It recurs from
the accepted SCF observation and remains unresolved.

The complete external inventory contains 41 regular files totaling 3,011,573
bytes, seven directories, and no symbolic links. Relative to the pre-execution
workspace, 34 files were created, one file changed, and six files were
unchanged. QE changed the run-local `silicon.save/data-file-schema.xml`, created
28 path wavefunction files, and created the run-local `silicon.xml` and
`silicon.wfc1`. The copied charge density and pseudopotential remained
byte-identical. Native outputs remain external and uncommitted.

The accepted source `/Users/eugene/projects/q-e-qe-7.2/tempdir/silicon.save`
was re-enumerated after execution. Its complete path, type, size, and SHA-256
manifest agrees exactly with the retained pre-execution manifest; accepted-source
nonmutation passed.

The bundled legacy output has the same 28 ordered coordinates and 224 printed
eigenvalues. At printed precision, 166 values are exactly equal and the largest
observed absolute printed difference is approximately 0.0001 eV. This is an
observational description only: no comparison tolerance is accepted, and no
pass/fail numerical conclusion follows.

The calculation remains the fixed-operator QE tutorial evaluation

$$
\hat H_{\mathrm{KS}}[n_{\mathrm{SCF}}]\psi_{n\mathbf k}
=
\epsilon_{n\mathbf k}\psi_{n\mathbf k},
\qquad \mathbf k\in\mathcal K_{\mathrm{tutorial}}.
$$

The 28 `tpiba` points and delta, sigma, and lambda descriptions are the legacy
QE tutorial path, not an accepted modern silicon high-symmetry path. Eight bands
remain a tutorial choice. This result is not an effective-mass, Wannier, or
tight-binding dataset. The Task remains active awaiting human review, automatic
successor activation remains disabled, and no successor was activated.
