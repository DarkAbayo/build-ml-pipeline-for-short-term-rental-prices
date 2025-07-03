# Cheat Sheet: Explorative Datenanalyse (EDA)

## Essenz

Die EDA-Komponente dient dazu, ein schnelles und umfassendes Verständnis der Rohdaten zu gewinnen. Sie identifiziert Datenqualitätsprobleme, deckt Muster auf und generiert erste Hypothesen, die als Grundlage für die weitere Datenvorverarbeitung und Modellentwicklung dienen.

## Wichtigste Analysen

*   **Umgebungsprüfung:** Sicherstellung der korrekten Conda-Umgebung (`nyc_airbnb_dev`).
*   **Wandb-Integration:** Initialisierung eines Wandb-Runs zum Tracking und zur Speicherung von Metadaten und Artefakten.
*   **Datenartefakt-Download:** Herunterladen des neuesten `sample.csv`-Datenartefakts von Wandb.
*   **Automatisiertes Datenprofiling:** Erstellung eines detaillierten HTML-Berichts mit `ydata-profiling`, der folgende Informationen enthält:
    *   Statistische Übersichten
    *   Variablenverteilungen
    *   Korrelationen zwischen Variablen
    *   Analyse fehlender Werte
    *   Identifizierung doppelter Zeilen