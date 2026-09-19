r"""Software verification of explicit-input neutral Python production-source facts.

Evidence profile: claim_bearing

Bounded artifact scope: explicit-input neutral Python production-source facts.

Facet and represented meaning

This module verifies deterministic source identity, neutral AST facts, failures,
ordering, immutability, and the absence of discovery and policy classification.

Intrinsic and cross-object scope

Immutable records own intrinsic invariants; one inspector owns parsing of exact bytes.
Python syntax semantics, exact authored fixtures, and SHA-256 are the oracles.

VVUQ and scientific exclusions

Passing establishes bounded structural software behavior only. It establishes no
runtime semantics, architecture conformance, numerical verification, scientific
validation, uncertainty quantification, support disposition, or human acceptance.
"""

from __future__ import annotations

import hashlib
from dataclasses import FrozenInstanceError
from pathlib import Path, PurePosixPath

import pytest

from ksdft2effmass.harness.pi.conformance.python.production import (
    PythonProductionAllOperation,
    PythonProductionAllResolution,
    PythonProductionAugmentedOperator,
    PythonProductionCallableKind,
    PythonProductionContextKind,
    PythonProductionFailureKind,
    PythonProductionImportKind,
    PythonProductionLiteralSequenceKind,
    PythonProductionModuleInspection,
    PythonProductionSource,
    PythonProductionSourceInspector,
    PythonProductionSourceProfile,
)
from ksdft2effmass.harness.pi.conformance.python.strict import (
    PythonCodingStandardsContract,
)

pytestmark = pytest.mark.software_verification
RESOURCE_ROOT = Path(__file__).parent / "resources/production_facts"


class TestProductionSourceFacts:
    """Verify the production-source fact artifact through exact public class values."""

    @staticmethod
    def source_input(identity: str, resource: str, path: str) -> PythonProductionSource:
        """Construct one explicit input from an exact maintained resource."""
        return PythonProductionSource.from_payload(
            input_identity=identity,
            path=PurePosixPath(path),
            payload=(RESOURCE_ROOT / resource).read_bytes(),
        )

    @staticmethod
    def inspect_sources(
        *sources: PythonProductionSource,
    ) -> tuple[
        PythonProductionSourceProfile, tuple[PythonProductionModuleInspection, ...]
    ]:
        """Execute the exact profile and return its immutable module outcomes."""
        profile = PythonProductionSourceProfile()
        result = PythonProductionSourceInspector().execute(profile, sources)
        return profile, result.modules

    @staticmethod
    def prohibit_path_read(path: Path) -> bytes:
        """Fail if the explicit-input inspector attempts filesystem reading."""
        raise AssertionError(f"unexpected filesystem read: {path}")

    def test_artifact__production_facts__represents_rich_source_exactly(self) -> None:
        """Evidence ID: software-verification.harness.production-facts.rich-source

        Requirement: Valid supplied bytes retain exact identity and neutral classes,
        callables, imports, contexts, calls, and literal export syntax.

        Method: Parse the maintained rich source fixture and project each fact to its
        explicitly expected syntax fields.

        Oracle: Python syntax semantics and manual inspection of the exact fixture.

        Acceptance: SHA-256, byte count, names, lexical owners, contexts, receivers,
        operations, and effective literal exports equal the explicit expected tuples.

        Interpretation: Failure identifies identity loss, incomplete syntax facts,
        incorrect attribution, policy inference, or nondeterministic ordering.

        Limitations: The fixture is parsed but never imported or executed.
        """
        source = self.source_input(
            "rich",
            "rich_source.py.txt",
            "python/src/example/rich_source.py",
        )
        profile, modules = self.inspect_sources(source)
        module = modules[0]
        assert profile.subject_family_identity == "python.production-source"
        assert profile.profile_identity == "ksdft2effmass.python.production-facts"
        assert profile.profile_version == "1"
        assert module.path == source.path
        assert module.source_sha256 == hashlib.sha256(source.payload or b"").hexdigest()
        assert module.source_byte_count == len(source.payload or b"")
        assert module.failure is None
        assert module.facts is not None
        facts = module.facts
        assert tuple((fact.name, fact.qualified_name) for fact in facts.classes) == (
            ("Outer", "Outer"),
            ("Nested", "Outer.Nested"),
        )
        assert tuple(
            (
                fact.name,
                fact.qualified_name,
                fact.kind,
                tuple(owner.qualified_name for owner in fact.owners),
            )
            for fact in facts.callables
        ) == (
            (
                "nested_method",
                "Outer.Nested.nested_method",
                PythonProductionCallableKind.ASYNC_FUNCTION,
                ("Outer", "Outer.Nested"),
            ),
            (
                "method",
                "Outer.method",
                PythonProductionCallableKind.FUNCTION,
                ("Outer",),
            ),
            (
                "inner",
                "Outer.method.inner",
                PythonProductionCallableKind.FUNCTION,
                ("Outer", "Outer.method"),
            ),
            (
                "<lambda>@39:19",
                "Outer.method.<lambda>@39:19",
                PythonProductionCallableKind.LAMBDA,
                ("Outer", "Outer.method"),
            ),
            (
                "module_function",
                "module_function",
                PythonProductionCallableKind.FUNCTION,
                (),
            ),
        )
        assert tuple(
            (
                fact.kind,
                fact.module,
                fact.name,
                fact.alias,
                tuple(owner.qualified_name for owner in fact.owners),
                tuple((context.kind, context.expression) for context in fact.contexts),
                (
                    fact.location.line,
                    fact.location.column,
                    fact.location.end_line,
                    fact.location.end_column,
                ),
            )
            for fact in facts.imports
        ) == (
            (
                PythonProductionImportKind.FROM_IMPORT,
                "typing",
                "TYPE_CHECKING",
                None,
                (),
                (),
                (3, 19, 3, 32),
            ),
            (
                PythonProductionImportKind.IMPORT,
                "os",
                "os",
                "operating",
                (),
                (),
                (4, 7, 4, 22),
            ),
            (
                PythonProductionImportKind.FROM_IMPORT,
                None,
                "sibling",
                None,
                (),
                (),
                (5, 14, 5, 21),
            ),
            (
                PythonProductionImportKind.FROM_IMPORT,
                "package.types",
                "TypeOnly",
                "TypeAlias",
                (),
                ((PythonProductionContextKind.IF_BODY, "TYPE_CHECKING"),),
                (11, 30, 11, 51),
            ),
            (
                PythonProductionImportKind.IMPORT,
                "optional_backend",
                "optional_backend",
                None,
                (),
                ((PythonProductionContextKind.IF_BODY, "feature_enabled"),),
                (15, 11, 15, 27),
            ),
            (
                PythonProductionImportKind.IMPORT,
                "fast_backend",
                "fast_backend",
                None,
                (),
                ((PythonProductionContextKind.TRY_BODY, None),),
                (19, 11, 19, 23),
            ),
            (
                PythonProductionImportKind.IMPORT,
                "slow_backend",
                "slow_backend",
                None,
                (),
                ((PythonProductionContextKind.TRY_HANDLER, "ImportError"),),
                (22, 11, 22, 23),
            ),
            (
                PythonProductionImportKind.IMPORT,
                "local_module",
                "local_module",
                None,
                ("Outer", "Outer.method"),
                (),
                (34, 15, 34, 27),
            ),
        )
        assert tuple(
            (
                fact.callee_expression,
                fact.receiver_expression,
                fact.callee_name,
                tuple(owner.qualified_name for owner in fact.owners),
                tuple((context.kind, context.expression) for context in fact.contexts),
                (
                    fact.location.line,
                    fact.location.column,
                    fact.location.end_line,
                    fact.location.end_column,
                ),
            )
            for fact in facts.calls
        ) == (
            (
                "type_only_factory",
                None,
                "type_only_factory",
                (),
                ((PythonProductionContextKind.IF_BODY, "TYPE_CHECKING"),),
                (12, 4, 12, 23),
            ),
            (
                "conditional_factory",
                None,
                "conditional_factory",
                (),
                ((PythonProductionContextKind.IF_BODY, "feature_enabled"),),
                (16, 4, 16, 25),
            ),
            (
                "try_factory",
                None,
                "try_factory",
                (),
                ((PythonProductionContextKind.TRY_BODY, None),),
                (20, 4, 20, 17),
            ),
            (
                "handler_factory",
                None,
                "handler_factory",
                (),
                ((PythonProductionContextKind.TRY_HANDLER, "ImportError"),),
                (23, 4, 23, 21),
            ),
            ("module_factory", None, "module_factory", (), (), (25, 0, 25, 16)),
            (
                "module_factory().configure",
                "module_factory()",
                "configure",
                (),
                (),
                (25, 0, 25, 28),
            ),
            ("class_bound", None, "class_bound", (), (), (28, 15, 28, 28)),
            ("class_default", None, "class_default", (), (), (28, 31, 28, 46)),
            (
                "nested_bound",
                None,
                "nested_bound",
                ("Outer",),
                (),
                (29, 20, 29, 34),
            ),
            (
                "service.fetch",
                "service",
                "fetch",
                ("Outer", "Outer.Nested", "Outer.Nested.nested_method"),
                (),
                (31, 25, 31, 40),
            ),
            (
                "target._private",
                "target",
                "_private",
                ("Outer", "Outer.method", "Outer.method.inner"),
                (),
                (37, 19, 37, 36),
            ),
            (
                "target.public",
                "target",
                "public",
                ("Outer", "Outer.method", "Outer.method.<lambda>@39:19"),
                (),
                (39, 27, 39, 42),
            ),
            (
                "self._method",
                "self",
                "_method",
                ("Outer", "Outer.method"),
                (),
                (40, 8, 40, 22),
            ),
            ("inner", None, "inner", ("Outer", "Outer.method"), (), (41, 15, 41, 22)),
            (
                "function_bound",
                None,
                "function_bound",
                (),
                (),
                (44, 23, 44, 39),
            ),
            (
                "function_default",
                None,
                "function_default",
                (),
                (),
                (44, 42, 44, 60),
            ),
            ("Outer", None, "Outer", ("module_function",), (), (45, 11, 45, 18)),
        )
        assert tuple(
            (
                fact.operation,
                fact.raw_expression,
                fact.literal_names,
                fact.literal_sequence_kind,
                fact.augmented_operator,
            )
            for fact in facts.all_syntax
        ) == (
            (
                PythonProductionAllOperation.ASSIGN,
                "['Outer']",
                ("Outer",),
                PythonProductionLiteralSequenceKind.LIST,
                None,
            ),
            (
                PythonProductionAllOperation.AUGMENTED_ASSIGN,
                "('module_function',)",
                ("module_function",),
                PythonProductionLiteralSequenceKind.TUPLE,
                PythonProductionAugmentedOperator.ADD,
            ),
        )
        assert facts.effective_all_resolution is PythonProductionAllResolution.LITERAL
        assert facts.effective_all_names == ("Outer", "module_function")

    @pytest.mark.parametrize(
        ("source", "expected_kind", "expected_message", "expected_line"),
        (
            pytest.param(
                PythonProductionSource.from_payload(
                    input_identity="decode",
                    path=PurePosixPath("src/invalid_utf8.py"),
                    payload=(RESOURCE_ROOT / "invalid_utf8.bin").read_bytes(),
                ),
                PythonProductionFailureKind.DECODE,
                "invalid UTF-8 at byte 0: invalid start byte",
                None,
                id="invalid_utf8_bytes",
            ),
            pytest.param(
                PythonProductionSource.from_payload(
                    input_identity="syntax",
                    path=PurePosixPath("src/invalid_syntax.py"),
                    payload=(RESOURCE_ROOT / "invalid_syntax.py.txt").read_bytes(),
                ),
                PythonProductionFailureKind.SYNTAX,
                "invalid syntax",
                1,
                id="invalid_python_syntax",
            ),
            pytest.param(
                PythonProductionSource(
                    input_identity="read",
                    path=PurePosixPath("src/unreadable.py"),
                    payload=None,
                    read_error="permission denied",
                ),
                PythonProductionFailureKind.READ,
                "permission denied",
                None,
                id="represented_read_failure",
            ),
        ),
    )
    def test_artifact__production_facts__retains_one_deterministic_failure(
        self,
        source: PythonProductionSource,
        expected_kind: PythonProductionFailureKind,
        expected_message: str,
        expected_line: int | None,
    ) -> None:
        """Evidence ID: software-verification.harness.production-facts.failures

        Requirement: Decode, syntax, and represented read failures each retain one
        input outcome and never silently omit an explicitly supplied module.

        Method: Inspect controlled semantic failure partitions through one operation.

        Oracle: UTF-8 and Python parsing semantics plus exact caller read diagnostics.

        Acceptance: Each semantic case returns exactly one expected failure with exact
        path and message; byte failures retain hashlib identity while read failures do
        not.

        Interpretation: Failure identifies omission, unstable diagnostics, or identity
        loss at an explicit-input boundary.

        Limitations: Operating-system reads are not performed by the inspector.
        """
        _, modules = self.inspect_sources(source)
        module = modules[0]
        assert len(modules) == 1
        assert module.path == source.path
        assert module.facts is None
        assert module.failure is not None
        assert module.failure.kind is expected_kind
        assert module.failure.message == expected_message
        assert module.failure.line == expected_line
        if source.payload is None:
            assert module.source_sha256 is None
            assert module.source_byte_count is None
        else:
            assert module.source_sha256 == hashlib.sha256(source.payload).hexdigest()
            assert module.source_byte_count == len(source.payload)

    def test_artifact__production_facts__orders_and_retains_duplicate_paths(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.production-facts.ordering

        Requirement: Input order cannot alter canonical result order, and duplicate
        paths remain separate represented outcomes.

        Method: Inspect three inline exact modules plus reversed equal-path,
        equal-identity read failures with distinct represented diagnostics.

        Oracle: Lexicographic path then input-identity ordering from the architecture
        contract, with tuple multiplicity as the no-collapse criterion.

        Acceptance: Exact module keys are canonical, duplicate-path byte entries
        remain present, and distinct read diagnostics have the same order regardless
        of caller order.

        Interpretation: Failure identifies ambient ordering or input collapse.

        Limitations: Exact duplicate entries are value-equal but remain repeated.
        """
        sources = (
            PythonProductionSource.from_payload(
                input_identity="zeta",
                path=PurePosixPath("pkg/z.py"),
                payload=b"z = 1\n",
            ),
            PythonProductionSource.from_payload(
                input_identity="second",
                path=PurePosixPath("pkg/a.py"),
                payload=b"value = 2\n",
            ),
            PythonProductionSource.from_payload(
                input_identity="first",
                path=PurePosixPath("pkg/a.py"),
                payload=b"value = 1\n",
            ),
        )
        _, modules = self.inspect_sources(*sources)
        assert tuple(
            (item.path.as_posix(), item.input_identity) for item in modules
        ) == (
            ("pkg/a.py", "first"),
            ("pkg/a.py", "second"),
            ("pkg/z.py", "zeta"),
        )
        assert len(modules) == len(sources)
        assert modules[0].source_sha256 == hashlib.sha256(b"value = 1\n").hexdigest()
        assert modules[1].source_sha256 == hashlib.sha256(b"value = 2\n").hexdigest()

        first_failure = PythonProductionSource(
            input_identity="same",
            path=PurePosixPath("pkg/unreadable.py"),
            payload=None,
            read_error="alpha diagnostic",
        )
        second_failure = PythonProductionSource(
            input_identity="same",
            path=PurePosixPath("pkg/unreadable.py"),
            payload=None,
            read_error="zeta diagnostic",
        )
        _, forward = self.inspect_sources(first_failure, second_failure)
        _, reverse = self.inspect_sources(second_failure, first_failure)
        assert forward == reverse
        assert tuple(
            item.failure.message for item in forward if item.failure is not None
        ) == ("alpha diagnostic", "zeta diagnostic")

    @pytest.mark.parametrize(
        ("payload", "expected_resolution", "expected_names"),
        (
            pytest.param(
                b"__all__: list[str] = ['a']\n__all__ += ['b']\n",
                PythonProductionAllResolution.LITERAL,
                ("a", "b"),
                id="annotated_list_plus_list",
            ),
            pytest.param(
                b"__all__ = ['a']\n__all__ += ('b',)\n",
                PythonProductionAllResolution.LITERAL,
                ("a", "b"),
                id="list_plus_tuple",
            ),
            pytest.param(
                b"__all__ = ('a',)\n__all__ += ('b',)\n",
                PythonProductionAllResolution.LITERAL,
                ("a", "b"),
                id="tuple_plus_tuple",
            ),
            pytest.param(
                b"__all__ = ('a',)\n__all__ += ['b']\n",
                PythonProductionAllResolution.DYNAMIC,
                None,
                id="tuple_plus_list_unresolved",
            ),
        ),
    )
    def test_artifact__production_facts__resolves_only_proven_literal_partitions(
        self,
        payload: bytes,
        expected_resolution: PythonProductionAllResolution,
        expected_names: tuple[str, ...] | None,
    ) -> None:
        """Evidence ID: software-verification.harness.production-facts.literal-all

        Requirement: Effective literal exports resolve only for exact direct
        list/tuple assignments and compatible additive list/tuple partitions.

        Method: Inspect semantic partitions for annotated/direct assignment and
        list/tuple ``+=`` compatibility.

        Oracle: Python built-in list in-place addition and tuple concatenation
        semantics for exact string-literal sequences.

        Acceptance: List plus list/tuple and tuple plus tuple resolve exactly; tuple
        plus list remains dynamic with no names.

        Interpretation: Failure identifies unsound evaluation or missing exact syntax.

        Limitations: Nonliteral iterables and runtime-overridden sequence types remain
        outside the bounded resolver.
        """
        source = PythonProductionSource.from_payload(
            input_identity="literal-partition",
            path=PurePosixPath("pkg/literal_partition.py"),
            payload=payload,
        )
        _, modules = self.inspect_sources(source)
        facts = modules[0].facts
        assert facts is not None
        assert facts.effective_all_resolution is expected_resolution
        assert facts.effective_all_names == expected_names
        assert facts.all_syntax[-1].augmented_operator is (
            PythonProductionAugmentedOperator.ADD
        )

    def test_artifact__production_facts__represents_dynamic_exports_without_guessing(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.production-facts.dynamic-all

        Requirement: Dynamic and conditional ``__all__`` syntax remains unresolved
        rather than being evaluated or guessed.

        Method: Inspect exact annotated, non-add augmented, deletion, dynamic,
        mutation, and conditional assignment syntax.

        Oracle: Python assignment/call syntax and the bounded literal-only contract.

        Acceptance: Raw operations remain source ordered and effective state is exactly
        dynamic with no effective names.

        Interpretation: Failure identifies accidental evaluation or lossy export facts.

        Limitations: Runtime branch values and mutation results are intentionally
        absent.
        """
        source = PythonProductionSource.from_payload(
            input_identity="dynamic-all",
            path=PurePosixPath("pkg/dynamic.py"),
            payload=(
                b"__all__: list[str] = ['annotated']\n"
                b"__all__ -= ('removed',)\n"
                b"del __all__\n"
                b"__all__ = build_exports()\n"
                b"__all__.append('later')\n"
                b"if enabled:\n    __all__ = ['conditional']\n"
            ),
        )
        _, modules = self.inspect_sources(source)
        facts = modules[0].facts
        assert facts is not None
        assert tuple(fact.operation for fact in facts.all_syntax) == (
            PythonProductionAllOperation.ANNOTATED_ASSIGN,
            PythonProductionAllOperation.AUGMENTED_ASSIGN,
            PythonProductionAllOperation.DELETE,
            PythonProductionAllOperation.ASSIGN,
            PythonProductionAllOperation.MUTATION,
            PythonProductionAllOperation.ASSIGN,
        )
        assert facts.all_syntax[0].literal_names == ("annotated",)
        assert (
            facts.all_syntax[0].literal_sequence_kind
            is PythonProductionLiteralSequenceKind.LIST
        )
        assert (
            facts.all_syntax[1].augmented_operator
            is PythonProductionAugmentedOperator.SUBTRACT
        )
        assert facts.all_syntax[1].raw_expression == "('removed',)"
        assert facts.all_syntax[2].raw_expression is None
        assert facts.all_syntax[3].raw_expression == "build_exports()"
        assert facts.all_syntax[4].raw_expression == "__all__.append('later')"
        assert facts.all_syntax[5].literal_names == ("conditional",)
        assert tuple(context.kind for context in facts.all_syntax[5].contexts) == (
            PythonProductionContextKind.IF_BODY,
        )
        assert facts.effective_all_resolution is PythonProductionAllResolution.DYNAMIC
        assert facts.effective_all_names is None

    def test_artifact__production_facts__is_deeply_immutable(self) -> None:
        """Evidence ID: software-verification.harness.production-facts.immutability

        Requirement: Inputs, results, nested facts, and collections are operationally
        immutable and retain no mutable AST.

        Method: Inspect one module, assert tuple nesting, and attempt field mutation.

        Oracle: Frozen slotted dataclass and tuple semantics.

        Acceptance: Nested collections are tuples and assignment raises
        ``FrozenInstanceError`` without changing the represented result.

        Interpretation: Failure identifies mutable retained parser state.

        Limitations: Python runtime reflection outside ordinary public APIs is excluded.
        """
        source = PythonProductionSource.from_payload(
            input_identity="immutable",
            path=PurePosixPath("pkg/immutable.py"),
            payload=b"class Stable:\n    pass\n",
        )
        profile = PythonProductionSourceProfile()
        result = PythonProductionSourceInspector().execute(profile, (source,))
        facts = result.modules[0].facts
        assert type(result.modules) is tuple
        assert facts is not None
        assert type(facts.classes) is tuple
        with pytest.raises(FrozenInstanceError):
            result.modules = ()  # type: ignore[misc]
        assert result.modules[0].input_identity == "immutable"

    def test_artifact__production_facts__has_no_discovery_policy_or_export_effect(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Evidence ID: software-verification.harness.production-facts.boundaries

        Requirement: Inspection uses only supplied bytes, emits neutral facts, remains
        unsupported, and leaves accepted test-evidence identity unchanged.

        Method: Prohibit ``Path.read_bytes`` during execution, inspect inline bytes,
        and compare implementation/package namespaces and accepted v1 constants.

        Oracle: Exact class fields, package namespace membership, and accepted identity
        literals provide independent boundary observations.

        Acceptance: Inspection passes without a read, fact fields contain no policy
        result, new names are not re-exported, and v1 identities remain exact.

        Interpretation: Failure identifies discovery, policy, export, or compatibility
        boundary widening.

        Limitations: Existing v1 behavioral tests separately verify complete accepted
        adapter behavior.
        """

        monkeypatch.setattr(Path, "read_bytes", self.prohibit_path_read)
        source = PythonProductionSource.from_payload(
            input_identity="inline",
            path=PurePosixPath("pkg/inline.py"),
            payload=b"import dependency\ncallable_name()\n",
        )
        _, modules = self.inspect_sources(source)
        facts = modules[0].facts
        assert facts is not None
        assert tuple(fact.name for fact in facts.imports) == ("dependency",)
        assert tuple(fact.callee_name for fact in facts.calls) == ("callable_name",)
        assert not hasattr(facts, "findings")
        assert not hasattr(facts, "support_status")

        import ksdft2effmass.harness.pi.conformance.python as python_conformance

        assert not hasattr(python_conformance, "PythonProductionSourceInspector")
        assert (
            PythonCodingStandardsContract.SUBJECT_FAMILY_IDENTITY
            == "python.test-evidence"
        )
        assert PythonCodingStandardsContract.PROFILE_VERSION == "1"
