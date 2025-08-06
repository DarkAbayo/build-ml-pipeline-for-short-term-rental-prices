# Cheat Sheet: Train Random Forest

## Essenz

Diese Komponente trainiert ein Random Forest Modell für die Vorhersage von Airbnb-Mietpreisen in NYC. Sie verwendet Feature Engineering (TF-IDF für Text, Datumsfeatures), stratifizierte Aufteilung und umfassende Modellbewertung mit Metriken und Visualisierungen.

## Durchgeführte Schritte

*   Initialisierung eines `wandb`-Laufs zur Nachvollziehbarkeit
*   Herunterladen des Trainingsdatensatzes als `wandb` Artefakt
*   Laden der Daten in einen `pandas` DataFrame
*   Aufteilung in Trainings- und Validierungssatz mit stratifizierter Aufteilung
*   Feature Engineering Pipeline erstellen (TF-IDF, Datumsfeatures, kategorische Variablen)
*   Random Forest Modell mit konfigurierbaren Hyperparametern trainieren
*   Modellbewertung mit R² und Mean Absolute Error (MAE)
*   Feature Importance Analyse und Visualisierung
*   Speichern des trainierten Modells im MLflow-Format
*   Hochladen des Modells als `wandb` Artefakt mit Metadaten
*   Beenden des `wandb`-Laufs

## Wichtige Parameter

*   `trainval_artifact`: Eingangsdaten für Training und Validierung
*   `val_size`: Anteil der Daten für Validierung (z.B. 0.2)
*   `random_seed`: Seed für reproduzierbare Ergebnisse
*   `stratify_by`: Spalte für stratifizierte Aufteilung
*   `rf_config`: JSON-Datei mit Random Forest Hyperparametern
*   `max_tfidf_features`: Maximale Anzahl TF-IDF Features für Textverarbeitung
*   `output_artifact`: Name des Ausgangsartefakts für das trainierte Modell 