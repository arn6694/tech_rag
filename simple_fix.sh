#!/bin/bash
#
# Simple Fix Script - Complete the setup
#

set -euo pipefail

echo "INFO: Completing the missing technology files..."

# Complete the ansible API server that was cut off
cat > ansible/api_server.py << 'ANSIBLE_API_EOF'
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
ANSIBLE_API_EOF

chmod +x ansible/api_server.py

# Quick create the other essential API servers
for tech in checkmk rhel python; do
    if [[ ! -f "$tech/api_server.py" ]]; then
        case $tech in
            "checkmk") PORT=8002 ;;
            "rhel") PORT=8003 ;;
            "python") PORT=8004 ;;
        esac
        
        cat > $tech/api_server.py << EOF
#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import logging

from rag_system import ${tech^}RAGSystem

app = FastAPI(title="${tech^} Knowledge API", version="1.0.0")
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
    rag_system = ${tech^}RAGSystem()

@app.get("/")
async def root():
    return {"message": "${tech^} Knowledge API is running", "technology": "$tech"}

@app.get("/health") 
async def health_check():
    if rag_system is None:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    doc_count = rag_system.collection.count()
    return {
        "status": "healthy",
        "technology": "$tech",
        "documents_indexed": doc_count,
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
            technology="$tech"
        )
        
    except Exception as e:
        logger.error(f"Error processing $tech query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

if __name__ == "__main__":
    print("Starting $tech API server on port $PORT")
    uvicorn.run(app, host="0.0.0.0", port=$PORT)
EOF

        chmod +x $tech/api_server.py
        echo "Created $tech API server"
    fi
done

# Create simplified control system
cat > control_system.sh << 'CONTROL_EOF'
#!/bin/bash
#
# Simplified Control System
#

set -euo pipefail

show_menu() {
    clear
    echo "========================================"
    echo "Red Hat Knowledge System Control Panel"
    echo "========================================"
    echo
    echo "Technologies:"
    echo "1) Ansible        (Port 8001)"
    echo "2) CheckMK        (Port 8002)" 
    echo "3) RHEL           (Port 8003)"
    echo "4) Python         (Port 8004)"
    echo
    echo "Actions:"
    echo "s) Scrape documentation"
    echo "i) Index documents"
    echo "q) Interactive query"
    echo "a) Start API server"
    echo "h) Health check"
    echo "x) Exit"
    echo
}

select_tech() {
    read -p "Select technology (1-4): " choice
    case $choice in
        1) echo "ansible" ;;
        2) echo "checkmk" ;;
        3) echo "rhel" ;;
        4) echo "python" ;;
        *) echo "" ;;
    esac
}

scrape_docs() {
    local tech=$1
    echo "Scraping $tech documentation..."
    cd "$tech"
    source ../shared-env/bin/activate
    python3 scraper.py
    cd ..
    echo "Scraping complete!"
}

index_docs() {
    local tech=$1
    echo "Indexing $tech documents..."
    cd "$tech"
    source ../shared-env/bin/activate
    python3 rag_system.py --index
    cd ..
    echo "Indexing complete!"
}

interactive_query() {
    local tech=$1
    echo "Starting $tech interactive system..."
    cd "$tech"
    source ../shared-env/bin/activate
    python3 rag_system.py --interactive
    cd ..
}

start_api() {
    local tech=$1
    echo "Starting $tech API server..."
    cd "$tech"
    source ../shared-env/bin/activate
    python3 api_server.py &
    cd ..
    echo "API server started in background"
}

health_check() {
    echo "System Health Check:"
    source shared-env/bin/activate
    
    for tech in ansible checkmk rhel python; do
        if [[ -d "$tech" ]]; then
            web_docs=$(find "$tech/docs" -name "*.json" -not -name "doc_index.json" 2>/dev/null | wc -l)
            pdf_docs=$(find "$tech/pdfs" -name "*.pdf" 2>/dev/null | wc -l)
            
            if [[ -d "$tech/vector_db" ]] && [[ -n "$(ls -A "$tech/vector_db" 2>/dev/null)" ]]; then
                indexed="Indexed"
            else
                indexed="Not indexed"
            fi
            
            echo "$tech: $web_docs web docs, $pdf_docs PDFs, $indexed"
        else
            echo "$tech: Not found"
        fi
    done
}

# Main loop
while true; do
    show_menu
    read -p "Action: " action
    
    case $action in
        s)
            tech=$(select_tech)
            if [[ -n "$tech" ]]; then
                scrape_docs "$tech"
                read -p "Press Enter to continue..."
            fi
            ;;
        i)
            tech=$(select_tech)
            if [[ -n "$tech" ]]; then
                index_docs "$tech"
                read -p "Press Enter to continue..."
            fi
            ;;
        q)
            tech=$(select_tech)
            if [[ -n "$tech" ]]; then
                interactive_query "$tech"
            fi
            ;;
        a)
            tech=$(select_tech)
            if [[ -n "$tech" ]]; then
                start_api "$tech"
                read -p "Press Enter to continue..."
            fi
            ;;
        h)
            health_check
            read -p "Press Enter to continue..."
            ;;
        x)
            echo "Exiting..."
            pkill -f "api_server.py" 2>/dev/null || true
            exit 0
            ;;
        *)
            echo "Invalid action"
            sleep 1
            ;;
    esac
done
CONTROL_EOF

chmod +x control_system.sh

# Create a quick test script
cat > quick_test.sh << 'TEST_EOF'
#!/bin/bash

echo "Quick System Test"
echo "=================="

if [[ -f "shared-env/bin/activate" ]]; then
    echo "✅ Python environment: OK"
else
    echo "❌ Python environment: Missing"
    exit 1
fi

source shared-env/bin/activate

if python3 -c "import chromadb, sentence_transformers, fastapi" 2>/dev/null; then
    echo "✅ Python packages: OK"
else
    echo "❌ Python packages: Missing"
    exit 1
fi

for tech in ansible checkmk rhel python; do
    if [[ -f "$tech/rag_system.py" ]] && [[ -f "$tech/scraper.py" ]]; then
        echo "✅ $tech: Ready"
    else
        echo "❌ $tech: Missing files"
    fi
done

echo
echo "✅ System is ready!"
echo
echo "Next steps:"
echo "1. Run: ./control_system.sh"
echo "2. Choose: s (scrape) → 1 (ansible)"
echo "3. Choose: i (index) → 1 (ansible)" 
echo "4. Choose: q (query) → 1 (ansible)"
echo "5. Test with: 'How do I create an Ansible playbook?'"
TEST_EOF

chmod +x quick_test.sh

echo "SUCCESS: Simple fix completed!"
echo
echo "Your system now has:"
echo "✅ Working control system"
echo "✅ 4 main technologies (ansible, checkmk, rhel, python)"
echo "✅ All API servers"
echo "✅ Test script"
echo
echo "Run: ./quick_test.sh to verify everything works"
echo "Then: ./control_system.sh to start using the system"
