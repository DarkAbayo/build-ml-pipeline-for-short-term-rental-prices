# Schnittstellenbeschreibung: Data Check

## Aufruf
Die Data-Check-Komponente wird über `mlflow run` aufgerufen. Der Aufruf erfolgt typischerweise aus dem Hauptverzeichnis des Projekts und referenziert den Pfad zur Komponente. Die benötigten Parameter werden direkt als Argumente übergeben.

Beispielaufruf:
```bash
mlflow run src/data_check -P csv=data/my_input.csv -P ref=data/my_reference.csv -P kl_threshold=0.1 -P min_price=10.0 -P max_price=1000.0
```

## Parameter
Die folgenden Parameter können beim Aufruf der Komponente übergeben werden, wie in der `MLproject`-Datei definiert:

| Parameter    | Typ    | Beschreibung                                                              |
| :----------- | :----- | :------------------------------------------------------------------------ |
| `csv`        | string | Input CSV-Datei, die getestet werden soll.                                |
| `ref`        | string | Referenz-CSV-Datei zum Vergleich mit der neuen CSV-Datei.                 |
| `kl_threshold` | float  | Schwellenwert für den KL-Divergenztest in der Spalte 'neighborhood group'. |
| `min_price`  | float  | Minimal akzeptierter Preis.                                               |
| `max_price`  | float  | Maximal akzeptierter Preis.                                               |