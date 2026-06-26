#!/usr/bin/env python3
"""
Create Mesh with PML (Perfectly Matched Layer)

This script executes the model_01.py to generate a 3-layer flat mesh with
PML (Perfectly Matched Layer) absorbing boundaries for seismic wave simulation.

The script runs the model from the data/models/ directory and generates
mesh files with appropriate PML configurations.
"""

import os
import sys
import subprocess
from pathlib import Path


def get_project_root():
    """Get the project root directory."""
    current_dir = Path(__file__).parent
    # Navigate up from src/preprocessing to project root
    return current_dir.parent.parent


def run_model_01():
    """Execute model_01.py from data/models/ directory."""
    project_root = get_project_root()
    model_script = project_root / "data" / "models" / "model_01.py"
    
    if not model_script.exists():
        raise FileNotFoundError(f"Model script not found at {model_script}")
    
    print(f"Running mesh generation with PML using: {model_script}")
    print("-" * 60)
    
    try:
        # Set up environment with proper Python path for local modules
        env = os.environ.copy()
        pythonpath = str(project_root / "src" / "preprocessing" / "from_specfem")
        if "PYTHONPATH" in env:
            env["PYTHONPATH"] = f"{pythonpath}:{env['PYTHONPATH']}"
        else:
            env["PYTHONPATH"] = pythonpath
        
        # Execute the model script using specfempp conda environment
        result = subprocess.run(
            ["conda", "run", "-n", "specfempp", "python", str(model_script)],
            cwd=str(project_root / "data" / "models"),
            env=env,
            check=True,
            capture_output=False
        )
        print("-" * 60)
        print("Mesh generation with PML completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running model_01.py: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def main():
    """Main entry point."""
    try:
        success = run_model_01()
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
