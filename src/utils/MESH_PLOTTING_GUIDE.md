"""
MESH PLOTTING MODULE - UPDATED FEATURES
========================================

The mesh_plotting.py module has been redesigned to be more generic and flexible,
supporting both single geometries and multiple geometries while separating
data (statistics) from visualization (plots).

KEY CHANGES
===========

1. STATISTICS EXPORT TO JSON
   - Stats are now saved separately in JSON format (not in plot panel)
   - Function: save_mesh_stats(stats, output_file)
   - Function: load_mesh_stats(stats_file)
   - Output format: {num_nodes, num_elements, materials, bounds}

2. CLEANER MESH VISUALIZATION
   - Plots now use single subplot (full figure width)
   - Removed embedded statistics panel
   - Better focus on mesh geometry and material regions
   - Improved legend display

3. GENERIC FUNCTIONS
   - read_msh_file(msh_file): Parse any .msh file (geometry-agnostic)
   - get_mesh_stats(mesh_data): Calculate statistics from any mesh
   - create_color_map(material_ids, custom_colors): Generate color maps
   - create_material_names(material_ids, custom_names): Generate labels

4. FLEXIBLE PLOTTING
   - plot_single_mesh(): Plot one mesh with optional JSON stats export
   - plot_multiple_meshes(): Compare multiple meshes side-by-side
   - plot_mesh(): Legacy wrapper for backward compatibility

5. CUSTOMIZATION OPTIONS
   - material_names: Dict[int, str] for custom material labels
   - material_colors: Dict[int, str] for custom colors (hex format)
   - figsize: Custom figure dimensions
   - show_plot: Control display (useful for batch processing)
   - stats_file: Optional JSON output path


USAGE EXAMPLES
==============

1. BASIC SINGLE MESH PLOT
   ----------------------
   from utils.mesh_plotting import read_msh_file, plot_single_mesh
   
   mesh_data = read_msh_file(Path("model.msh"))
   stats = plot_single_mesh(
       mesh_data,
       output_file=Path("plot.png"),
       stats_file=Path("stats.json")
   )

2. CUSTOM MATERIALS AND COLORS
   ---------------------------
   custom_names = {5: "Water", 6: "Sand"}
   custom_colors = {5: "#0066CC", 6: "#D4A574"}
   
   stats = plot_single_mesh(
       mesh_data,
       output_file=Path("plot.png"),
       stats_file=Path("stats.json"),
       material_names=custom_names,
       material_colors=custom_colors
   )

3. COMPARE MULTIPLE MESHES
   -----------------------
   mesh_files = [Path("model1.msh"), Path("model2.msh")]
   
   stats_list = plot_multiple_meshes(
       mesh_files,
       output_file=Path("comparison.png"),
       titles=["Model 1", "Model 2"]
   )

4. BATCH PROCESSING (NO DISPLAY)
   ----------------------------
   from pathlib import Path
   from utils.mesh_plotting import read_msh_file, get_mesh_stats
   
   mesh_dir = Path("data/meshes")
   for msh_file in mesh_dir.glob("*//*.msh"):
       mesh_data = read_msh_file(msh_file)
       stats = get_mesh_stats(mesh_data)
       print(f"{msh_file.stem}: {stats['num_nodes']} nodes")


JSON OUTPUT FORMAT
==================

{
  "num_nodes": 19245,
  "num_elements": 18800,
  "materials": {
    "5": 15580,
    "6": 3220
  },
  "bounds": {
    "x_min": 0.0,
    "x_max": 30.0,
    "z_min": 0.0,
    "z_max": 3.0,
    "width": 30.0,
    "height": 3.0
  }
}


BACKWARD COMPATIBILITY
======================

The plot_mesh() function maintains backward compatibility:

   plot_mesh(msh_file, output_file=None, stats_file=None)

Works with existing code while supporting new JSON stats export.


GEOMETRY SUPPORT
================

Generic Parser - works with ANY 2D Gmsh mesh:
✓ Simple geometries (single material)
✓ Multi-material domains
✓ Structured and unstructured grids
✓ Triangular and quadrilateral elements

Not limited to specific domain shapes or layer configurations.
"""
