from abc import ABC, abstractmethod

class BaseScraper(ABC):
    @abstractmethod
    async def scrape(self, url: str, location_number: int):
        """Return a list of Availability objects"""
        pass