"""
FK Spectrum computation class.

This module provides a class for computing F-K (frequency-wavenumber) spectra 
from 2D seismic data with configurable windowing and tapering options.
"""

import numpy as np
from scipy.signal.windows import tukey, hann
from scipy.fft import fft2, fftshift


class FKSpectrum:
    """
    Compute F-K (frequency-wavenumber) spectrum from 2D seismic data.
    
    This class handles temporal and spatial tapering, zero-padding, and FFT
    computation of the F-K spectrum.
    
    Attributes:
        dt (float): Temporal sampling interval (seconds)
        dx (float): Spatial sampling interval (meters)
        tw_type (str): Temporal window type ('tukey', 'hann', or 'none')
        tw_alpha (float): Temporal window parameter for Tukey taper (0-1)
        sw_type (str): Spatial window type ('tukey', 'hann', or 'none')
        sw_alpha (float): Spatial window parameter for Tukey taper (0-1)
    """
    
    def __init__(self, dt, dx, tw_type='tukey', tw_alpha=0.1, 
                 sw_type='tukey', sw_alpha=0.1):
        """
        Initialize FK spectrum processor.
        
        Parameters:
            dt (float): Temporal sampling interval (seconds)
            dx (float): Spatial sampling interval (meters)
            tw_type (str): Temporal window type. Options: 'tukey', 'hann', 'none'
                Default: 'tukey'
            tw_alpha (float): Temporal Tukey window parameter (0-1).
                Default: 0.1
            sw_type (str): Spatial window type. Options: 'tukey', 'hann', 'none'
                Default: 'tukey'
            sw_alpha (float): Spatial Tukey window parameter (0-1).
                Default: 0.1
        """
        self.dt = dt
        self.dx = dx
        self.tw_type = tw_type
        self.tw_alpha = tw_alpha
        self.sw_type = sw_type
        self.sw_alpha = sw_alpha
        
        # Storage for results
        self._fk_spectrum = None
        self._frequencies = None
        self._wavenumbers = None
        self._tapered_data = None
        self._window_2d = None
    
    def _create_temporal_window(self, nt):
        """
        Create temporal window.
        
        Parameters:
            nt (int): Number of temporal samples
            
        Returns:
            numpy.ndarray: Temporal window array
        """
        if self.tw_type == 'tukey':
            return tukey(nt, alpha=self.tw_alpha)
        elif self.tw_type == 'hann':
            return hann(nt)
        elif self.tw_type == 'none':
            return np.ones(nt)
        else:
            raise ValueError(f"Unknown temporal window type: {self.tw_type}")
    
    def _create_spatial_window(self, nx):
        """
        Create spatial window.
        
        Parameters:
            nx (int): Number of spatial samples
            
        Returns:
            numpy.ndarray: Spatial window array
        """
        if self.sw_type == 'tukey':
            return tukey(nx, alpha=self.sw_alpha)
        elif self.sw_type == 'hann':
            return hann(nx)
        elif self.sw_type == 'none':
            return np.ones(nx)
        else:
            raise ValueError(f"Unknown spatial window type: {self.sw_type}")
    
    def compute(self, shotgather):
        """
        Compute FK spectrum from 2D seismic data.
        
        Parameters:
            shotgather (numpy.ndarray): 2D array with shape (nt, nx)
                where nt is number of time samples and nx is number of spatial samples
                
        Returns:
            tuple: (FK_shifted, frequencies, wavenumbers, tapered_data, window_2d)
                - FK_shifted (numpy.ndarray): Shifted FFT result (magnitude)
                - frequencies (numpy.ndarray): Frequency array (Hz)
                - wavenumbers (numpy.ndarray): Wavenumber array (1/m)
                - tapered_data (numpy.ndarray): Tapered input data
                - window_2d (numpy.ndarray): 2D window applied
        """
        nt, nx = shotgather.shape
        
        # Create windows
        t_win = self._create_temporal_window(nt)
        x_win = self._create_spatial_window(nx)
        
        # Create 2D window via outer product
        win2d = np.outer(t_win, x_win)
        
        # Apply taper
        tapered = shotgather * win2d
        
        # Zero-pad to next power of 2 for improved resolution
        nt_padded = 2 ** int(np.ceil(np.log2(nt)))
        nx_padded = 2 ** int(np.ceil(np.log2(nx)))
        padded = np.zeros((nt_padded, nx_padded))
        padded[:nt, :nx] = tapered
        
        # Compute 2D FFT
        fk = np.fft.fft2(padded)
        fk_shifted = np.fft.fftshift(fk)
        
        # Compute frequency and wavenumber arrays
        f = np.fft.fftfreq(nt_padded, self.dt)
        f = np.fft.fftshift(f)
        
        k = np.fft.fftfreq(nx_padded, self.dx)
        k = np.fft.fftshift(k)
        
        # Store results
        self._fk_spectrum = fk_shifted
        self._frequencies = f
        self._wavenumbers = k
        self._tapered_data = tapered
        self._window_2d = win2d
        
        return fk_shifted, f, k, tapered, win2d
    
    def get_amplitude_spectrum(self):
        """
        Get amplitude spectrum (magnitude of FK spectrum).
        
        Returns:
            numpy.ndarray: Amplitude spectrum
            
        Raises:
            RuntimeError: If compute() has not been called yet
        """
        if self._fk_spectrum is None:
            raise RuntimeError("Compute FK spectrum first using compute() method")
        return np.abs(self._fk_spectrum)
    
    def get_power_spectrum(self):
        """
        Get power spectrum (magnitude squared of FK spectrum).
        
        Returns:
            numpy.ndarray: Power spectrum
            
        Raises:
            RuntimeError: If compute() has not been called yet
        """
        if self._fk_spectrum is None:
            raise RuntimeError("Compute FK spectrum first using compute() method")
        return np.abs(self._fk_spectrum) ** 2
    
    @property
    def frequencies(self):
        """Get frequency array from last computation."""
        return self._frequencies
    
    @property
    def wavenumbers(self):
        """Get wavenumber array from last computation."""
        return self._wavenumbers
    
    @property
    def tapered_data(self):
        """Get tapered data from last computation."""
        return self._tapered_data
    
    @property
    def window_2d(self):
        """Get 2D window from last computation."""
        return self._window_2d
    
    def filter_frequency_range(self, f_min, f_max):
        """
        Filter FK spectrum to a specific frequency range.
        
        Parameters:
            f_min (float): Minimum frequency (Hz)
            f_max (float): Maximum frequency (Hz)
            
        Returns:
            tuple: (fk_filtered, f_filtered, k)
                - fk_filtered (numpy.ndarray): Filtered FK spectrum
                - f_filtered (numpy.ndarray): Filtered frequency array
                - k (numpy.ndarray): Original wavenumber array
                
        Raises:
            RuntimeError: If compute() has not been called yet
        """
        if self._fk_spectrum is None:
            raise RuntimeError("Compute FK spectrum first using compute() method")
        
        f_idx = np.where((self._frequencies >= f_min) & 
                         (self._frequencies <= f_max))[0]
        fk_filtered = self._fk_spectrum[f_idx, :]
        f_filtered = self._frequencies[f_idx]
        
        return fk_filtered, f_filtered, self._wavenumbers
