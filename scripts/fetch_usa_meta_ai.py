import os
import json
import logging
from datetime import datetime
from openai import OpenAI

# Configure logging
def setup_logging():
    # Create logs directory if it doesn't exist
    log_dir = "./logs/usa"
    os.makedirs(log_dir, exist_ok=True)
    
    # Generate a timestamp for the log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"geoguessr_clues_usa_{timestamp}.log")
    
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
def generate_state_clues(client, state_name, state_info):
    try:
        # Requesting clues from the OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
    "role": "user",
    "content": f"""You are a USA geography compiling a concise fact sheet to help GeoGuessr players identify details about the US state of {state_name} that might be visible on Google Street View. Strictly adhere to the following JSON format without adding any explanatory text. Format your response as valid JSON, ensuring proper syntax:

{{
  "cars": "The main color of {state_name}'s most-common vehicle registration plate, e.g. New York being yellow and Oregon having a tree, and any unique color elements, such as blue and yellow stripes horizontally in Pennsylvania",
  "driving": "Any major highways or Interstates that would identify {state_name}",
  "signs": "Road/highway sign characteristics in {state_name}, if they differ from the US norm",
  "environment": "Geographical and natural landscape features of {state_name}: trees, soil, agriculture, etc.",
  "infrastructure": "Architectural styles and urban design elements most common or unique to {state_name}",
  "culture": "Distinctive markers that help identify {state_name} along roadways, e.g. grain silos in Iowa or churches in Texas",
  "bonus": "Any other interesting features to serve as clues that would identify {state_name} on Google Street View"
}}

For example, provide complete JSON data in the structure above."""
}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        # Extract the text response
        response_text = response.choices[0].message.content.strip()
        
        # Parse the JSON
        clues = json.loads(response_text)
        
        # Merge with existing state information
        return {**state_info, "geoguessr_clues": clues}
    
    except json.JSONDecodeError:
        # Handle JSON parsing errors
        logging.error(f"JSON parsing error for {state_name}")
        return {
            **state_info,
            "Error": f"Failed to parse JSON for {state_name}",
            "Raw Response": response_text
        }
    except Exception as e:
        # Structured error handling
        logging.error(f"Error generating clues for {state_name}: {str(e)}")
        return {
            **state_info,
            "Error": f"Failed to generate clues for {state_name}",
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
            state_data = json.load(f)
    except Exception as e:
        logging.error(f"Error loading input file {input_file}: {str(e)}")
        return
    
    # Load existing factbook to resume or skip processed states
    geoguessr_clues = load_existing_factbook(output_file)
    
    # Process states
    processed_count = 0
    skipped_count = 0
    error_count = 0

    
    for state_info in state_data:
        state_name = state_info.get('state_name', '')
        
        # Check if country already processed
        if state_name in geoguessr_clues:
            logging.info(f"Skipping {state_name} - already processed")
            skipped_count += 1
            continue
        
        try:
            logging.info(f"Processing {state_name}...")
            
            # Generate clues
            state_details = generate_state_clues(client, state_name, state_info)
            
            # Add to factbook
            geoguessr_clues[state_name] = state_details
            processed_count += 1
            
            # Periodically save progress
            if processed_count % 10 == 0:
                save_progress(geoguessr_clues, output_file)
        
        except Exception as e:
            logging.error(f"Unexpected error processing {state_name}: {str(e)}")
            error_count += 1
    
    # Final save
    save_progress(geoguessr_clues, output_file)
    
    # Log summary
    logging.info("=" * 50)
    logging.info("Processing Summary:")
    logging.info(f"Total states: {len(state_data)}")
    logging.info(f"Processed states: {processed_count}")
    logging.info(f"Skipped states: {skipped_count}")
    logging.info(f"states with Errors: {error_count}")
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
    input_file = "./data/usa_states_regions.json"
    output_file = "./data/geoguessr_clues_usa_states.json"
    generate_geoguessr_clues(input_file, output_file)