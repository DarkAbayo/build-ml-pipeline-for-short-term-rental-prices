# Detaillierte Erklärungen: Explorative Datenanalyse (EDA)

## Hintergrund

Die Explorative Datenanalyse (EDA) ist ein entscheidender Schritt in jeder Machine-Learning-Pipeline. Ihr Hauptzweck ist es, ein tiefes Verständnis der Daten zu gewinnen, Muster zu erkennen, Anomalien zu identifizieren und Hypothesen zu generieren, die für die nachfolgenden Schritte der Datenvorverarbeitung und Modellentwicklung von entscheidender Bedeutung sind. Durch die EDA können potenzielle Probleme wie fehlende Werte, Ausreißer oder Inkonsistenzen frühzeitig erkannt und behoben werden.

## Verwendete Methoden

### Jupyter Notebook

Das Jupyter Notebook-Format ist für die EDA besonders gut geeignet, da es eine interaktive und iterative Arbeitsweise ermöglicht. Code, Visualisierungen und erklärender Text können nahtlos in einem einzigen Dokument kombiniert werden. Dies fördert die Reproduzierbarkeit der Analyse und erleichtert die Kommunikation der Ergebnisse an andere Teammitglieder oder Stakeholder.

### ydata-profiling

Für die automatisierte Erstellung umfassender EDA-Berichte wird die Bibliothek `ydata-profiling` (ehemals Pandas Profiling) verwendet. Diese Bibliothek generiert mit nur wenigen Zeilen Code einen detaillierten HTML-Bericht, der statistische Übersichten, Verteilungen, Korrelationen und Informationen zu fehlenden Werten für jede Variable im Datensatz enthält. Dies beschleunigt den EDA-Prozess erheblich und stellt sicher, dass keine wichtigen Aspekte übersehen werden.

### Visualisierungsbibliotheken

Obwohl `ydata-profiling` bereits umfangreiche Visualisierungen automatisch generiert, spielen allgemeine Visualisierungsbibliotheken wie Matplotlib, Seaborn oder Plotly eine wichtige Rolle bei der tiefergehenden EDA. Sie ermöglichen es, spezifische Beziehungen zwischen Variablen zu untersuchen, benutzerdefinierte Diagramme zu erstellen und die Daten aus verschiedenen Perspektiven zu betrachten, um verborgene Muster und Erkenntnisse aufzudecken.

## Analyse des Notebooks (`EDA.ipynb`)

Das `EDA.ipynb` Notebook führt eine explorative Datenanalyse für den `nyc_airbnb`-Datensatz durch. Die wichtigsten Schritte und Erkenntnisse sind:

1.  **Importe und Umgebungsprüfung:** Das Notebook beginnt mit dem Import notwendiger Bibliotheken wie `wandb`, `numpy`, `pandas` und `ydata_profiling`. Es wird eine Überprüfung der Conda-Umgebung (`nyc_airbnb_dev`) durchgeführt, um sicherzustellen, dass die Analyse in der korrekten Umgebung ausgeführt wird.
2.  **Wandb-Integration:** Ein Weights & Biases (Wandb)-Run wird initialisiert (`wandb.init(project="nyc_airbnb", group="eda", save_code=True)`). Dies ermöglicht das Tracking der Experimente, das Speichern von Metadaten und das Hochladen von Artefakten, was die Nachvollziehbarkeit und Vergleichbarkeit von EDA-Ergebnissen verbessert.
3.  **Datenartefakt-Download:** Das neueste Datenartefakt (`sample.csv:latest`) wird von Wandb heruntergeladen. Dies stellt sicher, dass die Analyse immer mit der aktuellsten Version der Daten durchgeführt wird.
4.  **Datenprofiling mit `ydata-profiling`:** Der Kern der EDA in diesem Notebook ist die Erstellung eines detaillierten Datenprofils mithilfe von `ydata-profiling`. Diese Bibliothek generiert einen interaktiven HTML-Bericht, der eine umfassende Übersicht über den Datensatz bietet. Der Bericht enthält:
    *   **Übersicht:** Allgemeine Statistiken über den Datensatz.
    *   **Variablen:** Detaillierte Informationen und Verteilungen für jede einzelne Variable (numerisch, kategorial, boolesch).
    *   **Interaktionen:** Korrelationsmatrizen (z.B. Pearson, Spearman) zur Identifizierung von Beziehungen zwischen numerischen Variablen.
    *   **Korrelationen:** Verschiedene Korrelationsanalysen.
    *   **Fehlende Werte:** Visualisierungen und Zählungen fehlender Werte, um deren Muster und Umfang zu verstehen.
    *   **Duplikate:** Informationen über doppelte Zeilen im Datensatz.
    *   **Beispiel:** Kopf- und Fußzeilen des Datensatzes.

Die durchgeführte Analyse konzentriert sich auf die automatisierte Generierung eines umfassenden Berichts, der einen schnellen Überblick über die Datenqualität und -struktur ermöglicht. Dies ist besonders nützlich, um erste Hypothesen zu bilden und die nächsten Schritte in der Datenvorverarbeitung zu planen.