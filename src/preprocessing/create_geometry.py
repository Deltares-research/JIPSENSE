#!/usr/bin/env python3
"""
Generate .geo and .msh files for SPECFEM2D simulations using Gmsh.

This script creates customizable mesh geometries with multiple material layers
and boundary definitions, then converts them to SPECFEM2D format via Gmsh.
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Tuple

# Import mesh utilities
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.mesh_plotting import read_msh_file, plot_mesh


class GeometryParameters:
    """Store geometry parameters for .geo file generation."""
    
    def __init__(self, name: str = "model_01", width: float = 30.0, height: float = 3.0,
                 sand_thk: float = 0.5,
                 lc_fine: float = 0.3, lc_coarse: float = 0.25, lc_medium: float = 0.3):
        """
        Initialize geometry parameters.
        
        Args:
            name: Model name (used for filename)
            width: Domain width in meters
            height: Domain height in meters
            sand_thk: Sand/sediment layer thickness in meters (bottom layer)
            lc_fine: Fine mesh characteristic length
            lc_coarse: Coarse mesh characteristic length
            lc_medium: Medium mesh characteristic length
        """
        self.name = name
        self.width = width
        self.height = height
        self.sand_thickness = sand_thk
        self.lc_fine = lc_fine
        self.lc_coarse = lc_coarse
        self.lc_medium = lc_medium


class GeoFileGenerator:
    """Generate Gmsh .geo files with customizable geometry and material layers."""
    
    def __init__(self, params: GeometryParameters):
        """
        Initialize geometry generator.
        
        Args:
            params: GeometryParameters object with mesh configuration
        """
        self.params = params
        self.points = []
        self.lines = []
        self.surfaces = []
        self.physical_lines = {}
        self.physical_surfaces = {}
        
    def generate(self):
        """Generate all geometric entities (points, lines, surfaces)."""
        w, h = self.params.width, self.params.height
        d_sand = self.params.sand_thickness
        lc, lc0, lc1 = self.params.lc_fine, self.params.lc_coarse, self.params.lc_medium
        
        # Domain box corners
        self.points = [
            (1, 0, 0, 0, lc0),           # Bottom-left
            (2, w, 0, 0, lc0),           # Bottom-right
            (3, w, h, 0, lc1),           # Top-right
            (4, 0, h, 0, lc1)            # Top-left
        ]
        
        # Water/sand interface points
        self.points += [
            (5, 0, d_sand, 0, lc),       # Interface left
            (6, w, d_sand, 0, lc)        # Interface right
        ]
        
        # Lines connecting points
        self.lines = [
            (100, [1, 2]),               # Bottom boundary
            (101, [2, 6]),               # Right side lower
            (102, [6, 3]),               # Right side upper
            (103, [3, 4]),               # Top boundary
            (104, [4, 5]),               # Left side upper
            (105, [5, 1]),               # Left side lower
            (106, [5, 6])                # Water/sand interface
        ]
        
        # Surfaces with material identification
        self.surfaces = [
            ('water', 1, [106, 102, 103, 104]),           # Water layer (M1)
            ('sand', 2, [100, 101, -106, 105])            # Sand/sediment layer (M2)
        ]
        
        # Physical boundaries for SPECFEM2D
        self.physical_lines = {
            'Top': [103],
            'Bottom': [100],
            'Left': [104, 105],
            'Right': [101, 102]
        }
        
        # Physical surfaces (material definitions)
        self.physical_surfaces = {
            'M1': (1, 1),       # Material 1 - Water
            'M2': (2, 2)        # Material 2 - Sand/Sediment
        }
        
    def write(self, output_dir: str = None) -> Path:
        """
        Write geometry to .geo file.
        
        Args:
            output_dir: Output directory path (defaults to data/meshes/model_01)
            
        Returns:
            Path to generated .geo file
        """
        if output_dir is None:
            output_dir = Path(__file__).parent.parent.parent / "data" / "meshes" / "model_01"
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        filepath = output_dir / f"{self.params.name}.geo"
        
        # Build .geo file content
        lines = [
            f"// Gmsh geometry file: {self.params.name}",
            ""
        ]
        
        # Define characteristic lengths
        lines.append(f"lc = {self.params.lc_fine};")
        lines.append(f"lc0 = {self.params.lc_coarse};")
        lines.append(f"lc1 = {self.params.lc_medium};")
        lines.append(f"h = {self.params.height};")
        lines.append(f"l = {self.params.width};")
        lines.append(f"d_sand = {self.params.sand_thickness};")
        lines.append("")
        
        # Points section
        lines.append("// Points")
        for pid, x, y, z, lc in self.points:
            lines.append(f"Point({pid}) = {{{x}, {y}, {z}, {lc}}};")
        
        # Lines section
        lines.append("\n// Lines")
        for lid, [p1, p2] in self.lines:
            lines.append(f"Line({lid}) = {{{p1}, {p2}}};")
        
        # Surfaces and physical entities
        lines.append("\n// Surfaces & Line Loops")
        for name, loop_id, line_ids in self.surfaces:
            lines.append(f"Line Loop({loop_id}) = {{{', '.join(map(str, line_ids))}}};")
            lines.append(f"Plane Surface({loop_id}) = {{{loop_id}}};")
        
        # Mesh options
        lines.append("\n// Mesh settings")
        lines.append("Recombine Surface{1, 2};")
        lines.append("Mesh.SubdivisionAlgorithm = 1;")
        lines.append("Mesh.ElementOrder = 1;")
        lines.append("")
        
        # Physical boundaries
        lines.append("// Physical boundaries")
        for name, line_ids in self.physical_lines.items():
            line_str = ", ".join(map(str, line_ids))
            lines.append(f'Physical Line("{name}") = {{{line_str}}};')
        
        # Physical surfaces (materials)
        lines.append("\n// Physical surfaces (materials)")
        for name, (surf_id, _) in self.physical_surfaces.items():
            lines.append(f'Physical Surface("{name}") = {{{surf_id}}};')
        
        # Write to file
        filepath.write_text("\n".join(lines))
        print(f"✓ Generated .geo file: {filepath}")
        return filepath


def generate_msh_file(geo_file: Path, output_msh: Path = None) -> Path:
    """
    Convert .geo file to .msh format using Gmsh.
    
    Args:
        geo_file: Path to .geo file
        output_msh: Path to output .msh file (defaults to same name)
        
    Returns:
        Path to generated .msh file
    """
    if output_msh is None:
        output_msh = geo_file.with_suffix('.msh')
    
    # Run Gmsh to generate mesh
    cmd = [
        'gmsh',
        str(geo_file),
        '-2',                          # 2D mesh
        '-format', 'msh22',             # MSH format version 2.2 (compatible with SPECFEM2D)
        '-o', str(output_msh)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✓ Generated .msh file: {output_msh}")
        return output_msh
    except subprocess.CalledProcessError as e:
        print(f"✗ Gmsh error: {e.stderr}")
        raise


def main():
    """Main execution: generate geometry and mesh files."""
    try:
        # Get output directory (data/meshes/model_01)
        output_dir = Path(__file__).parent.parent.parent / "data" / "meshes" / "model_01"
        
        # Create geometry parameters
        params = GeometryParameters(
            name="model_01",
            width=30.0,
            height=3.0,
            sand_thk=0.5,
            lc_fine=0.15,
            lc_coarse=0.15,
            lc_medium=0.15
        )
        
        # Generate geometry
        print(f"\n{'='*60}")
        print("GEOMETRY GENERATION")
        print(f"{'='*60}\n")
        
        generator = GeoFileGenerator(params)
        generator.generate()
        geo_file = generator.write(output_dir=str(output_dir))
        
        # Generate mesh
        print(f"\n{'='*60}")
        print("MESH GENERATION")
        print(f"{'='*60}\n")
        
        msh_file = generate_msh_file(geo_file)
        
        # Plot mesh and show statistics
        print(f"\n{'='*60}")
        print("MESH VISUALIZATION")
        print(f"{'='*60}\n")
        
        plot_output = output_dir / f"{params.name}_mesh_plot.png"
        stats_output = output_dir / f"{params.name}_mesh_stats.json"
        
        # Custom colors and names for water/sand model
        material_colors = {5: '#0066CC', 6: '#CD853F'}  # Blue water, tan sand
        material_names = {5: 'Water (M5)', 6: 'Sand (M6)'}
        
        mesh_stats = plot_mesh(
            msh_file, 
            output_file=plot_output, 
            stats_file=stats_output,
            material_colors=material_colors,
            material_names=material_names
        )
        
        print(f"\n{'='*60}")
        print("SUMMARY")
        print(f"{'='*60}")
        print(f"Model name:      {params.name}")
        print(f"Domain size:     {params.width} × {params.height} m")
        print(f"Sand thickness:  {params.sand_thickness} m")
        print(f"Mesh nodes:      {mesh_stats['num_nodes']:,}")
        print(f"Mesh elements:   {mesh_stats['num_elements']:,}")
        print(f"Output location: {output_dir}")
        print(f"✓ Geometry and mesh generation complete!\n")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
