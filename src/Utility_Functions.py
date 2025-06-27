import os
import sys

def get_current_environment():
    """Get current environment name from environment variables"""
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
    """Check if all required packages are installed"""
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
    Verify that we're running in the correct conda environment
    
    Args:
        expected_env (str): Name of the expected environment
    
    Returns:
        bool: True if environment is correct, False otherwise
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