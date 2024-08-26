import json

def load_json(filename):
    """Load JSON data from a file."""
    with open(filename, 'r') as f:
        return json.load(f)

def save_json(data, filename):
    """Save JSON data to a file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def update_anchor_texts(first_file, second_file, output_file):
    """Update anchor texts in the first JSON file based on the second JSON file."""
    # Load data from JSON files
    first_data = load_json(first_file)
    second_data = load_json(second_file)

    # Create a dictionary mapping URLs to their anchor texts from the second file
    anchor_map = {item['url']: item['title'] for item in second_data}
    
    # Update the anchor texts in the first file's data
    for item in first_data:
        url = item['url']
        if url in anchor_map:
            item['title'] = anchor_map[url]

    # Save the updated data to a new JSON file
    save_json(first_data, output_file)
    print(f"Updated data saved to {output_file}")

# Define file paths
first_file = 'output1.json'  # Replace with your first JSON file path
second_file = 'output2.json'  # Replace with your second JSON file path
output_file = 'final_output.json'  # Output file for the updated data

# Run the update function
update_anchor_texts(first_file, second_file, output_file)
