Historical CPN v1 contract software verification
================================================

Retirement status
-----------------

This page retains the software-verification record for the retired
``ksdft2effmass.workflows.cpn`` version-1 API. Its inventories, node names, counts,
and present-tense contract statements describe the accepted historical evidence at
the time it was maintained; those tests and the 49-name runtime are no longer live.
The current generic API and evidence are owned by
``ksdft2effmass.petrinet.colored``. This retained record is not a compatibility
promise, executable verification inventory, scientific claim, or release claim.

Evidence classification and ownership
-------------------------------------

P1 evidence is software verification and language-neutral contract-conformance
evidence. It is not numerical verification, scientific validation, uncertainty
quantification, persistence verification, SNAKES-adapter verification, Rust
conformance, or scientific-execution authorization.

Stable identifiers ``SV-CPN-001`` through ``SV-CPN-088`` are contiguous and
unique. The maintained P1 surface has 88 ordinary pytest test functions, which
collect 91 parameter cases across 32 one-class object modules and five
artifact-owned integration modules. Every object module is named
``test__ClassName.py``, declares exactly that exported class as its sole primary
system under test, and carries the executable
``pytest.mark.software_verification`` module marker. Collaborators construct
synthetic setup only; assertions concern state, behavior, results, or structured
errors owned by the named class.

Exactly 18 dedicated class modules were added by the bounded completeness
correction:

* ``ArcDefinition`` and ``ColorDefinition``;
* ``CpnContractError``, ``CpnErrorDetail``, ``CpnNetDefinition``,
  ``CpnValidationIssue``, and ``CpnValidationResult``;
* ``GuardEvaluationResult``, ``InputInscription``, and ``OutputInscription``;
* ``PlaceDefinition`` and ``PlaceMarking``;
* ``TokenBinding``, ``TokenFieldAssignment``, ``TokenPattern``, and
  ``TokenTemplate``;
* ``TransitionBinding`` and ``TransitionDefinition``.

Together with the 14 previously dedicated owners, these modules provide one
module for each of the 32 public concrete classes covered by the manifest. The
17 remaining public exports are enums or marker-exception types for which the
P1 test-module rule does not require a dedicated class module; their branches
are exercised through their concrete object owners. This exception is explicit
inventory state, not a claim that an untested public class is complete.

The ownership manifest at
``.pi/evidence/backend-neutral-cpn-P1-contract/test-ownership-manifest.json``
records all 49 public exports, dedicated-module status, evidence IDs,
requirements, and every former module/test/assertion partition. It preserves
``SV-CPN-001`` through ``SV-CPN-034``, the five explicit assertion splits at
``SV-CPN-035`` through ``SV-CPN-039``, the completeness extension at
``SV-CPN-040`` through ``SV-CPN-079``, and the bounded numeric-contract evidence
at ``SV-CPN-080`` through ``SV-CPN-088``. The accompanying
``test-completeness-matrix.json`` records the maintained module, function, and
collected-case totals.

Artifact-owned integration evidence
-----------------------------------

Package topology and specification-fixture orchestration are not class-owned.
Five maintained integration modules under
``python/tests/software_verification/ksdft2effmass/integration/`` own that
evidence:

* ``test__workflow_cpn_python_public_api.py`` owns the public Python package
  surface at
  ``test_artifact__public_api__exposes_approved_export_inventory``;
* ``test__workflow_cpn_v1_python_json_contract.py`` is boundary-owned by the
  version-1 CPN Python runtime <-> version-1 CPN JSON Schema/wire contract;
* ``test__workflow_cpn_v1_json_fixtures_python_runtime_contract.py`` owns the
  version-1 JSON fixture family and its Python-runtime checks;
* ``test__workflow_cpn_python_import_dependency_direction.py`` owns the
  directional production import topology; and
* ``test__workflow_cpn_python_snakes_and_deferred_engine_isolation.py`` owns
  Python isolation from SNAKES and the deferred engine/persistence scope.

These modules provide ordinary-pytest ownership for ``SV-CPN-023`` and
``SV-CPN-027`` through ``SV-CPN-033``. They cover the 49-name public export
inventory, schema metaschema validity, local schema entry points, valid and
invalid fixture sets, relational fixture orchestration, dependency direction,
and isolation. Current semantic nodes include
``test_artifact__json_schemas__satisfy_draft_2020_12_metaschema``,
``test_artifact__schema_entry_points__resolve_locally_and_match_public_enums``,
``test_artifact__valid_json_fixtures__conform_to_declared_schemas``,
``test_artifact__import_dependency_direction__follows_approved_layers``, and
``test_artifact__snakes_isolation__excludes_deferred_engine_scope``.
``contract_gates.py`` invokes and audits this pytest evidence; it is not an
evidence implementation owner.

``SV-CPN-028`` remains one accepted conjunctive nonnumeric boundary requirement:
local schema resolution, required-definition agreement, closed-enum agreement,
and representative wire agreement remain facets of that single requirement.
The migration does not split it or create new evidence identifiers. Numeric
runtime/wire agreement remains separately owned by ``SV-CPN-087`` and
``SV-CPN-088``.

Class filenames, artifact and boundary names, directional relations, and genuine
Workflow ownership follow the concise rules in :doc:`testing-and-evidence`; the
complete shared convention is
``.pi/skills/develop-python-test-evidence/references/test-evidence-conventions.md``.

The deterministic completeness command is::

  cd python
  uv run python ../.pi/evidence/backend-neutral-cpn-P1-contract/validate_test_ownership.py

The validator enforces canonical filenames, one declared public owner per
object module, module markers and documentation, manifest agreement, structural
owner exercise, unique contiguous IDs, predecessor and split-map traceability,
export inventory, and the five artifact- or boundary-owned integration modules.
Historical reviews retain their original paths and counts; their combined-module
inventories and predecessor filenames are explicitly historical evidence, not
current replay paths or edited findings.

Fixture inventory and acceptance
--------------------------------

``specification/workflow-cpn/v1`` contains fixed net, marking, firing,
validation, executable-result, error, and shared-contract schemas. Synthetic
valid fixtures expose a minimal net, multiset marking, synchronized firing,
retry/recovery/iteration state, and scoped outcomes. Invalid fixtures separate
structural rejection from relations that require public ActionObjects.

The two-cycle firing evidence verifies repeated transition execution with
successive explicit authorization tokens. Their ``iteration_index`` values are
supplied routing data and copied into outputs; the evidence does not verify
arithmetic or automatic ``current + 1`` advancement. Version 1 provides neither.
Repeated index values are permitted. Future automatic advancement would require
a future ActionObject or a separately authorized expression revision.

Acceptance requires the ownership validator, focused class-owned pytest, full
Python suite, Ruff format/check, mypy, strict evidence audit, Sphinx
warnings-as-errors, checkpoint validation, checksum validation, and
``git diff --check``. The strict evidence audit retains exactly 22 pre-existing
non-P1 unowned-test warnings as a separately classified baseline.

Deterministic branch completion and limitations
-----------------------------------------------

Nine existing object modules own the deterministic branch-completion evidence:
``ContractValue`` (``SV-CPN-058``--``060``), ``CpnMarking`` (``061``--``062``),
``CpnToken`` (``063``--``067``), ``FiringRequest`` (``068``--``069``),
``FiringResult`` (``070``--``073``), ``GuardExpression`` (``074``--``075``),
``TokenOutcome`` (``076``), ``TransitionEnablementResult`` (``077``), and
``ValueExpression`` (``078``--``079``). These are deterministic software
contract checks only.

The bounded numeric-contract evidence is now implemented. ``SV-CPN-080``
verifies that tagged ``REAL`` accepts finite exact built-in Python ``int`` and
``float`` values except ``bool``, canonicalizes to a built-in IEEE-754 binary64
``float`` using round-to-nearest, ties-to-even, permits documented large-integer
rounding, and maps conversion overflow or nonfinite state to ``ValueError``.
``SV-CPN-087`` distinguishes the two exact tagged-``REAL`` conversion domains.
General noninteger number values are bounded inclusively by
:math:`\pm M`, where
:math:`M=(2-2^{-52})2^{1023}=2^{1024}-2^{971}` is the maximum finite binary64
value. Built-in Python ``int`` values and integer-valued JSON ``real`` inputs
are admitted through the exact inclusive endpoints :math:`\pm L`, where
:math:`L=2^{1024}-2^{970}-1`. The evidence verifies that integer values above
:math:`M`, including :math:`M+1` and :math:`L`, are admitted and round to finite
:math:`M`, while both signs of :math:`L+1` overflow or fail schema validation.
Strict JSON wire input excludes ``NaN``, ``Infinity``, and ``-Infinity``. A
Python ``nan`` passed directly to ``jsonschema`` is an in-memory instance
outside the permitted wire form; the evidence therefore does not treat that
library's ordered-bound behavior for ``nan`` as wire acceptance.
``SV-CPN-081`` verifies the exact signed-i64 ``INTEGER`` interval.
``SV-CPN-082``--``SV-CPN-085`` cover the
nonnegative signed-i64 interval for expression-visible token controls, marking
and prior revisions, and expression routing while preserving the separate
nonarithmetic ``iteration_index`` semantics. ``SV-CPN-086`` verifies structured
``REVISION_OVERFLOW`` before output evaluation or successor construction at
revision ``2**63 - 1``. ``SV-CPN-087``--``SV-CPN-088`` verify matching schema
numeric tags and bounds. There is no unsigned ``ContractValue`` kind. The
intended Rust mappings are ``f64`` for ``REAL``, ``i64`` for ``INTEGER``, and
nonnegative controls represented within the ``i64`` range; this is contract
agreement, not Rust conformance evidence.

JSON Schema cannot decide cross-object graph references, enabledness, output
identity novelty, or sibling-field equality. P1 adds no serializer,
authoritative persistence, SNAKES adapter, concrete workflow, external
execution, scientific payload, Rust implementation, or cross-language
conformance test. True u64 artifact sizes and counters are deferred to explicitly
typed P2 fields and are not implemented. ``P1-HC01`` Option A and ``P1-HC02``
Option B are resolved. Final P1 acceptance was granted as Option A through
``P1-HC03`` on 2026-08-04, after reviews and parent verification; P1 is closed
as human-accepted ``PASS``. No successor was selected or launched, and P2--P11
and production or scientific execution remain blocked and unauthorized.
