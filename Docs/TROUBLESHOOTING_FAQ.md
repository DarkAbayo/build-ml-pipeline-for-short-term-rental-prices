# 🛠️ Troubleshooting & FAQ - Häufige Probleme und Lösungen

## 🚨 Kritische Fehler

### **1. "ModuleNotFoundError: No module named 'wandb'**

**Symptom:**
```bash
ModuleNotFoundError: No module named 'wandb'
```

**Ursache:** W&B ist nicht installiert oder nicht im aktuellen Environment

**Lösung:**
```bash
# Environment aktivieren
conda activate nyc_airbnb_dev

# W&B installieren
pip install wandb

# Oder mit conda
conda install -c conda-forge wandb
```

**Prävention:** Immer `environment.yml` verwenden

---

### **2. "wandb: ERROR Unable to fetch artifact"**

**Symptom:**
```bash
wandb: ERROR Unable to fetch artifact with name dark_pn-private/nyc_airbnb/random_forest_export:prod
```

**Ursache:** Artifact existiert nicht oder hat falschen Namen

**Lösung:**
```bash
# 1. W&B Projekt prüfen
# Gehe zu: https://wandb.ai/dark_pn-private/nyc_airbnb

# 2. Artifact-Name prüfen
wandb artifacts list

# 3. Korrekten Namen verwenden
mlflow run . -P steps=test_regression_model -P mlflow_model=random_forest_export:latest
```

**Prävention:** Immer Artifact-Namen in W&B UI prüfen

---

### **3. "test_proper_boundaries failed"**

**Symptom:**
```bash
FAILED test_data.py::test_proper_boundaries - assert 1 == 0
```

**Ursache:** Daten enthalten Koordinaten außerhalb NYC-Grenzen

**Lösung:**
```python
# In basic_cleaning/run.py hinzufügen:
idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
df = df[idx].copy()
```

**Prävention:** Geografische Filter immer anwenden

---

## ⚠️ Warnungen und Performance-Probleme

### **4. "UserWarning: pkg_resources is deprecated"**

**Symptom:**
```bash
UserWarning: pkg_resources is deprecated as an API
```

**Ursache:** Veraltete setuptools Version

**Lösung:**
```bash
pip install --upgrade setuptools
```

**Prävention:** Regelmäßige Dependency-Updates

---

### **5. "Memory Error" bei großen Datensätzen**

**Symptom:**
```bash
MemoryError: Unable to allocate array
```

**Ursache:** Zu wenig RAM für Datenverarbeitung

**Lösung:**
```python
# Chunked Processing
def process_large_data(df, chunk_size=10000):
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i+chunk_size]
        # Process chunk
        yield process_chunk(chunk)

# Memory-efficient loading
df = pd.read_csv('large_file.csv', chunksize=10000)
```

**Prävention:** Daten in kleineren Batches verarbeiten

---

### **6. "MLflow run failed" - Conda Environment**

**Symptom:**
```bash
ERROR: conda environment creation failed
```

**Ursache:** Conda Environment kann nicht erstellt werden

**Lösung:**
```bash
# 1. Conda Environment löschen
conda env list | grep mlflow | awk '{print $1}' | xargs -I {} conda env remove -n {} -y

# 2. MLflow Cache löschen
rm -rf ~/.mlflow

# 3. Neu versuchen
mlflow run . -P steps=all
```

**Prävention:** Regelmäßige Environment-Bereinigung

---

## 🔧 Konfigurationsprobleme

### **7. "Hydra configuration error"**

**Symptom:**
```bash
KeyError: 'modeling.random_forest.max_depth'
```

**Ursache:** Falsche Konfiguration in config.yaml

**Lösung:**
```yaml
# config.yaml prüfen
modeling:
  random_forest:
    max_depth: 50  # ← Korrekte Einrückung
    n_estimators: 100
```

**Prävention:** YAML-Syntax immer validieren

---

### **8. "W&B Login required"**

**Symptom:**
```bash
wandb: ERROR wandb.login() required
```

**Ursache:** Nicht bei W&B angemeldet

**Lösung:**
```bash
# 1. W&B Login
wandb login

# 2. API Key eingeben
# 3. Erneut versuchen
mlflow run . -P steps=all
```

**Prävention:** W&B Login in Setup-Script

---

## 📊 Datenqualitätsprobleme

### **9. "KL divergence too high"**

**Symptom:**
```bash
FAILED test_data.py::test_similar_neigh_distrib
```

**Ursache:** Datenverteilung unterscheidet sich stark von Referenz

**Lösung:**
```python
# 1. Datenverteilung analysieren
print(df['neighbourhood_group'].value_counts())

# 2. KL-Threshold anpassen
# In config.yaml:
data_check:
  kl_threshold: 0.5  # Erhöhen von 0.2
```

**Prävention:** Regelmäßige Datenqualitäts-Checks

---

### **10. "Price range validation failed"**

**Symptom:**
```bash
FAILED test_data.py::test_price_range
```

**Ursache:** Preise außerhalb erwarteter Range

**Lösung:**
```python
# 1. Preisverteilung analysieren
print(df['price'].describe())

# 2. Range anpassen
# In config.yaml:
etl:
  min_price: 5    # Erweitern
  max_price: 500  # Erweitern
```

**Prävention:** Datenexploration vor Tests

---

## 🐍 Python-spezifische Probleme

### **11. "Python version mismatch"**

**Symptom:**
```bash
ERROR: Python 3.9 not supported, requires Python 3.10
```

**Ursache:** Falsche Python-Version

**Lösung:**
```bash
# 1. Python-Version prüfen
python --version

# 2. Korrekte Version installieren
conda install python=3.10.0

# 3. Environment neu erstellen
conda env create -f environment.yml
```

**Prävention:** Immer environment.yml verwenden

---

### **12. "ImportError: cannot import name"**

**Symptom:**
```bash
ImportError: cannot import name 'ColumnTransformer' from 'sklearn.compose'
```

**Ursache:** Falsche scikit-learn Version

**Lösung:**
```bash
# 1. scikit-learn Version prüfen
pip show scikit-learn

# 2. Korrekte Version installieren
pip install scikit-learn==1.7.0

# 3. Alle Dependencies neu installieren
pip install -r requirements.txt
```

**Prävention:** Versions-Pinning in requirements.txt

---

## 🌐 Netzwerk-Probleme

### **13. "Connection timeout to W&B"**

**Symptom:**
```bash
wandb: ERROR Connection timeout
```

**Ursache:** Netzwerk-Probleme oder W&B Server down

**Lösung:**
```bash
# 1. Offline Mode verwenden
wandb offline

# 2. Später synchronisieren
wandb sync

# 3. Proxy-Einstellungen prüfen
export WANDB_BASE_URL=https://api.wandb.ai
```

**Prävention:** Offline-First Development

---

### **14. "GitHub connection failed"**

**Symptom:**
```bash
ERROR: Failed to clone repository
```

**Ursache:** GitHub Repository nicht erreichbar

**Lösung:**
```bash
# 1. Repository-URL prüfen
git remote -v

# 2. SSH-Key prüfen
ssh -T git@github.com

# 3. HTTPS verwenden
git remote set-url origin https://github.com/username/repo.git
```

**Prävention:** Backup-Repositorys

---

## 📈 Performance-Optimierung

### **15. "Training takes too long"**

**Symptom:** Random Forest Training dauert > 30 Minuten

**Lösung:**
```python
# 1. Weniger Bäume verwenden
rf_config = {
    'n_estimators': 50,  # Reduzieren von 100
    'max_depth': 20,     # Reduzieren von 50
    'n_jobs': -1         # Alle CPUs nutzen
}

# 2. Daten-Sample verwenden
df_sample = df.sample(n=10000, random_state=42)
```

**Prävention:** Progressive Training (klein → groß)

---

### **16. "Memory usage too high"**

**Symptom:** System wird langsam, hohe RAM-Nutzung

**Lösung:**
```python
# 1. Daten-Typen optimieren
df['price'] = df['price'].astype('float32')
df['latitude'] = df['latitude'].astype('float32')

# 2. Unnötige Spalten entfernen
df = df.drop(['id', 'host_id'], axis=1)

# 3. Kategorische Spalten optimieren
df['room_type'] = df['room_type'].astype('category')
```

**Prävention:** Regelmäßige Memory-Profiling

---

## 🔍 Debugging-Tipps

### **17. Verbose Logging aktivieren**

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Oder in MLflow
mlflow run . -P steps=all -v
```

### **18. Zwischenergebnisse speichern**

```python
# In jedem Schritt
import pickle

# Daten speichern
with open('intermediate_data.pkl', 'wb') as f:
    pickle.dump(df, f)

# Daten laden
with open('intermediate_data.pkl', 'rb') as f:
    df = pickle.load(f)
```

### **19. W&B Runs vergleichen**

```python
# Runs anzeigen
wandb runs list --project nyc_airbnb

# Spezifischen Run analysieren
wandb run [run_id]
```

---

## ❓ Häufige Fragen (FAQ)

### **Q: Wie lange dauert die komplette Pipeline?**
A: 5-15 Minuten je nach Hardware und Datenmenge

### **Q: Kann ich die Pipeline auf meinem Laptop ausführen?**
A: Ja, aber mit 8GB+ RAM empfohlen

### **Q: Was mache ich bei W&B Quota-Überschreitung?**
A: Offline Mode verwenden oder kostenloses Konto upgraden

### **Q: Kann ich andere ML-Algorithmen verwenden?**
A: Ja, einfach in `train_random_forest/run.py` anpassen

### **Q: Wie aktualisiere ich die Dokumentation?**
A: Änderungen in `/Docs` committen und pushen

### **Q: Was ist der Unterschied zwischen sample1.csv und sample2.csv?**
A: sample2.csv ist größer und enthält mehr Daten

### **Q: Kann ich die Pipeline in Docker ausführen?**
A: Ja, siehe [Next Steps](NEXT_STEPS.md#docker)

### **Q: Wie überwache ich die Pipeline in Produktion?**
A: W&B Monitoring oder eigene Dashboards

---

## 🆘 Notfall-Plan

### **Wenn alles schief geht:**

1. **Environment komplett neu erstellen:**
```bash
conda env remove -n nyc_airbnb_dev
conda env create -f environment.yml
conda activate nyc_airbnb_dev
```

2. **MLflow Cache löschen:**
```bash
rm -rf ~/.mlflow
rm -rf mlruns/
```

3. **W&B Runs zurücksetzen:**
```bash
wandb offline
# Neue Runs starten
```

4. **Git Repository zurücksetzen:**
```bash
git checkout main
git pull origin main
```

5. **Dokumentation lesen:**
- [Master Learning Guide](MASTER_LEARNING_GUIDE.md)
- [Best Practices](BEST_PRACTICES.md)
- [Error Solutions](ERRORS_AND_SOLUTIONS.md)

---

## 📞 Support und Community

### **Wo bekomme ich Hilfe?**

1. **GitHub Issues** - Technische Probleme
2. **W&B Community** - Experiment-Tracking Fragen
3. **Stack Overflow** - Code-spezifische Fragen
4. **Discord/Reddit** - Allgemeine ML-Fragen

### **Wie stelle ich eine gute Frage?**

1. **Fehlermeldung vollständig kopieren**
2. **System-Info angeben** (OS, Python-Version)
3. **Schritte zur Reproduktion**
4. **Was bereits versucht wurde**

---

**💡 Tipp:** Die meisten Probleme entstehen durch Versionskonflikte. Immer `environment.yml` verwenden!

**🔄 Letzte Aktualisierung:** September 2025
