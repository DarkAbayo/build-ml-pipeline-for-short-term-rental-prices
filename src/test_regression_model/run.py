#!/usr/bin/env python
"""
Model testing module for NYC Airbnb rental price prediction pipeline.

This module tests the production-ready model (tagged with "prod") against the
test dataset to evaluate final performance. It handles model loading, prediction,
and performance metric calculation with comprehensive error handling for
scikit-learn version compatibility issues.

Key Features:
- Loads production model from W&B artifacts
- Performs inference on test dataset
- Calculates performance metrics (R² and MAE)
- Handles scikit-learn version compatibility issues
- Logs results to W&B for tracking

Author: Niedermeier Patrick
Date: 2025-09-06
"""
import argparse
import logging
import wandb
import mlflow
import pandas as pd
from sklearn.metrics import mean_absolute_error
import warnings

from wandb_utils.log_artifact import log_artifact


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def fix_column_transformer_compatibility(sk_pipe):
    """
    Fix compatibility issues with ColumnTransformer between scikit-learn versions.
    
    This function addresses compatibility problems that arise when models trained
    with one version of scikit-learn are loaded with a different version. The
    main issue is the missing `_name_to_fitted_passthrough` attribute that was
    removed in newer versions of scikit-learn.
    
    Args:
        sk_pipe (sklearn.pipeline.Pipeline): The loaded ML pipeline containing a ColumnTransformer
        
    Returns:
        None: Modifies the pipeline in-place
        
    Note:
        This is a workaround for scikit-learn version compatibility issues.
        The function safely handles cases where the attribute doesn't exist
        or the pipeline structure is unexpected.
    """
    try:
        # Get the preprocessor step
        preprocessor = sk_pipe.named_steps['preprocessor']
        
        # Check if this is a ColumnTransformer and needs the _name_to_fitted_passthrough attribute
        if hasattr(preprocessor, 'transformers_') and not hasattr(preprocessor, '_name_to_fitted_passthrough'):
            logger.info("Fixing ColumnTransformer compatibility for scikit-learn 1.7.0")
            # Add the missing attribute that was removed in newer versions
            preprocessor._name_to_fitted_passthrough = {}
            
    except Exception as e:
        logger.warning(f"Could not fix ColumnTransformer compatibility: {e}")


def go(args):
    """
    Execute model testing against the test dataset.
    
    This function loads the production model (tagged with "prod"), performs
    inference on the test dataset, and calculates performance metrics. It includes
    comprehensive error handling for scikit-learn version compatibility issues
    that may arise between different versions of the library.
    
    Testing Process:
    1. Initialize W&B run for tracking
    2. Download production model artifact from W&B
    3. Download test dataset artifact from W&B
    4. Load test data and separate features from target
    5. Load MLflow model with compatibility fixes
    6. Perform predictions on test data
    7. Calculate performance metrics (R² and MAE)
    8. Log results to W&B
    
    Args:
        args: argparse.Namespace containing:
            - mlflow_model (str): W&B artifact name for the production model (e.g., "random_forest_export:prod")
            - test_dataset (str): W&B artifact name for the test dataset (e.g., "test_data.csv:latest")
    
    Returns:
        None: Results are logged to W&B run summary
    
    Raises:
        Exception: If model loading or prediction fails
        
    Compatibility Notes:
        - Handles scikit-learn version differences between 1.3.2 and 1.7.0
        - Fixes ColumnTransformer compatibility issues
        - Suppresses sklearn warnings during model loading
    """

    run = wandb.init(job_type="test_model")
    run.config.update(args)

    logger.info("Downloading artifacts")
    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    model_local_path = run.use_artifact(args.mlflow_model).download()

    # Download test dataset
    test_dataset_path = run.use_artifact(args.test_dataset).file()

    # Read test dataset
    X_test = pd.read_csv(test_dataset_path)
    y_test = X_test.pop("price")

    logger.info("Loading model and performing inference on test set")
    
    # Suppress sklearn version warnings
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")
        warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn")
        
        sk_pipe = mlflow.sklearn.load_model(model_local_path)
    
    # Fix compatibility issues
    fix_column_transformer_compatibility(sk_pipe)
    
    # Perform prediction with error handling
    try:
        y_pred = sk_pipe.predict(X_test)
    except AttributeError as e:
        if "_name_to_fitted_passthrough" in str(e):
            logger.warning("ColumnTransformer compatibility issue detected. Attempting to fix...")
            # Try to fix the ColumnTransformer issue
            try:
                # Access the preprocessor and try to fix the attribute issue
                preprocessor = sk_pipe.named_steps['preprocessor']
                if hasattr(preprocessor, 'transformers_'):
                    # Force re-initialization of problematic attributes
                    if not hasattr(preprocessor, '_name_to_fitted_passthrough'):
                        preprocessor._name_to_fitted_passthrough = {}
                    y_pred = sk_pipe.predict(X_test)
                else:
                    raise e
            except Exception as fix_error:
                logger.error(f"Could not fix ColumnTransformer issue: {fix_error}")
                raise e
        else:
            raise e

    logger.info("Scoring")
    r_squared = sk_pipe.score(X_test, y_test)

    mae = mean_absolute_error(y_test, y_pred)

    logger.info(f"Score: {r_squared}")
    logger.info(f"MAE: {mae}")

    # Log MAE and r2
    run.summary['r2'] = r_squared
    run.summary['mae'] = mae


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Test the provided model against the test dataset")

    parser.add_argument(
        "--mlflow_model",
        type=str, 
        help="Input MLFlow model",
        required=True
    )

    parser.add_argument(
        "--test_dataset",
        type=str, 
        help="Test dataset",
        required=True
    )

    args = parser.parse_args()

    go(args)
