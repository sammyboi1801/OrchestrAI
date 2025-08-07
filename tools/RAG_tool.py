from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path
from langchain.tools.retriever import create_retriever_tool
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

# db_location = Path("../resources")
db_location = Path("D:/Python Projects/AgenticAI + FastAPI2/resources")

files = [f.name for f in db_location.iterdir() if f.is_file() and f.suffix in ['.pdf', '.csv']]

pdf_docs = []
csv_docs = []

for file in files:
    if file.endswith('.pdf'):
        pdf_loader = PyPDFLoader(f"{db_location}/{file}")
        pdf_docs.extend(pdf_loader.load())
    elif file.endswith('.csv'):
        csv_loader = CSVLoader(f"{db_location}/{file}")
        csv_docs.extend(csv_loader.load())

documents = pdf_docs + csv_docs
# print(documents)

# Split documents into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
split_docs = splitter.split_documents(documents)
# print(split_docs)

# embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-exp-03-07")
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

# Store in ChromaDB
vector_store = Chroma.from_documents(
    documents=split_docs,
    embedding=embeddings,
    persist_directory=str(db_location)
)

retriever = vector_store.as_retriever(search_kwargs={"k": 5})

# Define RAG Tool
RAG_RETRIEVER_TOOL = create_retriever_tool(
    retriever,
    name="retrieval_tool",
    description="Use this tool to retrieve relevant information from the knowledge base to help answer complex or factual questions."
)
