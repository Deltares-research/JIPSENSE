#!/bin/bash
#
# script runs mesher and solver (in serial)
# using this example setup
#

echo "running example: `date`"
currentdir=`pwd`

# Capture timestamp for output folder
timestamp=$(date +"%Y-%m-%d_%H-%M-%S")

# sets up directory structure in current example directoy
echo
echo "setting up example..."
echo

mkdir -p OUTPUT_FILES

# cleans output files
rm -rf OUTPUT_FILES/*

cd $currentdir

# links executables
mkdir -p bin
cd bin/
rm -f xmeshfem2D xspecfem2D xcheck_quality_external_mesh
ln -s /home/obandohe/specfem2d/bin/xmeshfem2D
ln -s /home/obandohe/specfem2d/bin/xspecfem2D
ln -s /home/obandohe/specfem2d/bin/xcheck_quality_external_mesh
cd ../

# stores setup
cp DATA/Par_file OUTPUT_FILES/
cp DATA/SOURCE OUTPUT_FILES/

# Get the number of processors
NPROC=`grep ^NPROC DATA/Par_file | cut -d = -f 2 | cut -d \# -f 1 | tr -d ' '`

# runs database generation
if [ "$NPROC" -eq 1 ]; then
  # This is a serial simulation
  echo
  echo "running mesher..."
  echo
  ./bin/xmeshfem2D
else
  # This is a MPI simulation
  echo
  echo "running mesher on $NPROC processors..."
  echo
  mpirun -np $NPROC ./bin/xmeshfem2D
fi
# checks exit code
if [[ $? -ne 0 ]]; then exit 1; fi

# runs simulation
if [ "$NPROC" -eq 1 ]; then
  # This is a serial simulation
  echo
  echo "running solver..."
  echo
  ./bin/xspecfem2D
else
  # This is a MPI simulation
  echo
  echo "running solver on $NPROC processors..."
  echo
  mpirun -np $NPROC ./bin/xspecfem2D
fi
# checks exit code
if [[ $? -ne 0 ]]; then exit 1; fi

# stores output
cp DATA/*SOURCE* DATA/*STATIONS* OUTPUT_FILES

# check mesh
cd bin/
rm -f xcheck_quality_external_mesh
ln -s /home/obandohe/specfem2d/bin/xcheck_quality_external_mesh
cd ../

./bin/xcheck_quality_external_mesh <<EOF
3
EOF
# checks exit code
if [[ $? -ne 0 ]]; then exit 1; fi

# Move OUTPUT_FILES to output directory with timestamp
output_dir="../../data/output"
mkdir -p "$output_dir"
timestamped_output="${output_dir}/OUTPUT_FILES_${timestamp}"
mv OUTPUT_FILES "$timestamped_output"

echo
echo "see results in directory: ${timestamped_output}/"
echo
echo "done"
echo `date`
