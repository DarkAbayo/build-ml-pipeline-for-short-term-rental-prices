#!/usr/bin/env python
"""
Basic data cleaning module for NYC Airbnb rental price prediction pipeline.

This module downloads raw data from Weights & Biases, applies basic cleaning operations
including outlier removal and data type conversions, and uploads the cleaned data
as a new artifact.

Key cleaning operations:
- Remove price outliers outside specified range
- Convert last_review column to datetime format
- Handle missing values appropriately
- Save cleaned data to CSV format

Author: Niedermeier Patrick
Date: 2025-06-30
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()

def go(args):
    """
    Execute the basic data cleaning pipeline.
    
    This function orchestrates the entire cleaning process:
    1. Initialize W&B run
    2. Download input artifact
    3. Apply data cleaning transformations
    4. Save and upload cleaned data
    
    Args:
        args: argparse.Namespace
            Object containing all command line arguments:
            - input_artifact (str): Name of input artifact with version tag
            - output_artifact (str): Name for output artifact
            - output_type (str): Type classification for output artifact
            - output_description (str): Description of the cleaning process
            - min_price (float): Minimum price threshold for outlier removal
            - max_price (float): Maximum price threshold for outlier removal
    
    Raises:
        Exception: If any step in the cleaning process fails
        
    Returns:
        None: Function uploads artifact to W&B and logs results
    """
    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    logger.info("Starting basic cleaning process")

    try:
        # Download input artifact. This will also log that this script is using this
        # particular version of the artifact
        logger.info("Downloading artifact: %s", args.input_artifact)
        artifact_local_path = run.use_artifact(args.input_artifact).file()
        logger.info("Artifact downloaded successfully to: %s", artifact_local_path)

        # Load data from artifact
        logger.info("Loading data from artifact")
        df = pd.read_csv(artifact_local_path)

        logger.info("Original data shape: %s", df.shape)
        logger.info("Original price range: %s - %s", df['price'].min(), df['price'].max())

        # Before cleaning
        logger.info("Data types before cleaning: %s", df.dtypes.to_dict())
        logger.info("Missing values before cleaning: %s", df.isnull().sum().to_dict())

        # Remove price outliers
        logger.info("Removing price outliers outside range [%s, %s]", 
                   args.min_price, args.max_price)
        idx = df['price'].between(args.min_price, args.max_price)
        df = df[idx].copy()

        logger.info("Data shape after price filtering: %s", df.shape)

        # Convert last_review to datetime
        logger.info("Converting last_review column to datetime")
        df['last_review'] = pd.to_datetime(df['last_review'])

        # Save cleaned data
        logger.info("Saving cleaned data")
        # "index=False" is important to avoid an extra index column in the output file
        df.to_csv("clean_sample.csv", index=False) 

        # Upload to W&B
        logger.info("Uploading artifact: %s", args.output_artifact)
        artifact = wandb.Artifact(
            args.output_artifact, 
            type=args.output_type, 
            description=args.output_description
        )
        artifact.add_file("clean_sample.csv")
        run.log_artifact(artifact)

        logger.info("Basic cleaning completed successfully")

        # After cleaning
        logger.info("Data types after cleaning: %s", df.dtypes.to_dict())
        logger.info("Missing values after cleaning: %s", df.isnull().sum().to_dict())
        logger.info("Price statistics after cleaning: mean=%.2f, std=%.2f", 
                   df['price'].mean(), df['price'].std())

    except Exception as e:
        logger.error("Error during basic cleaning: %s", str(e))
        raise
    finally:
        run.finish()


if __name__ == "__main__":
    """
    Command line interface for basic data cleaning.
    
    This script can be run directly from the command line with appropriate
    arguments for input/output artifacts and cleaning parameters.
    
    Example usage:
        python run.py --input_artifact sample.csv:latest \
                     --output_artifact clean_sample.csv \
                     --output_type clean_sample \
                     --output_description "Data with outliers removed" \
                     --min_price 10.0 \
                     --max_price 350.0
    """
    parser = argparse.ArgumentParser(
        description="A very basic data cleaning",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input_artifact sample.csv:latest --output_artifact clean_sample.csv \\
           --output_type clean_sample --output_description "Cleaned data" \\
           --min_price 10.0 --max_price 350.0
        """
    )

    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Input artifact name with version tag (e.g., 'sample.csv:latest')",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Output artifact name (e.g., 'clean_sample.csv')",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Type classification for output artifact (e.g., 'clean_sample')",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description of the cleaning process and output data",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Minimum price threshold for filtering outliers (e.g., 10.0)",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Maximum price threshold for filtering outliers (e.g., 350.0)",
        required=True
    )

    parsed_args = parser.parse_args()

    go(parsed_args)
