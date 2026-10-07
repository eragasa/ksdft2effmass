"""Software verification for the bounded row-036 oracle resource family.

The artifact-owned tests validate three explicitly named candidate records, their local
Draft 2020-12 schema, an initially empty disposition ledger, exact pytest-node paths,
and qualification-test independence. The resource list is deliberately closed; this
module performs no ambient discovery or dynamic oracle dispatch.

Schema conformance and structural checks do not qualify an oracle or establish the
mathematics in its record. A passing candidate gate remains distinct from a later
technical disposition, scientific validation, UQ, and human acceptance.
"""

import ast
import json
from pathlib import Path
from typing import cast

import jsonschema  # type: ignore[import-untyped]
import pytest

pytestmark = [pytest.mark.unit, pytest.mark.software_verification]

type JsonScalar = None | bool | int | float | str
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]
type DispositionLink = tuple[str, str, str]


class TestPeriodic2DCommonSpaceOracleRecords:
    """Own schema, reference, independence, and disposition-chain evidence."""

    repository_root = Path(__file__).resolve().parents[6]
    numerical_resources = repository_root / (
        "python/tests/numerical_verification/ksdft2effmass/periodic2d/compare/resources"
    )
    qualification_schema_path = (
        numerical_resources / "oracle-qualification-record-v1.schema.json"
    )
    disposition_schema_path = (
        numerical_resources / "oracle-qualification-disposition-ledger-v1.schema.json"
    )
    disposition_path = numerical_resources / "oracle-qualification-dispositions-v1.json"
    record_paths = (
        numerical_resources / "dft-orthogonality-v1.oracle.json",
        numerical_resources / "centered-difference-dispersion-v1.oracle.json",
        numerical_resources / "resolved-cosine-fourier-transfer-v1.oracle.json",
    )
    numerical_ownership_path = numerical_resources / (
        "implementation-verification-ownership.json"
    )
    software_ownership_path = Path(__file__).resolve().parent / (
        "resources/implementation-verification-ownership.json"
    )

    @staticmethod
    def _read_json(path: Path) -> JsonObject:
        """Decode one maintained resource into the closed test representation.

        Parameters
        ----------
        path
            Repository path to the explicitly named JSON resource.

        Returns
        -------
        dict[str, JsonValue]
            Decoded JSON object. Schema tests establish its field-level contract.
        """
        return cast(JsonObject, json.loads(path.read_text(encoding="utf-8")))

    @staticmethod
    def _strings(value: JsonValue) -> tuple[str, ...]:
        """Narrow one schema-validated JSON string array.

        Parameters
        ----------
        value
            Decoded JSON value expected to be a list containing only strings.

        Returns
        -------
        tuple[str, ...]
            Immutable string sequence used by the bounded structural checks.
        """
        assert isinstance(value, list)
        assert all(isinstance(item, str) for item in value)
        return tuple(cast(str, item) for item in value)

    @staticmethod
    def _test_node_exists(repository_root: Path, reference: JsonObject) -> None:
        """Require the exact class-qualified pytest node named by one resource.

        Parameters
        ----------
        repository_root
            Root against which the record's repository-relative path is resolved.
        reference
            Closed ``path``/``node`` object from a validated qualification record.
        """
        path_value = reference["path"]
        node_value = reference["node"]
        assert isinstance(path_value, str)
        assert isinstance(node_value, str)
        source_path = repository_root / path_value
        assert source_path.is_file()
        class_name, method_name = node_value.split("::", maxsplit=1)
        tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=path_value)
        classes = [
            node
            for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == class_name
        ]
        assert len(classes) == 1
        methods = [
            node
            for node in classes[0].body
            if isinstance(node, ast.FunctionDef) and node.name == method_name
        ]
        assert len(methods) == 1

    @staticmethod
    def _assert_linear_disposition_chain(links: tuple[DispositionLink, ...]) -> None:
        """Require the documented single-root linear lifecycle for one oracle ID.

        Parameters
        ----------
        links
            Ordered-independent ``(decision_id, outcome, supersedes)`` records for one
            oracle identity. An empty tuple represents an undisposed candidate.
        """
        if not links:
            return
        by_id = {
            decision_id: (outcome, supersedes)
            for decision_id, outcome, supersedes in links
        }
        assert len(by_id) == len(links)
        roots = [
            decision_id
            for decision_id, (_, supersedes) in by_id.items()
            if supersedes == "not_applicable"
        ]
        assert len(roots) == 1
        successors: dict[str, list[str]] = {decision_id: [] for decision_id in by_id}
        allowed = {
            ("QUALIFIED", "QUALIFIED"),
            ("QUALIFIED", "SUSPENDED"),
            ("QUALIFIED", "RETIRED"),
            ("SUSPENDED", "QUALIFIED"),
            ("SUSPENDED", "RETIRED"),
        }
        for decision_id, (outcome, supersedes) in by_id.items():
            if supersedes == "not_applicable":
                assert outcome in {"QUALIFIED", "RETIRED"}
                continue
            assert supersedes in by_id
            successors[supersedes].append(decision_id)
            previous_outcome = by_id[supersedes][0]
            assert (previous_outcome, outcome) in allowed
        assert all(len(items) <= 1 for items in successors.values())
        terminals = [
            decision_id for decision_id, items in successors.items() if not items
        ]
        assert len(terminals) == 1

        # Root/terminal counts and successor degree alone admit a disconnected cycle.
        # Explicit traversal proves that every decision belongs to the sole root chain.
        visited: set[str] = set()
        current = roots[0]
        while True:
            assert current not in visited
            visited.add(current)
            next_decisions = successors[current]
            if not next_decisions:
                break
            current = next_decisions[0]
        assert visited == set(by_id)

    def test_schema_and_resources__candidate_family__conform(self) -> None:
        """The explicit candidate records and empty ledger conform to local schemas."""
        qualification_schema = self._read_json(self.qualification_schema_path)
        disposition_schema = self._read_json(self.disposition_schema_path)
        jsonschema.Draft202012Validator.check_schema(qualification_schema)
        jsonschema.Draft202012Validator.check_schema(disposition_schema)
        assert qualification_schema["$id"] == (
            "urn:ksdft2effmass:schema:testing:oracle-qualification-record:v1"
        )
        assert disposition_schema["$id"] == (
            "urn:ksdft2effmass:schema:testing:"
            "oracle-qualification-disposition-ledger:v1"
        )

        qualification_validator = jsonschema.Draft202012Validator(qualification_schema)
        oracle_ids: list[str] = []
        for path in self.record_paths:
            record = self._read_json(path)
            qualification_validator.validate(record)
            oracle_id = record["oracle_id"]
            assert isinstance(oracle_id, str)
            oracle_ids.append(oracle_id)
        assert len(set(oracle_ids)) == 3

        disposition = self._read_json(self.disposition_path)
        checker = jsonschema.FormatChecker()
        disposition_validator = jsonschema.Draft202012Validator(
            disposition_schema,
            format_checker=checker,
        )
        disposition_validator.validate(disposition)
        decisions = disposition["decisions"]
        # The candidate gate fails if lifecycle authority is added before the separate
        # reviewed disposition-and-status proposal and acceptance gate.
        assert decisions == []
        self._assert_linear_disposition_chain(())

    def test_ownership__candidate_modules__is_artifact_owned(self) -> None:
        """The two candidate-support modules have explicit evidence ownership."""
        numerical = self._read_json(self.numerical_ownership_path)
        software = self._read_json(self.software_ownership_path)
        numerical_modules = numerical["modules"]
        software_modules = software["modules"]
        assert isinstance(numerical_modules, list)
        assert isinstance(software_modules, list)

        expected = (
            (
                numerical_modules,
                "python/tests/numerical_verification/ksdft2effmass/periodic2d/"
                "compare/test__common_space_oracle_qualification.py",
                "numerical_verification",
                "claim_bearing",
            ),
            (
                software_modules,
                "python/tests/software_verification/ksdft2effmass/periodic2d/"
                "compare/test__common_space_oracle_records.py",
                "software_verification",
                "routine",
            ),
        )
        for modules, expected_path, evidence_class, evidence_profile in expected:
            matches = []
            for module in modules:
                assert isinstance(module, dict)
                if module.get("path") == expected_path:
                    matches.append(module)
            assert len(matches) == 1
            owner = matches[0]
            assert owner["mode"] == "artifact_owned"
            assert owner["evidence_class"] == evidence_class
            assert owner["evidence_profile"] == evidence_profile
            artifact = owner["artifact"]
            assert isinstance(artifact, str)
            assert artifact

    def test_schema__missing_representation_or_embedded_status__is_rejected(
        self,
    ) -> None:
        """The schema rejects ambiguous representation and embedded lifecycle state."""
        schema = self._read_json(self.qualification_schema_path)
        validator = jsonschema.Draft202012Validator(schema)

        missing_state_space = self._read_json(self.record_paths[0])
        representation = missing_state_space["representation_contract"]
        assert isinstance(representation, dict)
        del representation["state_spaces"]
        with pytest.raises(jsonschema.ValidationError):
            validator.validate(missing_state_space)

        embedded_status = self._read_json(self.record_paths[0])
        embedded_status["technical_status"] = "QUALIFIED"
        with pytest.raises(jsonschema.ValidationError):
            validator.validate(embedded_status)

    def test_references_and_independence__candidate_family__are_explicit(self) -> None:
        """Authorities and nodes exist; qualification avoids forbidden owners."""
        expected_ids = {
            "dft-orthogonality-v1.oracle.json": (
                "periodic2d.common-space.dft-orthogonality.v1"
            ),
            "centered-difference-dispersion-v1.oracle.json": (
                "periodic2d.common-space.centered-difference-dispersion.v1"
            ),
            "resolved-cosine-fourier-transfer-v1.oracle.json": (
                "periodic2d.common-space.resolved-cosine-fourier-transfer.v1"
            ),
        }
        bindings: dict[str, set[str]] = {}
        for path in self.record_paths:
            record = self._read_json(path)
            oracle_id = record["oracle_id"]
            authority = record["authoritative_definition"]
            implementation = record["implementation"]
            independence = record["independence_boundary"]
            comparator = record["comparator"]
            tolerance = record["tolerance"]
            assert isinstance(oracle_id, str)
            assert oracle_id == expected_ids[path.name]
            assert isinstance(authority, dict)
            assert isinstance(implementation, dict)
            assert isinstance(independence, dict)
            assert isinstance(comparator, dict)
            assert isinstance(tolerance, dict)

            authority_text_parts: list[str] = []
            for repository_path in self._strings(authority["repository_paths"]):
                authoritative_path = self.repository_root / repository_path
                assert authoritative_path.is_file()
                authority_text_parts.append(
                    authoritative_path.read_text(encoding="utf-8")
                )
            authority_text = "\n".join(authority_text_parts)
            for equation_id in self._strings(authority["equation_ids"]):
                assert equation_id in authority_text
            for section in self._strings(authority["sections"]):
                assert section in authority_text

            implementation_path = implementation["path"]
            assert isinstance(implementation_path, str)
            implementation_nodes = set(self._strings(implementation["nodes"]))
            qualification_path = self.repository_root / implementation_path
            tree = ast.parse(
                qualification_path.read_text(encoding="utf-8"),
                filename=implementation_path,
            )
            # AST inspection enforces the record-declared dependency direction without
            # importing or executing a qualification module during resource validation.
            imported_modules: set[str] = set()
            referenced_symbols: set[str] = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported_modules.update(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module is not None:
                    imported_modules.add(node.module)
                elif isinstance(node, ast.Name):
                    referenced_symbols.add(node.id)
                elif isinstance(node, ast.Attribute):
                    referenced_symbols.add(node.attr)

            for forbidden in self._strings(independence["forbidden_imports"]):
                assert all(
                    imported != forbidden and not imported.startswith(f"{forbidden}.")
                    for imported in imported_modules
                )
            for forbidden in self._strings(independence["forbidden_symbols"]):
                assert forbidden not in referenced_symbols

            qualification_references = record["qualification_evidence"]
            consumer_references = record["consumers"]
            assert isinstance(qualification_references, list)
            assert isinstance(consumer_references, list)
            qualification_nodes: set[str] = set()
            consumer_nodes: set[str] = set()
            for reference in qualification_references:
                assert isinstance(reference, dict)
                self._test_node_exists(self.repository_root, reference)
                reference_path = reference["path"]
                reference_node = reference["node"]
                assert isinstance(reference_path, str)
                assert isinstance(reference_node, str)
                assert reference_path == implementation_path
                qualification_nodes.add(reference_node)
            assert qualification_nodes == implementation_nodes
            for reference in consumer_references:
                assert isinstance(reference, dict)
                self._test_node_exists(self.repository_root, reference)
                reference_node = reference["node"]
                assert isinstance(reference_node, str)
                consumer_nodes.add(reference_node)
                bindings.setdefault(reference_node, set()).add(oracle_id)

            comparator_rules = comparator["rules"]
            tolerance_rules = tolerance["rules"]
            assert isinstance(comparator_rules, list)
            assert isinstance(tolerance_rules, list)
            comparator_nodes: set[str] = set()
            tolerance_nodes: set[str] = set()
            for rule in comparator_rules:
                assert isinstance(rule, dict)
                consumer_node = rule["consumer_node"]
                assert isinstance(consumer_node, str)
                comparator_nodes.add(consumer_node)
            for rule in tolerance_rules:
                assert isinstance(rule, dict)
                consumer_node = rule["consumer_node"]
                assert isinstance(consumer_node, str)
                tolerance_nodes.add(consumer_node)
            assert comparator_nodes == consumer_nodes
            assert tolerance_nodes == consumer_nodes

        # This closed map prevents a consumer assertion from silently gaining or losing
        # an oracle dependency while all individual record schemas still validate.
        assert bindings == {
            (
                "TestPeriodic2DCommonSpaceOperatorComparator::"
                "test_execute__equal_basis_and_grid_sides__map_is_unitary"
            ): {"periodic2d.common-space.dft-orthogonality.v1"},
            (
                "TestPeriodic2DCommonSpaceOperatorComparator::"
                "test_execute__free_operator__matches_discrete_fourier_dispersion"
            ): {
                "periodic2d.common-space.centered-difference-dispersion.v1",
                "periodic2d.common-space.dft-orthogonality.v1",
            },
            (
                "TestPeriodic2DCommonSpaceOperatorComparator::"
                "test_execute__cosine_operator__isolates_discrete_kinetic_error"
            ): {
                "periodic2d.common-space.centered-difference-dispersion.v1",
                "periodic2d.common-space.dft-orthogonality.v1",
                "periodic2d.common-space.resolved-cosine-fourier-transfer.v1",
            },
        }

    @pytest.mark.parametrize(
        "links",
        (
            (
                ("decision-1", "QUALIFIED", "not_applicable"),
                ("decision-2", "SUSPENDED", "decision-1"),
                ("decision-3", "QUALIFIED", "decision-2"),
                ("decision-4", "RETIRED", "decision-3"),
                ("decision-5", "QUALIFIED", "decision-4"),
            ),
            (
                ("decision-1", "QUALIFIED", "not_applicable"),
                ("decision-2", "SUSPENDED", "not_applicable"),
            ),
            (
                ("decision-1", "QUALIFIED", "not_applicable"),
                ("decision-2", "SUSPENDED", "decision-1"),
                ("decision-3", "RETIRED", "decision-1"),
            ),
            (
                ("decision-1", "RETIRED", "not_applicable"),
                ("decision-2", "QUALIFIED", "decision-3"),
                ("decision-3", "QUALIFIED", "decision-2"),
            ),
        ),
    )
    def test_disposition_chain__fork_root_cycle_or_retired_successor__is_rejected(
        self,
        links: tuple[DispositionLink, ...],
    ) -> None:
        """Invalid roots, forks, cycles, and post-retirement successors fail closed."""
        with pytest.raises(AssertionError):
            self._assert_linear_disposition_chain(links)
