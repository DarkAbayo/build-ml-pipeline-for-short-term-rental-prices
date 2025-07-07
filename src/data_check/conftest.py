#!/usr/bin/env python
"""
Pytest configuration and fixtures for NYC Airbnb data quality testing.

This module provides pytest fixtures and configuration for the data quality testing
suite. It handles artifact downloads from Weights & Biases and provides test data
to the individual test functions.

Key fixtures:
- data: Downloads and loads the current dataset for testing
- ref_data: Downloads and loads the reference dataset for comparison
- kl_threshold: Provides the KL divergence threshold parameter
- min_price: Provides the minimum price threshold parameter
- max_price: Provides the maximum price threshold parameter

Author: Niedermeier Patrick
Date: 2025-07-07
"""
import pytest
import pandas as pd
import wandb
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    """
    Add custom command line options for pytest.
    
    This function registers custom command line arguments that can be passed
    to pytest for configuring the data quality tests. These arguments are
    used to specify input artifacts and test parameters.
    
    Args:
        parser: pytest argument parser object
        
    Returns:
        None: Modifies parser in-place
    """
    logger.info("Configuring pytest command line options")
    
    parser.addoption("--csv", action="store", help="Input CSV artifact name")
    parser.addoption("--ref", action="store", help="Reference CSV artifact name")
    parser.addoption("--kl_threshold", action="store", help="KL divergence threshold")
    parser.addoption("--min_price", action="store", help="Minimum price threshold")
    parser.addoption("--max_price", action="store", help="Maximum price threshold")
    
    logger.info("Pytest options configured successfully")


@pytest.fixture(scope='session')
def data(request):
    """
    Fixture to download and load the current dataset for testing.
    
    This fixture initializes a W&B run, downloads the specified CSV artifact,
    loads it into a pandas DataFrame, and provides it to test functions.
    The fixture has session scope to avoid repeated downloads during testing.
    
    Args:
        request: pytest request object containing configuration
        
    Returns:
        pd.DataFrame: The loaded dataset for testing
        
    Raises:
        pytest.fail: If the --csv option is not provided
    """
    logger.info("Initializing data fixture")
    
    run = wandb.init(job_type="data_tests", resume=True)
    logger.info("W&B run initialized for data tests")

    # Download input artifact. This will also note that this script is using this
    # particular version of the artifact
    csv_artifact = request.config.option.csv
    logger.info("Downloading artifact: %s", csv_artifact)
    
    data_path = run.use_artifact(csv_artifact).file()
    logger.info("Artifact downloaded to: %s", data_path)

    if data_path is None:
        logger.error("No CSV artifact specified")
        pytest.fail("You must provide the --csv option on the command line")

    logger.info("Loading data from artifact")
    df = pd.read_csv(data_path)
    logger.info("Data loaded successfully. Shape: %s", df.shape)

    return df


@pytest.fixture(scope='session')
def ref_data(request):
    """
    Fixture to download and load the reference dataset for comparison.
    
    This fixture initializes a W&B run, downloads the specified reference CSV artifact,
    loads it into a pandas DataFrame, and provides it to test functions for
    distribution comparison. The fixture has session scope to avoid repeated downloads.
    
    Args:
        request: pytest request object containing configuration
        
    Returns:
        pd.DataFrame: The loaded reference dataset
        
    Raises:
        pytest.fail: If the --ref option is not provided
    """
    logger.info("Initializing reference data fixture")
    
    run = wandb.init(job_type="data_tests", resume=True)
    logger.info("W&B run initialized for reference data")

    # Download input artifact. This will also note that this script is using this
    # particular version of the artifact
    ref_artifact = request.config.option.ref
    logger.info("Downloading reference artifact: %s", ref_artifact)
    
    data_path = run.use_artifact(ref_artifact).file()
    logger.info("Reference artifact downloaded to: %s", data_path)

    if data_path is None:
        logger.error("No reference artifact specified")
        pytest.fail("You must provide the --ref option on the command line")

    logger.info("Loading reference data from artifact")
    df = pd.read_csv(data_path)
    logger.info("Reference data loaded successfully. Shape: %s", df.shape)

    return df


@pytest.fixture(scope='session')
def kl_threshold(request):
    """
    Fixture to provide the KL divergence threshold parameter.
    
    This fixture extracts the KL divergence threshold from command line arguments
    and provides it to test functions that need to compare distributions.
    
    Args:
        request: pytest request object containing configuration
        
    Returns:
        float: The KL divergence threshold value
        
    Raises:
        pytest.fail: If the --kl_threshold option is not provided
    """
    logger.info("Extracting KL threshold parameter")
    
    kl_threshold = request.config.option.kl_threshold
    logger.info("KL threshold from command line: %s", kl_threshold)

    if kl_threshold is None:
        logger.error("No KL threshold specified")
        pytest.fail("You must provide a threshold for the KL test")

    threshold_value = float(kl_threshold)
    logger.info("KL threshold converted to float: %s", threshold_value)
    
    return threshold_value


@pytest.fixture(scope='session')
def min_price(request):
    """
    Fixture to provide the minimum price threshold parameter.
    
    This fixture extracts the minimum price threshold from command line arguments
    and provides it to test functions that need to validate price ranges.
    
    Args:
        request: pytest request object containing configuration
        
    Returns:
        float: The minimum price threshold value
        
    Raises:
        pytest.fail: If the --min_price option is not provided
    """
    logger.info("Extracting minimum price parameter")
    
    min_price = request.config.option.min_price
    logger.info("Min price from command line: %s", min_price)

    if min_price is None:
        logger.error("No minimum price specified")
        pytest.fail("You must provide min_price")

    price_value = float(min_price)
    logger.info("Min price converted to float: %s", price_value)
    
    return price_value


@pytest.fixture(scope='session')
def max_price(request):
    """
    Fixture to provide the maximum price threshold parameter.
    
    This fixture extracts the maximum price threshold from command line arguments
    and provides it to test functions that need to validate price ranges.
    
    Args:
        request: pytest request object containing configuration
        
    Returns:
        float: The maximum price threshold value
        
    Raises:
        pytest.fail: If the --max_price option is not provided
    """
    logger.info("Extracting maximum price parameter")
    
    max_price = request.config.option.max_price
    logger.info("Max price from command line: %s", max_price)

    if max_price is None:
        logger.error("No maximum price specified")
        pytest.fail("You must provide max_price")

    price_value = float(max_price)
    logger.info("Max price converted to float: %s", price_value)
    
    return price_value
