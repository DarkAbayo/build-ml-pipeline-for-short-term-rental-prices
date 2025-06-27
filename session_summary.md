# ML Pipeline Session Summary

## 🎯 **Hauptprobleme gelöst:**

### 1. **Conda-Umgebungserkennung in Jupyter**
**Problem:** Jupyter erkannte `base` statt `nyc_airbnb_dev`
**Lösung:** Erweiterte `get_current_environment()` Funktion in `Utility_Functions.py`

```python
def get_current_environment():
    """Get current environment name from environment variables"""
    import sys
    
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
```

### 2. **Ydata_profiling Kompatibilitätsproblem**
**Problem:** `AttributeError: 'float' object has no attribute 'ndim'`
**Ursache:** Inkompatibilität zwischen `ydata_profiling` und `scipy`
**Lösung:** Spezifische Versionen in Conda-Umgebungen

## 📋 **Aktualisierte Conda-Umgebungen:**

### `environment.yml` (nyc_airbnb_dev):
```yaml
name: nyc_airbnb_dev
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.10
  - hydra-core=1.3.2
  - matplotlib=3.8.2
  - pandas=2.1.3
  - jupyterlab=4.0.9
  - pip=23.3.1
  - scipy=1.10.1
  - pip:
      - mlflow==2.8.1
      - wandb==0.16.0
      - ydata-profiling==4.6.3
```

### `conda.yml` (components):
```yaml
name: components
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.10
  - pyyaml
  - hydra-core=1.3.2
  - pip=23.3.1
  - scipy=1.10.1
  - pip:
      - mlflow==2.8.1
      - wandb==0.16.0
      - ydata-profiling==4.6.3
```

## 🛠️ **Utility Functions erstellt:**

### `src/Utility_Functions.py`:
```python
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
```

## 🚀 **Funktionierender EDA-Code:**

```python
import wandb
import pandas as pd
import ydata_profiling
import os
import warnings
from .. import Utility_Functions

# 1. Warnungen unterdrücken
warnings.filterwarnings("ignore", category=UserWarning, module="wandb")

# 2. Notebook-Name setzen
os.environ['WANDB_NOTEBOOK_NAME'] = 'EDA.ipynb'

# 3. Environment check
if not Utility_Functions.verify_environment("nyc_airbnb_dev"):
    print("❌ Please fix the environment before continuing!")

# 4. Wandb initialization
run = wandb.init(project="nyc_airbnb", group="eda", save_code=True)

# 5. Artifact laden
latest_artifact = wandb.use_artifact("sample.csv:latest")
local_path = latest_artifact.file()
df = pd.read_csv(local_path)

# 6. Profiling
profile = ydata_profiling.ProfileReport(df, title="Profiling Report")
profile.to_file("profile.html")
print("✅ Profiling successful!")
```

## 🔧 **Wichtige Befehle:**

### Umgebungen aktualisieren:
```bash
conda env update -f environment.yml
conda env update -f conda.yml
```

### Jupyter Kernel neu installieren:
```bash
conda activate nyc_airbnb_dev
python -m ipykernel install --user --name nyc_airbnb_dev --display-name "nyc_airbnb_dev"
```

## 🎯 **Nächste Schritte:**

1. **EDA abschließen** mit funktionierendem Profiling
2. **Artifact-Management-Funktion** entwickeln (für zukünftige Sessions)
3. **Pipeline-Komponenten** mit aktualisierten Umgebungen testen

## 💡 **Wichtige Erkenntnisse:**

1. **Python-Pfad ist zuverlässiger** als Umgebungsvariablen für Conda-Erkennung
2. **Beide Conda-Umgebungen müssen konsistent** sein (dev + pipeline)
3. **Spezifische Paketversionen** sind wichtig für Kompatibilität
4. **Wandb-Notebook-Name** sollte explizit gesetzt werden

## 📁 **Dateien erstellt/geändert:**

- ✅ `src/Utility_Functions.py` (neu)
- ✅ `environment.yml` (aktualisiert)
- ✅ `conda.yml` (aktualisiert)
- ✅ `session_summary.md` (diese Datei)

---
**Session-Datum:** 2025-01-27
**Status:** ✅ Alle Hauptprobleme gelöst
**Nächste Session:** EDA abschließen, Pipeline-Komponenten entwickeln 