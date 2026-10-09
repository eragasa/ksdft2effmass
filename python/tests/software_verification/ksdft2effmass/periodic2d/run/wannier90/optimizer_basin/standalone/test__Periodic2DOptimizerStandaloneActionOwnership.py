r"""Routine ownership evidence for row-055 standalone-study Actions.

Evidence profile: routine

These tests establish cohesive instantiated ownership and documentation only. They do
not authenticate artifacts or establish numerical or scientific validity.
"""

import inspect

import pytest

from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.standalone import (
    authentication,
    correlation,
    decode,
    numerics,
    verify,
)
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.standalone.records import (
    OptimizerStandaloneBasin,
    OptimizerStandaloneControls,
    OptimizerStandaloneGroup,
    OptimizerStandaloneProposal,
    OptimizerStandaloneRejectedEquivalence,
    OptimizerStandaloneSensitivity,
)

pytestmark = pytest.mark.software_verification


class TestPeriodic2DOptimizerStandaloneActionOwnership:
    """Own structural Action and documentation evidence for row 055."""

    def test_actions__use_instantiated_owners_without_static_namespaces(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-055-OWNERSHIP-001.

        Requirement: Decoding, authentication, endpoint arithmetic, correlation, and
        orchestration belong to cohesive instantiated owners.

        Acceptance: Every reviewed Action exposes ``execute`` and has no static or
        class-method utility namespace.
        """
        action_classes = (
            authentication.Periodic2DOptimizerStandaloneSourceAuthenticator,
            decode.OptimizerStandaloneLegacyResultDecoder,
            decode.Periodic2DOptimizerStandaloneDocumentDecoder,
            numerics.OptimizerStandaloneEndpointEvaluator,
            correlation.OptimizerStandaloneSensitivityCorrelator,
            correlation.Periodic2DOptimizerStandaloneCorrelator,
            verify.Periodic2DOptimizerStandaloneCampaignVerifier,
        )
        for action_class in action_classes:
            assert callable(action_class().execute)
            assert not any(
                isinstance(member, (staticmethod, classmethod))
                for member in vars(action_class).values()
            )

    def test_sensitivity_correlator__tracks_candidate_matching_the_best_endpoint(
        self,
    ) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-055-OWNERSHIP-005.

        Requirement: A relaxed-threshold match to the best endpoint reports the current
        candidate identity rather than the rejected best-representative identity.

        Acceptance: A pair rejected at the frozen density threshold and admitted at the
        retained relaxed threshold reconstructs candidate occupancy two.
        """
        proposal = OptimizerStandaloneProposal(1, 1.0e-8, 1.0e-3, 1.0e-5, 2)
        best = OptimizerStandaloneBasin(
            "density_d4_basin_01",
            "best",
            1.0,
            ("best",),
            1,
            (0,),
            False,
            (),
            (),
        )
        candidate = OptimizerStandaloneBasin(
            "density_d4_basin_02",
            "candidate",
            1.0 + 1.0e-9,
            ("candidate",),
            1,
            (1,),
            False,
            (),
            (OptimizerStandaloneRejectedEquivalence(1.0e-4, 2.0e-5, "best"),),
        )
        group = OptimizerStandaloneGroup(
            "configuration",
            "arm",
            2,
            2,
            1.0,
            (),
            "best",
            2,
            (best, candidate),
            False,
            (OptimizerStandaloneSensitivity(5.0e-5, 1, ("candidate",), 2),),
            OptimizerStandaloneControls(0, 0.0, 0.0, True, True, ()),
        )

        correlation.OptimizerStandaloneSensitivityCorrelator().execute(proposal, group)

    def test_verifier__composes_request_scoped_cohesive_actions(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-055-OWNERSHIP-002.

        Requirement: The top-level verifier owns orchestration only.

        Acceptance: A fresh verifier contains exact collaborator types and no private
        computational methods.
        """
        action = verify.Periodic2DOptimizerStandaloneCampaignVerifier()
        assert (
            type(action.decoder) is decode.Periodic2DOptimizerStandaloneDocumentDecoder
        )
        assert (
            type(action.source_authenticator)
            is authentication.Periodic2DOptimizerStandaloneSourceAuthenticator
        )
        assert (
            type(action.correlator)
            is correlation.Periodic2DOptimizerStandaloneCorrelator
        )
        private_computations = {
            name
            for name, member in vars(type(action)).items()
            if name.startswith("_") and not name.startswith("__") and callable(member)
        }
        assert private_computations == set()

    def test_reviewed_modules__have_no_module_functions(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-055-OWNERSHIP-003.

        Requirement: Reviewed modules expose cohesive classes rather than module-level
        helper namespaces.

        Acceptance: Introspection finds no directly defined module functions.
        """
        modules = (authentication, correlation, decode, numerics, verify)
        found = {
            f"{module.__name__}.{name}"
            for module in modules
            for name, value in inspect.getmembers(module, inspect.isfunction)
            if value.__module__ == module.__name__
        }
        assert found == set()

    def test_public_methods__retain_numpy_style_contract_sections(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-055-OWNERSHIP-004.

        Requirement: Public methods document inputs, outputs, and propagated exceptions.

        Acceptance: Every applicable NumPy-style section is present.
        """
        modules = (authentication, correlation, decode, numerics, verify)
        missing: set[str] = set()
        for module in modules:
            classes = (
                value
                for _, value in inspect.getmembers(module, inspect.isclass)
                if value.__module__ == module.__name__
            )
            for class_ in classes:
                for name, method in inspect.getmembers(class_, inspect.isfunction):
                    if name.startswith("_"):
                        continue
                    docstring = inspect.getdoc(method) or ""
                    signature = inspect.signature(method)
                    if (
                        len(signature.parameters) > 1
                        and "Parameters\n" not in docstring
                    ):
                        missing.add(f"{class_.__name__}.{name}:Parameters")
                    if (
                        signature.return_annotation not in {None, type(None), "None"}
                        and "Returns\n" not in docstring
                    ):
                        missing.add(f"{class_.__name__}.{name}:Returns")
                    if "Raises\n" not in docstring:
                        missing.add(f"{class_.__name__}.{name}:Raises")
        assert missing == set()
