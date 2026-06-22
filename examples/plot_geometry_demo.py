"""
Demo script: Plot geometry with sources and receivers overlaid.

Shows how to visualize the mesh geometry along with source and receiver positions
for model_01.
"""

from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.mesh_plotting import plot_geometry_with_sources_receivers


def main():
    """Plot model_01 geometry with sources and receivers."""
    
    # Define paths
    project_root = Path(__file__).parent.parent
    mesh_file = project_root / "data/meshes/model_01/model_01.msh"
    output_plot = project_root / "data/meshes/model_01/model_01_geometry_with_sources.png"
    
    # Read SOURCE and STATIONS from simulation DATA directory
    data_dir = project_root / "src/simulation/DATA"
    source_file = data_dir / "SOURCE"
    stations_file = data_dir / "STATIONS"
    
    print(f"\n{'='*60}")
    print("GEOMETRY VISUALIZATION WITH SOURCES & RECEIVERS")
    print(f"{'='*60}\n")
    
    print(f"Mesh file:      {mesh_file}")
    print(f"Source file:    {source_file}")
    print(f"Stations file:  {stations_file}")
    print(f"Output plot:    {output_plot}\n")
    
    # Verify files exist
    if not mesh_file.exists():
        print(f"❌ Mesh file not found: {mesh_file}")
        return
    
    if not source_file.exists():
        print(f"⚠️  Source file not found: {source_file}")
        source_file = None
    
    if not stations_file.exists():
        print(f"⚠️  Stations file not found: {stations_file}")
        stations_file = None
    
    # Custom colors and names for water/sand model
    material_colors = {5: '#0066CC', 6: '#CD853F'}  # Blue water, tan sand
    material_names = {5: 'Water (M5)', 6: 'Sand (M6)'}
    
    # Plot geometry with sources and receivers
    stats = plot_geometry_with_sources_receivers(
        mesh_file,
        source_file=source_file,
        stations_file=stations_file,
        output_file=output_plot,
        title='Model 01: Geometry with Source & Receivers',
        material_names=material_names,
        material_colors=material_colors,
        figsize=(14, 6),
        show_plot=False  # Don't display in script, just save
    )
    
    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Mesh nodes:      {stats['num_nodes']:,}")
    print(f"Mesh elements:   {stats['num_elements']:,}")
    print(f"Materials:       {stats['materials']}")
    print(f"\n✓ Geometry plot with sources & receivers saved!")
    print(f"  Location: {output_plot}\n")


if __name__ == '__main__':
    main()
