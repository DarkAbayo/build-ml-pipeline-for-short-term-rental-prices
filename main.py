#!/usr/bin/env python
"""
Main pipeline orchestration module for NYC Airbnb rental price prediction.

This module serves as the central orchestrator for the complete ML pipeline,
coordinating all pipeline steps from data ingestion to model training and testing.
It uses Hydra for configuration management and MLflow for step execution.

Pipeline Steps:
1. download: Download raw data from W&B
2. basic_cleaning: Clean and preprocess the data
3. data_check: Validate data quality and consistency
4. data_split: Split data into train/validation/test sets
5. train_random_forest: Train Random Forest model with hyperparameter optimization
6. test_regression_model: Test the production model against test data

Configuration:
- Uses Hydra configuration management with config.yaml
- Supports both local and remote component execution
- Configurable via command line parameters and Hydra overrides

Author: Niedermeier Patrick
Date: 2025-09-06
"""
import json

import mlflow
import tempfile
import os
import wandb
import hydra
from omegaconf import DictConfig

_steps = [
    "download",
    "basic_cleaning",
    "data_check",
    "data_split",
    "train_random_forest",
    # NOTE: We do not include this in the steps so it is not run by mistake.
    # You first need to promote a model export to "prod" before you can run this,
    # then you need to run this step explicitly
#    "test_regression_model"
]


# This automatically reads in the configuration
@hydra.main(config_name='config')
def go(config: DictConfig):
    """
    Execute the complete ML pipeline for NYC Airbnb rental price prediction.
    
    This function orchestrates the entire ML pipeline by executing the specified
    steps in sequence. It uses MLflow to run individual pipeline components
    and manages the flow of artifacts between steps.
    
    Pipeline Steps Executed:
    1. download: Downloads raw data from W&B using the specified sample
    2. basic_cleaning: Cleans data, removes outliers, applies geographic filters
    3. data_check: Validates data quality using comprehensive tests
    4. data_split: Splits data into train/validation/test sets
    5. train_random_forest: Trains Random Forest model with specified hyperparameters
    6. test_regression_model: Tests the production model (requires manual "prod" tag)
    
    Args:
        config (DictConfig): Hydra configuration object containing:
            - main: Pipeline configuration (project_name, experiment_name, steps)
            - etl: Data processing parameters (sample, price thresholds)
            - data_check: Data validation parameters (KL threshold)
            - modeling: Model training parameters (test_size, random_seed, hyperparameters)
    
    Environment Variables Set:
        WANDB_PROJECT: Set to config["main"]["project_name"]
        WANDB_RUN_GROUP: Set to config["main"]["experiment_name"]
    
    Returns:
        None: Pipeline execution results are logged to W&B and MLflow
    
    Raises:
        Exception: If any pipeline step fails during execution
        
    Example:
        The pipeline can be run with different configurations:
        - Full pipeline: mlflow run . -P steps=all
        - Specific steps: mlflow run . -P steps=train_random_forest
        - With overrides: mlflow run . -P hydra_options="etl.sample='sample2.csv'"
    """

    # Setup the wandb experiment. All runs will be grouped under this name
    os.environ["WANDB_PROJECT"] = config["main"]["project_name"]
    os.environ["WANDB_RUN_GROUP"] = config["main"]["experiment_name"]

    # Steps to execute
    steps_par = config['main']['steps']
    active_steps = steps_par.split(",") if steps_par != "all" else _steps

    # Move to a temporary directory
    with tempfile.TemporaryDirectory() as tmp_dir:

        if "download" in active_steps:
            # Download file and load in W&B
            _ = mlflow.run(
                f"{config['main']['components_repository']}/get_data",
                "main",
                version='main',
                env_manager="conda",
                parameters={
                    "sample": config["etl"]["sample"],
                    "artifact_name": "sample.csv",
                    "artifact_type": "raw_data",
                    "artifact_description": "Raw file as downloaded"
                },
            )

        if "basic_cleaning" in active_steps:
            # Run the basic_cleaning step
            _ = mlflow.run(
                os.path.join(hydra.utils.get_original_cwd(), "src", "basic_cleaning"),
                "main",
                parameters={
                    "input_artifact": "sample.csv:latest",
                    "output_artifact": "clean_sample.csv",
                    "output_type": "clean_sample",
                    "output_description": "Data with outliers and null values removed",
                    "min_price": config['etl']['min_price'],
                    "max_price": config['etl']['max_price']
                },
            )

        if "data_check" in active_steps:
            # run the data_check step
            _ = mlflow.run(
                os.path.join(hydra.utils.get_original_cwd(), "src", "data_check"),
                "main",
                parameters={
                    "csv": "clean_sample.csv:latest",
                    "ref": "clean_sample.csv:reference",
                    "kl_threshold": config["data_check"]["kl_threshold"],
                    "min_price": config["etl"]["min_price"],
                    "max_price": config["etl"]["max_price"]
                },
            )

        if "data_split" in active_steps:
            # run the data_split step
            _ = mlflow.run(
                f"{config['main']['components_repository']}/train_val_test_split",
                "main",
                version='main',
                env_manager="conda",
                parameters={
                    "input": "clean_sample.csv:latest",
                    "test_size": config["modeling"]["test_size"],
                    "random_seed": config["modeling"]["random_seed"],
                    "stratify_by": config["modeling"]["stratify_by"]
                },
            )

        if "train_random_forest" in active_steps:

            # NOTE: we need to serialize the random forest configuration into JSON
            rf_config = os.path.abspath("rf_config.json")
            with open(rf_config, "w+") as fp:
                json.dump(dict(config["modeling"]["random_forest"].items()), fp)  # DO NOT TOUCH

            # NOTE: use the rf_config we just created as the rf_config parameter for the train_random_forest
            # step

            # Run the train_random_forest step
            _ = mlflow.run(
                os.path.join(hydra.utils.get_original_cwd(), "src", "train_random_forest"),
                "main",
                parameters={
                    "trainval_artifact": "trainval_data.csv:latest",
                    "val_size": config["modeling"]["val_size"],
                    "random_seed": config["modeling"]["random_seed"],
                    "stratify_by": config["modeling"]["stratify_by"],
                    "rf_config": rf_config,
                    "max_tfidf_features": config["modeling"]["max_tfidf_features"],
                    "output_artifact": "random_forest_export"
                },
            )

        if "test_regression_model" in active_steps:

            # Run the test_regression_model step (local version)
            _ = mlflow.run(
                os.path.join(hydra.utils.get_original_cwd(), "src", "test_regression_model"),
                "main",
                parameters={
                    "mlflow_model": "random_forest_export:prod",
                    "test_dataset": "test_data.csv:latest"
                },
            )


if __name__ == "__main__":
    go()
