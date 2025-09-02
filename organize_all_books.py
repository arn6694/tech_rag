#!/usr/bin/env python3
"""
Enhanced Book Organizer for PDF and EPUB files
Organizes books from ~/books into appropriate technology categories
"""

import os
import shutil
import json
from pathlib import Path
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedBookOrganizer:
    def __init__(self):
        # Technology keywords for categorization
        self.category_keywords = {
            'ansible': [
                'ansible', 'playbook', 'automation', 'configuration management',
                'devops', 'infrastructure as code', 'iac', 'tower', 'awx'
            ],
            'rhel': [
                'red hat', 'rhel', 'centos', 'enterprise linux', 'systemd',
                'linux administration', 'system admin', 'redhat', 'rhcsa', 'rhce'
            ],
            'python': [
                'python', 'programming', 'coding', 'software development',
                'scripting', 'django', 'flask', 'pandas', 'numpy', 'learn python',
                'automate the boring stuff', 'python crash course', 'openai api'
            ],
            'bash': [
                'bash', 'shell scripting', 'shell programming', 'bash scripting',
                'command line', 'terminal scripting', 'awk', 'sed', 'grep',
                'linux shell', 'shell scripts', 'pentesters'
            ],
            'powershell': [
                'powershell', 'powershell scripting', 'windows scripting',
                'cmdlets', 'powershell core', 'automation', 'windows automation'
            ],
            'containers': [
                'docker', 'podman', 'containers', 'containerization',
                'kubernetes', 'container orchestration', 'dockerfile',
                'container images', 'microservices'
            ],
            'cybersecurity': [
                'security', 'cybersecurity', 'penetration testing', 'pentest',
                'ethical hacking', 'vulnerability', 'malware', 'forensics',
                'incident response', 'nmap', 'metasploit', 'wireshark',
                'malware development', 'ethical hackers'
            ],
            'checkmk': [
                'checkmk', 'check_mk', 'nagios', 'monitoring', 'alerting',
                'observability', 'metrics', 'grafana', 'prometheus'
            ],
            'linux_general': [
                'linux', 'unix', 'gnu', 'open source', 'kernel', 'networking'
            ],
            'ai_ml': [
                'ai', 'artificial intelligence', 'machine learning', 'chatgpt',
                'openai', 'conversational ai', 'chatbots', 'home assistant'
            ]
        }
        
        # Technology priority (if multiple matches, use this order)
        self.priority_order = [
            'ansible', 'checkmk', 'rhel', 'python', 'bash', 'powershell', 
            'containers', 'cybersecurity', 'linux_general', 'ai_ml'
        ]
    
    def analyze_filename(self, filename: str) -> dict:
        """Analyze filename for technology keywords"""
        filename_lower = filename.lower()
        scores = {}
        
        for tech, keywords in self.category_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in filename_lower:
                    # Longer keywords get higher scores
                    score += len(keyword.split())
            scores[tech] = score
        
        return scores
    
    def categorize_book(self, book_path: Path) -> tuple:
        """Categorize a single book file"""
        logger.info(f"Categorizing: {book_path.name}")
        
        # Analyze filename
        filename_scores = self.analyze_filename(book_path.name)
        
        # Find best match using priority order
        best_category = 'general'
        best_score = 0
        
        for tech in self.priority_order:
            if filename_scores.get(tech, 0) > best_score:
                best_score = filename_scores[tech]
                best_category = tech
        
        # Special handling for specific books
        book_name_lower = book_path.name.lower()
        
        if 'rhcsa' in book_name_lower or 'red hat' in book_name_lower:
            best_category = 'rhel'
        elif 'ansible' in book_name_lower:
            best_category = 'ansible'
        elif 'python' in book_name_lower or 'automate the boring' in book_name_lower:
            best_category = 'python'
        elif 'bash' in book_name_lower or 'shell' in book_name_lower:
            best_category = 'bash'
        elif 'malware' in book_name_lower or 'ethical hack' in book_name_lower:
            best_category = 'cybersecurity'
        elif 'chatgpt' in book_name_lower or 'openai' in book_name_lower or 'ai' in book_name_lower:
            best_category = 'ai_ml'
        elif 'linux' in book_name_lower and 'networking' in book_name_lower:
            best_category = 'linux_general'
        elif 'home assistant' in book_name_lower:
            best_category = 'ai_ml'
        elif 'roblox' in book_name_lower:
            best_category = 'general'  # Skip this one
        
        categorization_info = {
            'category': best_category,
            'confidence_score': best_score,
            'filename_scores': filename_scores
        }
        
        logger.info(f"Categorized {book_path.name} as: {best_category} (score: {best_score})")
        return best_category, categorization_info
    
    def organize_books_directory(self, books_dir: Path, target_base_dir: Path) -> dict:
        """Organize existing Books directory into technology categories"""
        if not books_dir.exists():
            logger.warning(f"Books directory not found: {books_dir}")
            return {}
        
        # Find all book files (PDF and EPUB)
        book_files = []
        for ext in ['*.pdf', '*.epub']:
            book_files.extend(list(books_dir.glob(ext)))
        
        if not book_files:
            logger.info(f"No book files found in {books_dir}")
            return {}
        
        organization_results = {
            'total_files': len(book_files),
            'categorized': {},
            'errors': []
        }
        
        for book_file in book_files:
            try:
                category, info = self.categorize_book(book_file)
                
                # Skip general category books
                if category == 'general':
                    logger.info(f"Skipping {book_file.name} (general category)")
                    continue
                
                # Create target directory
                target_dir = target_base_dir / category / 'pdfs'
                target_dir.mkdir(parents=True, exist_ok=True)
                
                # Copy (don't move) book to maintain original
                target_path = target_dir / book_file.name
                if not target_path.exists():
                    shutil.copy2(book_file, target_path)
                    logger.info(f"Copied {book_file.name} to {category}/pdfs/")
                else:
                    logger.info(f"{book_file.name} already exists in {category}/pdfs/")
                
                # Track results
                if category not in organization_results['categorized']:
                    organization_results['categorized'][category] = []
                
                organization_results['categorized'][category].append({
                    'filename': book_file.name,
                    'confidence': info['confidence_score'],
                    'source_path': str(book_file),
                    'target_path': str(target_path)
                })
                
            except Exception as e:
                error_msg = f"Error processing {book_file.name}: {e}"
                logger.error(error_msg)
                organization_results['errors'].append(error_msg)
        
        # Save organization report
        report_path = target_base_dir / 'book_organization_report.json'
        with open(report_path, 'w') as f:
            json.dump(organization_results, f, indent=2)
        
        return organization_results

def main():
    """Main function to organize books"""
    books_dir = Path.home() / 'books'
    target_dir = Path('/home/brian/redhat-knowledge')
    
    organizer = EnhancedBookOrganizer()
    results = organizer.organize_books_directory(books_dir, target_dir)
    
    print(f"\nBook Organization Complete!")
    print(f"Total files processed: {results['total_files']}")
    print(f"Categories created:")
    
    for category, files in results['categorized'].items():
        print(f"  {category}: {len(files)} files")
        for file_info in files:
            print(f"    - {file_info['filename']}")
    
    if results['errors']:
        print(f"\nErrors encountered:")
        for error in results['errors']:
            print(f"  - {error}")

if __name__ == "__main__":
    main()
