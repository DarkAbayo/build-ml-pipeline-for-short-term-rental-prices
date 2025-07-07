# Cheat Sheet: Data Splitting

## Essenz

Diese Komponente teilt die bereinigten Daten in Trainings- und Testsätze auf. Sie verwendet stratifizierte Aufteilung für unausgewogene Daten und speichert die aufgeteilten Datensätze als versionierte `wandb` Artefakte.

## Durchgeführte Schritte

*   Initialisierung eines `wandb`-Laufs zur Nachvollziehbarkeit
*   Herunterladen des bereinigten Datensatzes als `wandb` Artefakt
*   Laden der Daten in einen `pandas` DataFrame
*   Vorbereitung der Stratifizierung (falls gewünscht) durch Erstellung von Preis-Bins
*   Aufteilung der Daten mit `sklearn.model_selection.train_test_split`
*   Speichern der Trainings- und Testdaten als separate CSV-Dateien
*   Hochladen beider Datensätze als separate `wandb` Artefakte
*   Beenden des `wandb`-Laufs

## Wichtige Parameter

*   `test_size`: Anteil der Daten für den Testsatz (z.B. 0.3 für 30%)
*   `random_state`: Seed für reproduzierbare Aufteilung
*   `stratify`: Spalte für stratifizierte Aufteilung (z.B. 'price') 