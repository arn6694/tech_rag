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
            
        pdf_files = list(self.pdfs_dir.glob('*.pdf')) + list(self.pdfs_dir.glob('*.epub'))
        if not pdf_files:
            return 0
        
        logger.info(f"Processing {len(pdf_files)} PDF books for {self.technology_name}...")
        
        documents = []
        metadatas = []
        ids = []
        
        for pdf_file in pdf_files:
            try:
                # Handle both PDF and EPUB files
                if pdf_file.suffix.lower() == '.epub':
                    doc_data = self.pdf_processor.process_epub(pdf_file)
                else:
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
