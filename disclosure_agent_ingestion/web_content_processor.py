import requests
import json
from bs4 import BeautifulSoup
from typing import Dict, Any
import os
from datetime import datetime
from markdownify import markdownify as md

from disclosure_agent_ingestion.content_analysis import ContentAnalysisEngine


analysis_engine = ContentAnalysisEngine()


class WebContentProcessor:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def html_to_markdown(self, html_content: str) -> str:
        """
        Converts HTML content to Markdown format
        """
        try:
            # Convert HTML to markdown using markdownify
            markdown_content = md(html_content,
                                  heading_style="ATX",      # Use # style headings
                                  bullets="-",              # Use - for unordered lists
                                  code_language="python",   # Default language for code blocks
                                  strip=['script', 'style', 'form',
                                         'iframe']  # Elements to remove
                                  )

            return markdown_content.strip()

        except Exception as e:
            print(f"Error converting HTML to Markdown: {e}")
            return None

    def scrape_url(self, url: str) -> Dict[str, Any]:
        """
        Scrapes content from a URL using similar logic to firecrawl.dev
        Returns structured content including metadata
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract key elements
            title = soup.title.string if soup.title else ""

            # Get main content (prioritize article or main content areas)
            main_content = soup.find('article') or soup.find(
                'main') or soup.find('body')

            # Remove unwanted elements
            for element in main_content.find_all(['script', 'style', 'nav', 'header', 'footer', 'iframe']):
                element.decompose()

            # Extract text content
            content = main_content.get_text(separator='\n', strip=True)
            print(content)
            # Convert to markdown
            markdown_content = self.html_to_markdown(str(main_content))

            # Extract metadata
            metadata = {
                'url': url,
                'title': title,
                'timestamp': datetime.now().isoformat(),
                'length': len(content)
            }

            return {
                'metadata': metadata,
                'content': content,
                'markdown': markdown_content,
                'html': str(main_content)
            }

        except Exception as e:
            print(f"Error scraping URL: {e}")
            return None


def process_url(url: str) -> Dict[str, Any]:
    """
    Process a URL and return the formatted content with multiple formats
    """
    processor = WebContentProcessor()
    processed_content = processor.scrape_url(url)

    if processed_content:
        content = processed_content['content']
        metadata = processed_content['metadata']
        summary = analysis_engine.analyze_content(content)

        print(summary)

        return {
            'content': content,
            'markdown': processed_content['markdown'],
            'html': processed_content['html'],
            'metadata': metadata,
            'summary': summary
        }

    return None
