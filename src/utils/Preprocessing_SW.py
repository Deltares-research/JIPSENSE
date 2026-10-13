# Databricks notebook source
import os
import glob
import numpy as np
import matplotlib.pylab as plt
import matplotlib
from obspy.signal.cross_correlation import correlate, xcorr_max
import h5py
from obspy import Trace, Stream, UTCDateTime
import scipy.signal as sp
from datetime import datetime
from obspy.core.util import AttribDict
from obspy.io.sac.sactrace import SACTrace
from scipy.signal import hilbert
from scipy.signal import  iirfilter
from scipy.signal.windows import tukey  
from scipy.signal import sosfilt
from scipy.signal import zpk2sos
import numpy as np
from scipy import signal
from scipy.fftpack import fft,ifft,next_fast_len


def Convert_3d_to_2d_array(data_3D):
    """
    DESCRIPTION:
    -----------------------
    Basic function for converting 3D numpy array into a 2D array.
    
    INPUT PARAMETERS:
    -----------------------
    data_3D: a 3d numpy array containing time domain signals
    
    RETURNS:
    -----------------------
    data_2D a 2d array  
    """
    data_2D = data_3D.transpose(2, 0, 1).reshape(-1, data_3D.shape[1])
    return data_2D


def raw2strain(trace, n, L):
    """
    DESCRIPTION:
    -----------------------
    Function for converting raw DAS data into strain data after applying all OptaSense parameters. 
    This function is written based on: https://github.com/ethanfwilliams/OOI_RCA_DAS_notebook/blob/main/OOI_RCA_OptaSense_DAS_intro.ipynb. 
    
    INPUT PARAMETERS:
    -----------------------
    trace: 1d array coontaning a single trace (time domain)
    n    : index of refraction typically assigned as 1.46
    L    : Gauge lengt in meters
    
    RETURNS:
    -----------------------
    trace_strain  : 1d array containing a strain values 
    
    """
    # Remove the mean from the trace
    trace = trace.astype(float)                    
    trace -= np.mean(trace)
    # Convert to units of radians
    trace *= (2 * np.pi) / 2 ** 16  
    # Convert to units of strain
    trace *= (1550.12 * 1e-9) / (0.78 * 4 * np.pi * n * L)   
    trace_strain = trace
    return trace_strain


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

    
    # Loop to assign input traces inside st object
    for ii in range(0, size[1]):                 
        
        trace = Trace(header={'station': 'DAS', 'channel': 'Z' + str(ii)})
        trace.data = data[:, ii]
        year = 2022                               # year -- Default value
        month = 1                                 # month -- Default value
        day = 1                                   # day -- Default value
        hours = 12                                # hours -- Default value
        minutes = 0                               # minutes -- Default value
        seconds = 0                               # seconds -- Default value
    
        # Assign defaults values for date and time attributes
        trace.stats.starttime = UTCDateTime(year, month, day, hours, minutes, seconds)     
        trace.stats.npts = len(trace.data)        # Assign number of samples per trace
        trace.stats.sampling_rate = fs            # Assign sampling frequency in Hz
        trace.stats.station = str(ii)             # Assign default station number 
        trace.stats.channel = 'Z' + str(ii)       # Assign channel number
        trace.stats.distance = ii                 # Assign default distance
        trace.stats.network = 'DAS'               # Assign default network name

        #  Create multi-trace Obspy object
        st.append(trace)                          

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
    size = np.shape(st)                           # Defining the array dimenions in the st object
    Array = np.zeros((size[1], size[0]))          # Declaring the 2d array 
    # Loop for assigning trace values inside Array
    for ii in range(0, size[0]):                
        Array[:, ii] = st[ii].data

    return Array
    
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
    
    
def OptaSense_Props(fp):
    """
    DESCRIPTION:
    -----------------------
    Function for inspecting main properties of the OptaSense DAS data. This function is written based on:    
    https://github.com/ethanfwilliams/OOI_RCA_DAS_notebook/blob/main/OOI_RCA_OptaSense_DAS_intro.ipynb. 

    INPUT PARAMETERS:
    -----------------------
    fp  : list with all file properties 

    RETURNS:
    -----------------------
    dt : sampling interval of the DAS data in seconds
    fs : sampling frequency of the DAS data in Hz
    dx : channel spacing in meters
    nx : number of channels
    ns : number of samples
    """
    # Print DAS acqusition parameters
    print('\nThe gauge length is ',fp['Acquisition'].attrs['GaugeLength'],'m.')                              # Print gauge lengt in meters.                          
    print('The pulse rate is ',fp['Acquisition'].attrs['PulseRate'],'Hz.')                                   # Print pulse rate in Hz
    print('The spatial sampling interval is ',fp['Acquisition'].attrs['SpatialSamplingInterval'],'m.')       # Print spatial sampling interval
    
    # Print date/time
    rawDataTime = fp['Acquisition']['Raw[0]']['RawDataTime']                                                 # Print the first entry in "RawDataTime"
    print('The first value in \"RawDataTime\" is',rawDataTime[0],\
    'which is the timestamp of the first sample in microseconds.')
    print('This equates to the date and time',datetime.utcfromtimestamp(rawDataTime[0]*1e-6))                # Print UTC timestamp
    rawDataTimeArr = rawDataTime[:]                                                                          # We can load the full contents of "RawDataTime" into a NumPy array
    print('\nThere are',len(rawDataTimeArr),'values in \"RawDataTime\"')                                     # Print the length of the array
    dt = (rawDataTime[1]-rawDataTime[0]) * 1e-6                                                              # Get the sample interval either from the time stamps
    fs = fp['Acquisition']['Raw[0]'].attrs['OutputDataRate']                                                 # Get sampling frequency, fs
    dx = fp['Acquisition'].attrs['SpatialSamplingInterval']                                                  # Get channel spacing in m
    nx = fp['Acquisition']['Raw[0]'].attrs['NumberOfLoci']                                                   # Get number of channels
    ns = fp['Acquisition']['Raw[0]']['RawDataTime'].attrs['Count']                                           # Get number of samples
    print('The sampling frequency is',fs,'Hz.')                                                              # Print the sampling frequency in Hz                    
    print('Number of channels is',nx)                                                                        # Print the number of traces

    return (dt, fs, dx, nx, ns)

def all_strain(fp, channel0, channel1, fmin, fmax,filter_type='bandpass'):
    """
    DESCRIPTION:
    -----------------------
    Function for extracting and filtering raw signals bounded by channels0 and channel1. This function is written based on:   
    https://github.com/ethanfwilliams/OOI_RCA_DAS_notebook/blob/main/OOI_RCA_OptaSense_DAS_intro.ipynb. 
    
    INPUT PARAMETERS:
    -----------------------
    fp       : List with all file properties 
    channel0 : First channel
    channel1 : Last channel

    RETURNS:
    -----------------------
    strain : 2d-numpy array with strain values
    rawData_sel : 2d-numpy array with band-pass filtered raw data
    """
#     rawData = fp['Acquisition']['Raw[0]']['RawData']                               # Extracting raw data from fp dictionary
    rawData_sel = fp['Acquisition']['Raw[0]']['RawData'][:, channel0:channel1]
    fs = fp['Acquisition']['Raw[0]'].attrs['OutputDataRate']                       # Sampling frequency in Hz
#     rawData_sel = rawData[:, channel0:channel1]                                    # Selecting rawData traces bounded by channel0 and channel1
    rawData_filt = filtering(rawData_sel, fs, fmin, fmax,filter_type=filter_type)  # Band-pass filtered traces bounded by channel0 and channel1
    n = fp['Acquisition']['Custom'].attrs['Fibre Refractive Index']                # Extracting n factor from fp
    L = fp['Acquisition'].attrs['GaugeLength']                                     # Extracting L value from fp

    # Loop to convert raw data signals into strain
    strain = np.zeros((np.shape(rawData_sel)))                                    # Declaring strain array to store computed strain signals  
    
    for col_num in range(np.shape(rawData_filt)[1]):
        trace = rawData_filt[:, col_num]
        trace_strain = raw2strain(trace, n, L)
        strain[:, col_num] = trace_strain

    return (strain,rawData_filt,rawData_sel)


def sac_coord(n_sta, coord, dr):
    """
    DESCRIPTION:
    -----------------------
    Function for creating receiver coordinates required to create SAC files.  
    
    INPUT PARAMETERS:
    -----------------------
    n_sta       : Number of receivers 
    coord       : First and last coordinate (lat and lon) of the linear receiver spread.
    dr          : receiver or station separation in degrees

    RETURNS:
    -----------------------
    coord_sta : 1d -numpy array with computed receiver or station coordinates
    """
    coord_sta = np.zeros((n_sta, 2))
    lat = coord[0]
    lon = coord[1]
    R = ((coord[0] - coord[2]) ** 2 + (coord[1] - coord[3]) ** 2) ** 0.5
    sin_theta = (coord[1] - coord[3]) / R
    
    for rec_num in range(n_sta):
        lat += abs(sin_theta * dr)
        lon += abs(sin_theta * dr)
        coord_sta[rec_num, :] = (np.array([lat, lon]))
    
    return coord_sta


def writeSAC(Data, fs, init_time, netname, staname, coord, name_str, dx):
    """
    DESCRIPTION:
    -----------------------
    Function for converting 2D-numpy arrays into *SAC format. 
    
    INPUT PARAMETERS:
    -----------------------
    Data      : 2D - numpy array.
    fs        : Sampling frequency in Hz
    init_time : datetime format e.g. UTCDateTime(year, month, day, hours, minutes, seconds)
    netname   : String with the Network name
    staname   : String with the Station name
    coord     : Coordinates of receivers or stations in lat, lon. These coordinates depict a linear receivers spread computed using sac_coord function.
    name_str  : Base name of sac files.
    dx        : Station separation in meters.

    RETURNS:
    -----------------------
    SAC files per channel
    """
    st = Stream()                                 # Creating an object of multiple obspy traces
    lat = coord[:, 0]                             # Extracting latitude
    lon = coord[:, 1]                             # Extracting longitude
    
    # Loop for writing sac files.
    for ii in range(len(lat)):                 
        # Conditions to create names with 2 digits sufix
        stati = f'{staname}{str(ii).zfill(3)}'
        # Defning header with network, station names, latitude, longitude and distance of stations.     
        header = {'knetwk': netname, 'kstnm': stati, 'kcmpnm': 'ZZ', 'stla': lat[ii], 'stlo': lon[ii],
                  'evla': lat[ii] - 0.05, 'evlo': lon[ii] - 0.05, 'dist': 4 + (ii / 1000) * dx}
        # Indexing default parameters required by the SAC format
        sac = SACTrace(data=Data[:, ii], **header)
        tr = sac.to_obspy_trace()               # Creating a Obspy container to add basic properties.
        tr.stats.starttime = init_time          # Initial date and time.
        tr.stats.npts = len(tr.data)            # Number of samples in a single trace. 
        tr.stats.sampling_rate = fs             # Sampling frequency of the signal in Hz.
        tr.stats.station = header['kstnm']      # Station name.
        tr.stats.channel = header['kcmpnm']     # Channel name.
        tr.stats.distance = header['dist']      # Distance of the station respect to the source in km (Default value).
        tr.stats.network = header['knetwk']     # Network name.
        
        # Writing inididual SAC records per trace
        tr.write(f'{name_str}{str(ii).zfill(3)}'+'.sac', format='SAC')   
                                                      
def resampled_data(data, fs, fs_new):
    """
    DESCRIPTION:
    -----------------------
    Function for resampling signals. 
    
    INPUT PARAMETERS:
    -----------------------
    data      : 2D - numpy array.
    fs        : Sampling frequency in Hz
    fs_new    : New sampling frequency in Hz

    RETURNS:
    -----------------------
    res_array : 2D-numpy array with resampled signals using fs_new
    """
    st = Array_to_ObsPy(data, fs)
    st.resample(fs_new)
    res_array = Obspy_to_Array(st)
    
    return res_array

  
    
def lowpass(data, freq, df, corners=4, zerophase=True):
    """
    :type data: numpy.ndarray
    :param data: Data to filter.
    :param freq: Filter corner frequency.
    :param df: Sampling rate in Hz.
    :param corners: Filter corners / order.
    :param zerophase: If True, apply filter once forwards and once backwards.
        This results in twice the number of corners but zero phase shift in
        the resulting filtered trace.
    :return: Filtered data.
    """
    fe = 0.5 * df
    f = freq / fe
    z, p, k = iirfilter(corners, f, btype='lowpass', ftype='butter',
                        output='zpk')
    sos = zpk2sos(z, p, k)
    if zerophase:
        firstpass = sosfilt(sos, data)
        return sosfilt(sos, firstpass[::-1])[::-1]
    else:
        return sosfilt(sos, data)
    
def highpass(data, freq, df, corners=4, zerophase=True):
    """
    :type data: numpy.ndarray
    :param data: Data to filter.
    :param freq: Filter corner frequency.
    :param df: Sampling rate in Hz.
    :param corners: Filter corners / order.
    :param zerophase: If True, apply filter once forwards and once backwards.
        This results in twice the number of corners but zero phase shift in
        the resulting filtered trace.
    :return: Filtered data.
    """
    fe = 0.5 * df
    f = freq / fe
    
    z, p, k = iirfilter(corners, f, btype='highpass', ftype='butter',
                        output='zpk')
    sos = zpk2sos(z, p, k)
    if zerophase:
        firstpass = sosfilt(sos, data)
        return sosfilt(sos, firstpass[::-1])[::-1]
    else:
        return sosfilt(sos, data)
    
    
def bandpass(data, freqmin, freqmax, df, corners=4, zerophase=True):
    """
    :type data: numpy.ndarray
    :param data: Data to filter.
    :param freqmin: Pass band low corner frequency.
    :param freqmax: Pass band high corner frequency.
    :param df: Sampling rate in Hz.
    :param corners: Filter corners / order.
    :param zerophase: If True, apply filter once forwards and once backwards.
        This results in twice the filter order but zero phase shift in
        the resulting filtered trace.
    :return: Filtered data.
    """
    fe = 0.5 * df
    low = freqmin / fe
    high = freqmax / fe
    z, p, k = iirfilter(corners, [low, high], btype='band',
                        ftype='butter', output='zpk')
    sos = zpk2sos(z, p, k)
    if zerophase:
        firstpass = sosfilt(sos, data)
        return sosfilt(sos, firstpass[::-1])[::-1]
    else:
        return sosfilt(sos, data)    




def agc_gain(data, agc_gate,fs,method='rms'):
    '''
    Applying AGC gain to seismic data. Fast way to find trends in the F-K domain
    However, it is not true amplitude correction, so the input gives not valid
    results when using for AVO analysis or inversion.
    
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
    
    for k in range(0,nx):
        
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



def pws(arr, sampling_rate, power=2, pws_timegate=5.0):
    """
    Performs phase-weighted stack on array of time series. Modified on the noise function by Tim Climents.
    Follows methods of Schimmel and Paulssen, 1997.
    If s(t) is time series data (seismogram, or cross-correlation),
    S(t) = s(t) + i*H(s(t)), where H(s(t)) is Hilbert transform of s(t)
    S(t) = s(t) + i*H(s(t)) = A(t)*exp(i*phi(t)), where
    A(t) is envelope of s(t) and phi(t) is phase of s(t)
    Phase-weighted stack, g(t), is then:
    g(t) = 1/N sum j = 1:N s_j(t) * | 1/N sum k = 1:N exp[i * phi_k(t)]|^v
    where N is number of traces used, v is sharpness of phase-weighted stack

    PARAMETERS:
    ---------------------
    arr: N length array of time series data (numpy.ndarray)
    sampling_rate: sampling rate of time series arr (int)
    power: exponent for phase stack (int)
    pws_timegate: number of seconds to smooth phase stack (float)

    RETURNS:
    ---------------------
    weighted: Phase weighted stack of time series data (numpy.ndarray)
    """

    if arr.ndim == 1:
        return arr
    N, M = arr.shape
    analytic = hilbert(arr, axis=1, N=next_fast_len(M))[:, :M]
    phase = np.angle(analytic)
    phase_stack = np.mean(np.exp(1j * phase), axis=0)
    phase_stack = np.abs(phase_stack) ** (power)

    # smoothing
    # timegate_samples = int(pws_timegate * sampling_rate)
    # phase_stack = moving_ave(phase_stack,timegate_samples)
    weighted = np.multiply(arr, phase_stack)
    return np.mean(weighted, axis=0)
