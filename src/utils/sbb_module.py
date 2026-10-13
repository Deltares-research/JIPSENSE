
# Databricks notebook source
import obspy
import numpy as np
from obspy import Trace, Stream, UTCDateTime
import os
import glob
import math
from scipy.fft import fft2, fftshift
from scipy import signal
import TDMS_Read as tdms_

def Array_to_ObsPy(data, fs):
    """
    DESCRIPTION:
    -----------------------
    Function for indexing traces into an Obspy object. This enables the possibility of using the Obspy processing features.
    
    INPUT PARAMETERS:
    -----------------------
    data  : 2d array coontaning a N number of traces
    fs    : sampling frequency in Hz
    
    RETURNS:
    -----------------------
    st  : Obspy object containing N number traces and sampling frequency
    """

    size = np.shape(data)                        # Determining number of samples and traces in data
    st = Stream()                                # Creating a list of multiple obspy traces objects
    for ii in range(0, size[1]):                 # Loop to assign input traces inside st object
        trace = Trace(header={'station': 'DAS', 'channel': 'Z' + str(ii)})
        trace.data = data[:, ii]
        year = 2022                                                                                # year -- Defaul value
        month = 1                                                                                  # month -- Defaul value
        day = 1                                                                                    # day -- Defaul value
        hours = 12                                                                                 # hours -- Defaul value
        minutes = 0                                                                                # minutes -- Defaul value
        seconds = 0                                                                                # seconds -- Defaul value
        trace.stats.starttime = UTCDateTime(year, month, day, hours, minutes, seconds)     # Assign defaults values for date and time attributes
        trace.stats.npts = len(trace.data)                                                         # Assign number of samples per trace
        trace.stats.sampling_rate = fs                                                             # Assign sampling frequency in Hz
        trace.stats.station = str(ii)                                                              # Assign default station number 
        trace.stats.channel = 'Z' + str(ii)                                                        # Assign channel number
        trace.stats.distance = ii                                                                  # Assign default distance
        trace.stats.network = 'DAS'                                                                # Assign default network name

        st.append(trace)                                                                           #  Create multi-trace Obspy object

    return (st)


def Obspy_to_Array(st):
    """
    DESCRIPTION:
    -----------------------
    Function for extracting signals (processed) from the Obspy object.
    
    
    INPUT PARAMETERS:
    -----------------------
    st  : Obspy object containing N number traces and sampling frequency

    RETURNS:
    -----------------------
    Array  : 2d-numpy array contaning a N number of traces 
    """

    size = np.shape(st)                      # Defining the array dimenions in the st object
    Array = np.zeros((size[1], size[0]))     # Declaring the 2d array 

    for ii in range(0, size[0]):             # Loop for assigning trace values inside Array
        Array[:, ii] = st[ii].data

    return Array




def agc_gain(data,fs,agc_gate, method='rms'):
    '''
    Applying AGC gain to seismic data. Fast way to find trends in the F-K domain
    However, it is not true amplitude correction, so the input gives not valid
    results when using for AVO analysis or inversion.
    
    TODO: improve readability by renaming of variables and adding annotation
    
    Parameters
    ----------
    data : 2D array of floats
        seismic data input with samples in rows and traces in columns (use data.transpose() if required)
    fs : int
        sampling frequency in Hz, this is equal to 1/sampling interval (dt) in seconds
    agc_gate : float
        length of window in seconds to use for the AGC gain correction
    method : string, optional
        Normalization method for AGC correction. The default is 'rms'.

    Returns
    -------
    data_agc : 2D array of floats
        seismic data that has AGC gain applied. 

    '''


    nt,nx = np.shape(data)
    
    samples_agc = (agc_gate*fs) + 1
    samples_agc = np.floor(samples_agc/2)
    
    h = signal.windows.triang(2*samples_agc+1)
    
    data_agc = np.zeros((np.shape(data)))
    
    for k in range(nx):
        
        aux = data[:,k]
        e = pow(aux,2)
        rms = np.sqrt(np.convolve(e,h,mode='same'))
        epsi = 1.e-10*max(rms)
        op = rms/(pow(rms,2)+epsi)
        data_agc[:,k] = data[:,k]*op
    
    if method=='amplitude':                # Normalize by amplitude
    
        for k in range(0,nx):
            aux =  data_agc[:,k]
            amax = np.max(np.abs(aux))
            data_agc[:,k] = data_agc[:,k]/amax
    
    elif method=='rms':                # Normalize by rms
        
        for k in range(0,nx):
            aux =  data_agc[:,k]
            amax =  np.sqrt(np.sum(pow(aux,2))/nt)
            data_agc[:,k] = data_agc[:,k]/amax
    
    else:
        
        print("please specify method as 'rms'(default) or 'amplitude'")

    return data_agc 



def filtering(data,fs,fmin,fmax,filter_type='bandpass'):
    """
    DESCRIPTION:
    -----------------------
    Function for filtering raw signals. For this we use a Butterworth filter type of order 4 and zero-phase.
    
    INPUT PARAMETERS:
    -----------------------
    data  : 2d-numpy array contaning traces. 
    fs    : Sampling frequency in Hz.
    fmin  : Minimum frequency in Hz.
    fmax  : Maxmimum frequency in Hz.
    filter_type = "bandpass","lowpass", and "highpass". For highpass filter, the corner frequency, freq, is set to fmin, so all frequencies bellow fmin are removed and fmax is not used, while
    for lowpass filter, the corner frequency, freq, is set to fmax, so all frequencies above fmax are removed and fmin is not used. We use filter_type="bandpass" as Default.
    
    RETURNS:
    -----------------------
    filt_data  : 2d-numpy array contaning band-pass filtered traces 
    """
    st2filt = Array_to_ObsPy(data, fs)                                                 # Converting data into an Obspy object
    st_f = st2filt.copy()                 
    st_f.detrend('constant')                                                           # Signal detrend
    st_f.taper(0.01, type='cosine')                                                    # Cosine taper of 1%
    # Implemente filtering based on filtering type selection.
    if filter_type=="bandpass":
        st_f.filter(filter_type, freqmin=fmin, freqmax=fmax, corners=4, zerophase=True)      # Band-pass filter of butterworth type, order 4 and zero-phase
    elif filter_type=="lowpass":
        st_f.filter(filter_type, freq=fmax, corners=4, zerophase=True)                       # Low-pass filter of butterworth type, order 4 and zero-phase
    elif filter_type=="highpass":
        st_f.filter(filter_type, freq=fmin, corners=4, zerophase=True)                       # High-pass filter of butterworth type, order 4 and zero-phase
    else:
         print("please, select a proper filter type e.g. bandpass,lowpass or highpass")
        
    filt_data = Obspy_to_Array(st_f)                                                          # Extracting filtered traces

    return filt_data


def fk_spectrum(data,fs,dx,pad_t=2,pad_x=2):
    '''
    Calculates the 2D Fourier transform, for seismic data this results in
    the data being transformed into the F-K domain. Zero-padding of the input 
    data is performed for both axis before the transform is applied.
    
    Parameters
    ----------
    pad_t : int, optional
        Time axis zero-padding factor. The default is 2.
    pad_x : in, optional
        Spatial (trace) axis zero-adding factor. The default is 2.

    Returns
    -------
    data_fk : 2D Array of floats
        2D fourier transformed data (F-K domain)
    f : 1D Array of floats
        Frequency axis vecor belonging to data_fk
    kx : 1D Array of floats
        Wavenumber axis vecor belonging to data_fk
    '''
    
    nt,nx = np.shape(data)
    
    nt_fft = pad_t*nt #padding for time axis
    nx_fft = pad_x*nx #padding for trace axis
    
    
    fk_full = fft2(data, s=(nt_fft, nx_fft))/len(data)  
    
    fk_shift = fftshift((np.abs(fk_full)))
    data_fk = fk_shift[int(len(fk_full)/2):-1,:]
    
    f=np.linspace(-0.5,0.5,2*fk_full.shape[0])*fs
    kx=np.linspace(-0.5,0.5,2*fk_full.shape[1])/dx
    
    
    return data_fk, f, kx


def loadTDMS(file_path,params):
    """
    DESCRIPTION:        
    ----------------------- 
    Function for loading TDMS files. This function uses the TDMS_Read.py script to read the TDMS files.
    
    INPUT PARAMETERS:
    -----------------------
    file_path  : Path to the TDMS file.
    params     : Dictionary containing the following keys:
        first_channel     : First channel to be read.
        last_channel      : Last channel to be read.
        first_time_sample : First time sample to be read.
        last_time_sample  : Last time sample to be read.

    RETURNS:
    -----------------------
    tdms  : TDMS object containing the loaded data.
    """

    tdms = tdms_.TdmsReader(file_path)

    props = tdms.get_properties()

    zero_offset = props.get('Zero Offset (m)') 
    channel_spacing = props.get('SpatialResolution[m]') * props.get('Fibre Length Multiplier')
    n_channels = tdms.fileinfo['n_channels']
    depth = zero_offset + np.arange(n_channels) * channel_spacing
    fs = props.get('SamplingFrequency[Hz]')
    

    first_channel = params['first_channel']
    last_channel = params['last_channel']
    first_time_sample = params['first_time_sample']
    last_time_sample = params['last_time_sample']
    
    data = tdms.get_data(first_channel, last_channel, first_time_sample, last_time_sample)

    print('Number of channels in file: {0}'.format(n_channels))

    # print selected dimensions and indices
    print('Number of channels selected: {0}'.format(data.shape[1]))
    print('First channel selected: {0}'.format(first_channel))
    print('Last channel selected: {0}'.format(last_channel))
    print('Time samples in file: {0}'.format(tdms.channel_length))
    print('Sampling frequency (Hz): {0}'.format(fs))

    
    return data, props
