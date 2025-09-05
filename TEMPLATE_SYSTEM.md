# Template System Documentation

## Overview

The project now uses a unified template system with Jinja2 templates and a single CSS file. This replaces the previous system where each Python file generated its own embedded CSS and HTML.

## Structure

```
templates/
├── base.html                    # Base template with common structure
├── building_permits_report.html # Specific template for building permits
├── index.html                   # Template for index pages
└── generic_report.html          # Generic report template

static/
└── css/
    └── styles.css               # Unified CSS file with all styles

src/
├── template_manager.py          # Centralized template management
├── building_permits_report.py   # Updated to use templates
└── html_report.py               # Updated to use templates
```

## Key Components

### 1. TemplateManager (src/template_manager.py)
- Centralizes all template rendering
- Manages CSS file copying to output directories
- Provides specialized methods for different report types
- Handles Jinja2 environment setup with custom filters

### 2. Unified CSS (static/css/styles.css)
- Contains all styling for different report types
- Uses CSS variables for consistent theming
- Supports both the new Montserrat design and building permits styling
- Responsive design with media queries

### 3. Template Files

#### base.html
- Common HTML structure
- CSS and JavaScript includes
- Block system for customization
- Consistent header and footer

#### building_permits_report.html
- Extends base template
- Specific layout for building permits analysis
- Statistics grid and analysis sections
- Chart and table positioning

#### index.html
- Report listing template
- Grid layout for provinces and regions
- Consistent styling with other reports

#### generic_report.html
- For general reports from html_report.py
- Section-based content structure
- Chart container support

## Usage

### Building Permits Reports
```python
from template_manager import TemplateManager

template_manager = TemplateManager()

# Render building permits report
html_content = template_manager.render_building_permits_report(
    region_name="VLAAMS GEWEST",
    stats={"total_permits": 100000, ...},
    quarterly_table="<table>...</table>",
    chart_html="<div>...</div>",
    output_dir=Path("reports/building_permits")
)

# Save report
template_manager.save_report(html_content, output_path)
```

### Generic Reports
```python
# The html_report.py automatically uses the template system
report = HTMLReportGenerator("My Report")
report.add_section("Analysis", content, charts)
html_content = report.generate_html(output_path)
```

### Index Pages
```python
html_content = template_manager.render_index_page(
    provinces=["PROVINCIE ANTWERPEN", ...],
    regions=["VLAAMS GEWEST", ...],
    output_dir=output_dir
)
```

## Benefits

1. **Consistency**: Single CSS file ensures consistent styling across all reports
2. **Maintainability**: Changes to styling only need to be made in one place
3. **Separation of Concerns**: Templates handle presentation, Python handles data
4. **Flexibility**: Easy to create new report types by extending base template
5. **Performance**: CSS is cached by browsers, external file loads faster
6. **Reusability**: Templates can be reused across different report generators

## CSS Variables

The unified CSS uses CSS variables for easy theming:

```css
:root {
  --primary-dark: #2f2f2f;
  --header-bg: #f7f7f7;
  --section-bg: #f3f3f3;
  --link-accent: #19b6c8;
  --link-hover: #15a0ab;
  --card-bg: #fff;
  --border-radius: 8px;
  
  /* Building permits specific */
  --primary-blue: #1f3563;
  --accent-yellow: #ffd600;
  --light-gray: #f5f6fa;
}
```

## Migration Complete

All existing functionality has been migrated to the new template system:
- ✅ Building permits reports use templates
- ✅ Index page uses templates  
- ✅ Generic reports use templates
- ✅ Unified CSS system implemented
- ✅ All reports generated successfully
- ✅ CSS files automatically copied to output directories

The system maintains backward compatibility while providing a much cleaner and more maintainable architecture.
