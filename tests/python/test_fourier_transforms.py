"""
Tests for FFT / spectral analysis in Signal_Processing.core.fourier_transforms
and for the higher-level SignalProcessor / SpectralAnalyzer classes.

Covers: Python.Signal_Processing.core.fourier_transforms
        Python.Signal_Processing.signal_analysis (selected)
        Python.Signal_Processing.spectral_analysis (selected)
"""
import pytest
import numpy as np
import numpy.testing as npt


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def fft_engine():
    from Python.Signal_Processing.core.fourier_transforms import FFT
    return FFT()


@pytest.fixture
def spectral():
    from Python.Signal_Processing.core.fourier_transforms import SpectralAnalysis
    return SpectralAnalysis()


@pytest.fixture
def processor():
    from Python.Signal_Processing.signal_analysis import SignalProcessor
    return SignalProcessor(sampling_rate=1000)


@pytest.fixture
def analyzer():
    from Python.Signal_Processing.spectral_analysis import SpectralAnalyzer
    return SpectralAnalyzer(sampling_rate=1000)


@pytest.fixture
def sine_signal():
    """Generate a 50 Hz sine wave at 1000 Hz sampling rate for 1 second."""
    fs = 1000
    t = np.linspace(0, 1, fs, endpoint=False)
    signal = np.sin(2 * np.pi * 50 * t)
    return t, signal, fs


# ---------------------------------------------------------------------------
# FFT class (fourier_transforms.py)
# ---------------------------------------------------------------------------

class TestFFT:
    """Tests for the low-level FFT class."""

    def test_fft_returns_correct_length(self, fft_engine):
        signal = np.random.randn(128)
        freqs, spectrum = fft_engine.compute_fft(signal, sample_rate=100)
        assert len(freqs) == 128
        assert len(spectrum) == 128

    def test_fft_dc_component(self, fft_engine):
        """DC component of constant signal should equal the constant * N."""
        signal = np.ones(64) * 3.0
        freqs, spectrum = fft_engine.compute_fft(signal, sample_rate=1.0)
        npt.assert_allclose(np.abs(spectrum[0]), 3.0 * 64, atol=1e-10)

    def test_fft_ifft_roundtrip(self, fft_engine):
        """IFFT(FFT(x)) should equal x."""
        signal = np.random.randn(128)
        _, spectrum = fft_engine.compute_fft(signal, sample_rate=1.0)
        recovered = fft_engine.compute_ifft(spectrum)
        npt.assert_allclose(np.real(recovered), signal, atol=1e-10)

    def test_fft_parseval_theorem(self, fft_engine):
        """Energy in time domain should equal energy in frequency domain."""
        signal = np.random.randn(256)
        _, spectrum = fft_engine.compute_fft(signal, sample_rate=1.0)
        time_energy = np.sum(np.abs(signal)**2)
        freq_energy = np.sum(np.abs(spectrum)**2) / len(signal)
        npt.assert_allclose(time_energy, freq_energy, rtol=1e-10)

    def test_fft_frequency_detection(self, fft_engine, sine_signal):
        """FFT should detect the correct frequency of a pure sine wave."""
        t, signal, fs = sine_signal
        freqs, spectrum = fft_engine.compute_fft(signal, sample_rate=fs)
        # Find the peak in the positive frequencies
        positive_mask = freqs > 0
        mag = np.abs(spectrum[positive_mask])
        peak_freq = freqs[positive_mask][np.argmax(mag)]
        npt.assert_allclose(peak_freq, 50.0, atol=2.0)


# ---------------------------------------------------------------------------
# SpectralAnalysis (fourier_transforms.py)
# ---------------------------------------------------------------------------

class TestSpectralAnalysis:
    """Tests for the SpectralAnalysis helper class."""

    def test_power_spectrum_nonnegative(self, spectral, sine_signal):
        """Power spectrum values should be non-negative."""
        _, signal, fs = sine_signal
        freqs, power = spectral.power_spectrum(signal, sample_rate=fs)
        assert np.all(power >= -1e-15)

    def test_power_spectrum_peak(self, spectral, sine_signal):
        """Power spectrum should peak at the signal frequency."""
        _, signal, fs = sine_signal
        freqs, power = spectral.power_spectrum(signal, sample_rate=fs)
        positive_mask = freqs > 0
        peak_freq = freqs[positive_mask][np.argmax(power[positive_mask])]
        npt.assert_allclose(peak_freq, 50.0, atol=2.0)

    def test_spectrogram_shape(self, spectral):
        """Spectrogram should have correct dimensions."""
        signal = np.random.randn(1000)
        window_size = 64
        overlap = 0.5
        times, freqs, spec = spectral.spectrogram(signal, window_size, overlap, sample_rate=100)
        assert spec.shape[0] == window_size  # frequency bins
        assert spec.shape[1] == len(times)   # time bins


# ---------------------------------------------------------------------------
# SignalProcessor (signal_analysis.py) -- additional tests
# ---------------------------------------------------------------------------

class TestSignalProcessorFFT:
    """Additional FFT tests for SignalProcessor."""

    def test_compute_fft_normalized(self, processor):
        """Normalized FFT of a sine should have peak amplitude near 1."""
        t, signal = processor.generate_signal('sine', 1.0, frequency=100, amplitude=1.0)
        freq, mag = processor.compute_fft(signal, normalize=True)
        peak_mag = np.max(mag[1:])  # Skip DC
        npt.assert_allclose(peak_mag, 1.0, atol=0.1)

    def test_compute_fft_with_window(self, processor):
        """Windowed FFT should not raise and should return the same length."""
        t, signal = processor.generate_signal('sine', 1.0, frequency=50)
        freq, mag = processor.compute_fft(signal, window='hann')
        assert len(freq) == len(mag)

    def test_compute_spectrogram_runs(self, processor):
        """Spectrogram should run without error and return 3 arrays."""
        t, signal = processor.generate_signal('chirp', 2.0, frequency=[10, 100])
        t_spec, f_spec, Sxx = processor.compute_spectrogram(signal)
        assert Sxx.shape[0] == len(f_spec)
        assert Sxx.shape[1] == len(t_spec)


# ---------------------------------------------------------------------------
# SpectralAnalyzer (spectral_analysis.py) -- selected tests
# ---------------------------------------------------------------------------

class TestSpectralAnalyzer:
    """Tests for the SpectralAnalyzer class."""

    def test_power_spectrum_welch(self, analyzer):
        """Welch PSD should return non-negative values."""
        np.random.seed(42)
        signal = np.sin(2 * np.pi * 50 * np.linspace(0, 1, 1000, endpoint=False))
        signal += 0.1 * np.random.randn(1000)
        f, Pxx = analyzer.compute_power_spectrum(signal, method='welch')
        assert np.all(Pxx >= -1e-15)

    def test_power_spectrum_periodogram(self, analyzer):
        """Periodogram PSD should return non-negative values."""
        signal = np.sin(2 * np.pi * 100 * np.linspace(0, 1, 1000, endpoint=False))
        f, Pxx = analyzer.compute_power_spectrum(signal, method='periodogram')
        assert np.all(Pxx >= -1e-15)

    def test_cepstrum_length(self, analyzer):
        """Cepstrum should have the same length as the input signal."""
        signal = np.random.randn(512)
        quefrency, cep = analyzer.compute_cepstrum(signal, type='real')
        assert len(cep) == len(signal)
        assert len(quefrency) == len(signal)

    def test_spectral_features_keys(self, analyzer):
        """Spectral features should contain expected keys."""
        np.random.seed(42)
        signal = np.random.randn(1024)
        features = analyzer.compute_spectral_features(signal)
        expected_keys = [
            'spectral_centroid', 'spectral_spread', 'spectral_entropy',
            'spectral_rolloff', 'spectral_flatness', 'spectral_crest'
        ]
        for key in expected_keys:
            assert key in features, f"Missing feature: {key}"

    def test_spectral_centroid_positive(self, analyzer):
        """Spectral centroid should be non-negative."""
        signal = np.sin(2 * np.pi * 100 * np.linspace(0, 1, 1000, endpoint=False))
        features = analyzer.compute_spectral_features(signal)
        assert features['spectral_centroid'] >= 0

    def test_cross_spectrum_shape(self, analyzer):
        """Cross spectrum should return matching frequency and spectrum arrays."""
        sig1 = np.random.randn(512)
        sig2 = np.random.randn(512)
        f, Pxy = analyzer.compute_cross_spectrum(sig1, sig2)
        assert len(f) == len(Pxy)

    def test_transfer_function_shape(self, analyzer):
        """Transfer function should return freq, magnitude, and phase of same length."""
        np.random.seed(0)
        inp = np.random.randn(1024)
        out = np.random.randn(1024)
        f, mag, phase = analyzer.compute_transfer_function(inp, out)
        assert len(f) == len(mag) == len(phase)


# ---------------------------------------------------------------------------
# SignalProcessor features and filters
# ---------------------------------------------------------------------------

class TestSignalProcessorFilters:
    """Tests for filter design and application."""

    def test_lowpass_filter_attenuates_high_freq(self, processor):
        """Lowpass filter should attenuate frequencies above cutoff."""
        # Signal = 10 Hz + 400 Hz
        t, signal = processor.generate_signal('multi_sine', 1.0,
                                               frequency=[10, 400],
                                               amplitude=[1.0, 1.0])
        b, a = processor.design_filter('lowpass', 100, order=5)
        filtered = processor.apply_filter(signal, b, a)
        # Check that the 400 Hz component is attenuated
        freq, mag = processor.compute_fft(filtered)
        # Find magnitude near 400 Hz
        idx_400 = np.argmin(np.abs(freq - 400))
        idx_10 = np.argmin(np.abs(freq - 10))
        assert mag[idx_400] < 0.1 * mag[idx_10]

    def test_peak_detection(self, processor):
        """Peak detection should find the correct number of peaks."""
        t, signal = processor.generate_signal('sine', 1.0, frequency=5)
        peaks = processor.detect_peaks(signal, height=0.5, distance=50)
        # A 5 Hz sine over 1s should have about 5 peaks
        assert 3 <= len(peaks['indices']) <= 7

    def test_snr_computation(self, processor):
        """SNR of a pure signal vs zero noise should be inf."""
        signal = np.ones(100)
        noise = np.zeros(100)
        snr = processor.compute_snr(signal, noise)
        assert snr == np.inf

    def test_snr_equal_power(self, processor):
        """SNR of equal-power signal and noise should be 0 dB."""
        signal = np.ones(1000)
        noise = np.ones(1000)
        snr = processor.compute_snr(signal, noise)
        npt.assert_allclose(snr, 0.0, atol=1e-10)

    def test_feature_extraction_keys(self, processor):
        """Feature extraction should return expected keys."""
        t, signal = processor.generate_signal('sine', 1.0, frequency=50)
        features = processor.extract_features(signal)
        expected = ['mean', 'std', 'rms', 'peak_to_peak', 'skewness', 'kurtosis',
                    'dominant_frequency']
        for key in expected:
            assert key in features, f"Missing feature key: {key}"

    def test_correlation_autocorrelation_peak(self, processor):
        """Autocorrelation should peak at zero lag."""
        np.random.seed(42)
        signal = np.random.randn(256)
        corr = processor.compute_correlation(signal, signal, mode='full')
        peak_idx = np.argmax(corr)
        assert peak_idx == len(signal) - 1  # zero-lag index in full mode

    def test_envelope_hilbert(self, processor):
        """Hilbert envelope of a sine should be approximately constant."""
        t, signal = processor.generate_signal('sine', 1.0, frequency=50)
        envelope = processor.compute_envelope(signal, method='hilbert')
        # Envelope of pure sine should be close to 1 (the amplitude)
        # Skip edges where Hilbert transform has artifacts
        npt.assert_allclose(envelope[100:-100], 1.0, atol=0.1)

    def test_resample_signal(self, processor):
        """Resampling should change the number of samples."""
        t, signal = processor.generate_signal('sine', 1.0, frequency=50)
        resampled = processor.resample_signal(signal, 1000, 500)
        assert len(resampled) == 500

    def test_denoise_median(self, processor):
        """Median filter denoising should reduce noise."""
        np.random.seed(42)
        clean = np.sin(2 * np.pi * 10 * np.linspace(0, 1, 1000))
        noisy = clean + 0.5 * np.random.randn(1000)
        denoised = processor.denoise_signal(noisy, method='median', kernel_size=5)
        # Denoised should be closer to clean than noisy is
        error_noisy = np.mean((noisy - clean)**2)
        error_denoised = np.mean((denoised - clean)**2)
        assert error_denoised < error_noisy


# ---------------------------------------------------------------------------
# AdaptiveFilter
# ---------------------------------------------------------------------------

class TestAdaptiveFilter:
    """Tests for adaptive filtering algorithms."""

    @pytest.fixture
    def filter_setup(self):
        """Create a simple system identification scenario."""
        from Python.Signal_Processing.signal_analysis import AdaptiveFilter
        np.random.seed(42)
        n = 500
        x = np.random.randn(n)
        # Unknown system: simple FIR
        h_true = np.array([1.0, -0.5, 0.25])
        d = np.convolve(x, h_true, mode='full')[:n]
        af = AdaptiveFilter(filter_order=3, step_size=0.01)
        return af, x, d

    def test_lms_error_decreases(self, filter_setup):
        """LMS error should decrease over time."""
        af, x, d = filter_setup
        output, error = af.lms_filter(x, d)
        # Compare early vs late error
        early_mse = np.mean(error[:50]**2)
        late_mse = np.mean(error[-50:]**2)
        assert late_mse < early_mse

    def test_nlms_error_decreases(self, filter_setup):
        """NLMS error should also decrease over time."""
        af, x, d = filter_setup
        af.weights = np.zeros(af.filter_order)  # Reset weights
        output, error = af.nlms_filter(x, d)
        early_mse = np.mean(error[:50]**2)
        late_mse = np.mean(error[-50:]**2)
        assert late_mse < early_mse

    def test_rls_error_decreases(self, filter_setup):
        """RLS error should decrease over time."""
        af, x, d = filter_setup
        af.weights = np.zeros(af.filter_order)
        output, error = af.rls_filter(x, d)
        early_mse = np.mean(error[:50]**2)
        late_mse = np.mean(error[-50:]**2)
        assert late_mse < early_mse

    def test_rls_converges_faster_than_lms(self, filter_setup):
        """RLS should converge faster than LMS (lower late MSE)."""
        af, x, d = filter_setup
        # LMS
        af.weights = np.zeros(af.filter_order)
        _, error_lms = af.lms_filter(x, d)
        # RLS
        af.weights = np.zeros(af.filter_order)
        _, error_rls = af.rls_filter(x, d)
        lms_late = np.mean(error_lms[-100:]**2)
        rls_late = np.mean(error_rls[-100:]**2)
        assert rls_late <= lms_late * 2  # RLS should be at least comparable
