from fastapi import FastAPI
from app.api.v1.endpoints import router
from app.core.config import settings

# 1. Initialize the App
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="A Production-Ready RAG API with Multi-User Support"
)

# 2. Include the Router
# This tells the app: "All routes defined in endpoints.py start with /api/v1"
app.include_router(router, prefix="/api/v1")

# 3. Health Check (Optional but good for deployment)
@app.get("/")
def health_check():
    return {"status": "System is running", "docs_url": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)