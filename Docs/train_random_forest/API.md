# Schnittstellenbeschreibung: Train Random Forest

## Aufruf

Die `train_random_forest`-Komponente wird über `mlflow run` aufgerufen. Dies ermöglicht die Ausführung der Komponente innerhalb einer MLflow-Pipeline, wobei die Parameter direkt über die Kommandozeile oder eine MLflow-Konfiguration übergeben werden können.

Beispiel für den Aufruf:

```bash
mlflow run src/train_random_forest -P trainval_artifact="trainval_data.csv:latest" \
                                   -P val_size=0.2 \
                                   -P random_seed=42 \
                                   -P stratify_by="neighbourhood_group" \
                                   -P rf_config="rf_config.json" \
                                   -P max_tfidf_features=10 \
                                   -P output_artifact="random_forest_export"
```

## Parameter

Die folgenden Parameter können beim Aufruf der `train_random_forest`-Komponente übergeben werden:

| Parameter          | Typ    | Beschreibung                                                              |
| :----------------- | :----- | :------------------------------------------------------------------------ |
| `trainval_artifact` | `string` | Name des Trainingsartefakts mit Versions-Tag (z.B. 'trainval_data.csv:latest') |
| `val_size`        | `float`  | Anteil der Daten für die Validierung (z.B. 0.2 für 20%)                |
| `random_seed`     | `int`    | Seed für reproduzierbare Ergebnisse (z.B. 42)                           |
| `stratify_by`     | `string` | Spalte für stratifizierte Aufteilung (z.B. 'neighbourhood_group')       |
| `rf_config`       | `string` | Pfad zur JSON-Datei mit Random Forest Konfiguration                     |
| `max_tfidf_features` | `int` | Maximale Anzahl TF-IDF Features für Textverarbeitung (z.B. 10)         |
| `output_artifact` | `string` | Name des Ausgangsartefakts für das trainierte Modell (z.B. 'random_forest_export') | 