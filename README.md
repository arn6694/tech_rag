# Red Hat Knowledge RAG System

A comprehensive Retrieval-Augmented Generation (RAG) system for managing and querying technical documentation across 8 technology domains: Ansible, CheckMK, RHEL, Python, Bash, PowerShell, Containers, and Cybersecurity.

## 🚀 Quick Start

### 1. Activate the Environment
```bash
cd /home/brian/redhat-knowledge
source shared-env/bin/activate
```

### 2. Check System Status
```bash
./control_system.sh
```

### 3. Test a Query
```bash
python3 bash/rag_system.py --query "How do I create a bash script?" --pdf-only
```

## 📋 System Overview

### Technology Modules
- **🚀 Ansible** (Port 8001) - Automation and playbook development
- **📊 CheckMK** (Port 8002) - Monitoring and alerting (Version 2.3)
- **🐧 RHEL** (Port 8003) - Red Hat Enterprise Linux administration
- **🐍 Python** (Port 8004) - Python programming and development
- **🔒 Cybersecurity** (Port 8005) - Security practices and tools
- **📜 Bash** (Port 8006) - Shell scripting and automation
- **💻 PowerShell** (Port 8007) - Windows automation and scripting
- **📦 Containers** (Port 8008) - Docker and Podman containerization

### Knowledge Sources
- **PDF Books**: 14+ technical books automatically categorized
- **Web Documentation**: Scraped from official sources
- **Vector Database**: ChromaDB for semantic search
- **AI Model**: Mistral via Ollama for response generation

## 🎯 Usage Guide

### Interactive Mode
Start an interactive session for any technology:

```bash
# Bash scripting help
python3 bash/rag_system.py --interactive

# Python programming help
python3 python/rag_system.py --interactive

# RHEL administration help
python3 rhel/rag_system.py --interactive
```

### Single Query Mode
Ask specific questions:

```bash
# Search only PDF books
python3 bash/rag_system.py --query "How do I use grep?" --pdf-only

# Search only web documentation
python3 ansible/rag_system.py --query "How do I create a playbook?" --web-only

# Search all sources (default)
python3 rhel/rag_system.py --query "How do I configure networking?"
```

### API Server Mode
Start API servers for Open WebUI integration:

```bash
# Start individual API servers
python3 bash/api_server.py      # http://localhost:8006
python3 python/api_server.py    # http://localhost:8004
python3 rhel/api_server.py      # http://localhost:8003

# Or use the control system
./control_system.sh
# Choose option 'a' for API servers
```

## 🔧 Management Commands

### Control System
The main management interface:

```bash
./control_system.sh
```

**Available Actions:**
- `s` - Scrape documentation from web sources
- `i` - Index documents into vector database
- `q` - Interactive queries
- `a` - Start API servers
- `h` - Health check
- `p` - Organize PDF books
- `c` - Configure cron jobs
- `x` - Exit

### Health Check
Monitor system status:

```bash
./control_system.sh
# Choose option 'h'
```

Shows:
- Document counts per technology
- Vector database status
- API server status
- System resources

### Indexing Documents
Index new or updated content:

```bash
# Index specific technology
python3 bash/rag_system.py --index

# Index all technologies via control system
./control_system.sh
# Choose option 'i'
```

## 📚 Content Management

### Adding New Books
1. Place PDF/EPUB files in `~/books/`
2. Run the organizer:
   ```bash
   python3 organize_all_books.py
   ```
3. Index the new content:
   ```bash
   python3 <technology>/rag_system.py --index
   ```

### Updating Documentation
Update web documentation sources:

```bash
# Update all documentation sources
python3 update_documentation_sources.py

# Scrape updated content
./control_system.sh
# Choose option 's' for scraping
```

### Organizing Books
The system automatically categorizes books by content:

```bash
python3 organize_all_books.py
```

**Supported Categories:**
- Ansible, CheckMK, RHEL, Python
- Bash, PowerShell, Containers
- Cybersecurity, Linux General, AI/ML

## 🌐 Open WebUI Integration

### Setup Open WebUI
1. Start API servers:
   ```bash
   ./control_system.sh
   # Choose option 'a' -> 'all systems'
   ```

2. Add knowledge sources in Open WebUI:
   - **Bash**: `http://localhost:8006`
   - **Python**: `http://localhost:8004`
   - **RHEL**: `http://localhost:8003`
   - **Ansible**: `http://localhost:8001`
   - **CheckMK**: `http://localhost:8002`
   - **Cybersecurity**: `http://localhost:8005`
   - **PowerShell**: `http://localhost:8007`
   - **Containers**: `http://localhost:8008`

### API Endpoints
Each technology provides REST API endpoints:

- `GET /` - Service status
- `GET /health` - Health check
- `POST /query` - Query the knowledge base
- `POST /retrieve` - Retrieve context without generation

**Example API Usage:**
```bash
curl -X POST http://localhost:8006/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I create a bash script?", "max_results": 5}'
```

## 🔄 Automation

### Cron Jobs
Set up automatic updates:

```bash
./control_system.sh
# Choose option 'c'
```

This configures:
- **Weekly**: Documentation scraping
- **Daily**: Content indexing
- **Logging**: All activities to `auto_update.log`

### Manual Updates
```bash
# Update specific technology
cd ansible
source ../shared-env/bin/activate
python3 scraper.py
python3 rag_system.py --index

# Update all technologies
./auto_update.sh
```

## 🛠️ Troubleshooting

### Common Issues

**"No relevant documentation found"**
- Check if documents are indexed: `python3 <tech>/rag_system.py --index`
- Verify books are in correct directories
- Check vector database: `ls <tech>/vector_db/`

**"Error connecting to Ollama"**
- Start Ollama: `ollama serve`
- Check model availability: `ollama list`
- Install Mistral: `ollama pull mistral:latest`

**"Module not found" errors**
- Activate environment: `source shared-env/bin/activate`
- Check Python path: `echo $PYTHONPATH`

**API server won't start**
- Check port availability: `netstat -tlnp | grep :800`
- Kill existing processes: `pkill -f api_server.py`
- Check logs: `tail -f logs/<tech>_api.log`

### Log Files
- **Auto updates**: `auto_update.log`
- **API servers**: `logs/<tech>_api.log`
- **Book organization**: `book_organization_report.json`
- **Documentation updates**: `documentation_update_report.json`

### Performance Tuning
- **Chunk size**: Modify in `shared/enhanced_rag_system.py`
- **Embedding model**: Change in `shared/enhanced_rag_system.py`
- **Batch size**: Adjust in indexing methods
- **Memory usage**: Monitor with `htop` during indexing

## 📊 System Architecture

### Components
```
redhat-knowledge/
├── shared/                    # Shared libraries
│   ├── enhanced_rag_system.py # Core RAG functionality
│   ├── enhanced_pdf_processor.py # PDF/EPUB processing
│   └── pdf_categorizer.py     # Book categorization
├── <technology>/              # Technology modules
│   ├── scraper.py            # Web documentation scraper
│   ├── rag_system.py         # RAG system implementation
│   ├── api_server.py         # REST API server
│   ├── docs/                 # Scraped web documentation
│   ├── pdfs/                 # PDF/EPUB books
│   └── vector_db/            # ChromaDB vector database
├── shared-env/               # Python virtual environment
├── control_system.sh         # Main management interface
└── auto_update.sh           # Automated update script
```

### Data Flow
1. **Content Ingestion**: Books → Categorization → PDFs directory
2. **Web Scraping**: Documentation sites → JSON files → Docs directory
3. **Processing**: PDFs/EPUBs → Text extraction → Chunking
4. **Indexing**: Chunks → Embeddings → ChromaDB
5. **Querying**: User question → Vector search → Context → LLM → Answer

## 🔐 Security Considerations

### Access Control
- API servers bind to `0.0.0.0` (all interfaces)
- Consider firewall rules for production
- Use reverse proxy (nginx) for HTTPS

### Data Privacy
- All processing happens locally
- No data sent to external services (except Ollama)
- Vector databases stored locally

### Backup Strategy
- Backup `vector_db/` directories
- Backup `pdfs/` and `docs/` directories
- Backup configuration files

## 📈 Monitoring

### System Metrics
- Document counts per technology
- Vector database sizes
- API response times
- Memory and CPU usage

### Health Monitoring
```bash
# Check all systems
./control_system.sh
# Choose option 'h'

# Check specific API
curl http://localhost:8006/health

# Monitor logs
tail -f auto_update.log
```

## 🆘 Support

### Getting Help
1. Check this documentation
2. Review log files
3. Run health checks
4. Test with simple queries

### System Requirements
- **OS**: Linux (tested on Ubuntu/RHEL)
- **Python**: 3.12+
- **Memory**: 8GB+ recommended
- **Storage**: 10GB+ for books and vector databases
- **Dependencies**: Ollama, ChromaDB, sentence-transformers

### Performance Expectations
- **Indexing**: ~1-2 minutes per book
- **Query Response**: 2-5 seconds
- **Memory Usage**: 2-4GB during indexing
- **Storage**: ~100MB per book in vector database

---

## 🎯 Quick Reference

| Command | Purpose |
|---------|---------|
| `./control_system.sh` | Main management interface |
| `python3 <tech>/rag_system.py --interactive` | Interactive query mode |
| `python3 <tech>/rag_system.py --index` | Index documents |
| `python3 <tech>/api_server.py` | Start API server |
| `python3 organize_all_books.py` | Organize new books |
| `python3 update_documentation_sources.py` | Update doc sources |

**Happy querying! 🚀**
