from bs4 import BeautifulSoup
import logging

from scraper.parser import ProductParser
from scraper.stores.base_store import BaseStore

# AINDA NÃO FINALIZADO
logger = logging.getLogger(__name__)

class MagazineLuizaSearch(BaseStore):
    
    def track_magazineluiza(self, product: str) -> BeautifulSoup:
        self.url = f"{self.base_url}/busca/{product.replace(' ', '+')}/"
        html = self._fetch_html(self.url)
        
        soup = self._parse_html(html)
        return soup
    
    def get_title_info(self, product_soup: BeautifulSoup) -> str:
        title = product_soup.find("h2", class_="sc-ksCcjW bohfAy").text
        return title
    
    def get_link_info(self, product_soup: BeautifulSoup) -> str:
        link_path = product_soup.find("a", class_="sc-fHjqPf eXlKzg sc-cYxjnA eeTzEb sc-cYxjnA eeTzEb").get("href")
        link = self.base_url + link_path
        return link
    
    def construct_product_info(self, soup: BeautifulSoup) -> list:
        
        products = soup.find_all("ul", class_="sc-cWSHoV kRWXIt sc-fAGzit CKWPN sc-fgSWkL qZclM")
        # print(products)
        prod_list = []
        
        for product in products[:1]:
            
            title = self.get_title_info(product)
            link = self.get_link_info(product)
            print(title)    
            print(link)
                
        return [1, 2 , 3]
