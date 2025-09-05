"""
Template Manager

Centralized template management system using Jinja2 for all HTML reports.
"""

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import shutil
import os


class TemplateManager:
    """Manages HTML templates and CSS for all reports."""
    
    def __init__(self, project_root: Optional[Path] = None):
        """Initialize the template manager.
        
        Args:
            project_root: Root directory of the project
        """
        if project_root is None:
            project_root = Path(__file__).parent.parent
        
        self.project_root = project_root
        self.templates_dir = project_root / "templates"
        self.static_dir = project_root / "static"
        self.css_file = self.static_dir / "css" / "styles.css"
        
        # Initialize Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )
        
        # Add custom filters
        self.env.filters['number_format'] = self._number_format
    
    def _number_format(self, value):
        """Format numbers with thousands separator."""
        if isinstance(value, (int, float)):
            return f"{value:,.0f}"
        return value
    
    def copy_css_to_output(self, output_dir: Path) -> str:
        """Copy CSS file to output directory and return relative path.
        
        Args:
            output_dir: Directory where reports are generated
            
        Returns:
            Relative path to CSS file
        """
        output_css_dir = output_dir / "css"
        output_css_dir.mkdir(exist_ok=True)
        
        output_css_file = output_css_dir / "styles.css"
        shutil.copy2(self.css_file, output_css_file)
        
        return "css/styles.css"
    
    def render_building_permits_report(
        self, 
        region_name: str,
        stats: Dict[str, Any],
        quarterly_table: str,
        chart_html: str,
        yearly_quarters_chart_html: str,
        rolling_average_chart_html: str,
        output_dir: Path
    ) -> str:
        """Render building permits report.
        
        Args:
            region_name: Name of the region
            stats: Dictionary with statistics (total_permits, total_houses, etc.)
            quarterly_table: HTML table string
            chart_html: Plotly chart HTML for quarterly analysis
            yearly_quarters_chart_html: Plotly chart HTML for yearly quarters
            rolling_average_chart_html: Plotly chart HTML for rolling average
            output_dir: Output directory for the report
            
        Returns:
            Rendered HTML content
        """
        css_path = self.copy_css_to_output(output_dir)
        
        template = self.env.get_template('building_permits_report.html')
        
        context = {
            'title': f'Bouwvergunningen Rapport - {region_name}',
            'stats': stats,
            'quarterly_table': quarterly_table,
            'chart_html': chart_html,
            'yearly_quarters_chart_html': yearly_quarters_chart_html,
            'rolling_average_chart_html': rolling_average_chart_html,
            'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'css_path': css_path
        }
        
        return template.render(**context)
    
    def render_index_page(
        self,
        provinces: list,
        regions: list,
        output_dir: Path
    ) -> str:
        """Render index page with links to all reports.
        
        Args:
            provinces: List of provinces
            regions: List of regions
            output_dir: Output directory
            
        Returns:
            Rendered HTML content
        """
        css_path = self.copy_css_to_output(output_dir)
        
        # Format province and region data
        provinces_data = []
        for province in provinces:
            filename = f"{province.replace(' ', '_').replace('/', '_')}_rapport.html"
            display_name = province.replace('PROVINCIE ', '')
            provinces_data.append({
                'filename': filename,
                'display_name': display_name
            })
        
        regions_data = []
        for region in regions:
            filename = f"{region.replace(' ', '_').replace('/', '_')}_rapport.html"
            regions_data.append({
                'filename': filename,
                'display_name': region
            })
        
        template = self.env.get_template('index.html')
        
        context = {
            'title': 'Bouwvergunningen Rapporten - Overzicht',
            'provinces': provinces_data,
            'regions': regions_data,
            'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'css_path': css_path
        }
        
        return template.render(**context)
    
    def render_generic_report(
        self,
        title: str,
        sections: list,
        output_dir: Path
    ) -> str:
        """Render generic report using the base template system.
        
        Args:
            title: Report title
            sections: List of sections with content and charts
            output_dir: Output directory
            
        Returns:
            Rendered HTML content
        """
        css_path = self.copy_css_to_output(output_dir)
        
        template = self.env.get_template('generic_report.html')
        
        context = {
            'title': title,
            'sections': sections,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'css_path': css_path
        }
        
        return template.render(**context)
    
    def save_report(self, html_content: str, output_path: Path):
        """Save HTML report to file.
        
        Args:
            html_content: Rendered HTML content
            output_path: Path to save the file
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
