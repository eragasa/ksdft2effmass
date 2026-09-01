r"""Software verification of ``QuantumEspressoXsdDocumentParser``.

Evidence profile: routine

Bounded artifact scope: mechanical QEXSD 23.03.10 parsing from explicit bytes.

Facet and represented meaning

The parser recognizes the bounded root/version and preserves native source order.

Intrinsic and cross-object scope

Parsing and structural relationships are tested; semantic adaptation is excluded.

VVUQ and scientific exclusions

The reduced XML is a controlled fixture, not exhaustive QEXSD support or physical data.
"""

import builtins

import pytest
from qexsd_fixtures import CONTROLLED_QEXSD, controlled_source_bytes

from ksdft2effmass.io.quantum_espresso.qexsd import (
    QexsdSource,
    QuantumEspressoXsdDocumentParser,
)

SUT = QuantumEspressoXsdDocumentParser
pytestmark = pytest.mark.software_verification


def make_source(content: bytes = CONTROLLED_QEXSD) -> QexsdSource:
    """Build an explicit controlled source for parser evidence.

    Evidence ID: Helper owns no identifier.

    Requirement: Support the named tests without owning evidence.

    Acceptance: Return deterministic controlled support data.
    """
    digest, count = controlled_source_bytes(content)
    return QexsdSource("/controlled/data-file-schema.xml", digest, count, content)


def test_method__execute__extracts_native_order_and_dimensions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Evidence ID: SV-PERIODIC-004

    Requirement: Parsing uses only supplied bytes and preserves all ordered native
    values.

    Acceptance: Expected source order, shapes, units, grids, and status are exact
    and no open occurs.
    """
    monkeypatch.setattr(
        builtins,
        "open",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("unexpected open")
        ),
    )
    document = QuantumEspressoXsdDocumentParser().execute(make_source())
    assert document.namespace.endswith("qes-1.0")
    assert document.qexsd_version == "23.03.10"
    assert document.species == (("Si", 28.086, "Si.UPF"),)
    assert tuple(atom[0] for atom in document.atoms) == (1, 2)
    assert document.direct_lattice_vectors == (
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 1.0),
    )
    assert document.k_points == ((0.0, 0.0, 0.0), (0.5, 0.0, 0.0))
    assert document.k_point_weights == (0.25, 0.75)
    assert document.eigenvalues == ((-1.0, 0.0), (-0.5, 0.5))
    assert document.occupations == ((1.0, 1.0), (1.0, 0.0))
    assert document.fft_grid == document.fft_smooth == document.fft_box == (4, 5, 6)
    assert document.exit_status == 0


@pytest.mark.parametrize(
    "content",
    [
        pytest.param(b"<broken", id="malformed_xml"),
        pytest.param(
            CONTROLLED_QEXSD.replace(b"qes/qes-1.0", b"qes/qes-2.0"),
            id="unsupported_namespace",
        ),
        pytest.param(
            CONTROLLED_QEXSD.replace(b"qes:espresso", b"qes:other", 1).replace(
                b"</qes:espresso>", b"</qes:other>"
            ),
            id="unsupported_root",
        ),
        pytest.param(
            CONTROLLED_QEXSD.replace(b"23.03.10", b"99.00.00"), id="unsupported_version"
        ),
    ],
)
def test_method__execute__rejects_unsupported_or_malformed_xml(content: bytes) -> None:
    """Evidence ID: SV-PERIODIC-005

    Requirement: Malformed XML and unsupported namespace, root, or version fail closed.

    Acceptance: Every named controlled partition raises ValueError.
    """
    with pytest.raises(ValueError):
        QuantumEspressoXsdDocumentParser().execute(make_source(content))


@pytest.mark.parametrize(
    "content",
    [
        pytest.param(
            CONTROLLED_QEXSD.replace(
                b"<total_energy><etot>-1.25</etot></total_energy>", b""
            ),
            id="missing_required_section",
        ),
        pytest.param(
            CONTROLLED_QEXSD.replace(
                b"<exit_status>0</exit_status>",
                b"<exit_status>0</exit_status><exit_status>0</exit_status>",
            ),
            id="duplicate_singleton",
        ),
        pytest.param(CONTROLLED_QEXSD.replace(b"-1.25", b"NaN"), id="nonfinite_number"),
        pytest.param(
            CONTROLLED_QEXSD.replace(b"<a1>1 0 0</a1>", b"<a1>1 0</a1>"),
            id="invalid_vector_dimension",
        ),
        pytest.param(
            CONTROLLED_QEXSD.replace(b"name='Si' index='2'", b"name='Ge' index='2'"),
            id="unresolved_species",
        ),
        pytest.param(
            CONTROLLED_QEXSD.replace(b"nat='2'", b"nat='3'"),
            id="atom_count_disagreement",
        ),
        pytest.param(
            CONTROLLED_QEXSD.replace(b"<nks>2</nks>", b"<nks>3</nks>"),
            id="spectrum_kpoint_disagreement",
        ),
        pytest.param(
            CONTROLLED_QEXSD.replace(b"size='2'>-0.5 0.5", b"size='3'>-0.5 0.5"),
            id="declared_band_size",
        ),
        pytest.param(
            CONTROLLED_QEXSD.replace(b"nr1='4'", b"nr1='0'", 1), id="invalid_fft_grid"
        ),
        pytest.param(
            CONTROLLED_QEXSD.replace(
                b"<exit_status>0</exit_status>", b"<exit_status>-1</exit_status>"
            ),
            id="invalid_exit_status",
        ),
    ],
)
def test_method__execute__rejects_structural_invariant_failures(content: bytes) -> None:
    """Evidence ID: SV-PERIODIC-006

    Requirement: Required QEXSD structural and cardinality invariants fail
    deterministically.

    Acceptance: Every named invalid controlled fixture raises ValueError.
    """
    with pytest.raises(ValueError):
        QuantumEspressoXsdDocumentParser().execute(make_source(content))
