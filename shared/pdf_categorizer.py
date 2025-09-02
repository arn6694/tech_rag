#!/usr/bin/env python3
"""
Intelligent PDF Categorization System
Automatically categorizes PDF books by content and filename analysis
"""

import os
import re
import json
from pathlib import Path
import logging
from typing import Dict, List, Tuple
import fitz  # PyMuPDF

logger = logging.getLogger(__name__)

class PDFCategorizer:
    def __init__(self):
        # Technology keywords for categorization
        self.category_keywords = {
            'ansible': [
                'ansible', 'playbook', 'automation', 'configuration management',
                'devops', 'infrastructure as code', 'iac', 'tower', 'awx'
            ],
            'rhel': [
                'red hat', 'rhel', 'centos', 'enterprise linux', 'systemd',
                'linux administration', 'system admin', 'redhat'
            ],
            'python': [
                'python', 'programming', 'coding', 'software development',
                'scripting', 'django', 'flask', 'pandas', 'numpy', 'learn python'
            ],
            'bash': [
                'bash', 'shell scripting', 'shell programming', 'bash scripting',
                'command line', 'terminal scripting', 'awk', 'sed', 'grep'
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
                'incident response', 'nmap', 'metasploit', 'wireshark'
            ],
            'checkmk': [
                'checkmk', 'check_mk', 'nagios', 'monitoring', 'alerting',
                'observability', 'metrics', 'grafana', 'prometheus'
            ],
            'linux_general': [
                'linux', 'unix', 'gnu', 'open source', 'kernel'
            ],
            'networking': [
                'networking', 'tcp/ip', 'cisco', 'routing', 'switching',
                'firewall', 'vpn', 'dns', 'dhcp'
            ]
        }
        
        # Technology priority (if multiple matches, use this order)
        self.priority_order = [
            'ansible', 'checkmk', 'rhel', 'python', 'bash', 'powershell', 
            'containers', 'cybersecurity', 'linux_general', 'networking'
        ]
    
    def extract_text_sample(self, pdf_path: Path, max_pages: int = 3) -> str:
        """Extract text sample from first few pages for analysis"""
        try:
            doc = fitz.open(str(pdf_path))
            text_sample = ""
            
            # Extract text from first few pages
            for page_num in range(min(max_pages, doc.page_count)):
                page = doc[page_num]
                text_sample += page.get_text().lower()
            
            doc.close()
            return text_sample
        except Exception as e:
            logger.error(f"Error extracting text sample from {pdf_path}: {e}")
            return ""
    
    def analyze_filename(self, filename: str) -> Dict[str, int]:
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
    
    def analyze_content(self, text_content: str) -> Dict[str, int]:
        """Analyze PDF content for technology keywords"""
        text_lower = text_content.lower()
        scores = {}
        
        for tech, keywords in self.category_keywords.items():
            score = 0
            for keyword in keywords:
                # Count occurrences, with diminishing returns
                count = text_lower.count(keyword)
                if count > 0:
                    score += min(count, 10)  # Cap at 10 mentions
            scores[tech] = score
        
        return scores
    
    def categorize_pdf(self, pdf_path: Path) -> Tuple[str, Dict]:
        """Categorize a single PDF file"""
        logger.info(f"Categorizing: {pdf_path.name}")
        
        # Analyze filename
        filename_scores = self.analyze_filename(pdf_path.name)
        
        # Analyze content sample
        text_sample = self.extract_text_sample(pdf_path)
        content_scores = self.analyze_content(text_sample)
        
        # Combine scores (filename weighted higher)
        combined_scores = {}
        all_techs = set(filename_scores.keys()) | set(content_scores.keys())
        
        for tech in all_techs:
            filename_score = filename_scores.get(tech, 0)
            content_score = content_scores.get(tech, 0)
            # Weight filename more heavily
            combined_scores[tech] = (filename_score * 3) + content_score
        
        # Find best match using priority order
        best_category = 'general'
        best_score = 0
        
        for tech in self.priority_order:
            if combined_scores.get(tech, 0) > best_score:
                best_score = combined_scores[tech]
                best_category = tech
        
        # If no good matches, try generic categories
        if best_score == 0:
            if any(word in pdf_path.name.lower() for word in ['linux', 'unix']):
                best_category = 'linux_general'
            elif any(word in pdf_path.name.lower() for word in ['network', 'cisco']):
                best_category = 'networking'
        
        categorization_info = {
            'category': best_category,
            'confidence_score': best_score,
            'filename_scores': filename_scores,
            'content_scores': content_scores,
            'combined_scores': combined_scores
        }
        
        logger.info(f"Categorized {pdf_path.name} as: {best_category} (score: {best_score})")
        return best_category, categorization_info
    
    def organize_books_directory(self, books_dir: Path, target_base_dir: Path) -> Dict:
        """Organize existing Books directory into technology categories"""
        if not books_dir.exists():
            logger.warning(f"Books directory not found: {books_dir}")
            return {}
        
        pdf_files = list(books_dir.glob('*.pdf'))
        if not pdf_files:
            logger.info(f"No PDF files found in {books_dir}")
            return {}
        
        organization_results = {
            'total_files': len(pdf_files),
            'categorized': {},
            'errors': []
        }
        
        for pdf_file in pdf_files:
            try:
                category, info = self.categorize_pdf(pdf_file)
                
                # Create target directory
                target_dir = target_base_dir / category / 'pdfs'
                target_dir.mkdir(parents=True, exist_ok=True)
                
                # Copy (don't move) PDF to maintain original
                target_path = target_dir / pdf_file.name
                if not target_path.exists():
                    import shutil
                    shutil.copy2(pdf_file, target_path)
                    logger.info(f"Copied {pdf_file.name} to {category}/pdfs/")
                
                # Track results
                if category not in organization_results['categorized']:
                    organization_results['categorized'][category] = []
                
                organization_results['categorized'][category].append({
                    'filename': pdf_file.name,
                    'confidence': info['confidence_score'],
                    'source_path': str(pdf_file),
                    'target_path': str(target_path)
                })
                
            except Exception as e:
                error_msg = f"Error processing {pdf_file.name}: {e}"
                logger.error(error_msg)
                organization_results['errors'].append(error_msg)
        
        # Save organization report
        report_path = target_base_dir / 'pdf_organization_report.json'
        with open(report_path, 'w') as f:
            json.dump(organization_results, f, indent=2)
        
        return organization_results

if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='PDF Categorization System')
    parser.add_argument('--books-dir', required=True, help='Source books directory')
    parser.add_argument('--target-dir', required=True, help='Target organization directory')
    parser.add_argument('--single-file', help='Categorize a single PDF file')
    
    args = parser.parse_args()
    
    categorizer = PDFCategorizer()
    
    if args.single_file:
        category, info = categorizer.categorize_pdf(Path(args.single_file))
        print(f"Category: {category}")
        print(f"Confidence: {info['confidence_score']}")
    else:
        results = categorizer.organize_books_directory(
            Path(args.books_dir), 
            Path(args.target_dir)
        )
        print(f"Organized {results['total_files']} files")
        for category, files in results['categorized'].items():
            print(f"  {category}: {len(files)} files")
