# OOSC Hackathon Project
Team MAP (IIT Kanpur)-
Anant Srivastava
Pratyush Gupta
Madhav Lata
# Clone the Repository
git clone https://github.com/your-username/your-repository.git
cd your-repository

# Create a Virtual Environment
# For Windows:
python -m venv venv
venv\Scripts\activate

# For macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# Install Required Packages
pip install -r requirements.txt

# Run the Setup Script
python main.py 

# For Evaluation, run the evaluation script
python evaluation.py

# For Model 2
python model2.py

# Sample Website used - https://spo.iitk.ac.in/ 
## Final Output in the file - final_output_with_relevant_links.json

Our OPENAI_KEY was getting disabled on uploading on GitHub, if it is required contact on anantsrivastava02@gmail.com

# Web Scraping and Question Generation Model

This project combines web scraping, natural language processing, and machine learning techniques to extract information from websites and generate multiple-choice questions (MCQs) based on the extracted content.

#### Project Overview

This project consists of two main models:

1. Web Scraping and Initial Question Generation
2. Enhanced Question Generation with Embeddings and LLM

### Model 1: Web Scraping and Initial Question Generation

#### Features

- *Web Scraping*: Utilizes Beautiful Soup to extract links from web pages in a tree-like structure.
- *API Integration*: Incorporates ChatGPT API for generating initial questions.
- *Question Generation*: Creates a list of 10 questions along with their answers.
- *Accuracy Evaluation*: Implements an evaluation mechanism for the generated questions.
- *LangChain Integration*: Uses LangChain's Sequential and Chain components to build a checking loop.

#### How it works

1. The script uses Beautiful Soup to parse HTML content and extract links.
2. It then uses the ChatGPT API to generate questions based on the extracted content
3. A list of 10 questions is created.
4. The accuracy of the generated questions is evaluated using a custom mechanism.
5. LangChain's Sequential and Chain components are used to create a checking loop for quality assurance.

### Model 2: Enhanced Question Generation with Embeddings and LLM

#### Features

- *LangChain Integration*: Utilizes LangChain for advanced NLP tasks.
- *Vector Database*: Implements Pinecone as a vector database for efficient similarity searches.
- *Embeddings Generation*: Creates 384-dimensional embeddings for improved text representation.
- *LLaMA Model Integration*: Incorporates the LLaMA (Large Language Model Meta AI) for reaugmented learning.
- *Contextual Answer Generation*: Produces more relevant and context-aware answers.

#### How it works

1. The script uses LangChain to process the extracted text.
2. It generates 384-dimensional embeddings of the processed text.
3. These embeddings are stored in the Pinecone vector database for quick retrieval.
4. The LLaMA model is used for reaugmented learning, improving the quality of generated questions and answers.
5. The system produces contextually relevant answers based on the enhanced understanding of the content.


### Dependencies

- Beautiful Soup 4
- Requests
- LangChain
- Pinecone
- LLaMA2-7B (Large Language Model Meta AI)

### License

Apache 2.0 license

