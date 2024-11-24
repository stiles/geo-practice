import pandas as pd
import json

# Load the country data
with open("countries.json", "r") as f:
    country_data = json.load(f)

country_df = pd.DataFrame(country_data)  # Convert JSON to DataFrame

# Load the ISO to continents mapping
iso_mapping = pd.read_csv("iso_to_continents.csv")

# Select relevant columns from the ISO dataset
iso_mapping = iso_mapping[["alpha-2", "region", "sub-region"]].rename(columns={"alpha-2": "code"})
iso_mapping['code'] = iso_mapping['code'].str.lower()

# Merge datasets on the 'code' column
merged_df = country_df.merge(iso_mapping, on="code", how="left")

# Fill missing regions with "Unknown"
merged_df["region"] = merged_df["region"].fillna("Unknown")
merged_df["sub-region"] = merged_df["sub-region"].fillna("Unknown")

# Save the updated dataset back to JSON
merged_data = merged_df.to_dict(orient="records")
with open("data/country_data_with_regions.json", "w") as f:
    json.dump(merged_data, f, indent=2)

print("Regions added successfully!")