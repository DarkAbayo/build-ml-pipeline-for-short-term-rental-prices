# Cheat Sheet: Release Pipeline

## Essenz

Die Release-Pipeline ermöglicht es, die optimierte ML-Pipeline als versionierte Release zu veröffentlichen und mit neuen Daten zu testen. Sie umfasst Hyperparameter-Optimierung, Modell-Selektion und Release-Management.

## Durchgeführte Schritte

*   Beste Hyperparameter aus W&B-Experimenten identifizieren
*   config.yaml mit optimalen Parametern aktualisieren
*   GitHub Release mit Tag erstellen
*   Release mit neuem Datensatz testen
*   Performance-Metriken überwachen

## Wichtige Parameter

*   Beste Hyperparameter: max_tfidf_features=15, max_depth=50, max_features=0.33
*   Release-Version: v1.0.0, v1.0.1, etc.
*   Neuer Datensatz: sample2.csv für Release-Testing
