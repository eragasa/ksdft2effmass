Wannier90 artifact adapters
===========================

The :mod:`ksdft2effmass.integration.wannier90` package provides typed,
execution-independent adaptation of retained Wannier90 text artifacts. These parsers
consume bytes supplied by the caller; they do not discover files, run Wannier90, or
reproduce Wannier localization. Public artifact records and the correlator can
authenticate a complete caller-supplied inventory against expected names, sizes, and
SHA-256 identities. Authentication establishes byte identity only.

Native artifact identity and correlated parsing
-------------------------------------------------

``Wannier90NativeArtifactSetParser`` parses the seven supported scientific text files
only from explicit named bytes: ``.nnkp``, ``.eig``, ``.amn``, ``.mmn``, ``.wout``,
``_u.mat``, and ``_hr.dat``. It checks common k-point, band, and Wannier dimensions.
Other supplied artifacts, including ``.win``, ``.chk``, standard output, and standard
error, may be authenticated without being interpreted.

.. currentmodule:: ksdft2effmass.integration.wannier90

.. autoclass:: Wannier90NativeArtifactIdentity
   :members:

.. autoclass:: Wannier90NativeArtifact
   :members:

.. autoclass:: Wannier90NativeArtifactCorrelationResult
   :members:

.. autoclass:: Wannier90NativeArtifactCorrelator
   :members:

.. autoclass:: Wannier90ParsedNativeArtifactSet
   :members:

.. autoclass:: Wannier90NativeArtifactSetParser
   :members:

Interface eigenvalues, projections, and neighbor overlaps
---------------------------------------------------------

``.nnkp``, ``.eig``, ``.amn``, and ``.mmn`` parsing preserves preprocessing
fractional reciprocal points and neighbor lists, complete indexed eigenvalue tables,
band-by-projection amplitudes, and ordered neighbor overlap records. Reciprocal shifts
remain explicit integer triples, and
native complex matrix entries retain their column-major interpretation.

The package also prepares deterministic ``.win``, ``.eig``, ``.amn``, and ``.mmn``
text from explicit typed records. Preparation checks common k-point, band, and Wannier
dimensions, compares the fixed-precision coordinates actually serialized into
``.win`` with parsed ``.nnkp`` fractional reciprocal points under an explicit absolute
coordinate tolerance, and requires exact ordered agreement
between every ``.mmn`` neighbor header and the parsed ``.nnkp`` record. It neither
constructs eigenvalues, projections, or overlaps nor performs file access, unit
conversion, or Wannier90
execution. Because ``.eig`` does not encode its energy unit, the preparation result
retains the caller-declared physical unit separately.

.. currentmodule:: ksdft2effmass.integration.wannier90

.. autoclass:: Wannier90NeighborListData
   :members:

.. autoclass:: Wannier90NeighborListParser
   :members:

.. autoclass:: Wannier90EigenvalueData
   :members:

.. autoclass:: Wannier90EigenvalueParser
   :members:

.. autoclass:: Wannier90ProjectionData
   :members:

.. autoclass:: Wannier90ProjectionParser
   :members:

.. autoclass:: Wannier90NeighborOverlapData
   :members:

.. autoclass:: Wannier90NeighborOverlapParser
   :members:

.. autoclass:: Wannier90InputData
   :members:

.. autoclass:: Wannier90InputFileWriter
   :members:

.. autoclass:: Wannier90EigenvalueFileWriter
   :members:

.. autoclass:: Wannier90ProjectionFileWriter
   :members:

.. autoclass:: Wannier90NeighborOverlapFileWriter
   :members:

.. autoclass:: Wannier90InterfacePreparationRequest
   :members:

.. autoclass:: Wannier90InterfacePreparationResult
   :members:

.. autoclass:: Wannier90InterfacePreparationWorkflow
   :members:

Native gauge matrices
---------------------

``_u.mat`` parsing preserves ordered fractional three-coordinate reciprocal points and
native column-major complex matrices. Rectangular matrices are retained, so parsing
does not imply unitarity or absence of disentanglement.

.. autoclass:: Wannier90UnitaryMatrixData
   :members:

.. autoclass:: Wannier90UnitaryMatrixParser
   :members:

Real-space Hamiltonian blocks
-----------------------------

``_hr.dat`` parsing preserves each integer three-coordinate representative and its
native Wigner--Seitz degeneracy alongside the energy-valued matrix block. No
interpolation or degeneracy convention is applied by the parser.

.. autoclass:: Wannier90HamiltonianBlockData
   :members:

.. autoclass:: Wannier90HamiltonianBlockParser
   :members:

Final localization observations
--------------------------------

``.wout`` parsing selects the last ``Final State`` section and retains all reported
centers, individual spreads, the four-part Omega decomposition, and the maximum
converged iteration. The caller declares the center length unit; spreads and Omega
values use its square.

.. autoclass:: Wannier90LocalizationData
   :members:

.. autoclass:: Wannier90LocalizationParser
   :members:
