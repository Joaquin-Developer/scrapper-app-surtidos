import logging
import time
import json
from datetime import datetime
from typing import List, Any
from abc import ABC, abstractmethod

from playwright.sync_api import sync_playwright, Page

logging.basicConfig(level=logging.INFO)


class BaseScrapper(ABC):
    def __init__(self, url: str, wait_time: int = 3, save_in_json: bool = False):
        self.url = url
        self.wait_time = wait_time
        self.save_in_json = save_in_json
        self.data: List[Any] = []

    @abstractmethod
    def parse(self, page: Page):
        raise NotImplementedError()

    def run(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            logging.info(f"Scrapping: {self.url}")
            page.goto(self.url)

            logging.info("Scrolling to the bottom of the page...")
            self.scroll_to_bottom(page)

            logging.info("Waiting to load elements...")
            time.sleep(self.wait_time)

            logging.info("Extracting data...")
            self.parse(page)

            logging.info("Saving data in JSON...")
            self.save_to_json()

            browser.close()
            logging.info("End.")

    def scroll_to_bottom(self, page: Page, scrolls=5, delay=3):
        for _ in range(scrolls):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(delay)

    def save_to_json(self):
        """Guarda los datos extraídos en un archivo JSON."""
        if not self.save_in_json:
            print(self.data)
            return

        output_file = f"data/raw/{self.__class__.__name__}_{datetime.now().strftime('%Y%m%d_%H:%M')}.json"

        json_data = {
            "url": self.url,
            "data": self.data
        }

        logging.info("Total elements scrapped: %i", len(self.data))

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(json_data, file, ensure_ascii=False, indent=4)
