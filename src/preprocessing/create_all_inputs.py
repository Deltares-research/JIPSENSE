#!/usr/bin/env python
"""
SPECFEM2D Complete Input File Generator

This master script runs all input generation scripts in sequence:
1. create_mesh.py - Generates mesh files
2. create_par_file.py - Generates Par_file
3. create_source.py - Generates SOURCE file
"""

import subprocess
import sys
from pathlib import Path

# ==============================================================================
# Setup
# ==============================================================================
scripts_dir = Path(__file__).parent
scripts = [
    ('create_mesh.py', 'Mesh generation'),
    ('create_par_file.py', 'Par_file generation'),
    ('create_source.py', 'SOURCE file generation'),
]

print("=" * 80)
print("SPECFEM2D Input File Generator")
print("=" * 80)
print()

# ==============================================================================
# Run all scripts
# ==============================================================================
failed_scripts = []

for script_name, description in scripts:
    script_path = scripts_dir / script_name
    
    if not script_path.exists():
        print(f"✗ {description}: Script not found at {script_path}")
        failed_scripts.append(script_name)
        continue
    
    print(f"\n{'='*80}")
    print(f"Running: {description}")
    print(f"{'='*80}")
    print()
    
    try:
        result = subprocess.run([sys.executable, str(script_path)], check=True)
        print()
    except subprocess.CalledProcessError as e:
        print(f"\n✗ {description} failed with exit code {e.returncode}")
        failed_scripts.append(script_name)
        continue

# ==============================================================================
# Summary
# ==============================================================================
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print()

if failed_scripts:
    print(f"✗ {len(failed_scripts)} script(s) failed:")
    for script in failed_scripts:
        print(f"  - {script}")
    sys.exit(1)
else:
    print("✓ All input files generated successfully!")
    print()
    print("Generated files:")
    print("  - MESH/: Mesh files (Mesh_*, Nodes_*, Material_*, Surf_*)")
    print("  - DATA/Par_file: SPECFEM2D parameter file")
    print("  - DATA/SOURCE: Source parameters file")
    print()

sys.exit(0)
