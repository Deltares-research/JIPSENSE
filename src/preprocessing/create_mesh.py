#!/usr/bin/env python3
"""
Create the absorbing and free surface files from the Gmsh file.
"""

import os
import sys
import subprocess

def main():
    """Main function to create mesh files."""
    print("processing Gmsh...")
    print()
    
    # Change to MESH directory
    os.chdir("MESH/")
    
    try:
        print("creating msh file")
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
                "../../../utils/Gmsh/LibGmsh2Specfem_convert_Gmsh_to_Specfem2D_official.py",
                "model_01.msh",
                "-t", "F",
                "-l", "A",
                "-b", "A",
                "-r", "A"
            ],
            check=True
        )
        
        os.chdir("../")
        
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
