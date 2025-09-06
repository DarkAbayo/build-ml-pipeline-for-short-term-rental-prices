# Detaillierte Erklärungen: Test Regression Model

## Hintergrund

Das Testen von Machine Learning Modellen ist ein kritischer Schritt in jeder ML-Pipeline. Diese Komponente evaluiert die finale Performance des besten trainierten Modells gegen einen ungesehenen Testdatensatz. Dies ist entscheidend für:

*   **Modellvalidierung**: Überprüfung der Generalisierungsfähigkeit
*   **Performance-Messung**: Finale Metriken für Produktionsentscheidungen
*   **Qualitätssicherung**: Sicherstellung der Modellqualität vor Deployment

## Verwendete Methoden

### MLflow Modell-Laden

MLflow wird verwendet, um das trainierte Modell zu laden:

```python
sk_pipe = mlflow.sklearn.load_model(model_local_path)
```

**Vorteile:**
*   **Standardisiertes Format**: Konsistente Modell-Serialisierung
*   **Metadaten-Erhaltung**: Behält alle Trainings-Informationen
*   **Reproduzierbarkeit**: Gleiche Modellversion kann wiederholt geladen werden

### Kompatibilitätsfix für scikit-learn

Aufgrund von Versionsinkompatibilitäten zwischen scikit-learn 1.7.0 (Training) und 1.3.2 (Testing) wurde ein Workaround implementiert:

```python
def fix_column_transformer_compatibility(sk_pipe):
    preprocessor = sk_pipe.named_steps['preprocessor']
    if not hasattr(preprocessor, '_name_to_fitted_passthrough'):
        preprocessor._name_to_fitted_passthrough = {}
```

**Problem:** ColumnTransformer in scikit-learn 1.7.0 hat das `_name_to_fitted_passthrough` Attribut entfernt
**Lösung:** Manuelles Hinzufügen des fehlenden Attributs

### Warnungs-Unterdrückung

Sklearn Versionswarnungen werden unterdrückt, um die Ausführung nicht zu stören:

```python
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")
    sk_pipe = mlflow.sklearn.load_model(model_local_path)
```

### Modellbewertung

Die finale Modellbewertung erfolgt mit zwei Metriken:

*   **R² Score**: Maß für die erklärte Varianz (0-1, höher ist besser)
*   **Mean Absolute Error (MAE)**: Durchschnittlicher absoluter Fehler in Dollar

```python
r_squared = sk_pipe.score(X_test, y_test)
mae = mean_absolute_error(y_test, y_pred)
```

## Funktionsanalyse: `go` Funktion

### 1. **W&B Initialisierung**
```python
run = wandb.init(job_type="test_model")
```
*   Erstellt einen neuen W&B-Run für das Testing
*   Ermöglicht Tracking der Test-Ergebnisse

### 2. **Artefakt-Download**
```python
model_local_path = run.use_artifact(args.mlflow_model).download()
test_dataset_path = run.use_artifact(args.test_dataset).file()
```
*   Lädt das als "prod" markierte Modell
*   Lädt den Testdatensatz

### 3. **Datenvorbereitung**
```python
X_test = pd.read_csv(test_dataset_path)
y_test = X_test.pop("price")
```
*   Lädt Testdaten in DataFrame
*   Trennt Features (X) und Zielvariable (y)

### 4. **Modell-Laden mit Kompatibilitätsfix**
```python
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")
    sk_pipe = mlflow.sklearn.load_model(model_local_path)

fix_column_transformer_compatibility(sk_pipe)
```
*   Lädt Modell mit unterdrückten Warnungen
*   Wendet Kompatibilitätsfix an

### 5. **Vorhersage und Bewertung**
```python
y_pred = sk_pipe.predict(X_test)
r_squared = sk_pipe.score(X_test, y_test)
mae = mean_absolute_error(y_test, y_pred)
```
*   Führt Vorhersagen durch
*   Berechnet finale Metriken

### 6. **Ergebnis-Logging**
```python
run.summary['r2'] = r_squared
run.summary['mae'] = mae
```
*   Loggt Ergebnisse in W&B
*   Ermöglicht Tracking und Visualisierung

## Wichtige Aspekte

### Modell-Promotion

Das zu testende Modell muss in W&B als "prod" markiert sein:
1. Gehe zu W&B: https://wandb.ai/dark_pn-private/nyc_airbnb
2. Finde das beste Modell (niedrigster MAE)
3. Klicke auf das Modell → "Artifacts"
4. Klicke auf "random_forest_export" → "Add tag" → "prod"

### Versionsinkompatibilitäten

Das Problem entsteht, wenn:
*   **Training**: scikit-learn 1.7.0 verwendet
*   **Testing**: scikit-learn 1.3.2 verwendet
*   **Lösung**: Workaround in der Komponente implementiert

### Lokale vs. Remote Komponenten

**Problem:** MLflow lädt GitHub-Komponente statt lokaler Version
**Lösung:** Lokale Komponente erstellen und main.py anpassen

## Best Practices

1. **Immer "prod" Modell testen**: Nur finale Modelle evaluieren
2. **Kompatibilitätsfixes dokumentieren**: Workarounds für zukünftige Referenz
3. **Detailliertes Logging**: Alle Metriken in W&B tracken
4. **Warnungs-Unterdrückung**: Saubere Ausführung ohne Störungen
5. **Lokale Komponenten**: Für Custom-Fixes verwenden

## Troubleshooting

### Häufige Probleme

1. **Modell nicht als "prod" markiert**: In W&B als "prod" taggen
2. **Versionsinkompatibilität**: Workaround in Komponente implementiert
3. **MLflow Cache-Probleme**: Umgebungen löschen und neu erstellen
4. **GitHub vs. lokale Komponenten**: Lokale Version verwenden

### Debugging-Schritte

1. Prüfe W&B für "prod" Modell
2. Prüfe scikit-learn Versionen
3. Prüfe MLflow-Cache
4. Prüfe lokale vs. remote Komponenten
