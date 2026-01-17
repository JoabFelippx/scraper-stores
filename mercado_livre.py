from bs4 import BeautifulSoup
import logging

from scraper.parser import ProductParser
from scraper.stores.base_store import BaseStore

logger = logging.getLogger(__name__)

class MercadoLivreSearch(BaseStore):
    
    def track_mercardolivre(self, product: str) -> BeautifulSoup:
        self.url = f"{self.base_url}{product.replace(' ', '-')}"
        html = self._fetch_html(self.url)

        soup = self._parse_html(html)
        return soup

    def get_title_info(self, product_soup: BeautifulSoup) -> str:
        title = product_soup.find("h3", class_="poly-component__title-wrapper").text
        return title

    def get_link_info(self, product_soup: BeautifulSoup) -> str:
        tag_link = product_soup.find("a", class_="poly-component__title")
        if tag_link:        
            link_raw = tag_link.get("href")
            return link_raw
        return "Link não encontrado"

    def get_current_price_info(self, product_soup: BeautifulSoup) -> list:
        current_price_whole_tag = product_soup.find("span", class_="andes-money-amount andes-money-amount--cents-superscript")
        if current_price_whole_tag:
            current_price_whole_text = current_price_whole_tag.find("span", class_="andes-money-amount__fraction").text
            current_price_cents = current_price_whole_tag.find("span", class_="andes-money-amount__cents")
            if current_price_cents:
                current_price_whole_text = f"{current_price_whole_text}  ,{current_price_cents.text}"
            else:
                current_price_whole_text = f"{current_price_whole_text},00"
            current_price = ProductParser.clean_price(current_price_whole_text)
            return current_price

    def get_old_price_info(self, product_soup: BeautifulSoup) -> list:
        old_price_whole_tag = product_soup.find("s", class_="andes-money-amount andes-money-amount--previous andes-money-amount--cents-comma")
        if old_price_whole_tag:
            old_price_whole_text = old_price_whole_tag.find("span", class_="andes-money-amount__fraction").text
            old_price_cents = old_price_whole_tag.find("span", class_="andes-money-amount__cents")
            if old_price_cents:
                old_price_whole_text = f"{old_price_whole_text}  ,{old_price_cents.text}"
            else:
                old_price_whole_text = f"{old_price_whole_text},00"
            old_price = ProductParser.clean_price(old_price_whole_text)
            return old_price
        return None        

    def construct_product_info(self, soup: BeautifulSoup) -> list:
        
        products = soup.find_all("li", class_="ui-search-layout__item")
        
        prod_list = []
        
        for product in products:
            
            title = self.get_title_info(product)
            link = self.get_link_info(product)

            old_price = self.get_old_price_info(product)
            current_price = self.get_current_price_info(product)
            
            discount = ProductParser.calculate_discount(old_price, current_price)
            
            prod_list.append({
                "title": title,
                "old_price": old_price,
                "current_price": current_price,
                "discount": discount,
                "link": link
            })
            
        return prod_list

    