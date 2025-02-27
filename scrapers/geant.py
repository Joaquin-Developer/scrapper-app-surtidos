from base_scraper import BaseScrapper, Page


class Geant(BaseScrapper):
    SUPERMARKET_CHAIN_ID = 1

    def parse(self, page: Page):
        articles = page.query_selector_all(
            ".vtex-product-summary-2-x-element.pointer.pt3.pb4.flex.flex-column.h-100"
        )

        # TODO permitir ean null en el backend
        ean = 1111

        for article in articles:
            name = article.query_selector(".vtex-product-summary-2-x-productBrand").inner_text()
            image = article.query_selector("img")
            image_link = image.get_attribute("src") if image else None

            price = article.query_selector(".devotouy-products-components-0-x-sellingPriceWithUnitMultiplier")
            price = price.inner_text().replace("\n", " ") if price else None

            self.data.append({
                "ean": str(ean),
                "name": name,
                "imageLink": image_link,
                "currency": price.split(" ")[0],
                "price": price.split(" ")[1],
                "supermarketChainId": self.SUPERMARKET_CHAIN_ID,
            })
            ean += 1


if __name__ == "__main__":
    url = "https://www.geant.com.uy/frescos/congelados/pre-fritos-rebozados"
    scraper = Geant(url=url, save_in_json=True)
    scraper.run()
