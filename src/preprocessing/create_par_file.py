#!/usr/bin/env python
"""
SPECFEM2D Complete Parameter File Generator

This script creates and manages the Par_file for SPECFEM2D simulations.
All parameters from the original Par_file are included.
"""

import os
from pathlib import Path

# ==============================================================================
# Define the output directory
# ==============================================================================
output_dir = Path('par_files')
output_dir.mkdir(exist_ok=True)
par_file_path = output_dir / 'Par_file'
print(f"Par_file will be created at: {par_file_path}")

# ==============================================================================
# Simulation & Time Parameters
# ==============================================================================
title = "model to create training the neural network"
SIMULATION_TYPE = 1  # 1=forward, 2=adjoint, 3=both
NOISE_TOMOGRAPHY = 0  # 0=regular, 1/2/3=noise simulation
SAVE_FORWARD = False
NPROC = 1  # number of processes

# Time step parameters
NSTEP = 500  # total number of time steps
DT = 1.18e-5  # duration of a time step
time_stepping_scheme = 1  # 1=Newmark, 2=LDDRK4-6, 3=classical RK4

# Wave type
P_SV = True  # True=P-SV, False=SH/membrane
AXISYM = False  # True=axisymmetric (2.5D), False=Cartesian (2D)

print("✓ Simulation parameters set")

# ==============================================================================
# Mesh & Attenuation Parameters
# ==============================================================================
# Mesh parameters
PARTITIONING_TYPE = 3  # 3=SCOTCH, 1=ascending order
NGNOD = 4  # number of control nodes per element (4 or 9)
setup_with_binary_database = 0  # 0=no, 1=create, 2=read
MODEL = "default"
SAVE_MODEL = "default"

# Attenuation parameters
ATTENUATION_VISCOELASTIC = False
ATTENUATION_VISCOACOUSTIC = False
N_SLS = 3
ATTENUATION_f0_REFERENCE = 5.196
READ_VELOCITIES_AT_f0 = False
USE_SOLVOPT = False
ATTENUATION_PORO_FLUID_PART = False
Q0_poroelastic = 1
freq0_poroelastic = 10
UNDO_ATTENUATION_AND_OR_PML = False
NT_DUMP_ATTENUATION = 100
NO_BACKWARD_RECONSTRUCTION = False

# Electromagnetic attenuation (tryout parameters)
ATTENUATION_PERMITTIVITY = False
ATTENUATION_CONDUCTIVITY = False
f0_electromagnetic = 1000

print("✓ Mesh and attenuation parameters set")

# ==============================================================================
# Source Parameters
# ==============================================================================
# Source parameters
NSOURCES = 1
force_normal_to_surface = False
initialfield = False
add_Bielak_conditions_bottom = False
add_Bielak_conditions_right = False
add_Bielak_conditions_top = False
add_Bielak_conditions_left = False
ACOUSTIC_FORCING = False
noise_source_time_function_type = 4  # 0-4 types available
write_moving_sources_database = False

print("✓ Source parameters set")

# ==============================================================================
# Receiver Parameters
# ==============================================================================
# Receiver/station parameters
seismotype = 4  # 1=displ, 2=veloc, 3=accel, 4=pressure, 5=curl of displ, 6=fluid potential
NTSTEP_BETWEEN_OUTPUT_SEISMOS = 200
NTSTEP_BETWEEN_OUTPUT_SAMPLE = 1
USE_TRICK_FOR_BETTER_PRESSURE = False
USER_T0 = 0.0
save_ASCII_seismograms = True
save_binary_seismograms_single = True
save_binary_seismograms_double = False
SU_FORMAT = False
use_existing_STATIONS = False
nreceiversets = 1
anglerec = 0.0
rec_normal_to_surface = False

# Receiver set 1
nrec = 100  # number of receivers
xdeb = 50.0  # first receiver x
zdeb = 78.0  # first receiver z
xfin = 151.0  # last receiver x
zfin = 78.0  # last receiver z
record_at_surface_same_vertical = False

print("✓ Receiver parameters set")

# ==============================================================================
# Kernel & Boundary Condition Parameters
# ==============================================================================
# Adjoint kernel outputs
save_ASCII_kernels = True
NTSTEP_BETWEEN_COMPUTE_KERNELS = 1
APPROXIMATE_HESS_KL = False

# Boundary conditions - PML
PML_BOUNDARY_CONDITIONS = False
NELEM_PML_THICKNESS = 1
ROTATE_PML_ACTIVATE = False
ROTATE_PML_ANGLE = 30.0
K_MIN_PML = 1.0
K_MAX_PML = 1.0
damping_change_factor_acoustic = 0.5
damping_change_factor_elastic = 1.0
PML_PARAMETER_ADJUSTMENT = False

# Boundary conditions - Stacey and periodic
STACEY_ABSORBING_CONDITIONS = True
ADD_PERIODIC_CONDITIONS = False
PERIODIC_HORIZ_DIST = 30.0

print("✓ Kernel and boundary condition parameters set")

# ==============================================================================
# Velocity Model & Meshing Parameters
# ==============================================================================
# Velocity and density models
nbmodels = 3
# Model definitions: [model_number, rho, Vp, Vs, ...]
models = [
    [1, 1, 1000.0, 1500.0, 0.0, 0, 0, 9999, 9999, 0, 0, 0, 0, 0, 0],
    [2, 1, 1200.0, 1700.0, 200.0, 0, 0, 9999, 9999, 0, 0, 0, 0, 0, 0],
    [3, 1, 1800.0, 1900.0, 400.0, 0, 0, 9999, 9999, 0, 0, 0, 0, 0, 0]
]
TOMOGRAPHY_FILE = "dummy"
read_external_mesh = True  # True=use external mesh, False=use internal mesher

print(f"✓ Velocity model parameters set ({nbmodels} models)")

# ==============================================================================
# External Mesh Files
# ==============================================================================
# External mesh files
mesh_file = "MESH/Mesh_model_01"
nodes_coords_file = "MESH/Nodes_model_01"
materials_file = "MESH/Material_model_01"
free_surface_file = "MESH/Surf_free_model_01"
axial_elements_file = "dummy"
absorbing_surface_file = "MESH/Surf_abs_model_01"
acoustic_forcing_surface_file = "dummy"
absorbing_cpml_file = "dummy"
tangential_detection_curve_file = "dummy"

print("✓ External mesh file parameters set")

# ==============================================================================
# Internal Mesh Parameters
# ==============================================================================
# Internal mesh parameters (used if read_external_mesh=False)
interfacesfile = "dummy"
xmin = 0.0
xmax = 4000.0
nx = 100  # number of elements along X

# Absorbing boundaries
absorbbottom = True
absorbright = True
absorbtop = False
absorbleft = True

# Mesh regions
nbregions = 1
# Format: nxmin nxmax nzmin nzmax material_number
regions = [[1, 100, 1, 60, 1]]

print("✓ Internal mesh parameters set")

# ==============================================================================
# Display & Output Parameters
# ==============================================================================
# Display parameters
NTSTEP_BETWEEN_OUTPUT_INFO = 200
output_grid_Gnuplot = False
output_grid_ASCII = True
OUTPUT_ENERGY = False
NTSTEP_BETWEEN_OUTPUT_ENERGY = 200
COMPUTE_INTEGRATED_ENERGY_FIELD = False

# Image/snapshot parameters
NTSTEP_BETWEEN_OUTPUT_IMAGES = 200
cutsnaps = 1.0
output_color_image = True
imagetype_JPEG = 10  # 1-10 types available
factor_subsample_image = 1.0
USE_CONSTANT_MAX_AMPLITUDE = False
CONSTANT_MAX_AMPLITUDE_TO_USE = 1.17e4
POWER_DISPLAY_COLOR = 0.30
DRAW_SOURCES_AND_RECEIVERS = True
DRAW_WATER_IN_BLUE = True
USE_SNAPSHOT_NUMBER_IN_FILENAME = False

# PostScript snapshots
output_postscript_snapshot = False
imagetype_postscript = 1
meshvect = True
modelvect = False
boundvect = True
interpol = True
pointsdisp = 6
subsamp_postscript = 1
sizemax_arrows = 1.0
US_LETTER = False

# Wavefield dumps
output_wavefield_dumps = False
imagetype_wavefield_dumps = 2
use_binary_for_wavefield_dumps = False

print("✓ Display and output parameters set")

# ==============================================================================
# Parallel & GPU Parameters
# ==============================================================================
# Parallel simulation parameters
NUMBER_OF_SIMULTANEOUS_RUNS = 1
BROADCAST_SAME_MESH_AND_MODEL = True

# GPU mode
GPU_MODE = False

print("✓ Parallel and GPU parameters set")

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
        # Use d notation for Fortran double precision
        if value == int(value):
            return f"{int(value)}.d0"
        else:
            return f"{value:.10e}".replace('e', 'd')
    return str(value)

# ==============================================================================
# Generate Par_file Content
# ==============================================================================

# Build the Par_file content
par_lines = [
    "#-----------------------------------------------------------",
    "#",
    "# Simulation input parameters",
    "#",
    "#-----------------------------------------------------------",
    "",
    "# title of job",
    f"title                           = {title}",
    "",
    "# forward or adjoint simulation",
    "# 1 = forward, 2 = adjoint, 3 = both simultaneously",
    "# note: 2 is purposely UNUSED (for compatibility with the numbering of our 3D codes)",
    f"SIMULATION_TYPE                 = {SIMULATION_TYPE}",
    "# 0 = regular wave propagation simulation, 1/2/3 = noise simulation",
    f"NOISE_TOMOGRAPHY                = {NOISE_TOMOGRAPHY}",
    "# save the last frame, needed for adjoint simulation",
    f"SAVE_FORWARD                    = {bool_to_fortran(SAVE_FORWARD)}",
    "",
    "# parameters concerning partitioning",
    f"NPROC                           = {NPROC}              # number of processes",
    "",
    "# time step parameters",
    "# total number of time steps",
    f"NSTEP                           = {NSTEP}",
    "",
    "# duration of a time step (see section \"How to choose the time step\" of the manual for how to do this)",
    f"DT                              = {format_value(DT)}",
    "",
    "# time stepping",
    "# 1 = Newmark (2nd order), 2 = LDDRK4-6 (4th-order 6-stage low storage Runge-Kutta), 3 = classical RK4 4th-order 4-stage Runge-Kutta",
    f"time_stepping_scheme            = {time_stepping_scheme}",
    "",
    "# set the type of calculation (P-SV or SH/membrane waves)",
    f"P_SV                            = {bool_to_fortran(P_SV)}",
    "",
    "# axisymmetric (2.5D) or Cartesian planar (2D) simulation",
    f"AXISYM                          = {bool_to_fortran(AXISYM)}",
    "",
    "#-----------------------------------------------------------",
    "#",
    "# Mesh",
    "#",
    "#-----------------------------------------------------------",
    "",
    "# Partitioning algorithm for decompose_mesh",
    f"PARTITIONING_TYPE               = {PARTITIONING_TYPE}              # SCOTCH = 3, ascending order (very bad idea) = 1",
    "",
    "# number of control nodes per element (4 or 9)",
    f"NGNOD                           = {NGNOD}",
    "",
    "# creates/reads a binary database that allows to skip all time consuming setup steps in initialization",
    "# 0 = does not read/create database",
    "# 1 = creates database",
    "# 2 = reads database",
    f"setup_with_binary_database      = {setup_with_binary_database}",
    "",
    "# available models",
    "#   default       - define model using nbmodels below",
    "#   ascii         - read model from ascii database file",
    "#   binary        - read model from binary databse file",
    "#   binary_voigt  - read Voigt model from binary database file",
    "#   external      - define model using define_external_model subroutine",
    "#   gll           - read GLL model from binary database file",
    "#   legacy        - read model from model_velocity.dat_input",
    f"MODEL                           = {MODEL}",
    "",
    "# Output the model with the requested type, does not save if turn to default or .false.",
    "# (available output formats: ascii,binary,gll,legacy)",
    f"SAVE_MODEL                      = {SAVE_MODEL}",
    "",
    "",
    "#-----------------------------------------------------------",
    "#",
    "# Attenuation",
    "#",
    "#-----------------------------------------------------------",
    "",
    "# attenuation parameters",
    f"ATTENUATION_VISCOELASTIC        = {bool_to_fortran(ATTENUATION_VISCOELASTIC)}        # turn attenuation (viscoelasticity) on or off for non-poroelastic solid parts of the model",
    f"ATTENUATION_VISCOACOUSTIC       = {bool_to_fortran(ATTENUATION_VISCOACOUSTIC)}        # turn attenuation (viscoacousticity) on or off for non-poroelastic fluid parts of the model",
    "",
    "# for viscoelastic or viscoacoustic attenuation",
    f"N_SLS                           = {N_SLS}              # number of standard linear solids for attenuation (3 is usually the minimum)",
    f"ATTENUATION_f0_REFERENCE        = {ATTENUATION_f0_REFERENCE}          # in case of attenuation, reference frequency in Hz at which the velocity values in the velocity model are given (unused otherwise); relevant only if source is a Dirac or a Heaviside, otherwise it is automatically set to f0 the dominant frequency of the source in the DATA/SOURCE file",
    f"READ_VELOCITIES_AT_f0           = {bool_to_fortran(READ_VELOCITIES_AT_f0)}        # read seismic velocities at ATTENUATION_f0_REFERENCE instead of at infinite frequency (see user manual for more information)",
    f"USE_SOLVOPT                     = {bool_to_fortran(USE_SOLVOPT)}        # use more precise but much more expensive way of determining the Q factor relaxation times, as in https://doi.org/10.1093/gji/ggw024",
    "",
    "# for poroelastic attenuation",
    f"ATTENUATION_PORO_FLUID_PART     = {bool_to_fortran(ATTENUATION_PORO_FLUID_PART)}        # turn viscous attenuation on or off for the fluid part of poroelastic parts of the model",
    f"Q0_poroelastic                  = {Q0_poroelastic}              # quality factor for viscous attenuation (ignore it if you are not using a poroelastic material)",
    f"freq0_poroelastic               = {freq0_poroelastic}             # frequency for viscous attenuation (ignore it if you are not using a poroelastic material)",
    "",
    "# to undo attenuation and/or PMLs for sensitivity kernel calculations or forward runs with SAVE_FORWARD",
    "# use the flag below. It performs undoing of attenuation and/or of PMLs in an exact way for sensitivity kernel calculations",
    "# but requires disk space for temporary storage, and uses a significant amount of memory used as buffers for temporary storage.",
    "# When that option is on the second parameter indicates how often the code dumps restart files to disk (if in doubt, use something between 100 and 1000).",
    f"UNDO_ATTENUATION_AND_OR_PML     = {bool_to_fortran(UNDO_ATTENUATION_AND_OR_PML)}",
    f"NT_DUMP_ATTENUATION             = {NT_DUMP_ATTENUATION}",
    "",
    "# Instead of reconstructing the forward wavefield, this option reads it from the disk using asynchronous I/O.",
    "# Outperforms conventional mode using a value of NTSTEP_BETWEEN_COMPUTE_KERNELS high enough.",
    f"NO_BACKWARD_RECONSTRUCTION      = {bool_to_fortran(NO_BACKWARD_RECONSTRUCTION)}",
    "",
    "# below three parameters added as tryout`",
    f"ATTENUATION_PERMITTIVITY        = {bool_to_fortran(ATTENUATION_PERMITTIVITY)}",
    "",
    f"ATTENUATION_CONDUCTIVITY       = {bool_to_fortran(ATTENUATION_CONDUCTIVITY)}",
    "",
    f"f0_electromagnetic                  = {f0_electromagnetic}",
    "",
    "#-----------------------------------------------------------",
    "#",
    "# Sources",
    "#",
    "#-----------------------------------------------------------",
    "",
    "# source parameters",
    f"NSOURCES                        = {NSOURCES}              # number of sources (source information is then read from the DATA/SOURCE file)",
    f"force_normal_to_surface         = {bool_to_fortran(force_normal_to_surface)}        # angleforce normal to surface (external mesh and curve file needed)",
    "",
    "# use an existing initial wave field as source or start from zero (medium initially at rest)",
    f"initialfield                    = {bool_to_fortran(initialfield)}",
    f"add_Bielak_conditions_bottom    = {bool_to_fortran(add_Bielak_conditions_bottom)}        # add Bielak conditions or not if initial plane wave",
    f"add_Bielak_conditions_right     = {bool_to_fortran(add_Bielak_conditions_right)}",
    f"add_Bielak_conditions_top       = {bool_to_fortran(add_Bielak_conditions_top)}",
    f"add_Bielak_conditions_left      = {bool_to_fortran(add_Bielak_conditions_left)}",
    "",
    "# acoustic forcing",
    f"ACOUSTIC_FORCING                = {bool_to_fortran(ACOUSTIC_FORCING)}        # acoustic forcing of an acoustic medium with a rigid interface",
    "",
    "# noise simulations - type of noise source time function:",
    "# 0=external (S_squared), 1=Ricker(second derivative), 2=Ricker(first derivative), 3=Gaussian, 4=Figure 2a of Tromp et al. 2010",
    "# (default value 4 is chosen to reproduce the time function from Fig 2a of \"Tromp et al., 2010, Noise Cross-Correlation Sensitivity Kernels\")",
    f"noise_source_time_function_type = {noise_source_time_function_type}",
    "",
    "# moving sources",
    "# Set write_moving_sources_database to .true. if the generation of moving source databases takes",
    "# a long time. Then the simulation is done in two steps: first you run the code and it writes the databases to file",
    "# (in DATA folder by default). Then you rerun the code and it will read the databases in there directly possibly",
    "# saving a lot of time.",
    "# This is only useful for GPU version (for now)",
    f"write_moving_sources_database   = {bool_to_fortran(write_moving_sources_database)}",
    "",
    "#-----------------------------------------------------------",
    "#",
    "# Receivers",
    "#",
    "#-----------------------------------------------------------",
    "",
    "# receiver set parameters for recording stations (i.e. recording points)",
    "# seismotype : record 1=displ 2=veloc 3=accel 4=pressure 5=curl of displ 6=the fluid potential",
    f"seismotype                      = {seismotype}              # several values can be chosen. For example : 1,2,4",
    "",
    "",
    "# subsampling of the seismograms to create smaller files (but less accurately sampled in time)",
    "#subsamp_seismos                 = 1",
    "",
    "# interval in time steps for writing of seismograms",
    "# every how many time steps we save the seismograms",
    "# (costly, do not use a very small value; if you use a very large value that is larger than the total number",
    "#  of time steps of the run, the seismograms will automatically be saved once at the end of the run anyway)",
    f"NTSTEP_BETWEEN_OUTPUT_SEISMOS   = {NTSTEP_BETWEEN_OUTPUT_SEISMOS}",
    "",
    "# set to n to reduce the sampling rate of output seismograms by a factor of n",
    "# defaults to 1, which means no down-sampling",
    f"NTSTEP_BETWEEN_OUTPUT_SAMPLE    = {NTSTEP_BETWEEN_OUTPUT_SAMPLE}",
    "",
    "# so far, this option can only be used if all the receivers are in acoustic elements",
    f"USE_TRICK_FOR_BETTER_PRESSURE   = {bool_to_fortran(USE_TRICK_FOR_BETTER_PRESSURE)}",
    "",
    "# use this t0 as earliest starting time rather than the automatically calculated one",
    f"USER_T0                         = {format_value(USER_T0)}",
    "",
    "# seismogram formats",
    f"save_ASCII_seismograms          = {bool_to_fortran(save_ASCII_seismograms)}         # save seismograms in ASCII format or not",
    f"save_binary_seismograms_single  = {bool_to_fortran(save_binary_seismograms_single)}         # save seismograms in single precision binary format or not (can be used jointly with ASCII above to save both)",
    f"save_binary_seismograms_double  = {bool_to_fortran(save_binary_seismograms_double)}        # save seismograms in double precision binary format or not (can be used jointly with both flags above to save all)",
    f"SU_FORMAT                       = {bool_to_fortran(SU_FORMAT)}        # output single precision binary seismograms in Seismic Unix format (adjoint traces will be read in the same format)",
    "",
    "# use an existing STATION file found in ./DATA or create a new one from the receiver positions below in this Par_file",
    f"use_existing_STATIONS           = {bool_to_fortran(use_existing_STATIONS)}",
    "",
    "# number of receiver sets (i.e. number of receiver lines to create below)",
    f"nreceiversets                   = {nreceiversets}",
    "",
    "# orientation",
    f"anglerec                        = {format_value(anglerec)}          # angle to rotate components at receivers",
    f"rec_normal_to_surface           = {bool_to_fortran(rec_normal_to_surface)}        # base anglerec normal to surface (external mesh and curve file needed)",
    "",
    "# first receiver set (repeat these 6 lines and adjust nreceiversets accordingly)",
    f"nrec                            = {nrec}             # number of receivers",
    f"xdeb                            = {format_value(xdeb)}           # first receiver x in meters",
    f"zdeb                            = {format_value(zdeb)}          # first receiver z in meters",
    f"xfin                            = {format_value(xfin)}          # last receiver x in meters (ignored if only one receiver)",
    f"zfin                            = {format_value(zfin)}          # last receiver z in meters (ignored if only one receiver)",
    f"record_at_surface_same_vertical = {bool_to_fortran(record_at_surface_same_vertical)}       # receivers inside the medium or at the surface (z values are ignored if this is set to true, they are replaced with the topography height)",
    "",
    "",
    "#-----------------------------------------------------------",
    "#",
    "# adjoint kernel outputs",
    "#",
    "#-----------------------------------------------------------",
    "",
    "# save sensitivity kernels in ASCII format (much bigger files, but compatible with current GMT scripts) or in binary format",
    f"save_ASCII_kernels              = {bool_to_fortran(save_ASCII_kernels)}",
    "",
    "# since the accuracy of kernel integration may not need to respect the CFL, this option permits to save computing time, and memory with UNDO_ATTENUATION_AND_OR_PML mode",
    f"NTSTEP_BETWEEN_COMPUTE_KERNELS  = {NTSTEP_BETWEEN_COMPUTE_KERNELS}",
    "",
    "# outputs approximate Hessian for preconditioning",
    f"APPROXIMATE_HESS_KL             = {bool_to_fortran(APPROXIMATE_HESS_KL)}",
    "",
    "#-----------------------------------------------------------",
    "#",
    "# Boundary conditions",
    "#",
    "#-----------------------------------------------------------",
    "",
    "# Perfectly Matched Layer (PML) boundaries",
    "# absorbing boundary active or not",
    f"PML_BOUNDARY_CONDITIONS         = {bool_to_fortran(PML_BOUNDARY_CONDITIONS)}",
    f"NELEM_PML_THICKNESS             = {NELEM_PML_THICKNESS}",
    f"ROTATE_PML_ACTIVATE             = {bool_to_fortran(ROTATE_PML_ACTIVATE)}",
    f"ROTATE_PML_ANGLE                = {format_value(ROTATE_PML_ANGLE)}",
    "# change the four parameters below only if you know what you are doing; they change the damping profiles inside the PMLs",
    f"K_MIN_PML                       = {format_value(K_MIN_PML)}          # from Gedney page 8.11",
    f"K_MAX_PML                       = {format_value(K_MAX_PML)}",
    f"damping_change_factor_acoustic  = {format_value(damping_change_factor_acoustic)}",
    f"damping_change_factor_elastic   = {format_value(damping_change_factor_elastic)}",
    "# set the parameter below to .false. unless you know what you are doing; this implements automatic adjustment of the PML parameters for elongated models.",
    "# The goal is to improve the absorbing efficiency of PML for waves with large incidence angles, but this can lead to artefacts.",
    "# In particular, this option is efficient only when the number of sources NSOURCES is equal to one.",
    f"PML_PARAMETER_ADJUSTMENT        = {bool_to_fortran(PML_PARAMETER_ADJUSTMENT)}",
    "",
    "# Stacey ABC",
    f"STACEY_ABSORBING_CONDITIONS     = {bool_to_fortran(STACEY_ABSORBING_CONDITIONS)}",
    "",
    "# periodic boundaries",
    f"ADD_PERIODIC_CONDITIONS         = {bool_to_fortran(ADD_PERIODIC_CONDITIONS)}",
    f"PERIODIC_HORIZ_DIST             = {format_value(PERIODIC_HORIZ_DIST)}",
    "",
    "#-----------------------------------------------------------",
    "#",
    "# Velocity and density models",
    "#",
    "#-----------------------------------------------------------",
    "",
    "# number of model materials",
    f"nbmodels                        = {nbmodels}",
    "# available material types (see user manual for more information)",
    "#   acoustic:              model_number 1 rho Vp 0  0 0 QKappa 9999 0 0 0 0 0 0 (for QKappa use 9999 to ignore it)",
    "#   elastic:               model_number 1 rho Vp Vs 0 0 QKappa Qmu  0 0 0 0 0 0 (for QKappa and Qmu use 9999 to ignore them)",
    "#   anisotropic:           model_number 2 rho c11 c13 c15 c33 c35 c55 c12 c23 c25   0 QKappa Qmu",
    "#   anisotropic in AXISYM: model_number 2 rho c11 c13 c15 c33 c35 c55 c12 c23 c25 c22 QKappa Qmu",
    "#   poroelastic:           model_number 3 rhos rhof phi c kxx kxz kzz Ks Kf Kfr etaf mufr Qmu",
    "#   tomo:                  model_number -1 0 0 A 0 0 0 0 0 0 0 0 0 0",
    "#",
    "# note: When viscoelasticity or viscoacousticity is turned on,",
    "#       the Vp and Vs values that are read here are the UNRELAXED ones i.e. the values at infinite frequency",
    "#       unless the READ_VELOCITIES_AT_f0 parameter above is set to true, in which case they are the values at frequency f0.",
    "#",
    "#       Please also note that Qmu is always equal to Qs, but Qkappa is in general not equal to Qp.",
    "#       To convert one to the other see doc/Qkappa_Qmu_versus_Qp_Qs_relationship_in_2D_plane_strain.pdf and",
    "#       utils/attenuation/conversion_from_Qkappa_Qmu_to_Qp_Qs_from_Dahlen_Tromp_959_960.f90.",
]

# Add model definitions
for model in models:
    model_line = " ".join(str(m) for m in model)
    par_lines.append(model_line)

par_lines.extend([
    "# external tomography file",
    f"TOMOGRAPHY_FILE                 = {TOMOGRAPHY_FILE}",
    "",
    "# use an external mesh created by an external meshing tool or use the internal mesher",
    f"read_external_mesh              = {bool_to_fortran(read_external_mesh)}",
    "",
    "#-----------------------------------------------------------",
    "#",
    "# PARAMETERS FOR EXTERNAL MESHING",
    "#",
    "#-----------------------------------------------------------",
    "",
    "# data concerning mesh, when generated using third-party app (more info in README)",
    "# (see also absorbing_conditions above)",
    "",
    f"mesh_file                       = {mesh_file}         # file containing the mesh",
    f"nodes_coords_file               = {nodes_coords_file}        # file containing the nodes coordinates",
    f"materials_file                  = {materials_file}     # file containing the material number for each element",
    f"free_surface_file               = {free_surface_file}    # file containing the free surface",
    f"axial_elements_file             = {axial_elements_file}                             # file containing the axial elements if AXISYM is true",
    f"absorbing_surface_file          = {absorbing_surface_file}     # file containing the absorbing surface",
    f"acoustic_forcing_surface_file   = {acoustic_forcing_surface_file}                             # file containing the acoustic forcing surface",
    f"absorbing_cpml_file             = {absorbing_cpml_file}                             # file containing the CPML element numbers",
    f"tangential_detection_curve_file = {tangential_detection_curve_file}                             # file containing the curve delimiting the velocity model",
    "",
    "#-----------------------------------------------------------",
    "#",
    "# PARAMETERS FOR INTERNAL MESHING",
    "#",
    "#-----------------------------------------------------------",
    "",
    "# file containing interfaces for internal mesh",
    f"interfacesfile                  = {interfacesfile}",
    "",
    "# geometry of the model (origin lower-left corner = 0,0) and mesh description",
    f"xmin                            = {format_value(xmin)}           # abscissa of left side of the model",
    f"xmax                            = {format_value(xmax)}        # abscissa of right side of the model",
    f"nx                              = {nx}            # number of elements along X",
    "",
    "# absorbing boundary parameters (see absorbing_conditions above)",
    f"absorbbottom                    = {bool_to_fortran(absorbbottom)}",
    f"absorbright                     = {bool_to_fortran(absorbright)}",
    f"absorbtop                       = {bool_to_fortran(absorbtop)}",
    f"absorbleft                      = {bool_to_fortran(absorbleft)}",
    "",
    "# define the different regions of the model in the (nx,nz) spectral-element mesh",
    f"nbregions                       = {nbregions}              # then set below the different regions and model number for each region",
    "# format of each line: nxmin nxmax nzmin nzmax material_number",
])

# Add region definitions
for region in regions:
    region_line = " ".join(str(r) for r in region)
    par_lines.append(region_line)

par_lines.extend([
    "",
    "#-----------------------------------------------------------",
    "#",
    "# Display parameters",
    "#",
    "#-----------------------------------------------------------",
    "",
    "# interval at which we output time step info and max of norm of displacement",
    "# (every how many time steps we display information about the simulation. costly, do not use a very small value)",
    f"NTSTEP_BETWEEN_OUTPUT_INFO      = {NTSTEP_BETWEEN_OUTPUT_INFO}",
    "",
    "# meshing output",
    f"output_grid_Gnuplot             = {bool_to_fortran(output_grid_Gnuplot)}        # generate a GNUPLOT file containing the grid, and a script to plot it",
    f"output_grid_ASCII               = {bool_to_fortran(output_grid_ASCII)}        # dump the grid in an ASCII text file consisting of a set of X,Y,Z points or not",
    "",
    "# to plot total energy curves, for instance to monitor how CPML absorbing layers behave;",
    "# should be turned OFF in most cases because a bit expensive",
    f"OUTPUT_ENERGY                   = {bool_to_fortran(OUTPUT_ENERGY)}",
    "",
    "# every how many time steps we compute energy (which is a bit expensive to compute)",
    f"NTSTEP_BETWEEN_OUTPUT_ENERGY    = {NTSTEP_BETWEEN_OUTPUT_ENERGY}",
    "",
    "# Compute the field int_0^t v^2 dt for a set of GLL points and write it to file. Use",
    "# the script utils/visualisation/plotIntegratedEnergyFile.py to watch. It is refreshed at the same time than the seismograms",
    f"COMPUTE_INTEGRATED_ENERGY_FIELD = {bool_to_fortran(COMPUTE_INTEGRATED_ENERGY_FIELD)}",
    "",
    "#-----------------------------------------------------------",
    "#",
    "# Movies/images/snaphots visualizations",
    "#",
    "#-----------------------------------------------------------",
    "",
    "# every how many time steps we draw JPEG or PostScript pictures of the simulation",
    "# and/or we dump results of the simulation as ASCII or binary files (costly, do not use a very small value)",
    f"NTSTEP_BETWEEN_OUTPUT_IMAGES    = {NTSTEP_BETWEEN_OUTPUT_IMAGES}",
    "",
    "# minimum amplitude kept in % for the JPEG and PostScript snapshots; amplitudes below that are muted",
    f"cutsnaps                        = {format_value(cutsnaps)}",
    "",
    "#### for JPEG color images ####",
    f"output_color_image              = {bool_to_fortran(output_color_image)}         # output JPEG color image of the results every NTSTEP_BETWEEN_OUTPUT_IMAGES time steps or not",
    f"imagetype_JPEG                  = {imagetype_JPEG}              # display 1=displ_Ux 2=displ_Uz 3=displ_norm 4=veloc_Vx 5=veloc_Vz 6=veloc_norm 7=accel_Ax 8=accel_Az 9=accel_norm 10=pressure",
    f"factor_subsample_image          = {format_value(factor_subsample_image)}          # (double precision) factor to subsample or oversample (if set to e.g. 0.5) color images output by the code (useful for very large models, or to get nicer looking denser pictures)",
    f"USE_CONSTANT_MAX_AMPLITUDE      = {bool_to_fortran(USE_CONSTANT_MAX_AMPLITUDE)}        # by default the code normalizes each image independently to its maximum; use this option to use the global maximum below instead",
    f"CONSTANT_MAX_AMPLITUDE_TO_USE   = {format_value(CONSTANT_MAX_AMPLITUDE_TO_USE)}         # constant maximum amplitude to use for all color images if the above USE_CONSTANT_MAX_AMPLITUDE option is true",
    f"POWER_DISPLAY_COLOR             = {format_value(POWER_DISPLAY_COLOR)}         # non linear display to enhance small amplitudes in JPEG color images",
    f"DRAW_SOURCES_AND_RECEIVERS      = {bool_to_fortran(DRAW_SOURCES_AND_RECEIVERS)}         # display sources as orange crosses and receivers as green squares in JPEG images or not",
    f"DRAW_WATER_IN_BLUE              = {bool_to_fortran(DRAW_WATER_IN_BLUE)}         # display acoustic layers as constant blue in JPEG images, because they likely correspond to water in the case of ocean acoustics or in the case of offshore oil industry experiments (if off, display them as greyscale, as for elastic or poroelastic elements, for instance for acoustic-only oil industry models of solid media)",
    f"USE_SNAPSHOT_NUMBER_IN_FILENAME = {bool_to_fortran(USE_SNAPSHOT_NUMBER_IN_FILENAME)}        # use snapshot number in the file name of JPEG color snapshots instead of the time step (for instance to create movies in an easier way later)",
    "",
    "#### for PostScript snapshots ####",
    f"output_postscript_snapshot      = {bool_to_fortran(output_postscript_snapshot)}         # output Postscript snapshot of the results every NTSTEP_BETWEEN_OUTPUT_IMAGES time steps or not",
    f"imagetype_postscript            = {imagetype_postscript}              # display 1=displ vector 2=veloc vector 3=accel vector; small arrows are displayed for the vectors",
    f"meshvect                        = {bool_to_fortran(meshvect)}         # display mesh on PostScript plots or not",
    f"modelvect                       = {bool_to_fortran(modelvect)}        # display velocity model on PostScript plots or not",
    f"boundvect                       = {bool_to_fortran(boundvect)}         # display boundary conditions on PostScript plots or not",
    f"interpol                        = {bool_to_fortran(interpol)}         # interpolation of the PostScript display on a regular grid inside each spectral element, or use the non-evenly spaced GLL points",
    f"pointsdisp                      = {pointsdisp}              # number of points in each direction for interpolation of PostScript snapshots (set to 1 for lower-left corner only)",
    f"subsamp_postscript              = {subsamp_postscript}              # subsampling of background velocity model in PostScript snapshots",
    f"sizemax_arrows                  = {format_value(sizemax_arrows)}           # maximum size of arrows on PostScript plots in centimeters",
    f"US_LETTER                       = {bool_to_fortran(US_LETTER)}        # use US letter or European A4 paper for PostScript plots",
    "",
    "#### for wavefield dumps ####",
    f"output_wavefield_dumps          = {bool_to_fortran(output_wavefield_dumps)}        # output wave field to a text file (creates very big files)",
    f"imagetype_wavefield_dumps       = {imagetype_wavefield_dumps}              # display 1=displ vector 2=veloc vector 3=accel vector 4=pressure",
    f"use_binary_for_wavefield_dumps  = {bool_to_fortran(use_binary_for_wavefield_dumps)}        # use ASCII or single-precision binary format for the wave field dumps",
    "",
    "#-----------------------------------------------------------",
    "",
    "# Ability to run several calculations (several earthquakes)",
    "# in an embarrassingly-parallel fashion from within the same run;",
    "# this can be useful when using a very large supercomputer to compute",
    "# many earthquakes in a catalog, in which case it can be better from",
    "# a batch job submission point of view to start fewer and much larger jobs,",
    "# each of them computing several earthquakes in parallel.",
    "# To turn that option on, set parameter NUMBER_OF_SIMULTANEOUS_RUNS to a value greater than 1.",
    "# To implement that, we create NUMBER_OF_SIMULTANEOUS_RUNS MPI sub-communicators,",
    "# each of them being labeled \"my_local_mpi_comm_world\", and we use them",
    "# in all the routines in \"src/shared/parallel.f90\", except in MPI_ABORT() because in that case",
    "# we need to kill the entire run.",
    "# When that option is on, of course the number of processor cores used to start",
    "# the code in the batch system must be a multiple of NUMBER_OF_SIMULTANEOUS_RUNS,",
    "# all the individual runs must use the same number of processor cores,",
    "# which as usual is NPROC in the Par_file,",
    "# and thus the total number of processor cores to request from the batch system",
    "# should be NUMBER_OF_SIMULTANEOUS_RUNS * NPROC.",
    "# All the runs to perform must be placed in directories called run0001, run0002, run0003 and so on",
    "# (with exactly four digits).",
    "#",
    "# Imagine you have 10 independent calculations to do, each of them on 100 cores; you have three options:",
    "#",
    "# 1/ submit 10 jobs to the batch system",
    "#",
    "# 2/ submit a single job on 1000 cores to the batch, and in that script create a sub-array of jobs to start 10 jobs,",
    "# each running on 100 cores (see e.g. http://www.schedmd.com/slurmdocs/job_array.html )",
    "#",
    "# 3/ submit a single job on 1000 cores to the batch, start SPECFEM2D on 1000 cores, create 10 sub-communicators,",
    "# cd into one of 10 subdirectories (called e.g. run0001, run0002,... run0010) depending on the sub-communicator",
    "# your MPI rank belongs to, and run normally on 100 cores using that sub-communicator.",
    "#",
    "# The option below implements 3/.",
    "#",
    f"NUMBER_OF_SIMULTANEOUS_RUNS     = {NUMBER_OF_SIMULTANEOUS_RUNS}",
    "",
    "# if we perform simultaneous runs in parallel, if only the source and receivers vary between these runs",
    "# but not the mesh nor the model (velocity and density) then we can also read the mesh and model files",
    "# from a single run in the beginning and broadcast them to all the others; for a large number of simultaneous",
    "# runs for instance when solving inverse problems iteratively this can DRASTICALLY reduce I/Os to disk in the solver",
    "# (by a factor equal to NUMBER_OF_SIMULTANEOUS_RUNS), and reducing I/Os is crucial in the case of huge runs.",
    "# Thus, always set this option to .true. if the mesh and the model are the same for all simultaneous runs.",
    "# In that case there is no need to duplicate the mesh and model file database (the content of the DATABASES_MPI",
    "# directories) in each of the run0001, run0002,... directories, it is sufficient to have one in run0001",
    "# and the code will broadcast it to the others",
    f"BROADCAST_SAME_MESH_AND_MODEL   = {bool_to_fortran(BROADCAST_SAME_MESH_AND_MODEL)}",
    "",
    "#-----------------------------------------------------------",
    "",
    "# set to true to use GPUs",
    f"GPU_MODE                        = {bool_to_fortran(GPU_MODE)}",
    "",
])

par_content = "\n".join(par_lines)
print("✓ Par_file content generated")

# ==============================================================================
# Write to File
# ==============================================================================

# Write to file
with open(par_file_path, 'w') as f:
    f.write(par_content)

print(f"✓ Par_file created successfully at: {par_file_path}")
print(f"  File size: {par_file_path.stat().st_size} bytes")

# ==============================================================================
# Display Output
# ==============================================================================

# Display the generated Par_file (first 100 lines)
print("\n" + "="*80)
print("Generated Par_file (first 100 lines):")
print("="*80 + "\n")
with open(par_file_path, 'r') as f:
    lines = f.readlines()
    for i, line in enumerate(lines[:100], 1):
        print(f"{i:3d}: {line}", end='')
