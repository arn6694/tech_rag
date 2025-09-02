#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from enhanced_rag_system import EnhancedRAGSystem

class CheckmkRAGSystem(EnhancedRAGSystem):
    def __init__(self):
        import os
        base_dir = os.path.dirname(os.path.abspath(__file__))
        super().__init__(
            technology_name="checkmk",
            docs_dir=os.path.join(base_dir, "docs"),
            pdfs_dir=os.path.join(base_dir, "pdfs"), 
            chroma_db_path=os.path.join(base_dir, "vector_db"),
            collection_name="checkmk_docs"
        )
        # Use the mistral model you have installed
        self.model_name = "mistral:latest"

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Checkmk RAG System')
    parser.add_argument('--index', action='store_true', help='Index documents')
    parser.add_argument('--query', help='Single query mode')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode')
    parser.add_argument('--pdf-only', action='store_true', help='Search only PDF books')
    parser.add_argument('--web-only', action='store_true', help='Search only web docs')
    
    args = parser.parse_args()
    
    rag = CheckmkRAGSystem()
    
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
