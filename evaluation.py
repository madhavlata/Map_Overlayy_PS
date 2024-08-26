import os
import json
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.callbacks import get_openai_callback
from langchain.prompts import PromptTemplate

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key
KEY = os.getenv("OPENAI_KEY")
llm = ChatOpenAI(openai_api_key=KEY, model_name="gpt-3.5-turbo", temperature=0.5)

# Define the templates
Template = """
Text : {text}
You are an expert evaluator. Your job is to assess the quality of the multiple-choice questions (MCQs) generated from the given text. Evaluate the questions based on the following criteria and provide a score between 0 (lowest) and 100 (highest):
Relevance Check: Verify if the MCQs are relevant to the content provided and accurately reflect the information. Each question should be directly related to the text without any repetition.
Word Count Check: Ensure that each MCQ contains fewer than 80 words.
Question Count Check: Confirm that exactly 10 MCQs have been provided.
Link Count Check: Ensure that exactly 5 relevant links are included.
Make sure your response is in given json format

{RESPONSE_JSON} 
"""

RESPONSE_JSON = json.dumps({
    "relevance_check": "{Relevance check: PASS/FAIL}",
    "word_count_check": "{Word count check: PASS/FAIL}",
    "question_count_check": "{Question count: PASS/FAIL}",
    "link_count_check": "{Link count: PASS/FAIL}",
    "overall_score": "{Overall score out of 100}",
    "feedback": "{Detailed feedback on what was done well or areas for improvement}"
}, indent=4)

# First prompt chain
prompt1 = PromptTemplate(
    input_variables=["text", "RESPONSE_JSON"],
    template=Template,
)

quiz_chain = LLMChain(llm=llm, prompt=prompt1, output_key="quiz", verbose=True)

Template2 = """
TEXT = {quiz}
You are an expert evaluator. Your job is to assess the quality of the multiple-choice questions (MCQs) generated from the given text. Evaluate the questions based on the following criteria and provide a score between 0 (lowest) and 100 (highest). give the final answer in as a result(integer) and print the answer in score 
Make sure you output the answer in given json format
{RESPONSE_JSON1}
"""

RESPONSE_JSON1 = json.dumps({
    "Total Score": "{score}"
}, indent=4)

# Second prompt chain
quiz_ev_prompt = PromptTemplate(
    input_variables=["quiz", "RESPONSE_JSON1"],
    template=Template2,
)

review_chain = LLMChain(llm=llm, prompt=quiz_ev_prompt, output_key="review", verbose=True)

# Sequential Chain combining both chains
evaluate_chains = SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=["text", "RESPONSE_JSON", "RESPONSE_JSON1"],
    output_variables=["quiz", "review"],
    verbose=True
)

def get_content_by_url(data, url):
    """Retrieve content associated with a given URL from the JSON data."""
    for item in data:
        if item['url'] == url:
            return item['content']
    return None

def evaluate_link_relevance(content, links, data):
    """Evaluate the relevance of links based on their content."""
    link_relevance = []
    for link in links:
        link_content = get_content_by_url(data, link)
        if link_content:
            # Here you would include logic to evaluate relevance
            # For demonstration, let's assume all links are relevant
            relevance = "Relevant"  # Placeholder, replace with actual evaluation
            link_relevance.append({
                "link": link,
                "relevance": relevance
            })
    return link_relevance

# Load input data from JSON file
with open('merged_output.json', 'r') as file:
    input_data = json.load(file)

# Process each item in the list
for item in input_data:
    text = item.get("content", "")
    relevant_links = item.get("relevant_links", [])  # Ensure this key exists

    if text:  # Ensure text is not empty
        # Process the data and get the response
        with get_openai_callback() as cb:
            response = evaluate_chains({
                "text": text,
                "RESPONSE_JSON": RESPONSE_JSON,
                "RESPONSE_JSON1": RESPONSE_JSON1
            })

        # Print token usage
        print(f"Total tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Total cost: {cb.total_cost}")

        # Extract and print results
        quiz = response.get("quiz", "")
        review = response.get("review", "")

        print("Quiz evaluation:")
        print(quiz)
        print("\nReview:")
        print(review)

        # Check relevance of the relevant links
        link_relevance = evaluate_link_relevance(text, relevant_links, input_data)

        # Save results to JSON file
        output_data = {
            "quiz": json.loads(quiz),
            "review": json.loads(review),
            "link_relevance": link_relevance
        }

        output_filename = f'output_{item.get("id", "unknown")}.json'
        with open(output_filename, 'w') as file:
            json.dump(output_data, file, indent=4)
