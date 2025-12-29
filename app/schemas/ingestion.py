import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.database import get_vector_store
import shutil

def load_pdf(file_path):
    loader = PyPDFLoader(file_path=file_path)
    load = loader.load()
    return load

def splitting(load):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap= 100)

    splitted_text = text_splitter.split_documents(load)
    return splitted_text

async def process_pdf(file_path: str, session_id: str):
 
    documents = load_pdf(file_path)
    text_chunks = splitting(documents)
    
    vector_store = get_vector_store(session_id)

    vector_store.add_documents(text_chunks)
    
    return {
        "status": "Success", 
        "filename": os.path.basename(file_path),
        "chunks_processed": len(text_chunks)
    }


def embeds(splitted_text):
    embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
    embed = HuggingFaceEmbeddings(model_name=embedding_model)
    PERSIST_DIR = "./chroma_db"
    final_embed = Chroma.from_documents(
        documents=splitted_text,
        embedding_function=embed,
        collection_name="pdfs",
        persist_directory=PERSIST_DIR)
    
    return final_embed
    

