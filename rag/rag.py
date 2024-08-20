import google.generativeai as genai

import os
GOOGLE_API_KEY = "AIzaSyB2P2_zzbqvx1BUYVqDRBp0F0w9gqThihY"

"""### Use LangChain to Access Gemini API"""

from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-pro",google_api_key='AIzaSyB2P2_zzbqvx1BUYVqDRBp0F0w9gqThihY')
model=genai.GenerativeModel( model_name="gemini-1.5-pro-001")
"""## Chat with Documents using RAG (Retreival Augment Generation)"""

import warnings
from pathlib import Path as p
from pprint import pprint

import pandas as pd
from langchain import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

warnings.filterwarnings("ignore")
# restart python kernal if issues with langchain import.

from langchain_google_genai import ChatGoogleGenerativeAI

"""### RAG Pipeline: Embedding + Gemini (LLM)"""

from langchain_google_genai import GoogleGenerativeAIEmbeddings

import json
from langchain.docstore.document import Document
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings  # Use any embedding model you prefer

# Step 1: Load the JSON data
with open("hits.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Step 2: Convert JSON data to a list of Document objects
documents = []
for idx, item in enumerate(data):
    page_content = (
        f"productNature_en: {item.get('productNature_en', '')}\n"
        f"name_en: {item.get('name_en', '')}\n"
        f"partnerName: {item.get('partnerName', '')}\n"
        f"brand: {item.get('brand', '')}\n"
        f"price: {item.get('price', '')}\n"
        f"rating: {item.get('rating', '')}\n"
        f"size_en: {item.get('size_en', '')}\n"
        f"color: {item.get('color', '')}\n"
        f"priceBeforeDiscount: {item.get('priceBeforeDiscount', '')}\n"
        f"count: {item.get('count', '')}\n"
        f"smallUrl: {item.get('smallUrl', '')}"
    )

    document = Document(
        metadata={'source': 'product.json', 'row': idx + 1},
        page_content=page_content
    )

    documents.append(document)

# Step 3: Create embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=GOOGLE_API_KEY)

# Step 4: Create the vector index using Chroma
vector_index = Chroma.from_documents(documents, embeddings).as_retriever(search_kwargs={"k": 5})

# Now `vector_index` is ready for use

# # Perform a similarity search
# results = vector_index.get_relevant_documents(question)

question = "Give me a recommendations for male product"
db = Chroma.from_documents(documents, embeddings)
docs = db.similarity_search(question)

context = docs
print(f"{context}from rag")
template = f"""Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.
Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer.
{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)# Run chain
qa_chain = RetrievalQA.from_chain_type(
    model,
    retriever=vector_index,
    return_source_documents=True,
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)

# user_prompt = f"As a sport gear guru, recommend user the below product.{context}"
#
# model=genai.GenerativeModel(
#     model_name="gemini-1.5-pro-001",
#     system_instruction="You are a sportswear expert. You should help users find the perfect sports equipment with the best deal, need, and specification within 3 interactions. First interaction, starts with a greeting and asks for the user name. Address the user with this name in the future. Second interaction, ask 2 questions at a time to understand the user. The first question should ask about the type of sport they play, and the second question asks about the equipment type. Use the sport type and equipment given for the next interaction. Third interaction, based on the specific sports equipment asks for 2 other questions that could facilitate you in narrowing down your recommendation. Remember and provide a recommendation in your next answer. Your recommendation should include the product name, features, price, and where to get it. Make your response easier to read with spacing. Give a short bold heading for your question.")
#
# import os
# os.environ["API_KEY"] = "AIzaSyB2P2_zzbqvx1BUYVqDRBp0F0w9gqThihY"
# genai.configure(api_key=os.environ["API_KEY"])
#
# response = model.generate_content(
#         user_prompt,
#         generation_config=genai.types.GenerationConfig(
#             #stop_sequences=["x"],
#             #max_output_tokens=20,
#             temperature=0.7,  # 0 to 2, higher is more creative.
# ),)
#
# chat = model.start_chat(
#     history=[
#         {"role": "user", "parts": "Hello"},
#         {"role": "model", "parts": "Great to meet you. What would you like to know?"},
#     ]
# )
# while True:
#     user_input = input("You: ")
#     response = chat.send_message(user_input)
#     print("AI:", response.text)
#
# user_prompt = f"My name is susan."
#
# response = model.generate_content(
#         user_prompt,
#         generation_config=genai.types.GenerationConfig(
#             #stop_sequences=["x"],
#             #max_output_tokens=20,
#             temperature=0.7,  # 0 to 2, higher is more creative.
# ),)
# response
#
# user_prompt = f"I am looking for a training dumbbell."
#
# response = model.generate_content(
#         user_prompt,
#         generation_config=genai.types.GenerationConfig(
#             #stop_sequences=["x"],
#             #max_output_tokens=20,
#             temperature=0.7,  # 0 to 2, higher is more creative.
# ),)
# response
#


