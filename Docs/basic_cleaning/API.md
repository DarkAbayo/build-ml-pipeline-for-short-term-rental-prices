# Schnittstellenbeschreibung: Basic Cleaning

## Aufruf

Die `basic_cleaning`-Komponente wird typischerweise über `mlflow run` aufgerufen. Dies ermöglicht die Ausführung der Komponente innerhalb einer MLflow-Pipeline, wobei die Parameter direkt über die Kommandozeile oder eine MLflow-Konfiguration übergeben werden können.

Beispiel für den Aufruf:

```bash
mlflow run . -P input_artifact="sample.csv:latest" \
             -P output_artifact="clean_sample.csv" \
             -P output_type="clean_sample" \
             -P output_description="Data with outliers removed" \
             -P min_price=10.0 \
             -P max_price=350.0
```

## Parameter

Die folgenden Parameter können beim Aufruf der `basic_cleaning`-Komponente übergeben werden:

| Parameter          | Typ    | Beschreibung                                                              |
| :----------------- | :----- | :------------------------------------------------------------------------ |
| `input_artifact`   | `string` | Name des Eingangsartefakts mit Versions-Tag (z.B. 'sample.csv:latest')    |
| `output_artifact`  | `string` | Name des Ausgangsartefakts (z.B. 'clean_sample.csv')                      |
| `output_type`      | `string` | Typklassifizierung für das Ausgangsartefakt (z.B. 'clean_sample')        |
| `output_description` | `string` | Beschreibung des Bereinigungsprozesses und der Ausgabedaten             |
| `min_price`        | `float`  | Minimaler Preisschwellenwert zum Filtern von Ausreißern (z.B. 10.0)     |
| `max_price`        | `float`  | Maximaler Preisschwellenwert zum Filtern von Ausreißern (z.B. 350.0)    |