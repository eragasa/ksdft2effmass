# Provisional S1 Gamma-centered k-point confirmation preflight

This directory retains compact **preflight only** material for the first stage of
fresh setting confirmation on
`Si.PrimitiveUnitCell.RightHanded.RelaxedS1`:

- byte size: `758`;
- SHA-256: `d131107753512c53dc0a32b9e07e0081f8277d8eeafcb9fad5f1fc7f153ded03`;
- fixed wavefunction/density cutoffs: `42/336 Ry`;
- Gamma-centered meshes: K6, K8, K10, and K12; and
- calculation-owned selection rule: select the smallest sampled mesh whose absolute
  total-energy difference from K12 is at most `1.0 meV/atom`.

[`campaign-preflight.json`](campaign-preflight.json) binds the exact structure,
relaxation lineage, executable, pseudopotential, settings, input identities, order,
and resource limits. The `K*/pw.in` files are exact rendered inputs. The preparation
used ProjectKoios revision
`e146f3722e87ca2de2243421a94448cfa6e27037` and performed no calculator execution.

## Authorization and execution state

The requested bound was exactly four sequential `pw.x` invocations in order K6, K8,
K10, K12, with one process per occurrence, `600 s` timeout per occurrence, at most
`2 GiB` retained per occurrence, zero retries, and stop on the first failure. The
operator subsequently authorized that exact packet. All four invocations succeeded;
no retry occurred. Compact retained evidence is under
[`../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-right-handed-s1-gamma-c42-kpoint-confirmation/`](../../evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-right-handed-s1-gamma-c42-kpoint-confirmation/).

The sampled calculation-owned rule again selects K10. The next step is a separately
preflighted and separately authorized cutoff-confirmation axis at K10. This occurrence
does not automatically accept a stable production pair.
