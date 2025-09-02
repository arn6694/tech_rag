#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import logging

from rag_system import AnsibleRAGSystem

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Ansible Knowledge API", version="1.0.0")
rag_system = None

class QueryRequest(BaseModel):
    query: str
    max_results: Optional[int] = 5
    search_scope: Optional[str] = "all"

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    context_chunks: int
    technology: str

@app.on_event("startup")
async def startup_event():
    global rag_system
    logger.info("Initializing Ansible RAG system...")
    rag_system = AnsibleRAGSystem()
    logger.info("Ansible RAG API ready!")

@app.get("/")
async def root():
    return {"message": "Ansible Knowledge API is running", "technology": "ansible"}

@app.get("/health") 
async def health_check():
    if rag_system is None:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    doc_count = rag_system.collection.count()
    pdf_count = len(list(rag_system.pdfs_dir.glob('*.pdf'))) if rag_system.pdfs_dir.exists() else 0
    
    return {
        "status": "healthy",
        "technology": "ansible",
        "documents_indexed": doc_count,
        "pdf_books": pdf_count,
        "ollama_url": rag_system.ollama_base_url,
        "model": rag_system.model_name
    }

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    if rag_system is None:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        answer = rag_system.answer_question(request.query, search_scope=request.search_scope)
        context_chunks = rag_system.retrieve_relevant_context(request.query, request.max_results)
        
        sources = []
        for chunk in context_chunks:
            if chunk['metadata'].get('source_type') == 'pdf':
                source_info = f"📖 {chunk['metadata']['filename']}"
            else:
                source_info = f"🌐 {chunk['metadata']['title']}"
            
            if source_info not in sources:
                sources.append(source_info)
        
        return QueryResponse(
            answer=answer,
            sources=sources,
            context_chunks=len(context_chunks),
            technology="ansible"
        )
        
    except Exception as e:
        logger.error(f"Error processing Ansible query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

if __name__ == "__main__":
    print("Starting Ansible API server on port 8001")
    print("Add http://localhost:8001 as a knowledge source in Open WebUI")
    uvicorn.run(app, host="0.0.0.0", port=8001)
