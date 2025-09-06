# 💻 Practical Examples - Code zum Ausprobieren

## 🚀 Schnellstart-Beispiele

### **1. Datenqualität schnell prüfen**

```python
import pandas as pd
import numpy as np

def quick_data_check(df):
    """Schnelle Datenqualitätsprüfung"""
    print("=== DATA QUALITY CHECK ===")
    print(f"Shape: {df.shape}")
    print(f"Missing values: {df.isnull().sum().sum()}")
    print(f"Duplicates: {df.duplicated().sum()}")
    print(f"Price range: ${df['price'].min():.2f} - ${df['price'].max():.2f}")
    print(f"Unique neighborhoods: {df['neighbourhood_group'].nunique()}")
    
    # Geografische Verteilung
    print(f"Longitude range: {df['longitude'].min():.3f} - {df['longitude'].max():.3f}")
    print(f"Latitude range: {df['latitude'].min():.3f} - {df['latitude'].max():.3f}")

# Verwendung
df = pd.read_csv('sample1.csv')
quick_data_check(df)
```

### **2. Feature Engineering Experiment**

```python
def create_advanced_features(df):
    """Erweiterte Features erstellen"""
    df = df.copy()
    
    # Zeitbasierte Features
    df['last_review'] = pd.to_datetime(df['last_review'])
    df['days_since_review'] = (pd.Timestamp.now() - df['last_review']).dt.days
    df['is_weekend'] = df['last_review'].dt.dayofweek >= 5
    
    # Geografische Features
    df['distance_to_center'] = np.sqrt(
        (df['latitude'] - 40.7589)**2 + (df['longitude'] - (-73.9851))**2
    )
    
    # Text-Features
    df['name_length'] = df['name'].str.len()
    df['has_wifi'] = df['name'].str.contains('wifi', case=False, na=False)
    df['has_parking'] = df['name'].str.contains('parking', case=False, na=False)
    df['has_gym'] = df['name'].str.contains('gym', case=False, na=False)
    
    # Preis-Features
    df['price_per_night'] = df['price'] / df['minimum_nights'].clip(lower=1)
    df['has_reviews'] = df['number_of_reviews'] > 0
    
    return df

# Testen
df_enhanced = create_advanced_features(df)
print(f"Neue Features: {df_enhanced.columns.tolist()}")
```

### **3. Modell-Vergleich**

```python
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

def compare_models(X_train, y_train, X_test, y_test):
    """Verschiedene ML-Algorithmen vergleichen"""
    
    models = {
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(random_state=42),
        'Linear Regression': LinearRegression()
    }
    
    results = {}
    
    for name, model in models.items():
        # Training
        model.fit(X_train, y_train)
        
        # Vorhersage
        y_pred = model.predict(X_test)
        
        # Evaluation
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        results[name] = {'MAE': mae, 'R²': r2}
        
        print(f"{name}: MAE={mae:.2f}, R²={r2:.3f}")
    
    return results

# Verwendung
results = compare_models(X_train, y_train, X_test, y_test)
```

## 📊 Visualisierung

### **4. Datenvisualisierung**

```python
import matplotlib.pyplot as plt
import seaborn as sns

def create_visualizations(df):
    """Umfassende Datenvisualisierung"""
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    # Preisverteilung
    axes[0,0].hist(df['price'], bins=50, alpha=0.7)
    axes[0,0].set_title('Price Distribution')
    axes[0,0].set_xlabel('Price ($)')
    
    # Nachbarschaften
    df['neighbourhood_group'].value_counts().plot(kind='bar', ax=axes[0,1])
    axes[0,1].set_title('Neighborhood Distribution')
    axes[0,1].tick_params(axis='x', rotation=45)
    
    # Geografische Verteilung
    axes[0,2].scatter(df['longitude'], df['latitude'], 
                     c=df['price'], cmap='viridis', alpha=0.6)
    axes[0,2].set_title('Geographic Distribution')
    axes[0,2].set_xlabel('Longitude')
    axes[0,2].set_ylabel('Latitude')
    
    # Preis vs. Reviews
    axes[1,0].scatter(df['number_of_reviews'], df['price'], alpha=0.6)
    axes[1,0].set_title('Price vs Reviews')
    axes[1,0].set_xlabel('Number of Reviews')
    axes[1,0].set_ylabel('Price ($)')
    
    # Room Type
    df['room_type'].value_counts().plot(kind='pie', ax=axes[1,1])
    axes[1,1].set_title('Room Type Distribution')
    
    # Korrelationsmatrix
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    corr_matrix = df[numeric_cols].corr()
    sns.heatmap(corr_matrix, annot=True, ax=axes[1,2], cmap='coolwarm')
    axes[1,2].set_title('Correlation Matrix')
    
    plt.tight_layout()
    plt.show()

# Verwendung
create_visualizations(df)
```

### **5. Feature Importance Visualisierung**

```python
def plot_feature_importance(model, feature_names, top_n=15):
    """Feature Importance visualisieren"""
    
    importance = model.feature_importances_
    indices = np.argsort(importance)[::-1][:top_n]
    
    plt.figure(figsize=(10, 8))
    plt.title(f"Top {top_n} Feature Importance")
    plt.bar(range(top_n), importance[indices])
    plt.xticks(range(top_n), [feature_names[i] for i in indices], rotation=45)
    plt.tight_layout()
    plt.show()
    
    # Feature Importance als DataFrame
    importance_df = pd.DataFrame({
        'feature': [feature_names[i] for i in indices],
        'importance': importance[indices]
    })
    
    return importance_df

# Verwendung
importance_df = plot_feature_importance(model, feature_names)
print(importance_df)
```

## 🔧 Pipeline-Erweiterungen

### **6. Automatische Hyperparameter-Optimierung**

```python
from sklearn.model_selection import GridSearchCV

def optimize_hyperparameters(X_train, y_train):
    """Hyperparameter automatisch optimieren"""
    
    rf = RandomForestRegressor(random_state=42)
    
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [10, 20, 50, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': ['sqrt', 'log2', 0.33]
    }
    
    grid_search = GridSearchCV(
        rf, param_grid, cv=5, 
        scoring='neg_mean_absolute_error',
        n_jobs=-1, verbose=1
    )
    
    grid_search.fit(X_train, y_train)
    
    print(f"Best parameters: {grid_search.best_params_}")
    print(f"Best score: {-grid_search.best_score_:.2f}")
    
    return grid_search.best_estimator_

# Verwendung
best_model = optimize_hyperparameters(X_train, y_train)
```

### **7. Cross-Validation mit verschiedenen Metriken**

```python
from sklearn.model_selection import cross_validate

def comprehensive_evaluation(model, X, y):
    """Umfassende Modell-Evaluation"""
    
    scoring = {
        'mae': 'neg_mean_absolute_error',
        'mse': 'neg_mean_squared_error',
        'r2': 'r2_score'
    }
    
    cv_results = cross_validate(
        model, X, y, cv=5, scoring=scoring, return_train_score=True
    )
    
    results = {}
    for metric in scoring.keys():
        results[f'{metric}_mean'] = -cv_results[f'test_{metric}'].mean()
        results[f'{metric}_std'] = cv_results[f'test_{metric}'].std()
    
    return results

# Verwendung
model = RandomForestRegressor(random_state=42)
results = comprehensive_evaluation(model, X, y)
print(results)
```

## 🚀 API-Entwicklung

### **8. Einfache Flask API**

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
        
        # Daten validieren
        required_fields = ['neighbourhood_group', 'room_type', 'latitude', 'longitude']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        # DataFrame erstellen
        df = pd.DataFrame([data])
        
        # Vorhersage
        prediction = model.predict(df)[0]
        
        return jsonify({
            'predicted_price': float(prediction),
            'confidence': 'high' if prediction > 0 else 'low'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health Check"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### **9. API-Testing**

```python
import requests
import json

def test_api():
    """API testen"""
    
    # Test-Daten
    test_data = {
        'neighbourhood_group': 'Manhattan',
        'room_type': 'Entire home/apt',
        'latitude': 40.7589,
        'longitude': -73.9851,
        'minimum_nights': 1,
        'number_of_reviews': 50
    }
    
    # API aufrufen
    response = requests.post(
        'http://localhost:5000/predict',
        json=test_data
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"Predicted price: ${result['predicted_price']:.2f}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Verwendung
test_api()
```

## 📊 Monitoring

### **10. Einfaches Monitoring Dashboard**

```python
import streamlit as st
import plotly.express as px
import pandas as pd

def create_dashboard():
    """Streamlit Monitoring Dashboard"""
    
    st.title("🏠 Airbnb Price Prediction Dashboard")
    
    # Sidebar
    st.sidebar.header("Settings")
    model_version = st.sidebar.selectbox("Model Version", ["v1.0", "v1.1", "v1.2"])
    
    # Hauptbereich
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("MAE", "32.5", "↓ 2.1")
    
    with col2:
        st.metric("R² Score", "0.588", "↑ 0.05")
    
    with col3:
        st.metric("Predictions Today", "1,234", "↑ 12%")
    
    # Charts
    st.subheader("Performance Over Time")
    
    # Simulierte Daten
    dates = pd.date_range('2025-01-01', periods=30, freq='D')
    mae_data = pd.DataFrame({
        'date': dates,
        'mae': np.random.normal(32, 2, 30)
    })
    
    fig = px.line(mae_data, x='date', y='mae', title='MAE Over Time')
    st.plotly_chart(fig)
    
    # Feature Importance
    st.subheader("Feature Importance")
    
    importance_data = pd.DataFrame({
        'feature': ['neighbourhood_group', 'room_type', 'latitude', 'longitude'],
        'importance': [0.3, 0.25, 0.2, 0.15]
    })
    
    fig = px.bar(importance_data, x='importance', y='feature', orientation='h')
    st.plotly_chart(fig)

# Verwendung
if __name__ == '__main__':
    create_dashboard()
```

## 🧪 Testing

### **11. Automatisierte Tests**

```python
import pytest
import pandas as pd

class TestDataQuality:
    """Datenqualitäts-Tests"""
    
    def test_no_missing_values(self, df):
        """Keine fehlenden Werte in kritischen Spalten"""
        critical_columns = ['price', 'latitude', 'longitude']
        assert df[critical_columns].isnull().sum().sum() == 0
    
    def test_price_range(self, df):
        """Preise im erwarteten Bereich"""
        assert df['price'].between(10, 500).all()
    
    def test_coordinate_range(self, df):
        """Koordinaten im NYC-Bereich"""
        assert df['longitude'].between(-74.25, -73.50).all()
        assert df['latitude'].between(40.5, 41.2).all()

class TestModel:
    """Modell-Tests"""
    
    def test_model_prediction(self, model, X_test):
        """Modell kann Vorhersagen machen"""
        predictions = model.predict(X_test)
        assert len(predictions) == len(X_test)
        assert all(pred > 0 for pred in predictions)
    
    def test_model_accuracy(self, model, X_test, y_test):
        """Modell-Genauigkeit"""
        predictions = model.predict(X_test)
        mae = mean_absolute_error(y_test, predictions)
        assert mae < 50  # MAE sollte unter 50 sein

# Tests ausführen
# pytest test_examples.py -v
```

## 🔄 CI/CD

### **12. GitHub Actions Workflow**

```yaml
# .github/workflows/ml-pipeline.yml
name: ML Pipeline CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest tests/ -v
    
    - name: Run data quality checks
      run: |
        python -m pytest src/data_check/ -v
    
    - name: Run ML pipeline
      run: |
        mlflow run . -P steps=all
```

---

**💡 Tipp:** Kopieren Sie diese Beispiele und passen Sie sie an Ihre Bedürfnisse an!

**🔄 Letzte Aktualisierung:** September 2025
