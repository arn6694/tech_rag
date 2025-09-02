#!/usr/bin/env python3
"""
RHEL Documentation Scraper for RAG Pipeline
Scrapes Red Hat Enterprise Linux documentation
"""

import requests
from bs4 import BeautifulSoup
import os
import time
import json
from urllib.parse import urljoin, urlparse
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RHELDocScraper:
    def __init__(self, output_dir="docs"):
        self.output_dir = output_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # RHEL documentation sources
        self.doc_sources = {
            'rhel9_admin': {
                'base_url': 'https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/',
                'guides': [
                    'system_administrators_guide/index',
                    'configuring_and_managing_networking/index',
                    'managing_storage/index',
                    'securing_rhel/index',
                    'installing_using_anaconda/index',
                    'performing_a_standard_rhel_9_installation/index',
                    'upgrading_from_rhel_8_to_rhel_9/index',
                    'managing_software_with_the_dnf_tool/index',
                    'managing_users_and_groups/index',
                    'managing_services_with_systemd/index'
                ]
            },
            'rhel8_admin': {
                'base_url': 'https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/',
                'guides': [
                    'system_administrators_guide/index',
                    'configuring_and_managing_networking/index',
                    'managing_storage/index',
                    'securing_rhel/index',
                    'installing_using_anaconda/index',
                    'performing_a_standard_rhel_8_installation/index',
                    'upgrading_from_rhel_7_to_rhel_8/index',
                    'managing_software_with_the_dnf_tool/index',
                    'managing_users_and_groups/index',
                    'managing_services_with_systemd/index'
                ]
            },
            'rhel_security': {
                'base_url': 'https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/',
                'guides': [
                    'security_hardening/index',
                    'using_selinux/index',
                    'auditing_system/index',
                    'compliance_and_vulnerability_scanning/index',
                    'network_security/index'
                ]
            },
            'rhel_networking': {
                'base_url': 'https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/',
                'guides': [
                    'configuring_and_managing_networking/index',
                    'configuring_ip_networking/index',
                    'configuring_ethernet_connections/index',
                    'configuring_wireless_networking/index',
                    'configuring_vpn_connections/index'
                ]
            }
        }
        
        os.makedirs(output_dir, exist_ok=True)

    def fetch_page(self, url, max_retries=3):
        """Fetch a web page with retry logic"""
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    logger.error(f"Failed to fetch {url}")
                    return None

    def extract_text_content(self, html_content, url):
        """Extract meaningful text content from HTML"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'noscript']):
            element.decompose()
        
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "No Title"
        
        # Find main content
        content_selectors = [
            'main', 'article', '.content', '#content', 
            '.documentation', '.body', '.document', '.chapter'
        ]
        
        main_content = None
        for selector in content_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        if not main_content:
            main_content = soup.find('body') or soup
        
        # Extract structured text
        text_content = []
        
        for element in main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'code', 'pre', 'blockquote']):
            text = element.get_text().strip()
            if text and len(text) > 10:
                if element.name.startswith('h'):
                    level = element.name[1]
                    text_content.append(f"\n{'#' * int(level)} {text}\n")
                elif element.name in ['code', 'pre']:
                    text_content.append(f"```\n{text}\n```")
                elif element.name == 'blockquote':
                    text_content.append(f"> {text}")
                else:
                    text_content.append(text)
        
        return {
            'title': title_text,
            'url': url,
            'content': '\n\n'.join(text_content),
            'scraped_at': datetime.now().isoformat()
        }

    def scrape_documentation(self):
        """Scrape all configured RHEL documentation sources"""
        all_docs = []
        
        for source_name, source_config in self.doc_sources.items():
            logger.info(f"Scraping {source_name} documentation...")
            
            for guide in source_config['guides']:
                url = urljoin(source_config['base_url'], guide)
                logger.info(f"Fetching: {url}")
                
                response = self.fetch_page(url)
                if not response:
                    continue
                
                doc_data = self.extract_text_content(response.text, url)
                doc_data['source'] = source_name
                doc_data['guide'] = guide
                
                # Save individual document
                filename = f"{source_name}_{guide.replace('/', '_').replace('.html', '')}.json"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(doc_data, f, indent=2, ensure_ascii=False)
                
                all_docs.append(doc_data)
                logger.info(f"Saved: {filepath}")
                
                # Be respectful
                time.sleep(1)
        
        # Save index
        index_file = os.path.join(self.output_dir, 'doc_index.json')
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump({
                'scraped_at': datetime.now().isoformat(),
                'total_docs': len(all_docs),
                'sources': list(self.doc_sources.keys()),
                'documents': [
                    {
                        'source': doc['source'],
                        'title': doc['title'],
                        'url': doc['url'],
                        'filename': f"{doc['source']}_{doc['guide'].replace('/', '_').replace('.html', '')}.json"
                    }
                    for doc in all_docs
                ]
            }, f, indent=2)
        
        logger.info(f"RHEL scraping complete! {len(all_docs)} documents saved")
        return all_docs

if __name__ == "__main__":
    scraper = RHELDocScraper()
    docs = scraper.scrape_documentation()
