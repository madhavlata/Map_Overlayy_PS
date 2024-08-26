import json
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from langchain_community.vectorstores import Pinecone as LangchainPinecone
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()
os.environ['PINECONE_API_KEY'] = 'your_pinecone_api_key'
KEY = os.getenv("PINECONE_API_KEY")

# Load the JSON files
def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

questions_data = load_json('generated_questions1.json')  # Contains URL and 10 questions per URL
content_data = load_json('output1.json')  # Contains URL and corresponding content

# Initialize model and prompt
def download_hugging_face_embedding():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings

embeddings = download_hugging_face_embedding()

# Initialize the language model
llm = CTransformers(
    model="C:/Users/anant/deep learning/Medical_chat_bot/model/llama-2-7b-chat.ggmlv3.q4_0.bin",
    model_type="llama",
    config={'max_new_tokens': 512, 'temperature': 0.8}
)

# Define the prompt template
prompt = """
Use the following piece of information to answer the user's question 
if you don't know the answer, say just that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}
Only return the helpful answer below and nothing else.
Helpful answer:
"""

prompt_template = PromptTemplate(template=prompt, input_variables=["context", "question"])
chain_type_kwargs = {"prompt": prompt_template}

# Create a dictionary to store the results
result_data = []

# Process each URL, questions, and content
for item in questions_data:
    url = item['url']
    questions = item['questions']

    # Find the corresponding content for the URL
    content_item = next((content for content in content_data if content['url'] == url), None)
    
    if not content_item:
        continue  # Skip if no corresponding content is found

    content = content_item['content']

    # Prepare the retrieval QA chain
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=None,  # No external retriever needed, content is provided directly
        return_source_documents=True,
        chain_type_kwargs=chain_type_kwargs
    )

    # Generate answers for each question
    answers = []
    for question in questions:
        query_result = qa({"query": question, "context": content})
        answer = query_result['result']
        answers.append({"question": question, "answer": answer})

    # Store the results for this URL
    result_data.append({"url": url, "qa_pairs": answers})

# Save the results to a new JSON file
with open('output_answers.json', 'w') as f:
    json.dump(result_data, f, indent=4)

print("Answers generated and saved to output_answers.json.")