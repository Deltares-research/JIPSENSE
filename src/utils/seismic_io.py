"""
Seismic data I/O utilities for reading SPECFEM2D output and storing in HDF5 format.

Handles reading .semp trace files, computing dt, and storing traces with metadata.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import numpy as np
import h5py
from .mesh_plotting import parse_source_file, parse_stations_file


def read_semp_file(semp_file: Path) -> Tuple[np.ndarray, np.ndarray, float]:
    """
    Read a SPECFEM2D seismic trace file (.semp format).
    
    Format: Two columns separated by whitespace
    - Column 1: Time (seconds)
    - Column 2: Pressure/Amplitude
    
    Args:
        semp_file: Path to .semp file
        
    Returns:
        Tuple of (time array, pressure array, dt)
    """
    try:
        data = np.loadtxt(semp_file)
        
        if data.ndim == 1:
            # Single sample (unlikely, but handle it)
            time = np.array([data[0]])
            pressure = np.array([data[1]])
        else:
            time = data[:, 0]
            pressure = data[:, 1]
        
        # Compute dt from time differences
        if len(time) > 1:
            dt = float(np.mean(np.diff(time)))
        else:
            dt = 1.0  # Default if only one sample
        
        return time, pressure, dt
    
    except Exception as e:
        print(f"Error reading {semp_file}: {e}")
        return None, None, None


def read_all_traces(output_dir: Path, network: str = 'AA', 
                    component: str = 'PRE') -> Dict[str, Dict]:
    """
    Read all seismic traces from a simulation output directory.
    
    Reads all files matching pattern: {NETWORK}.S{STATION_ID}.{COMPONENT}.semp
    
    Args:
        output_dir: Path to OUTPUT_FILES directory
        network: Network code (default 'AA' for SPECFEM2D)
        component: Component type (default 'PRE' for pressure)
        
    Returns:
        Dictionary with station names as keys, each containing:
        - 'time': Time array
        - 'pressure': Pressure array
        - 'dt': Sampling rate (seconds)
        - 'num_samples': Number of samples
    """
    traces = {}
    
    # Find all matching files
    pattern = f"{network}.S*.{component}.semp"
    semp_files = sorted(output_dir.glob(pattern))
    
    print(f"Found {len(semp_files)} trace files matching {pattern}")
    
    for semp_file in semp_files:
        # Extract station name from filename (e.g., AA.S0001.PRE.semp -> S0001)
        station_id = semp_file.stem.split('.')[1]  # Get 'S0001' from filename
        
        time, pressure, dt = read_semp_file(semp_file)
        
        if time is not None:
            traces[station_id] = {
                'time': time,
                'pressure': pressure,
                'dt': dt,
                'num_samples': len(time)
            }
            print(f"  ✓ {station_id}: {len(time)} samples, dt={dt:.6f}s")
    
    return traces


def save_traces_to_hdf5(traces: Dict, output_file: Path,
                        source_file: Optional[Path] = None,
                        stations_file: Optional[Path] = None) -> None:
    """
    Save seismic traces to HDF5 file with metadata.
    
    Structure:
    - /traces/{station_id}/time: Time array
    - /traces/{station_id}/pressure: Pressure array
    - /traces/{station_id}/dt: Sampling rate
    - /metadata/dt: Global sampling rate (from first trace)
    - /metadata/source_x: Source x coordinate
    - /metadata/source_z: Source z coordinate
    - /receivers/{station_id}: Receiver x, z coordinates
    
    Args:
        traces: Dictionary from read_all_traces()
        output_file: Path to output .h5 file
        source_file: Optional path to SOURCE file for metadata
        stations_file: Optional path to STATIONS file for receiver geometry
    """
    
    # Read metadata
    source_data = None
    stations_data = {}
    
    if source_file and source_file.exists():
        source_data = parse_source_file(source_file)
        print(f"✓ Source metadata: x={source_data['x']}, z={source_data['z']}")
    
    if stations_file and stations_file.exists():
        stations_list = parse_stations_file(stations_file)
        stations_data = {s['name']: {'x': s['x'], 'z': s['z']} 
                        for s in stations_list}
        print(f"✓ Loaded {len(stations_data)} receiver positions")
    
    # Create HDF5 file
    with h5py.File(output_file, 'w') as f:
        
        # Store traces
        traces_group = f.create_group('traces')
        
        for station_id, trace_data in sorted(traces.items()):
            station_group = traces_group.create_group(station_id)
            
            # Store time and pressure arrays
            station_group.create_dataset('time', data=trace_data['time'])
            station_group.create_dataset('pressure', data=trace_data['pressure'])
            station_group.attrs['dt'] = trace_data['dt']
            station_group.attrs['num_samples'] = trace_data['num_samples']
        
        # Store global metadata
        metadata_group = f.create_group('metadata')
        
        # Use dt from first trace as global dt
        if traces:
            first_dt = list(traces.values())[0]['dt']
            metadata_group.attrs['dt'] = first_dt
            metadata_group.attrs['num_traces'] = len(traces)
        
        # Store source geometry
        if source_data:
            metadata_group.attrs['source_x'] = source_data['x']
            metadata_group.attrs['source_z'] = source_data['z']
        
        # Store receiver geometry
        if stations_data:
            receivers_group = f.create_group('receivers')
            for station_id, coords in sorted(stations_data.items()):
                recv_group = receivers_group.create_group(station_id)
                recv_group.attrs['x'] = coords['x']
                recv_group.attrs['z'] = coords['z']
    
    print(f"✓ Traces saved to {output_file}")


def load_traces_from_hdf5(h5_file: Path) -> Tuple[Dict, Dict]:
    """
    Load seismic traces and metadata from HDF5 file.
    
    Args:
        h5_file: Path to .h5 file
        
    Returns:
        Tuple of (traces dict, metadata dict)
    """
    traces = {}
    metadata = {}
    
    with h5py.File(h5_file, 'r') as f:
        
        # Load traces
        if 'traces' in f:
            for station_id in f['traces'].keys():
                station_group = f['traces'][station_id]
                traces[station_id] = {
                    'time': station_group['time'][:],
                    'pressure': station_group['pressure'][:],
                    'dt': float(station_group.attrs.get('dt', 0))
                }
        
        # Load metadata
        if 'metadata' in f:
            for key, value in f['metadata'].attrs.items():
                metadata[key] = value
        
        # Load receiver geometry
        receivers = {}
        if 'receivers' in f:
            for station_id in f['receivers'].keys():
                recv_group = f['receivers'][station_id]
                receivers[station_id] = {
                    'x': float(recv_group.attrs.get('x', 0)),
                    'z': float(recv_group.attrs.get('z', 0))
                }
        
        if receivers:
            metadata['receivers'] = receivers
    
    return traces, metadata


def print_hdf5_info(h5_file: Path) -> None:
    """
    Print information about HDF5 trace file.
    
    Args:
        h5_file: Path to .h5 file
    """
    with h5py.File(h5_file, 'r') as f:
        
        print(f"\n{'='*60}")
        print(f"HDF5 File: {h5_file.name}")
        print(f"{'='*60}\n")
        
        # Print metadata
        if 'metadata' in f:
            print("Metadata:")
            for key, value in f['metadata'].attrs.items():
                print(f"  {key}: {value}")
            print()
        
        # Print trace info
        if 'traces' in f:
            print(f"Traces: {len(f['traces'])} stations")
            for station_id in sorted(f['traces'].keys())[:5]:  # Show first 5
                station_group = f['traces'][station_id]
                num_samples = len(station_group['time'])
                dt = station_group.attrs.get('dt', 0)
                duration = (num_samples - 1) * dt if num_samples > 1 else 0
                print(f"  {station_id}: {num_samples} samples, "
                      f"dt={dt:.6f}s, duration={duration:.3f}s")
            if len(f['traces']) > 5:
                print(f"  ... and {len(f['traces']) - 5} more stations")
            print()
        
        # Print receiver geometry
        if 'receivers' in f:
            print(f"Receivers: {len(f['receivers'])} stations")
            for station_id in sorted(f['receivers'].keys())[:5]:  # Show first 5
                recv_group = f['receivers'][station_id]
                x = recv_group.attrs.get('x', 0)
                z = recv_group.attrs.get('z', 0)
                print(f"  {station_id}: x={x:.1f}m, z={z:.1f}m")
            if len(f['receivers']) > 5:
                print(f"  ... and {len(f['receivers']) - 5} more stations")
            print()
