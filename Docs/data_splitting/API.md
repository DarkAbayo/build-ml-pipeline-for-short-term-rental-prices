# Schnittstellenbeschreibung: Data Splitting

## Aufruf

Die `data_splitting`-Komponente wird über `mlflow run` aufgerufen. Dies ermöglicht die Ausführung der Komponente innerhalb einer MLflow-Pipeline, wobei die Parameter direkt über die Kommandozeile oder eine MLflow-Konfiguration übergeben werden können.

Beispiel für den Aufruf:

```bash
mlflow run . -P input_artifact="clean_sample.csv:latest" \
             -P test_size=0.3 \
             -P random_state=42 \
             -P stratify="price"
```

## Parameter

Die folgenden Parameter können beim Aufruf der `data_splitting`-Komponente übergeben werden:

| Parameter          | Typ    | Beschreibung                                                              |
| :----------------- | :----- | :------------------------------------------------------------------------ |
| `input_artifact`   | `string` | Name des Eingangsartefakts mit Versions-Tag (z.B. 'clean_sample.csv:latest') |
| `test_size`        | `float`  | Anteil der Daten für den Testsatz (z.B. 0.3 für 30%)                    |
| `random_state`     | `int`    | Seed für reproduzierbare Aufteilung (z.B. 42)                           |
| `stratify`         | `string` | Spalte für stratifizierte Aufteilung (z.B. 'price')                     | 