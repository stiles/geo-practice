import os
import json
import logging
from datetime import datetime
from openai import OpenAI

# Configure logging
def setup_logging():
    # Create logs directory if it doesn't exist
    log_dir = "./logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # Generate a timestamp for the log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"geoguessr_clues_{timestamp}.log")
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()  # Also print to console
        ]
    )
    return log_file

# Function to load existing factbook
def load_existing_factbook(output_file):
    try:
        with open(output_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logging.info(f"No existing factbook found at {output_file}. Starting fresh.")
        return {}

# Function to generate GeoGuessr clues with enhanced error handling
def generate_geoguessr_clues(client, country, country_info):
    try:
        # Requesting clues from the OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a geography expert creating structured insights for GeoGuessr players."},
                {"role": "user", "content": f"""Provide details for {country} to help identify it from Google Street View in this exact JSON format:

{{
  "language": "Common languages and descriptions of alphabet and any special characters",
  "cars": "Details on vehicle registration plates",
  "driving": "The side of roads where vehicles drive",
  "signs": "Road/highway sign characteristics",
  "environment": "Geographical and natural landscape features",
  "infrastructure": "Architectural styles and urban design elements",
  "culture": "Distinctive markers that help identify the location",
  "bonus": "Other features to identify country on Google Street View",
  "flag": "Flag description"
}}

Format the response as a strict JSON object. Do not include any explanatory text."""}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        # Extract the text response
        response_text = response.choices[0].message.content.strip()
        
        # Parse the JSON
        clues = json.loads(response_text)
        
        # Merge with existing country information
        return {**country_info, "geoguessr_clues": clues}
    
    except json.JSONDecodeError:
        # Handle JSON parsing errors
        logging.error(f"JSON parsing error for {country}")
        return {
            **country_info,
            "Error": f"Failed to parse JSON for {country}",
            "Raw Response": response_text
        }
    except Exception as e:
        # Structured error handling
        logging.error(f"Error generating clues for {country}: {str(e)}")
        return {
            **country_info,
            "Error": f"Failed to generate clues for {country}",
            "Details": str(e)
        }

# Main function to generate country factbook
def generate_geoguessr_clues(input_file, output_file):
    # Setup logging
    log_file = setup_logging()
    logging.info(f"Logging to {log_file}")
    
    # Initialize the OpenAI client
    client = OpenAI(api_key=os.environ.get("OPEN_AI"))
    
    # Load country data
    try:
        with open(input_file, "r") as f:
            country_data = json.load(f)
    except Exception as e:
        logging.error(f"Error loading input file {input_file}: {str(e)}")
        return
    
    # Load existing factbook to resume or skip processed countries
    geoguessr_clues = load_existing_factbook(output_file)
    
    # Process countries
    processed_count = 0
    skipped_count = 0
    error_count = 0
    
    for country_info in country_data:
        country_name = country_info.get('name', '')
        
        # Check if country already processed
        if country_name in geoguessr_clues:
            logging.info(f"Skipping {country_name} - already processed")
            skipped_count += 1
            continue
        
        try:
            logging.info(f"Processing {country_name}...")
            
            # Generate clues
            country_details = generate_geoguessr_clues(client, country_name, country_info)
            
            # Add to factbook
            geoguessr_clues[country_name] = country_details
            processed_count += 1
            
            # Periodically save progress
            if processed_count % 10 == 0:
                save_progress(geoguessr_clues, output_file)
        
        except Exception as e:
            logging.error(f"Unexpected error processing {country_name}: {str(e)}")
            error_count += 1
    
    # Final save
    save_progress(geoguessr_clues, output_file)
    
    # Log summary
    logging.info("=" * 50)
    logging.info("Processing Summary:")
    logging.info(f"Total Countries: {len(country_data)}")
    logging.info(f"Processed Countries: {processed_count}")
    logging.info(f"Skipped Countries: {skipped_count}")
    logging.info(f"Countries with Errors: {error_count}")
    logging.info(f"Output saved to: {output_file}")

# Helper function to save progress
def save_progress(geoguessr_clues, output_file):
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(geoguessr_clues, f, ensure_ascii=False, indent=4)
        logging.info(f"Progress saved to {output_file}")
    except Exception as e:
        logging.error(f"Error saving progress: {str(e)}")

# Main execution
if __name__ == "__main__":
    input_file = "./data/countries_regions.json"
    output_file = "./data/geoguessr_clues.json"
    generate_geoguessr_clues(input_file, output_file)