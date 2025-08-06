# Detaillierte Erklärungen: Train Random Forest

## Hintergrund

Das Training von Machine Learning Modellen ist der Kern jeder ML-Pipeline. In dieser Komponente wird ein Random Forest Regressor trainiert, um Airbnb-Mietpreise in NYC vorherzusagen. Random Forest ist besonders geeignet für diese Aufgabe, da er:

*   **Robustheit:** Gut mit Ausreißern und Rauschen umgehen kann
*   **Feature-Importance:** Automatisch die Wichtigkeit von Features bestimmt
*   **Non-lineare Beziehungen:** Komplexe Beziehungen zwischen Features und Zielvariable erfasst
*   **Interpretierbarkeit:** Im Vergleich zu anderen Algorithmen relativ interpretierbar ist

Die Komponente implementiert eine vollständige ML-Pipeline mit Feature Engineering, Modelltraining, Evaluation und Artefakt-Management.

## Verwendete Methoden

### Scikit-learn Pipeline

Die `sklearn.pipeline.Pipeline` wird verwendet, um Feature Engineering und Modelltraining in einem einzigen, reproduzierbaren Workflow zu kombinieren. Dies bietet:

*   **Konsistenz:** Gleiche Transformationen werden auf Trainings- und Testdaten angewendet
*   **Reproduzierbarkeit:** Der gesamte Workflow kann als einheitliches Objekt gespeichert und geladen werden
*   **Effizienz:** Vermeidet Data Leakage durch korrekte Anwendung von `fit_transform` und `transform`
*   **Modularität:** Verschiedene Feature Engineering Schritte können einfach kombiniert werden

### Feature Engineering

#### TF-IDF für Textverarbeitung

Die `name`-Spalte enthält Beschreibungen der Airbnb-Listings. TF-IDF (Term Frequency-Inverse Document Frequency) wird verwendet, um diese Texte in numerische Features zu konvertieren:

```python
TfidfVectorizer(
    max_features=max_tfidf_features,
    stop_words='english',
    ngram_range=(1, 2)
)
```

*   **max_features:** Begrenzt die Anzahl der Features und verhindert Dimensionalitätsprobleme
*   **stop_words:** Entfernt häufige Wörter wie "the", "and", "is"
*   **ngram_range:** Berücksichtigt sowohl einzelne Wörter als auch Wortpaare

#### Kategorische Variablen

Kategorische Variablen werden mit verschiedenen Strategien behandelt:

*   **Ordinal Encoding:** Für Variablen mit natürlicher Ordnung (z.B. room_type)
*   **One-Hot Encoding:** Für nominale Variablen ohne natürliche Ordnung
*   **Simple Imputer:** Behandelt fehlende Werte in kategorischen Spalten

#### Datumsfeatures

Die `last_review`-Spalte wird in numerische Features umgewandelt:

```python
FunctionTransformer(delta_date_feature)
```

Diese Funktion berechnet die Anzahl der Tage seit dem letzten Review, was ein wichtiger Indikator für die Aktualität und Qualität eines Listings ist.

### Random Forest Regressor

Der Random Forest Algorithmus wird mit konfigurierbaren Hyperparametern aus der JSON-Konfigurationsdatei trainiert:

*   **n_estimators:** Anzahl der Bäume im Wald
*   **max_depth:** Maximale Tiefe jedes Baums
*   **min_samples_split:** Minimale Anzahl von Samples für einen Split
*   **min_samples_leaf:** Minimale Anzahl von Samples in einem Blatt
*   **max_features:** Anteil der Features, die bei jedem Split betrachtet werden
*   **criterion:** Verlustfunktion (squared_error für Regression)

### Modellbewertung

Die Modellleistung wird mit mehreren Metriken bewertet:

*   **R² Score:** Maß für die erklärte Varianz (0-1, höher ist besser)
*   **Mean Absolute Error (MAE):** Durchschnittlicher absoluter Fehler in Dollar
*   **Feature Importance:** Relative Wichtigkeit jedes Features für die Vorhersage

### Wandb Integration

Wandb wird für umfassendes Experiment-Tracking verwendet:

*   **Konfiguration:** Alle Hyperparameter werden protokolliert
*   **Metriken:** R² und MAE werden automatisch geloggt
*   **Artefakte:** Das trainierte Modell wird als versioniertes Artefakt gespeichert
*   **Visualisierungen:** Feature Importance Plots werden automatisch erstellt

## Funktionsanalyse: `go` Funktion in `run.py`

Die `go`-Funktion orchestriert den gesamten Modelltraining-Prozess:

1.  **W&B-Lauf initialisieren:**
    ```python
    run = wandb.init(job_type="train_random_forest")
    run.config.update(args)
    ```
    Ein neuer `wandb`-Lauf wird gestartet und die Konfigurationsparameter werden protokolliert.

2.  **Random Forest Konfiguration laden:**
    ```python
    with open(args.rf_config) as fp:
        rf_config = json.load(fp)
    run.config.update(rf_config)
    ```
    Die Hyperparameter werden aus der JSON-Datei geladen und in W&B protokolliert.

3.  **Trainingsdaten laden:**
    ```python
    trainval_local_path = run.use_artifact(args.trainval_artifact).file()
    X = pd.read_csv(trainval_local_path)
    y = X.pop("price")
    ```
    Die Trainingsdaten werden heruntergeladen und die Zielvariable (price) wird separiert.

4.  **Trainings-/Validierungssplit:**
    ```python
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, 
        test_size=args.val_size, 
        stratify=X[args.stratify_by], 
        random_state=args.random_seed
    )
    ```
    Die Daten werden stratifiziert aufgeteilt, um die Verteilung der Zielvariable zu erhalten.

5.  **Feature Engineering Pipeline erstellen:**
    ```python
    sk_pipe, processed_features = get_inference_pipeline(rf_config, args.max_tfidf_features)
    ```
    Eine vollständige Pipeline wird erstellt, die Feature Engineering und Modelltraining kombiniert.

6.  **Modell trainieren:**
    ```python
    sk_pipe.fit(X_train, y_train)
    ```
    Die Pipeline wird auf den Trainingsdaten trainiert.

7.  **Modell bewerten:**
    ```python
    r_squared = sk_pipe.score(X_val, y_val)
    y_pred = sk_pipe.predict(X_val)
    mae = mean_absolute_error(y_val, y_pred)
    ```
    Die Modellleistung wird auf dem Validierungssatz bewertet.

8.  **Feature Importance visualisieren:**
    ```python
    plot_feature_importance(sk_pipe, processed_features)
    ```
    Die Wichtigkeit der Features wird analysiert und visualisiert.

9.  **Modell speichern:**
    ```python
    mlflow.sklearn.save_model(sk_pipe, "random_forest_dir")
    ```
    Das trainierte Modell wird im MLflow-Format gespeichert.

10. **Artefakt hochladen:**
    ```python
    artifact = wandb.Artifact(
        args.output_artifact,
        type="model_export",
        description="Random Forest model for price prediction",
        metadata=rf_config
    )
    artifact.add_dir("random_forest_dir")
    run.log_artifact(artifact)
    ```
    Das Modell wird als W&B Artefakt hochgeladen und versioniert.

11. **Lauf beenden:**
    ```python
    run.finish()
    ```
    Der W&B-Lauf wird ordnungsgemäß beendet.

## Wichtige Konzepte

### Feature Engineering Pipeline

Die Pipeline kombiniert verschiedene Feature Engineering Schritte:

1.  **Textverarbeitung:** TF-IDF für die `name`-Spalte
2.  **Kategorische Variablen:** Encoding für `neighbourhood_group`, `room_type`, etc.
3.  **Numerische Variablen:** Standardisierung für `latitude`, `longitude`, etc.
4.  **Datumsfeatures:** Transformation der `last_review`-Spalte
5.  **Fehlende Werte:** Imputation für alle Spalten

### Stratifizierte Aufteilung

Die stratifizierte Aufteilung stellt sicher, dass die Verteilung der Zielvariable in Trainings- und Validierungssatz ähnlich ist. Dies ist besonders wichtig bei unausgewogenen Daten.

### Modellversionierung

Jedes trainierte Modell wird als versioniertes Artefakt gespeichert, was ermöglicht:
*   Verschiedene Modellversionen zu vergleichen
*   Zu früheren Modellversionen zurückzukehren
*   Modelle in nachfolgenden Pipeline-Schritten zu verwenden

### Hyperparameter-Optimierung

Die JSON-Konfigurationsdatei ermöglicht einfache Hyperparameter-Optimierung:
*   Verschiedene Konfigurationen können getestet werden
*   Ergebnisse werden automatisch in W&B protokolliert
*   Beste Konfiguration kann identifiziert werden 