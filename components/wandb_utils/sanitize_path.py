#!/usr/bin/env python
"""
Path sanitization utility for file system operations.

This module provides utility functions for sanitizing and normalizing file paths
to ensure consistent and safe file system operations across different environments.

Author: Niedermeier Patrick
Date: 2025-09-06
"""
import os


def sanitize_path(s):
    """
    Sanitize and normalize a file path for safe file system operations.
    
    This function processes an input path by expanding environment variables,
    resolving the home directory, and converting it to an absolute path. This
    ensures consistent path handling across different operating systems and
    user environments.
    
    Processing Steps:
    1. Expand environment variables (e.g., $HOME, $USER)
    2. Expand home directory tilde (~) to actual home path
    3. Convert to absolute path for consistency
    
    Args:
        s (str): Input path to sanitize (can be relative or absolute)
        
    Returns:
        str: Sanitized absolute path
        
    Example:
        >>> sanitize_path("~/data/file.csv")
        '/home/user/data/file.csv'
        >>> sanitize_path("$HOME/project/data")
        '/home/user/project/data'
    """
    return os.path.abspath(os.path.expanduser(os.path.expandvars(s)))
