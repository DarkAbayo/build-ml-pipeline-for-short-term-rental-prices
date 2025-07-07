# Pytest und Fixtures für ML-Projekte

## Was ist Pytest?

Pytest ist ein beliebtes Test-Framework für Python. Es macht das Schreiben und Ausführen von Tests einfach und effizient. In ML-Projekten verwenden wir Pytest, um sicherzustellen, dass unsere Daten und Code korrekt funktionieren.

## Warum testen wir in ML-Projekten?

1. **Datenqualität sicherstellen** - Wir testen, ob unsere Daten die erwarteten Eigenschaften haben
2. **Code-Funktionalität prüfen** - Wir testen, ob unsere Funktionen korrekt arbeiten
3. **Regressionen verhindern** - Wir stellen sicher, dass Änderungen nichts kaputt machen
4. **Dokumentation** - Tests zeigen, wie Code verwendet werden soll

## Grundlegende Test-Struktur

### Einfacher Test

```python
def test_addition():
    """Test für eine einfache Addition"""
    result = 2 + 2
    assert result == 4

def test_string_concatenation():
    """Test für String-Verkettung"""
    name = "John"
    greeting = f"Hello, {name}!"
    assert greeting == "Hello, John!"
```

### Test mit Pandas

```python
import pandas as pd

def test_dataframe_creation():
    """Test für DataFrame-Erstellung"""
    data = {'price': [100, 150, 200]}
    df = pd.DataFrame(data)
    
    # Test: DataFrame hat die erwartete Anzahl Zeilen
    assert len(df) == 3
    
    # Test: Spalte 'price' existiert
    assert 'price' in df.columns
    
    # Test: Alle Preise sind positiv
    assert (df['price'] > 0).all()
```

## Was sind Fixtures?

Fixtures sind wiederverwendbare Test-Daten oder Setup-Code. Sie werden einmal erstellt und können von mehreren Tests verwendet werden. Das spart Zeit und macht Tests konsistent.

### Einfache Fixture

```python
import pytest
import pandas as pd

@pytest.fixture
def sample_data():
    """Erstellt Beispieldaten für Tests"""
    data = {
        'name': ['Apartment A', 'Apartment B', 'Apartment C'],
        'price': [100, 150, 200],
        'location': ['Manhattan', 'Brooklyn', 'Queens']
    }
    return pd.DataFrame(data)

def test_data_has_expected_columns(sample_data):
    """Test: Daten haben die erwarteten Spalten"""
    expected_columns = ['name', 'price', 'location']
    assert list(sample_data.columns) == expected_columns

def test_data_has_positive_prices(sample_data):
    """Test: Alle Preise sind positiv"""
    assert (sample_data['price'] > 0).all()
```

## Fixture-Scopes

Fixtures können verschiedene "Lebensdauern" haben:

```python
@pytest.fixture(scope='function')  # Standard: wird für jeden Test neu erstellt
def function_scope_fixture():
    return "neue Daten für jeden Test"

@pytest.fixture(scope='class')     # Wird einmal pro Testklasse erstellt
def class_scope_fixture():
    return "Daten für alle Tests in einer Klasse"

@pytest.fixture(scope='module')    # Wird einmal pro Modul erstellt
def module_scope_fixture():
    return "Daten für alle Tests in einem Modul"

@pytest.fixture(scope='session')   # Wird einmal pro Test-Session erstellt
def session_scope_fixture():
    return "Daten für alle Tests in einer Session"
```

## Fixtures mit Parametern

```python
@pytest.fixture
def price_threshold():
    """Gibt verschiedene Preisschwellen für Tests zurück"""
    return 150

def test_expensive_apartments(sample_data, price_threshold):
    """Test: Teure Apartments werden korrekt identifiziert"""
    expensive = sample_data[sample_data['price'] > price_threshold]
    assert len(expensive) == 1  # Nur Apartment C ist teurer als 150
```

## Fixtures mit Setup und Teardown

```python
@pytest.fixture
def temporary_file():
    """Erstellt eine temporäre Datei für Tests"""
    # Setup: Datei erstellen
    filename = "temp_test_data.csv"
    data = {'price': [100, 150, 200]}
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    
    yield filename  # Gibt Dateinamen an Test weiter
    
    # Teardown: Datei löschen
    import os
    if os.path.exists(filename):
        os.remove(filename)

def test_file_loading(temporary_file):
    """Test: Datei kann korrekt geladen werden"""
    df = pd.read_csv(temporary_file)
    assert len(df) == 3
    assert 'price' in df.columns
```

## Fixtures in conftest.py

Die `conftest.py` Datei ist speziell für Fixtures gedacht. Alle Fixtures in dieser Datei sind automatisch für alle Tests verfügbar.

### Beispiel: conftest.py

```python
import pytest
import pandas as pd
import wandb

@pytest.fixture(scope='session')
def sample_data():
    """Lädt Beispieldaten für alle Tests"""
    data = {
        'name': ['Apartment A', 'Apartment B', 'Apartment C'],
        'price': [100, 150, 200],
        'location': ['Manhattan', 'Brooklyn', 'Queens'],
        'rating': [4.5, 4.2, 4.8]
    }
    return pd.DataFrame(data)

@pytest.fixture(scope='session')
def price_threshold():
    """Definiert Preisschwelle für Tests"""
    return 150

@pytest.fixture(scope='session')
def wandb_run():
    """Initialisiert W&B Run für Tests"""
    run = wandb.init(job_type="testing", mode="disabled")
    yield run
    run.finish()
```

## Praktische Beispiele für ML-Tests

### Datenqualitätstests

```python
def test_no_missing_values(sample_data):
    """Test: Keine fehlenden Werte in wichtigen Spalten"""
    important_columns = ['name', 'price', 'location']
    for col in important_columns:
        assert sample_data[col].isnull().sum() == 0

def test_price_range(sample_data):
    """Test: Preise sind in vernünftigem Bereich"""
    min_price = 10
    max_price = 1000
    assert (sample_data['price'] >= min_price).all()
    assert (sample_data['price'] <= max_price).all()

def test_location_values(sample_data):
    """Test: Nur gültige Orte sind vorhanden"""
    valid_locations = ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island']
    assert sample_data['location'].isin(valid_locations).all()
```

### Funktionalitätstests

```python
def test_price_categorization(sample_data):
    """Test: Preis-Kategorisierung funktioniert korrekt"""
    def categorize_price(price):
        if price < 100:
            return "Günstig"
        elif price < 200:
            return "Mittel"
        else:
            return "Teuer"
    
    sample_data['category'] = sample_data['price'].apply(categorize_price)
    
    # Test: Kategorien sind korrekt
    assert sample_data.loc[sample_data['price'] == 100, 'category'].iloc[0] == "Günstig"
    assert sample_data.loc[sample_data['price'] == 150, 'category'].iloc[0] == "Mittel"
    assert sample_data.loc[sample_data['price'] == 200, 'category'].iloc[0] == "Teuer"
```

### W&B Integration Tests

```python
def test_wandb_artifact_loading(wandb_run):
    """Test: W&B Artefakte können geladen werden"""
    # Simuliere Artefakt-Download
    artifact_path = "sample_data.csv"
    sample_data = pd.DataFrame({'price': [100, 150, 200]})
    sample_data.to_csv(artifact_path, index=False)
    
    # Test: Datei kann geladen werden
    loaded_data = pd.read_csv(artifact_path)
    assert len(loaded_data) == 3
    assert 'price' in loaded_data.columns
```

## Test-Ausführung

### Tests ausführen

```bash
# Alle Tests ausführen
pytest

# Tests in spezifischem Verzeichnis
pytest tests/

# Spezifischen Test ausführen
pytest tests/test_data_quality.py::test_no_missing_values

# Tests mit Ausgabe
pytest -v

# Tests mit detaillierter Ausgabe
pytest -vv
```

### Test-Parameter

```bash
# Tests mit Kommandozeilen-Parametern
pytest --csv="data.csv" --min_price=10 --max_price=1000

# Tests mit Konfigurationsdatei
pytest --config=test_config.yaml
```

## Best Practices

### 1. Test-Namen sind beschreibend

```python
# Gut
def test_price_is_positive():
    pass

def test_data_has_expected_columns():
    pass

# Schlecht
def test1():
    pass

def test_data():
    pass
```

### 2. Tests sind unabhängig

```python
# Jeder Test sollte unabhängig von anderen funktionieren
def test_independent_1():
    data = create_test_data()  # Lokale Daten
    assert len(data) == 3

def test_independent_2():
    data = create_test_data()  # Lokale Daten
    assert 'price' in data.columns
```

### 3. Tests sind schnell

```python
# Verwende Fixtures für teure Operationen
@pytest.fixture(scope='session')
def expensive_data():
    # Wird nur einmal erstellt
    return load_large_dataset()

def test_with_expensive_data(expensive_data):
    # Test ist schnell
    assert len(expensive_data) > 0
```

### 4. Assertions sind spezifisch

```python
# Gut
assert len(df) == 3, f"Erwartet 3 Zeilen, aber {len(df)} gefunden"
assert 'price' in df.columns, "Spalte 'price' fehlt"

# Schlecht
assert df is not None
```

## Häufige Fehler und Lösungen

### 1. Fixture nicht gefunden

```python
# Problem: Fixture wird nicht gefunden
def test_something(missing_fixture):
    pass

# Lösung: Fixture in conftest.py definieren oder importieren
@pytest.fixture
def missing_fixture():
    return "data"
```

### 2. Scope-Probleme

```python
# Problem: Fixture wird zu oft neu erstellt
@pytest.fixture(scope='function')  # Standard
def expensive_fixture():
    return load_large_dataset()

# Lösung: Scope vergrößern
@pytest.fixture(scope='session')
def expensive_fixture():
    return load_large_dataset()
```

### 3. Test-Daten werden verändert

```python
# Problem: Test verändert globale Daten
def test_modifies_data(sample_data):
    sample_data['new_column'] = 'value'  # Verändert Original

# Lösung: Kopie erstellen
def test_modifies_data(sample_data):
    test_data = sample_data.copy()
    test_data['new_column'] = 'value'  # Verändert nur Kopie
```

## Nächste Schritte

Nachdem du Pytest verstanden hast, kannst du:

1. **Wandb lernen** - Für Experiment-Tracking
2. **MLflow verstehen** - Für Pipeline-Orchestrierung
3. **Scikit-learn kennenlernen** - Für Machine Learning

Pytest ist essentiell für die Qualitätssicherung in ML-Projekten! 