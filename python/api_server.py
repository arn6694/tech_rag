#!/usr/bin/env python3
"""
Python RAG API Server for OpenWebUI Integration
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import logging
import sys
import os

# Add shared directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from enhanced_rag_system import EnhancedRAGSystem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Python RAG API", version="1.0.0")

# Initialize RAG pipeline
rag_pipeline = None

class QueryRequest(BaseModel):
    query: str
    max_results: Optional[int] = 5

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    context_chunks: int

@app.on_event("startup")
async def startup_event():
    global rag_pipeline
    logger.info("Initializing Python RAG pipeline...")
    rag_pipeline = EnhancedRAGSystem(
        technology_name="python",
        docs_dir="docs",
        pdfs_dir="pdfs", 
        chroma_db_path="vector_db",
        collection_name="python_docs"
    )
    logger.info("Python RAG API ready!")

@app.get("/")
async def root():
    return {"message": "Python RAG API is running", "technology": "Python Programming"}

@app.get("/health")
async def health_check():
    if rag_pipeline is None:
        raise HTTPException(status_code=503, detail="RAG pipeline not initialized")
    
    # Check if we have documents indexed
    doc_count = rag_pipeline.collection.count()
    
    return {
        "status": "healthy",
        "technology": "Python",
        "documents_indexed": doc_count,
        "ollama_url": rag_pipeline.ollama_base_url,
        "model": rag_pipeline.model_name
    }

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    if rag_pipeline is None:
        raise HTTPException(status_code=503, detail="RAG pipeline not initialized")
    
    try:
        # Get answer using RAG pipeline
        answer = rag_pipeline.answer_question(request.query)
        
        # Get context for metadata
        context_chunks = rag_pipeline.retrieve_relevant_context(request.query, request.max_results)
        
        # Extract sources
        sources = []
        for chunk in context_chunks:
            if chunk['metadata'].get('source_type') == 'pdf':
                source_info = f"📖 {chunk['metadata']['filename']}"
            else:
                source_info = f"🌐 {chunk['metadata']['title']} - {chunk['metadata']['url']}"
            if source_info not in sources:
                sources.append(source_info)
        
        return QueryResponse(
            answer=answer,
            sources=sources,
            context_chunks=len(context_chunks)
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.post("/retrieve")
async def retrieve_context(request: QueryRequest):
    """Retrieve relevant context without generating answer - useful for debugging"""
    if rag_pipeline is None:
        raise HTTPException(status_code=503, detail="RAG pipeline not initialized")
    
    try:
        context_chunks = rag_pipeline.retrieve_relevant_context(request.query, request.max_results)
        
        return {
            "query": request.query,
            "technology": "Python",
            "chunks_found": len(context_chunks),
            "context": [
                {
                    "content": chunk['content'][:200] + "...",  # Truncate for API response
                    "source": chunk['metadata']['source'],
                    "title": chunk['metadata']['title'],
                    "url": chunk['metadata'].get('url', ''),
                    "source_type": chunk['metadata'].get('source_type', 'unknown')
                }
                for chunk in context_chunks
            ]
        }
        
    except Exception as e:
        logger.error(f"Error retrieving context: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving context: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
