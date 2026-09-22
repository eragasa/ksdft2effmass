r"""Software verification of ``TaskCatalogConfiguration``.

Evidence profile: routine

Bounded artifact scope: immutable, explicit categorized Task root values.

Facet and represented meaning

The class represents three lexical repository-relative directory paths, not files
or execution permissions. The approved Task catalog plan is the contract oracle.

Intrinsic and cross-object scope

Construction owns exact strings and pairwise component-aware non-overlap. File
existence, symlinks, Task discovery and aggregate wire versions belong elsewhere.

VVUQ and scientific exclusions

Software verification only; no filesystem alias detection or scientific validity.
"""

from dataclasses import FrozenInstanceError, fields

import pytest

from ksdft2effmass.harness import TaskCatalogConfiguration

pytestmark = pytest.mark.software_verification
SUT = TaskCatalogConfiguration


class TestTaskCatalogConfiguration:
    """Own intrinsic lexical and immutable-value evidence."""

    def test_field__inventory__matches_explicit_required_roots(self) -> None:
        """Evidence ID: software-verification.task-catalog.value.inventory

        Requirement: Exactly three required roots represent the categorized value.

        Acceptance: Dataclass field names and constructed values match literals.
        """
        value = TaskCatalogConfiguration("questions", "calculations", "code")
        assert tuple(field.name for field in fields(value)) == (
            "research_root",
            "simulation_root",
            "software_root",
        )
        assert (value.research_root, value.simulation_root, value.software_root) == (
            "questions",
            "calculations",
            "code",
        )

    def test_field__immutability__rejects_mutation(self) -> None:
        """Evidence ID: software-verification.task-catalog.value.immutability

        Requirement: The roots are frozen and have no mutable instance dictionary.

        Acceptance: Assignment raises FrozenInstanceError and __dict__ is absent.
        """
        value = TaskCatalogConfiguration("research", "simulation", "software")
        with pytest.raises(FrozenInstanceError):
            value.research_root = "replacement"  # type: ignore[misc]
        assert not hasattr(value, "__dict__")

    def test_method__eq__preserves_exact_value_semantics(self) -> None:
        """Evidence ID: software-verification.task-catalog.value.equality

        Requirement: Equality uses the exact named values, without normalization.

        Acceptance: Equal values compare and hash equally; case changes differ.
        """
        value = TaskCatalogConfiguration("research", "simulation", "software")
        equal = TaskCatalogConfiguration("research", "simulation", "software")
        different = TaskCatalogConfiguration("Research", "simulation", "software")
        assert value == equal
        assert hash(value) == hash(equal)
        assert value != different

    @pytest.mark.parametrize(
        "root",
        (
            pytest.param("", id="empty"),
            pytest.param("/research", id="absolute"),
            pytest.param("C:research", id="drive_prefix"),
            pytest.param("tasks/../research", id="parent_traversal"),
            pytest.param("tasks/./research", id="current_segment"),
            pytest.param("tasks//research", id="empty_segment"),
            pytest.param("tasks/research/", id="trailing_separator"),
            pytest.param("tasks\\research", id="backslash"),
            pytest.param("tasks/CON.json", id="reserved_device"),
            pytest.param("re\u0301search", id="non_nfc"),
            pytest.param("tasks/\nresearch", id="control"),
            pytest.param("tasks/\u2028research", id="unicode_line_separator"),
            pytest.param("tasks/\ud800research", id="surrogate"),
        ),
    )
    def test_constructor__paths__rejects_invalid_lexical_values(
        self, root: str
    ) -> None:
        """Evidence ID: software-verification.task-catalog.value.invalid-paths

        Requirement: Category roots obey the existing Harness path contract.

        Acceptance: Every named invalid lexical partition raises ValueError.
        """
        with pytest.raises(ValueError):
            TaskCatalogConfiguration(root, "simulation", "software")

    @pytest.mark.parametrize(
        "roots",
        (
            pytest.param((True, "simulation", "software"), id="boolean_research"),
            pytest.param((42, "simulation", "software"), id="integer_research"),
            pytest.param((None, "simulation", "software"), id="null_research"),
            pytest.param((b"research", "simulation", "software"), id="bytes_research"),
            pytest.param(("research", False, "software"), id="boolean_simulation"),
            pytest.param(("research", "simulation", None), id="null_software"),
        ),
    )
    def test_constructor__types__rejects_non_string_roots(
        self, roots: tuple[str | bool | int | bytes | None, ...]
    ) -> None:
        """Evidence ID: software-verification.task-catalog.value.wrong-types

        Requirement: Every root requires an exact string, without coercion.

        Acceptance: Each closed invalid-type case raises TypeError.
        """
        with pytest.raises(TypeError):
            TaskCatalogConfiguration(*roots)  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        "roots",
        (
            pytest.param(
                ("tasks/a", "tasks/a", "tasks/c"), id="equal_research_simulation"
            ),
            pytest.param(
                ("tasks/a", "tasks/b", "tasks/a"), id="equal_research_software"
            ),
            pytest.param(
                ("tasks/a", "tasks/b", "tasks/b"), id="equal_simulation_software"
            ),
            pytest.param(("tasks", "tasks/b", "code"), id="research_ancestor"),
            pytest.param(("tasks/a", "tasks", "code"), id="simulation_ancestor"),
            pytest.param(("research", "tasks/b", "tasks"), id="software_ancestor"),
            pytest.param(("tasks/A", "tasks/a", "code"), id="case_alias"),
            pytest.param(
                ("Tasks/A", "tasks/a/child", "code"), id="case_folded_ancestor"
            ),
            pytest.param(
                ("tasks/straße", "tasks/STRASSE", "code"), id="unicode_case_alias"
            ),
        ),
    )
    def test_constructor__overlap__rejects_aliases_and_ancestors(
        self, roots: tuple[str, str, str]
    ) -> None:
        """Evidence ID: software-verification.task-catalog.value.overlap

        Requirement: No pair may overlap by path components after case folding.

        Acceptance: Equal, nested and case-aliased partitions raise ValueError.
        """
        with pytest.raises(ValueError, match="overlap or alias"):
            TaskCatalogConfiguration(*roots)

    def test_constructor__siblings__accepts_near_prefixes(self) -> None:
        """Evidence ID: software-verification.task-catalog.value.siblings

        Requirement: Similar spelling without a shared directory boundary is valid.

        Acceptance: Near-prefix siblings and NFC Unicode survive unchanged.
        """
        value = TaskCatalogConfiguration(
            "tasks/research", "tasks/research-extra", "tasks/études"
        )
        assert value.simulation_root == "tasks/research-extra"
        assert value.software_root == "tasks/études"
