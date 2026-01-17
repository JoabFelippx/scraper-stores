import re

class ProductParser:
    
    @staticmethod
    def calculate_discount(original_price: float, current_price: float) -> float:
        if original_price and current_price:
            discount = ((original_price - current_price) / original_price) * 100
            return round(discount, 2)
        return 0.0
    
    @staticmethod
    def clean_price(price_str: str) -> float:
        price_str = re.sub(r'[^\d,]', '', price_str) 
        price_str = price_str.replace(',', '.') 
        try:
            return float(price_str)
        except ValueError:
            return 0.0
        
    @staticmethod
    def order_by_price(products: list) -> list:
        return sorted(products, key=lambda x: x["current_price"])

    @staticmethod
    def order_by_discount(products: list) -> list:
        return sorted(products, key=lambda x: x["discount"] if x["discount"] else 0, reverse=True)
    
    
    
    
    
    