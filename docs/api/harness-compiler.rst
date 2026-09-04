Development-harness compiler
============================

The compiler API loads one explicitly selected, complete repository source set and
constructs one immutable development-harness aggregate. Here, complete means every
required selected source family is present; it does not mean downstream graph or
evidence semantics have passed validation. Loading and
compilation grant no authority and perform no validation, persistence, projection,
protected execution, or scientific computation.

``HarnessSourceFamilyContract`` supports the plural catalog roots already owned by
resolved harness configuration. Legacy checkpoints require an explicit
``HarnessLegacyDecisionBinding``; decision identities are never inferred. The loader
receives ``PiHarnessConfiguration`` explicitly and uses it only while resolving agent
definitions. Evidence Option A reuses ``PythonModuleSource`` and preserves exact selected paths,
bytes, and source identities. Downstream Python conformance owns parsing, evidence
owners, evidence IDs, and claim boundaries; loading and compilation make no
evidence-semantic validation claim.

Sources and loading
-------------------

.. currentmodule:: ksdft2effmass.harness

.. autoclass:: HarnessSourceFamily
.. autoclass:: HarnessSourceFamilyContract
.. autoclass:: HarnessLegacyDecisionBinding
.. autoclass:: HarnessSourceContract
.. autoclass:: HarnessSourceIdentity
.. autoclass:: HarnessSourceProvenance
.. autoclass:: HarnessSourceRecord
.. autodata:: HarnessParsedValue
.. autoclass:: HarnessSourceSnapshot
.. autoclass:: HarnessSourceLoadStatus
.. autoclass:: HarnessSourceLoadSucceeded
.. autoclass:: HarnessSourceLoadFailed
.. autodata:: HarnessSourceLoadResult
.. autoclass:: HarnessRepositoryLoader
   :members:

Aggregate and compilation
-------------------------

.. autoclass:: HarnessCapabilityCatalog
.. autoclass:: HarnessResourceCatalog
.. autoclass:: HarnessEvidenceCatalog
.. autoclass:: HarnessStateIdentity
.. autoclass:: HarnessState
.. autoclass:: HarnessCompilerPhase
.. autoclass:: HarnessDiagnosticSeverity
.. autoclass:: HarnessCompilerFailureCode
.. autoclass:: HarnessCompilerDiagnostic
   :members:
.. autoclass:: HarnessCompilationStatus
.. autoclass:: HarnessCompilationSucceeded
.. autoclass:: HarnessCompilationFailed
.. autodata:: HarnessCompilationResult
.. autoclass:: HarnessCompiler
   :members:

Identity and failure boundary
-----------------------------

Derived identities use canonical UTF-8 JSON and the documented domain-separated,
length-framed SHA-256 profile. Source-contract and snapshot identities describe exact
selected source semantics; snapshot identity binds both exact source identities and
the complete typed parsed-record values. Capability and resource catalog identities exclude source
layout; the source-level evidence catalog intentionally includes exact Python source
paths, bytes, and source identities. State identities exclude provenance, diagnostics,
and loader/compiler versions but include that selected evidence-source catalog. Failed results contain no
snapshot or state, respectively; a successful result is structural software state,
not validation or acceptance.
