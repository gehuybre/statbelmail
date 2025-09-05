"""
Building Permits Report Generator

This module creates HTML reports for building permits data with quarterly analysis
per province and region, including interactive Plotly charts and summary tables.
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.io as pio
from pathlib import Path
import sys
from typing import Dict, List, Tuple
from datetime import datetime

# Add src to path for imports
sys.path.append(str(Path(__file__).parent))
from date_utils import standardize_date_columns, create_period_column
from template_manager import TemplateManager


class BuildingPermitsReportGenerator:
    """Generate HTML reports for building permits data."""
    
    def __init__(self, csv_file_path: str):
        """Initialize with CSV file path."""
        self.csv_path = Path(csv_file_path)
        self.data = None
        self.standardized_data = None
        self.template_manager = TemplateManager()
        
    def load_and_prepare_data(self):
        """Load and prepare the data with date standardization."""
        print(f"Loading data from {self.csv_path.name}...")
        
        # Load data
        self.data = pd.read_csv(self.csv_path)
        
        # Standardize date columns
        self.standardized_data = standardize_date_columns(self.data)
        
        # Calculate derived metrics
        self.standardized_data['aantal_huizen'] = self.standardized_data['aantal gebouwen met één woning']
        self.standardized_data['aantal_flats'] = (
            self.standardized_data['aantal woningen'] - 
            self.standardized_data['aantal gebouwen met één woning']
        )
        self.standardized_data['alle_woningen'] = self.standardized_data['aantal woningen']
        
        print(f"Data loaded: {self.standardized_data.shape[0]} rows, {self.standardized_data.shape[1]} columns")
        print(f"Date range: {self.standardized_data['jaar'].min()} - {self.standardized_data['jaar'].max()}")
        
    def get_provinces(self) -> List[str]:
        """Get list of provinces (regions starting with 'PROVINCIE')."""
        if self.standardized_data is None:
            self.load_and_prepare_data()
        
        provinces = self.standardized_data[
            self.standardized_data['regio'].str.startswith('PROVINCIE')
        ]['regio'].unique()
        
        return sorted(provinces)
    
    def get_regions(self) -> List[str]:
        """Get list of main regions (gewesten)."""
        regions = [
            'VLAAMS GEWEST',
            'WAALS GEWEST', 
            'BRUSSELS HOOFDSTEDELIJK GEWEST'
        ]
        return regions
    
    def create_quarterly_chart(self, region_data: pd.DataFrame, region_name: str) -> go.Figure:
        """Create a quarterly line chart for the three housing metrics."""
        
        # Filter data from Q1 2015 onwards
        region_data_filtered = region_data[region_data['jaar'] >= 2015].copy()
        
        # Group by quarter and sum the metrics
        quarterly_data = region_data_filtered.groupby('kwartaal').agg({
            'aantal_huizen': 'sum',
            'aantal_flats': 'sum', 
            'alle_woningen': 'sum'
        }).reset_index()
        
        # Sort by quarter (format: YYYY-QX)
        quarterly_data = quarterly_data.sort_values('kwartaal')
        
        # Create line chart
        fig = go.Figure()
        
        # Add traces for each metric with new color scheme
        fig.add_trace(go.Scatter(
            x=quarterly_data['kwartaal'].tolist(),
            y=quarterly_data['aantal_huizen'].tolist(),
            mode='lines+markers',
            name='Aantal Huizen',
            line=dict(color='#19b6c8', width=3),  # Teal accent
            marker=dict(size=8, color='#19b6c8')
        ))
        
        fig.add_trace(go.Scatter(
            x=quarterly_data['kwartaal'].tolist(),
            y=quarterly_data['aantal_flats'].tolist(),
            mode='lines+markers',
            name='Aantal Flats',
            line=dict(color='#2f2f2f', width=3),  # Primary dark
            marker=dict(size=8, color='#2f2f2f')
        ))
        
        fig.add_trace(go.Scatter(
            x=quarterly_data['kwartaal'].tolist(),
            y=quarterly_data['alle_woningen'].tolist(),
            mode='lines+markers',
            name='Alle Woningen',
            line=dict(color='#15a0ab', width=3),  # Darker teal
            marker=dict(size=8, color='#15a0ab')
        ))
        
        # Update layout with new styling
        fig.update_layout(
            title={
                'text': f'Bouwvergunningen per Kwartaal - {region_name}',
                'font': {'size': 20, 'color': '#2f2f2f', 'family': 'Montserrat'},
                'x': 0.5
            },
            xaxis_title='Kwartaal',
            yaxis_title='Aantal Vergunningen',
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color='#2f2f2f')
            ),
            height=500,
            plot_bgcolor='#f7f7f7',
            paper_bgcolor='white',
            font=dict(color='#2f2f2f', family='Montserrat')
        )
        
        # Update axes styling
        fig.update_xaxes(
            tickangle=45,
            gridcolor='#e2e8f0',
            linecolor='#2f2f2f',
            title_font=dict(color='#2f2f2f', size=14)
        )
        fig.update_yaxes(
            gridcolor='#e2e8f0',
            linecolor='#2f2f2f',
            title_font=dict(color='#2f2f2f', size=14)
        )
        
        return fig
    
    def create_yearly_quarters_chart(self, region_data: pd.DataFrame, region_name: str) -> go.Figure:
        """Create a yearly chart with separate lines for each quarter."""
        
        # Filter data from Q1 2015 onwards
        region_data_filtered = region_data[region_data['jaar'] >= 2015].copy()
        
        # Group by year and quarter, sum the metrics
        yearly_quarterly = region_data_filtered.groupby(['jaar', 'kwartaal']).agg({
            'alle_woningen': 'sum'
        }).reset_index()
        
        # Extract quarter number from kwartaal (format: YYYY-QX)
        yearly_quarterly['quarter_num'] = yearly_quarterly['kwartaal'].str.extract(r'Q(\d)')[0]
        
        # Create line chart
        fig = go.Figure()
        
        # Define colors for each quarter using the new color scheme
        quarter_colors = {
            '1': '#19b6c8',  # Teal accent for Q1
            '2': '#2f2f2f',  # Primary dark for Q2
            '3': '#15a0ab',  # Darker teal for Q3
            '4': '#666666'   # Medium gray for Q4
        }
        
        # Add a line for each quarter
        for quarter in ['1', '2', '3', '4']:
            quarter_data = yearly_quarterly[yearly_quarterly['quarter_num'] == quarter].copy()
            quarter_data = quarter_data.sort_values('jaar')
            
            if not quarter_data.empty:
                fig.add_trace(go.Scatter(
                    x=quarter_data['jaar'].tolist(),
                    y=quarter_data['alle_woningen'].tolist(),
                    mode='lines+markers',
                    name=f'Q{quarter}',
                    line=dict(color=quarter_colors[quarter], width=3),
                    marker=dict(size=8, color=quarter_colors[quarter])
                ))
        
        # Update layout
        fig.update_layout(
            title={
                'text': f'Woningen per Jaar en Kwartaal - {region_name}',
                'font': {'size': 20, 'color': '#2f2f2f', 'family': 'Montserrat'},
                'x': 0.5
            },
            xaxis_title='Jaar',
            yaxis_title='Aantal Woningen',
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color='#2f2f2f')
            ),
            height=500,
            plot_bgcolor='#f7f7f7',
            paper_bgcolor='white',
            font=dict(color='#2f2f2f', family='Montserrat')
        )
        
        # Update axes styling
        fig.update_xaxes(
            tickangle=0,
            gridcolor='#e2e8f0',
            linecolor='#2f2f2f',
            title_font=dict(color='#2f2f2f', size=14),
            dtick=1  # Show every year
        )
        fig.update_yaxes(
            gridcolor='#e2e8f0',
            linecolor='#2f2f2f',
            title_font=dict(color='#2f2f2f', size=14)
        )
        
        return fig
    
    def create_rolling_average_chart(self, region_data: pd.DataFrame, region_name: str) -> go.Figure:
        """Create a chart showing 12-month rolling average."""
        
        # Filter data from Q1 2015 onwards
        region_data_filtered = region_data[region_data['jaar'] >= 2015].copy()
        
        # Group by year and month, sum the metrics
        monthly_data = region_data_filtered.groupby(['jaar', 'maand']).agg({
            'alle_woningen': 'sum',
            'aantal_huizen': 'sum',
            'aantal_flats': 'sum'
        }).reset_index()
        
        # Create a proper date column for sorting
        month_mapping = {
            'Januari': 1, 'Februari': 2, 'Maart': 3, 'April': 4,
            'Mei': 5, 'Juni': 6, 'Juli': 7, 'Augustus': 8,
            'September': 9, 'Oktober': 10, 'November': 11, 'December': 12
        }
        
        monthly_data['maand_nummer'] = monthly_data['maand'].map(month_mapping)
        
        # Filter out any rows where month mapping failed
        monthly_data = monthly_data.dropna(subset=['maand_nummer'])
        
        # Create date column safely
        monthly_data['datum'] = pd.to_datetime(
            monthly_data['jaar'].astype(str) + '-' + 
            monthly_data['maand_nummer'].astype(int).astype(str).str.zfill(2) + '-01'
        )
        monthly_data = monthly_data.sort_values('datum')
        
        # Calculate 12-month rolling averages
        monthly_data['rolling_alle_woningen'] = monthly_data['alle_woningen'].rolling(window=12, min_periods=1).mean()
        monthly_data['rolling_aantal_huizen'] = monthly_data['aantal_huizen'].rolling(window=12, min_periods=1).mean()
        monthly_data['rolling_aantal_flats'] = monthly_data['aantal_flats'].rolling(window=12, min_periods=1).mean()
        
        # Create the chart
        fig = go.Figure()
        
        # Add traces for rolling averages
        fig.add_trace(go.Scatter(
            x=monthly_data['datum'].tolist(),
            y=monthly_data['rolling_aantal_huizen'].tolist(),
            mode='lines',
            name='Huizen (12m gemiddelde)',
            line=dict(color='#19b6c8', width=3),
            hovertemplate='<b>%{fullData.name}</b><br>' +
                         'Datum: %{x|%Y-%m}<br>' +
                         'Gemiddelde: %{y:.0f}<br>' +
                         '<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=monthly_data['datum'].tolist(),
            y=monthly_data['rolling_aantal_flats'].tolist(),
            mode='lines',
            name='Flats (12m gemiddelde)',
            line=dict(color='#2f2f2f', width=3),
            hovertemplate='<b>%{fullData.name}</b><br>' +
                         'Datum: %{x|%Y-%m}<br>' +
                         'Gemiddelde: %{y:.0f}<br>' +
                         '<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=monthly_data['datum'].tolist(),
            y=monthly_data['rolling_alle_woningen'].tolist(),
            mode='lines',
            name='Alle Woningen (12m gemiddelde)',
            line=dict(color='#15a0ab', width=4),  # Slightly thicker for total
            hovertemplate='<b>%{fullData.name}</b><br>' +
                         'Datum: %{x|%Y-%m}<br>' +
                         'Gemiddelde: %{y:.0f}<br>' +
                         '<extra></extra>'
        ))
        
        # Update layout
        fig.update_layout(
            title={
                'text': f'12-Maands Lopend Gemiddelde - {region_name}',
                'font': {'size': 20, 'color': '#2f2f2f', 'family': 'Montserrat'},
                'x': 0.5
            },
            xaxis_title='Datum',
            yaxis_title='Gemiddeld Aantal Woningen (12 maanden)',
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color='#2f2f2f')
            ),
            height=500,
            plot_bgcolor='#f7f7f7',
            paper_bgcolor='white',
            font=dict(color='#2f2f2f', family='Montserrat')
        )
        
        # Update axes styling
        fig.update_xaxes(
            gridcolor='#e2e8f0',
            linecolor='#2f2f2f',
            title_font=dict(color='#2f2f2f', size=14),
            tickformat='%Y-%m'
        )
        fig.update_yaxes(
            gridcolor='#e2e8f0',
            linecolor='#2f2f2f',
            title_font=dict(color='#2f2f2f', size=14)
        )
        
        # Add annotation explaining the rolling average
        fig.add_annotation(
            x=0.02, y=0.98,
            xref='paper', yref='paper',
            text='12-maands lopend gemiddelde gladde seizoensschommelingen uit',
            showarrow=False,
            font=dict(size=10, color='#666666'),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#e2e8f0',
            borderwidth=1
        )
        
        return fig
    
    def create_yearly_quarterly_table(self, region_data: pd.DataFrame) -> str:
        """Create HTML table showing yearly totals by quarter."""
        
        # Filter data from 2015 onwards
        region_data_filtered = region_data[region_data['jaar'] >= 2015].copy()
        
        # Group by year and quarter, sum all woningen
        yearly_quarterly = region_data_filtered.groupby(['jaar', 'kwartaal']).agg({
            'alle_woningen': 'sum'
        }).reset_index()
        
        # Extract quarter number from kwartaal (format: YYYY-QX)
        yearly_quarterly['quarter_num'] = yearly_quarterly['kwartaal'].str.extract(r'Q(\d)')[0]
        
        # Pivot to create year vs quarter table
        pivot_table = yearly_quarterly.pivot(
            index='jaar', 
            columns='quarter_num', 
            values='alle_woningen'
        ).fillna(0)
        
        # Ensure all quarters are present
        for q in ['1', '2', '3', '4']:
            if q not in pivot_table.columns:
                pivot_table[q] = 0
        
        # Reorder columns
        pivot_table = pivot_table[['1', '2', '3', '4']]
        
        # Add yearly totals
        pivot_table['Totaal'] = pivot_table.sum(axis=1)
        
        # Create HTML table with new styling
        html_table = '<table class="quarterly-table">\n'
        html_table += '<thead>\n<tr>\n<th>Jaar</th><th>Q1</th><th>Q2</th><th>Q3</th><th>Q4</th><th>Totaal</th>\n</tr>\n</thead>\n'
        html_table += '<tbody>\n'
        
        for year in sorted(pivot_table.index):
            row = pivot_table.loc[year]
            html_table += f'<tr>\n<td><strong>{year}</strong></td>\n'
            
            for quarter in ['1', '2', '3', '4']:
                value = int(row[quarter]) if not pd.isna(row[quarter]) else 0
                html_table += f'<td>{value:,}</td>\n'
            
            total_value = int(row['Totaal']) if not pd.isna(row['Totaal']) else 0
            html_table += f'<td><strong>{total_value:,}</strong></td>\n'
            html_table += '</tr>\n'
        
        html_table += '</tbody>\n</table>\n'
        
        return html_table
    
    def create_region_report(self, region_name: str, output_dir: Path):
        """Create HTML report for a specific region."""
        
        if self.standardized_data is None:
            self.load_and_prepare_data()
        
        # Filter data for the region
        region_data = self.standardized_data[
            self.standardized_data['regio'] == region_name
        ].copy()
        
        if region_data.empty:
            print(f"No data found for region: {region_name}")
            return
        
        # Create chart
        chart = self.create_quarterly_chart(region_data, region_name)
        
        # Create yearly quarters chart
        yearly_quarters_chart = self.create_yearly_quarters_chart(region_data, region_name)
        
        # Create rolling average chart
        rolling_average_chart = self.create_rolling_average_chart(region_data, region_name)
        
        # Convert charts to HTML (only div content, no full HTML document)
        chart_html = pio.to_html(
            chart,
            include_plotlyjs=False,
            div_id="quarterly-chart",
            full_html=False
        )
        
        yearly_quarters_chart_html = pio.to_html(
            yearly_quarters_chart,
            include_plotlyjs=False,
            div_id="yearly-quarters-chart",
            full_html=False
        )
        
        rolling_average_chart_html = pio.to_html(
            rolling_average_chart,
            include_plotlyjs=False,
            div_id="rolling-average-chart",
            full_html=False
        )
        
        # Create table
        table_html = self.create_yearly_quarterly_table(region_data)
        
        # Calculate summary statistics (filtered from 2015)
        region_data_filtered = region_data[region_data['jaar'] >= 2015].copy()
        total_permits = region_data_filtered['alle_woningen'].sum()
        total_houses = region_data_filtered['aantal_huizen'].sum()
        total_flats = region_data_filtered['aantal_flats'].sum()
        date_range = f"{region_data_filtered['jaar'].min()} - {region_data_filtered['jaar'].max()}"
        
        # Prepare statistics for template
        stats = {
            'total_permits': total_permits,
            'total_houses': total_houses,
            'total_flats': total_flats,
            'date_range': date_range
        }
        
        # Generate HTML using template manager
        html_content = self.template_manager.render_building_permits_report(
            region_name=region_name,
            stats=stats,
            quarterly_table=table_html,
            chart_html=chart_html,
            yearly_quarters_chart_html=yearly_quarters_chart_html,
            rolling_average_chart_html=rolling_average_chart_html,
            output_dir=output_dir
        )
        
        # Save report
        output_file = output_dir / f"{region_name.replace(' ', '_').replace('/', '_')}_rapport.html"
        self.template_manager.save_report(html_content, output_file)
        
        print(f"Report generated: {output_file}")
        return output_file
    
    def generate_all_reports(self, output_dir: str = "reports/building_permits"):
        """Generate reports for all provinces and regions."""
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        if self.standardized_data is None:
            self.load_and_prepare_data()
        
        generated_reports = []
        
        print("Generating reports for all regions...")
        print("="*50)
        
        # Generate reports for provinces
        provinces = self.get_provinces()
        print(f"Generating reports for {len(provinces)} provinces...")
        
        for province in provinces:
            try:
                report_file = self.create_region_report(province, output_path)
                generated_reports.append(report_file)
            except Exception as e:
                print(f"Error generating report for {province}: {e}")
        
        # Generate reports for main regions
        regions = self.get_regions()
        print(f"Generating reports for {len(regions)} main regions...")
        
        for region in regions:
            try:
                report_file = self.create_region_report(region, output_path)
                generated_reports.append(report_file)
            except Exception as e:
                print(f"Error generating report for {region}: {e}")
        
        print("="*50)
        print(f"Report generation complete!")
        print(f"Generated {len(generated_reports)} reports in: {output_path.absolute()}")
        
        # Create index file
        self.create_index_file(output_path, generated_reports)
        
        return generated_reports
    
    def create_index_file(self, output_dir: Path, report_files: List[Path]):
        """Create an index HTML file linking to all reports."""
        
        provinces = self.get_provinces()
        regions = self.get_regions()
        
        # Generate HTML using template manager
        html_content = self.template_manager.render_index_page(
            provinces=provinces,
            regions=regions,
            output_dir=output_dir
        )
        
        # Save index file
        index_file = output_dir / "index.html"
        self.template_manager.save_report(html_content, index_file)
        
        print(f"Index file created: {index_file}")


def main():
    """Main function to generate all reports."""
    
    # CSV file path
    csv_file = "data/csv/Bouwvergunningen_voor_woongebouwen,_indeling_naar_arrondissementen.csv"
    
    if not Path(csv_file).exists():
        print(f"CSV file not found: {csv_file}")
        print("Please run the Excel processor notebook first to generate CSV files.")
        return
    
    # Create report generator
    generator = BuildingPermitsReportGenerator(csv_file)
    
    # Generate all reports
    reports = generator.generate_all_reports()
    
    print(f"\n🎉 All reports generated successfully!")
    print(f"📁 Open 'reports/building_permits/index.html' to view all reports")


if __name__ == "__main__":
    main()
