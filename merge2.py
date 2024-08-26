import json

def load_json(filename):
    """Load JSON data from a file."""
    with open(filename, 'r') as file:
        return json.load(file)

def save_json(data, filename):
    """Save JSON data to a file."""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def merge_json_files(content_file, links_file, output_file):
    """Merge the content and links from two JSON files into one."""
    content_data = load_json(content_file)
    links_data = load_json(links_file)

    # Create a dictionary for quick lookup
    content_dict = {entry['url']: entry for entry in content_data}
    
    # Merge data
    for entry in links_data:
        url = entry['url']
        if url in content_dict:
            content_dict[url]['relevant_links'] = entry.get('relevant_links', [])
            content_dict[url]['questions'] = entry.get('questions', [])
        else:
            content_dict[url] = {
                'url': url,
                'content': '',
                'title': '',
                'relevant_links': entry.get('relevant_links', []),
                'questions': entry.get('questions', [])
            }
    
    # Save the merged data
    merged_data = list(content_dict.values())
    save_json(merged_data, output_file)

def main():
    # Define file names
    final_output_file = 'final_output.json'
    final_output_links_file = 'final_output_with_relevant_links.json'
    merged_output_file = 'merged_output.json'
    
    # Merge JSON files
    merge_json_files(final_output_file, final_output_links_file, merged_output_file)
    print(f"Merged data saved to {merged_output_file}")

if __name__ == "__main__":
    main()
