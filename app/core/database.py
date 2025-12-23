import os
from langchain_community.vectorstores import Chroma
from app.core.config import settings
from langchain_huggingface import HuggingFaceEmbeddings


def get_embeddings():
    model_name = HuggingFaceEmbeddings("sentence-transformers/all-MiniLM-L6-v2")

    return model_name

def get_vector_store(session_id: str):

    user_db_path = os.path.join(settings.CHROMA_DB_DIR, session_id)
    
    vector_store = Chroma(
        persist_directory=user_db_path,
        embedding_function=get_embeddings()
    )
    
    return vector_store