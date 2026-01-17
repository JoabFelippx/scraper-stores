from scraper.stores.mercado_livre import MercadoLivreSearch

def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    
    base_url = "https://lista.mercadolivre.com.br/"    
    
    product_name = "camisa"
    
    mercado_livre_search = MercadoLivreSearch(headers, base_url)
        
    soup = mercado_livre_search.track_mercardolivre(product_name)
    
    if soup:
        products_info = mercado_livre_search.construct_product_info(soup)
        
        for product in products_info:
            print(product)

if __name__ == "__main__":
    main()
    