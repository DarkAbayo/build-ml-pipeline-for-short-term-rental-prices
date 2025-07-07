# Python-Grundlagen für ML-Projekte

## Was ist Python?

Python ist eine Programmiersprache, die besonders beliebt in der Datenanalyse und im Machine Learning ist. Sie ist bekannt für ihre einfache, lesbare Syntax und die große Anzahl verfügbarer Bibliotheken.

## Grundlegende Konzepte

### 1. Variablen und Datentypen

Variablen sind wie "Schubladen", in denen du Daten speicherst:

```python
# Zahlen
age = 25
price = 150.50

# Text (Strings)
name = "Airbnb Listing"
city = 'New York'

# Wahrheitswerte (Booleans)
is_available = True
is_expensive = False

# Listen (können verschiedene Datentypen enthalten)
features = ["wifi", "kitchen", "parking"]
prices = [100, 150, 200, 300]
```

### 2. Funktionen

Funktionen sind wiederverwendbare Code-Blöcke:

```python
def calculate_average_price(prices):
    """
    Berechnet den Durchschnittspreis aus einer Liste von Preisen.
    
    Args:
        prices (list): Liste von Preisen
        
    Returns:
        float: Durchschnittspreis
    """
    if len(prices) == 0:
        return 0
    
    total = sum(prices)
    average = total / len(prices)
    return average

# Funktion verwenden
price_list = [100, 150, 200, 300]
avg_price = calculate_average_price(price_list)
print(f"Durchschnittspreis: ${avg_price}")
```

### 3. Kontrollstrukturen

#### if-else Statements

```python
def categorize_price(price):
    if price < 100:
        return "Günstig"
    elif price < 200:
        return "Mittel"
    else:
        return "Teuer"

# Beispiel
listing_price = 150
category = categorize_price(listing_price)
print(f"Kategorie: {category}")
```

#### Schleifen

```python
# For-Schleife über eine Liste
prices = [100, 150, 200, 300]
for price in prices:
    category = categorize_price(price)
    print(f"Preis ${price}: {category}")

# While-Schleife
counter = 0
while counter < 5:
    print(f"Zähler: {counter}")
    counter += 1
```

### 4. Listen und Dictionary

#### Listen

```python
# Liste erstellen
airbnb_listings = ["Listing 1", "Listing 2", "Listing 3"]

# Element hinzufügen
airbnb_listings.append("Listing 4")

# Element entfernen
airbnb_listings.remove("Listing 2")

# Liste durchsuchen
for listing in airbnb_listings:
    print(listing)
```

#### Dictionary (Wörterbuch)

```python
# Dictionary erstellen
listing_info = {
    "name": "Cozy Apartment",
    "price": 150,
    "location": "Manhattan",
    "amenities": ["wifi", "kitchen"]
}

# Werte abrufen
print(f"Name: {listing_info['name']}")
print(f"Preis: ${listing_info['price']}")

# Werte ändern
listing_info['price'] = 160

# Neuen Schlüssel hinzufügen
listing_info['rating'] = 4.5
```

### 5. Module und Imports

Module sind Python-Dateien mit wiederverwendbarem Code:

```python
# Standardbibliothek importieren
import math
import random

# Spezifische Funktionen importieren
from datetime import datetime

# Bibliothek mit Alias importieren
import pandas as pd
import numpy as np

# Beispiel
radius = 5
area = math.pi * radius ** 2
print(f"Fläche: {area}")

# Zufällige Zahl
random_number = random.randint(1, 100)
print(f"Zufallszahl: {random_number}")
```

## Best Practices

### 1. Namenskonventionen

```python
# Variablen und Funktionen: snake_case
user_name = "John"
def calculate_price():
    pass

# Klassen: PascalCase
class AirbnbListing:
    pass

# Konstanten: UPPER_CASE
MAX_PRICE = 1000
```

### 2. Kommentare

```python
# Einzeiliger Kommentar
def process_data(data):
    """
    Mehrzeiliger Kommentar (Docstring)
    Verarbeitet die eingegebenen Daten.
    
    Args:
        data: Die zu verarbeitenden Daten
        
    Returns:
        Verarbeitete Daten
    """
    # Verarbeitung hier
    return processed_data
```

### 3. Fehlerbehandlung

```python
def safe_divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("Fehler: Division durch Null!")
        return None
    except Exception as e:
        print(f"Unerwarteter Fehler: {e}")
        return None

# Beispiel
result = safe_divide(10, 0)  # Gibt None zurück
```

## Häufige Fehler und Lösungen

### 1. IndentationError

```python
# Falsch - falsche Einrückung
def my_function():
print("Hello")  # Fehler!

# Richtig - korrekte Einrückung
def my_function():
    print("Hello")  # 4 Leerzeichen oder Tab
```

### 2. NameError

```python
# Falsch - Variable nicht definiert
print(undefined_variable)  # Fehler!

# Richtig - Variable definieren
my_variable = "Hello"
print(my_variable)
```

### 3. TypeError

```python
# Falsch - falsche Datentypen
result = "5" + 3  # Fehler!

# Richtig - Datentypen konvertieren
result = int("5") + 3  # 8
```

## Nächste Schritte

Nachdem du diese Grundlagen verstanden hast, kannst du:

1. **Pandas lernen** - Für Datenverarbeitung
2. **Pytest verstehen** - Für das Testen
3. **Wandb kennenlernen** - Für Experiment-Tracking

Diese Grundlagen sind die Basis für alle weiteren Konzepte in diesem ML-Projekt! 