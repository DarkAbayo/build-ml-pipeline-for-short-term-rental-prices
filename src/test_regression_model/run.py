#!/usr/bin/env python
"""
This step takes the best model, tagged with the "prod" tag, and tests it against the test dataset
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
    Fix compatibility issues with ColumnTransformer between scikit-learn versions
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
