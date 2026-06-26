#!/usr/bin/env python3
"""
Tests for create_mesh_with_PML.py

Tests the mesh creation with PML script functionality.
"""

import sys
import os
from pathlib import Path
from unittest import mock
import subprocess

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "preprocessing"))

from create_mesh_with_PML import get_project_root, run_model_01


class TestMeshWithPML:
    """Test suite for create_mesh_with_PML module."""

    def test_get_project_root(self):
        """Test that get_project_root returns correct path."""
        root = get_project_root()
        assert root.exists(), "Project root should exist"
        assert (root / "data" / "models" / "model_01.py").exists(), "model_01.py should exist in project"
        assert (root / "src" / "preprocessing").exists(), "src/preprocessing should exist in project"

    def test_model_script_exists(self):
        """Test that model_01.py script exists."""
        root = get_project_root()
        model_script = root / "data" / "models" / "model_01.py"
        assert model_script.exists(), f"Model script not found at {model_script}"

    def test_meshio2spec2d_module_exists(self):
        """Test that meshio2spec2d module exists."""
        root = get_project_root()
        meshio_module = root / "src" / "preprocessing" / "from_specfem" / "meshio2spec2d.py"
        assert meshio_module.exists(), f"meshio2spec2d module not found at {meshio_module}"

    @mock.patch("subprocess.run")
    def test_run_model_01_with_mock(self, mock_subprocess):
        """Test run_model_01 function with mocked subprocess."""
        # Configure mock to simulate successful execution
        mock_result = mock.Mock()
        mock_subprocess.return_value = mock_result

        # Run the function
        success = run_model_01()

        # Assertions
        assert success, "run_model_01 should return True on successful execution"
        assert mock_subprocess.called, "subprocess.run should be called"

        # Check that conda run with specfempp is used
        call_args = mock_subprocess.call_args
        assert call_args is not None
        assert call_args[0][0][0] == "conda", "Should use conda"
        assert "specfempp" in call_args[0][0], "Should use specfempp environment"
        assert "python" in call_args[0][0], "Should call python"

    @mock.patch("subprocess.run")
    def test_run_model_01_failure_handling(self, mock_subprocess):
        """Test run_model_01 error handling on subprocess failure."""
        # Configure mock to simulate failure
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, "cmd")

        # Run the function
        success = run_model_01()

        # Assertions
        assert not success, "run_model_01 should return False on subprocess failure"

    @mock.patch("subprocess.run")
    def test_pythonpath_environment_set(self, mock_subprocess):
        """Test that PYTHONPATH is properly set for local modules."""
        # Configure mock
        mock_subprocess.return_value = mock.Mock()

        # Run the function
        run_model_01()

        # Check that environment was passed with PYTHONPATH
        call_kwargs = mock_subprocess.call_args[1]
        assert "env" in call_kwargs, "Environment should be passed to subprocess"
        
        env = call_kwargs["env"]
        assert "PYTHONPATH" in env, "PYTHONPATH should be set"
        assert "from_specfem" in env["PYTHONPATH"], "PYTHONPATH should include from_specfem directory"

    def test_project_structure(self):
        """Test that project structure is as expected."""
        root = get_project_root()
        
        # Check required directories
        assert (root / "data" / "models").exists(), "data/models directory should exist"
        assert (root / "src" / "preprocessing").exists(), "src/preprocessing directory should exist"
        assert (root / "src" / "preprocessing" / "from_specfem").exists(), "src/preprocessing/from_specfem should exist"

    def test_script_imports(self):
        """Test that all required modules can be imported."""
        try:
            import create_mesh_with_PML  # noqa: F401
        except ImportError as e:
            raise AssertionError(f"Failed to import create_mesh_with_PML: {e}")


if __name__ == "__main__":
    # Run tests with pytest if available
    try:
        import pytest
        pytest.main([__file__, "-v"])
    except ImportError:
        print("pytest not found. Running basic tests...")
        test_suite = TestMeshWithPML()
        
        print("Running test_get_project_root...")
        test_suite.test_get_project_root()
        print("✓ PASSED")
        
        print("Running test_model_script_exists...")
        test_suite.test_model_script_exists()
        print("✓ PASSED")
        
        print("Running test_meshio2spec2d_module_exists...")
        test_suite.test_meshio2spec2d_module_exists()
        print("✓ PASSED")
        
        print("Running test_project_structure...")
        test_suite.test_project_structure()
        print("✓ PASSED")
        
        print("Running test_script_imports...")
        test_suite.test_script_imports()
        print("✓ PASSED")
        
        print("\n5/5 tests passed!")
