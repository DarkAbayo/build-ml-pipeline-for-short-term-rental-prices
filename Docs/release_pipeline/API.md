# API: Release Pipeline

## GitHub Commands

### Release erstellen
```bash
git tag -a v1.0.0 -m "Release 1.0.0 with optimized hyperparameters"
git push origin v1.0.0
```

### Release testen
```bash
mlflow run https://github.com/[username]/build-ml-pipeline-for-short-term-rental-prices.git \
  -v v1.0.0 \
  -P hydra_options="etl.sample='sample2.csv'"
```

## Konfiguration

### config.yaml Updates
- Beste Hyperparameter eintragen
- Random Seed für Reproduzierbarkeit
- Optimale TF-IDF Features
