# Errors & Solutions - ML-Pipeline Troubleshooting

## 1. MLflow Experiment Errors

### Error: `Could not find experiment with ID 0`

**Symptome:**
```
mlflow.exceptions.MlflowException: Could not find experiment with ID 0
```

**Ursache:** MLflow-Experiment wurde gelöscht oder beschädigt

**Lösung:**
```bash
# MLflow-Runs löschen
rm -rf mlruns/

# Neues Experiment erstellen
mlflow experiments create --experiment-name development

# Test erneut ausführen
mlflow run . -P steps=test_regression_model
```

## 2. Scikit-learn Versionsinkompatibilität

### Error: `AttributeError: 'ColumnTransformer' object has no attribute '_name_to_fitted_passthrough'`

**Symptome:**
```
AttributeError: 'ColumnTransformer' object has no attribute '_name_to_fitted_passthrough'
```

**Ursache:** Modell wurde mit scikit-learn 1.7.0 trainiert, aber Testumgebung verwendet 1.3.2

**Lösung:**
```python
# Workaround in test_regression_model/run.py
def fix_column_transformer_compatibility(sk_pipe):
    try:
        preprocessor = sk_pipe.named_steps['preprocessor']
        if hasattr(preprocessor, 'transformers_') and not hasattr(preprocessor, '_name_to_fitted_passthrough'):
            preprocessor._name_to_fitted_passthrough = {}
    except Exception as e:
        logger.warning(f"Could not fix ColumnTransformer compatibility: {e}")
```

## 3. MLflow Cache Probleme

### Error: MLflow verwendet falsche scikit-learn Version

**Symptome:**
```
InconsistentVersionWarning: Trying to unpickle estimator from version 1.7.0 when using version 1.3.2
```

**Ursache:** MLflow cached Umgebung mit falscher Version

**Lösung:**
```bash
# MLflow-Umgebungen löschen
conda env list | grep mlflow | awk '{print $1}' | xargs -I {} conda env remove -n {} -y

# Pipeline erneut ausführen
mlflow run . -P steps=test_regression_model
```

## 4. W&B Model Promotion

### Error: Modell nicht als "prod" markiert

**Symptome:**
```
Error: Model not found or not promoted to production
```

**Lösung:**
1. Gehe zu W&B: https://wandb.ai/dark_pn-private/nyc_airbnb
2. Finde das beste Modell (niedrigster MAE)
3. Klicke auf das Modell → "Artifacts"
4. Klicke auf "random_forest_export" → "Add tag" → "prod"

## 5. Speicherplatz-Probleme

### Error: System voll nach Hyperparameter-Optimierung

**Symptome:**
- WSL läuft langsam
- Kein Speicherplatz verfügbar

**Lösung:**
```bash
# Größte Verzeichnisse finden
du -sh ~/* | sort -hr | head -10

# MLflow-Umgebungen löschen
conda env list | grep mlflow | awk '{print $1}' | xargs -I {} conda env remove -n {} -y

# W&B Cache bereinigen
rm -rf ~/.cache/wandb/old-runs/
```

## 6. Hydra-Konfigurationsfehler

### Error: Falsche Hydra-Syntax

**Symptome:**
```
Error: Missing option '--experiment-name' / '-n'
```

**Lösung:**
```bash
# Korrekte Syntax
mlflow experiments create --experiment-name development

# Oder mit -n Flag
mlflow experiments create -n development
```

## 7. GitHub vs. Lokale Komponenten

### Error: GitHub-Komponente verwendet alte Version

**Symptome:**
```
=== Fetching project from https://github.com/udacity/build-ml-pipeline-for-short-term-rental-prices#components/test_regression_model
```

**Lösung:**
```bash
# Lokale Komponente erstellen
mkdir -p src/test_regression_model
cp components/test_regression_model/* src/test_regression_model/

# main.py anpassen für lokalen Pfad
# Ändern von:
# f"{config['main']['components_repository']}/test_regression_model"
# zu:
# os.path.join(hydra.utils.get_original_cwd(), "src", "test_regression_model")
```

## 8. Conda-Umgebungsprobleme

### Error: Umgebung nicht gefunden

**Symptome:**
```
conda: command not found
```

**Lösung:**
```bash
# Conda initialisieren
source ~/miniconda3/etc/profile.d/conda.sh

# Umgebung aktivieren
conda activate nyc_airbnb_dev
```

## 9. WSL Remote-Zugang Probleme

### Error: Falsche Umgebungsvariablen in WSL Remote

**Symptome:**
- Terminal-Befehle zeigen andere Werte als direktes WSL
- Umgebungen sind unterschiedlich

**Lösung:**
- Verwende direktes WSL Terminal statt VS Code/Cursor Remote
- Oder verwende WSL Remote nur für Code-Editing, nicht für Terminal-Befehle

## 10. Python-Versionsinkonsistenz

### Error: Unterschiedliche Python-Versionen

**Symptome:**
- Einige Komponenten verwenden `python=3.10`
- Andere verwenden `python=3.10.0`

**Lösung:**
```yaml
# Alle conda.yml Dateien vereinheitlichen
dependencies:
  - python=3.10.0  # Präzise Version verwenden
```

## 11. Hyperparameter-Optimierung Speicherprobleme

### Error: Zu viele Experimente führen zu Speicherproblemen

**Symptome:**
- WSL wird langsam
- Kein Speicherplatz verfügbar
- Pipeline bricht ab

**Lösung:**
```bash
# Reduzierte Experimente
mlflow run . \
  -P steps=train_random_forest \
  -P hydra_options="modeling.max_tfidf_features=10,15 modeling.random_forest.max_features=0.33,0.5 -m"

# Oder schrittweise Experimente
mlflow run . -P steps=train_random_forest -P hydra_options="modeling.random_forest.n_estimators=100,200 -m"
mlflow run . -P steps=train_random_forest -P hydra_options="modeling.random_forest.max_depth=10,50 -m"
```

## 12. Release Pipeline Fehler

### Error: Release funktioniert nicht mit neuen Daten

**Symptome:**
```
test_proper_boundaries failed
```

**Lösung:**
- Das ist ein "erfolgreicher Fehler" - der Test hat ein Problem in den neuen Daten erkannt
- Prüfe die Datenqualität
- Erstelle neue Release-Version (v1.0.1, v1.0.2, etc.)

## Präventive Maßnahmen

1. **Regelmäßige Cache-Bereinigung**
2. **Versionskonsistenz prüfen**
3. **Lokale Komponenten für Workarounds**
4. **Detailliertes Logging**
5. **Systematische Fehlerdokumentation**
6. **Schrittweise Experimente**
7. **Release-Testing mit verschiedenen Daten**
