# API: Test Regression Model

## Funktionen

### `go(args)`
Hauptfunktion für das Testen des Modells.

**Parameter:**
- `args`: ArgumentParser-Objekt mit mlflow_model und test_dataset

**Rückgabe:** None

### `fix_column_transformer_compatibility(sk_pipe)`
Behebt Kompatibilitätsprobleme mit ColumnTransformer zwischen scikit-learn Versionen.

**Parameter:**
- `sk_pipe`: Sklearn Pipeline-Objekt

**Rückgabe:** None

## Kommandozeilen-Argumente

- `--mlflow_model`: Pfad zum MLflow-Modell (z.B. "random_forest_export:prod")
- `--test_dataset`: Pfad zum Testdatensatz (z.B. "test_data.csv:latest")

## Abhängigkeiten

- wandb: Für Experiment-Tracking
- mlflow: Für Modell-Laden
- pandas: Für Datenverarbeitung
- sklearn: Für Metriken und Kompatibilitätsfixes
