# 📋 Master CheatSheet - ML-Pipeline Komplettübersicht

## 🚀 Schnellstart

### **Pipeline ausführen**
```bash
# Vollständige Pipeline
mlflow run . -P steps=all

# Einzelne Schritte
mlflow run . -P steps=train_random_forest
mlflow run . -P steps=test_regression_model

# Mit neuen Daten
mlflow run . -P hydra_options="etl.sample='sample2.csv'"
```

### **Wichtige URLs**
- **W&B Projekt:** https://wandb.ai/dark_pn-private/nyc_airbnb
- **GitHub Repository:** [Ihr Repository]
- **MLflow UI:** `mlflow ui` (lokal)

## 📊 Pipeline-Übersicht

| Schritt | Input | Output | Beschreibung |
|---------|-------|--------|--------------|
| **Download** | sample1.csv | sample.csv | Daten von W&B laden |
| **Basic Cleaning** | sample.csv | clean_sample.csv | Daten bereinigen |
| **Data Check** | clean_sample.csv | - | Datenqualität prüfen |
| **Data Split** | clean_sample.csv | trainval_data.csv, test_data.csv | Daten aufteilen |
| **Train RF** | trainval_data.csv | random_forest_export | Modell trainieren |
| **Test Model** | random_forest_export:prod, test_data.csv | - | Modell testen |

## 🛠️ Technologie-Stack

### **Core Libraries**
```python
# Data Processing
import pandas as pd
import numpy as np

# Machine Learning
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

# Experiment Tracking
import wandb
import mlflow

# Testing
import pytest
```

### **Konfiguration (config.yaml)**
```yaml
main:
  project_name: nyc_airbnb
  experiment_name: development
  steps: all

etl:
  sample: "sample1.csv"
  min_price: 10
  max_price: 350

modeling:
  test_size: 0.2
  val_size: 0.2
  random_seed: 456
  stratify_by: "neighbourhood_group"
  max_tfidf_features: 15
  random_forest:
    n_estimators: 100
    max_depth: 50
    max_features: 0.33
```

## 🔧 Häufige Befehle

### **MLflow Commands**
```bash
# Pipeline ausführen
mlflow run . -P steps=all

# Mit Hydra Overrides
mlflow run . -P hydra_options="etl.sample='sample2.csv'"

# Einzelne Komponente
mlflow run src/basic_cleaning -P input_artifact=sample.csv:latest

# MLflow UI starten
mlflow ui
```

### **W&B Commands**
```bash
# W&B Login
wandb login

# Offline Mode
wandb offline

# Sync offline runs
wandb sync
```

### **Git Commands**
```bash
# Änderungen committen
git add .
git commit -m "Add feature: improved data cleaning"
git push

# Release erstellen
git tag v1.0.1
git push origin v1.0.1
```

## 📈 Performance-Metriken

### **Erwartete Werte**
- **MAE (Mean Absolute Error):** < 35 Dollar
- **R² Score:** > 0.55
- **Training Time:** < 5 Minuten
- **Prediction Time:** < 100ms

### **Metriken berechnen**
```python
from sklearn.metrics import mean_absolute_error, r2_score

# MAE berechnen
mae = mean_absolute_error(y_true, y_pred)
print(f"MAE: {mae:.2f}")

# R² Score berechnen
r2 = r2_score(y_true, y_pred)
print(f"R²: {r2:.3f}")
```

## 🐛 Troubleshooting

### **Häufige Fehler**

| Fehler | Ursache | Lösung |
|--------|---------|--------|
| `ModuleNotFoundError` | Fehlende Dependencies | `pip install -r requirements.txt` |
| `W&B Login Error` | Nicht angemeldet | `wandb login` |
| `MLflow Run Failed` | Falsche Parameter | Parameter in config.yaml prüfen |
| `Test Failed` | Datenqualität | Daten in W&B prüfen |
| `Memory Error` | Zu große Daten | Batch-Processing verwenden |

### **Debug Commands**
```bash
# Verbose Output
mlflow run . -P steps=all -v

# Einzelne Komponente debuggen
python src/basic_cleaning/run.py --input_artifact sample.csv:latest

# W&B Runs anzeigen
wandb runs list --project nyc_airbnb
```

## 📁 Projektstruktur

```
build-ml-pipeline-for-short-term-rental-prices/
├── config.yaml                 # Hauptkonfiguration
├── main.py                     # Pipeline-Orchestrator
├── environment.yml             # Conda Environment
├── src/                        # Lokale Komponenten
│   ├── basic_cleaning/
│   ├── data_check/
│   ├── train_random_forest/
│   └── test_regression_model/
├── components/                 # Remote Komponenten
├── Docs/                       # Dokumentation
└── mlruns/                     # MLflow Runs
```

## 🔍 Data Quality Checks

### **Automatische Tests**
```python
# Spalten prüfen
def test_column_names(data):
    expected_columns = ['id', 'name', 'host_id', ...]
    assert list(data.columns) == expected_columns

# Geografische Grenzen
def test_proper_boundaries(data):
    assert data['longitude'].between(-74.25, -73.50).all()
    assert data['latitude'].between(40.5, 41.2).all()

# Preisbereich
def test_price_range(data, min_price=10, max_price=350):
    assert data['price'].between(min_price, max_price).all()
```

## 🎯 Feature Engineering

### **Kategorische Features**
```python
# Ordinal Encoding
from sklearn.preprocessing import OrdinalEncoder
ordinal_encoder = OrdinalEncoder()

# One-Hot Encoding
from sklearn.preprocessing import OneHotEncoder
onehot_encoder = OneHotEncoder(handle_unknown='ignore')
```

### **Text Features (TF-IDF)**
```python
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(
    max_features=15,
    stop_words='english',
    ngram_range=(1, 2)
)
```

### **Date Features**
```python
def delta_date_feature(dates):
    date_sanitized = pd.DataFrame(dates).apply(pd.to_datetime)
    return date_sanitized.apply(
        lambda d: (d.max() - d).dt.days, axis=0
    ).to_numpy()
```

## 🌲 Random Forest

### **Hyperparameter**
```python
rf_config = {
    'n_estimators': 100,        # Anzahl Bäume
    'max_depth': 50,            # Maximale Tiefe
    'min_samples_split': 4,     # Min. Samples zum Teilen
    'min_samples_leaf': 3,      # Min. Samples pro Blatt
    'max_features': 0.33,       # Features pro Split
    'random_state': 456,        # Reproduzierbarkeit
    'n_jobs': -1,               # Alle CPUs nutzen
    'criterion': 'squared_error'
}
```

### **Feature Importance**
```python
# Feature Importance anzeigen
feature_importance = model.feature_importances_
feature_names = ['feature1', 'feature2', ...]

importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': feature_importance
}).sort_values('importance', ascending=False)
```

## 📊 W&B Integration

### **Run initialisieren**
```python
import wandb

run = wandb.init(
    job_type="train_random_forest",
    project="nyc_airbnb",
    group="experiment_1"
)
```

### **Metriken loggen**
```python
# Metriken loggen
run.log({
    'mae': mae,
    'r2': r2_score,
    'epoch': epoch
})

# Artifacts loggen
artifact = wandb.Artifact(
    'model', 
    type='model',
    description='Trained Random Forest'
)
artifact.add_file('model.pkl')
run.log_artifact(artifact)
```

### **Config loggen**
```python
# Konfiguration loggen
run.config.update({
    'learning_rate': 0.01,
    'batch_size': 32,
    'epochs': 100
})
```

## 🧪 Testing

### **Pytest Fixtures**
```python
@pytest.fixture(scope='session')
def data(request):
    run = wandb.init(job_type="data_tests")
    csv_artifact = request.config.option.csv
    data_path = run.use_artifact(csv_artifact).file()
    return pd.read_csv(data_path)
```

### **Tests ausführen**
```bash
# Alle Tests
pytest

# Spezifische Tests
pytest src/data_check/test_data.py

# Mit Parametern
pytest src/data_check/test_data.py --csv=clean_sample.csv:latest
```

## 🚀 Deployment

### **Docker**
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app.py"]
```

### **GitHub Release**
```bash
# Tag erstellen
git tag v1.0.1
git push origin v1.0.1

# Release mit GitHub CLI
gh release create v1.0.1 --title "Version 1.0.1" --notes "Bug fixes"
```

## 📚 Wichtige Links

### **Dokumentation**
- [Master Learning Guide](MASTER_LEARNING_GUIDE.md)
- [Next Steps](NEXT_STEPS.md)
- [Best Practices](BEST_PRACTICES.md)
- [Error Solutions](ERRORS_AND_SOLUTIONS.md)

### **Komponenten**
- [Basic Cleaning](basic_cleaning/CheatSheet.md)
- [Data Check](data_check/CheatSheet.md)
- [Train Random Forest](train_random_forest/CheatSheet.md)
- [Test Model](test_regression_model/CheatSheet.md)

### **Externe Ressourcen**
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [MLflow Documentation](https://mlflow.org/)
- [W&B Documentation](https://docs.wandb.ai/)
- [Pandas Documentation](https://pandas.pydata.org/)

## 🎯 Quick Wins

### **Performance verbessern**
1. **Feature Engineering** - Neue Features hinzufügen
2. **Hyperparameter Tuning** - Grid Search verwenden
3. **Feature Selection** - Unwichtige Features entfernen
4. **Ensemble Methods** - Mehrere Modelle kombinieren

### **Code-Qualität verbessern**
1. **Type Hints** - Alle Funktionen typisieren
2. **Docstrings** - Vollständige Dokumentation
3. **Tests** - Code Coverage erhöhen
4. **Logging** - Detailliertes Logging

### **Pipeline erweitern**
1. **Monitoring** - Model Performance überwachen
2. **Alerting** - Automatische Benachrichtigungen
3. **A/B Testing** - Modelle vergleichen
4. **AutoML** - Automatische Modellauswahl

---

**💡 Tipp:** Drucken Sie dieses CheatSheet aus und hängen Sie es an Ihren Arbeitsplatz!

**🔄 Letzte Aktualisierung:** September 2025
