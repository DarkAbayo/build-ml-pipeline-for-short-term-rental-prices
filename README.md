# 🏠 NYC Airbnb Short-Term Rental Price Prediction Pipeline

A complete Machine Learning pipeline for predicting short-term rental prices in New York City, developed with MLflow and Weights & Biases.

## 📋 Project Overview

This project implements an end-to-end ML pipeline for a property management company that rents rooms and properties for short periods on various rental platforms. The pipeline estimates typical prices for given properties based on similar characteristics and is retrained weekly with new data.

### 🎯 Main Objectives
- **Automated price estimation** for Airbnb properties in NYC
- **Weekly retraining** with new data
- **Reproducible pipeline** with MLflow
- **Experiment tracking** with Weights & Biases
- **Production-ready** solution with tests and validation

## 🏗️ Pipeline Architecture

```
Raw Data → EDA → Data Cleaning → Data Testing → Train/Val/Test Split → Model Training → Hyperparameter Optimization → Model Selection → Testing → Production
```

### Pipeline Components

1. **Data Download** - Download raw data
2. **Exploratory Data Analysis (EDA)** - Data exploration with Jupyter Notebook
3. **Basic Cleaning** - Data cleaning and outlier removal
4. **Data Testing** - Automated data quality tests
5. **Data Splitting** - Split into Train/Validation/Test sets
6. **Model Training** - Random Forest Regressor training
7. **Hyperparameter Optimization** - Grid Search for best parameters
8. **Model Selection** - Select best performing model
9. **Model Testing** - Evaluation on test data
10. **Production Deployment** - Deploy for production use

## 🚀 Quick Start

### Prerequisites

- **Python 3.10** (required)
- **Conda** installed
- **Git** for repository management

### Supported Operating Systems

- ✅ Ubuntu 22.04 (Jammy Jellyfish) - Ubuntu installation and WSL
- ✅ Ubuntu 24.04 - Ubuntu installation and WSL  
- ✅ macOS - Compatible with recent macOS versions

### Installation

1. **Clone repository:**
```bash
git clone https://github.com/DarkAbayo/build-ml-pipeline-for-short-term-rental-prices.git
cd build-ml-pipeline-for-short-term-rental-prices
```

2. **Create conda environment:**
```bash
conda env create -f environment.yml
conda activate nyc_airbnb_dev
```

3. **Setup Weights & Biases:**
```bash
wandb login [your-api-key]
```

### Running the Pipeline

**Full pipeline:**
```bash
mlflow run .
```

**Individual steps:**
```bash
# Download only
mlflow run . -P steps=download

# Download and cleaning
mlflow run . -P steps=download,basic_cleaning

# With parameter override
mlflow run . \
  -P steps=train_random_forest \
  -P hydra_options="modeling.random_forest.n_estimators=200 etl.min_price=50"
```

## 📊 Data

### Dataset
- **Source:** NYC Airbnb Open Data
- **Size:** ~48,895 samples
- **Features:** 16 columns (geolocation, price, room type, etc.)
- **Target variable:** Price per night (USD)

### Data Quality
- **Price range:** $10 - $350 per night
- **Geographic boundaries:** NYC coordinates
- **Missing values:** Handled in pipeline
- **Outliers:** Automatically removed

## 🤖 Model

### Algorithm
- **Random Forest Regressor** (Scikit-learn)
- **Hyperparameter optimization** with Grid Search
- **Feature engineering** with TF-IDF for text data

### Optimal Parameters
```yaml
random_forest:
  n_estimators: 100
  max_depth: 50
  min_samples_split: 4
  min_samples_leaf: 3
  max_features: 0.33
  criterion: squared_error
```

### Performance
- **Mean Absolute Error (MAE):** ~$32.50
- **R² Score:** ~0.588
- **Cross-Validation:** 5-Fold CV

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.10** - Programming language
- **MLflow** - Pipeline orchestration
- **Weights & Biases** - Experiment tracking
- **Hydra** - Configuration management

### Data Science Libraries
- **Pandas** - Data processing
- **NumPy** - Numerical operations
- **Scikit-learn** - Machine Learning
- **Matplotlib/Seaborn** - Visualization

### Development Tools
- **Pytest** - Testing framework
- **Jupyter** - Interactive development
- **Cookiecutter** - Project templates

## 📁 Project Structure

```
build-ml-pipeline-for-short-term-rental-prices/
├── src/                          # Pipeline components
│   ├── basic_cleaning/          # Data cleaning
│   ├── data_check/              # Data quality tests
│   ├── eda/                     # Exploratory Data Analysis
│   └── train_random_forest/     # Model training
├── components/                   # Reusable components
├── Docs/                        # Documentation
├── images/                      # Project images
├── config.yaml                  # Pipeline configuration
├── main.py                      # Main pipeline
├── environment.yml              # Conda environment
└── README.md                    # This file
```

## 🔧 Configuration

The pipeline is configured via `config.yaml`:

```yaml
main:
  project_name: nyc_airbnb
  experiment_name: development

etl:
  sample: "sample1.csv"
  min_price: 10
  max_price: 350

modeling:
  test_size: 0.2
  val_size: 0.2
  random_seed: 456
  stratify_by: "neighbourhood_group"
  max_tfidf_features: 15
```

## 🧪 Testing

### Data Quality Tests
- **Row count:** 15,000 < rows < 1,000,000
- **Price range:** Between min_price and max_price
- **Geographic boundaries:** NYC coordinates
- **Kolmogorov-Smirnov test:** Data distribution

### Model Tests
- **Performance metrics:** MAE, R², RMSE
- **Cross-validation:** 5-Fold CV
- **Feature importance:** Identify top features

## 📈 Monitoring & Tracking

### Weights & Biases Integration
- **Experiment tracking:** All runs are logged
- **Artifact management:** Models and datasets versioned
- **Visualization:** Pipeline graph and metrics
- **Hyperparameter tracking:** All parameters tracked

### MLflow Integration
- **Pipeline orchestration:** Step-by-step execution
- **Model registry:** Model versioning
- **Reproducibility:** Deterministic execution

## 🚀 Deployment

### Production Pipeline
```bash
# Use release
mlflow run https://github.com/DarkAbayo/build-ml-pipeline-for-short-term-rental-prices.git \
  -v 1.0.0 \
  -P hydra_options="etl.sample='sample2.csv'"
```

### API Integration
The trained model can be used via a REST API:
```python
import requests

# Example API call
data = {
    'latitude': 40.7589,
    'longitude': -73.9851,
    'room_type': 'Entire home/apt',
    'neighbourhood_group': 'Manhattan'
}

response = requests.post('http://localhost:5000/predict', json=data)
prediction = response.json()['predicted_price']
```

## 📚 Learning Resources

### For Beginners
- [Beginner Learning Path](Docs/BEGINNER_LEARNING_PATH.md) - Step-by-step guide
- [Python Basics](https://docs.python.org/3/tutorial/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

### For Advanced Users
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [Weights & Biases Docs](https://docs.wandb.ai/)
- [Scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)

## 🔗 Important Links

- **📊 Pipeline Visualization:** [W&B Pipeline Graph](https://wandb.ai/dark_pn-private/nyc_airbnb/artifacts/model_export/random_forest_export/v220/lineage)
- **🐙 GitHub Repository:** [GitHub Repository](https://github.com/DarkAbayo/build-ml-pipeline-for-short-term-rental-prices)
- **📈 Weights & Biases:** [W&B Project](https://wandb.ai/dark_pn-private/nyc_airbnb)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE.txt](LICENSE.txt) for details.

## 👨‍💻 Author

**Dark Abayo**
- GitHub: [@DarkAbayo](https://github.com/DarkAbayo)
- W&B: [dark_pn-private](https://wandb.ai/dark_pn-private)

## 🤖 AI-Assisted Development

**Development Note:** This project was developed using AI tools (e.g., code generation, documentation, suggestions), with human review and refinement applied throughout the development process. AI assistance served as a tool to accelerate development, while all critical decisions, code reviews, and final implementations were conducted by human developers.

---

**Last Updated:** January 2025  
**Version:** 1.0.0  
**Status:** Production Ready ✅