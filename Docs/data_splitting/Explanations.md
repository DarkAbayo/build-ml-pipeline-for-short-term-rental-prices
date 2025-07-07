# Detaillierte Erklärungen: Data Splitting

## Hintergrund

Das Data Splitting ist ein fundamentaler Schritt in jeder Machine-Learning-Pipeline. Sein Hauptzweck ist es, die verfügbaren Daten in separate Sätze für Training, Validierung und Test aufzuteilen. Diese Aufteilung ist entscheidend für:

*   **Modellbewertung:** Ein separater Testsatz ermöglicht eine unvoreingenommene Bewertung der Modellleistung
*   **Überanpassungserkennung:** Ein Validierungssatz hilft bei der Erkennung von Overfitting während des Trainings
*   **Reproduzierbarkeit:** Durch feste Seeds wird sichergestellt, dass die Aufteilung konsistent bleibt
*   **Stratifizierung:** Bei unausgewogenen Daten kann eine stratifizierte Aufteilung die Verteilung der Zielvariable in allen Sätzen erhalten

In dieser Komponente konzentrieren wir uns auf die Aufteilung der bereinigten Airbnb-Daten in Trainings- und Testsätze, wobei besonderes Augenmerk auf die Reproduzierbarkeit und die Erhaltung der Datenverteilung gelegt wird.

## Verwendete Methoden

### Scikit-learn train_test_split

`sklearn.model_selection.train_test_split` ist die Standardmethode für die Aufteilung von Datensätzen in Machine-Learning-Projekten. Diese Funktion bietet:

*   **Flexibilität:** Verschiedene Aufteilungsstrategien (zufällig, stratifiziert, zeitbasiert)
*   **Reproduzierbarkeit:** Durch `random_state` Parameter wird die Aufteilung konsistent
*   **Stratifizierung:** Bei unausgewogenen Daten kann die Verteilung der Zielvariable erhalten werden
*   **Effizienz:** Optimierte Implementierung für große Datensätze

### Pandas

`pandas` wird für das Laden und Speichern der Daten verwendet:

*   **Datenladen:** `pd.read_csv()` zum Laden der bereinigten Daten
*   **Datenexport:** `df.to_csv()` zum Speichern der aufgeteilten Datensätze
*   **Dateninspektion:** Methoden wie `df.shape`, `df.head()` für Qualitätskontrolle

### Wandb Artifacts

`wandb` wird verwendet, um die aufgeteilten Datensätze zu versionieren und zu protokollieren:

*   **Versionierung:** Jede Aufteilung wird als separate Artefakte gespeichert
*   **Nachvollziehbarkeit:** Die verwendeten Parameter werden protokolliert
*   **Zentrale Speicherung:** Artefakte können von nachfolgenden Pipeline-Schritten verwendet werden

## Funktionsanalyse: `go` Funktion in `run.py`

Die `go`-Funktion orchestriert den gesamten Data-Splitting-Prozess:

1.  **W&B-Lauf initialisieren:**
    ```python
    run = wandb.init(job_type="data_splitting")
    run.config.update(args)
    ```
    Ein neuer `wandb`-Lauf wird gestartet und die Konfigurationsparameter werden protokolliert.

2.  **Eingangsartefakt herunterladen:**
    ```python
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    ```
    Das bereinigte Datensatz-Artefakt wird heruntergeladen.

3.  **Daten laden:**
    ```python
    df = pd.read_csv(artifact_local_path)
    ```
    Die bereinigten Daten werden in einen DataFrame geladen.

4.  **Stratifizierung vorbereiten:**
    ```python
    if args.stratify:
        # Erstelle Bins für stratifizierte Aufteilung
        df['price_bins'] = pd.cut(df[args.stratify], bins=10, labels=False)
        stratify_column = 'price_bins'
    else:
        stratify_column = None
    ```
    Falls eine Stratifizierung gewünscht ist, werden Bins für die Zielvariable erstellt. Dies ist besonders wichtig bei unausgewogenen Daten.

5.  **Daten aufteilen:**
    ```python
    train_df, test_df = train_test_split(
        df,
        test_size=args.test_size,
        random_state=args.random_state,
        stratify=stratify_column
    )
    ```
    Die Daten werden in Trainings- und Testsatz aufgeteilt. Die Parameter werden über die Kommandozeile konfiguriert.

6.  **Aufgeteilte Daten speichern:**
    ```python
    train_df.to_csv("train.csv", index=False)
    test_df.to_csv("test.csv", index=False)
    ```
    Die aufgeteilten Datensätze werden als separate CSV-Dateien gespeichert.

7.  **Artefakte hochladen:**
    ```python
    # Trainingsdaten als Artefakt
    train_artifact = wandb.Artifact(
        "train.csv",
        type="train_data",
        description="Training dataset"
    )
    train_artifact.add_file("train.csv")
    run.log_artifact(train_artifact)

    # Testdaten als Artefakt
    test_artifact = wandb.Artifact(
        "test.csv", 
        type="test_data",
        description="Test dataset"
    )
    test_artifact.add_file("test.csv")
    run.log_artifact(test_artifact)
    ```
    Beide Datensätze werden als separate `wandb` Artefakte hochgeladen und versioniert.

8.  **Lauf beenden:**
    ```python
    run.finish()
    ```
    Der `wandb`-Lauf wird ordnungsgemäß beendet.

## Wichtige Konzepte

### Stratifizierte Aufteilung

Bei unausgewogenen Daten (z.B. wenige teure Wohnungen) kann eine einfache zufällige Aufteilung dazu führen, dass der Testsatz nicht repräsentativ ist. Die stratifizierte Aufteilung stellt sicher, dass die Verteilung der Zielvariable in beiden Sätzen ähnlich ist.

### Reproduzierbarkeit

Durch die Verwendung eines festen `random_state` wird sichergestellt, dass die Aufteilung bei wiederholter Ausführung identisch bleibt. Dies ist entscheidend für die Reproduzierbarkeit von Experimenten.

### Artefakt-Versionierung

Jede Aufteilung wird als separate Artefakte gespeichert, was es ermöglicht:
*   Verschiedene Aufteilungsstrategien zu vergleichen
*   Zu früheren Versionen zurückzukehren
*   Die Aufteilung in nachfolgenden Pipeline-Schritten zu referenzieren 