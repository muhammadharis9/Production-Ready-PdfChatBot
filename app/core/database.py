import os
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings

def get_embeddings():

    return GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", 
        google_api_key=settings.GOOGLE_API_KEY
    )

def get_vector_store(session_id: str):

    user_db_path = os.path.join(settings.CHROMA_DB_DIR, session_id)
    
    vector_store = Chroma(
        persist_directory=user_db_path,
        embedding_function=get_embeddings()
    )
    
    return vector_store