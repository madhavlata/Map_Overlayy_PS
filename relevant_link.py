import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_json(filename):
    """Load JSON data from a file."""
    with open(filename, 'r') as f:
        return json.load(f)

def calculate_relevance(questions, content):
    """Calculate relevance score between questions and content."""
    questions_text = " ".join(questions) if isinstance(questions, list) else questions
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([questions_text, content])
    similarity = cosine_similarity(vectors[0:1], vectors[1:])
    return similarity[0][0]

def get_top_relevant_links(questions, content_data):
    """Find the top 5 relevant links for a set of questions based on content."""
    relevance_scores = []
    for entry in content_data:
        url = entry['url']
        content = entry['content']
        title = entry.get('title', 'No Title')  # Get title or use 'No Title' if missing
        if content:  # Skip empty content
            score = calculate_relevance(questions, content)
            relevance_scores.append((url, title, score))
    
    # Sort links by relevance score in descending order
    relevance_scores.sort(key=lambda x: x[2], reverse=True)
    
    # Get the top 5 links with titles
    top_links = [{'url': url, 'title': title} for url, title, score in relevance_scores[:5]]
    return top_links

def main():
    # Load questions and content data
    questions_file = 'generated_questions1.json'  # Replace with your questions file
    content_file = 'final_output.json'  # Replace with your content file
    
    questions_data = load_json(questions_file)
    content_data = load_json(content_file)
    
    results = []
    
    # Process each set of 10 questions
    for entry in questions_data:
        url = entry['url']
        questions = entry['questions']  # Assuming questions are stored as a list
        
        # Get top relevant links for this set of questions
        top_links = get_top_relevant_links(questions, content_data)
        
        results.append({
            'url': url,
            'questions': questions,  # Include the 10 questions
            'relevant_links': top_links
        })
    
    # Save results to a new JSON file
    output_json_path = 'final_output_with_relevant_links.json'
    with open(output_json_path, 'w') as f:
        json.dump(results, f, indent=4)
    
    print(f"Relevant links saved to {output_json_path}")

if __name__ == "__main__":
    main()
