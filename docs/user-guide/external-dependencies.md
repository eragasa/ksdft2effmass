# External dependency catalog

## Status vocabulary

Each record distinguishes:

```text
documented upstream version
installable version
locally smoke-tested version
scientifically validated version
```

An empty or unknown field is not evidence of support. The architecture pass did not install prospective dependencies; the later bounded P0 preflight installed and probed SNAKES and MyST in a disposable environment. P0A now declares them only in the accepted optional extras and verifies them through isolated locked environments.

## Python libraries

### NumPy

- **Category:** runtime Python library
- **Purpose:** immutable numerical array payloads and linear algebra inputs
- **Required or optional:** required by the implemented Python package
- **Installation source:** Python package index through the repository lock workflow
- **Supported-version policy:** `numpy>=1.26` currently declared
- **Version actually tested:** current lock records 2.5.1; existing repository tests cover implemented operator code, not prospective CPN workflows
- **License:** upstream license; verify from installed/package metadata for release records
- **Import/executable names:** `numpy`
- **Capability probes:** import, scalar/array behavior, BLAS-backed operations where relevant
- **Configuration inputs:** Python environment and platform
- **Artifacts consumed:** project-owned scalar and array payloads
- **Artifacts produced:** project-owned scalar and array payloads; no external executable artifacts
- **Associated CPN places/transitions:** project token payload validation; not an engine transition
- **Failure modes:** import failure, unsupported dtype/platform behavior, numerical warnings
- **Software-verification status:** existing operator software-verification evidence; prospective CPN use not performed
- **Numerical-verification status:** selected existing operator numerical-verification evidence; prospective CPN use not performed
- **Scientific-validation status:** not performed

### SciPy

- **Category:** runtime Python library
- **Purpose:** declared dependency for future scientific numerical algorithms; no SciPy-backed maintained behavior was identified in the current package
- **Required or optional:** required by the implemented Python package
- **Installation source:** Python package index through the repository lock workflow
- **Supported-version policy:** `scipy>=1.12` currently declared
- **Version actually tested:** current lock records 1.18.0; no prospective CPN role tested
- **License:** upstream license; verify from package metadata for release records
- **Import/executable names:** `scipy`
- **Capability probes:** import and specifically required numerical routines
- **Configuration inputs:** Python environment and numerical backend
- **Artifacts consumed:** project-owned numerical arrays and configurations
- **Artifacts produced:** project-owned numerical results
- **Associated CPN places/transitions:** analyzer payloads only where an accepted task requires them
- **Failure modes:** import, linear-algebra, convergence, warning, or platform failures
- **Software-verification status:** no SciPy-specific maintained behavior or verification evidence identified
- **Numerical-verification status:** no SciPy-specific numerical-verification evidence identified
- **Scientific-validation status:** not performed

### jsonschema

- **Category:** development/test Python library
- **Purpose:** independent public-schema validation
- **Required or optional:** optional development/test dependency; not runtime
- **Installation source:** Python package index through the dev extra
- **Supported-version policy:** `jsonschema>=4.23`
- **Version actually tested:** current lock records 4.26.0 for existing schema tests
- **License:** upstream metadata to retain in environment provenance
- **Import/executable names:** `jsonschema`
- **Capability probes:** import and validation against approved schemas
- **Configuration inputs:** schema and fixture paths
- **Artifacts consumed:** approved schemas and fixtures
- **Artifacts produced:** validation reports/results
- **Associated CPN places/transitions:** future manifest/token schema-verification transition
- **Failure modes:** invalid schema/instance or import failure
- **Software-verification status:** existing operator-schema software verification only
- **Numerical-verification status:** not applicable/not performed
- **Scientific-validation status:** not performed

### SNAKES

- **Category:** selected optional Python CPN engine dependency; the implemented P1 neutral contract does not import it
- **Purpose:** candidate engine for a future isolated adapter; P1 implements only the backend-neutral project contract, not that adapter, persistence, or a concrete workflow
- **Required or optional:** optional `workflow` extra; absent from core and development-only dependencies
- **Installation source:** PyPI sdist `SNAKES-0.9.33.tar.gz`, SHA-256 `af8c3046bfedf3e088b6bf37d451ad6aeeb79716f68a6253e44ddbd1c7e250f3`
- **Supported-version policy:** `SNAKES>=0.9.33,<0.10` is declared only in the optional `workflow` extra; the lock retains the exact artifact and Python 3.14 probes retain runtime evidence
- **Version actually tested:** 0.9.33 on CPython 3.14.6, macOS 26.5.1 arm64; sdist installation, import, and required synthetic behavior passed
- **Python metadata:** no `Requires-Python` and no version-specific classifier; successful Python 3.14 execution is local evidence, not a metadata declaration
- **Dependency footprint:** no declared direct or optional Python dependencies; distribution includes scripts and resources and is built locally from sdist
- **License:** for project governance the human PI records the explicit upstream grant as `LGPL-2.1-or-later`; the observed distributed license file contains LGPLv3 text. This is a project packaging decision, not a general legal conclusion. SNAKES must not be presented as Apache-2.0 project code; vendoring, modification/fork redistribution, or bundled executable/application/container distribution requires a new human checkpoint
- **Project/documentation:** <https://codeberg.org/fpom/snakes> and <https://snakes.ibisc.univ-evry.fr/>; 0.9.33/current-tree snapshot is dated 2024-06-03
- **Import/API names tested:** `snakes`, `snakes.nets`, `snakes.data.Substitution`, and `snakes.plugins`
- **Capability result:** basic net construction, immutable structured tokens, multiset multiplicity, pure guards, bindings, arc expressions, firing, failure/retry history, provenance joins, neutral extraction, and bounded core `StateGraph` exploration are feasible
- **Limitations:** tokens used in multisets must be hashable; expressions can execute arbitrary Python and may be evaluated repeatedly; ordering, persistence, type registries, canonicalization, lineage, and structured failures remain project-owned
- **Configuration inputs:** future project CPN model and engine-adapter configuration
- **Artifacts consumed:** project-owned net definitions and immutable token payloads through the adapter
- **Artifacts produced:** runtime firing results returned through project adapters; never pickled live engine state
- **Associated CPN places/transitions:** engine may realize project transitions only after P1 human acceptance and separately authorized adapter/persistence work
- **Failure modes:** source-build failure, unsupported Python/API, evaluator side effects, unhashable payloads, invalid binding, unbounded exploration, or license/distribution rejection
- **Software-verification status:** P0 capability preflight `CONDITIONAL_PASS`; not production software verification
- **Numerical-verification status:** not applicable/not performed
- **Scientific-validation status:** not performed

### Graphviz integration

- **Category:** optional visualization plugin and system executable
- **Purpose:** derived, nonauthoritative CPN diagrams
- **Required or optional:** optional; absence does not block the CPN runtime
- **Python integration:** SNAKES 0.9.33 plugin `gv`; it uses direct subprocess calls and does not require a Python `graphviz` distribution
- **Plugin result:** import, documented `snakes.plugins.load("gv", "snakes.nets")`, automatic `clusters`/`pos` composition, and DOT construction passed
- **System executable result:** `dot` was not available in the tested environment; version reporting and SVG rendering were not tested
- **Python 3.14 limitation:** plugin rendering calls deprecated `codecs.open`, producing a `DeprecationWarning` and failing when warnings are errors
- **Supported-version policy:** none until an environment with `dot` and a bounded warning correction is separately tested
- **License:** system Graphviz license/distribution facts remain deployment-specific and were not resolved because no executable was installed
- **Configuration inputs:** nonauthoritative net view and output format
- **Artifacts consumed:** derived nonauthoritative net views
- **Artifacts produced:** prospective derived DOT/SVG/PNG; no generated diagram was retained by P0
- **Associated CPN places/transitions:** optional external rendering request/result boundary only
- **Failure modes:** missing `dot`, Python 3.14 deprecation promoted to error, subprocess/rendering failure, plugin-composition conflict, or stale diagram
- **Software-verification status:** plugin `CONDITIONAL_PASS`; system Graphviz `NOT_AVAILABLE`
- **Numerical-verification status:** not applicable/not performed
- **Scientific-validation status:** not performed

### cpnpy

- **Category:** comparative Python CPN reference
- **Purpose:** conceptual API comparison only
- **Required or optional:** not a dependency
- **Installation source:** not selected
- **Supported-version policy:** none
- **Version actually tested:** not tested
- **License:** unverified; accepted P0 did not adopt the package
- **Import/executable names:** supplied example uses `cpnpy`; API unverified
- **Capability probes:** P0 retained comparison context without installing or testing the package; any future probe requires separate authorization
- **Configuration inputs:** none approved
- **Artifacts consumed:** none approved
- **Artifacts produced:** none approved
- **Associated CPN places/transitions:** none authoritative
- **Failure modes:** supplied example/API drift, license or packaging mismatch
- **Software-verification status:** not performed
- **Numerical-verification status:** not performed
- **Scientific-validation status:** not performed

### SimPN

- **Category:** comparative Python simulation/Petri-net reference
- **Purpose:** comparative documentation only
- **Required or optional:** not a dependency
- **Installation source:** not selected
- **Supported-version policy:** none
- **Version actually tested:** not tested
- **License:** unverified; accepted P0 did not adopt the package
- **Import/executable names:** unverified
- **Capability probes:** P0 retained comparison context without installing or testing the package; any future probe requires separate authorization
- **Configuration inputs:** none approved
- **Artifacts consumed:** none approved
- **Artifacts produced:** none approved
- **Associated CPN places/transitions:** none authoritative
- **Failure modes:** capability, API, packaging, or license mismatch
- **Software-verification status:** not performed
- **Numerical-verification status:** not performed
- **Scientific-validation status:** not performed

### MyST Markdown parser

- **Category:** optional maintained documentation dependency
- **Purpose:** render Markdown-first narrative documentation in Sphinx
- **Required or optional:** declared in the optional `docs` extra; not a runtime dependency
- **Installation source:** PyPI universal wheel `myst_parser-5.1.0-py3-none-any.whl`, SHA-256 `9c91c52b3cdb4d94a6506e4fab4e2f296c7623a0da0dcbe6de1565c3dad67a8a`
- **Supported-version policy:** the docs extra declares `myst-parser>=5.1,<6` and Sphinx `>=8,<10`; the lockfile retains exact selected artifacts and hashes
- **Version actually tested:** MyST 5.1.0 with Sphinx 9.1.0 on CPython 3.14.6, macOS arm64
- **Python metadata:** requires Python `>=3.11` and explicitly classifies Python 3.14
- **Direct dependencies:** Docutils, Jinja2, markdown-it-py, mdit-py-plugins, PyYAML, and Sphinx
- **License:** MIT license in the installed distribution
- **Project/documentation:** <https://github.com/executablebooks/MyST-Parser> and <https://myst-parser.readthedocs.io/>
- **Import/executable names:** `myst_parser`; Sphinx invoked from the repository root through `python/.venv/bin/python -m sphinx`
- **Capability result:** disposable mixed RST/Markdown navigation, fenced Python, dollar mathematics, relative links, Markdown toctree, cross-reference, Unicode, table, nested fence, and raw HTML built with warnings as errors
- **Required configuration:** `extensions += ["myst_parser"]`, `myst_enable_extensions = ["dollarmath"]`, and bounded heading-anchor/navigation policy
- **Maintained-source policy:** every RST source remains collected; Markdown collection is restricted to `docs/user-guide/*.md`, whose 14 pages are listed in one explicit toctree. Other Markdown trees remain repository/Obsidian sources. The three directory links were replaced with concrete source links, and obsolete duplicate user-guide download navigation was removed
- **Artifacts consumed:** Markdown sources and Sphinx configuration after approval
- **Artifacts produced:** derived Sphinx HTML; disposable P0 HTML was removed
- **Associated CPN places/transitions:** none; documentation tooling only
- **Failure modes:** parser/config incompatibility, broken MyST targets, duplicate navigation, Mermaid lexer warning, or divergent authoring/rendering expectations
- **Software-verification status:** representative P0 build `PASS`; maintained mixed RST/MyST user-guide builds with locked Sphinx 9.1.0 and lower-range Sphinx 8.2.3 `PASS`; P0A is human-accepted and closed; `P1-HC01` Option A and `P1-HC02` Option B are resolved; the earlier independent final review reported only deterministic stale prose/evidence findings for the consolidated correction cycle; after correction, reviews and parent verification completed; final P1 acceptance was granted as Option A through `P1-HC03` on 2026-08-04; P1 is closed as human-accepted `PASS`; P2 is active and provisional pending correction review, replacement replay, parent verification, and human acceptance; H5 and P3–P11 remain inactive, and production/scientific execution remains unauthorized
- **Numerical-verification status:** not applicable
- **Scientific-validation status:** not applicable

## Declared development, documentation, and notebook toolchain

The following packages are declared in `python/pyproject.toml`. Their presence in the lockfile or use for software checks does not establish scientific validation.

| Package | Declared purpose | Declared minimum | Current lock record | Status in this architecture correction |
|---|---|---:|---:|---|
| setuptools | PEP 517 build backend | 77 | build-environment resolved | declared build requirement; not changed or invoked by this correction |
| wheel | wheel build support | unspecified | build-environment resolved | declared build requirement; not changed or invoked by this correction |
| mypy | static type checking | 1.10 | 2.3.0 | declared development tool; no new check or dependency change |
| pytest | test execution | 8.0 | 9.1.1 | declared development tool; no tests added or changed |
| pytest-cov | coverage reporting | 5.0 | 7.1.0 | declared development tool; not run for documentation-only correction |
| Ruff | formatting/lint policy | 0.5 | 0.16.1 | declared development tool; no Python source changed |
| Sphinx | documentation build | 8.0,<10 | 9.1.0 | maintained mixed RST/MyST user-guide build passes warnings-as-errors; non-user-guide Markdown is explicitly uncollected |
| ipykernel | notebook kernel | 6.29 | 7.3.0 | declared notebook tool; not used |
| JupyterLab | notebook environment | 4.2 | 4.6.2 | declared notebook tool; not used |
| Matplotlib | notebook visualization | 3.8 | 3.11.1 | declared notebook tool; not used |

Exact release/tooling provenance must use the selected environment and lockfile at the time of execution. The P0A lock resolves MyST 5.1.0 and Sphinx 9.1.0 for the optional docs environment.

## External tools

### Quantum ESPRESSO

- **Category:** periodic electronic-structure executable suite and initial production backend
- **Purpose:** periodic KS/GKS-capable SCF/NSCF and selected postprocessing; the immediate project lane is semilocal KS
- **Required or optional:** capability-specific; suite membership does not make every executable required
- **Installation source:** unresolved production environment
- **Supported-version policy:** exact version/build must be recorded and interface-compatible
- **Version actually tested:** none accepted for this architecture
- **License:** verify for the selected installation and redistribution context
- **Import/executable names:** `pw.x`; capability-specific optional `bands.x`, `projwfc.x`, and `pw2wannier90.x`
- **Executable capabilities:** `pw.x` SCF, `pw.x` NSCF, optional `bands.x`, optional `projwfc.x`, and `pw2wannier90.x`
- **Capability probes:** executable identity/hash, version, minimal authorized interface smoke test, output compatibility
- **Configuration inputs:** neutral specification mapped to QE input plus execution configuration
- **Artifacts consumed:** inputs, pseudopotentials, parent density/restart, `.nnkp` for bridge use
- **Artifacts produced:** output/logs, density, wavefunctions, `.save`, spectra, and bridge files through `pw2wannier90.x`
- **Associated CPN places/transitions:** QE capability verification, input-ready, requested/result/failure places, parse/adapt/SCF-validation transitions
- **Failure modes:** unavailable executable, nonzero exit, interruption, nonconvergence, malformed/incomplete/mismatched output, checksum failure
- **Software-verification status:** prospective adapter software verification not performed
- **Numerical-verification status:** no accepted convergence or numerical-verification evidence
- **Scientific-validation status:** not performed

### ABINIT

- **Category:** planned secondary periodic electronic-structure conformance backend
- **Purpose:** future software verification of neutral periodic input/output abstractions and bounded QE–ABINIT numerical verification
- **Required or optional:** deferred; not required for production QE campaigns
- **Installation source:** none selected; no installation authorized
- **Supported-version policy:** none until a separately approved post-dopant conformance task
- **Version actually tested:** not installed or tested
- **License:** must be verified before any dependency, executable use, or fixture redistribution
- **Import/executable names:** prospective backend-specific names; not probed or approved
- **Capability probes:** future narrow semilocal SCF mapping, deterministic serialization, parsing, neutral dataset adaptation, capability reporting, and selected paired comparisons
- **Configuration inputs:** future neutral `PeriodicElectronicStructureSpecification` mapped independently by a concrete ABINIT adapter; no QE variable names or QE-to-ABINIT translation
- **Artifacts consumed:** no current artifacts; future authorized input and pseudopotential references
- **Artifacts produced:** no current artifacts; future parsed records, immutable execution evidence, and neutral periodic datasets
- **Associated CPN places/transitions:** deferred paired-backend qualification subnet only; absent from the prospective QE production path and P0–P11
- **Failure modes:** unsupported capability, mapper/parser mismatch, pseudopotential confounding, nonconvergence, or backend disagreement
- **Implementation status:** planned and deferred until an accepted end-to-end dopant result
- **Software-verification status:** not performed
- **Numerical-verification status:** not performed
- **Scientific-validation status:** not performed

ABINIT is not an oracle, a mandatory duplicate of every QE calculation, or a replacement for experimental or all-electron validation. Tutorial-derived future cases are behavioral references and must retain source, version, URL, retrieval date, license, checksum, modifications, convergence status, and allowed VVUQ classification.

### Wannier90

- **Category:** localization/interpolation executable suite
- **Purpose:** preprocessing, disentanglement, localization, interpolation, and selected postprocessing
- **Required or optional:** capability-specific
- **Installation source:** unresolved production environment
- **Supported-version policy:** exact interface-compatible version required
- **Version actually tested:** none accepted for this architecture
- **License:** verify for selected installation
- **Import/executable names:** `wannier90.x`; optional `postw90.x`
- **Executable capabilities:** `wannier90.x -pp`, `wannier90.x` localization/interpolation, optional `postw90.x`
- **Capability probes:** executable identity/version, QE bridge compatibility, minimal authorized interface smoke test
- **Configuration inputs:** Wannier specification/input set and bridge artifacts
- **Artifacts consumed:** `.win`, `.nnkp`, `.amn`, `.mmn`, `.eig`, optional approved bridge files
- **Artifacts produced:** logs, checkpoints, centers/spreads, interpolation outputs, translation-indexed Hamiltonian data
- **Associated CPN places/transitions:** Wannier capability, request/result/failure, adaptation, validation, and Wannier-TB places/transitions
- **Failure modes:** interface mismatch, missing artifacts, disentanglement/localization failure, unacceptable validation
- **Software-verification status:** not performed
- **Numerical-verification status:** not performed
- **Scientific-validation status:** not performed

### MPI implementation

- **Category:** optional external execution capability
- **Purpose:** parallel launch when required by an authorized calculation
- **Required or optional:** environment/campaign specific
- **Installation source:** unresolved until production checkpoint
- **Supported-version policy:** exact implementation and version must be recorded by the production checkpoint
- **Version actually tested:** not tested
- **License:** unresolved for the selected implementation
- **Import/executable names:** implementation-specific launcher; not selected
- **Capability probes:** launcher identity/version and controlled smoke test
- **Configuration inputs:** immutable launch request and resource allocation
- **Artifacts consumed:** immutable launch request and authorized resource allocation
- **Artifacts produced:** launch records, stdout/stderr, and exit evidence
- **Associated CPN places/transitions:** MPI capability and external request/result/failure boundary
- **Failure modes:** launcher unavailable, allocation mismatch, rank failure, partial termination
- **Software-verification status:** not performed
- **Numerical-verification status:** not performed
- **Scientific-validation status:** not performed

### Scheduler

- **Category:** optional deployment service/tool
- **Purpose:** submit and monitor authorized external jobs
- **Required or optional:** cluster-specific
- **Installation source:** unresolved until a scheduler is selected
- **Supported-version policy:** none until selection and capability preflight
- **Version actually tested:** not tested
- **License:** unresolved for the selected scheduler/client
- **Import/executable names:** scheduler-specific; not selected
- **Capability probes:** authenticated capability through an approved adapter without storing credentials in tokens
- **Configuration inputs:** immutable submission request and authorized resource policy
- **Artifacts consumed:** immutable submission request and authorized resource policy
- **Artifacts produced:** submission/result/failure records and scheduler IDs
- **Associated CPN places/transitions:** scheduler capability and two-phase request/result boundary
- **Failure modes:** rejection, timeout, cancellation, preemption, unreachable service
- **Software-verification status:** not performed
- **Numerical-verification status:** not applicable/not performed
- **Scientific-validation status:** not performed

### Container runtime

- **Category:** optional deployment tool
- **Purpose:** reproduce an approved execution environment when selected
- **Required or optional:** optional and unresolved
- **Installation source:** unresolved until a runtime is selected
- **Supported-version policy:** none until selection and capability preflight
- **Version actually tested:** not tested
- **License:** unresolved for the selected runtime
- **Import/executable names:** runtime-specific; not selected
- **Capability probes:** runtime identity, image digest, controlled execution
- **Configuration inputs:** immutable image/execution request
- **Artifacts consumed:** approved image digest, execution request, and artifact mounts
- **Artifacts produced:** execution evidence and produced artifact references
- **Associated CPN places/transitions:** environment capability and external request/result boundary
- **Failure modes:** missing runtime/image, digest mismatch, mount/permission/network policy failure
- **Software-verification status:** not performed
- **Numerical-verification status:** not applicable/not performed
- **Scientific-validation status:** not performed
