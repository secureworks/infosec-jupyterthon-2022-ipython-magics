from setuptools import setup, find_packages
from pathlib import Path


setup(
    name="azmagic",
    author="Ryan Marcotte Cobb, Micah Pegman, Secureworks",
    description="Azure CLI IPython Magic PoC",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    version="0.1",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=["pandas>=1.1.5", "azure-cli>=2.40.0", "IPython>=7.30.1"],
)
