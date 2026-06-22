#!/usr/bin/env python
"""
SPECFEM2D Complete Parameter File Generator

This script creates and manages the Par_file for SPECFEM2D simulations.
Configuration parameters are loaded from specfem2d_config.yml
"""

import os
import glob
import yaml
from pathlib import Path

# ==============================================================================
# Setup
# ==============================================================================
config_file = Path('/home/obandohe/JIPSENSE/JIPSENSE/specfem2d_config/specfem2d_config.yml')
if not config_file.exists():
    raise FileNotFoundError(f"Configuration file not found: {config_file}")

with open(config_file, 'r') as f:
    cfg = yaml.safe_load(f)

data_dir = Path('/home/obandohe/JIPSENSE/JIPSENSE/src/simulation/DATA')
par_file_path = data_dir / 'Par_file'
original_dir = os.getcwd()

print(f"✓ Loaded configuration from: {config_file}\n")

# Clean DATA directory
print("Cleaning existing DATA files...")
for pattern in ["Par_file", "*.dat", "*.txt"]:
    for file in glob.glob(str(data_dir / pattern)):
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
    """Format a value for the Par_file"""
    if isinstance(value, bool):
        return bool_to_fortran(value)
    elif isinstance(value, float):
        if value == int(value):
            return f"{int(value)}.d0"
        else:
            return f"{value:.10e}".replace('e', 'd')
    return str(value)

# ==============================================================================
# Generate Par_file Content
# ==============================================================================
print(f"Par_file will be created at: {par_file_path}\n")

par_lines = [
    "#-----------------------------------------------------------",
    "# Simulation input parameters",
    "#-----------------------------------------------------------",
    "",
    "# title of job",
    f"title                           = {cfg['simulation']['title']}",
    "",
    "# forward or adjoint simulation",
    "# 1 = forward, 2 = adjoint, 3 = both simultaneously",
    f"SIMULATION_TYPE                 = {cfg['simulation']['simulation_type']}",
    f"NOISE_TOMOGRAPHY                = {cfg['simulation']['noise_tomography']}",
    f"SAVE_FORWARD                    = {bool_to_fortran(cfg['simulation']['save_forward'])}",
    "",
    "# parameters concerning partitioning",
    f"NPROC                           = {cfg['simulation']['nproc']}              # number of processes",
    "",
    "# time step parameters",
    f"NSTEP                           = {cfg['time_parameters']['nstep']}",
    f"DT                              = {format_value(cfg['time_parameters']['dt'])}",
    f"time_stepping_scheme            = {cfg['time_parameters']['time_stepping_scheme']}",
    "",
    "# set the type of calculation (P-SV or SH/membrane waves)",
    f"P_SV                            = {bool_to_fortran(cfg['wave_type']['p_sv'])}",
    "",
    "# axisymmetric (2.5D) or Cartesian planar (2D) simulation",
    f"AXISYM                          = {bool_to_fortran(cfg['wave_type']['axisym'])}",
    "",
    "#-----------------------------------------------------------",
    "# Mesh and Material Properties",
    "#-----------------------------------------------------------",
    "",
    f"PARTITIONING_TYPE               = {cfg['mesh']['partitioning_type']}",
    f"NGNOD                           = {cfg['mesh']['ngnod']}",
    f"setup_with_binary_database      = {cfg['mesh']['setup_with_binary_database']}",
    f"MODEL                           = {cfg['mesh']['model']}",
    f"SAVE_MODEL                      = {cfg['mesh']['save_model']}",
    f"read_external_mesh              = {bool_to_fortran(cfg['mesh']['read_external_mesh'])}",
    "",
    "#-----------------------------------------------------------",
    "# Attenuation",
    "#-----------------------------------------------------------",
    "",
    f"ATTENUATION_VISCOELASTIC        = {bool_to_fortran(cfg['attenuation']['attenuation_viscoelastic'])}",
    f"ATTENUATION_VISCOACOUSTIC       = {bool_to_fortran(cfg['attenuation']['attenuation_viscoacoustic'])}",
    f"N_SLS                           = {cfg['attenuation']['n_sls']}",
    f"ATTENUATION_f0_REFERENCE        = {format_value(cfg['attenuation']['attenuation_f0_reference'])}",
    f"READ_VELOCITIES_AT_f0           = {bool_to_fortran(cfg['attenuation']['read_velocities_at_f0'])}",
    f"USE_SOLVOPT                     = {bool_to_fortran(cfg['attenuation']['use_solvopt'])}",
    f"ATTENUATION_PORO_FLUID_PART     = {bool_to_fortran(cfg['attenuation']['attenuation_poro_fluid_part'])}",
    f"Q0_poroelastic                  = {cfg['attenuation']['q0_poroelastic']}",
    f"freq0_poroelastic               = {cfg['attenuation']['freq0_poroelastic']}",
    f"UNDO_ATTENUATION_AND_OR_PML     = {bool_to_fortran(cfg['attenuation']['undo_attenuation_and_or_pml'])}",
    f"NT_DUMP_ATTENUATION             = {cfg['attenuation']['nt_dump_attenuation']}",
    f"NO_BACKWARD_RECONSTRUCTION      = {bool_to_fortran(cfg['attenuation']['no_backward_reconstruction'])}",
    f"ATTENUATION_PERMITTIVITY        = {bool_to_fortran(cfg['attenuation']['attenuation_permittivity'])}",
    f"ATTENUATION_CONDUCTIVITY        = {bool_to_fortran(cfg['attenuation']['attenuation_conductivity'])}",
    f"f0_electromagnetic              = {cfg['attenuation']['f0_electromagnetic']}",
    "",
    "#-----------------------------------------------------------",
    "# Sources and Receivers",
    "#-----------------------------------------------------------",
    "",
    f"NSOURCES                        = {cfg['sources']['nsources']}",
    f"force_normal_to_surface         = {bool_to_fortran(cfg['sources']['force_normal_to_surface'])}",
    f"initialfield                    = {bool_to_fortran(cfg['sources']['initialfield'])}",
    f"add_Bielak_conditions_bottom    = {bool_to_fortran(cfg['sources']['add_bielak_conditions_bottom'])}",
    f"add_Bielak_conditions_right     = {bool_to_fortran(cfg['sources']['add_bielak_conditions_right'])}",
    f"add_Bielak_conditions_top       = {bool_to_fortran(cfg['sources']['add_bielak_conditions_top'])}",
    f"add_Bielak_conditions_left      = {bool_to_fortran(cfg['sources']['add_bielak_conditions_left'])}",
    f"ACOUSTIC_FORCING                = {bool_to_fortran(cfg['sources']['acoustic_forcing'])}",
    f"noise_source_time_function_type = {cfg['sources']['noise_source_time_function_type']}",
    f"write_moving_sources_database   = {bool_to_fortran(cfg['sources']['write_moving_sources_database'])}",
    "",
    "# Receivers",
    f"seismotype                      = {cfg['receivers']['seismotype']}",
    f"NTSTEP_BETWEEN_OUTPUT_SEISMOS   = {cfg['receivers']['ntstep_between_output_seismos']}",
    f"NTSTEP_BETWEEN_OUTPUT_SAMPLE    = {cfg['receivers']['ntstep_between_output_sample']}",
    f"USE_TRICK_FOR_BETTER_PRESSURE   = {bool_to_fortran(cfg['receivers']['use_trick_for_better_pressure'])}",
    f"USER_T0                         = {format_value(cfg['receivers']['user_t0'])}",
    f"save_ASCII_seismograms          = {bool_to_fortran(cfg['receivers']['save_ascii_seismograms'])}",
    f"save_binary_seismograms_single  = {bool_to_fortran(cfg['receivers']['save_binary_seismograms_single'])}",
    f"save_binary_seismograms_double  = {bool_to_fortran(cfg['receivers']['save_binary_seismograms_double'])}",
    f"SU_FORMAT                       = {bool_to_fortran(cfg['receivers']['su_format'])}",
    f"use_existing_STATIONS           = {bool_to_fortran(cfg['receivers']['use_existing_stations'])}",
    f"nreceiversets                   = {cfg['receivers']['nreceiversets']}",
    f"anglerec                        = {format_value(cfg['receivers']['anglerec'])}",
    f"rec_normal_to_surface           = {bool_to_fortran(cfg['receivers']['rec_normal_to_surface'])}",
    f"nrec                            = {cfg['receivers']['nrec']}",
    f"xdeb                            = {format_value(cfg['receivers']['xdeb'])}",
    f"zdeb                            = {format_value(cfg['receivers']['zdeb'])}",
    f"xfin                            = {format_value(cfg['receivers']['xfin'])}",
    f"zfin                            = {format_value(cfg['receivers']['zfin'])}",
    f"record_at_surface_same_vertical = {bool_to_fortran(cfg['receivers']['record_at_surface_same_vertical'])}",
    "",
    "#-----------------------------------------------------------",
    "# Kernels and Boundary Conditions",
    "#-----------------------------------------------------------",
    "",
    f"save_ASCII_kernels              = {bool_to_fortran(cfg['kernels']['save_ascii_kernels'])}",
    f"NTSTEP_BETWEEN_COMPUTE_KERNELS  = {cfg['kernels']['ntstep_between_compute_kernels']}",
    f"APPROXIMATE_HESS_KL             = {bool_to_fortran(cfg['kernels']['approximate_hess_kl'])}",
    "",
    "# PML",
    f"PML_BOUNDARY_CONDITIONS         = {bool_to_fortran(cfg['pml']['pml_boundary_conditions'])}",
    f"NELEM_PML_THICKNESS             = {cfg['pml']['nelem_pml_thickness']}",
    f"ROTATE_PML_ACTIVATE             = {bool_to_fortran(cfg['pml']['rotate_pml_activate'])}",
    f"ROTATE_PML_ANGLE                = {format_value(cfg['pml']['rotate_pml_angle'])}",
    f"K_MIN_PML                       = {format_value(cfg['pml']['k_min_pml'])}",
    f"K_MAX_PML                       = {format_value(cfg['pml']['k_max_pml'])}",
    f"damping_change_factor_acoustic  = {format_value(cfg['pml']['damping_change_factor_acoustic'])}",
    f"damping_change_factor_elastic   = {format_value(cfg['pml']['damping_change_factor_elastic'])}",
    f"PML_PARAMETER_ADJUSTMENT        = {bool_to_fortran(cfg['pml']['pml_parameter_adjustment'])}",
    "",
    "# Stacey and Periodic",
    f"STACEY_ABSORBING_CONDITIONS     = {bool_to_fortran(cfg['boundary_conditions']['stacey_absorbing_conditions'])}",
    f"ADD_PERIODIC_CONDITIONS         = {bool_to_fortran(cfg['boundary_conditions']['add_periodic_conditions'])}",
    f"PERIODIC_HORIZ_DIST             = {format_value(cfg['boundary_conditions']['periodic_horiz_dist'])}",
    "",
    "#-----------------------------------------------------------",
    "# Velocity and Density Models",
    "#-----------------------------------------------------------",
    "",
    f"nbmodels                        = {cfg['velocity_model']['nbmodels']}",
]

for model in cfg['velocity_model']['models']:
    par_lines.append(" ".join(str(m) for m in model))

par_lines.extend([
    f"TOMOGRAPHY_FILE                 = {cfg['velocity_model']['tomography_file']}",
    "",
    "#-----------------------------------------------------------",
    "# External Mesh Files",
    "#-----------------------------------------------------------",
    "",
    f"mesh_file                       = {cfg['external_mesh']['mesh_file']}",
    f"nodes_coords_file               = {cfg['external_mesh']['nodes_coords_file']}",
    f"materials_file                  = {cfg['external_mesh']['materials_file']}",
    f"free_surface_file               = {cfg['external_mesh']['free_surface_file']}",
    f"axial_elements_file             = {cfg['external_mesh']['axial_elements_file']}",
    f"absorbing_surface_file          = {cfg['external_mesh']['absorbing_surface_file']}",
    f"acoustic_forcing_surface_file   = {cfg['external_mesh']['acoustic_forcing_surface_file']}",
    f"absorbing_cpml_file             = {cfg['external_mesh']['absorbing_cpml_file']}",
    f"tangential_detection_curve_file = {cfg['external_mesh']['tangential_detection_curve_file']}",
    "",
    "#-----------------------------------------------------------",
    "# Internal Mesh",
    "#-----------------------------------------------------------",
    "",
    f"interfacesfile                  = {cfg['internal_mesh']['interfacesfile']}",
    f"xmin                            = {format_value(cfg['internal_mesh']['xmin'])}",
    f"xmax                            = {format_value(cfg['internal_mesh']['xmax'])}",
    f"nx                              = {cfg['internal_mesh']['nx']}",
    "",
    f"absorbbottom                    = {bool_to_fortran(cfg['internal_mesh']['absorbbottom'])}",
    f"absorbright                     = {bool_to_fortran(cfg['internal_mesh']['absorbright'])}",
    f"absorbtop                       = {bool_to_fortran(cfg['internal_mesh']['absorbtop'])}",
    f"absorbleft                      = {bool_to_fortran(cfg['internal_mesh']['absorbleft'])}",
    "",
    f"nbregions                       = {cfg['internal_mesh']['nbregions']}",
])

for region in cfg['internal_mesh']['regions']:
    par_lines.append(" ".join(str(r) for r in region))

par_lines.extend([
    "",
    "#-----------------------------------------------------------",
    "# Display and Output",
    "#-----------------------------------------------------------",
    "",
    f"NTSTEP_BETWEEN_OUTPUT_INFO      = {cfg['display']['ntstep_between_output_info']}",
    f"output_grid_Gnuplot             = {bool_to_fortran(cfg['display']['output_grid_gnuplot'])}",
    f"output_grid_ASCII               = {bool_to_fortran(cfg['display']['output_grid_ascii'])}",
    f"OUTPUT_ENERGY                   = {bool_to_fortran(cfg['display']['output_energy'])}",
    f"NTSTEP_BETWEEN_OUTPUT_ENERGY    = {cfg['display']['ntstep_between_output_energy']}",
    f"COMPUTE_INTEGRATED_ENERGY_FIELD = {bool_to_fortran(cfg['display']['compute_integrated_energy_field'])}",
    "",
    "# Snapshots",
    f"NTSTEP_BETWEEN_OUTPUT_IMAGES    = {cfg['snapshots']['ntstep_between_output_images']}",
    f"cutsnaps                        = {format_value(cfg['snapshots']['cutsnaps'])}",
    f"output_color_image              = {bool_to_fortran(cfg['snapshots']['output_color_image'])}",
    f"imagetype_JPEG                  = {cfg['snapshots']['imagetype_jpeg']}",
    f"factor_subsample_image          = {format_value(cfg['snapshots']['factor_subsample_image'])}",
    f"USE_CONSTANT_MAX_AMPLITUDE      = {bool_to_fortran(cfg['snapshots']['use_constant_max_amplitude'])}",
    f"CONSTANT_MAX_AMPLITUDE_TO_USE   = {format_value(cfg['snapshots']['constant_max_amplitude_to_use'])}",
    f"POWER_DISPLAY_COLOR             = {format_value(cfg['snapshots']['power_display_color'])}",
    f"DRAW_SOURCES_AND_RECEIVERS      = {bool_to_fortran(cfg['snapshots']['draw_sources_and_receivers'])}",
    f"DRAW_WATER_IN_BLUE              = {bool_to_fortran(cfg['snapshots']['draw_water_in_blue'])}",
    f"USE_SNAPSHOT_NUMBER_IN_FILENAME = {bool_to_fortran(cfg['snapshots']['use_snapshot_number_in_filename'])}",
    "",
    "# PostScript",
    f"output_postscript_snapshot      = {bool_to_fortran(cfg['postscript']['output_postscript_snapshot'])}",
    f"imagetype_postscript            = {cfg['postscript']['imagetype_postscript']}",
    f"meshvect                        = {bool_to_fortran(cfg['postscript']['meshvect'])}",
    f"modelvect                       = {bool_to_fortran(cfg['postscript']['modelvect'])}",
    f"boundvect                       = {bool_to_fortran(cfg['postscript']['boundvect'])}",
    f"interpol                        = {bool_to_fortran(cfg['postscript']['interpol'])}",
    f"pointsdisp                      = {cfg['postscript']['pointsdisp']}",
    f"subsamp_postscript              = {cfg['postscript']['subsamp_postscript']}",
    f"sizemax_arrows                  = {format_value(cfg['postscript']['sizemax_arrows'])}",
    f"US_LETTER                       = {bool_to_fortran(cfg['postscript']['us_letter'])}",
    "",
    "# Wavefield dumps",
    f"output_wavefield_dumps          = {bool_to_fortran(cfg['wavefield']['output_wavefield_dumps'])}",
    f"imagetype_wavefield_dumps       = {cfg['wavefield']['imagetype_wavefield_dumps']}",
    f"use_binary_for_wavefield_dumps  = {bool_to_fortran(cfg['wavefield']['use_binary_for_wavefield_dumps'])}",
    "",
    "#-----------------------------------------------------------",
    "# Parallel & GPU",
    "#-----------------------------------------------------------",
    "",
    f"NUMBER_OF_SIMULTANEOUS_RUNS     = {cfg['parallel']['number_of_simultaneous_runs']}",
    f"BROADCAST_SAME_MESH_AND_MODEL   = {bool_to_fortran(cfg['parallel']['broadcast_same_mesh_and_model'])}",
    f"GPU_MODE                        = {bool_to_fortran(cfg['parallel']['gpu_mode'])}",
])

# Write Par_file
with open(par_file_path, 'w') as f:
    f.write("\n".join(par_lines))

print(f"✓ Par_file created successfully at: {par_file_path}")
print(f"  File size: {par_file_path.stat().st_size} bytes")

os.chdir(original_dir)
