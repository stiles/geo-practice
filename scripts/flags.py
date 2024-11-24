import os
import pandas as pd
import json

# Fetch the country data
with open("data/countries_regions.json", "r") as f:
    country_codes_df = json.load(f)

# Directory where the flag images are stored
images_dir = "images"

# Output HTML file
output_file = "flags.html"

# HTML template with escaped curly braces in the CSS
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://api.mapbox.com/mapbox-gl-js/v3.8.0/mapbox-gl.js"></script>
    <link href="https://api.mapbox.com/mapbox-gl-js/v3.8.0/mapbox-gl.css" rel="stylesheet" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Text:ital@0;1&family=Noto+Sans:ital,wght@0,100..900;1,100..900&family=Playfair+Display:ital,wght@0,400..900;1,400..900&family=Roboto+Slab:wght@100..900&family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&family=Source+Sans+3:ital,wght@0,200..900;1,200..900&display=swap" rel="stylesheet">
    <title>Country Flags Grid</title>
    <style>
        :root {{
            --white: #ffffff;
            --gray: #f0f0f0;
            --dark-gray: #333;
            --blue: #4a90e2;
        }}
        body {{
            font-family: 'Roboto', Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: var(--gray);
            color: var(--dark-gray);
        }}
        h1 {{
            text-align: center;
            padding: 20px 0;
            margin: 0;
            background-color: var(--blue);
            color: var(--white);
            font-size: 26px;
        }}
        .filter-container {{
            text-align: center;
            margin: 20px 0;
        }}
        .filter-input {{
            padding: 10px;
            width: 80%;
            max-width: 400px;
            font-size: 16px;
            font-family: 'Roboto', Arial, sans-serif;
            border: .2px solid var(--dark-gray);
            border-radius: 5px;
        }}
        .region-section {{
            margin: 30px auto;
            width: 90%;
            max-width: 1800px;
        }}
        .region-title {{
            font-size: 20px;
            font-weight: bold;
            margin: 20px 0 10px;
            color: var(--dark-gray);
        }}
        .grid-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); /* Ensure min width of 110px */
            gap: 10px;
            justify-content: center; /* Center-align items in the grid */
         }}

        .grid-item {{
            text-align: center;
            font-size: 14px;
            background-color: var(--white);
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            display: inline-block; /* Maintain consistent item size */
            width: 100%; /* Prevent items from exceeding their natural width */
            max-width: 100px; /* Limit the maximum width */
         }}
        .grid-item img {{
            width: 80%;
            max-height: 50px;
            height: auto;
            border-radius: 5px;
        }}
    </style>
    <script>
        // Filter function
        function filterFlags() {{
            const input = document.getElementById('filter-input').value.toLowerCase();
            const items = document.querySelectorAll('.grid-item');
            items.forEach(item => {{
                const text = item.getAttribute('data-name').toLowerCase();
                item.style.display = text.includes(input) ? 'block' : 'none';
            }});
        }}
    </script>
</head>
<body>
    <h1>Explore national flags</h1>
    <div class="filter-container">
        <input type="text" id="filter-input" class="filter-input" oninput="filterFlags()" placeholder="Filter the grid for a specific place...">
    </div>
    {regions}
</body>
</html>
"""

# Group countries by region
regions = {}
for country in country_codes_df:
    region = country.get("region", "Unknown")
    if region not in regions:
        regions[region] = []
    flag_file = f"{images_dir}/{country['code']}.png"
    if os.path.exists(flag_file):
        regions[region].append({
            "name": country["name"],
            "code": country["code"],
            "flag_path": flag_file
        })

# Generate HTML for each region and its flags
regions_html = ""
for region, countries in regions.items():
    flags_html = "".join([
        f"""
        <div class="grid-item" data-name="{country['name']}">
            <img src="{country['flag_path']}" alt="{country['name']}">
            <p>{country['name']}</p>
        </div>
        """
        for country in countries
    ])
    regions_html += f"""
    <div class="region-section">
        <div class="region-title">{region}</div>
        <div class="grid-container">
            {flags_html}
        </div>
    </div>
    """

# Combine the template with the regions HTML
final_html = html_template.format(regions=regions_html)

# Write to the output file
with open(output_file, "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"HTML file generated: {output_file}")