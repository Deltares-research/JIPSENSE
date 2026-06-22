#!/usr/bin/env python3
"""
Demo script showing generic mesh plotting capabilities.

Examples:
  - Single mesh with custom colors and material names
  - Multiple meshes comparison
  - Batch processing
"""

from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))
from utils.mesh_plotting import (
    read_msh_file, 
    plot_single_mesh, 
    plot_multiple_meshes,
    get_mesh_stats
)


def example_single_mesh_basic():
    """Example 1: Plot single mesh with default settings."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Single Mesh (Basic)")
    print("="*60 + "\n")
    
    msh_file = Path("data/meshes/model_01/model_01.msh")
    
    if msh_file.exists():
        mesh_data = read_msh_file(msh_file)
        stats = plot_single_mesh(
            mesh_data,
            title="Coastal Water-Sand Model",
            figsize=(14, 5)
        )
        print(f"✓ Mesh stats: {stats['num_nodes']} nodes, {stats['num_elements']} elements")
    else:
        print(f"✗ File not found: {msh_file}")


def example_single_mesh_custom():
    """Example 2: Plot single mesh with custom colors and names."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Single Mesh (Custom Colors & Names)")
    print("="*60 + "\n")
    
    msh_file = Path("data/meshes/model_01/model_01.msh")
    
    if msh_file.exists():
        mesh_data = read_msh_file(msh_file)
        
        # Custom material definitions
        custom_names = {
            5: "Water Column",
            6: "Sandy Bottom"
        }
        custom_colors = {
            5: "#0066CC",  # Deep blue
            6: "#D4A574"   # Sandy brown
        }
        
        stats = plot_single_mesh(
            mesh_data,
            title="Coastal Model - Custom Theme",
            material_names=custom_names,
            material_colors=custom_colors,
            figsize=(14, 5),
            show_plot=False  # Don't display
        )
        print(f"✓ Custom plot generated")
        print(f"  Materials: {', '.join(custom_names.values())}")
    else:
        print(f"✗ File not found: {msh_file}")


def example_mesh_stats():
    """Example 3: Extract and display mesh statistics."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Mesh Statistics")
    print("="*60 + "\n")
    
    msh_file = Path("data/meshes/model_01/model_01.msh")
    
    if msh_file.exists():
        mesh_data = read_msh_file(msh_file)
        stats = get_mesh_stats(mesh_data)
        
        print(f"Nodes:       {stats['num_nodes']:,}")
        print(f"Elements:    {stats['num_elements']:,}")
        print(f"Materials:   {list(stats['materials'].keys())}")
        
        bounds = stats['bounds']
        print(f"\nDomain Bounds:")
        print(f"  X: {bounds['x_min']:.2f} to {bounds['x_max']:.2f} m (width: {bounds['width']:.2f} m)")
        print(f"  Z: {bounds['z_min']:.2f} to {bounds['z_max']:.2f} m (height: {bounds['height']:.2f} m)")
        print(f"  Aspect ratio: {bounds['width']/bounds['height']:.2f}")
        
        print(f"\nMaterial Distribution:")
        total = stats['num_elements']
        for mat_id, count in sorted(stats['materials'].items()):
            pct = (count / total) * 100
            print(f"  Material {mat_id}: {count:,} elements ({pct:.1f}%)")
    else:
        print(f"✗ File not found: {msh_file}")


def example_multiple_meshes():
    """Example 4: Compare multiple meshes side-by-side (template)."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Multiple Meshes (Template)")
    print("="*60 + "\n")
    
    # This is a template showing how to use plot_multiple_meshes
    # when you have multiple mesh files to compare
    
    print("""
To compare multiple meshes, use:

    from pathlib import Path
    from utils.mesh_plotting import plot_multiple_meshes
    
    mesh_files = [
        Path("data/meshes/model_01/model_01.msh"),
        Path("data/meshes/model_02/model_02.msh"),  # (if exists)
    ]
    
    stats = plot_multiple_meshes(
        mesh_files,
        titles=["Model 1", "Model 2"],
        output_file=Path("comparison.png")
    )
""")


def example_batch_processing():
    """Example 5: Batch process multiple mesh files."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Batch Processing (Template)")
    print("="*60 + "\n")
    
    print("""
To batch process multiple mesh files:

    from pathlib import Path
    from utils.mesh_plotting import read_msh_file, get_mesh_stats
    
    mesh_dir = Path("data/meshes")
    
    for msh_file in mesh_dir.glob("*//*.msh"):
        mesh_data = read_msh_file(msh_file)
        stats = get_mesh_stats(mesh_data)
        print(f"{msh_file.stem}: {stats['num_nodes']} nodes, "
              f"{stats['num_elements']} elements")
""")


if __name__ == "__main__":
    print("\n" + "#"*60)
    print("# Generic Mesh Plotting Examples")
    print("#"*60)
    
    example_single_mesh_basic()
    example_single_mesh_custom()
    example_mesh_stats()
    example_multiple_meshes()
    example_batch_processing()
    
    print("\n" + "#"*60)
    print("# Examples Complete")
    print("#"*60 + "\n")
