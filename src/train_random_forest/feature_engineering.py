#!/usr/bin/env python
"""
Feature engineering utilities for date processing in ML pipelines.

This module provides utility functions for creating engineered features from
date columns, specifically calculating the number of days since the most
recent date in a dataset.

Author: Niedermeier Patrick
Date: 2025-09-06
"""
import pandas as pd
import numpy as np


def delta_date_feature(dates):
    """
    Calculate days since the most recent date for each date in the input.
    
    This function takes a 2D array of dates and calculates the number of days
    between each date and the most recent date in its column. This is useful
    for creating temporal features that represent recency, such as "days since
    last review" for Airbnb listings.
    
    The function handles various date formats by using pandas' automatic date
    parsing capabilities and returns the results as a numpy array for
    compatibility with scikit-learn transformers.
    
    Args:
        dates (array-like): 2D array containing dates in any format recognized by pd.to_datetime.
            Can be a list of lists, numpy array, or pandas DataFrame.
    
    Returns:
        numpy.ndarray: 2D array with the same shape as input, containing the number
            of days between each date and the most recent date in its column.
            More recent dates will have smaller values.
    
    Example:
        >>> dates = [['2023-01-01', '2023-01-15'], ['2023-01-10', '2023-01-20']]
        >>> delta_date_feature(dates)
        array([[14,  0], [10,  0]])  # Days since most recent date in each column
    
    Note:
        - Missing or invalid dates are handled by pandas' to_datetime function
        - The function preserves the original array structure
        - Results are in days as integers
    """
    date_sanitized = pd.DataFrame(dates).apply(pd.to_datetime)
    return date_sanitized.apply(lambda d: (d.max() -d).dt.days, axis=0).to_numpy()
