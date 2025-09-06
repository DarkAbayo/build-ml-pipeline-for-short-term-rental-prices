#!/usr/bin/env python
"""
Utility functions for environment and dependency management.

This module provides utility functions for checking the current conda environment,
verifying dependencies, and ensuring the correct environment is being used for
the ML pipeline execution.

Key Functions:
- get_current_environment: Detect the current conda environment name
- check_dependencies: Verify all required packages are installed
- verify_environment: Ensure the correct environment is active

Author: Niedermeier Patrick
Date: 2025-09-06
"""
import os
import sys

def get_current_environment():
    """
    Get current conda environment name from various sources.
    
    This function attempts to detect the current conda environment using multiple
    methods in order of reliability. It checks the Python executable path first
    (most reliable), then falls back to environment variables.
    
    Detection Methods (in order):
    1. Python executable path analysis (most reliable)
    2. CONDA_DEFAULT_ENV environment variable
    3. CONDA_PREFIX environment variable
    
    Returns:
        str or None: The name of the current conda environment, or None if not detected
        
    Example:
        >>> env_name = get_current_environment()
        >>> print(f"Current environment: {env_name}")
        Current environment: nyc_airbnb_dev
    """
    # Method 1: Check Python executable path (MOST RELIABLE)
    python_path = sys.executable
    if 'conda' in python_path.lower() and 'envs' in python_path:
        path_parts = python_path.split('/')
        for i, part in enumerate(path_parts):
            if part == 'envs' and i + 1 < len(path_parts):
                return path_parts[i + 1]
    
    # Method 2: Environment variables (fallback)
    env_name = os.environ.get('CONDA_DEFAULT_ENV')
    if env_name:
        return env_name
    
    # Method 3: CONDA_PREFIX
    conda_prefix = os.environ.get('CONDA_PREFIX')
    if conda_prefix:
        return os.path.basename(conda_prefix)
    
    return None

def check_dependencies():
    """
    Check if all required packages are installed and available.
    
    This function verifies that all essential packages for the ML pipeline
    are properly installed and can be imported. It checks for the core
    dependencies needed for data processing, ML training, and experiment tracking.
    
    Required Packages:
    - wandb: Weights & Biases for experiment tracking
    - pandas: Data manipulation and analysis
    - numpy: Numerical computing
    
    Returns:
        bool: True if all packages are available, False otherwise
        
    Side Effects:
        - Prints status messages to stdout
        - Lists missing packages if any are found
        
    Example:
        >>> if check_dependencies():
        ...     print("All dependencies are available")
        ... else:
        ...     print("Some dependencies are missing")
    """
    required_packages = ['wandb', 'pandas', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {missing_packages}")
        return False
    
    print("✅ All required packages are installed")
    return True

def verify_environment(expected_env="nyc_airbnb_dev"):
    """
    Verify that we're running in the correct conda environment.
    
    This function checks if the current conda environment matches the expected
    environment name. It provides detailed feedback about the environment status
    and helpful instructions if the wrong environment is detected.
    
    Args:
        expected_env (str, optional): Name of the expected conda environment.
            Defaults to "nyc_airbnb_dev".
    
    Returns:
        bool: True if the correct environment is active, False otherwise
        
    Side Effects:
        - Prints status messages to stdout
        - Provides activation instructions if wrong environment is detected
        
    Example:
        >>> if verify_environment("nyc_airbnb_dev"):
        ...     print("Environment is correct")
        ... else:
        ...     print("Please activate the correct environment")
    """
    current_env = get_current_environment()
    
    if not current_env:
        print("⚠️  WARNING: Could not detect conda environment!")
        print("   Make sure you're running in a conda environment")
        return False
    
    if current_env != expected_env:
        print(f"⚠️  WARNING: Wrong conda environment detected!")
        print(f"   Expected: {expected_env}")
        print(f"   Current:  {current_env}")
        print(f"   Please activate the correct environment:")
        print(f"   conda activate {expected_env}")
        return False
    
    print(f"✅ Correct environment detected: {current_env}")
    return True