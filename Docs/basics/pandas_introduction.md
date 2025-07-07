# Pandas-Einführung für ML-Projekte

## Was ist Pandas?

Pandas ist eine Python-Bibliothek für Datenanalyse und -manipulation. Sie ist das wichtigste Werkzeug für die Arbeit mit tabellarischen Daten (wie Excel-Tabellen) in Python. Der Name "Pandas" kommt von "Panel Data".

## Grundlegende Datenstrukturen

### 1. Series

Eine Series ist wie eine einzelne Spalte in einer Tabelle:

```python
import pandas as pd

# Series erstellen
prices = pd.Series([100, 150, 200, 300])
print(prices)
# Ausgabe:
# 0    100
# 1    150
# 2    200
# 3    300
# dtype: int64

# Series mit benannten Indizes
prices_named = pd.Series([100, 150, 200], index=['Apartment A', 'Apartment B', 'Apartment C'])
print(prices_named)
# Ausgabe:
# Apartment A    100
# Apartment B    150
# Apartment C    200
# dtype: int64
```

### 2. DataFrame

Ein DataFrame ist wie eine komplette Tabelle mit mehreren Spalten:

```python
# DataFrame erstellen
data = {
    'name': ['Apartment A', 'Apartment B', 'Apartment C'],
    'price': [100, 150, 200],
    'location': ['Manhattan', 'Brooklyn', 'Queens'],
    'rating': [4.5, 4.2, 4.8]
}

df = pd.DataFrame(data)
print(df)
# Ausgabe:
#            name  price  location  rating
# 0  Apartment A    100  Manhattan     4.5
# 1  Apartment B    150   Brooklyn     4.2
# 2  Apartment C    200     Queens     4.8
```

## Daten laden und speichern

### CSV-Dateien

```python
# Daten aus CSV-Datei laden
df = pd.read_csv('airbnb_data.csv')

# Daten in CSV-Datei speichern
df.to_csv('processed_data.csv', index=False)
```

### Andere Formate

```python
# Excel-Datei
df = pd.read_excel('data.xlsx')

# JSON-Datei
df = pd.read_json('data.json')

# SQL-Datenbank
df = pd.read_sql('SELECT * FROM listings', connection)
```

## Daten erkunden

### Grundlegende Informationen

```python
# Erste Zeilen anzeigen
print(df.head())  # Erste 5 Zeilen
print(df.head(10))  # Erste 10 Zeilen

# Letzte Zeilen anzeigen
print(df.tail())  # Letzte 5 Zeilen

# Grundlegende Informationen
print(df.info())  # Datentypen und fehlende Werte
print(df.shape)   # Anzahl Zeilen und Spalten
print(df.describe())  # Statistische Zusammenfassung
```

### Spalten und Zeilen

```python
# Spaltennamen
print(df.columns)

# Datentypen
print(df.dtypes)

# Einzelne Spalte auswählen
prices = df['price']
print(prices)

# Mehrere Spalten auswählen
subset = df[['name', 'price', 'rating']]
print(subset)
```

## Daten filtern

### Bedingte Filterung

```python
# Filter: Nur teure Apartments (>150)
expensive = df[df['price'] > 150]
print(expensive)

# Filter: Nur Manhattan
manhattan = df[df['location'] == 'Manhattan']
print(manhattan)

# Mehrere Bedingungen
good_manhattan = df[(df['location'] == 'Manhattan') & (df['rating'] > 4.5)]
print(good_manhattan)
```

### isin() für Listen

```python
# Filter: Bestimmte Orte
selected_locations = ['Manhattan', 'Brooklyn']
filtered = df[df['location'].isin(selected_locations)]
print(filtered)
```

## Daten sortieren

```python
# Nach Preis sortieren (aufsteigend)
sorted_by_price = df.sort_values('price')
print(sorted_by_price)

# Nach Rating sortieren (absteigend)
sorted_by_rating = df.sort_values('rating', ascending=False)
print(sorted_by_rating)

# Nach mehreren Spalten sortieren
sorted_multiple = df.sort_values(['location', 'price'])
print(sorted_multiple)
```

## Fehlende Werte behandeln

```python
# Fehlende Werte identifizieren
print(df.isnull().sum())

# Zeilen mit fehlenden Werten entfernen
df_clean = df.dropna()

# Fehlende Werte mit Durchschnitt ersetzen
df['price'].fillna(df['price'].mean(), inplace=True)

# Fehlende Werte mit spezifischem Wert ersetzen
df['location'].fillna('Unknown', inplace=True)
```

## Gruppierung und Aggregation

```python
# Nach Ort gruppieren und Durchschnittspreis berechnen
avg_price_by_location = df.groupby('location')['price'].mean()
print(avg_price_by_location)

# Mehrere Aggregationen
summary = df.groupby('location').agg({
    'price': ['mean', 'min', 'max'],
    'rating': ['mean', 'count']
})
print(summary)

# Gruppierung mit mehreren Spalten
location_rating = df.groupby(['location', 'rating']).size()
print(location_rating)
```

## Daten transformieren

### Neue Spalten erstellen

```python
# Neue Spalte basierend auf bestehenden
df['price_category'] = df['price'].apply(lambda x: 'Cheap' if x < 100 else 'Expensive')

# Bedingte Spalte
df['is_expensive'] = df['price'] > 150

# Berechnete Spalte
df['price_per_rating'] = df['price'] / df['rating']
```

### Datentypen konvertieren

```python
# String zu Datum
df['date'] = pd.to_datetime(df['date_string'])

# String zu Zahl
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Kategorische Daten
df['location'] = df['location'].astype('category')
```

## Daten zusammenführen

### Concatenation

```python
# Vertikal zusammenfügen (neue Zeilen)
combined = pd.concat([df1, df2], ignore_index=True)

# Horizontal zusammenfügen (neue Spalten)
combined = pd.concat([df1, df2], axis=1)
```

### Merge/Join

```python
# Inner Join (nur übereinstimmende Zeilen)
merged = df1.merge(df2, on='id')

# Left Join (alle Zeilen aus df1)
merged = df1.merge(df2, on='id', how='left')

# Right Join (alle Zeilen aus df2)
merged = df1.merge(df2, on='id', how='right')
```

## Praktische Beispiele für ML-Projekte

### Datenqualität prüfen

```python
def check_data_quality(df):
    """Prüft die Qualität eines DataFrames"""
    
    print("=== DATENQUALITÄTSBERICHT ===")
    print(f"Anzahl Zeilen: {len(df)}")
    print(f"Anzahl Spalten: {len(df.columns)}")
    print("\nFehlende Werte:")
    print(df.isnull().sum())
    print("\nDatentypen:")
    print(df.dtypes)
    print("\nStatistische Zusammenfassung:")
    print(df.describe())
    
    return df

# Verwendung
clean_df = check_data_quality(df)
```

### Daten für ML vorbereiten

```python
def prepare_ml_data(df):
    """Bereitet Daten für Machine Learning vor"""
    
    # Fehlende Werte behandeln
    df = df.fillna(df.mean())
    
    # Kategorische Variablen kodieren
    df_encoded = pd.get_dummies(df, columns=['location'])
    
    # Skalierung (normalisieren)
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df_encoded.select_dtypes(include=[np.number]))
    
    return df_scaled

# Verwendung
ml_ready_data = prepare_ml_data(df)
```

## Häufige Fehler und Lösungen

### 1. SettingWithCopyWarning

```python
# Falsch
df[df['price'] > 100]['price'] = 0  # Warnung!

# Richtig
df.loc[df['price'] > 100, 'price'] = 0
```

### 2. Index-Probleme

```python
# Index zurücksetzen
df = df.reset_index(drop=True)

# Index als Spalte behalten
df = df.reset_index()
```

### 3. Datentyp-Probleme

```python
# Datentyp prüfen
print(df['price'].dtype)

# Datentyp konvertieren
df['price'] = df['price'].astype(float)
```

## Best Practices

1. **Immer .copy() verwenden** bei Subset-Operationen
2. **Datentypen prüfen** vor Operationen
3. **Fehlende Werte früh behandeln**
4. **Dokumentation schreiben** für komplexe Transformationen
5. **Datenqualität regelmäßig prüfen**

## Nächste Schritte

Nachdem du Pandas verstanden hast, kannst du:

1. **Pytest lernen** - Für das Testen von Datenqualität
2. **Wandb verstehen** - Für Experiment-Tracking
3. **Scikit-learn kennenlernen** - Für Machine Learning

Pandas ist die Grundlage für alle Datenverarbeitung in diesem ML-Projekt! 