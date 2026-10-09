r"""Routine ownership evidence for row-054 Action decomposition.

Evidence profile: routine

These tests establish cohesive instantiated ownership and documentation only. They do
not authenticate artifacts or establish numerical or scientific validity.
"""

import inspect

import pytest

from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin.convergence_regression import (  # noqa: E501
    authentication,
    correlation,
    decode,
    design,
    numerics,
    verify,
)

pytestmark = pytest.mark.software_verification


class TestPeriodic2DOptimizerRegressionActionOwnership:
    """Own structural Action and documentation evidence for row 054."""

    def test_actions__use_instantiated_owners_without_static_namespaces(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-054-OWNERSHIP-001.

        Requirement: Decoding, authentication, design, numerics, correlation, and
        orchestration belong to cohesive instantiated Actions.

        Acceptance: Every reviewed Action exposes ``execute`` and has no static or
        class-method namespace.
        """
        action_classes = (
            authentication.Periodic2DOptimizerRegressionSourceAuthenticator,
            decode.OptimizerRegressionLegacySourceDecoder,
            decode.Periodic2DOptimizerRegressionDocumentDecoder,
            design.OptimizerRegressionDesignConstructor,
            numerics.CensoredLogNormalObservationScoreEvaluator,
            numerics.CensoredLogNormalLikelihoodEvaluator,
            numerics.CensoredLogNormalClusteredCovarianceConstructor,
            correlation.Periodic2DOptimizerRegressionCorrelator,
            verify.Periodic2DOptimizerRegressionCampaignVerifier,
        )
        for action_class in action_classes:
            assert callable(action_class().execute)
            assert not any(
                isinstance(member, (staticmethod, classmethod))
                for member in vars(action_class).values()
            )

    def test_verifier__composes_request_scoped_cohesive_actions(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-054-OWNERSHIP-002.

        Requirement: The top-level verifier owns orchestration only.

        Acceptance: A fresh verifier contains exact collaborator types and no private
        computational methods.
        """
        action = verify.Periodic2DOptimizerRegressionCampaignVerifier()
        assert (
            type(action.decoder) is decode.Periodic2DOptimizerRegressionDocumentDecoder
        )
        assert (
            type(action.source_authenticator)
            is authentication.Periodic2DOptimizerRegressionSourceAuthenticator
        )
        assert (
            type(action.correlator)
            is correlation.Periodic2DOptimizerRegressionCorrelator
        )
        private_computations = {
            name
            for name, member in vars(type(action)).items()
            if name.startswith("_") and not name.startswith("__") and callable(member)
        }
        assert private_computations == set()

    def test_reviewed_modules__have_no_module_functions(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-054-OWNERSHIP-003.

        Requirement: Reviewed modules expose cohesive classes rather than module-level
        helper namespaces.

        Acceptance: Introspection finds no directly defined module functions.
        """
        modules = (authentication, correlation, decode, design, numerics, verify)
        found = {
            f"{module.__name__}.{name}"
            for module in modules
            for name, value in inspect.getmembers(module, inspect.isfunction)
            if value.__module__ == module.__name__
        }
        assert found == set()

    def test_public_methods__retain_numpy_style_contract_sections(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-054-OWNERSHIP-004.

        Requirement: Public reviewed methods document inputs, non-None outputs, and
        propagated exceptions with NumPy-style sections.

        Acceptance: No applicable section is absent.
        """
        modules = (authentication, correlation, decode, design, numerics, verify)
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
