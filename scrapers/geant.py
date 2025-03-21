from typing import List, Dict, Any

try:
    from scrapers.base_scraper import BaseScrapper, Page
except ImportError:
    from base_scraper import BaseScrapper, Page

from config import config


class Geant(BaseScrapper):
    SUPERMARKET_CHAIN_ID = 1

    def parse(self, page: Page) -> List[Dict[str, Any]]:
        data = []
        articles = page.query_selector_all(
            ".vtex-product-summary-2-x-element.pointer.pt3.pb4.flex.flex-column.h-100"
        )

        for article in articles:
            name = article.query_selector(".vtex-product-summary-2-x-productBrand").inner_text()
            image = article.query_selector("img")
            image_link = image.get_attribute("src") if image else None

            price = article.query_selector(".devotouy-products-components-0-x-sellingPriceWithUnitMultiplier")
            price = price.inner_text().replace("\n", " ") if price else None

            data.append({
                "name": name,
                "imageLink": image_link,
                "currency": price.split(" ")[0],
                "price": price.split(" ")[1].replace(".", ""),
                "supermarketChainId": self.SUPERMARKET_CHAIN_ID,
            })
        return data


if __name__ == "__main__":
    domain = "https://www.geant.com.uy"
    urls = [
        # "/frescos/congelados/pescados-congelados",
        "/frescos",
        "/bebidas",
        "/almacen",
        "/perfumeria-y-limpieza/limpieza",
    ]
    is_test = config.DEBUG
    print("is_test", not is_test)
    scraper = Geant(domain=domain, urls=urls, save_in_json=True, send_to_backend=(not is_test))
    scraper.run()
