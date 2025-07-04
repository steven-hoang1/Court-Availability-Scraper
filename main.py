from CityCommTennis.CityCommTennisScraper import CityCommTennisScraper

scraper = CityCommTennisScraper()

try:
    results = scraper.scrape()
finally:
    scraper.close()