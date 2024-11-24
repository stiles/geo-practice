import os
import requests
import pandas as pd

# Fetch the country lookup
url = "https://flagcdn.com/en/codes.json"
response = requests.get(url)

# Parse the JSON content into dict
country_codes = response.json()

# Filter out entries with "us-" codes and any other known invalid entries
valid_country_codes = {
    code: name for code, name in country_codes.items()
    if not code.startswith("us-") and name not in ["United States", "European Union", "United Nations"]
}

# URL base for flag images
base_url = "https://flagpedia.net/data/flags/h80"

# Directory to store images
images_dir = "images"
os.makedirs(images_dir, exist_ok=True)

# Iterate through country codes and names
for code, country in valid_country_codes.items():
    # Construct the flag image URL
    flag_url = f"{base_url}/{code}.png?v=un"
    
    try:
        # Fetch the flag image
        response = requests.get(flag_url)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        # Save the image to the images directory
        image_path = os.path.join(images_dir, f"{code}.png")
        with open(image_path, "wb") as f:
            f.write(response.content)
        
        print(f"Downloaded: {country} ({code})")
    except Exception as e:
        # Handle errors (e.g., image not found)
        print(f"Failed to download flag for {country} ({code}): {e}")

print("Flag download complete!")