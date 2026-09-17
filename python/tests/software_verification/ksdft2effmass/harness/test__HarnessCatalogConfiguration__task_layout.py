r"""Software verification of ``HarnessCatalogConfiguration``.

Evidence profile: routine

Bounded artifact scope: required categorized Task layout and other catalog roots.

Facet and represented meaning

The public value requires an explicit categorized component. The human-approved
clean cutover retires the flat constructor rather than keeping a compatibility API.

Intrinsic and cross-object scope

Composition owns component typing and exact catalog collisions; categorized root
lexical validity is independently owned by TaskCatalogConfiguration.

VVUQ and scientific exclusions

Software verification only; no discovery, migration or execution authority.
"""

import pytest
from ksdft2effmass.harness import HarnessCatalogConfiguration, TaskCatalogConfiguration

pytestmark = pytest.mark.software_verification
SUT = HarnessCatalogConfiguration


class TestHarnessCatalogConfigurationTaskLayout:
    """Own the required categorized composition facet."""

    def test_constructor__categorized__preserves_named_component(self) -> None:
        """Evidence ID: software-verification.task-catalog.composition.categorized

        Requirement: Categorized composition carries the exact immutable component.

        Acceptance: The supplied component is retained without an obsolete flat field.
        """
        tasks = TaskCatalogConfiguration("research", "simulation", "software")
        value = SUT(tasks, ("agents",), ("checkpoints",), ("skills",))
        assert value.task_catalog is tasks
        assert not hasattr(value, "task_root")

    @pytest.mark.parametrize(
        "component",
        (
            pytest.param(None, id="missing_component"),
            pytest.param("tasks", id="retired_flat_root"),
            pytest.param(("research", "simulation", "software"), id="structural_tuple"),
        ),
    )
    def test_constructor__component_type__rejects_unnamed_substitutes(
        self, component: None | str | tuple[str, ...]
    ) -> None:
        """Evidence ID: software-verification.task-catalog.composition.required-type

        Requirement: Neither legacy flat construction nor structural substitutes
        may bypass the named categorized component.

        Acceptance: Each wrong-semantic-type partition raises TypeError.
        """
        with pytest.raises(TypeError, match="TaskCatalogConfiguration"):
            SUT(component, ("agents",), ("checkpoints",), ("skills",))  # type: ignore[arg-type]

    def test_constructor__legacy_keyword__rejects_obsolete_option(self) -> None:
        """Evidence ID: software-verification.task-catalog.composition.retired-keyword

        Requirement: The retired flat field must not remain a compatibility option.

        Acceptance: Supplying task_root is rejected as an unsupported argument.
        """
        tasks = TaskCatalogConfiguration("research", "simulation", "software")
        with pytest.raises(TypeError, match="task_root"):
            SUT(tasks, ("agents",), ("checkpoints",), ("skills",), task_root="old")  # type: ignore[call-arg]

    @pytest.mark.parametrize(
        "agent_root",
        (
            pytest.param("research", id="research_collision"),
            pytest.param("simulation", id="simulation_collision"),
            pytest.param("software", id="software_collision"),
        ),
    )
    def test_constructor__catalogs__rejects_cross_category_collision(
        self, agent_root: str
    ) -> None:
        """Evidence ID: software-verification.task-catalog.composition.collision

        Requirement: Task roots cannot exactly repeat another catalog's root.

        Acceptance: Each category collision raises ValueError.
        """
        tasks = TaskCatalogConfiguration("research", "simulation", "software")
        with pytest.raises(ValueError, match="may not repeat"):
            SUT(tasks, (agent_root,), ("checkpoints",), ("skills",))
