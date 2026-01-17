import httpx
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class BaseStore:
    def __init__(self, headers: dict, base_url: str):
        self.headers = headers
        self.base_url = base_url
        self.current_url = ""
        
    def _fetch_html(self, url) -> str:
        self.current_url = url
        try:
            response = httpx.get(url, headers=self.headers, timeout=15.0)
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as e:
            logger.error(f"Error fetching HTML from {url}: {e}")
            return None
    
    def _parse_html(self, html: str) -> BeautifulSoup:
        soup = BeautifulSoup(html, "html.parser")
        return soup
    
        
        