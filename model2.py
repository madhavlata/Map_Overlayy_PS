import json
from langchain_community.llms import CTransformers
from langchain.prompts import PromptTemplate

# Load the JSON file containing content
def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Save the results in the specified format
def save_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Initialize the language model
llm = CTransformers(
    model="/Users/pratyushgupta/Desktop/overlayy_PS_OOSC--master/llama-2-7b-chat.ggmlv3.q4_0.bin",
    model_type="llama",
    config={'max_new_tokens': 512, 'temperature': 0.8}
)

# Define the prompt template for question generation
question_generation_prompt = """
Generate questions that can be answered by the following piece of content:

Content: {content}

Questions:
"""

prompt_template = PromptTemplate(template=question_generation_prompt, input_variables=["content"])

# Function to split content into chunks and halve the content size
def split_content(content, max_tokens=256):  # Halved token limit
    words = content.split()
    chunks = []
    current_chunk = []

    for word in words:
        # Estimate token count for the current chunk + new word
        estimated_tokens = len(" ".join(current_chunk + [word]).split())

        if estimated_tokens <= max_tokens:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

# Load content data from JSON
content_data = load_json('final_output.json')  # Path to your input JSON file

# Create a list to store the results
result_data = []

# Process each URL and content
for item in content_data:
    url = item['url']
    content = item['content']

    # Split content into chunks to avoid exceeding context length, halving content size
    content_chunks = split_content(content, max_tokens=256)

    questions = []
    for chunk in content_chunks:
        # Generate questions using the model
        prompt_input = prompt_template.format(content=chunk)
        generated_output = llm.invoke(prompt_input)  # Use 'invoke' instead of '__call__'

        # Split the generated output into individual questions
        chunk_questions = [q.strip() for q in generated_output.split('\n') if q.strip()]
        questions.extend(chunk_questions)

    # Ensure only 10 questions are stored
    questions = questions[:10]

    # Store the results for this URL in the required format
    result_data.append({
        "url": url,
        "questions": [f"{i+1}. {question}" for i, question in enumerate(questions)]
    })

# Save the generated questions to a new JSON file
save_json(result_data, 'generated_questions2.json')

print("Questions generated and saved to generated_questions2.json.")
