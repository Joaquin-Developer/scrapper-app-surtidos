from scrapers.geant import Geant


SCRAPERS = [
    Geant,
]


def main():
    for scraper in SCRAPERS:
        scraper().run()


if __name__ == "__main__":
    main()
