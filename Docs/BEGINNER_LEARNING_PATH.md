# 🎓 Beginner Learning Path - Schritt-für-Schritt Anleitung

## 🎯 Für wen ist dieser Lernpfad?

- **Python-Anfänger** (0-6 Monate Erfahrung)
- **ML-Neueinsteiger** (keine praktische Erfahrung)
- **Studenten** (Lernen durch praktische Projekte)
- **Career-Changer** (Wechsel in Data Science/ML)

## ⏱️ Zeitplan

- **Gesamtdauer:** 6-8 Wochen
- **Zeitaufwand:** 10-15 Stunden pro Woche
- **Flexibilität:** Selbstbestimmtes Lernen

## 📚 Lernpfad-Übersicht

```
Woche 1-2: Grundlagen verstehen
    ↓
Woche 3-4: Pipeline entwickeln
    ↓
Woche 5-6: Erweitern und optimieren
    ↓
Woche 7-8: Produktion und Deployment
```

---

## 📖 Woche 1-2: Grundlagen verstehen

### **Tag 1-3: Python Grundlagen**

#### **Lernziele:**
- Python-Syntax verstehen
- Variablen, Funktionen, Klassen
- Datenstrukturen (Listen, Dictionaries)

#### **Praktische Übungen:**
```python
# Übung 1: Grundlegende Python-Konzepte
def calculate_rental_price(base_price, location_multiplier, amenities_bonus):
    """Berechne Mietpreis basierend auf verschiedenen Faktoren"""
    total_price = base_price * location_multiplier + amenities_bonus
    return total_price

# Testen
price = calculate_rental_price(100, 1.5, 20)
print(f"Calculated price: ${price}")

# Übung 2: Datenstrukturen
rental_data = {
    'neighborhood': 'Manhattan',
    'price': 150,
    'room_type': 'Entire home/apt',
    'amenities': ['wifi', 'parking', 'gym']
}

print(f"Rental in {rental_data['neighborhood']}: ${rental_data['price']}")
```

#### **Ressourcen:**
- [Python Basics](basics/python_basics.md)
- [Python.org Tutorial](https://docs.python.org/3/tutorial/)
- [Codecademy Python](https://www.codecademy.com/learn/learn-python-3)

---

### **Tag 4-7: Pandas für Datenverarbeitung**

#### **Lernziele:**
- DataFrames verstehen
- Daten laden und speichern
- Daten filtern und transformieren

#### **Praktische Übungen:**
```python
import pandas as pd
import numpy as np

# Übung 1: Daten laden und erkunden
df = pd.read_csv('sample1.csv')
print(f"Data shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"First few rows:\n{df.head()}")

# Übung 2: Daten filtern
expensive_rentals = df[df['price'] > 200]
print(f"Expensive rentals: {len(expensive_rentals)}")

# Übung 3: Gruppierung und Aggregation
neighborhood_stats = df.groupby('neighbourhood_group')['price'].agg(['mean', 'count'])
print(neighborhood_stats)

# Übung 4: Neue Spalten erstellen
df['price_per_night'] = df['price'] / df['minimum_nights']
df['is_expensive'] = df['price'] > df['price'].median()
```

#### **Ressourcen:**
- [Pandas Introduction](basics/pandas_introduction.md)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [10 Minutes to Pandas](https://pandas.pydata.org/docs/user_guide/10min.html)

---

### **Tag 8-10: Machine Learning Grundlagen**

#### **Lernziele:**
- Was ist Machine Learning?
- Überwachtes vs. unüberwachtes Lernen
- Train/Test Split verstehen

#### **Praktische Übungen:**
```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# Übung 1: Einfaches Modell erstellen
# Features und Zielvariable definieren
X = df[['latitude', 'longitude', 'minimum_nights']]
y = df['price']

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Modell trainieren
model = LinearRegression()
model.fit(X_train, y_train)

# Vorhersagen machen
predictions = model.predict(X_test)

# Modell evaluieren
mae = mean_absolute_error(y_test, predictions)
print(f"Mean Absolute Error: {mae:.2f}")
```

#### **Ressourcen:**
- [Scikit-learn Tutorial](https://scikit-learn.org/stable/tutorial/index.html)
- [Machine Learning Basics](https://www.coursera.org/learn/machine-learning)

---

### **Tag 11-14: Experiment-Tracking**

#### **Lernziele:**
- W&B verstehen
- Experimente verfolgen
- Metriken visualisieren

#### **Praktische Übungen:**
```python
import wandb

# Übung 1: W&B Run starten
run = wandb.init(
    project="my-first-ml-project",
    name="linear-regression-experiment"
)

# Übung 2: Konfiguration loggen
run.config.update({
    'learning_rate': 0.01,
    'test_size': 0.2,
    'random_state': 42
})

# Übung 3: Metriken loggen
run.log({
    'mae': mae,
    'r2': model.score(X_test, y_test),
    'epoch': 1
})

# Übung 4: Run beenden
run.finish()
```

#### **Ressourcen:**
- [W&B Quickstart](https://docs.wandb.ai/quickstart)
- [W&B & MLflow](basics/wandb_mlflow.md)

---

## 🛠️ Woche 3-4: Pipeline entwickeln

### **Tag 15-17: Data Cleaning**

#### **Lernziele:**
- Datenqualität verstehen
- Outlier erkennen und behandeln
- Fehlende Werte handhaben

#### **Praktische Übungen:**
```python
def clean_data(df):
    """Daten bereinigen"""
    # Kopie erstellen
    df_clean = df.copy()
    
    # Preise filtern
    df_clean = df_clean[
        (df_clean['price'] >= 10) & 
        (df_clean['price'] <= 500)
    ]
    
    # Geografische Grenzen
    df_clean = df_clean[
        (df_clean['longitude'].between(-74.25, -73.50)) &
        (df_clean['latitude'].between(40.5, 41.2))
    ]
    
    # Fehlende Werte in last_review
    df_clean['last_review'] = pd.to_datetime(df_clean['last_review'])
    
    return df_clean

# Testen
df_clean = clean_data(df)
print(f"Original: {len(df)} rows")
print(f"Cleaned: {len(df_clean)} rows")
```

#### **Ressourcen:**
- [Basic Cleaning](basic_cleaning/Explanations.md)
- [Data Quality Best Practices](BEST_PRACTICES.md)

---

### **Tag 18-21: Data Testing**

#### **Lernziele:**
- Automatisierte Tests schreiben
- Datenqualität sicherstellen
- Pytest verstehen

#### **Praktische Übungen:**
```python
import pytest

def test_data_quality(df):
    """Datenqualität testen"""
    # Spalten prüfen
    expected_columns = ['id', 'name', 'price', 'latitude', 'longitude']
    assert all(col in df.columns for col in expected_columns)
    
    # Preise prüfen
    assert df['price'].between(10, 500).all()
    
    # Koordinaten prüfen
    assert df['longitude'].between(-74.25, -73.50).all()
    assert df['latitude'].between(40.5, 41.2).all()
    
    # Keine Duplikate
    assert df.duplicated().sum() == 0

# Test ausführen
test_data_quality(df_clean)
print("✅ All tests passed!")
```

#### **Ressourcen:**
- [Data Check](data_check/Explanations.md)
- [Pytest Fixtures](basics/pytest_fixtures.md)

---

### **Tag 22-24: Feature Engineering**

#### **Lernziele:**
- Features erstellen
- Kategorische Variablen behandeln
- Text-Daten verarbeiten

#### **Praktische Übungen:**
```python
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

def create_features(df):
    """Features erstellen"""
    df_features = df.copy()
    
    # Kategorische Features
    le = LabelEncoder()
    df_features['room_type_encoded'] = le.fit_transform(df_features['room_type'])
    
    # One-Hot Encoding für Nachbarschaften
    neighborhood_dummies = pd.get_dummies(df_features['neighbourhood_group'])
    df_features = pd.concat([df_features, neighborhood_dummies], axis=1)
    
    # Text-Features
    tfidf = TfidfVectorizer(max_features=10, stop_words='english')
    name_features = tfidf.fit_transform(df_features['name'].fillna(''))
    name_df = pd.DataFrame(
        name_features.toarray(),
        columns=[f'name_{i}' for i in range(name_features.shape[1])]
    )
    df_features = pd.concat([df_features, name_df], axis=1)
    
    # Geografische Features
    df_features['distance_to_center'] = np.sqrt(
        (df_features['latitude'] - 40.7589)**2 + 
        (df_features['longitude'] - (-73.9851))**2
    )
    
    return df_features

# Testen
df_with_features = create_features(df_clean)
print(f"Features created: {df_with_features.shape[1]} columns")
```

#### **Ressourcen:**
- [Feature Engineering](train_random_forest/Explanations.md#feature-engineering)
- [Scikit-learn Preprocessing](https://scikit-learn.org/stable/modules/preprocessing.html)

---

### **Tag 25-28: Modell-Training**

#### **Lernziele:**
- Random Forest verstehen
- Modell trainieren
- Performance evaluieren

#### **Praktische Übungen:**
```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

def train_model(df):
    """Modell trainieren"""
    # Features und Zielvariable
    feature_columns = [col for col in df.columns if col not in ['price', 'id', 'name']]
    X = df[feature_columns]
    y = df['price']
    
    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Modell trainieren
    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    
    # Evaluieren
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"MAE: {mae:.2f}")
    print(f"R²: {r2:.3f}")
    
    return model, X_test, y_test, y_pred

# Modell trainieren
model, X_test, y_test, y_pred = train_model(df_with_features)
```

#### **Ressourcen:**
- [Train Random Forest](train_random_forest/Explanations.md)
- [Random Forest Documentation](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html)

---

## 🚀 Woche 5-6: Erweitern und optimieren

### **Tag 29-31: Hyperparameter-Optimierung**

#### **Lernziele:**
- Hyperparameter verstehen
- Grid Search verwenden
- Beste Parameter finden

#### **Praktische Übungen:**
```python
from sklearn.model_selection import GridSearchCV

def optimize_hyperparameters(X_train, y_train):
    """Hyperparameter optimieren"""
    rf = RandomForestRegressor(random_state=42)
    
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5, 10]
    }
    
    grid_search = GridSearchCV(
        rf, param_grid, cv=3, 
        scoring='neg_mean_absolute_error',
        n_jobs=-1
    )
    
    grid_search.fit(X_train, y_train)
    
    print(f"Best parameters: {grid_search.best_params_}")
    print(f"Best score: {-grid_search.best_score_:.2f}")
    
    return grid_search.best_estimator_

# Optimieren
best_model = optimize_hyperparameters(X_train, y_train)
```

---

### **Tag 32-35: Modell-Evaluation**

#### **Lernziele:**
- Verschiedene Metriken verstehen
- Cross-Validation verwenden
- Modell interpretieren

#### **Praktische Übungen:**
```python
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt

def evaluate_model(model, X, y):
    """Modell umfassend evaluieren"""
    # Cross-Validation
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='neg_mean_absolute_error')
    print(f"CV MAE: {-cv_scores.mean():.2f} (+/- {cv_scores.std() * 2:.2f})")
    
    # Feature Importance
    feature_importance = model.feature_importances_
    feature_names = X.columns
    
    # Top 10 Features
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': feature_importance
    }).sort_values('importance', ascending=False).head(10)
    
    print("\nTop 10 Features:")
    print(importance_df)
    
    # Visualisierung
    plt.figure(figsize=(10, 6))
    plt.barh(importance_df['feature'], importance_df['importance'])
    plt.title('Feature Importance')
    plt.xlabel('Importance')
    plt.tight_layout()
    plt.show()

# Evaluieren
evaluate_model(best_model, X, y)
```

---

## 🏭 Woche 7-8: Produktion und Deployment

### **Tag 36-38: API-Entwicklung**

#### **Lernziele:**
- REST API verstehen
- Flask verwenden
- API testen

#### **Praktische Übungen:**
```python
from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Modell laden
model = joblib.load('model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    """Preisvorhersage API"""
    try:
        data = request.get_json()
        
        # DataFrame erstellen
        df = pd.DataFrame([data])
        
        # Vorhersage
        prediction = model.predict(df)[0]
        
        return jsonify({
            'predicted_price': float(prediction),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

---

### **Tag 39-42: Dokumentation und Präsentation**

#### **Lernziele:**
- Code dokumentieren
- Ergebnisse präsentieren
- Portfolio erstellen

#### **Praktische Übungen:**
```python
def create_project_summary():
    """Projekt-Zusammenfassung erstellen"""
    summary = {
        'project_name': 'Airbnb Price Prediction',
        'model_type': 'Random Forest Regressor',
        'performance': {
            'mae': 32.5,
            'r2': 0.588
        },
        'features_used': 15,
        'data_size': '48,895 samples',
        'key_insights': [
            'Neighborhood is the most important feature',
            'Room type significantly affects price',
            'Location (latitude/longitude) matters'
        ]
    }
    
    return summary

# Zusammenfassung erstellen
summary = create_project_summary()
print("Project Summary:")
for key, value in summary.items():
    print(f"{key}: {value}")
```

---

## 🎯 Lernziele-Checkliste

### **Woche 1-2: Grundlagen**
- [ ] Python-Syntax beherrschen
- [ ] Pandas für Datenverarbeitung nutzen
- [ ] ML-Grundkonzepte verstehen
- [ ] W&B für Experiment-Tracking verwenden

### **Woche 3-4: Pipeline**
- [ ] Daten bereinigen und validieren
- [ ] Features erstellen
- [ ] Modell trainieren
- [ ] Performance evaluieren

### **Woche 5-6: Optimierung**
- [ ] Hyperparameter optimieren
- [ ] Verschiedene Algorithmen testen
- [ ] Modell interpretieren
- [ ] Ergebnisse visualisieren

### **Woche 7-8: Produktion**
- [ ] API entwickeln
- [ ] Code dokumentieren
- [ ] Portfolio erstellen
- [ ] Projekt präsentieren

---

## 📚 Zusätzliche Ressourcen

### **Bücher**
- "Python for Data Analysis" von Wes McKinney
- "Hands-On Machine Learning" von Aurélien Géron
- "The Elements of Statistical Learning" von Hastie, Tibshirani, Friedman

### **Online-Kurse**
- [Coursera: Machine Learning](https://www.coursera.org/learn/machine-learning)
- [edX: Introduction to Machine Learning](https://www.edx.org/learn/machine-learning)
- [Udacity: Intro to Machine Learning](https://www.udacity.com/course/intro-to-machine-learning--ud120)

### **Praktische Projekte**
- [Kaggle Learn](https://www.kaggle.com/learn)
- [Google Colab](https://colab.research.google.com/)
- [GitHub: Awesome Machine Learning](https://github.com/josephmisiti/awesome-machine-learning)

---

## 🎉 Abschluss

Herzlichen Glückwunsch! Sie haben erfolgreich eine vollständige ML-Pipeline entwickelt. Sie sind jetzt bereit für:

- **Fortgeschrittene ML-Projekte**
- **Bewerbungen für Data Science Positionen**
- **Eigene ML-Projekte**
- **Weiterbildung in spezialisierten Bereichen**

**Viel Erfolg bei Ihren nächsten Schritten! 🚀**

---

**Letzte Aktualisierung:** September 2025  
**Version:** 1.0  
**Autor:** Prof. Dr. ML Pipeline Expert
