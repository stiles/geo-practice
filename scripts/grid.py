import os
import requests

# Fetch the country lookup
url = "https://flagcdn.com/en/codes.json"
response = requests.get(url)

# Parse the JSON content into dict
country_codes = response.json()

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
    <title>Country Flags</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-color: #f4f4f9;
        }}
        .grid-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
            gap: 10px;
            width: 90%;
            max-width: 1600px;
        }}
        .grid-item {{
            text-align: center;
            font-size: 12px;
        }}
        .grid-item img {{
            width: 100%;
            max-width: 100px;
            height: auto;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        }}
    </style>
</head>
<body>
    <div class="grid-container">
        {flags}
    </div>
</body>
</html>
"""

# Generate HTML for each flag
flags_html = ""
for image_file in os.listdir(images_dir):
    if image_file.endswith(".png"):
        country_code = os.path.splitext(image_file)[0]
        country_name = country_codes.get(country_code, "Unknown")
        flags_html += f"""
        <div class="grid-item">
            <img src="{images_dir}/{image_file}" alt="{country_name}">
            <p>{country_name}</p>
        </div>
        """

# Combine the template with the flags HTML
final_html = html_template.format(flags=flags_html)

# Write to the output file
with open(output_file, "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"HTML file generated: {output_file}")