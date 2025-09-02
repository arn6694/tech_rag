# Quick Start Guide - Red Hat Knowledge RAG System

## 🚀 5-Minute Setup

### 1. Activate Environment
```bash
cd /home/brian/redhat-knowledge
source shared-env/bin/activate
```

### 2. Check Status
```bash
./control_system.sh
# Press 'h' for health check
# Press 'x' to exit
```

### 3. Test Bash System (Already Working!)
```bash
python3 bash/rag_system.py --query "How do I create a bash script?" --pdf-only
```

## 🎯 Common Tasks

### Ask Questions
```bash
# Interactive mode
python3 bash/rag_system.py --interactive

# Single question
python3 bash/rag_system.py --query "How do I use grep?" --pdf-only
```

### Index New Content
```bash
# Index bash books (already done)
python3 bash/rag_system.py --index

# Index other technologies
python3 python/rag_system.py --index
python3 rhel/rag_system.py --index
```

### Start API Servers
```bash
# Start all API servers
./control_system.sh
# Press 'a' then '9' for all systems

# Or start individual servers
python3 bash/api_server.py      # Port 8006
python3 python/api_server.py    # Port 8004
```

### Add New Books
```bash
# 1. Copy books to ~/books/
cp new_book.pdf ~/books/

# 2. Organize them
python3 organize_all_books.py

# 3. Index the new content
python3 <technology>/rag_system.py --index
```

## 🔧 Management Commands

| Command | What it does |
|---------|--------------|
| `./control_system.sh` | Main menu - manage everything |
| `python3 <tech>/rag_system.py --interactive` | Chat with a technology |
| `python3 <tech>/rag_system.py --index` | Index documents |
| `python3 <tech>/api_server.py` | Start API server |
| `python3 organize_all_books.py` | Organize new books |

## 🌐 Open WebUI Integration

1. **Start API servers:**
   ```bash
   ./control_system.sh
   # Press 'a' then '9'
   ```

2. **Add to Open WebUI:**
   - Bash: `http://localhost:8006`
   - Python: `http://localhost:8004`
   - RHEL: `http://localhost:8003`
   - Ansible: `http://localhost:8001`
   - CheckMK: `http://localhost:8002`

## 🆘 Troubleshooting

**"No relevant documentation found"**
```bash
python3 bash/rag_system.py --index
```

**"Error connecting to Ollama"**
```bash
ollama serve
ollama pull mistral:latest
```

**"Module not found"**
```bash
source shared-env/bin/activate
```

## 📊 What's Working Now

✅ **Bash System**: 4,658 indexed chunks from 5 books  
✅ **All 8 Technologies**: Ready to use  
✅ **EPUB Processing**: Fixed and working  
✅ **Book Organization**: 14 books categorized  
✅ **API Servers**: Ready for Open WebUI  

## 🎯 Next Steps

1. **Test other technologies:**
   ```bash
   python3 python/rag_system.py --index
   python3 python/rag_system.py --query "How do I use lists?" --pdf-only
   ```

2. **Set up Open WebUI integration**

3. **Configure automatic updates:**
   ```bash
   ./control_system.sh
   # Press 'c' to configure cron jobs
   ```

**You're ready to go! 🚀**
