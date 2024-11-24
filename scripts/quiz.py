import random
import json
import requests
import json
import os

# Fetch the country lookup
url = "https://flagcdn.com/en/codes.json"
response = requests.get(url)

# Parse the JSON content into dict
country_codes_src = response.json()

# Filter out entries with "us-" codes and any other known invalid entries
country_codes = {
    code: name for code, name in country_codes_src.items()
    if not code.startswith("us-") and name not in ["United States", "European Union", "United Nations"]
}

# Paths to input and output files
centroid_file = "country_centroids.json"
output_file = "quiz.html"

# Load the country centroid data
if not os.path.exists(centroid_file):
    raise FileNotFoundError(f"{centroid_file} not found in the current directory.")

with open(centroid_file, "r") as f:
    country_centroids = json.load(f)

# Build a lookup dictionary for centroids by alpha2 code
centroid_lookup = {entry["alpha2"].lower(): entry for entry in country_centroids}

# Filter and merge valid countries with geolocation data
valid_country_data = [
    {
        "code": code,
        "name": name,
        "lat": centroid_lookup[code]["latitude"],
        "lon": centroid_lookup[code]["longitude"]
    }
    for code, name in country_codes.items()
    if code in centroid_lookup
]

# Generate JSON representation of the valid country data
country_data_json = json.dumps(valid_country_data)

# HTML Template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Country Quiz</title>
    <script src="https://api.mapbox.com/mapbox-gl-js/v3.8.0/mapbox-gl.js"></script>
    <link href="https://api.mapbox.com/mapbox-gl-js/v3.8.0/mapbox-gl.css" rel="stylesheet" />
    <style>
        :root {{
            --french-gray: #aaabbcff;
            --battleship-gray: #8b8982ff;
            --charcoal: #373f47ff;
            --silver-lake-blue: #6c91c2ff;
            --periwinkle: #c3c9e9ff;
        }}
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: var(--french-gray);
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        #map {{
            width: 100%;
            max-width: 800px;
            height: 400px;
            margin: 20px 0;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .quiz-container {{
            text-align: center;
        }}
        .options {{
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .option {{
            padding: 10px 20px;
            background-color: var(--silver-lake-blue);
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }}
        .option:hover {{
            background-color: var(--charcoal);
        }}
        .flag {{
            width: 30px;
            height: auto;
            margin-right: 8px;
        }}
        .answer-display {{
            margin-top: 20px;
            font-size: 18px;
            color: var(--charcoal);
        }}
    </style>
</head>
<body>
    <div id="map"></div>
    <div class="quiz-container">
        <h1 id="question"></h1>
        <div class="options" id="options"></div>
        <div class="answer-display" id="answer-display"></div>
    </div>

    <script>
        mapboxgl.accessToken = 'pk.eyJ1Ijoic3RpbGVzIiwiYSI6ImNsd3Rpc3V2aTAzeXUydm9sMHdoN210b2oifQ.66AJmPYxe2ixku1o7Rwdlg';

        const countryData = {country_data_json};

        function getRandomCountry(exclude = null) {{
            let filtered = countryData.filter(c => c.code !== exclude);
            return filtered[Math.floor(Math.random() * filtered.length)];
        }}

        function generateQuiz() {{
            const correctCountry = getRandomCountry();
            const map = new mapboxgl.Map({{
                container: 'map',
                style: 'mapbox://styles/stiles/cm3uoaup0005901pzbh9e9vxy',
                center: [correctCountry.lon, correctCountry.lat],
                zoom: 4,
                maxZoom: 8
            }});

            new mapboxgl.Marker({{
                color: 'var(--periwinkle)'
            }})
                .setLngLat([correctCountry.lon, correctCountry.lat])
                .addTo(map);

            const questionEl = document.getElementById('question');
            const optionsEl = document.getElementById('options');
            const answerDisplay = document.getElementById('answer-display');

            questionEl.textContent = `Which country is shown on the map?`;
            answerDisplay.textContent = '';

            const options = [correctCountry];
            while (options.length < 4) {{
                const randomCountry = getRandomCountry(correctCountry.code);
                if (!options.some(o => o.code === randomCountry.code)) {{
                    options.push(randomCountry);
                }}
            }}

            options.sort(() => Math.random() - 0.5);

            optionsEl.innerHTML = '';
            options.forEach(option => {{
                const btn = document.createElement('button');
                btn.classList.add('option');
                btn.innerHTML = `<img src="https://flagcdn.com/w40/${{option.code}}.png" class="flag">${{option.name}}`;
                btn.addEventListener('click', () => {{
                    if (option.code === correctCountry.code) {{
                        answerDisplay.textContent = `Correct! The country is ${{correctCountry.name}}.`;
                    }} else {{
                        answerDisplay.textContent = `Oops! The correct answer was ${{correctCountry.name}}.`;
                    }}
                    setTimeout(generateQuiz, 2000);
                }});
                optionsEl.appendChild(btn);
            }});
        }}

        generateQuiz();
    </script>
</body>
</html>
"""


# Write the HTML file
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_template.format(country_data_json=country_data_json))

print(f"Quiz page generated: {output_file}")
