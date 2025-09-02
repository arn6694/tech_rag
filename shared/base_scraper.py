#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import os
import time
import json
from urllib.parse import urljoin
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseDocScraper:
    def __init__(self, output_dir, technology_name):
        self.output_dir = output_dir
        self.technology_name = technology_name
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
        os.makedirs(output_dir, exist_ok=True)

    def fetch_page(self, url, max_retries=3):
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
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            element.decompose()
        
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "No Title"
        
        # Find main content
        content_selectors = ['main', 'article', '.content', '#content', '.documentation', '.body', '.document']
        main_content = None
        for selector in content_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        if not main_content:
            main_content = soup.find('body') or soup
        
        # Extract structured text
        text_content = []
        for element in main_content.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li', 'code', 'pre']):
            text = element.get_text().strip()
            if text and len(text) > 10:
                if element.name.startswith('h'):
                    text_content.append(f"\n## {text}\n")
                elif element.name in ['code', 'pre']:
                    text_content.append(f"```\n{text}\n```")
                else:
                    text_content.append(text)
        
        return {
            'title': title_text,
            'url': url,
            'content': '\n\n'.join(text_content),
            'scraped_at': datetime.now().isoformat(),
            'technology': self.technology_name
        }

    def scrape_documentation(self):
        all_docs = []
        
        for source_name, source_config in self.doc_sources.items():
            logger.info(f"Scraping {source_name} documentation for {self.technology_name}...")
            
            for guide in source_config['guides']:
                url = urljoin(source_config['base_url'], guide)
                logger.info(f"Fetching: {url}")
                
                response = self.fetch_page(url)
                if not response:
                    continue
                
                doc_data = self.extract_text_content(response.text, url)
                doc_data['source'] = source_name
                doc_data['guide'] = guide
                
                filename = f"{source_name}_{guide.replace('/', '_').replace('.html', '')}.json"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(doc_data, f, indent=2, ensure_ascii=False)
                
                all_docs.append(doc_data)
                logger.info(f"Saved: {filepath}")
                time.sleep(1)
        
        # Save index
        index_file = os.path.join(self.output_dir, 'doc_index.json')
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump({
                'technology': self.technology_name,
                'scraped_at': datetime.now().isoformat(),
                'total_docs': len(all_docs),
                'sources': list(self.doc_sources.keys()),
                'documents': [{
                    'source': doc['source'],
                    'title': doc['title'],
                    'url': doc['url'],
                    'filename': f"{doc['source']}_{doc['guide'].replace('/', '_').replace('.html', '')}.json"
                } for doc in all_docs]
            }, f, indent=2)
        
        logger.info(f"Scraping complete! {len(all_docs)} documents saved for {self.technology_name}")
        return all_docs
