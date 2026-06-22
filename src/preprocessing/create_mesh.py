#!/usr/bin/env python3
"""
Create the absorbing and free surface files from the Gmsh file.
"""

import os
import sys
import subprocess
import glob
import shutil

def clean_mesh_files():
    """Remove existing mesh files to ensure fresh generation."""
    mesh_patterns = [
        "*.msh",           # Gmsh mesh files
        "Mesh_*",          # SPECFEM2D mesh connectivity
        "Nodes_*",         # SPECFEM2D node coordinates
        "Material_*",      # SPECFEM2D material properties
        "Surf_*",          # SPECFEM2D surface definitions (free and absorbing)
        "*.dat",           # Data files
        "boundaries.txt"   # Legacy boundary files
    ]
    for pattern in mesh_patterns:
        for file in glob.glob(pattern):
            try:
                os.remove(file)
                print(f"  Removed: {file}")
            except OSError:
                pass

def main():
    """Main function to create mesh files."""
    print("processing Gmsh...")
    print()
    
    # Store the original directory
    original_dir = os.getcwd()
    
    # Change to MESH directory within simulation
    mesh_dir = "/home/obandohe/JIPSENSE/JIPSENSE/src/simulation/MESH"
    os.chdir(mesh_dir)
    print(f"Changed to MESH directory: {mesh_dir}")
    print()
    
    try:
        # Clean existing mesh files
        print("Cleaning existing mesh files...")
        clean_mesh_files()
        print()
        
        print("creating msh file")
        print()

        # Check if mesh source directory exists
        mesh_source_dir = "../../../data/meshes/model_01"
        if not os.path.exists(mesh_source_dir):
            print(f"Error: Source mesh directory not found at {mesh_source_dir}")
            print("Please add your Gmsh geometry files (model_01.geo, model_01.msh) to data/meshes/model_01/")
            sys.exit(1)
        
        # Copy files from data/meshes/model_01 to simulation/MESH
        for file in glob.glob(f"{mesh_source_dir}/*"):
            if os.path.isfile(file):
                shutil.copy(file, os.path.basename(file))
                print(f"  Copied: {os.path.basename(file)}")
        # check if model_01.geo and model_01.msh were copied
        if not os.path.exists("model_01.geo"):
            print("Error: model_01.geo not found in simulation/MESH")
            sys.exit(1)
        if not os.path.exists("model_01.msh"):
            print("Error: model_01.msh not found in simulation/MESH")
            sys.exit(1)
        else:
            print("✓ model_01.msh and model_01.geo copied successfully")
            print()

        
        # Create Gmsh mesh
        result = subprocess.run(
            ["gmsh", "model_01.geo", "-2", "-format", "msh22", "-o", "model_01.msh"],
            check=True
        )
        
        print()
        print("exporting to specfem mesh files")
        print()
        
        # Convert to SPECFEM format files
        result = subprocess.run(
            [
                "python",
                "/home/obandohe/specfem2d/utils/Gmsh/LibGmsh2Specfem_convert_Gmsh_to_Specfem2D_official.py",
                "model_01.msh",
                "-t", "F",
                "-l", "A",
                "-b", "A",
                "-r", "A"
            ],
            check=True
        )
        
        # Return to original directory
        os.chdir(original_dir)
        
        print()
        print("done")
        print()
        
    except subprocess.CalledProcessError as e:
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
