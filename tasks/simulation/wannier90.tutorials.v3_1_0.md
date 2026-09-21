# Wannier90 3.1.0 bundled tutorial campaign

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `wannier90.tutorials.v3_1_0`
- **Status:** `inactive`
- **Status detail:** Inventory-only campaign for 33 source-directory Tasks covering the 32 numbered Wannier90 3.1.0 examples; example16 has supplied-matrix and Quantum ESPRESSO variants. Example05 and example11 are blocked candidate tutorials, the other 31 Tasks are deliberately deferred, and no execution or workspace creation is authorized. Private Project Koios notes are AUTOMATED_UNREVIEWED procedure aids rather than authority; the Tutorial 11 note has a known compressed-procedure omission.
- **Parent Task:** `wannier90.tutorials`
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Coordinate source-pinned preflight, execution-or-deferral, and evidence disposition for each bundled Wannier90 3.1.0 tutorial directory while keeping tutorial learning separate from project production calculations.

## Relationships

### Task prerequisites

- `P2`

### External prerequisites

- None.

### Superseded by

- None.

## Authorized scope

- Maintain one Task per bundled example source directory, including separate example16 supplied-matrix and Quantum ESPRESSO routes.
- Use private Project Koios documentation-derived notes only as AUTOMATED_UNREVIEWED learning and procedure aids; read them in place, do not copy their content into Git, and treat the retained Wannier90 3.1.0 inputs plus `doc/compiled_docs/tutorial.pdf` and `doc/compiled_docs/solution_booklet.pdf` as authoritative.
- Prioritize only example05 followed by example11 under separate exact operator decisions; leave every other child deferred unless explicitly selected later.
- Preflight an explicitly selected child for exact source, executable, interface, input, pseudopotential and terms, resources, warning handling, retention, and protected-execution authority before creating a workspace.
- After an authorized run, keep native outputs, manifests, diagnostics, and semantic extraction under ksdft2effmass ownership; extract each supported retained QEXSD document into a canonical plane-wave calculation record and inventory supported Wannier90 artifacts without inferring missing semantics.
- Make any later Koios return path a canonical content-addressed record handoff for retrieval and review only, after a separately accepted handoff and private-locator policy; do not expose native workspaces or private absolute paths.
- Retain compact provenance outside the upstream source tree and classify any observations as tutorial learning evidence.
- Review campaign evidence only after every child has an explicit execution, failure, unsupported, or deliberate-deferral disposition.

## Completion criteria

- All 33 source-directory Tasks have explicit evidence-backed execution or deliberate-deferral dispositions.
- Every attempted stage retains exact source, executable, interface, input, pseudopotential, command, attempt, stream, runtime, exit, warning, and artifact provenance.
- Every executed Quantum ESPRESSO child records a supported-QEXSD extraction or an explicit unsupported/missing disposition, and every executed Wannier90 child records an inventory and parser-eligibility disposition for `.eig`, `.amn`, `.mmn`, `.nnkp`, `.wout`, `_u.mat`, and `_hr.dat` artifacts that are actually emitted.
- The campaign review separates reusable operational findings from unsupported production, convergence, verification, validation, and acceptance claims.
- No child is activated automatically and no upstream source directory is used as a mutable run workspace.

## Exclusions

- This campaign does not itself authorize Quantum ESPRESSO, pw2wannier90, Wannier90, MPI, network, remote, cluster, cloud, or other protected execution.
- Project Koios notes do not authorize execution, replace source PDFs or inputs, establish scientific meaning, or provide acceptance; their private content and storage paths are not copied into this repository.
- It does not infer pseudopotential or data-file terms from the GPLv2 statement for the Wannier90 code.
- It does not adopt bundled settings, pseudopotentials, projections, windows, gauges, material systems, dependencies, or outputs as project defaults.
- It does not satisfy or activate the production bulk-silicon Wannier-reference milestone.

## Authority references

- `docs/computational/wannier90.tutorials.v3_1_0.md`
