# Troubleshooting Guide - Red Hat Knowledge RAG System

## 🚨 Common Issues & Solutions

### 1. "No relevant documentation found"

**Symptoms:**
```
No relevant bash documentation found for your question.
```

**Solutions:**
```bash
# Check if documents are indexed
python3 bash/rag_system.py --index

# Verify books are in the right place
ls bash/pdfs/

# Check vector database
ls bash/vector_db/
```

**Root Cause:** Documents haven't been indexed into the vector database.

---

### 2. "Error connecting to Ollama"

**Symptoms:**
```
Error: Could not connect to Ollama at http://localhost:11434
```

**Solutions:**
```bash
# Start Ollama service
ollama serve

# Check if Mistral model is installed
ollama list

# Install Mistral if missing
ollama pull mistral:latest

# Test Ollama connection
curl http://localhost:11434/api/tags
```

**Root Cause:** Ollama service not running or Mistral model not installed.

---

### 3. "Module not found" errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'chromadb'
```

**Solutions:**
```bash
# Activate the virtual environment
source shared-env/bin/activate

# Verify you're in the right directory
pwd  # Should show /home/brian/redhat-knowledge

# Check Python path
which python3
```

**Root Cause:** Virtual environment not activated.

---

### 4. API server won't start

**Symptoms:**
```
Address already in use
```

**Solutions:**
```bash
# Check what's using the port
netstat -tlnp | grep :8006

# Kill existing API servers
pkill -f api_server.py

# Start the server again
python3 bash/api_server.py
```

**Root Cause:** Port already in use by another process.

---

### 5. EPUB files not processing

**Symptoms:**
```
Successfully indexed 0 total chunks (0 web + 0 PDF)
```

**Solutions:**
```bash
# Check if EPUB files exist
ls bash/pdfs/*.epub

# Test EPUB processing manually
python3 -c "
import sys
sys.path.append('shared')
from enhanced_pdf_processor import EnhancedPDFProcessor
from pathlib import Path
processor = EnhancedPDFProcessor('bash')
result = processor.process_epub(Path('bash/pdfs/Bash Command Line and Shell Scripts Pocket Primer.epub'))
print(f'Success: {result[\"success\"]}')
"
```

**Root Cause:** EPUB processing issue or files not found.

---

### 6. Slow query responses

**Symptoms:**
- Queries take more than 10 seconds
- System becomes unresponsive

**Solutions:**
```bash
# Check system resources
htop

# Reduce chunk size in enhanced_rag_system.py
# Change chunk_size from 1500 to 1000

# Check vector database size
du -sh bash/vector_db/
```

**Root Cause:** Large vector database or insufficient system resources.

---

### 7. "Permission denied" errors

**Symptoms:**
```
PermissionError: [Errno 13] Permission denied
```

**Solutions:**
```bash
# Check file permissions
ls -la bash/

# Fix permissions
chmod +x bash/rag_system.py
chmod +x bash/api_server.py

# Check directory permissions
chmod 755 bash/
```

**Root Cause:** Incorrect file permissions.

---

### 8. Vector database corruption

**Symptoms:**
```
Error querying collection: ...
```

**Solutions:**
```bash
# Remove corrupted vector database
rm -rf bash/vector_db/*

# Recreate the database
python3 bash/rag_system.py --index
```

**Root Cause:** Corrupted ChromaDB files.

---

## 🔍 Diagnostic Commands

### System Health Check
```bash
# Check all systems
./control_system.sh
# Press 'h' for health check

# Check specific API
curl http://localhost:8006/health

# Check Ollama
curl http://localhost:11434/api/tags
```

### File System Check
```bash
# Check directory structure
find . -name "*.py" -type f | head -10

# Check book organization
ls -la */pdfs/

# Check vector databases
ls -la */vector_db/
```

### Process Check
```bash
# Check running API servers
ps aux | grep api_server.py

# Check Ollama process
ps aux | grep ollama

# Check port usage
netstat -tlnp | grep :800
```

### Log Analysis
```bash
# Check auto-update logs
tail -f auto_update.log

# Check book organization report
cat book_organization_report.json

# Check documentation update report
cat documentation_update_report.json
```

## 🛠️ Advanced Troubleshooting

### Memory Issues
```bash
# Monitor memory usage
htop

# Check Python memory usage
python3 -c "
import psutil
import os
process = psutil.Process(os.getpid())
print(f'Memory usage: {process.memory_info().rss / 1024 / 1024:.2f} MB')
"
```

### Performance Tuning
```bash
# Reduce chunk size for faster processing
# Edit shared/enhanced_rag_system.py
# Change chunk_size from 1500 to 1000

# Reduce batch size for lower memory usage
# Change batch_size from 100 to 50
```

### Network Issues
```bash
# Test web scraping
python3 -c "
import requests
response = requests.get('https://docs.checkmk.com/2.3/en/')
print(f'Status: {response.status_code}')
"

# Check DNS resolution
nslookup docs.checkmk.com
```

## 📊 Performance Benchmarks

### Expected Performance
- **Indexing**: 1-2 minutes per book
- **Query Response**: 2-5 seconds
- **Memory Usage**: 2-4GB during indexing
- **Storage**: ~100MB per book in vector database

### Performance Issues
If performance is below expectations:

1. **Check system resources:**
   ```bash
   free -h
   df -h
   ```

2. **Monitor during indexing:**
   ```bash
   htop
   ```

3. **Optimize settings:**
   - Reduce chunk size
   - Reduce batch size
   - Use smaller embedding model

## 🆘 Getting Help

### Self-Diagnosis Steps
1. Check this troubleshooting guide
2. Run health checks
3. Review log files
4. Test with simple queries
5. Verify system requirements

### Log Files to Check
- `auto_update.log` - Automated update logs
- `logs/<tech>_api.log` - API server logs
- `book_organization_report.json` - Book organization results
- `documentation_update_report.json` - Documentation update results

### System Requirements
- **OS**: Linux (Ubuntu/RHEL)
- **Python**: 3.12+
- **Memory**: 8GB+ recommended
- **Storage**: 10GB+ available
- **Network**: Internet access for web scraping

### Emergency Reset
If all else fails:

```bash
# Stop all services
pkill -f api_server.py
pkill -f ollama

# Remove all vector databases
rm -rf */vector_db/*

# Reinstall dependencies
source shared-env/bin/activate
pip install --upgrade -r requirements.txt

# Reindex everything
./control_system.sh
# Press 'i' then '9' for all systems
```

---

## 📞 Support Checklist

Before asking for help, please check:

- [ ] Virtual environment activated
- [ ] Ollama service running
- [ ] Mistral model installed
- [ ] Documents indexed
- [ ] System resources adequate
- [ ] Log files reviewed
- [ ] Health check run

**Most issues can be resolved by following this guide! 🚀**
