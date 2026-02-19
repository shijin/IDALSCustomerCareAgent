from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_aws import BedrockEmbeddings
from faq_loader import load_faq_csv

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_PATH = os.path.join(BASE_DIR, "data", "idals_qna.csv")


_store = None

def get_vector_store(csv_path: str = CSV_PATH):
    global _store
    if _store:
        return _store

    docs = load_faq_csv(CSV_PATH)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=0
    )

    chunks = splitter.split_documents(docs)

    embeddings = BedrockEmbeddings(
        model_id="amazon.titan-embed-text-v2:0",
        region_name=os.getenv("AWS_REGION", "ap-south-1")
    )

    _store = FAISS.from_documents(chunks, embeddings)
    return _store
