from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from app.core.database import get_vector_store
from app.core.config import settings

PROMPT_TEMPLATE = """
Answer the question as detailed as possible from the provided context. 
If the answer is not in the context, say "I don't know".

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
        model="gemini-1.5-flash", 
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
   