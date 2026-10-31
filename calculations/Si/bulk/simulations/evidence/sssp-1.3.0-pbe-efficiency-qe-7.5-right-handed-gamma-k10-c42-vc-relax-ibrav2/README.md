# Right-handed Gamma-K10 C42 FCC-native bulk relaxation

This directory retains compact evidence from one authorized Quantum ESPRESSO 7.5
`vc-relax` occurrence on the provisional right-handed bulk-silicon seed.

## Outcome

- calculator invocations: `1`;
- retries: `0`;
- execution return code: `0`;
- QE terminal marker: present;
- electronic convergence: reported;
- BFGS convergence: reported after three BFGS steps and four structural SCF cycles;
- optimizer-terminal pressure: `0.01 kbar`;
- final-SCF pressure: `0.09 kbar`;
- declared pressure tolerance: `0.5 kbar`;
- optimizer-terminal maximum force: `0.0 Ry/bohr`;
- final conventional cubic lattice parameter: `5.469182093640207 angstrom`.

The native input used `ibrav=2`, `A=5.43`, and `cell_dofree='ibrav'`.
For cubic FCC this varies the scalar lattice parameter without opening shape or
shear modes. The input contains no `CELL_PARAMETERS` card. Its SHA-256 is
`512d3a35f663db7cf74ef58119942ed0eb8c598fb8fc907b698ed82383c29329`.

## QEXSD and provisional structure

The retained QEXSD bytes were parsed by the existing
`ksdft2effmass.integration.quantum_espresso.qexsd.QuantumEspressoXsdDocumentParser`.
ProjectKoios then extracted the final native unit cell and restored the maintained
right-handed source basis through
`QeFccPrimitiveBravaisMapping.restore_source_basis`. The resulting provisional
structure is:

- structure ID: `Si.PrimitiveUnitCell.RightHanded.RelaxedS1`;
- byte size: `758`;
- SHA-256: `d131107753512c53dc0a32b9e07e0081f8277d8eeafcb9fad5f1fc7f153ded03`;
- repository copy:
  [`../../structures/Si.PrimitiveUnitCell.RightHanded.RelaxedS1.json`](../../structures/Si.PrimitiveUnitCell.RightHanded.RelaxedS1.json).

`S1` is provisional. It requires fresh k-point and cutoff confirmation and is not
an accepted production parent.

## Diagnostics and provenance

QE retained `IEEE_INVALID_FLAG`, `IEEE_DIVIDE_BY_ZERO`, `IEEE_OVERFLOW_FLAG`, and
`IEEE_UNDERFLOW_FLAG` in stderr. They are retained as native QE diagnostics, not
an automatic blocker: this occurrence completed, converged, and produced finite
observations. They do not establish scientific acceptance.

The calculator completed successfully before the driver encountered a
post-execution field-name error (`return_code` versus retained `returncode`). The
campaign manifest was repaired from `execution.json` without another calculator
invocation. `retain_result.py` uses the maintained QEXSD parser; an earlier ad hoc
postprocessing attempt failed before producing a result and did not invoke QE.

Large saved-state artifacts remain under the authenticated external root:

`/Users/eugene/projects/ksdft2effmass/si-bulk-vc-relax-ibrav2-gamma-k10-c42-20261031T061128Z`

`external-artifact-inventory.json` records all external files. The repository
retains the exact input, streams, execution and artifact manifests, QEXSD,
provisional structure, interpreted result, and postprocessing provenance.
