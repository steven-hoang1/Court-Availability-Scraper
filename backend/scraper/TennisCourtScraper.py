from .centralSydneyScraper import CentralSydneyScraper
from .fullagarRoadScraper import FullagarRoadScraper

class TennisCourtScraper:
    async def scrape(self, url, location_number):
        if location_number == 100:
            return await FullagarRoadScraper().scrape(url, location_number)
        
        centralSydneyResults = await CentralSydneyScraper().scrape(url, location_number)
        return centralSydneyResults

