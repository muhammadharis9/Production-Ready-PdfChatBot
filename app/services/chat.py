from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from app.core.database import get_vector_store
from app.core.config import settings

PROMPT_TEMPLATE = """
You are a knowledgeable and friendly assistant. 

DIRECTIONS:
1. If the user greets you (e.g., "Hi", "Hello") or asks a general question (e.g., "How are you?", "Who are you?"), answer naturally using your internal knowledge.
2. If the user asks a specific question about the provided context, prioritize the information in the context to answer.
3. If a question is specifically about the documents but the information is truly missing, tell the user you couldn't find it in the records, but offer a general helpful response if possible.

Context:
{context}

Question: 
{question}

Answer:
"""

def get_chat_response(query: str, session_id: str):

    vector_store = get_vector_store(session_id)
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=0.3, 
        google_api_key=settings.GOOGLE_API_KEY
    )

    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE, 
        input_variables=["context", "question"]
    )
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )

    response = qa_chain.invoke({"query": query})
    return response["result"]
   