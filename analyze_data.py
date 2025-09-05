#!/usr/bin/env python3
"""
Data Analysis Script for Excel Files

This script demonstrates how to analyze Excel files and generate HTML reports.
Usage: python analyze_data.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from excel_analyzer import ExcelAnalyzer, load_all_excel_files, create_comparison_chart
from html_report import HTMLReportGenerator, create_data_summary_table


def main():
    """Main analysis function."""
    # Configuration
    data_dir = Path("data")
    output_dir = Path("reports")
    output_dir.mkdir(exist_ok=True)
    
    print("Starting data analysis...")
    
    # Load all Excel files
    print(f"Loading Excel files from {data_dir}...")
    analyzers = load_all_excel_files(data_dir)
    
    if not analyzers:
        print(f"No Excel files found in {data_dir}")
        return
    
    print(f"Found {len(analyzers)} Excel files")
    
    # Create HTML report
    report = HTMLReportGenerator("Excel Data Analysis Report")
    
    # Add overview section
    overview_content = f"""
    <p>This report analyzes <strong>{len(analyzers)}</strong> Excel files found in the data directory.</p>
    <p>Files analyzed:</p>
    <ul>
    """
    for filename in analyzers.keys():
        overview_content += f"<li>{filename}</li>"
    overview_content += "</ul>"
    
    report.add_section("Overview", overview_content)
    
    # Add data summary for each file
    for filename, analyzer in analyzers.items():
        info = analyzer.get_sheet_info()
        summary_table = create_data_summary_table(info)
        
        content = f"""
        <p>File: <strong>{filename}</strong></p>
        <p>Number of sheets: <strong>{len(info)}</strong></p>
        {summary_table}
        """
        
        # Create sample charts for the first few sheets
        charts = []
        for sheet_name, sheet_info in list(info.items())[:3]:  # First 3 sheets
            df = analyzer.data[sheet_name]
            
            # Find a good column for visualization
            numeric_cols = [col for col, dtype in sheet_info['dtypes'].items() 
                          if dtype in ['int64', 'float64'] and not df[col].isnull().all()]
            
            if numeric_cols:
                col_to_plot = numeric_cols[0]
                try:
                    chart = analyzer.create_summary_chart(sheet_name, col_to_plot)
                    charts.append(chart)
                except Exception as e:
                    print(f"Could not create chart for {sheet_name}.{col_to_plot}: {e}")
        
        report.add_section(f"Analysis: {filename}", content, charts)
    
    # Generate comparison charts if multiple files have similar structure
    if len(analyzers) > 1:
        # Find common sheet names
        all_sheets = [set(analyzer.sheet_names) for analyzer in analyzers.values()]
        common_sheets = set.intersection(*all_sheets) if all_sheets else set()
        
        if common_sheets:
            comparison_content = f"""
            <p>Found <strong>{len(common_sheets)}</strong> common sheet(s) across all files:</p>
            <ul>
            """
            for sheet in common_sheets:
                comparison_content += f"<li>{sheet}</li>"
            comparison_content += "</ul>"
            
            # Create comparison charts for common sheets
            comparison_charts = []
            for sheet_name in list(common_sheets)[:2]:  # First 2 common sheets
                # Find common numeric columns
                all_columns = []
                for analyzer in analyzers.values():
                    if sheet_name in analyzer.data:
                        df = analyzer.data[sheet_name]
                        numeric_cols = [col for col in df.columns 
                                      if df[col].dtype in ['int64', 'float64']]
                        all_columns.append(set(numeric_cols))
                
                if all_columns:
                    common_columns = set.intersection(*all_columns)
                    if common_columns:
                        col_to_compare = list(common_columns)[0]
                        try:
                            chart = create_comparison_chart(analyzers, sheet_name, col_to_compare)
                            comparison_charts.append(chart)
                        except Exception as e:
                            print(f"Could not create comparison chart: {e}")
            
            report.add_section("File Comparisons", comparison_content, comparison_charts)
    
    # Generate and save report
    output_path = output_dir / "analysis_report.html"
    report.generate_html(output_path)
    
    print(f"Analysis complete! Report saved to: {output_path}")
    print(f"Open the report in your browser: file://{output_path.absolute()}")


if __name__ == "__main__":
    main()
