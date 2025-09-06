#!/usr/bin/env python
"""
Random Forest training module for NYC Airbnb rental price prediction pipeline.

This module implements the complete Random Forest training pipeline including
feature engineering, preprocessing, model training, and evaluation. It creates
a comprehensive ML pipeline with categorical encoding, text processing, and
geographic feature handling.

Key Features:
- Comprehensive feature engineering with TF-IDF text processing
- Categorical encoding for room types and neighborhoods
- Geographic coordinate processing and imputation
- Date feature engineering (days since last review)
- Random Forest model training with configurable hyperparameters
- Feature importance visualization and logging

Author: Niedermeier Patrick
Date: 2025-09-06
"""
import argparse
import logging
import os
import shutil
import matplotlib.pyplot as plt

import mlflow
import json

import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder, FunctionTransformer

import wandb
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import Pipeline, make_pipeline


def delta_date_feature(dates):
    """
    Given a 2d array containing dates (in any format recognized by pd.to_datetime), it returns the delta in days
    between each date and the most recent date in its column
    """
    date_sanitized = pd.DataFrame(dates).apply(pd.to_datetime)
    return date_sanitized.apply(lambda d: (d.max() -d).dt.days, axis=0).to_numpy()


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):
    """
    Execute the complete Random Forest training pipeline.
    
    This function orchestrates the entire training process including data loading,
    preprocessing, feature engineering, model training, evaluation, and artifact
    creation. It creates a comprehensive ML pipeline and trains a Random Forest
    regressor for Airbnb rental price prediction.
    
    Training Process:
    1. Load training/validation data from W&B artifact
    2. Split data into train/validation sets with stratification
    3. Create comprehensive preprocessing pipeline with:
       - Categorical encoding (ordinal and one-hot)
       - Text processing with TF-IDF vectorization
       - Geographic coordinate imputation
       - Date feature engineering
    4. Train Random Forest model with specified hyperparameters
    5. Evaluate model performance (R² and MAE)
    6. Export model in MLflow format
    7. Create feature importance visualization
    8. Log results and artifacts to W&B
    
    Args:
        args: argparse.Namespace containing:
            - trainval_artifact (str): W&B artifact name for training data
            - val_size (float): Fraction of data to use for validation
            - random_seed (int): Random seed for reproducibility
            - stratify_by (str): Column name for stratified splitting
            - rf_config (str): Path to JSON file with Random Forest hyperparameters
            - max_tfidf_features (int): Maximum number of TF-IDF features
            - output_artifact (str): Name for the output model artifact
    
    Returns:
        None: Results are logged to W&B and model is saved as artifact
    
    Raises:
        Exception: If any step in the training process fails
        
    Side Effects:
        - Creates 'random_forest_dir' directory with MLflow model
        - Logs model artifact to W&B
        - Logs feature importance plot to W&B
        - Updates W&B run summary with performance metrics
    """

    run = wandb.init(job_type="train_random_forest")
    run.config.update(args)

    # Get the Random Forest configuration and update W&B
    with open(args.rf_config) as fp:
        rf_config = json.load(fp)
    run.config.update(rf_config)

    # Fix the random seed for the Random Forest, so we get reproducible results
    rf_config['random_state'] = args.random_seed

    # Get the train and validation artifact
    trainval_local_path = run.use_artifact(args.trainval_artifact).file()

    X = pd.read_csv(trainval_local_path)
    y = X.pop("price")  # this removes the column "price" from X and puts it into y

    logger.info(f"Minimum price: {y.min()}, Maximum price: {y.max()}")

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=args.val_size, stratify=X[args.stratify_by], random_state=args.random_seed
    )

    logger.info("Preparing sklearn pipeline")

    sk_pipe, processed_features = get_inference_pipeline(rf_config, args.max_tfidf_features)

    # Then fit it to the X_train, y_train data
    logger.info("Fitting")

    # Fit the pipeline sk_pipe by calling the .fit method on X_train and y_train
    sk_pipe.fit(X_train, y_train)

    # Compute r2 and MAE
    logger.info("Scoring")
    r_squared = sk_pipe.score(X_val, y_val)

    y_pred = sk_pipe.predict(X_val)
    mae = mean_absolute_error(y_val, y_pred)

    logger.info(f"Score: {r_squared}")
    logger.info(f"MAE: {mae}")

    logger.info("Exporting model")

    # Save model package in the MLFlow sklearn format
    if os.path.exists("random_forest_dir"):
        shutil.rmtree("random_forest_dir")

    # Save the sk_pipe pipeline as a mlflow.sklearn model in the directory "random_forest_dir"
    mlflow.sklearn.save_model(sk_pipe, "random_forest_dir")

    # Upload the model we just exported to W&B
    artifact = wandb.Artifact(
        args.output_artifact, 
        type="model_export", 
        description="Random Forest", 
        metadata=rf_config
    )
    artifact.add_dir("random_forest_dir")
    run.log_artifact(artifact)

    # Plot feature importance
    fig_feat_imp = plot_feature_importance(sk_pipe, processed_features)

    run.summary['r2'] = r_squared
    run.summary['mae'] = mae

    # Upload to W&B the feture importance visualization
    run.log(
        {
          "feature_importance": wandb.Image(fig_feat_imp),
        }
    )


def plot_feature_importance(pipe, feat_names):
    """
    Create a feature importance visualization for the trained Random Forest model.
    
    This function extracts feature importances from the trained Random Forest model
    and creates a bar chart visualization. For NLP features (TF-IDF), it aggregates
    all TF-IDF dimensions into a single importance score.
    
    Args:
        pipe (sklearn.pipeline.Pipeline): The trained ML pipeline containing the Random Forest
        feat_names (list): List of feature names corresponding to the model features
        
    Returns:
        matplotlib.figure.Figure: Figure object containing the feature importance plot
        
    Note:
        - Non-NLP features get individual importance scores
        - NLP features (TF-IDF) are aggregated into a single importance score
        - The plot shows features in the order they appear in the pipeline
    """
    # We collect the feature importance for all non-nlp features first
    feat_imp = pipe["random_forest"].feature_importances_[: len(feat_names)-1]
    # For the NLP feature we sum across all the TF-IDF dimensions into a global
    # NLP importance
    nlp_importance = sum(pipe["random_forest"].feature_importances_[len(feat_names) - 1:])
    feat_imp = np.append(feat_imp, nlp_importance)
    fig_feat_imp, sub_feat_imp = plt.subplots(figsize=(10, 10))
    # idx = np.argsort(feat_imp)[::-1]
    sub_feat_imp.bar(range(feat_imp.shape[0]), feat_imp, color="r", align="center")
    _ = sub_feat_imp.set_xticks(range(feat_imp.shape[0]))
    _ = sub_feat_imp.set_xticklabels(np.array(feat_names), rotation=90)
    fig_feat_imp.tight_layout()
    return fig_feat_imp


def get_inference_pipeline(rf_config, max_tfidf_features):
    """
    Create a comprehensive ML preprocessing and inference pipeline.
    
    This function constructs a complete scikit-learn pipeline for Airbnb rental
    price prediction. It includes comprehensive feature engineering, preprocessing,
    and a Random Forest regressor for final prediction.
    
    Pipeline Components:
    1. Categorical Encoding:
       - Ordinal encoding for room_type (meaningful order)
       - One-hot encoding for neighbourhood_group (no inherent order)
    2. Numerical Feature Imputation:
       - Zero imputation for missing numerical values
    3. Date Feature Engineering:
       - Days since last review calculation
    4. Text Processing:
       - TF-IDF vectorization of property names
    5. Random Forest Regression:
       - Final prediction model with configurable hyperparameters
    
    Args:
        rf_config (dict): Random Forest hyperparameters including:
            - n_estimators: Number of trees
            - max_depth: Maximum tree depth
            - min_samples_split: Minimum samples to split a node
            - min_samples_leaf: Minimum samples in a leaf
            - max_features: Number of features to consider for splits
            - criterion: Splitting criterion
            - random_state: Random seed for reproducibility
        max_tfidf_features (int): Maximum number of TF-IDF features to extract
    
    Returns:
        tuple: (sk_pipe, processed_features) where:
            - sk_pipe (sklearn.pipeline.Pipeline): Complete ML pipeline
            - processed_features (list): List of feature names in order
    
    Feature Engineering Details:
        - Room types are encoded ordinally (Entire home/apt > Private room > Shared room)
        - Neighborhood groups are one-hot encoded
        - Missing numerical values are imputed with 0
        - Missing review dates are imputed with '2010-01-01' (old date)
        - Date features represent days since last review
        - Property names are processed with TF-IDF (English stop words removed)
    """
    # Let's handle the categorical features first
    # Ordinal categorical are categorical values for which the order is meaningful, for example
    # for room type: 'Entire home/apt' > 'Private room' > 'Shared room'
    ordinal_categorical = ["room_type"]
    non_ordinal_categorical = ["neighbourhood_group"]
    # NOTE: we do not need to impute room_type because the type of the room
    # is mandatory on the websites, so missing values are not possible in production
    # (nor during training). That is not true for neighbourhood_group
    ordinal_categorical_preproc = OrdinalEncoder()

    non_ordinal_categorical_preproc = make_pipeline(
        SimpleImputer(strategy="most_frequent"),
        OneHotEncoder(handle_unknown="ignore")
    )

    # Let's impute the numerical columns to make sure we can handle missing values
    # (note that we do not scale because the RF algorithm does not need that)
    zero_imputed = [
        "minimum_nights",
        "number_of_reviews",
        "reviews_per_month",
        "calculated_host_listings_count",
        "availability_365",
        "longitude",
        "latitude"
    ]
    zero_imputer = SimpleImputer(strategy="constant", fill_value=0)

    # A MINIMAL FEATURE ENGINEERING step:
    # we create a feature that represents the number of days passed since the last review
    # First we impute the missing review date with an old date (because there hasn't been
    # a review for a long time), and then we create a new feature from it,
    date_imputer = make_pipeline(
        SimpleImputer(strategy='constant', fill_value='2010-01-01'),
        FunctionTransformer(delta_date_feature, check_inverse=False, validate=False)
    )

    # Some minimal NLP for the "name" column
    reshape_to_1d = FunctionTransformer(np.reshape, kw_args={"newshape": -1})
    name_tfidf = make_pipeline(
        SimpleImputer(strategy="constant", fill_value=""),
        reshape_to_1d,
        TfidfVectorizer(
            binary=False,
            max_features=max_tfidf_features,
            stop_words='english'
        ),
    )

    # Let's put everything together
    preprocessor = ColumnTransformer(
        transformers=[
            ("ordinal_cat", ordinal_categorical_preproc, ordinal_categorical),
            ("non_ordinal_cat", non_ordinal_categorical_preproc, non_ordinal_categorical),
            ("impute_zero", zero_imputer, zero_imputed),
            ("transform_date", date_imputer, ["last_review"]),
            ("transform_name", name_tfidf, ["name"])
        ],
        remainder="drop",  # This drops the columns that we do not transform
    )

    processed_features = ordinal_categorical + non_ordinal_categorical + zero_imputed + ["last_review", "name"]

    # Create random forest
    random_forest = RandomForestRegressor(**rf_config)

    ######################################
    # Create the inference pipeline. The pipeline must have 2 steps: a step called "preprocessor" applying the
    # ColumnTransformer instance that we saved in the `preprocessor` variable, and a step called "random_forest"
    # with the random forest instance that we just saved in the `random_forest` variable.
    # HINT: Use the explicit Pipeline constructor so you can assign the names to the steps, do not use make_pipeline
    sk_pipe = Pipeline([
        ("preprocessor", preprocessor),
        ("random_forest", random_forest)
    ])

    return sk_pipe, processed_features


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Basic cleaning of dataset")

    parser.add_argument(
        "--trainval_artifact",
        type=str,
        help="Artifact containing the training dataset. It will be split into train and validation"
    )

    parser.add_argument(
        "--val_size",
        type=float,
        help="Size of the validation split. Fraction of the dataset, or number of items",
    )

    parser.add_argument(
        "--random_seed",
        type=int,
        help="Seed for random number generator",
        default=42,
        required=False,
    )

    parser.add_argument(
        "--stratify_by",
        type=str,
        help="Column to use for stratification",
        default="none",
        required=False,
    )

    parser.add_argument(
        "--rf_config",
        help="Random forest configuration. A JSON dict that will be passed to the "
        "scikit-learn constructor for RandomForestRegressor.",
        default="{}",
    )

    parser.add_argument(
        "--max_tfidf_features",
        help="Maximum number of words to consider for the TFIDF",
        default=10,
        type=int
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="Name for the output serialized model",
        required=True,
    )

    args = parser.parse_args()

    go(args)
