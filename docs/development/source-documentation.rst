Source documentation standard
=============================

Maintained first-party Python source must be understandable and auditable by a
researcher without reconstructing scientific or numerical intent from
implementation details.  This standard applies to maintained modules under
``python/src/ksdft2effmass/`` and to corresponding tests, Sphinx pages, public
schemas, fixtures, and control-plane records.  It excludes generated files,
build outputs, virtual environments, caches, Graphify-generated outputs,
third-party or copied upstream code, global agent configuration, and vendored
dependencies.

Module documentation
--------------------

Every maintained first-party Python module must have a module docstring that
documents, as applicable, its scientific or software purpose, represented
mathematical objects, physical and numerical scope, important equations, units
and conventions, assumptions and invariants, exclusions and non-goals,
relationship to neighboring modules, software-verification boundary, and
scientific-validation boundary.

Public objects
--------------

Every public DataObject, ResultObject, ActionObject, enum, exception, property,
and method must have complete NumPy-style documentation.  Use ``Parameters``,
``Attributes``, ``Returns``, ``Raises``, ``Notes``, ``Examples``, and ``See
Also`` only when the section is needed to explain the public contract.
Dataclass fields must be documented individually, including scientific meaning,
mathematical symbol when applicable, expected type, units, allowed values,
invariants, canonicalization, and relationship to other fields.

Public ActionObjects use
``<DataObject-or-operation-target><Actionizer>`` grammar.  The final word is a
precise agent noun such as ``Validator``, ``Resolver``, ``Evaluator``,
``Serializer``, ``Auditor``, ``Inspector``, ``Preparer``, ``Recorder``, or
``Comparator``.  Do not use verb-first forms or vague ``Manager``, ``Handler``,
or ``Processor`` suffixes.

Private implementation details
------------------------------

Private scientific or numerical policy and non-obvious implementation owners
must document their responsibility, assumptions, invariants, units, failure
behavior, and relationship to the public contract as applicable. Scientific
meaning, physical conventions, numerical policy, comparison policy,
compatibility policy, and public validation rules must not exist solely in
private methods. Cross-object private-method calls are prohibited.

Private mechanical helpers and obvious stored state need concise documentation
only when it improves understanding. Do not add repetitive docstrings or
attribute descriptions that merely restate assignments or types.

Meaningful local state
----------------------

Scientifically, numerically, or architecturally meaningful local variables need
nearby comments explaining their role, invariants, or algorithmic choices.
Examples include transformed or canonicalized values, intermediate mathematical
objects, residuals, norms, eigenvalues or singular values, masks or index maps,
compatibility findings, validation state, unit conversions, tolerance-dependent
values, array shapes or coordinate transformations, derived physical quantities,
and deterministic ordering state.  Comments must not merely paraphrase the
assignment.

Numerical and validation documentation
--------------------------------------

Every nontrivial numerical algorithm must document the represented mathematical
operation, numerical algorithm, appropriateness of the algorithm, assumptions,
array shape and dtype, numerical failure modes, invariance properties, Hermitian
or general-matrix scope, tolerance ownership, and physical units when present.

Every public validation rule must be documented in the defining source docstring,
corresponding tests, and Sphinx API or concept documentation when it affects
users.  ``TypeError`` is used for values of the wrong semantic type;
``ValueError`` is used for values of the correct semantic type that violate an
invariant.  Boolean values are not accepted as integers or real numbers unless
Boolean semantics are explicitly intended.  Numeric strings are not silently
converted.  NumPy scalar values may be accepted only where documented and must be
canonicalized to built-in Python scalar types at public Python/Rust boundaries.

VVUQ test classification
------------------------

Constructor rejection, schema rejection, public API behavior, intrinsic
invariant enforcement, exception taxonomy, ownership, immutability, exact value
semantics, serialization contracts, technical integration, and Workflow
composition are software verification: they show that implementation satisfies
its documented software contract.

Numerical verification is distinct evidence that a numerical algorithm correctly
implements or approximates a stated mathematical operation.  It includes
analytically checkable reference cases, manufactured solutions, convergence and
observed-order studies, floating-point scaling, conditioning, roundoff analysis,
limiting cases, and cross-implementation conformance. Numerical verification
does not establish physical model adequacy.

Scientific validation requires independent physical or scientific reference
evidence for a declared intended use, such as converged DFT references,
validated Wannier representations, benchmark data, experimental observables,
binding energies, effective masses, state or subspace fidelities, or justified
operator-residual acceptance thresholds. Constructor validation and schema
validation must not be called scientific validation.

Uncertainty quantification requires declared uncertainty sources and propagation
to reported intervals or distributions. Deterministic tolerance checks alone are
not uncertainty quantification.

Synchronization and completion gate
-----------------------------------

Source docstrings, tests, public schemas, fixtures, Sphinx API pages, Sphinx
concept pages, examples, and repository architecture documentation must describe
the same behavior where they cover the same contract. Authority follows
``AGENTS.md``: current human instruction and durable decisions; accepted
scientific and public contracts; root and scoped ``AGENTS.md``; active control
records; applicable procedures; then derived reports and historical evidence.

Completion gates are proportional to the changed surface. Public APIs,
scientific or numerical meaning, serialized contracts, units, assumptions, and
non-obvious invariants require complete synchronized documentation and the
applicable warnings-as-errors Sphinx build. Routine internal changes require
only affected documentation and relevant validation. Read-only documentation
review is required when an accepted task or material public-contract change
calls for it, not automatically for every maintained-source edit. Reports must
not infer scientific validation or uncertainty quantification from
software-verification success.

Python-version policy
---------------------

The maintained Python package targets Python 3.14.  Project metadata,
type-checking configuration, Sphinx documentation, installation documentation,
and control-plane validation commands must not claim compatibility with older
Python versions unless those versions are explicitly supported and verified.
Use Python 3.14 syntax and standard-library features where they improve clarity
and interoperability, including ``enum.StrEnum`` for string-valued public enums.
