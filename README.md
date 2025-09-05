# Data Analysis with Excel Files

This project provides tools for analyzing Excel files and generating interactive HTML reports using Plotly visualizations.

## Project Structure

```
statbelmail/
├── data/                   # Excel files to analyze
├── src/                    # Source code modules
│   ├── __init__.py
│   ├── excel_analyzer.py   # Excel data analysis utilities
│   └── html_report.py      # HTML report generation
├── notebooks/              # Jupyter notebooks for interactive analysis
├── reports/                # Generated HTML reports
├── output/                 # Other output files
├── tests/                  # Test files
├── analyze_data.py         # Main analysis script
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

## Setup

This project uses `uv` for Python package management and virtual environment management.

### Prerequisites

- Python 3.11+
- uv package manager

### Installation

The virtual environment and dependencies are already set up. To activate the environment:

```bash
# Activate the virtual environment
source .venv/bin/activate

# Or use uv to run commands directly
uv run python analyze_data.py
```

## Installed Dependencies

- **pandas**: Data manipulation and analysis
- **openpyxl**: Excel file reading/writing
- **plotly**: Interactive visualizations
- **jinja2**: HTML template rendering
- **jupyter**: Interactive notebooks

## View the Analysis Notebook

You can view the interactive analysis notebook online using nbviewer:

[![View on NBViewer](https://img.shields.io/badge/View%20on-NBViewer-orange?logo=jupyter)](https://nbviewer.org/github/gehuybre/statbelmail/blob/main/notebooks/analyse.ipynb)

## Features

- Analysis of building permits data from StatBel
- Interactive visualizations with Plotly
- Analysis for all three Belgian regions (Vlaams Gewest, Waals Gewest, Brussels Hoofdstedelijk Gewest)
- 12-month moving averages for trend analysis
- Professional formatting following Flemish notation standards

## Data Sources

The analysis uses official StatBel data on building permits and renovations in Belgium.