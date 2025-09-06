# Cheat Sheet: Test Regression Model

## Essenz

Diese Komponente testet das beste trainierte Modell gegen den Testdatensatz und evaluiert die finale Performance. Sie lädt das als "prod" markierte Modell aus W&B, führt Vorhersagen durch und berechnet finale Metriken.

## Durchgeführte Schritte

*   Initialisierung eines `wandb`-Laufs zur Nachvollziehbarkeit
*   Herunterladen des als "prod" markierten Modells als `wandb` Artefakt
*   Herunterladen des Testdatensatzes als `wandb` Artefakt
*   Laden der Testdaten in einen `pandas` DataFrame
*   Kompatibilitätsfix für scikit-learn Versionsinkompatibilitäten
*   Modell-Laden mit MLflow und Warnungs-Unterdrückung
*   Vorhersagen auf dem Testdatensatz durchführen
*   Berechnung von R² Score und Mean Absolute Error (MAE)
*   Logging der Ergebnisse in W&B
*   Beenden des `wandb`-Laufs

## Wichtige Parameter

*   `mlflow_model`: "random_forest_export:prod" - Das zu testende Modell
*   `test_dataset`: "test_data.csv:latest" - Der Testdatensatz

## Ausgabe

*   R² Score (0-1, höher ist besser)
*   Mean Absolute Error (MAE) in Dollar
*   Logs in W&B für Tracking und Visualisierung

## Kompatibilitätsprobleme

Diese Komponente enthält Workarounds für scikit-learn Versionsinkompatibilitäten zwischen 1.7.0 und 1.3.2.
