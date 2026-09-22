Coding-standards conformance
============================

The public conformance surface evaluates one explicitly identified source subject
against one identified policy.  A profile binds every policy rule to an exact
adapter version and configuration identity; it cannot omit or reclassify a
requirement.  Inputs carry caller-supplied paths, byte counts, SHA-256 identities,
and either exact bytes or a represented read failure.

``CodingStandardsConformanceValidator`` performs no current-directory discovery,
filesystem reads, repair, test execution, promotion, or authority selection.
Missing inputs, identity disagreement, incomplete profiles, unavailable adapters,
and incompatible versions produce blocking normalized ``error`` results.  Executed
rules return the shared immutable ``ValidationResult`` contract.

The version-one Python adapter preserves implemented maintained-evidence diagnostics
under one compatibility rule and adds explicitly selected project rules for:

* class-owned pytest tests and helpers;
* exact ``@pytest.fixture`` entry points and allowlisted pytest hooks in
  ``conftest.py``;
* class-owned test-method documentation;
* ``typing.Any`` and ``cast(Any, ...)``;
* generic ``object`` annotations unless configuration explicitly identifies a
  ``path:line`` whose declared domain genuinely includes every Python object;
* erased container annotations; and
* authored test-resource placement.

``PythonCodingStandardsContract`` constructs the identified version-one policy,
immutable adapter configuration, and complete profile.  Universal-object exceptions
are sorted unique ``path:line`` values in that identified configuration; they are
never inferred from syntax.  It performs no ambient selection.  Existing callers may continue using ``PythonConformanceValidator``;
the normalized adapter does not silently replace or weaken that compatibility
surface.

``ConformanceReportProjector`` derives a compact immutable view from one exact
validation result.  The report is not policy authority, source authority, promotion
evidence, or a maintained documentation projection.

API reference
-------------

.. currentmodule:: ksdft2effmass.harness

.. autoclass:: ConformanceInputRole
   :members:
.. autoclass:: ConformanceInput
   :members:
.. autoclass:: ConformanceSubject
   :members:
.. autoclass:: CodingStandardRequirement
.. autoclass:: CodingStandardsPolicy
   :members:
.. autoclass:: ConformanceAdapterConfiguration
.. autoclass:: ConformanceProfileBinding
   :members:
.. autoclass:: ConformanceProfile
.. autoclass:: CodingStandardsAdapter
   :members:
.. autoclass:: ConformanceRequest
.. autoclass:: CodingStandardsConformanceValidator
   :members:
.. autoclass:: ConformanceReport
.. autoclass:: ConformanceReportProjector
   :members:
.. autoclass:: PythonCodingStandardsContract
   :members:
.. autoclass:: PythonCodingStandardsAdapter
   :members:
