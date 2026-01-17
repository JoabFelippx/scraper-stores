import json
import logging
import argparse
from datetime import datetime

from scraper.stores.mercado_livre import MercadoLivreSearch
from scraper.stores.magazine_luiza import MagazineLuizaSearch

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_headers():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    
def run_scraper(search_term: str):

    all_products = []
    headers = get_headers()
    
    logger.info(f"============== Iniciando busca por: '{search_term}' ==============")
    
    # try:
    #     mlivre = MercadoLivreSearch(headers, "https://lista.mercadolivre.com.br/")
            
    #     soup = mlivre.track_mercardolivre(search_term)
        
    #     if soup:
    #         mlivre_products = mlivre.construct_product_info(soup)
            
    #         for p in mlivre_products:
    #             p['store'] = 'Mercado Livre'
    #         all_products.extend(mlivre_products)
    #         logger.info(f"Mercado Livre retornou {len(mlivre_products)} produtos.")
    #     else:
    #             logger.warning("Mercado Livre não retornou dados.")
                
    # except Exception as e:
    #     logger.error(f"Erro ao buscar em Mercado Livre: {e}")
                
    try:
        mluiza = MagazineLuizaSearch(headers, "https://www.magazineluiza.com.br")
        
        soup = mluiza.track_magazineluiza(search_term)
        
        if soup:
            mluiza_products = mluiza.construct_product_info(soup)

    except Exception as e:
        logger.error(f"Erro ao buscar em Magazine Luiza: {e}")
    
    return all_products

def save_to_json(data: list, filename: str):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logger.info(f"Dados salvos em: {filename}")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Comparador de Preços Runner")
    parser.add_argument("search_term", type=str, nargs='?', default="iphone 13", help="Produto a ser buscado")
    parser.add_argument("--sort", choices=["price", "discount"], help="Ordenar resultados por 'price' ou 'discount'")
    parser.add_argument("--save", action="store_true", help="Salvar resultados em arquivo JSON")
    
    args = parser.parse_args()
    resultados = run_scraper(args.search_term)
    
    if args.sort and resultados:
        from scraper.parser import ProductParser
        if args.sort == "price":
            resultados = ProductParser.order_by_price(resultados)
        elif args.sort == "discount":
            resultados = ProductParser.order_by_discount(resultados)
    
    if args.save and resultados:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resultados_{args.search_term.replace(' ', '_')}_{timestamp}.json"
        save_to_json(resultados, filename)
