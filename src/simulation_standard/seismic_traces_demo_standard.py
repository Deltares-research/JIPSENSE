"""
Demo script: Read seismic traces and save to HDF5 format.

Reads all .semp files from simulation output, extracts time and pressure,
computes dt, and saves to HDF5 with source and receiver geometry metadata.
"""

from pathlib import Path
import sys
import os

# Add src to path - robust path resolution
try:
    # Try using __file__ if available (direct execution)
    # Script is in src/simulation_standard, so go up 2 levels to project root
    project_root = Path(__file__).parent.parent.parent
except:
    # Fall back to current working directory (interactive/notebook context)
    project_root = Path(os.getcwd())

sys.path.insert(0, str(project_root))

from src.utils.seismic_io import (
    read_all_traces, save_traces_to_hdf5, load_traces_from_hdf5, print_hdf5_info
)


def main():
    """Read seismic traces from simulation output and save to HDF5."""
    
    # Define paths - robust resolution
    try:
        # Script is in src/simulation_standard, so go up 2 levels to project root
        project_root = Path(__file__).parent.parent.parent
    except:
        project_root = Path(os.getcwd())
    
    # Set up simulation_standard directory paths
    sim_standard_dir = project_root / "src/simulation_standard"
    data_dir = sim_standard_dir / "DATA"
    
    # Find the latest OUTPUT_FILES folder in simulation_standard/output_standard
    output_base = sim_standard_dir / "output_standard"
    if not output_base.exists():
        print(f"❌ Output directory not found: {output_base}")
        return
    
    output_folders = sorted([f for f in output_base.glob("OUTPUT_FILES_*") if f.is_dir()], reverse=True)
    
    if not output_folders:
        print("❌ No OUTPUT_FILES found. Please run simulation first.")
        return
    
    output_dir = output_folders[0]
    
    # Create h5 output directory if it doesn't exist
    h5_dir = sim_standard_dir / "h5"
    h5_dir.mkdir(exist_ok=True)
    h5_output = h5_dir / f"{output_dir.name}.h5"
    
    source_file = data_dir / "SOURCE"
    stations_file = data_dir / "STATIONS"
    
    print(f"\n{'='*60}")
    print("SEISMIC TRACE PROCESSING")
    print(f"{'='*60}\n")
    
    print(f"Output folder:  {output_dir}")
    print(f"Source file:    {source_file}")
    print(f"Stations file:  {stations_file}")
    print(f"HDF5 output:    {h5_output}\n")
    
    # Verify files exist
    if not output_dir.exists():
        print(f"❌ Output directory not found: {output_dir}")
        return
    
    if not source_file.exists():
        print(f"⚠️  Source file not found: {source_file}")
        source_file = None
    
    if not stations_file.exists():
        print(f"⚠️  Stations file not found: {stations_file}")
        stations_file = None
    
    # Read all traces
    print("Reading seismic traces...\n")
    traces = read_all_traces(output_dir, network='AA', component='PRE')
    
    if not traces:
        print("❌ No traces found!")
        return
    
    print(f"\n✓ Successfully read {len(traces)} traces\n")
    
    # Save to HDF5
    print("Saving to HDF5 format...\n")
    save_traces_to_hdf5(traces, h5_output, source_file, stations_file)
    
    # Print HDF5 info
    print_hdf5_info(h5_output)
    
    # Verify by loading
    print("Verifying HDF5 file...")
    loaded_traces, metadata = load_traces_from_hdf5(h5_output)
    print(f"✓ Loaded {len(loaded_traces)} traces from HDF5")
    print(f"✓ Metadata: {metadata}\n")


if __name__ == '__main__':
    main()
