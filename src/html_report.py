"""
HTML Report Generator

This module provides utilities for generating HTML reports with Plotly visualizations.
"""

import plotly.graph_objects as go
import plotly.io as pio
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import sys

# Add src to path for imports
sys.path.append(str(Path(__file__).parent))
from template_manager import TemplateManager


class HTMLReportGenerator:
    """Generate HTML reports with embedded Plotly charts."""
    
    def __init__(self, title: str = "Data Analysis Report"):
        """Initialize the report generator.
        
        Args:
            title: Title of the report
        """
        self.title = title
        self.sections: List[Dict] = []
        self.template_manager = TemplateManager()
        
    def add_section(self, title: str, content: str, charts: Optional[List[go.Figure]] = None):
        """Add a section to the report.
        
        Args:
            title: Section title
            content: HTML content or markdown text
            charts: List of Plotly figures to embed
        """
        section = {
            'title': title,
            'content': content,
            'charts': charts or []
        }
        self.sections.append(section)
    
    def generate_html(self, output_path: Optional[Path] = None) -> str:
        """Generate the HTML report.
        
        Args:
            output_path: Path to save the HTML file
            
        Returns:
            HTML content as string
        """
        # Convert charts to HTML
        for section in self.sections:
            chart_htmls = []
            for chart in section['charts']:
                chart_html = pio.to_html(
                    chart,
                    include_plotlyjs='cdn',
                    div_id=f"chart_{len(chart_htmls)}"
                )
                chart_htmls.append(chart_html)
            section['chart_htmls'] = chart_htmls
        
        # Determine output directory for CSS
        if output_path:
            output_dir = output_path.parent
        else:
            output_dir = Path.cwd()
        
        # Use template manager to render the report
        html_content = self.template_manager.render_generic_report(
            title=self.title,
            sections=self.sections,
            output_dir=output_dir
        )
        
        if output_path:
            self.template_manager.save_report(html_content, output_path)
        
        return html_content


def create_data_summary_table(data_info: Dict[str, Dict]) -> str:
    """Create an HTML table summarizing data information.
    
    Args:
        data_info: Dictionary with sheet information
        
    Returns:
        HTML table string
    """
    html = "<table><tr><th>Sheet Name</th><th>Rows</th><th>Columns</th><th>Column Names</th></tr>"
    
    for sheet_name, info in data_info.items():
        rows, cols = info['shape']
        column_names = ', '.join(info['columns'][:5])  # Show first 5 columns
        if len(info['columns']) > 5:
            column_names += f" ... (+{len(info['columns']) - 5} more)"
        
        html += f"<tr><td>{sheet_name}</td><td>{rows}</td><td>{cols}</td><td>{column_names}</td></tr>"
    
    html += "</table>"
    return html
