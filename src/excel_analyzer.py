"""
Excel Data Analysis Utilities

This module provides utilities for loading and analyzing Excel files.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from typing import Dict, List, Optional, Union


class ExcelAnalyzer:
    """Class for analyzing Excel files with multiple sheets."""
    
    def __init__(self, file_path: Union[str, Path]):
        """Initialize with Excel file path."""
        self.file_path = Path(file_path)
        self.data: Dict[str, pd.DataFrame] = {}
        self.sheet_names: List[str] = []
        
    def load_data(self, sheet_name: Optional[str] = None) -> None:
        """Load data from Excel file.
        
        Args:
            sheet_name: Specific sheet to load. If None, loads all sheets.
        """
        if sheet_name:
            self.data[sheet_name] = pd.read_excel(self.file_path, sheet_name=sheet_name)
        else:
            # Load all sheets
            excel_file = pd.ExcelFile(self.file_path)
            self.sheet_names = excel_file.sheet_names
            for sheet in self.sheet_names:
                self.data[sheet] = pd.read_excel(self.file_path, sheet_name=sheet)
    
    def get_sheet_info(self) -> Dict[str, Dict]:
        """Get information about each loaded sheet."""
        info = {}
        for sheet_name, df in self.data.items():
            info[sheet_name] = {
                'shape': df.shape,
                'columns': list(df.columns),
                'dtypes': df.dtypes.to_dict(),
                'null_counts': df.isnull().sum().to_dict()
            }
        return info
    
    def create_summary_chart(self, sheet_name: str, column: str) -> go.Figure:
        """Create a summary chart for a specific column.
        
        Args:
            sheet_name: Name of the sheet
            column: Column to analyze
            
        Returns:
            Plotly figure
        """
        if sheet_name not in self.data:
            raise ValueError(f"Sheet '{sheet_name}' not loaded")
        
        df = self.data[sheet_name]
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in sheet '{sheet_name}'")
        
        # Create appropriate chart based on data type
        if df[column].dtype in ['object', 'category']:
            # Categorical data - bar chart
            value_counts = df[column].value_counts()
            fig = px.bar(
                x=value_counts.index,
                y=value_counts.values,
                title=f"Distribution of {column} in {sheet_name}",
                labels={'x': column, 'y': 'Count'}
            )
        else:
            # Numerical data - histogram
            fig = px.histogram(
                df,
                x=column,
                title=f"Distribution of {column} in {sheet_name}",
                nbins=30
            )
        
        return fig


def load_all_excel_files(data_dir: Union[str, Path]) -> Dict[str, ExcelAnalyzer]:
    """Load all Excel files from a directory.
    
    Args:
        data_dir: Directory containing Excel files
        
    Returns:
        Dictionary mapping filename to ExcelAnalyzer instance
    """
    data_path = Path(data_dir)
    analyzers = {}
    
    for excel_file in data_path.glob("*.xlsx"):
        analyzer = ExcelAnalyzer(excel_file)
        analyzer.load_data()
        analyzers[excel_file.name] = analyzer
    
    return analyzers


def create_comparison_chart(analyzers: Dict[str, ExcelAnalyzer], 
                          sheet_name: str, 
                          column: str) -> go.Figure:
    """Create a comparison chart across multiple files.
    
    Args:
        analyzers: Dictionary of ExcelAnalyzer instances
        sheet_name: Sheet name to compare
        column: Column to compare
        
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    for filename, analyzer in analyzers.items():
        if sheet_name in analyzer.data and column in analyzer.data[sheet_name].columns:
            df = analyzer.data[sheet_name]
            if df[column].dtype in ['int64', 'float64']:
                # Add trace for numerical data
                fig.add_trace(go.Histogram(
                    x=df[column],
                    name=filename,
                    opacity=0.7
                ))
    
    fig.update_layout(
        title=f"Comparison of {column} across files",
        xaxis_title=column,
        yaxis_title="Count",
        barmode='overlay'
    )
    
    return fig
