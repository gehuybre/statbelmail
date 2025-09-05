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
- **matplotlib**: Additional plotting capabilities
- **seaborn**: Statistical data visualization
- **kaleido**: Static image export for Plotly

## Usage

### Quick Start

1. Place your Excel files in the `data/` directory
2. Run the analysis script:
   ```bash
   uv run python analyze_data.py
   ```
3. Open the generated report at `reports/analysis_report.html`

### Using the Analysis Classes

```python
from src.excel_analyzer import ExcelAnalyzer, load_all_excel_files
from src.html_report import HTMLReportGenerator

# Analyze a single Excel file
analyzer = ExcelAnalyzer('data/your_file.xlsx')
analyzer.load_data()

# Get information about the sheets
info = analyzer.get_sheet_info()
print(info)

# Create a chart
chart = analyzer.create_summary_chart('Sheet1', 'column_name')

# Generate HTML report
report = HTMLReportGenerator("My Analysis Report")
report.add_section("Analysis", "Description", [chart])
report.generate_html(Path("reports/my_report.html"))
```

### Jupyter Notebooks

Start Jupyter for interactive analysis:

```bash
uv run jupyter lab
```

## Features

- **Multi-file Excel Analysis**: Automatically load and analyze multiple Excel files
- **Interactive Visualizations**: Generate Plotly charts for data exploration
- **HTML Reports**: Create professional-looking HTML reports with embedded charts
- **Data Comparison**: Compare data across multiple Excel files
- **Flexible Architecture**: Easily extensible for custom analysis needs

## Excel File Support

The analyzer supports:
- Multiple sheets per file
- Various data types (numeric, categorical, dates)
- Automatic chart type selection based on data type
- Missing data handling

## Example Workflow

1. **Data Loading**: The analyzer automatically detects and loads all Excel files
2. **Data Inspection**: Get summaries of sheet structure, columns, and data types
3. **Visualization**: Create appropriate charts based on data types
4. **Report Generation**: Combine analysis into a comprehensive HTML report
5. **Comparison**: Compare similar data across multiple files

## Customization

### Adding Custom Analysis

Extend the `ExcelAnalyzer` class:

```python
class CustomAnalyzer(ExcelAnalyzer):
    def custom_analysis(self):
        # Your custom analysis code
        pass
```

### Custom Report Sections

Add custom sections to reports:

```python
report = HTMLReportGenerator("Custom Report")
report.add_section(
    title="Custom Analysis",
    content="<p>Your custom HTML content</p>",
    charts=[your_plotly_figure]
)
```

## Output

- **HTML Reports**: Interactive reports with embedded Plotly charts
- **Charts**: Individual chart files can be exported (PNG, SVG, PDF)
- **Data Summaries**: Structured information about your datasets

## Troubleshooting

- Ensure Excel files are in the `data/` directory
- Check that Excel files are not password-protected
- For large files, increase available memory or process files individually
- If charts don't display, check your internet connection (CDN-based Plotly)

## Development

To extend this project:

1. Add new analysis functions to `src/excel_analyzer.py`
2. Create custom report templates in `src/html_report.py`
3. Write tests in the `tests/` directory
4. Use notebooks for prototyping new features
