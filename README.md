# scrapper-app-surtidos

A web scraper application built with Python to extract product names, urls and prices from multiples e-commerce platforms.

## Technologies Used

- Python
- Playwright

## Installation

### Prerequisites

- Python 3.8+
- Virtual env (recommended). Visit [venv doc](https://docs.python.org/es/dev/library/venv.html)

### Setup

- Clone the repository. `git clone https://github.com/Joaquin-Developer/scrapper-app-surtidos`
- Execute setup script. `./setup.sh`

## Usage

Start application for all scrappers:

```bash
./start.sh
```

Start the app in development mode. (Saves data to a local JSON file and does not send data to the backend API.)

```bash
./start_dev.sh
```

Run a specific scrapper:

```bash
# example: Geant
python3 scrapers/geant.py
```

## Contributing

Pull requests are welcome. Please open an issue for discussion before making changes.

## License

This project is licensed under the MIT License.
 
🚀 Happy Scraping!
