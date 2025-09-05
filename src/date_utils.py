"""
Date Utilities for Dutch Statistical Data

This module provides utilities for converting Dutch date formats commonly found
in statistical data, particularly when dates are stored as separate year and month columns
with Dutch month names.
"""

import pandas as pd
from datetime import datetime, date
from typing import Union, Optional, Dict, List
import calendar

# Dutch month names mapping
DUTCH_MONTHS = {
    'januari': 1, 'jan': 1,
    'februari': 2, 'feb': 2,
    'maart': 3, 'mrt': 3,
    'april': 4, 'apr': 4,
    'mei': 5,
    'juni': 6, 'jun': 6,
    'juli': 7, 'jul': 7,
    'augustus': 8, 'aug': 8,
    'september': 9, 'sep': 9,
    'oktober': 10, 'okt': 10,
    'november': 11, 'nov': 11,
    'december': 12, 'dec': 12
}

# Reverse mapping for month number to Dutch name
DUTCH_MONTH_NAMES = {
    1: 'Januari', 2: 'Februari', 3: 'Maart', 4: 'April',
    5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Augustus',
    9: 'September', 10: 'Oktober', 11: 'November', 12: 'December'
}

# Quarter mapping
DUTCH_QUARTERS = {
    'Q1': [1, 2, 3], 'Q2': [4, 5, 6], 'Q3': [7, 8, 9], 'Q4': [10, 11, 12],
    'Kwartaal 1': [1, 2, 3], 'Kwartaal 2': [4, 5, 6], 
    'Kwartaal 3': [7, 8, 9], 'Kwartaal 4': [10, 11, 12],
    '1e kwartaal': [1, 2, 3], '2e kwartaal': [4, 5, 6],
    '3e kwartaal': [7, 8, 9], '4e kwartaal': [10, 11, 12]
}


def dutch_month_to_number(month_name: str) -> int:
    """
    Convert Dutch month name to month number.
    
    Args:
        month_name: Dutch month name (e.g., 'Januari', 'februari', 'Jan')
    
    Returns:
        Month number (1-12)
    
    Raises:
        ValueError: If month name is not recognized
    """
    if pd.isna(month_name) or not isinstance(month_name, str):
        raise ValueError(f"Invalid month name: {month_name}")
    
    month_clean = month_name.lower().strip()
    
    if month_clean in DUTCH_MONTHS:
        return DUTCH_MONTHS[month_clean]
    
    raise ValueError(f"Unknown Dutch month name: {month_name}")


def create_date_from_columns(df: pd.DataFrame, 
                           year_col: str = 'jaar', 
                           month_col: str = 'maand',
                           day: int = 1) -> pd.Series:
    """
    Create a datetime series from year and Dutch month columns.
    
    Args:
        df: DataFrame containing the date columns
        year_col: Name of the year column (default: 'jaar')
        month_col: Name of the month column (default: 'maand')
        day: Day of the month to use (default: 1 for first day of month)
    
    Returns:
        pandas Series with datetime values
    
    Example:
        >>> df = pd.DataFrame({
        ...     'jaar': [2023, 2023, 2023],
        ...     'maand': ['Januari', 'Februari', 'Maart']
        ... })
        >>> dates = create_date_from_columns(df)
        >>> print(dates)
        0   2023-01-01
        1   2023-02-01
        2   2023-03-01
    """
    if year_col not in df.columns:
        raise ValueError(f"Year column '{year_col}' not found in DataFrame")
    if month_col not in df.columns:
        raise ValueError(f"Month column '{month_col}' not found in DataFrame")
    
    # Convert Dutch months to numbers
    month_numbers = df[month_col].apply(dutch_month_to_number)
    
    # Create datetime series
    dates = pd.to_datetime(df[year_col].astype(str) + '-' + 
                          month_numbers.astype(str) + '-' + 
                          str(day))
    
    return dates


def add_date_column(df: pd.DataFrame, 
                   year_col: str = 'jaar', 
                   month_col: str = 'maand',
                   date_col_name: str = 'datum',
                   day: int = 1) -> pd.DataFrame:
    """
    Add a datetime column to DataFrame based on year and Dutch month columns.
    
    Args:
        df: DataFrame to modify
        year_col: Name of the year column
        month_col: Name of the month column
        date_col_name: Name for the new date column
        day: Day of the month to use
    
    Returns:
        DataFrame with added date column
    """
    df_copy = df.copy()
    df_copy[date_col_name] = create_date_from_columns(df_copy, year_col, month_col, day)
    return df_copy


def extract_year_month_from_date(df: pd.DataFrame, 
                                date_col: str,
                                year_col: str = 'jaar',
                                month_col: str = 'maand',
                                dutch_months: bool = True) -> pd.DataFrame:
    """
    Extract year and month columns from a datetime column.
    
    Args:
        df: DataFrame containing the date column
        date_col: Name of the datetime column
        year_col: Name for the new year column
        month_col: Name for the new month column
        dutch_months: If True, use Dutch month names; if False, use numbers
    
    Returns:
        DataFrame with added year and month columns
    """
    df_copy = df.copy()
    
    # Ensure datetime column
    if not pd.api.types.is_datetime64_any_dtype(df_copy[date_col]):
        df_copy[date_col] = pd.to_datetime(df_copy[date_col])
    
    # Extract year
    df_copy[year_col] = df_copy[date_col].dt.year
    
    # Extract month
    if dutch_months:
        df_copy[month_col] = df_copy[date_col].dt.month.map(DUTCH_MONTH_NAMES)
    else:
        df_copy[month_col] = df_copy[date_col].dt.month
    
    return df_copy


def create_period_column(df: pd.DataFrame,
                        year_col: str = 'jaar',
                        month_col: str = 'maand',
                        period_type: str = 'month') -> pd.Series:
    """
    Create a period string column for easy grouping and analysis.
    
    Args:
        df: DataFrame containing date columns
        year_col: Name of the year column
        month_col: Name of the month column
        period_type: Type of period ('month', 'quarter', 'year')
    
    Returns:
        pandas Series with period strings
    
    Example:
        >>> df = pd.DataFrame({
        ...     'jaar': [2023, 2023, 2023],
        ...     'maand': ['Januari', 'Februari', 'Maart']
        ... })
        >>> periods = create_period_column(df, period_type='month')
        >>> print(periods)
        0    2023-01
        1    2023-02
        2    2023-03
    """
    if period_type == 'year':
        return df[year_col].astype(str)
    
    elif period_type == 'month':
        month_numbers = df[month_col].apply(dutch_month_to_number)
        return df[year_col].astype(str) + '-' + month_numbers.astype(str).str.zfill(2)
    
    elif period_type == 'quarter':
        month_numbers = df[month_col].apply(dutch_month_to_number)
        quarters = ((month_numbers - 1) // 3 + 1)
        return df[year_col].astype(str) + '-Q' + quarters.astype(str)
    
    else:
        raise ValueError(f"Unknown period_type: {period_type}. Use 'month', 'quarter', or 'year'")


def filter_by_period(df: pd.DataFrame,
                    year_col: str = 'jaar',
                    month_col: str = 'maand',
                    start_year: Optional[int] = None,
                    end_year: Optional[int] = None,
                    months: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Filter DataFrame by year and/or month criteria.
    
    Args:
        df: DataFrame to filter
        year_col: Name of the year column
        month_col: Name of the month column
        start_year: Minimum year (inclusive)
        end_year: Maximum year (inclusive)
        months: List of Dutch month names to include
    
    Returns:
        Filtered DataFrame
    
    Example:
        >>> filtered = filter_by_period(df, start_year=2020, 
        ...                           months=['Januari', 'Februari', 'Maart'])
    """
    df_filtered = df.copy()
    
    # Filter by year range
    if start_year is not None:
        df_filtered = df_filtered[df_filtered[year_col] >= start_year]
    if end_year is not None:
        df_filtered = df_filtered[df_filtered[year_col] <= end_year]
    
    # Filter by months
    if months is not None:
        df_filtered = df_filtered[df_filtered[month_col].isin(months)]
    
    return df_filtered


def get_quarter_from_month(month_name: str) -> str:
    """
    Get quarter string from Dutch month name.
    
    Args:
        month_name: Dutch month name
    
    Returns:
        Quarter string (Q1, Q2, Q3, Q4)
    """
    month_num = dutch_month_to_number(month_name)
    quarter = ((month_num - 1) // 3 + 1)
    return f"Q{quarter}"


def format_period_for_display(df: pd.DataFrame,
                             year_col: str = 'jaar',
                             month_col: str = 'maand',
                             format_type: str = 'full') -> pd.Series:
    """
    Create human-readable period strings for display.
    
    Args:
        df: DataFrame containing date columns
        year_col: Name of the year column
        month_col: Name of the month column
        format_type: 'full' (e.g., 'Januari 2023'), 'short' (e.g., 'Jan 2023'), 
                    'compact' (e.g., '2023-01')
    
    Returns:
        pandas Series with formatted period strings
    """
    if format_type == 'full':
        return df[month_col] + ' ' + df[year_col].astype(str)
    
    elif format_type == 'short':
        # Convert to short month names
        short_months = df[month_col].apply(lambda x: x[:3] if isinstance(x, str) else x)
        return short_months + ' ' + df[year_col].astype(str)
    
    elif format_type == 'compact':
        return create_period_column(df, year_col, month_col, 'month')
    
    else:
        raise ValueError(f"Unknown format_type: {format_type}. Use 'full', 'short', or 'compact'")


# Convenience function for common use case
def standardize_date_columns(df: pd.DataFrame, 
                           year_col: str = 'jaar',
                           month_col: str = 'maand') -> pd.DataFrame:
    """
    Add standardized date columns to a DataFrame with Dutch date format.
    
    This function adds:
    - 'datum': datetime column
    - 'periode': period string (YYYY-MM)
    - 'kwartaal': quarter string (YYYY-QX)
    - 'periode_display': human-readable period
    
    Args:
        df: DataFrame with Dutch year/month columns
        year_col: Name of the year column
        month_col: Name of the month column
    
    Returns:
        DataFrame with added standardized date columns
    """
    df_result = df.copy()
    
    # Add datetime column
    df_result = add_date_column(df_result, year_col, month_col, 'datum')
    
    # Add period columns
    df_result['periode'] = create_period_column(df_result, year_col, month_col, 'month')
    df_result['kwartaal'] = create_period_column(df_result, year_col, month_col, 'quarter')
    df_result['periode_display'] = format_period_for_display(df_result, year_col, month_col, 'full')
    
    return df_result


if __name__ == "__main__":
    # Example usage and testing
    print("Testing Dutch Date Utilities")
    print("=" * 40)
    
    # Create sample data
    sample_data = pd.DataFrame({
        'jaar': [2023, 2023, 2023, 2024, 2024],
        'maand': ['Januari', 'Februari', 'Maart', 'April', 'Mei'],
        'waarde': [100, 110, 120, 130, 140]
    })
    
    print("Original data:")
    print(sample_data)
    print()
    
    # Test standardization
    standardized = standardize_date_columns(sample_data)
    print("Standardized data:")
    print(standardized[['jaar', 'maand', 'datum', 'periode', 'kwartaal', 'periode_display', 'waarde']])
    print()
    
    # Test filtering
    filtered = filter_by_period(sample_data, start_year=2024, months=['April', 'Mei'])
    print("Filtered data (2024, April-May):")
    print(filtered)
