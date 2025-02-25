from base_scraper import BaseScrapper, Page


class Geant(BaseScrapper):
    def parse(self, page: Page):
        articles = page.query_selector_all(
            ".vtex-product-summary-2-x-element.pointer.pt3.pb4.flex.flex-column.h-100"
        )

        for article in articles:
            name = article.query_selector(".vtex-product-summary-2-x-productBrand").inner_text()
            image = article.query_selector("img")
            image_link = image.get_attribute("src") if image else None

            price = article.query_selector(".devotouy-products-components-0-x-sellingPriceWithUnitMultiplier")
            price = price.inner_text().replace("\n", " ") if price else None

            self.data.append({
                "name": name,
                "price": price,
                "image_link": image_link
            })


if __name__ == "__main__":
    url = "https://www.geant.com.uy/frescos/congelados/pre-fritos-rebozados"
    scraper = Geant(url=url, save_in_json=True)
    scraper.run()
