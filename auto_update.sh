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
