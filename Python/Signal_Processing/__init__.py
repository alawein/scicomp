"""
Signal Processing Module
=======================
Comprehensive signal processing toolkit for scientific computing applications.
Modules:
    signal_analysis: Core signal processing operations
    spectral_analysis: Advanced spectral and time-frequency analysis
Author: Meshal Alawein
Date: 2024
"""
from .signal_analysis import (
    SignalProcessor,
    AdaptiveFilter,
    demo_signal_processing
)
from .spectral_analysis import (
    SpectralAnalyzer,
    demo_spectral_analysis
)
__all__ = [
    # Core signal processing
    'SignalProcessor',
    'AdaptiveFilter',
    # Spectral analysis
    'SpectralAnalyzer',
    # Demos
    'demo_signal_processing',
    'demo_spectral_analysis'
]
# Module metadata
__version__ = '1.0.0'
__author__ = 'Meshal Alawein'
__email__ = 'contact@meshal.ai'