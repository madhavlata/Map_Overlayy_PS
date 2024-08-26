import os
import json
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback
from langchain.prompts import PromptTemplate

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key
KEY = os.getenv("OPENAI_KEY")
llm = ChatOpenAI(openai_api_key=KEY, model_name="gpt-3.5-turbo", temperature=0.5)

# Define the template for generating questions
Template = """
Text: {text}
You are an expert in generating concise questions. Based on the above text, generate 10 questions that are directly related to the content. Each question should be clear, concise, and no more than 80 characters long.
"""

# Create the PromptTemplate object
prompt1 = PromptTemplate(
    input_variables=["text"],
    template=Template,
)

# Define the chain for generating questions
quiz_chain = LLMChain(llm=llm, prompt=prompt1, output_key="quiz", verbose=True)

# Read the JSON file with URLs and content
input_json_path = "final_output.json"
with open(input_json_path, 'r') as file:
    data = json.load(file)

# Initialize a list to store the final output
output_data = []

# Process each entry in the JSON file
for entry in data:
    url = entry.get("url", "")
    content = entry.get("content", "")

    # Generate questions for the content
    with get_openai_callback() as cb:
        response = quiz_chain.run({"text": content})

    # Parse the generated questions
    questions = response.strip().split('\n')[:10]  # Split the response into questions

    # Add the URL and generated questions to the output list
    output_data.append({
        "url": url,
        "questions": questions
    })

# Save the final output to a new JSON file
output_json_path = "generated_questions1.json"
with open(output_json_path, 'w') as outfile:
    json.dump(output_data, outfile, indent=4)

print(f"Questions generated and saved to {output_json_path}")
