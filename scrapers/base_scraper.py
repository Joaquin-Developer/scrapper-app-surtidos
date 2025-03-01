import logging
import time
import json
import sys
import os

from datetime import datetime
from typing import List, Dict, Any
from abc import ABC, abstractmethod

from playwright.sync_api import sync_playwright, Page

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


try:
    from utils import api
except ImportError:
    from ..utils import api

logging.basicConfig(level=logging.INFO)


class BaseScrapper(ABC):
    def __init__(
        self,
        domain: str,
        urls: List[str],
        wait_time: int = 3,
        save_in_json: bool = False,
        send_to_backend: bool = False
    ):
        self.domain = domain
        self.urls = urls
        self.wait_time = wait_time
        self.save_in_json = save_in_json
        self.send_to_backend = send_to_backend

        self.data: List[Dict[str, Any]] = []
        self._json_data: List[Dict[str, Any]] = []

    @abstractmethod
    def parse(self, page: Page) -> List[Dict[str, Any]]:
        raise NotImplementedError()

    def scroll_to_bottom(self, page: Page, scrolls=5, delay=3):
        for _ in range(scrolls):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(delay)

    def save_to_json(self):
        """Save extracted data in JSON file"""
        if not self.save_in_json:
            return

        output_file = f"data/raw/{self.__class__.__name__}_{datetime.now().strftime('%Y%m%d_%H:%M')}.json"
        logging.info("Total elements scrapped: %i", len(self.data))

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(self._json_data, file, ensure_ascii=False, indent=4)

    def send_data_to_backend(self):
        return api.send_data_to_backend(self.data)

    def _run(self, url: str) -> List[Dict[str, Any]]:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            logging.info(f"Scrapping: {url}")
            page.goto(url)

            logging.info("Scrolling to the bottom of the page...")
            self.scroll_to_bottom(page)

            logging.info("Waiting to load elements...")
            time.sleep(self.wait_time)

            logging.info("Extracting data...")
            data = self.parse(page)
            # self.data += data

            browser.close()
            return data

    def run(self):
        for _url in self.urls:
            url = self.domain + _url

            try:
                data = self._run(url)
                if not data:
                    continue
                self.data += data

                if self.save_in_json:
                    logging.info("Saving data in JSON...")
                    self._json_data.append({
                        "url": url,
                        "data": data
                    })

            except Exception as error:
                logging.warning("Failed scrapping for %s", url)
                logging.warning(str(error))

        self.save_to_json()

        if self.data and self.send_data_to_backend:
            logging.info("Send data to Backend...")
            self.send_data_to_backend()
        logging.info("End.")
