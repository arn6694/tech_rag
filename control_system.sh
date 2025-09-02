#!/bin/bash

# Red Hat Knowledge System Control Script
# Complete 8-Technology Management System

# Color codes for better UI
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Technology configuration
declare -A TECH_PORTS=(
    ["ansible"]="8001"
    ["checkmk"]="8002"
    ["rhel"]="8003"
    ["python"]="8004"
    ["cybersecurity"]="8005"
    ["bash"]="8006"
    ["powershell"]="8007"
    ["containers"]="8008"
)

declare -A TECH_NAMES=(
    ["ansible"]="Ansible"
    ["checkmk"]="CheckMK"
    ["rhel"]="RHEL"
    ["python"]="Python"
    ["cybersecurity"]="Cybersecurity"
    ["bash"]="Bash"
    ["powershell"]="PowerShell"
    ["containers"]="Containers"
)

declare -A TECH_ICONS=(
    ["ansible"]="🚀"
    ["checkmk"]="📊"
    ["rhel"]="🐧"
    ["python"]="🐍"
    ["cybersecurity"]="🔒"
    ["bash"]="📜"
    ["powershell"]="💻"
    ["containers"]="📦"
)

# Check technology status
check_tech_status() {
    local tech=$1
    local status=""
    
    if [[ -d "$tech" ]]; then
        if [[ -f "$tech/scraper.py" ]] || [[ -f "$tech/scripts/${tech}_scraper.py" ]]; then
            if [[ -d "$tech/vector_db" ]] && [[ -n "$(ls -A "$tech/vector_db" 2>/dev/null)" ]]; then
                status="${GREEN}✅ Ready${NC}"
            elif [[ -d "$tech/docs" ]] && [[ -n "$(ls -A "$tech/docs" 2>/dev/null)" ]]; then
                status="${YELLOW}🔧 Docs scraped, needs indexing${NC}"
            else
                status="${YELLOW}🔧 Ready to build${NC}"
            fi
        else
            status="${RED}❌ Not configured${NC}"
        fi
    else
        status="${RED}❌ Not found${NC}"
    fi
    
    echo -e "$status"
}

show_main_menu() {
    clear
    echo -e "${BLUE}===============================================${NC}"
    echo -e "${BLUE}Red Hat Knowledge System${NC}"
    echo -e "${BLUE}Complete 8-Technology Management System${NC}"
    echo -e "${BLUE}===============================================${NC}"
    echo
    echo -e "${CYAN}Technologies:${NC}"
    
    for tech in ansible checkmk rhel python cybersecurity bash powershell containers; do
        local port=${TECH_PORTS[$tech]}
        local name=${TECH_NAMES[$tech]}
        local icon=${TECH_ICONS[$tech]}
        local status=$(check_tech_status $tech)
        
        printf "%-2s) %-12s (Port %-4s) %s %s\n" \
            "${tech:0:1}" "$icon $name" "$port" "$status"
    done
    
    echo
    echo -e "${CYAN}Actions:${NC}"
    echo "s) Scrape documentation"
    echo "i) Index documents"
    echo "q) Interactive queries"
    echo "a) Start API server"
    echo "h) Health check"
    echo "p) Organize PDF books"
    echo "c) Configure cron jobs"
    echo "x) Exit"
    echo
}

show_tech_menu() {
    local action=$1
    echo
    echo -e "${CYAN}Choose technology:${NC}"
    
    local counter=1
    for tech in ansible checkmk rhel python cybersecurity bash powershell containers; do
        local name=${TECH_NAMES[$tech]}
        local icon=${TECH_ICONS[$tech]}
        local status=$(check_tech_status $tech)
        
        printf "%d) %s %-12s %s\n" "$counter" "$icon" "$name" "$status"
        counter=$((counter + 1))
    done
    
    echo "9) All systems"
    echo "0) Back to main menu"
    echo
}

get_tech_by_number() {
    case $1 in
        1) echo "ansible" ;;
        2) echo "checkmk" ;;
        3) echo "rhel" ;;
        4) echo "python" ;;
        5) echo "cybersecurity" ;;
        6) echo "bash" ;;
        7) echo "powershell" ;;
        8) echo "containers" ;;
        9) echo "all" ;;
        0) echo "back" ;;
        *) echo "invalid" ;;
    esac
}

scrape_documentation() {
    show_tech_menu "scrape"
    read -p "Technology (0-9): " tech_choice
    
    local tech=$(get_tech_by_number $tech_choice)
    
    case $tech in
        "back") return ;;
        "invalid") echo "Invalid choice"; sleep 1; return ;;
        "all")
            echo -e "${YELLOW}Scraping all technologies...${NC}"
            for t in ansible checkmk rhel python cybersecurity bash powershell containers; do
                if [[ -d "$t" ]]; then
                    echo -e "${BLUE}Scraping ${TECH_NAMES[$t]}...${NC}"
                    cd "$t"
                    source ../shared-env/bin/activate
                    
                    if [[ -f "scraper.py" ]]; then
                        python3 scraper.py
                    elif [[ -f "scripts/${t}_scraper.py" ]]; then
                        python3 "scripts/${t}_scraper.py"
                    else
                        echo -e "${RED}No scraper found for $t${NC}"
                    fi
                    
                    cd ..
                    echo -e "${GREEN}${TECH_NAMES[$t]} scraping complete!${NC}"
                    echo
                fi
            done
            ;;
        *)
            if [[ -d "$tech" ]]; then
                echo -e "${BLUE}Scraping ${TECH_NAMES[$tech]} documentation...${NC}"
                cd "$tech"
                source ../shared-env/bin/activate
                
                if [[ -f "scraper.py" ]]; then
                    python3 scraper.py
                elif [[ -f "scripts/${tech}_scraper.py" ]]; then
                    python3 "scripts/${tech}_scraper.py"
                else
                    echo -e "${RED}No scraper found for $tech${NC}"
                fi
                
                cd ..
                echo -e "${GREEN}${TECH_NAMES[$tech]} scraping complete!${NC}"
            else
                echo -e "${RED}Technology $tech not found${NC}"
            fi
            ;;
    esac
    
    read -p "Press Enter to continue..."
}

index_documents() {
    show_tech_menu "index"
    read -p "Technology (0-9): " tech_choice
    
    local tech=$(get_tech_by_number $tech_choice)
    
    case $tech in
        "back") return ;;
        "invalid") echo "Invalid choice"; sleep 1; return ;;
        "all")
            echo -e "${YELLOW}Indexing all technologies...${NC}"
            for t in ansible checkmk rhel python cybersecurity bash powershell containers; do
                if [[ -d "$t" ]] && [[ -f "$t/rag_system.py" ]]; then
                    echo -e "${BLUE}Indexing ${TECH_NAMES[$t]}...${NC}"
                    cd "$t"
                    source ../shared-env/bin/activate
                    python3 rag_system.py --index
                    cd ..
                    echo -e "${GREEN}${TECH_NAMES[$t]} indexing complete!${NC}"
                    echo
                fi
            done
            ;;
        *)
            if [[ -d "$tech" ]] && [[ -f "$tech/rag_system.py" ]]; then
                echo -e "${BLUE}Indexing ${TECH_NAMES[$tech]} documents...${NC}"
                cd "$tech"
                source ../shared-env/bin/activate
                python3 rag_system.py --index
                cd ..
                echo -e "${GREEN}${TECH_NAMES[$tech]} indexing complete!${NC}"
            else
                echo -e "${RED}Technology $tech not found or not configured${NC}"
            fi
            ;;
    esac
    
    read -p "Press Enter to continue..."
}

interactive_queries() {
    show_tech_menu "query"
    read -p "Technology (0-9): " tech_choice
    
    local tech=$(get_tech_by_number $tech_choice)
    
    case $tech in
        "back") return ;;
        "invalid") echo "Invalid choice"; sleep 1; return ;;
        "all") echo "Interactive mode not available for all systems"; sleep 1; return ;;
        *)
            if [[ -d "$tech" ]] && [[ -f "$tech/rag_system.py" ]]; then
                echo -e "${BLUE}Starting ${TECH_NAMES[$tech]} interactive system...${NC}"
                cd "$tech"
                source ../shared-env/bin/activate
                python3 rag_system.py --interactive
                cd ..
            else
                echo -e "${RED}Technology $tech not found or not configured${NC}"
                sleep 2
            fi
            ;;
    esac
}

start_api_server() {
    show_tech_menu "API server"
    read -p "Technology (0-9): " tech_choice
    
    local tech=$(get_tech_by_number $tech_choice)
    
    case $tech in
        "back") return ;;
        "invalid") echo "Invalid choice"; sleep 1; return ;;
        "all")
            echo -e "${YELLOW}Starting all API servers...${NC}"
            for t in ansible checkmk rhel python cybersecurity bash powershell containers; do
                if [[ -d "$t" ]] && [[ -f "$t/api_server.py" ]]; then
                    local port=${TECH_PORTS[$t]}
                    echo -e "${BLUE}Starting ${TECH_NAMES[$t]} on port $port...${NC}"
                    cd "$t"
                    source ../shared-env/bin/activate
                    nohup python3 api_server.py > ../logs/${t}_api.log 2>&1 &
                    echo $! > ../logs/${t}_api.pid
                    cd ..
                    sleep 1
                fi
            done
            echo
            echo -e "${GREEN}All API servers started!${NC}"
            echo -e "${CYAN}Add these to Open WebUI:${NC}"
            for t in ansible checkmk rhel python cybersecurity bash powershell containers; do
                if [[ -d "$t" ]] && [[ -f "$t/api_server.py" ]]; then
                    local port=${TECH_PORTS[$t]}
                    echo "http://localhost:$port - ${TECH_NAMES[$t]}"
                fi
            done
            ;;
        *)
            if [[ -d "$tech" ]] && [[ -f "$tech/api_server.py" ]]; then
                local port=${TECH_PORTS[$tech]}
                echo -e "${BLUE}Starting ${TECH_NAMES[$tech]} API server on port $port...${NC}"
                echo -e "${CYAN}Add http://localhost:$port to Open WebUI as knowledge source${NC}"
                cd "$tech"
                source ../shared-env/bin/activate
                python3 api_server.py
                cd ..
            else
                echo -e "${RED}Technology $tech not found or not configured${NC}"
                sleep 2
            fi
            ;;
    esac
    
    read -p "Press Enter to continue..."
}

health_check() {
    clear
    echo -e "${BLUE}===============================================${NC}"
    echo -e "${BLUE}System Health Check${NC}"
    echo -e "${BLUE}===============================================${NC}"
    echo
    
    source shared-env/bin/activate 2>/dev/null || true
    
    # Check each technology
    for tech in ansible checkmk rhel python cybersecurity bash powershell containers; do
        local name=${TECH_NAMES[$tech]}
        local icon=${TECH_ICONS[$tech]}
        local port=${TECH_PORTS[$tech]}
        
        if [[ -d "$tech" ]]; then
            local web_docs=$(find "$tech/docs" -name "*.json" -not -name "doc_index.json" 2>/dev/null | wc -l)
            local pdf_docs=$(find "$tech/pdfs" -name "*.pdf" 2>/dev/null | wc -l)
            
            if [[ -d "$tech/vector_db" ]] && [[ -n "$(ls -A "$tech/vector_db" 2>/dev/null)" ]]; then
                local indexed="${GREEN}✅ Indexed${NC}"
            else
                local indexed="${RED}❌ Not indexed${NC}"
            fi
            
            # Check if API server is running
            if curl -s "http://localhost:$port/health" > /dev/null 2>&1; then
                local api_status="${GREEN}✅ Running${NC}"
            else
                local api_status="${RED}❌ Stopped${NC}"
            fi
            
            printf "%s %-12s: %3d web docs, %2d PDFs, %s, API %s\n" \
                "$icon" "$name" "$web_docs" "$pdf_docs" "$indexed" "$api_status"
        else
            printf "%s %-12s: ${RED}❌ Not found${NC}\n" "$icon" "$name"
        fi
    done
    
    echo
    echo -e "${CYAN}System Status:${NC}"
    
    # Test Ollama connection
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo -e "Ollama: ${GREEN}✅ Running${NC}"
    else
        echo -e "Ollama: ${RED}❌ Not running${NC} (start with: ollama serve)"
    fi
    
    # Check Python environment
    if [[ -f "shared-env/bin/activate" ]]; then
        echo -e "Python Environment: ${GREEN}✅ Ready${NC}"
    else
        echo -e "Python Environment: ${RED}❌ Missing${NC}"
    fi
    
    # Check disk space
    local disk_usage=$(df -h . | awk 'NR==2 {print $5}' | sed 's/%//')
    if [[ $disk_usage -lt 80 ]]; then
        echo -e "Disk Space: ${GREEN}✅ ${disk_usage}% used${NC}"
    else
        echo -e "Disk Space: ${YELLOW}⚠️  ${disk_usage}% used${NC}"
    fi
    
    # Show running API servers
    echo
    echo -e "${CYAN}Running API Servers:${NC}"
    local running_apis=0
    for tech in ansible checkmk rhel python cybersecurity bash powershell containers; do
        local port=${TECH_PORTS[$tech]}
        if curl -s "http://localhost:$port/health" > /dev/null 2>&1; then
            echo "http://localhost:$port - ${TECH_NAMES[$tech]}"
            running_apis=$((running_apis + 1))
        fi
    done
    
    if [[ $running_apis -eq 0 ]]; then
        echo "No API servers currently running"
    fi
    
    echo
    read -p "Press Enter to continue..."
}

organize_pdfs() {
    echo -e "${BLUE}Organizing PDF books...${NC}"
    
    if [[ ! -d "$HOME/Books" ]]; then
        echo -e "${RED}~/Books directory not found${NC}"
        read -p "Press Enter to continue..."
        return
    fi
    
    echo "Scanning ~/Books for PDF files..."
    
    # Create technology PDF directories
    for tech in ansible checkmk rhel python cybersecurity bash powershell containers; do
        mkdir -p "$tech/pdfs"
    done
    
    # Simple PDF categorization based on filename
    find "$HOME/Books" -name "*.pdf" -type f | while read pdf; do
        local filename=$(basename "$pdf")
        local lowercase_name=$(echo "$filename" | tr '[:upper:]' '[:lower:]')
        local copied=false
        
        # Check for technology keywords in filename
        if [[ $lowercase_name =~ (ansible|playbook) ]] && [[ ! $copied ]]; then
            cp "$pdf" "ansible/pdfs/" && echo "📋 $filename → Ansible" && copied=true
        fi
        
        if [[ $lowercase_name =~ (checkmk|nagios|monitoring) ]] && [[ ! $copied ]]; then
            cp "$pdf" "checkmk/pdfs/" && echo "📊 $filename → CheckMK" && copied=true
        fi
        
        if [[ $lowercase_name =~ (rhel|redhat|centos|linux) ]] && [[ ! $copied ]]; then
            cp "$pdf" "rhel/pdfs/" && echo "🐧 $filename → RHEL" && copied=true
        fi
        
        if [[ $lowercase_name =~ (python|django|flask) ]] && [[ ! $copied ]]; then
            cp "$pdf" "python/pdfs/" && echo "🐍 $filename → Python" && copied=true
        fi
        
        if [[ $lowercase_name =~ (security|cyber|penetration|hacking) ]] && [[ ! $copied ]]; then
            cp "$pdf" "cybersecurity/pdfs/" && echo "🔒 $filename → Cybersecurity" && copied=true
        fi
        
        if [[ $lowercase_name =~ (bash|shell|scripting) ]] && [[ ! $copied ]]; then
            cp "$pdf" "bash/pdfs/" && echo "📜 $filename → Bash" && copied=true
        fi
        
        if [[ $lowercase_name =~ (powershell|windows) ]] && [[ ! $copied ]]; then
            cp "$pdf" "powershell/pdfs/" && echo "💻 $filename → PowerShell" && copied=true
        fi
        
        if [[ $lowercase_name =~ (docker|container|kubernetes|podman) ]] && [[ ! $copied ]]; then
            cp "$pdf" "containers/pdfs/" && echo "📦 $filename → Containers" && copied=true
        fi
    done
    
    echo -e "${GREEN}PDF organization complete!${NC}"
    read -p "Press Enter to continue..."
}

configure_cron() {
    echo -e "${BLUE}Configuring automatic updates...${NC}"
    
    # Create update script
    cat > auto_update.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source shared-env/bin/activate

echo "$(date): Starting automatic knowledge update" >> auto_update.log

for tech in ansible checkmk rhel python cybersecurity bash powershell containers; do
    if [[ -d "$tech" ]] && [[ -f "$tech/scraper.py" ]]; then
        echo "$(date): Updating $tech" >> auto_update.log
        cd "$tech"
        python3 scraper.py >> ../auto_update.log 2>&1
        python3 rag_system.py --index >> ../auto_update.log 2>&1
        cd ..
    fi
done

echo "$(date): Automatic update complete" >> auto_update.log
EOF
    
    chmod +x auto_update.sh
    
    # Add to crontab (runs every 2 days at 2 AM)
    (crontab -l 2>/dev/null; echo "0 2 */2 * * $(pwd)/auto_update.sh") | crontab -
    
    echo -e "${GREEN}Cron job configured to run every 2 days at 2 AM${NC}"
    echo "Logs will be written to auto_update.log"
    read -p "Press Enter to continue..."
}

# Main loop
while true; do
    show_main_menu
    read -p "Choose action: " choice
    
    case $choice in
        s|S) scrape_documentation ;;
        i|I) index_documents ;;
        q|Q) interactive_queries ;;
        a|A) start_api_server ;;
        h|H) health_check ;;
        p|P) organize_pdfs ;;
        c|C) configure_cron ;;
        x|X) 
            echo -e "${YELLOW}Shutting down API servers...${NC}"
            pkill -f "api_server.py" 2>/dev/null || true
            echo -e "${GREEN}Goodbye!${NC}"
            exit 0 
            ;;
        *)
            echo -e "${RED}Invalid choice${NC}"
            sleep 1
            ;;
    esac
done
