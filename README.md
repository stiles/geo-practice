# Geo practice: Tools for kids learning geography

This repository contains a growing set of tools designed to help my daughters improve their geography skills in a fun and interactive way. Currently, the project includes a **mapping quiz** and a **flag grid**, with more features planned for the future.

---

## 📂 Project structure

### Directories

#### `data/`
This directory contains various datasets used throughout the project:
- **`codes.json`**: A list of country codes and associated metadata.
- **`countries.json`**: A simplified dataset of country names and codes.
- **`countries_regions.json`**: An enriched dataset including countries, their regions, and sub-regions.
- **`iso_to_continents.csv`**: A CSV mapping ISO country codes to continents and regions.

#### `images/`
A directory containing flag images for all countries, saved as PNG files named by their country codes (e.g., `us.png` for the United States).

#### `scripts/`
Python scripts used for generating and managing the project assets:
- **`fetch.py`**: Handles data fetching and preprocessing for country metadata.
- **`flags.py`**: Generates the HTML file for the flag grid.
- **`quiz.py`**: Contains logic for the interactive map quiz.
- **`regions.py`**: Utility scripts for region-based categorization and filtering.

#### Other files
- **`flags.html`**: A dynamically generated HTML page displaying all country flags, grouped by region, with a search/filter feature.

---

## ✨ Features

### 1. Mapping quiz
An interactive quiz that challenges users to identify countries on a map:
- Uses the **Mapbox** library to display a world map.
- Dynamically fetches countries and provides multiple-choice options.
- Tracks the user's score over a 10-question quiz.
- Options to switch between map styles (e.g., satellite view) and navigate using controls.

### 2. Flag grid
A searchable and filterable grid of country flags:
- Flags are grouped by continent/region (e.g., Europe, Africa).
- Includes a search bar to filter flags by country name in real-time.
- Responsive grid layout with adjustable item sizing to handle varying screen sizes.

## Running the Quiz
- Start a local server, eg. `python -m http.server 8000`
- Open `index.html` in your browser.

## Customizing Data
- Modify `data/countries_regions.json` to add or adjust country data.
- Add or replace flag images in the `images/` directory.

## 🚀 Roadmap

Planned features and improvements:
1. **Timed quiz mode**: Add a time limit to answer each question.
2. **Detailed Score Feedback**: Provide insights into accuracy by continent or region.
3. **Interactive Learning Tools**: Incorporate capital cities, population data, and other trivia.
4. **Leaderboard**: Track scores and allow users to compete globally.
5. **Offline Mode**: Add support for using the flag grid offline.
6. **US states quiz**: Similar structure to the countries quiz

## 📜 License
This project is licensed under the MIT License. Feel free to use and modify it for personal or educational purposes.

## 👥 Contributors
- Contributions are welcome! Feel free to submit pull requests or report issues.