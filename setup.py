from setuptools import setup, find_packages

setup(
    name="jipsense",
    version="0.1.0",
    description="SPECFEM2D Modeling Suite",
    author="Deltares",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
        "pandas>=1.3.0",
    ],
    python_requires=">=3.8",
)
