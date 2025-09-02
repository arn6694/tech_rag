#!/usr/bin/env python3
"""
Enhanced PDF Processing with Smart Text Extraction
"""

import fitz  # PyMuPDF
import pdfplumber
import os
import json
from datetime import datetime
from pathlib import Path
import logging
import re

logger = logging.getLogger(__name__)

class EnhancedPDFProcessor:
    def __init__(self, technology_name: str):
        self.technology_name = technology_name
        
    def extract_metadata(self, pdf_path: Path) -> dict:
        """Extract comprehensive PDF metadata"""
        try:
            doc = fitz.open(str(pdf_path))
            metadata = doc.metadata
            
            # Get additional info
            page_count = doc.page_count
            file_size = pdf_path.stat().st_size
            
            doc.close()
            
            return {
                'filename': pdf_path.name,
                'file_size': file_size,
                'file_size_mb': round(file_size / (1024*1024), 2),
                'page_count': page_count,
                'title': metadata.get('title', ''),
                'author': metadata.get('author', ''),
                'subject': metadata.get('subject', ''),
                'creator': metadata.get('creator', ''),
                'producer': metadata.get('producer', ''),
                'creation_date': metadata.get('creationDate', ''),
                'modification_date': metadata.get('modDate', ''),
                'processed_at': datetime.now().isoformat(),
                'technology': self.technology_name,
                'source_type': 'pdf'
            }
        except Exception as e:
            logger.error(f"Error extracting metadata from {pdf_path}: {e}")
            return {'filename': pdf_path.name, 'error': str(e)}
    
    def clean_pdf_text(self, text: str) -> str:
        """Clean and normalize extracted PDF text"""
        if not text:
            return ""
        
        # Split into lines for processing
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Skip common header/footer patterns
            if self.is_header_footer_line(line):
                continue
            
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def is_header_footer_line(self, line: str) -> bool:
        """Check if line is a header/footer pattern"""
        line_lower = line.lower()
        header_footer_patterns = [
            'page', 'chapter', 'section', 'figure', 'table',
            'copyright', 'all rights reserved', 'confidential'
        ]
        return any(pattern in line_lower for pattern in header_footer_patterns)
    
    def process_pdf(self, pdf_path: Path) -> dict:
        """Process a PDF file and return structured data"""
        try:
            logger.info(f"Processing PDF: {pdf_path.name}")
            
            # Extract metadata
            metadata = self.extract_metadata(pdf_path)
            
            # Extract text content
            text_content = self.extract_text_pymupdf(pdf_path)
            
            # Clean the text
            cleaned_text = self.clean_pdf_text(text_content)
            
            return {
                'metadata': metadata,
                'content': cleaned_text,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path}: {e}")
            return {
                'metadata': {'filename': pdf_path.name, 'error': str(e)},
                'content': '',
                'success': False
            }
