from CityCommTennis.CityCommTennisScraper import CityCommTennisScraper
from CentennialParklands.ParklandsScraper import ParklandsScraper

# scraper = CityCommTennisScraper()
# results = scraper.scrape()

results_55 = ParklandsScraper().scrape(55)
results_72 = ParklandsScraper().scrape(72)

