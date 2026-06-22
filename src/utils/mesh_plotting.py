"""
Generic utilities for reading and visualizing Gmsh mesh files.

Supports single geometries and multiple geometries (batch plots).
Provides customizable material naming, coloring, and statistics.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Patch
from matplotlib.collections import PatchCollection


def read_msh_file(msh_file: Path) -> Dict:
    """
    Generic parser for MSH format files - extracts nodes and elements.
    
    Works with any MSH file regardless of geometry or material structure.
    
    Args:
        msh_file: Path to .msh file
        
    Returns:
        Dictionary with:
        - 'nodes': {node_id: (x, y, z), ...}
        - 'elements': {material_id: [[node1, node2, node3], ...], ...}
    """
    nodes = {}
    elements = {}
    
    # Element type properties: type_id -> num_nodes
    elem_nodes = {
        1: 2,   # Line
        2: 3,   # Triangle
        3: 4,   # Quadrilateral
        4: 4    # Tetrahedron
    }
    
    with open(msh_file, 'r') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Parse nodes section
        if line == '$Nodes':
            i += 1
            num_nodes = int(lines[i].strip())
            i += 1
            for _ in range(num_nodes):
                parts = lines[i].strip().split()
                node_id = int(parts[0])
                x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                nodes[node_id] = (x, y, z)
                i += 1
            i += 1  # Skip $EndNodes
        
        # Parse elements section
        elif line == '$Elements':
            i += 1
            num_elements = int(lines[i].strip())
            i += 1
            for _ in range(num_elements):
                parts = lines[i].strip().split()
                elem_id = int(parts[0])
                elem_type = int(parts[1])
                num_tags = int(parts[2])
                
                # Extract physical tag (material ID)
                physical_tag = int(parts[3]) if num_tags > 0 else 0
                
                # Get connectivity based on element type
                num_nodes_elem = elem_nodes.get(elem_type, 0)
                node_start = 3 + num_tags
                
                if node_start + num_nodes_elem <= len(parts):
                    node_ids = [int(parts[j]) for j in range(node_start, node_start + num_nodes_elem)]
                    
                    # Store 2D elements (triangles and quads)
                    if elem_type in [2, 3]:
                        if physical_tag not in elements:
                            elements[physical_tag] = []
                        elements[physical_tag].append(node_ids)
                i += 1
            i += 1  # Skip $EndElements
        else:
            i += 1
    
    return {'nodes': nodes, 'elements': elements}


def get_mesh_stats(mesh_data: Dict) -> Dict:
    """
    Calculate statistics from parsed mesh data.
    
    Args:
        mesh_data: Dictionary with 'nodes' and 'elements'
        
    Returns:
        Dictionary with node count, element count, material distribution, and domain bounds
    """
    nodes = mesh_data['nodes']
    elements = mesh_data['elements']
    
    num_nodes = len(nodes)
    num_elements = sum(len(elems) for elems in elements.values())
    material_counts = {mat: len(elems) for mat, elems in elements.items()}
    
    # Calculate domain bounds
    if nodes:
        x_coords = [nodes[nid][0] for nid in nodes.keys()]
        z_coords = [nodes[nid][1] for nid in nodes.keys()]
        bounds = {
            'x_min': min(x_coords), 'x_max': max(x_coords),
            'z_min': min(z_coords), 'z_max': max(z_coords),
            'width': max(x_coords) - min(x_coords),
            'height': max(z_coords) - min(z_coords)
        }
    else:
        bounds = {}
    
    return {
        'num_nodes': num_nodes,
        'num_elements': num_elements,
        'materials': material_counts,
        'bounds': bounds
    }


def save_mesh_stats(stats: Dict, output_file: Path) -> None:
    """
    Save mesh statistics to JSON file.
    
    Args:
        stats: Statistics dictionary from get_mesh_stats()
        output_file: Path to output .json file
    """
    # Convert to JSON-serializable format
    json_data = {
        'num_nodes': stats['num_nodes'],
        'num_elements': stats['num_elements'],
        'materials': {str(k): v for k, v in stats['materials'].items()},
        'bounds': stats.get('bounds', {})
    }
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(json_data, f, indent=2)
    print(f"✓ Statistics saved: {output_file}")


def load_mesh_stats(stats_file: Path) -> Dict:
    """
    Load mesh statistics from JSON file.
    
    Args:
        stats_file: Path to .json statistics file
        
    Returns:
        Statistics dictionary
    """
    with open(stats_file, 'r') as f:
        data = json.load(f)
    
    # Convert material keys back to integers
    data['materials'] = {int(k): v for k, v in data.get('materials', {}).items()}
    
    return data


def create_color_map(material_ids: List[int], 
                     custom_colors: Optional[Dict[int, str]] = None) -> Dict[int, str]:
    """
    Generate color map for materials (generic or custom).
    
    Args:
        material_ids: List of material IDs in the mesh
        custom_colors: Optional dict of {material_id: color_hex}
        
    Returns:
        Dictionary mapping material_id to color
    """
    if custom_colors:
        return custom_colors
    
    # Default color palette with high contrast
    # Optimized for distinguishing multiple materials
    default_palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                       '#8c564b', '#e377c2', '#7f7f7f']
    
    color_map = {}
    for idx, mat_id in enumerate(sorted(material_ids)):
        color_map[mat_id] = default_palette[idx % len(default_palette)]
    
    return color_map


def create_material_names(material_ids: List[int], 
                         custom_names: Optional[Dict[int, str]] = None) -> Dict[int, str]:
    """
    Generate material names (generic or custom).
    
    Args:
        material_ids: List of material IDs in the mesh
        custom_names: Optional dict of {material_id: name}
        
    Returns:
        Dictionary mapping material_id to name
    """
    if custom_names:
        return custom_names
    
    # Generate generic names
    name_map = {}
    for idx, mat_id in enumerate(sorted(material_ids)):
        name_map[mat_id] = f'Material {mat_id}'
    
    return name_map


def plot_single_mesh(mesh_data: Dict, 
                     output_file: Optional[Path] = None,
                     stats_file: Optional[Path] = None,
                     title: str = 'Mesh Geometry',
                     material_names: Optional[Dict[int, str]] = None,
                     material_colors: Optional[Dict[int, str]] = None,
                     figsize: Tuple = (10, 6),
                     show_plot: bool = True) -> Dict:
    """
    Plot a single mesh with optional custom materials and colors.
    
    Args:
        mesh_data: Parsed mesh data from read_msh_file()
        output_file: Optional path to save figure (PNG)
        stats_file: Optional path to save statistics (JSON)
        title: Title for the plot
        material_names: Custom material names {material_id: name}
        material_colors: Custom material colors {material_id: hex_color}
        figsize: Figure size (width, height)
        show_plot: Whether to display plot (set False for batch operations)
        
    Returns:
        Dictionary with mesh statistics
    """
    nodes = mesh_data['nodes']
    elements = mesh_data['elements']
    
    # Calculate statistics
    stats = get_mesh_stats(mesh_data)
    
    # Save stats to JSON if requested
    if stats_file:
        save_mesh_stats(stats, stats_file)
    
    # Generate color and name maps
    mat_ids = list(elements.keys())
    colors = create_color_map(mat_ids, material_colors)
    names = create_material_names(mat_ids, material_names)
    
    # Create figure with single subplot
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot elements by material
    for material_id, elem_list in sorted(elements.items()):
        patches = []
        for elem in elem_list:
            coords = [nodes[nid][:2] for nid in elem]
            patches.append(Polygon(coords))
        
        pc = PatchCollection(patches, facecolor=colors.get(material_id, '#CCCCCC'),
                            edgecolor='darkgray', linewidth=0.3, alpha=0.85)
        ax.add_collection(pc)
    
    # Plot nodes (very subtle)
    node_coords = np.array([nodes[nid][:2] for nid in sorted(nodes.keys())])
    ax.scatter(node_coords[:, 0], node_coords[:, 1], s=1, c='black', alpha=0.1)
    
    # Axis configuration
    ax.set_aspect('equal')
    ax.autoscale()
    ax.set_xlabel('x (m)')
    ax.set_ylabel('z (m)')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Legend
    legend_elements = [Patch(facecolor=colors.get(mat, '#CCCCCC'), edgecolor='black', 
                            label=names.get(mat, f'Material {mat}')) 
                      for mat in sorted(elements.keys())]
    ax.legend(handles=legend_elements, loc='upper right')
    
    plt.tight_layout()
    
    # Save if requested
    if output_file:
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"✓ Plot saved: {output_file}")
    
    if show_plot:
        plt.show()
    
    return stats


def plot_multiple_meshes(mesh_files: List[Path],
                        output_file: Optional[Path] = None,
                        titles: Optional[List[str]] = None,
                        material_names_list: Optional[List[Dict[int, str]]] = None,
                        material_colors_list: Optional[List[Dict[int, str]]] = None,
                        figsize: Optional[Tuple] = None,
                        show_plot: bool = True) -> List[Dict]:
    """
    Plot multiple meshes side-by-side for comparison.
    
    Args:
        mesh_files: List of paths to .msh files
        output_file: Optional path to save figure
        titles: Custom titles for each mesh (defaults to filenames)
        material_names_list: List of custom material names dicts
        material_colors_list: List of custom material colors dicts
        figsize: Figure size (auto-calculated if None)
        show_plot: Whether to display plot
        
    Returns:
        List of statistics dictionaries (one per mesh)
    """
    num_meshes = len(mesh_files)
    
    # Auto-calculate figure size
    if figsize is None:
        figsize = (6 * num_meshes, 5)
    
    # Set defaults for optional parameters
    if titles is None:
        titles = [f.stem for f in mesh_files]
    if material_names_list is None:
        material_names_list = [None] * num_meshes
    if material_colors_list is None:
        material_colors_list = [None] * num_meshes
    
    # Read all meshes
    mesh_data_list = [read_msh_file(f) for f in mesh_files]
    stats_list = [get_mesh_stats(data) for data in mesh_data_list]
    
    # Create figure with subplots
    fig, axes = plt.subplots(1, num_meshes, figsize=figsize)
    if num_meshes == 1:
        axes = [axes]
    
    # Plot each mesh
    for idx, (mesh_data, ax) in enumerate(zip(mesh_data_list, axes)):
        nodes = mesh_data['nodes']
        elements = mesh_data['elements']
        
        # Get colors and names
        mat_ids = list(elements.keys())
        colors = create_color_map(mat_ids, material_colors_list[idx])
        names = create_material_names(mat_ids, material_names_list[idx])
        
        # Plot elements
        for material_id, elem_list in sorted(elements.items()):
            patches = []
            for elem in elem_list:
                coords = [nodes[nid][:2] for nid in elem]
                patches.append(Polygon(coords))
            
            pc = PatchCollection(patches, facecolor=colors.get(material_id, '#CCCCCC'),
                                edgecolor='darkgray', linewidth=0.3, alpha=0.85)
            ax.add_collection(pc)
        
        # Plot nodes (very subtle)
        node_coords = np.array([nodes[nid][:2] for nid in sorted(nodes.keys())])
        ax.scatter(node_coords[:, 0], node_coords[:, 1], s=1, c='black', alpha=0.1)
        
        # Configure axis
        ax.set_aspect('equal')
        ax.autoscale()
        ax.set_xlabel('x (m)')
        ax.set_ylabel('z (m)')
        ax.set_title(titles[idx])
        ax.grid(True, alpha=0.3)
        
        # Add legend
        legend_elements = [Patch(facecolor=colors.get(mat, '#CCCCCC'), edgecolor='black',
                                label=names.get(mat, f'Material {mat}'))
                          for mat in sorted(elements.keys())]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=8)
    
    plt.tight_layout()
    
    # Save if requested
    if output_file:
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        print(f"✓ Comparison plot saved: {output_file}")
    
    if show_plot:
        plt.show()
    
    return stats_list


def plot_mesh(msh_file: Path, output_file: Path = None, stats_file: Path = None,
              material_colors: Optional[Dict[int, str]] = None,
              material_names: Optional[Dict[int, str]] = None):
    """
    Legacy function for backward compatibility - wraps plot_single_mesh().
    
    Args:
        msh_file: Path to .msh file
        output_file: Optional path to save figure
        stats_file: Optional path to save statistics (JSON)
        material_colors: Optional custom material colors {material_id: hex_color}
        material_names: Optional custom material names {material_id: name}
        
    Returns:
        Dictionary with mesh statistics
    """
    mesh_data = read_msh_file(msh_file)
    
    return plot_single_mesh(
        mesh_data,
        output_file=output_file,
        stats_file=stats_file,
        title='Mesh Geometry',
        material_colors=material_colors,
        material_names=material_names,
        show_plot=True
    )
