# GeoGuessr vibe generator

This repository contains a growing set of tools aimed at boosting your play on GeoGuessr, a game that challenges users to recognize locations from Google Street View's panoramic images. 

The project was born out of a desire to help my kids better understand geography, but it has turned into an experiement in using AI tools to generate structured data — in this case hints for identifying world countries and US states on the roadways. 

The project, for now, includes scripts to collect and generate game-specific metadata about counties. It also contains code to create a simple country mapping quiz and a filterable grid of national flags, with country-specific pages baked into static files. 

*It's very new and a work in progress.* 

---

## Project structure

### Directories

#### `data/`
This directory contains various datasets used throughout the project:
- **`codes.json`**: A file mapping of ISO-2 country codes and associated names.
- **`countries_regions.json`**: A metadata file that includes ~240 countries and territories with their centroid coordinates, regions and sub-regions, among other items. 
- **`geoguessr_clues.json`**: A JSON file derived by `gpt-4o-mini` that lists key Street View clues about ~240 countries and territories.
- **`geoguessr_clues_usa_states.json`**: A JSON file derived by `gpt-4o-mini` that lists key Street View clues about the 50 states and the District of Columbia.
- **`usa_states_regions.json`**: A metadata file that includes centroid coordinates, regions and other information about the 50 US states and the District of Columbia. 

#### `images/`
A directory containing flag images for all countries, saved as PNG files named by their country codes (e.g., `us.png` for the United States), sourced from [Flagpedia](https://flagpedia.net/).

#### `scripts/`
Python scripts used for generating and managing the project assets:
- **`fetch.py`**: Handles data fetching and preprocessing for country metadata.
- **`flags.py`**: Generates the HTML file for the flag grid.
- **`quiz.py`**: Contains logic for the interactive map quiz.
- **`regions.py`**: Utility scripts for region-based categorization and filtering.