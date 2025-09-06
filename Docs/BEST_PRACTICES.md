# Best Practices für ML-Pipeline Entwicklung

## 1. Versionskonsistenz

### ✅ Richtig:
- Alle conda.yml Dateien verwenden die gleichen Versionen
- Python 3.10.0 (präzise Version)
- scikit-learn=1.7.0 in allen ML-Komponenten
- mlflow==2.8.1 und wandb==0.16.0 konsistent

### ❌ Vermeiden:
- Unterschiedliche Python-Versionen (3.10 vs 3.10.0)
- Fehlende scikit-learn Abhängigkeiten
- Inkonsistente MLflow/W&B Versionen

## 2. MLflow Cache Management

### ✅ Richtig:
```bash
# MLflow-Umgebungen bei Versionsproblemen löschen
conda env list | grep mlflow | awk '{print $1}' | xargs -I {} conda env remove -n {} -y
```

### ❌ Vermeiden:
- MLflow-Runs löschen (enthält wichtige Daten)
- Nur einzelne Umgebungen löschen ohne Systematik

## 3. Hydra-Konfiguration

### ✅ Richtig:
```bash
# Multi-Run für Hyperparameter-Optimierung
mlflow run . \
  -P steps=train_random_forest \
  -P hydra_options="modeling.random_forest.max_depth=10,50,100 modeling.random_forest.n_estimators=100,200,500 -m"
```

### ❌ Vermeiden:
- Zu viele Parameter-Kombinationen (Speicherprobleme)
- Keine systematische Hyperparameter-Optimierung

## 4. W&B Model Management

### ✅ Richtig:
- Bestes Modell als "prod" markieren
- Metadaten und Hyperparameter dokumentieren
- Feature Importance Plots erstellen

### ❌ Vermeiden:
- Modelle ohne "prod" Tag testen
- Keine Dokumentation der Hyperparameter

## 5. Lokale vs. Remote Komponenten

### ✅ Richtig:
- Lokale Komponenten für Custom-Fixes
- GitHub-Komponenten für Standard-Funktionalität
- Klare Trennung zwischen lokalen und remote Komponenten

### ❌ Vermeiden:
- GitHub-Komponenten für Workarounds verwenden
- Inkonsistente Komponenten-Quellen

## 6. Error Handling

### ✅ Richtig:
- Versionsinkompatibilitäten proaktiv behandeln
- Workarounds in Komponenten implementieren
- Detailliertes Logging für Debugging

### ❌ Vermeiden:
- Fehler ignorieren oder umgehen
- Keine Dokumentation von Workarounds

## 7. Pipeline-Struktur

### ✅ Richtig:
- Schrittweise Ausführung für Debugging
- Klare Trennung zwischen Training und Testing
- Reproduzierbare Experimente

### ❌ Vermeiden:
- Alles in einem Durchlauf ohne Kontrolle
- Keine Zwischenergebnisse speichern

## 8. Dokumentation

### ✅ Richtig:
- README für jede Komponente
- Best Practices dokumentieren
- Error-Solutions sammeln

### ❌ Vermeiden:
- Keine Dokumentation
- Workarounds nicht dokumentieren

## 9. Hyperparameter-Optimierung

### ✅ Richtig:
- Systematische Parameter-Variation
- Multi-Run mit Hydra
- Performance-Tracking in W&B

### ❌ Vermeiden:
- Manuelle Parameter-Tests
- Keine systematische Optimierung

## 10. Release Management

### ✅ Richtig:
- Beste Hyperparameter in config.yaml eintragen
- Versionierte Releases erstellen
- Release mit neuen Daten testen

### ❌ Vermeiden:
- Releases ohne Testing
- Keine Versionierung
