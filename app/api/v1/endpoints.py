from fastapi import APIRouter, Form, File, UploadFile, HTTPException
import shutil
import os
from app.schemas.ingestion import process_pdf
from app.services.chat import get_chat_response

router = APIRouter()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...), 
    session_id: str = Form(...) 
):

    temp_filename = f"temp_{file.filename}"
    
    try:
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        result = await process_pdf(temp_filename, session_id)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

@router.post("/chat")
async def chat_endpoint(
    question: str = Form(...), 
    session_id: str = Form(...)
):

    
    answer = get_chat_response(question, session_id)
    return {"answer": answer}
    