#!/usr/bin/env python
"""
Weights & Biases artifact logging utility.

This module provides utility functions for logging artifacts to Weights & Biases
and integrating with MLflow for pipeline artifact management.

Author: Niedermeier Patrick
Date: 2025-09-06
"""
import wandb
import mlflow


def log_artifact(artifact_name, artifact_type, artifact_description, filename, wandb_run):
    """
    Log a file as an artifact in Weights & Biases and make it available for MLflow.
    
    This function creates a W&B artifact from a local file and ensures it's properly
    registered so that subsequent pipeline steps can access it. The artifact is
    logged to the current W&B run and made available for MLflow tracking.
    
    Args:
        artifact_name (str): Name for the artifact (e.g., "sample.csv", "model.pkl")
        artifact_type (str): Type classification for the artifact (e.g., "raw_data", "clean_data", "model")
        artifact_description (str): Brief description of what the artifact contains
        filename (str): Local file path to the artifact file
        wandb_run (wandb.sdk.wandb_run.Run): Current Weights & Biases run object
        
    Returns:
        None: Artifact is logged to W&B and made available for MLflow
        
    Side Effects:
        - Creates W&B artifact and uploads file
        - Waits for artifact to be processed and versioned
        - Makes artifact available for subsequent pipeline steps
        
    Example:
        >>> run = wandb.init()
        >>> log_artifact("clean_data.csv", "clean_data", "Cleaned dataset", "data/clean.csv", run)
    """
    # Log to W&B
    artifact = wandb.Artifact(
        artifact_name,
        type=artifact_type,
        description=artifact_description,
    )
    artifact.add_file(filename)
    wandb_run.log_artifact(artifact)
    # We need to call this .wait() method before we can use the
    # version below. This will wait until the artifact is loaded into W&B and a
    # version is assigned
    artifact.wait()
