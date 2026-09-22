Native toolchains
=================

``ksdft2effmass.toolchains`` owns execution-free native-toolchain declarations and
deterministic build planning. It represents exact declared tool roles, versions,
paths, pinned-or-explicitly-unpinned content evidence, CMake definitions, disjoint
source, scratch, and installation roots, expected outputs, and operational ceilings.

:class:`~ksdft2effmass.toolchains.NativeToolchainFingerprinter` hashes the
canonical runtime dependency declaration. It excludes absolute roots, logical labels,
and build-system tools. :class:`~ksdft2effmass.toolchains.NativeBuildFingerprinter`
separately hashes that complete runtime digest together with build-system provenance,
the source reference, platform, CMake definitions, target, and outputs. Neither hashes local files.

Both fingerprints retain complete SHA-256 values and can render filesystem identities
with 12 through 64 hexadecimal characters. This permits a future manifest-aware
installer to lengthen an identity after detecting a short-prefix collision.
:class:`~ksdft2effmass.toolchains.NativeBuildPlanner` emits the proposed manifest path
and direct configuration and build argument vectors without shell syntax. A plan
establishes represented software consistency only; it does not prove that tools or
source bytes exist, verify an installation, authorize protected execution, or
establish numerical or scientific validity.

The first consumer is
:class:`~ksdft2effmass.simulations.quantumespresso.QuantumEspressoOpenBlasComparatorBuildPlanner`.
Its caller supplies separate absolute roots corresponding to ``~/opt`` and
``~/build``. Independent packages use flat HPC-style prefixes:

.. code-block:: text

   ~/opt/software/cmake/4.3.3-<platform>/
   ~/opt/software/gcc/16.1.0-<platform>/
   ~/opt/software/openmpi/5.0.9-gcc16.1.0-<platform>/
   ~/opt/software/openblas/0.3.33-gcc16.1.0-<platform>/
   ~/opt/software/fftw/3.3.11-gcc16.1.0-<platform>/
   ~/opt/toolchains/tc-<digest-prefix>/manifest.json
   ~/opt/software/qe/7.2/tc-<digest-prefix>/release-nontrapping/
     build-<digest-prefix>/
   ~/opt/modules/qe/7.2/release-nontrapping/
     tc-<digest-prefix>-build-<digest-prefix>.lua
   ~/build/qe/7.2/tc-<digest-prefix>/build-<digest-prefix>/<workspace>/

The ``tc-`` identity represents runtime compatibility; ``build-`` represents the
artifact-producing recipe. Modulefiles are non-authoritative views. The implementation
never expands ``~`` and performs no discovery, local-file hashing, installation,
network access, workspace creation, compilation, or executable invocation.

Planning contracts
------------------

.. automodule:: ksdft2effmass.toolchains
   :members:
   :imported-members:
