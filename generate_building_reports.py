#!/usr/bin/env python3
"""
Generate Building Permits Reports

This script generates HTML reports for building permits data per province and region.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from building_permits_report import BuildingPermitsReportGenerator


def main():
    """Generate building permits reports."""
    
    csv_file = "data/csv/Bouwvergunningen_voor_woongebouwen,_indeling_naar_arrondissementen.csv"
    
    print("🏗️  Building Permits Report Generator")
    print("="*50)
    
    if not Path(csv_file).exists():
        print(f"❌ CSV file not found: {csv_file}")
        print("Please run the Excel processor notebook first to generate CSV files.")
        return
    
    # Create report generator
    generator = BuildingPermitsReportGenerator(csv_file)
    
    try:
        # Generate all reports
        reports = generator.generate_all_reports("reports/building_permits")
        
        print(f"\n✅ Successfully generated {len(reports)} reports!")
        print(f"📂 Reports saved in: reports/building_permits/")
        print(f"🌐 Open 'reports/building_permits/index.html' to view all reports")
        
    except Exception as e:
        print(f"❌ Error generating reports: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
