# Schnittstellenbeschreibung: Explorative Datenanalyse (EDA)

## Aufruf

Die EDA-Komponente wird über MLflow aufgerufen. Da es sich um ein Jupyter Notebook handelt, das interaktiv ausgeführt wird, wird der `main`-Einstiegspunkt in der `MLproject`-Datei so konfiguriert, dass er `jupyter-lab` startet.

Um die EDA-Komponente zu starten, navigieren Sie in das Verzeichnis `src/eda` und führen Sie den folgenden MLflow-Befehl aus:

```bash
mlflow run .
```

Dieser Befehl startet eine JupyterLab-Instanz, in der das `EDA.ipynb`-Notebook geöffnet und ausgeführt werden kann.

## Parameter

Basierend auf der `MLproject`-Datei sind keine expliziten Kommandozeilenparameter für diese Komponente definiert. Die Interaktion und Konfiguration erfolgt direkt innerhalb des `EDA.ipynb`-Notebooks.

| Parameter | Typ | Beschreibung |
| :-------- | :-- | :----------- |
| Keine     |     |              |