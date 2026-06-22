# Code Organization Guide

## Main Execution Scripts

**`src/simulation/`** - This is where your main scripts that execute SPECFEM2D commands should go.

Example files:
```
src/simulation/
├── __init__.py
├── run_simulation.py          # Main script to run SPECFEM2D
├── par_file_generator.py      # Generate Par_file configurations
├── specfem_wrapper.py         # Wrapper for SPECFEM2D commands
└── job_manager.py             # Manage simulation jobs/batches
```

## Supporting Code Organization

| Directory | Purpose | Example Files |
|-----------|---------|---|
| `src/preprocessing/` | Prepare inputs before simulation | `mesh_generator.py`, `model_setup.py`, `receiver_setup.py` |
| `src/simulation/` | **Execute SPECFEM2D** | `run_simulation.py`, `specfem_wrapper.py` |
| `src/postprocessing/` | Analyze results after simulation | `waveform_analysis.py`, `seismogram_plot.py`, `data_export.py` |
| `src/utils/` | Reusable helper functions | `file_io.py`, `data_conversion.py`, `plotting_utils.py` |

## Recommended Workflow Script

Create a top-level script that orchestrates the full pipeline:

```
JIPSENSE/
├── run_jipsense.py            # Main entry point (orchestrates workflow)
└── src/
    ├── preprocessing/         # Pre-simulation setup
    ├── simulation/            # SPECFEM2D execution
    └── postprocessing/        # Post-simulation analysis
```

This way, users can run:
```bash
python run_jipsense.py --config my_config.yaml
```

And it coordinates preprocessing → simulation → postprocessing through the modular scripts in each subdirectory.

## Directory Details

### src/preprocessing/
Contains scripts for preparing data before SPECFEM2D simulation:
- Mesh generation and refinement
- Velocity model setup
- Source and receiver configuration
- Parameter file creation

### src/simulation/
**Primary location for SPECFEM2D execution scripts:**
- Wrapper functions around SPECFEM2D command-line tools
- Job submission and management
- Parameter file generation and validation
- Simulation control and monitoring

### src/postprocessing/
Contains scripts for analyzing and visualizing simulation results:
- Waveform extraction and analysis
- Seismogram plotting and comparison
- Data format conversion
- Misfit calculations

### src/utils/
Reusable utility functions used across modules:
- File I/O operations
- Data parsing and conversion
- Common plotting utilities
- Configuration handling

## Best Practices

1. **Keep it modular** - Each script should have a single responsibility
2. **Document your functions** - Use docstrings explaining inputs, outputs, and purpose
3. **Use configuration files** - Store parameters in YAML/JSON, not hardcoded
4. **Test your code** - Add unit tests in `tests/` directory
5. **Version your dependencies** - Maintain `requirements.txt` with pinned versions
