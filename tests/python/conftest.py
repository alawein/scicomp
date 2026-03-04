"""
Shared test configuration for SciComp Python tests.

Registers lightweight stub packages for the ``Python`` namespace so that
individual source modules can be imported without triggering the heavyweight
top-level ``Python/__init__.py`` (which pulls in visualisation code that
may be incompatible with the installed matplotlib version).
"""
import importlib
import os
import sys
import types

_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Ensure project root is on sys.path
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


def _ensure_stub_packages():
    """Pre-register stub packages so sub-module imports bypass __init__.py."""
    stubs = [
        ('Python', 'Python'),
        ('Python.Control', 'Python/Control'),
        ('Python.Control.core', 'Python/Control/core'),
        ('Python.Crystallography', 'Python/Crystallography'),
        ('Python.Crystallography.core', 'Python/Crystallography/core'),
        ('Python.FEM', 'Python/FEM'),
        ('Python.FEM.core', 'Python/FEM/core'),
        ('Python.FEM.utils', 'Python/FEM/utils'),
    ]
    for pkg_name, rel_path in stubs:
        if pkg_name not in sys.modules:
            m = types.ModuleType(pkg_name)
            m.__path__ = [os.path.join(_PROJECT_ROOT, rel_path.replace('/', os.sep))]
            m.__package__ = pkg_name
            sys.modules[pkg_name] = m


_ensure_stub_packages()

# numpy 2.0+ removed np.trapz — alias to np.trapezoid for backwards compat
import numpy as np
if not hasattr(np, 'trapz'):
    np.trapz = np.trapezoid
