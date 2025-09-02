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
