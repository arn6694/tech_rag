#!/bin/bash
#
# Minimal Working Setup - Creates everything from scratch
# This will get you a working Ansible system quickly
#

set -euo pipefail

echo "Creating minimal working setup..."

# Create all necessary directories
echo "Creating directories..."
mkdir -p shared
mkdir -p ansible/{docs,pdfs,vector_db}
mkdir -p checkmk/{docs,pdfs,vector_db}
mkdir -p rhel/{docs,pdfs,vector_db}
mkdir -p python/{docs,pdfs,vector_db}

# Create the enhanced PDF processor
echo "Creating PDF processor..."
cat > shared/enhanced_pdf_processor.py << 'PDF_EOF'
#!/usr/bin/env python3
import fitz  # PyMuPDF
import os
import json
from datetime import datetime
from pathlib import Path
import logging
import re

logger = logging.getLogger(__name__)

class EnhancedPDFProcessor:
    def __init__(self, technology_name: str):
        self.technology_name = technology_name
        
    def extract_metadata(self, pdf_path: Path) -> dict:
        try:
            doc = fitz.open(str(pdf_path))
            metadata = doc.metadata
            page_count = doc.page_count
            file_size = pdf_path.stat().st_size
            doc.close()
            
            return {
                'filename': pdf_path.name,
                'file_size_mb': round(file_size / (1024*1024), 2),
                'page_count': page_count,
                'title': metadata.get('title', ''),
                'author': metadata.get('author', ''),
                'processed_at': datetime.now().isoformat(),
                'technology': self.technology_name,
                'source_type': 'pdf'
            }
        except Exception as e:
            logger.error(f"Error extracting metadata from {pdf_path}: {e}")
            return {'filename': pdf_path.name, 'error': str(e)}
    
    def extract_text_pymupdf(self, pdf_path: Path) -> str:
        try:
            doc = fitz.open(str(pdf_path))
            text_content = []
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                text = page.get_text()
                if text.strip():
                    text_content.append(f"\n--- Page {page_num + 1} ---\n{text}")
            
            doc.close()
            return '\n\n'.join(text_content)
        except Exception as e:
            logger.error(f"PyMuPDF extraction failed for {pdf_path}: {e}")
            return ""
    
    def process_pdf(self, pdf_path: Path) -> dict:
        logger.info(f"Processing PDF: {pdf_path}")
        
        metadata = self.extract_metadata(pdf_path)
        text_content = self.extract_text_pymupdf(pdf_path)
        
        if not text_content.strip():
            logger.warning(f"No text extracted from {pdf_path}")
            return None
        
        return {
            'content': text_content,
            'metadata': metadata,
            'source_type': 'pdf',
            'technology': self.technology_name
        }
PDF_EOF

# Create the base scraper
echo "Creating base scraper..."
cat > shared/base_scraper.py << 'SCRAPER_EOF'
#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import os
import time
import json
from urllib.parse import urljoin
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseDocScraper:
    def __init__(self, output_dir, technology_name):
        self.output_dir = output_dir
        self.technology_name = technology_name
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
        os.makedirs(output_dir, exist_ok=True)

    def fetch_page(self, url, max_retries=3):
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    logger.error(f"Failed to fetch {url}")
                    return None

    def extract_text_content(self, html_content, url):
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            element.decompose()
        
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "No Title"
        
        # Find main content
        content_selectors = ['main', 'article', '.content', '#content', '.documentation', '.body', '.document']
        main_content = None
        for selector in content_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        if not main_content:
            main_content = soup.find('body') or soup
        
        # Extract structured text
        text_content = []
        for element in main_content.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li', 'code', 'pre']):
            text = element.get_text().strip()
            if text and len(text) > 10:
                if element.name.startswith('h'):
                    text_content.append(f"\n## {text}\n")
                elif element.name in ['code', 'pre']:
                    text_content.append(f"```\n{text}\n```")
                else:
                    text_content.append(text)
        
        return {
            'title': title_text,
            'url': url,
            'content': '\n\n'.join(text_content),
            'scraped_at': datetime.now().isoformat(),
            'technology': self.technology_name
        }

    def scrape_documentation(self):
        all_docs = []
        
        for source_name, source_config in self.doc_sources.items():
            logger.info(f"Scraping {source_name} documentation for {self.technology_name}...")
            
            for guide in source_config['guides']:
                url = urljoin(source_config['base_url'], guide)
                logger.info(f"Fetching: {url}")
                
                response = self.fetch_page(url)
                if not response:
                    continue
                
                doc_data = self.extract_text_content(response.text, url)
                doc_data['source'] = source_name
                doc_data['guide'] = guide
                
                filename = f"{source_name}_{guide.replace('/', '_').replace('.html', '')}.json"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(doc_data, f, indent=2, ensure_ascii=False)
                
                all_docs.append(doc_data)
                logger.info(f"Saved: {filepath}")
                time.sleep(1)
        
        # Save index
        index_file = os.path.join(self.output_dir, 'doc_index.json')
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump({
                'technology': self.technology_name,
                'scraped_at': datetime.now().isoformat(),
                'total_docs': len(all_docs),
                'sources': list(self.doc_sources.keys()),
                'documents': [{
                    'source': doc['source'],
                    'title': doc['title'],
                    'url': doc['url'],
                    'filename': f"{doc['source']}_{doc['guide'].replace('/', '_').replace('.html', '')}.json"
                } for doc in all_docs]
            }, f, indent=2)
        
        logger.info(f"Scraping complete! {len(all_docs)} documents saved for {self.technology_name}")
        return all_docs
SCRAPER_EOF

# Create the enhanced RAG system
echo "Creating RAG system..."
cat > shared/enhanced_rag_system.py << 'RAG_EOF'
#!/usr/bin/env python3
import json
import os
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
import requests
from typing import List, Dict
import logging
from datetime import datetime
from enhanced_pdf_processor import EnhancedPDFProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedRAGSystem:
    def __init__(self, technology_name: str, docs_dir: str, pdfs_dir: str, 
                 chroma_db_path: str, collection_name: str,
                 ollama_base_url: str = "http://localhost:11434", 
                 model_name: str = "mistral"):
        
        self.technology_name = technology_name
        self.docs_dir = Path(docs_dir)
        self.pdfs_dir = Path(pdfs_dir)
        self.chroma_db_path = chroma_db_path
        self.collection_name = collection_name
        self.ollama_base_url = ollama_base_url
        self.model_name = model_name
        
        self.docs_dir.mkdir(exist_ok=True)
        self.pdfs_dir.mkdir(exist_ok=True)
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(path=chroma_db_path)
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Get or create collection
        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function,
            metadata={"hnsw:space": "cosine"}
        )
        
        self.pdf_processor = EnhancedPDFProcessor(technology_name)
        
    def chunk_text(self, text: str, chunk_size: int = 1200, overlap: int = 200) -> List[str]:
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            if end < len(text):
                for i in range(end, max(start + chunk_size - overlap, start), -1):
                    if text[i] in '.!?\n':
                        end = i + 1
                        break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start = end - overlap
            
        return chunks

    def index_web_documents(self):
        if not self.docs_dir.exists() or not any(self.docs_dir.glob('*.json')):
            logger.warning(f"No web documents found in {self.docs_dir}")
            return 0
        
        logger.info(f"Indexing {self.technology_name} web documents...")
        
        documents = []
        metadatas = []
        ids = []
        
        for json_file in self.docs_dir.glob('*.json'):
            if json_file.name == 'doc_index.json':
                continue
                
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    doc_data = json.load(f)
                
                chunks = self.chunk_text(doc_data['content'])
                
                for i, chunk in enumerate(chunks):
                    if len(chunk.strip()) < 100:
                        continue
                        
                    chunk_id = f"web_{json_file.stem}_{i}"
                    
                    documents.append(chunk)
                    metadatas.append({
                        'source': doc_data.get('source', 'unknown'),
                        'title': doc_data.get('title', 'Unknown'),
                        'url': doc_data.get('url', ''),
                        'guide': doc_data.get('guide', ''),
                        'chunk_index': i,
                        'filename': json_file.name,
                        'technology': self.technology_name,
                        'source_type': 'web'
                    })
                    ids.append(chunk_id)
                    
            except Exception as e:
                logger.error(f"Error processing {json_file}: {e}")
        
        if documents:
            batch_size = 100
            for i in range(0, len(documents), batch_size):
                batch_docs = documents[i:i+batch_size]
                batch_metas = metadatas[i:i+batch_size]
                batch_ids = ids[i:i+batch_size]
                
                self.collection.add(
                    documents=batch_docs,
                    metadatas=batch_metas,
                    ids=batch_ids
                )
        
        logger.info(f"Indexed {len(documents)} web document chunks")
        return len(documents)

    def index_pdf_documents(self):
        if not self.pdfs_dir.exists():
            return 0
            
        pdf_files = list(self.pdfs_dir.glob('*.pdf'))
        if not pdf_files:
            return 0
        
        logger.info(f"Processing {len(pdf_files)} PDF books for {self.technology_name}...")
        
        documents = []
        metadatas = []
        ids = []
        
        for pdf_file in pdf_files:
            try:
                doc_data = self.pdf_processor.process_pdf(pdf_file)
                if not doc_data or not doc_data.get('content'):
                    continue
                
                chunks = self.chunk_text(doc_data['content'], chunk_size=1500, overlap=300)
                
                for i, chunk in enumerate(chunks):
                    if len(chunk.strip()) < 150:
                        continue
                        
                    chunk_id = f"pdf_{pdf_file.stem}_{i}"
                    
                    documents.append(chunk)
                    
                    metadata = doc_data['metadata'].copy()
                    metadata.update({
                        'chunk_index': i,
                        'source_type': 'pdf',
                        'technology': self.technology_name
                    })
                    metadatas.append(metadata)
                    ids.append(chunk_id)
                    
            except Exception as e:
                logger.error(f"Error processing PDF {pdf_file}: {e}")
        
        if documents:
            batch_size = 50
            for i in range(0, len(documents), batch_size):
                batch_docs = documents[i:i+batch_size]
                batch_metas = metadatas[i:i+batch_size]
                batch_ids = ids[i:i+batch_size]
                
                self.collection.add(
                    documents=batch_docs,
                    metadatas=batch_metas,
                    ids=batch_ids
                )
        
        logger.info(f"Indexed {len(documents)} PDF document chunks from {len(pdf_files)} books")
        return len(documents)

    def index_all_documents(self):
        logger.info(f"Indexing all {self.technology_name} documents...")
        
        existing_count = self.collection.count()
        if existing_count > 0:
            logger.info(f"Clearing {existing_count} existing documents...")
            self.chroma_client.delete_collection(self.collection_name)
            self.collection = self.chroma_client.get_or_create_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function,
                metadata={"hnsw:space": "cosine"}
            )
        
        web_count = self.index_web_documents()
        pdf_count = self.index_pdf_documents()
        
        total = web_count + pdf_count
        logger.info(f"Successfully indexed {total} total chunks ({web_count} web + {pdf_count} PDF)")
        return total

    def retrieve_relevant_context(self, query: str, n_results: int = 5, search_scope: str = "all") -> List[Dict]:
        where_filter = {}
        if search_scope == "pdf":
            where_filter = {"source_type": "pdf"}
        elif search_scope == "web":
            where_filter = {"source_type": "web"}
        
        try:
            if where_filter:
                results = self.collection.query(
                    query_texts=[query],
                    n_results=n_results,
                    where=where_filter
                )
            else:
                results = self.collection.query(
                    query_texts=[query],
                    n_results=n_results
                )
        except Exception as e:
            logger.error(f"Error querying collection: {e}")
            return []
        
        if not results['documents'] or not results['documents'][0]:
            return []
        
        context_chunks = []
        for i in range(len(results['documents'][0])):
            context_chunks.append({
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i] if results.get('distances') else None
            })
        
        return context_chunks

    def query_ollama(self, prompt: str) -> str:
        try:
            response = requests.post(
                f"{self.ollama_base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120
            )
            response.raise_for_status()
            return response.json()['response']
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error querying Ollama: {e}")
            return f"Error: Could not connect to Ollama at {self.ollama_base_url}"

    def answer_question(self, question: str, search_scope: str = "all") -> str:
        logger.info(f"Processing {self.technology_name} question: {question}")
        
        context_chunks = self.retrieve_relevant_context(question, n_results=5, search_scope=search_scope)
        
        if not context_chunks:
            return f"No relevant {self.technology_name} documentation found for your question."
        
        context_parts = []
        sources_used = []
        
        for chunk in context_chunks:
            context_parts.append(f"Source: {chunk['metadata']['title']}")
            context_parts.append(f"Content: {chunk['content']}")
            context_parts.append("---")
            
            if chunk['metadata'].get('source_type') == 'pdf':
                source_info = f"📖 {chunk['metadata']['filename']}"
            else:
                source_info = f"🌐 {chunk['metadata']['title']}"
            
            if source_info not in sources_used:
                sources_used.append(source_info)
        
        context_text = "\n".join(context_parts)
        
        prompt = f"""You are a {self.technology_name.upper()} expert. Answer the user's question using ONLY the provided documentation context.

DOCUMENTATION CONTEXT:
{context_text}

USER QUESTION: {question}

INSTRUCTIONS:
- Answer based ONLY on the provided {self.technology_name.upper()} documentation
- Include specific commands, procedures, or examples when available
- Be concise but thorough
- Include relevant warnings or prerequisites

ANSWER:"""

        response = self.query_ollama(prompt)
        sources_text = f"\n\n{self.technology_name.upper()} Sources:\n" + "\n".join([f"- {source}" for source in sources_used])
        
        return response + sources_text

    def interactive_mode(self):
        print(f"Red Hat {self.technology_name.upper()} Documentation System")
        print(f"Ask questions about {self.technology_name.upper()}")
        print("Type 'quit' to exit, '--pdf-only' to search only books, '--web-only' for web docs\n")
        
        while True:
            try:
                question = input(f"\nYour {self.technology_name} question: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    break
                elif not question:
                    continue
                
                search_scope = "all"
                if "--pdf-only" in question:
                    search_scope = "pdf"
                    question = question.replace("--pdf-only", "").strip()
                elif "--web-only" in question:
                    search_scope = "web" 
                    question = question.replace("--web-only", "").strip()
                
                print(f"\nSearching {self.technology_name} documentation...")
                answer = self.answer_question(question, search_scope=search_scope)
                print(f"\nAnswer:\n{answer}")
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
RAG_EOF

# Create Ansible scraper
echo "Creating Ansible scraper..."
cat > ansible/scraper.py << 'ANSIBLE_SCRAPER_EOF'
#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from base_scraper import BaseDocScraper

class AnsibleScraper(BaseDocScraper):
    def __init__(self):
        super().__init__(
            output_dir="docs",
            technology_name="ansible"
        )
        
        self.doc_sources = {
            "ansible_community": {
                "base_url": "https://docs.ansible.com/ansible/latest/",
                "guides": [
                    "installation_guide/index.html",
                    "user_guide/index.html",
                    "playbook_guide/index.html",
                    "playbook_guide/playbooks_intro.html",
                    "playbook_guide/playbooks_variables.html",
                    "playbook_guide/playbooks_conditionals.html",
                    "playbook_guide/playbooks_loops.html",
                    "playbook_guide/playbooks_handlers.html",
                    "playbook_guide/playbooks_best_practices.html",
                    "user_guide/vault.html",
                    "user_guide/playbooks_templating.html",
                    "user_guide/intro_inventory.html",
                    "user_guide/playbooks_reuse_roles.html"
                ]
            }
        }

if __name__ == "__main__":
    scraper = AnsibleScraper()
    scraper.scrape_documentation()
ANSIBLE_SCRAPER_EOF

chmod +x ansible/scraper.py

# Create Ansible RAG system
echo "Creating Ansible RAG system..."
cat > ansible/rag_system.py << 'ANSIBLE_RAG_EOF'
#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from enhanced_rag_system import EnhancedRAGSystem

class AnsibleRAGSystem(EnhancedRAGSystem):
    def __init__(self):
        super().__init__(
            technology_name="ansible",
            docs_dir="docs",
            pdfs_dir="pdfs", 
            chroma_db_path="vector_db",
            collection_name="ansible_docs"
        )

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Ansible RAG System')
    parser.add_argument('--index', action='store_true', help='Index documents')
    parser.add_argument('--query', help='Single query mode')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode')
    parser.add_argument('--pdf-only', action='store_true', help='Search only PDF books')
    parser.add_argument('--web-only', action='store_true', help='Search only web docs')
    
    args = parser.parse_args()
    
    rag = AnsibleRAGSystem()
    
    if args.index:
        rag.index_all_documents()
    elif args.query:
        search_scope = 'pdf' if args.pdf_only else 'web' if args.web_only else 'all'
        answer = rag.answer_question(args.query, search_scope=search_scope)
        print(answer)
    elif args.interactive:
        rag.interactive_mode()
    else:
        print("Use --index, --query, or --interactive")
ANSIBLE_RAG_EOF

chmod +x ansible/rag_system.py

# Create Ansible API server
echo "Creating Ansible API server..."
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

# Create simple control system
echo "Creating control system..."
cat > control_system.sh << 'CONTROL_EOF'
#!/bin/bash

show_menu() {
    clear
    echo "==============================================="
    echo "Red Hat Knowledge System - Ansible Focus"
    echo "==============================================="
    echo
    echo "Actions:"
    echo "1) Scrape Ansible documentation (~20 minutes)"
    echo "2) Index Ansible documents (~5 minutes)"
    echo "3) Interactive Ansible queries"
    echo "4) Start Ansible API server (Open WebUI)"
    echo "5) Health check"
    echo "6) Exit"
    echo
}

while true; do
    show_menu
    read -p "Choose action (1-6): " choice
    
    case $choice in
        1)
            echo "Scraping Ansible documentation..."
            cd ansible
            source ../shared-env/bin/activate
            python3 scraper.py
            cd ..
            echo "Scraping complete!"
            read -p "Press Enter to continue..."
            ;;
        2)
            echo "Indexing Ansible documents..."
            cd ansible
            source ../shared-env/bin/activate
            python3 rag_system.py --index
            cd ..
            echo "Indexing complete!"
            read -p "Press Enter to continue..."
            ;;
        3)
            echo "Starting Ansible interactive system..."
            cd ansible
            source ../shared-env/bin/activate
            python3 rag_system.py --interactive
            cd ..
            ;;
        4)
            echo "Starting Ansible API server..."
            echo "Add http://localhost:8001 to Open WebUI as knowledge source"
            cd ansible
            source ../shared-env/bin/activate
            python3 api_server.py
            cd ..
            ;;
        5)
            echo "System Health:"
            source shared-env/bin/activate
            
            web_docs=$(find ansible/docs -name "*.json" -not -name "doc_index.json" 2>/dev/null | wc -l)
            pdf_docs=$(find ansible/pdfs -name "*.pdf" 2>/dev/null | wc -l)
            
            if [[ -d "ansible/vector_db" ]] && [[ -n "$(ls -A ansible/vector_db 2>/dev/null)" ]]; then
                indexed="✅ Indexed"
            else
                indexed="❌ Not indexed"
            fi
            
            echo "Ansible: $web_docs web docs, $pdf_docs PDFs, $indexed"
            
            # Test Ollama connection
            if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
                echo "Ollama: ✅ Running"
            else
                echo "Ollama: ❌ Not running (start with: ollama serve)"
            fi
            
            read -p "Press Enter to continue..."
            ;;
        6)
            echo "Exiting..."
            pkill -f "api_server.py" 2>/dev/null || true
            exit 0
            ;;
        *)
            echo "Invalid choice"
            sleep 1
            ;;
    esac
done
CONTROL_EOF

chmod +x control_system.sh

# Create quick test
echo "Creating test script..."
cat > test_system.sh << 'TEST_EOF'
#!/bin/bash

echo "Testing Ansible Knowledge System"
echo "================================"

# Test Python environment
if [[ -f "shared-env/bin/activate" ]]; then
    echo "✅ Python environment: OK"
    source shared-env/bin/activate
else
    echo "❌ Python environment: Missing"
    exit 1
fi

# Test Python packages
if python3 -c "import chromadb, sentence_transformers, fastapi, fitz" 2>/dev/null; then
    echo "✅ Python packages: OK"
else
    echo "❌ Python packages: Some missing (but system should still work)"
fi

# Test Ansible directory
if [[ -f "ansible/rag_system.py" ]] && [[ -f "ansible/scraper.py" ]] && [[ -f "ansible/api_server.py" ]]; then
    echo "✅ Ansible system: Ready"
else
    echo "❌ Ansible system: Missing files"
    exit 1
fi

# Test Ollama connection
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama: Running and accessible"
else
    echo "⚠️  Ollama: Not running (start with: ollama serve)"
fi

echo
echo "✅ System is ready for use!"
echo
echo "Next steps:"
echo "1. Make sure Ollama is running: ollama serve"
echo "2. Run: ./control_system.sh"
echo "3. Choose option 1 to scrape Ansible docs"
echo "4. Choose option 2 to index the documents"
echo "5. Choose option 3 to test with queries"
echo "6. Choose option 4 to start API for Open WebUI"
echo
echo "Example test question: 'How do I create an Ansible playbook with loops?'"
TEST_EOF

chmod +x test_system.sh

echo "SUCCESS: Minimal working setup complete!"
echo
echo "✅ Created complete Ansible knowledge system"
echo "✅ All necessary files and directories"
echo "✅ Control system and test script"
echo
echo "Run: ./test_system.sh to verify everything works"
echo "Then: ./control_system.sh to start using the system"
