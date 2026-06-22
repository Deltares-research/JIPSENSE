# JIPSENSE

SPECFEM2D Modeling Suite - A Python-based framework for seismic wave simulations using SPECFEM2D.

## Project Structure

- **src/**: Main Python package
  - `preprocessing/`: Mesh generation and model setup scripts
  - `simulation/`: SPECFEM2D simulation control
  - `postprocessing/`: Data analysis and visualization
  - `utils/`: Utility functions

- **data/**: Data directory
  - `models/`: Velocity models and parameters
  - `meshes/`: Mesh files
  - `input/`: Input data (sources, receivers)
  - `output/`: Simulation results

- **specfem2d_config/**: SPECFEM2D configuration templates
- **notebooks/**: Jupyter notebooks for interactive analysis
- **examples/**: Example workflows and tutorials
- **tests/**: Unit and integration tests
- **docs/**: Documentation

## Installation

```bash
pip install -r requirements.txt
pip install -e .
```

## Usage

See examples/ and notebooks/ for usage examples.

## License

MIT License - See LICENSE file for details
