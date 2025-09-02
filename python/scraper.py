#!/usr/bin/env python3
"""
Python Documentation Scraper for RAG Pipeline
Scrapes Python programming documentation
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

class PythonDocScraper:
    def __init__(self, output_dir="docs"):
        self.output_dir = output_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Python documentation sources
        self.doc_sources = {
            'python_tutorial': {
                'base_url': 'https://docs.python.org/3/tutorial/',
                'guides': [
                    'index.html',
                    'introduction.html',
                    'interpreter.html',
                    'introduction.html#using-python-as-a-calculator',
                    'controlflow.html',
                    'datastructures.html',
                    'modules.html',
                    'inputoutput.html',
                    'errors.html',
                    'classes.html',
                    'stdlib.html',
                    'stdlib2.html',
                    'whatnow.html',
                    'interactive.html',
                    'floatingpoint.html',
                    'appendix.html'
                ]
            },
            'python_library': {
                'base_url': 'https://docs.python.org/3/library/',
                'guides': [
                    'index.html',
                    'functions.html',
                    'builtin.html',
                    'types.html',
                    'exceptions.html',
                    'text.html',
                    'binary.html',
                    'data.html',
                    'numeric.html',
                    'math.html',
                    'cmath.html',
                    'decimal.html',
                    'fractions.html',
                    'random.html',
                    'statistics.html',
                    'itertools.html',
                    'functools.html',
                    'operator.html',
                    'pathlib.html',
                    'os.html',
                    'io.html',
                    'time.html',
                    'argparse.html',
                    'getopt.html',
                    'logging.html',
                    'getpass.html',
                    'curses.html',
                    'platform.html',
                    'errno.html',
                    'ctypes.html',
                    'threading.html',
                    'multiprocessing.html',
                    'concurrent.html',
                    'subprocess.html',
                    'sched.html',
                    'queue.html',
                    'contextvars.html',
                    '_thread.html',
                    'dummy_threading.html',
                    'asyncio.html',
                    'socket.html',
                    'ssl.html',
                    'select.html',
                    'selectors.html',
                    'signal.html',
                    'mmap.html',
                    'email.html',
                    'json.html',
                    'mailcap.html',
                    'mailbox.html',
                    'mimetypes.html',
                    'base64.html',
                    'binascii.html',
                    'quopri.html',
                    'uu.html',
                    'html.html',
                    'xml.html',
                    'urllib.html',
                    'http.html',
                    'ftplib.html',
                    'poplib.html',
                    'imaplib.html',
                    'nntplib.html',
                    'smtplib.html',
                    'smtpd.html',
                    'telnetlib.html',
                    'uuid.html',
                    'socketserver.html',
                    'xmlrpc.html',
                    'ipaddress.html',
                    'audioop.html',
                    'aifc.html',
                    'sunau.html',
                    'wave.html',
                    'chunk.html',
                    'colorsys.html',
                    'imghdr.html',
                    'sndhdr.html',
                    'ossaudiodev.html',
                    'gettext.html',
                    'locale.html',
                    'calendar.html',
                    'collections.html',
                    'heapq.html',
                    'bisect.html',
                    'array.html',
                    'weakref.html',
                    'types.html',
                    'copy.html',
                    'pprint.html',
                    'reprlib.html',
                    'enum.html',
                    'numbers.html',
                    'math.html',
                    'cmath.html',
                    'decimal.html',
                    'fractions.html',
                    'random.html',
                    'statistics.html',
                    'itertools.html',
                    'functools.html',
                    'operator.html',
                    'pathlib.html',
                    'fileinput.html',
                    'stat.html',
                    'filecmp.html',
                    'tempfile.html',
                    'glob.html',
                    'fnmatch.html',
                    'linecache.html',
                    'shutil.html',
                    'macpath.html',
                    'pickle.html',
                    'copyreg.html',
                    'shelve.html',
                    'marshal.html',
                    'dbm.html',
                    'sqlite3.html',
                    'zipfile.html',
                    'tarfile.html',
                    'csv.html',
                    'configparser.html',
                    'netrc.html',
                    'xdrlib.html',
                    'plistlib.html',
                    'hashlib.html',
                    'hmac.html',
                    'secrets.html',
                    'os.html',
                    'io.html',
                    'time.html',
                    'argparse.html',
                    'getopt.html',
                    'logging.html',
                    'getpass.html',
                    'curses.html',
                    'platform.html',
                    'errno.html',
                    'ctypes.html',
                    'threading.html',
                    'multiprocessing.html',
                    'concurrent.html',
                    'subprocess.html',
                    'sched.html',
                    'queue.html',
                    'contextvars.html',
                    '_thread.html',
                    'dummy_threading.html',
                    'asyncio.html',
                    'socket.html',
                    'ssl.html',
                    'select.html',
                    'selectors.html',
                    'signal.html',
                    'mmap.html',
                    'email.html',
                    'json.html',
                    'mailcap.html',
                    'mailbox.html',
                    'mimetypes.html',
                    'base64.html',
                    'binascii.html',
                    'quopri.html',
                    'uu.html',
                    'html.html',
                    'xml.html',
                    'urllib.html',
                    'http.html',
                    'ftplib.html',
                    'poplib.html',
                    'imaplib.html',
                    'nntplib.html',
                    'smtplib.html',
                    'smtpd.html',
                    'telnetlib.html',
                    'uuid.html',
                    'socketserver.html',
                    'xmlrpc.html',
                    'ipaddress.html',
                    'audioop.html',
                    'aifc.html',
                    'sunau.html',
                    'wave.html',
                    'chunk.html',
                    'colorsys.html',
                    'imghdr.html',
                    'sndhdr.html',
                    'ossaudiodev.html',
                    'gettext.html',
                    'locale.html',
                    'calendar.html',
                    'collections.html',
                    'heapq.html',
                    'bisect.html',
                    'array.html',
                    'weakref.html',
                    'types.html',
                    'copy.html',
                    'pprint.html',
                    'reprlib.html',
                    'enum.html',
                    'numbers.html',
                    'math.html',
                    'cmath.html',
                    'decimal.html',
                    'fractions.html',
                    'random.html',
                    'statistics.html',
                    'itertools.html',
                    'functools.html',
                    'operator.html',
                    'pathlib.html',
                    'fileinput.html',
                    'stat.html',
                    'filecmp.html',
                    'tempfile.html',
                    'glob.html',
                    'fnmatch.html',
                    'linecache.html',
                    'shutil.html',
                    'macpath.html',
                    'pickle.html',
                    'copyreg.html',
                    'shelve.html',
                    'marshal.html',
                    'dbm.html',
                    'sqlite3.html',
                    'zipfile.html',
                    'tarfile.html',
                    'csv.html',
                    'configparser.html',
                    'netrc.html',
                    'xdrlib.html',
                    'plistlib.html',
                    'hashlib.html',
                    'hmac.html',
                    'secrets.html'
                ]
            },
            'python_howto': {
                'base_url': 'https://docs.python.org/3/howto/',
                'guides': [
                    'index.html',
                    'logging.html',
                    'logging-cookbook.html',
                    'urllib2.html',
                    'regex.html',
                    'unicode.html',
                    'sorting.html',
                    'descriptor.html',
                    'functional.html',
                    'pyporting.html',
                    'argparse.html',
                    'curses.html',
                    'ipaddress.html',
                    'webservers.html',
                    'sockets.html',
                    'doanddont.html',
                    'indexing.html',
                    'advocacy.html',
                    'whatsnew.html',
                    'porting.html',
                    'cporting.html',
                    'curses.html',
                    'ipaddress.html',
                    'webservers.html',
                    'sockets.html',
                    'doanddont.html',
                    'indexing.html',
                    'advocacy.html',
                    'whatsnew.html',
                    'porting.html',
                    'cporting.html'
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
            '.documentation', '.body', '.document', '.chapter',
            '.section', '.body-content'
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
        
        for element in main_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'code', 'pre', 'blockquote', 'div']):
            text = element.get_text().strip()
            if text and len(text) > 10:
                if element.name.startswith('h'):
                    level = element.name[1]
                    text_content.append(f"\n{'#' * int(level)} {text}\n")
                elif element.name in ['code', 'pre']:
                    text_content.append(f"```python\n{text}\n```")
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
        """Scrape all configured Python documentation sources"""
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
        
        logger.info(f"Python scraping complete! {len(all_docs)} documents saved")
        return all_docs

if __name__ == "__main__":
    scraper = PythonDocScraper()
    docs = scraper.scrape_documentation()
