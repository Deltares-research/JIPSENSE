import sys
import os
import glob
from obspy import Trace, Stream, UTCDateTime
import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LogNorm
import matplotlib 

# import modules from scripts
sys.path.append('..\scripts')
import sbb_module as sbbm


def get_Props(allfiles_init):

    params_init = {}

    params_init['first_channel'] = 0
    params_init['last_channel'] = 10000  # Default value to extract all channels
    params_init['first_time_sample'] = 0 
    params_init['last_time_sample'] =  30000 # Default value to extract all time samples

    # Loadind data and properties

    _, props = sbbm.loadTDMS(allfiles_init,params_init)

    return props


def get_section(data, channels, chan_init, chan_end):
    """
    Extracts a section of the data based on channel range.
    
    Parameters:
    data (numpy.ndarray): The seismic data array.
    channels (numpy.ndarray): The array of channel positions.
    chan_init (float): The starting channel position.
    chan_end (float): The ending channel position.
    
    Returns:
    numpy.ndarray: The selected section of the data.
    """
    # Find index for channels between chan_init and chan_end
    chan_index = np.where((channels >= chan_init) & (channels <= chan_end))[0]
    # Select data for the specified channels
    return data[:, chan_index]


def scale_data(data, scale_factor,fs,gl):
    """
    Scales the seismic data based on the provided scale factor, sampling frequency, and gauge length.
    
    Parameters:
    data (numpy.ndarray): The seismic data array.
    scale_factor (float): The scale factor for the data.
    fs (float): Sampling frequency in Hz.
    gl (float): Gauge length in meters.
    
    Returns:
    numpy.ndarray: The scaled seismic data.
    """
    return (data / scale_factor) * 116 * fs / gl


allfiles = glob.glob(r'F:\Measurements GL 5m\*tdms')
if len(allfiles) == 0:
    print('No files found in the specified directory.')
    sys.exit()

len(allfiles)


allfiles_init = allfiles[0]  # Adjust the slice as needed

props = get_Props(allfiles_init)

start_ = props["Start Distance (m)"]
stop_ = props["Stop Distance (m)"]
dx = props['SpatialResolution[m]']
fs = props['SamplingFrequency[Hz]']
gl = props['GaugeLength']
channels = np.arange(start_, stop_, dx)


chan_init = 1200 #4200 #2100 #3500 #1700 # in meters
chan_end = 2500 #4300 #2200 #3600 #1800 # in meters

output_folder = r'C:\Users\obandohe\OneDrive - Stichting Deltares\Documents\DELTARES_PROJECTS\2025\10_DAS_Switzerland\03_RESULTS\SHOTS_INSPECTION'


chan_index = np.where((channels >= chan_init) & (channels <= chan_end))[0]

first_channel = np.min(chan_index)  
last_channel = np.max(chan_index)   
first_time_sample = 0
last_time_sample = fs*30

data_stored = []
store_names = []


for path_files in allfiles[225:235]:  # Adjust the slice as needed

    # Creating dictionary with fiber geometry
    params = {}

    params['first_channel'] = first_channel
    params['last_channel'] = last_channel
    params['first_time_sample'] = first_time_sample 
    params['last_time_sample'] =  last_time_sample 
    data_sel, props = sbbm.loadTDMS(path_files,params)

    data_stored.append(data_sel)
    store_names.append(os.path.basename(path_files))


    # plot full record
    plt.figure(figsize=(20, 8))
    plt.imshow(np.log10(np.abs(data_sel) + 1), aspect='auto', cmap='jet', extent=[channels[chan_index[0]], channels[chan_index[-1]], 0, data_sel.shape[0] / fs])
    plt.colorbar(label='Amplitude')

    plt.xlabel('Distance (m)')
    plt.ylabel('Time (s)')
    plt.title(f'Seismic Data from {os.path.basename(path_files)}')

    # add ticks every 1000 meters
    plt.xticks(np.arange(channels[chan_index[0]], channels[chan_index[-1]], 50))

    # make tick numbers vertical
    plt.xticks(rotation=45,fontsize=8)
    plt.grid()

    # save figure
    #plt.savefig(os.path.join(output_folder, f'seismic_data_{os.path.basename(path_files)}_outcrop.png'))
    plt.close()

    plt.show()