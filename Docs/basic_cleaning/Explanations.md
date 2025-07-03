# Detaillierte Erklärungen: Basic Cleaning

## Hintergrund

Die Datenbereinigung ist ein entscheidender Schritt in jeder Machine-Learning-Pipeline. Ihr Hauptzweck ist es, die Qualität der Rohdaten zu verbessern, indem Inkonsistenzen, Fehler und fehlende Werte behoben werden. Unbereinigte Daten können zu ungenauen Modellen, verzerrten Vorhersagen und ineffizienten Analysen führen.

In dieser Komponente konzentrieren wir uns auf grundlegende Bereinigungsvorgänge, die für die Vorhersage von Airbnb-Mietpreisen in NYC unerlässlich sind:

*   **Umgang mit fehlenden Werten:** Obwohl in diesem spezifischen Modul keine explizite Imputation oder Entfernung fehlender Werte für alle Spalten durchgeführt wird, ist es ein allgemeiner Aspekt der Datenbereinigung. Die `last_review`-Spalte wird in ein Datumsformat konvertiert, was implizit den Umgang mit nicht-konvertierbaren oder fehlenden Werten erfordert (Pandas behandelt diese oft als `NaT` - Not a Time).
*   **Korrektur von Datentypen:** Die Spalte `last_review` wird von einem generischen Objekttyp in ein `datetime`-Format umgewandelt, was für zeitbasierte Analysen und Feature Engineering unerlässlich ist.
*   **Entfernung von Ausreißern:** Preis-Ausreißer, die außerhalb eines definierten Bereichs liegen, werden entfernt, um die Modellleistung nicht durch extreme Werte zu verzerren.

## Verwendete Methoden

### Pandas

`pandas` ist das zentrale Werkzeug in diesem Modul für die Datenmanipulation und -bereinigung. Es bietet leistungsstarke und flexible Datenstrukturen wie DataFrames, die ideal für tabellarische Daten sind. Die Verwendung von `pandas` ermöglicht:

*   **Effizientes Laden und Speichern:** Daten können einfach aus CSV-Dateien geladen (`pd.read_csv`) und wieder als CSV gespeichert (`df.to_csv`) werden.
*   **Datenfilterung:** Das Filtern von Zeilen basierend auf Bedingungen (z.B. `df['price'].between(args.min_price, args.max_price)`) ist intuitiv und performant.
*   **Datentypkonvertierung:** Funktionen wie `pd.to_datetime()` ermöglichen eine einfache Umwandlung von Spaltentypen.
*   **Dateninspektion:** Methoden wie `df.shape`, `df.dtypes`, `df.isnull().sum()` bieten schnelle Einblicke in die Datenstruktur und das Vorhandensein fehlender Werte.

### Wandb Artifacts

`wandb` (Weights & Biases) wird in dieser Pipeline verwendet, um die Nachvollziehbarkeit und Versionierung von Datasets zu gewährleisten. Das bereinigte Dataset wird als `wandb` Artefakt protokolliert. Dies bietet folgende Vorteile:

*   **Versionierung:** Jede Version des bereinigten Datasets wird gespeichert, was es ermöglicht, zu früheren Zuständen zurückzukehren oder verschiedene Versionen in nachfolgenden Schritten der Pipeline zu verwenden.
*   **Nachvollziehbarkeit:** Es wird genau dokumentiert, welche Version des Rohdatensatzes für die Bereinigung verwendet wurde und welche Version des bereinigten Datensatzes erzeugt wurde. Dies ist entscheidend für die Reproduzierbarkeit von Experimenten.
*   **Zentrale Speicherung:** Artefakte können zentral in `wandb` gespeichert und von anderen Komponenten der Pipeline einfach heruntergeladen werden.

## Funktionsanalyse: `go` Funktion in `run.py`

Die `go`-Funktion ist der Haupttreiber für den Datenbereinigungsprozess. Sie orchestriert die Schritte von der Initialisierung bis zum Hochladen des bereinigten Artefakts.

1.  **W&B-Lauf initialisieren:**
    ```python
    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)
    ```
    Ein neuer `wandb`-Lauf wird gestartet und der Job-Typ auf "basic_cleaning" gesetzt. Die übergebenen Argumente werden in der Konfiguration des Laufs gespeichert, um die Parameter des Laufs zu protokollieren.

2.  **Eingangsartefakt herunterladen:**
    ```python
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    ```
    Das Rohdatensatz-Artefakt, dessen Name über `args.input_artifact` übergeben wird (z.B. `sample.csv:latest`), wird von `wandb` heruntergeladen. Dies stellt sicher, dass die Komponente mit einer spezifischen, versionierten Datenquelle arbeitet. Der lokale Pfad zum heruntergeladenen Artefakt wird gespeichert.

3.  **Daten laden:**
    ```python
    df = pd.read_csv(artifact_local_path)
    ```
    Die heruntergeladene CSV-Datei wird mit `pandas` in einen DataFrame geladen.

4.  **Datenbereinigungstransformationen anwenden:**

    *   **Entfernung von Preis-Ausreißern:**
        ```python
        idx = df['price'].between(args.min_price, args.max_price)
        df = df[idx].copy()
        ```
        Zeilen, deren `price`-Wert außerhalb des durch `args.min_price` und `args.max_price` definierten Bereichs liegt, werden entfernt. Die `.copy()`-Methode wird verwendet, um sicherzustellen, dass ein neuer DataFrame erstellt wird und keine `SettingWithCopyWarning` auftritt.

    *   **Konvertierung von `last_review` zu `datetime`:**
        ```python
        df['last_review'] = pd.to_datetime(df['last_review'])
        ```
        Die Spalte `last_review` wird in das `datetime`-Format konvertiert. Dies ist wichtig für die weitere Analyse oder die Erstellung zeitbasierter Features.

5.  **Bereinigte Daten speichern:**
    ```python
    df.to_csv("clean_sample.csv", index=False)
    ```
    Der bereinigte DataFrame wird als neue CSV-Datei namens `clean_sample.csv` gespeichert. `index=False` verhindert, dass `pandas` eine zusätzliche Indexspalte in die Ausgabedatei schreibt.

6.  **Bereinigte Daten als Artefakt hochladen:**
    ```python
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)
    ```
    Die `clean_sample.csv`-Datei wird als neues `wandb` Artefakt hochgeladen. Der Name, Typ und die Beschreibung des Artefakts werden über die Kommandozeilenargumente (`args.output_artifact`, `args.output_type`, `args.output_description`) festgelegt. Dies macht das bereinigte Dataset für nachfolgende Schritte in der ML-Pipeline verfügbar und versioniert.

7.  **Lauf beenden:**
    ```python
    run.finish()
    ```
    Der `wandb`-Lauf wird ordnungsgemäß beendet, wodurch alle Metadaten und Artefakte synchronisiert werden.