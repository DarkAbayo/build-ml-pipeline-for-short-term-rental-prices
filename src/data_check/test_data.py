#!/usr/bin/env python
"""
Data quality testing module for NYC Airbnb rental price prediction pipeline.

This module contains comprehensive data quality tests that validate the cleaned dataset
against expected standards and reference data. Tests include column validation,
geographic boundaries, neighborhood distributions, and price range validation.

Key test functions:
- test_column_names: Validates expected column structure
- test_neighborhood_names: Checks neighborhood group values
- test_proper_boundaries: Validates geographic coordinates
- test_similar_neigh_distrib: Compares distribution with reference data
- test_row_count: Ensures dataset size is reasonable
- test_price_range: Validates price values are within bounds

Author: Niedermeier Patrick
Date: 2025-07-07
"""
import pandas as pd
import numpy as np
import scipy.stats
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger(__name__)


def test_column_names(data):
    """
    Test that the dataset contains all expected columns in the correct order.
    
    This test validates the data schema by checking that all required columns
    are present and in the expected order. This is crucial for downstream
    processing steps that depend on specific column names and positions.
    
    Args:
        data (pd.DataFrame): The input DataFrame to validate
        
    Raises:
        AssertionError: If column names or order don't match expected schema
        
    Returns:
        None: Test passes silently if successful
    """
    logger.info("Testing column names and structure")
    
    expected_colums = [
        "id",
        "name",
        "host_id",
        "host_name",
        "neighbourhood_group",
        "neighbourhood",
        "latitude",
        "longitude",
        "room_type",
        "price",
        "minimum_nights",
        "number_of_reviews",
        "last_review",
        "reviews_per_month",
        "calculated_host_listings_count",
        "availability_365",
    ]

    these_columns = data.columns.values
    logger.info("Expected columns: %s", expected_colums)
    logger.info("Actual columns: %s", list(these_columns))

    # This also enforces the same order
    assert list(expected_colums) == list(these_columns)
    logger.info("Column structure validation passed")


def test_neighborhood_names(data):
    """
    Test that neighborhood group values match known NYC boroughs.
    
    This test validates that all neighborhood_group values are valid NYC boroughs.
    This ensures data quality and prevents downstream issues with geographic
    analysis and modeling.
    
    Args:
        data (pd.DataFrame): The input DataFrame to validate
        
    Raises:
        AssertionError: If neighborhood groups don't match expected values
        
    Returns:
        None: Test passes silently if successful
    """
    logger.info("Testing neighborhood group values")
    
    known_names = ["Bronx", "Brooklyn", "Manhattan", "Queens", "Staten Island"]
    neigh = set(data['neighbourhood_group'].unique())
    
    logger.info("Expected neighborhood groups: %s", known_names)
    logger.info("Actual neighborhood groups: %s", list(neigh))

    # Unordered check
    assert set(known_names) == set(neigh)
    logger.info("Neighborhood group validation passed")


def test_proper_boundaries(data: pd.DataFrame):
    """
    Test proper longitude and latitude boundaries for properties in and around NYC.
    
    This test validates that all geographic coordinates fall within reasonable
    boundaries for the NYC area. This prevents data quality issues from
    incorrect coordinates that could affect geographic analysis.
    
    Args:
        data (pd.DataFrame): The input DataFrame to validate
        
    Raises:
        AssertionError: If any coordinates fall outside expected boundaries
        
    Returns:
        None: Test passes silently if successful
    """
    logger.info("Testing geographic boundaries")
    
    # NYC area boundaries
    min_lon, max_lon = -74.25, -73.50
    min_lat, max_lat = 40.5, 41.2
    
    logger.info("Expected longitude range: [%s, %s]", min_lon, max_lon)
    logger.info("Expected latitude range: [%s, %s]", min_lat, max_lat)
    logger.info("Actual longitude range: [%s, %s]", data['longitude'].min(), data['longitude'].max())
    logger.info("Actual latitude range: [%s, %s]", data['latitude'].min(), data['latitude'].max())
    
    idx = data['longitude'].between(min_lon, max_lon) & data['latitude'].between(min_lat, max_lat)
    outliers_count = np.sum(~idx)
    
    logger.info("Properties within boundaries: %s", np.sum(idx))
    logger.info("Properties outside boundaries: %s", outliers_count)

    assert np.sum(~idx) == 0
    logger.info("Geographic boundary validation passed")


def test_similar_neigh_distrib(data: pd.DataFrame, ref_data: pd.DataFrame, kl_threshold: float):
    """
    Apply a threshold on the KL divergence to detect if the distribution of the new data is
    significantly different than that of the reference dataset.
    
    This test uses KL divergence to compare the distribution of neighborhood groups
    between the current dataset and a reference dataset. This helps detect data drift
    and ensures the new data is representative of the expected distribution.
    
    Args:
        data (pd.DataFrame): The current dataset to test
        ref_data (pd.DataFrame): The reference dataset for comparison
        kl_threshold (float): Maximum allowed KL divergence threshold
        
    Raises:
        AssertionError: If KL divergence exceeds the threshold
        
    Returns:
        None: Test passes silently if successful
    """
    logger.info("Testing neighborhood distribution similarity")
    
    dist1 = data['neighbourhood_group'].value_counts().sort_index()
    dist2 = ref_data['neighbourhood_group'].value_counts().sort_index()
    
    logger.info("Current dataset neighborhood distribution: %s", dist1.to_dict())
    logger.info("Reference dataset neighborhood distribution: %s", dist2.to_dict())
    
    kl_divergence = scipy.stats.entropy(dist1, dist2, base=2)
    logger.info("KL divergence: %s (threshold: %s)", kl_divergence, kl_threshold)

    assert kl_divergence < kl_threshold
    logger.info("Distribution similarity validation passed")


def test_row_count(data: pd.DataFrame):
    """
    Test if the number of rows in the DataFrame is within an expected range.
    
    This test ensures the dataset size is reasonable - not too small to be
    representative, and not too large to indicate potential data issues.
    
    Args:
        data (pd.DataFrame): The input DataFrame to check.
        
    Raises:
        AssertionError: If row count is outside expected range
        
    Returns:
        None: Test passes silently if successful
    """
    logger.info("Testing dataset row count")
    
    row_count = data.shape[0]
    min_expected = 15000
    max_expected = 1000000
    
    logger.info("Dataset row count: %s", row_count)
    logger.info("Expected range: [%s, %s]", min_expected, max_expected)
    
    # Assert that the row count is between 15,000 and 1,000,000
    assert min_expected < row_count < max_expected
    logger.info("Row count validation passed")


def test_price_range(data: pd.DataFrame, min_price: float, max_price: float):
    """
    Test if all prices in the DataFrame are within a specified minimum and maximum range.
    
    This test validates that all price values fall within the expected range,
    ensuring data quality and preventing outliers from affecting downstream analysis.
    
    Args:
        data (pd.DataFrame): The input DataFrame to check.
        min_price (float): The minimum allowed price.
        max_price (float): The maximum allowed price.
        
    Raises:
        AssertionError: If any price values fall outside the specified range
        
    Returns:
        None: Test passes silently if successful
    """
    logger.info("Testing price range validation")
    
    logger.info("Expected price range: [%s, %s]", min_price, max_price)
    logger.info("Actual price range: [%s, %s]", data['price'].min(), data['price'].max())
    
    valid_prices = data['price'].between(min_price, max_price)
    invalid_count = (~valid_prices).sum()
    
    logger.info("Valid prices: %s", valid_prices.sum())
    logger.info("Invalid prices: %s", invalid_count)
    
    # Assert that all values in the 'price' column are within the specified range
    assert data['price'].between(min_price, max_price).all()
    logger.info("Price range validation passed")
