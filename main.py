import asyncio
from TennisCourtScraper import TennisCourtScraper

CityCommunityTennisUrl = "https://jensenstennis.intrac.com.au/tennis/book.cfm?location="
ParklandsUrl = "https://parklands.intrac.com.au/sports/schedule.cfm?location="

async def main():
    scraper = TennisCourtScraper()
    results = await scraper.scrape(CityCommunityTennisUrl, 4)

asyncio.run(main())