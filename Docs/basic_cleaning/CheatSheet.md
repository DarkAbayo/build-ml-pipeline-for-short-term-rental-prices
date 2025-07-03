# Cheat Sheet: Basic Cleaning

## Essenz

Diese Komponente führt eine grundlegende Datenbereinigung für Airbnb-Mietpreisdaten durch. Sie entfernt Preis-Ausreißer und konvertiert Datentypen, um ein sauberes Dataset für nachfolgende Machine-Learning-Schritte zu erstellen und dieses als versioniertes `wandb` Artefakt zu protokollieren.

## Durchgeführte Schritte

*   Initialisierung eines `wandb`-Laufs zur Nachvollziehbarkeit.
*   Herunterladen des Rohdatensatzes als `wandb` Artefakt.
*   Laden der Daten in einen `pandas` DataFrame.
*   Entfernung von Preis-Ausreißern basierend auf konfigurierbaren Minimal- und Maximalwerten.
*   Konvertierung der Spalte `last_review` in das `datetime`-Format.
*   Speichern des bereinigten DataFrames als `clean_sample.csv`.
*   Hochladen der `clean_sample.csv` als neues `wandb` Artefakt mit spezifischem Namen, Typ und Beschreibung.
*   Beenden des `wandb`-Laufs.