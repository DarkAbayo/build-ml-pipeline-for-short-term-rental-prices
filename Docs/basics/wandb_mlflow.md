# Wandb und MLflow für ML-Projekte

## Was ist Wandb (Weights & Biases)?

Wandb ist ein Tool für Experiment-Tracking und -Management in Machine Learning. Es hilft dir dabei, deine ML-Experimente zu verfolgen, zu vergleichen und zu reproduzieren.

### Warum verwenden wir Wandb?

1. **Experiment-Tracking** - Alle Experimente werden automatisch protokolliert
2. **Vergleich** - Du kannst verschiedene Modelle und Parameter vergleichen
3. **Reproduzierbarkeit** - Jedes Experiment kann exakt wiederholt werden
4. **Visualisierung** - Automatische Grafiken und Dashboards
5. **Kollaboration** - Team-Mitglieder können Experimente teilen

## Grundlegende Wandb-Konzepte

### 1. Run (Lauf)

Ein "Run" ist ein einzelnes Experiment:

```python
import wandb

# Run starten
run = wandb.init(
    project="airbnb_price_prediction",
    name="experiment_001",
    config={
        "learning_rate": 0.01,
        "epochs": 100,
        "batch_size": 32
    }
)

# Metriken loggen
for epoch in range(100):
    train_loss = 0.5  # Simulierte Metrik
    val_loss = 0.4    # Simulierte Metrik
    
    wandb.log({
        "train_loss": train_loss,
        "val_loss": val_loss,
        "epoch": epoch
    })

# Run beenden
run.finish()
```

### 2. Config (Konfiguration)

Die Config speichert die Parameter deines Experiments:

```python
# Config beim Start definieren
run = wandb.init(
    project="my_project",
    config={
        "model_type": "random_forest",
        "max_depth": 10,
        "n_estimators": 100,
        "test_size": 0.2,
        "random_state": 42
    }
)

# Config während des Laufs verwenden
config = run.config
print(f"Model: {config.model_type}")
print(f"Max Depth: {config.max_depth}")
```

### 3. Logging (Protokollierung)

Metriken und Daten werden mit `wandb.log()` protokolliert:

```python
# Einzelne Werte loggen
wandb.log({"accuracy": 0.95})

# Mehrere Werte gleichzeitig loggen
wandb.log({
    "train_loss": 0.3,
    "val_loss": 0.25,
    "accuracy": 0.92,
    "learning_rate": 0.001
})

# Listen von Werten loggen
for epoch in range(10):
    wandb.log({
        "epoch": epoch,
        "loss": 0.5 - epoch * 0.05,  # Simulierte Abnahme
        "accuracy": 0.8 + epoch * 0.02  # Simulierte Zunahme
    })
```

## Artefakte (Artifacts)

Artefakte sind Dateien, die du in Wandb speichern kannst:

### Artefakte hochladen

```python
import pandas as pd

# Daten als Artefakt speichern
data = pd.DataFrame({
    'price': [100, 150, 200],
    'location': ['Manhattan', 'Brooklyn', 'Queens']
})

# Lokale Datei erstellen
data.to_csv("processed_data.csv", index=False)

# Als Artefakt hochladen
artifact = wandb.Artifact(
    name="processed_data",
    type="dataset",
    description="Processed Airbnb data"
)
artifact.add_file("processed_data.csv")
wandb.log_artifact(artifact)
```

### Artefakte herunterladen

```python
# Artefakt herunterladen
artifact = run.use_artifact("processed_data:latest")
data_path = artifact.file()

# Daten laden
df = pd.read_csv(data_path)
print(df.head())
```

## Was ist MLflow?

MLflow ist ein Tool für die Orchestrierung von ML-Pipelines. Es hilft dabei, komplexe Workflows zu verwalten und zu reproduzieren.

### Warum verwenden wir MLflow?

1. **Pipeline-Orchestrierung** - Automatische Ausführung von Pipeline-Schritten
2. **Reproduzierbarkeit** - Jeder Schritt kann exakt wiederholt werden
3. **Parameter-Management** - Zentrale Verwaltung von Konfigurationen
4. **Artefakt-Tracking** - Automatische Versionierung von Daten und Modellen

## MLflow-Konzepte

### 1. MLproject

Eine `MLproject` Datei definiert eine MLflow-Komponente:

```yaml
# MLproject
name: data_cleaning

conda_env: conda.yml

entry_points:
  main:
    parameters:
      input_artifact: {type: string, default: "raw_data.csv:latest"}
      output_artifact: {type: string, default: "clean_data.csv"}
      min_price: {type: float, default: 10.0}
      max_price: {type: float, default: 1000.0}
    command: "python run.py"
```

### 2. Pipeline-Ausführung

```bash
# Einzelne Komponente ausführen
mlflow run src/data_cleaning -P input_artifact="raw_data.csv:latest"

# Mit Parametern
mlflow run src/data_cleaning \
  -P input_artifact="raw_data.csv:latest" \
  -P output_artifact="clean_data.csv" \
  -P min_price=10.0 \
  -P max_price=1000.0
```

### 3. Komponenten-Struktur

Eine MLflow-Komponente hat typischerweise diese Struktur:

```
src/data_cleaning/
├── MLproject          # Komponenten-Definition
├── conda.yml          # Abhängigkeiten
├── run.py             # Hauptlogik
└── README.md          # Dokumentation
```

## Praktische Beispiele

### 1. Einfache Wandb-Integration

```python
import wandb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Run starten
run = wandb.init(
    project="airbnb_price_prediction",
    config={
        "test_size": 0.2,
        "random_state": 42,
        "n_estimators": 100,
        "max_depth": 10
    }
)

# Daten laden
df = pd.read_csv("airbnb_data.csv")

# Daten aufteilen
X = df.drop('price', axis=1)
y = df['price']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=run.config.test_size,
    random_state=run.config.random_state
)

# Modell trainieren
model = RandomForestRegressor(
    n_estimators=run.config.n_estimators,
    max_depth=run.config.max_depth,
    random_state=run.config.random_state
)
model.fit(X_train, y_train)

# Vorhersagen
y_pred = model.predict(X_test)

# Metriken berechnen und loggen
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5

wandb.log({
    "mse": mse,
    "rmse": rmse,
    "feature_importance": dict(zip(X.columns, model.feature_importances_))
})

# Modell als Artefakt speichern
import joblib
joblib.dump(model, "model.pkl")

artifact = wandb.Artifact(
    name="price_prediction_model",
    type="model",
    description="Random Forest model for price prediction"
)
artifact.add_file("model.pkl")
wandb.log_artifact(artifact)

run.finish()
```

### 2. MLflow-Komponente

```python
# run.py in einer MLflow-Komponente
import argparse
import wandb
import pandas as pd
from sklearn.model_selection import train_test_split

def go(args):
    """Hauptfunktion der Komponente"""
    
    # W&B Run starten
    run = wandb.init(job_type="data_splitting")
    run.config.update(args)
    
    # Artefakt herunterladen
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)
    
    # Daten aufteilen
    train_df, test_df = train_test_split(
        df,
        test_size=args.test_size,
        random_state=args.random_state
    )
    
    # Daten speichern
    train_df.to_csv("train.csv", index=False)
    test_df.to_csv("test.csv", index=False)
    
    # Als Artefakte hochladen
    train_artifact = wandb.Artifact(
        "train.csv",
        type="train_data",
        description="Training dataset"
    )
    train_artifact.add_file("train.csv")
    run.log_artifact(train_artifact)
    
    test_artifact = wandb.Artifact(
        "test.csv",
        type="test_data", 
        description="Test dataset"
    )
    test_artifact.add_file("test.csv")
    run.log_artifact(test_artifact)
    
    run.finish()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_artifact", type=str, required=True)
    parser.add_argument("--test_size", type=float, default=0.2)
    parser.add_argument("--random_state", type=int, default=42)
    
    args = parser.parse_args()
    go(args)
```

## Best Practices

### 1. Sinnvolle Run-Namen

```python
# Gut
run = wandb.init(
    project="airbnb_pricing",
    name="random_forest_depth10_estimators100"
)

# Schlecht
run = wandb.init(
    project="project",
    name="test"
)
```

### 2. Strukturierte Configs

```python
# Gut - Gruppierte Parameter
run = wandb.init(
    config={
        "data": {
            "test_size": 0.2,
            "random_state": 42
        },
        "model": {
            "type": "random_forest",
            "n_estimators": 100,
            "max_depth": 10
        },
        "training": {
            "epochs": 100,
            "batch_size": 32
        }
    }
)
```

### 3. Regelmäßiges Logging

```python
# Logge in regelmäßigen Abständen
for epoch in range(100):
    if epoch % 10 == 0:  # Alle 10 Epochen
        wandb.log({
            "epoch": epoch,
            "loss": current_loss,
            "accuracy": current_accuracy
        })
```

### 4. Artefakt-Versionierung

```python
# Verwende Versionierung für Artefakte
artifact = wandb.Artifact(
    name="model_v1",  # Version im Namen
    type="model",
    description="Random Forest model v1.0"
)
```

## Häufige Fehler und Lösungen

### 1. Wandb nicht initialisiert

```python
# Problem
wandb.log({"accuracy": 0.95})  # Fehler!

# Lösung
run = wandb.init(project="my_project")
wandb.log({"accuracy": 0.95})
```

### 2. Config-Zugriff

```python
# Problem
config = run.config
print(config.undefined_param)  # Fehler!

# Lösung
config = run.config
if hasattr(config, 'undefined_param'):
    print(config.undefined_param)
else:
    print("Parameter nicht definiert")
```

### 3. Artefakt-Pfade

```python
# Problem
artifact = run.use_artifact("nonexistent:latest")  # Fehler!

# Lösung
try:
    artifact = run.use_artifact("my_artifact:latest")
except Exception as e:
    print(f"Artefakt nicht gefunden: {e}")
```

## Nächste Schritte

Nachdem du Wandb und MLflow verstanden hast, kannst du:

1. **Scikit-learn lernen** - Für Machine Learning Algorithmen
2. **Feature Engineering verstehen** - Für bessere Modelle
3. **Hyperparameter-Tuning** - Für optimale Parameter

Wandb und MLflow sind die Grundlage für professionelle ML-Experimente! 