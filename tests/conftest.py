"""Top-level pytest configuration for the SciComp test tree.

Importing the ``Python`` package triggers a banner print in
``Python/init_berkeley.py`` (``print_berkeley_banner``) at import time. Under
pytest's captured-output context that side effect can abort the import, which
breaks collection of any test module that imports the real package directly
(for example ``tests/test_signal_processing.py``).

Setting ``BERKELEY_SCICOMP_QUIET`` before collection suppresses the banner so
the documented ``pytest`` invocation collects the whole tree. This is a
collection-time guard only; it does not change any numerical behavior.
"""
import os

# Must run before any test module imports the ``Python`` package.
os.environ.setdefault("BERKELEY_SCICOMP_QUIET", "1")
