#!/usr/bin/env python
"""
SPECFEM2D Source File Generator

This script creates the SOURCE file for SPECFEM2D simulations.
Configuration parameters are loaded from source_config.yml
"""

import os
import glob
import yaml
from pathlib import Path

# ==============================================================================
# Setup
# ==============================================================================
config_file = Path('/home/obandohe/JIPSENSE/JIPSENSE/specfem2d_config/source_config.yml')
if not config_file.exists():
    raise FileNotFoundError(f"Configuration file not found: {config_file}")

with open(config_file, 'r') as f:
    cfg = yaml.safe_load(f)

data_dir = Path('/home/obandohe/JIPSENSE/JIPSENSE/src/simulation/DATA')
source_file_path = data_dir / 'SOURCE'
original_dir = os.getcwd()

print(f"✓ Loaded configuration from: {config_file}\n")

# Clean DATA directory of old SOURCE files
print("Cleaning existing SOURCE files...")
for file in glob.glob(str(data_dir / "SOURCE*")):
    try:
        os.remove(file)
        print(f"  Removed: {os.path.basename(file)}")
    except OSError:
        pass
print()

# ==============================================================================
# Helper Functions
# ==============================================================================
def bool_to_fortran(value):
    """Convert Python boolean to Fortran logical format"""
    return ".true." if value else ".false."

def format_value(value):
    """Format a value for the SOURCE file"""
    if isinstance(value, bool):
        return bool_to_fortran(value)
    elif isinstance(value, float):
        if value == int(value):
            return f"{int(value)}."
        else:
            return f"{value:.10e}".replace('e', 'd')
    return str(value)

# ==============================================================================
# Generate SOURCE File Content
# ==============================================================================
print(f"SOURCE file will be created at: {source_file_path}\n")

source_lines = []

# Process each source
for source_id, source_cfg in cfg['sources'].items():
    source_num = source_id.split('_')[1]
    source_lines.append(f"## Source {source_num}")
    
    source_lines.extend([
        f"source_surf                     = {bool_to_fortran(source_cfg['source_surf'])}",
        f"xs                              = {format_value(source_cfg['xs'])}",
        f"zs                              = {format_value(source_cfg['zs'])}",
        "## Source type parameters:",
        "#  1 = elastic force or acoustic pressure",
        "#  2 = moment tensor",
        "# or Initial field type (when initialfield set in Par_file):",
        "# For a plane wave including converted and reflected waves at the free surface:",
        "#  1 = P wave,",
        "#  2 = S wave,",
        "#  3 = Rayleigh wave",
        "# For a plane wave without converted nor reflected waves at the free surface, i.e. with the incident wave only:",
        "#  4 = P wave,",
        "#  5 = S wave",
        "# For initial mode displacement:",
        "#  6 = mode (2,3) of a rectangular membrane",
        f"source_type                     = {source_cfg['source_type']}",
        "# Source time function:",
        "# In the case of a source located in an acoustic medium,",
        "# to get pressure for a Ricker in the seismograms, here we need to select a Gaussian for the potential Chi",
        "# used as a source, rather than a Ricker, because pressure = - Chi_dot_dot.",
        "# This is true both when USE_TRICK_FOR_BETTER_PRESSURE is set to .true. or to .false.",
        "# Options:",
        "#  1 = second derivative of a Gaussian (a.k.a. Ricker),",
        "#  2 = first derivative of a Gaussian,",
        "#  3 = Gaussian,",
        "#  4 = Dirac,",
        "#  5 = Heaviside (4 and 5 will produce noisy recordings because of frequencies above the mesh resolution limit),",
        "#  6 = ocean acoustics type I,",
        "#  7 = ocean acoustics type II,",
        "#  8 = external source time function = 8 (source read from file),",
        "#  9 = burst,",
        "# 10 = Sinus source time function,",
        "# 11 = Marmousi Ormsby wavelet",
        f"time_function_type              = {source_cfg['time_function_type']}",
        "# If time_function_type == 8, enter below the custom source file to read (two columns file with time and amplitude) :",
        "# (For the moment dt must be equal to the dt of the simulation. File name cannot exceed 150 characters)",
        "# IMPORTANT: do NOT put quote signs around the file name, just put the file name itself otherwise the run will stop",
        f"name_of_source_file             = {source_cfg['name_of_source_file']}",
        f"burst_band_width                = {format_value(source_cfg['burst_band_width'])}",
        f"f0                              = {format_value(source_cfg['f0'])}",
        f"tshift                          = {format_value(source_cfg['tshift'])}",
        "## Force source",
        "# angle of the source (for a force only); for a plane wave, this is the incidence angle; for moment tensor sources this is unused",
        f"anglesource                     = {format_value(source_cfg['anglesource'])}",
        "## Moment tensor",
        "# The components of a moment tensor source must be given in N.m, not in dyne.cm as in the DATA/CMTSOLUTION source file of the 3D version of the code.",
        f"Mxx                             = {format_value(source_cfg['mxx'])}",
        f"Mzz                             = {format_value(source_cfg['mzz'])}",
        f"Mxz                             = {format_value(source_cfg['mxz'])}",
        "## Amplification (factor to amplify source time function)",
        f"factor                          = {format_value(source_cfg['factor'])}",
        "## Moving source parameters",
        f"vx                              = {format_value(source_cfg['vx'])}",
        f"vz                              = {format_value(source_cfg['vz'])}",
        "",
    ])

# Write SOURCE file
with open(source_file_path, 'w') as f:
    f.write("\n".join(source_lines))

print(f"✓ SOURCE file created successfully at: {source_file_path}")
print(f"  File size: {source_file_path.stat().st_size} bytes")

os.chdir(original_dir)
