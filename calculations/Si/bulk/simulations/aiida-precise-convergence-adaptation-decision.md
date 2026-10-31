# AiiDA-precise convergence adaptation decision

## Decision

For the prospective `C6-B20-W21` route, adopt the convergence-derived parameter tuple
from the **precise** protocol in pinned `aiida-wannier90-workflows` release 3.1.0,
commit `1c0115cb7c77541a0bd549bc05005df435d651b6`. This is a calculation-owned adaptation
of that convergence tuple, not adoption or execution of the complete AiiDA workflow.

For the exact two-atom primitive Si cell, the pinned workflow constructs the native
Wannier90 tolerances by multiplying each per-atom meta-parameter by the number of
sites. The resulting prospective localization controls are:

```text
conv_tol       = 2.0e-9 angstrom^2
conv_window    = 6
num_iter       = 40000

dis_conv_tol   = 2.0e-9  # dimensionless native Wannier90 parameter
dis_num_iter   = 40000

num_cg_steps   = 200
```

`num_cg_steps = 200` is inherited by the precise protocol from the pinned default
inputs. The AiiDA meta-parameter name `dis_conv_tol_per_atom` describes its workflow
scaling convention; the emitted Wannier90 `dis_conv_tol` remains dimensionless.

## Source authority

The pinned protocol YAML has SHA-256
`f6b2bd7e95a4b8be387c12a35d9eef83a7e28a4f3c0128dbec8f8990f37890c7` and declares:

- precise `conv_tol_per_atom = 1.0e-9`;
- precise `dis_conv_tol_per_atom = 1.0e-9`;
- precise `conv_window = 6`;
- precise `dis_num_iter = 40000`;
- precise `num_iter = 40000`; and
- common `num_cg_steps = 200`.

The pinned builder source has SHA-256
`59f7100fabe5a1a6443a115634a50bc5f060f13006eea6826593d4aad4c34f43` and implements

```text
conv_tol     = number_of_sites * conv_tol_per_atom
dis_conv_tol = number_of_sites * dis_conv_tol_per_atom
```

Sources:

- [pinned protocol YAML](https://github.com/aiidateam/aiida-wannier90-workflows/blob/1c0115cb7c77541a0bd549bc05005df435d651b6/src/aiida_wannier90_workflows/workflows/protocols/base/wannier90.yaml)
- [pinned builder implementation](https://github.com/aiidateam/aiida-wannier90-workflows/blob/1c0115cb7c77541a0bd549bc05005df435d651b6/src/aiida_wannier90_workflows/workflows/base/wannier90.py)

## Superseded prospective controls

For `C6-B20-W21`, this decision supersedes the previously prepared hybrid tuple:

```text
dis_conv_tol = 1.0e-10
dis_num_iter = 4000
num_iter = 4000
```

The already selected `conv_tol = 2.0e-9 angstrom^2`, `conv_window = 6`, and
`num_cg_steps = 200` are unchanged numerically, but their provenance is now the coherent
pinned precise convergence adaptation. Historical occurrences retain their exact inputs
and dispositions; none is reclassified.

The earlier ungranted `C6-B20-W21` preprocessing request with SHA-256
`f94dd22f911a83aa2779996bfccef211e32ebfbcba2c689fccab476e3c9ad033` is superseded and
must not be authorized or replayed. A newly rendered input and a new authorization
request are required.

## Adaptation boundary

The following precise-protocol coordinates are **not** adopted by this decision:

- `num_bands_factor = 3.0` and a 30-band parent;
- `kpoints_distance = 0.1` and any automatic mesh replacement;
- the default `SSSP/1.3/PBEsol/efficiency` family;
- AiiDA-derived projections, semicore exclusion, energy-window automation, MPI layout,
  wall-clock limit, restart handlers, or work-directory policy.

The accepted PBE pseudopotential, exact relaxed structure, 42/336 Ry cutoffs, accepted
SCF parent, ordered C6 mesh, 20-band NSCF, rank 10, `[-6.0, 21.0] eV` outer window,
`[-5.85, 8.00] eV` frozen window, and declared projection family remain fixed.

## Stop and authorization boundary

The 40000-step values are fixed eligibility ceilings, not evidence that either local
optimization will converge or find a global minimum. If a fresh occurrence exhausts
either ceiling or lacks either native convergence message, no automatic extension,
retry, optimizer change, `C6-B30`, or mesh escalation follows.

This decision authorizes deterministic no-calculator preparation only. It does not
authorize `wannier90.x -pp`, `pw2wannier90.x`, localization, a retry, or any downstream
calculator occurrence.
