from fastapi import FastAPI
from .scraper.TennisCourtScraper import TennisCourtScraper
from .utils.urlMapper import urlMapper
import traceback
import time

app = FastAPI()

cache = {}  # key: location_id, value: (timestamp, data)
CACHE_TTL = 300

@app.get("/")
def root():
    return {"message": "Court Availability API is running 🚀"}

@app.get("/scrape/{location_id}")
async def scrape_parklands(location_id: int):
    try:
        now = time.time()

        # Check cache
        if location_id in cache:
            cached_time, cached_data = cache[location_id]
            if now - cached_time < CACHE_TTL:
                print("💾 Returning cached data")
                return cached_data
            else:
                print("⏰ Cache expired — scraping again")

        url = urlMapper.Map(location_id)
        scraper = TennisCourtScraper()
        results = await scraper.scrape(url, location_id)
        cache[location_id] = (now, results)
        return results
    except Exception as e:
        print("❌ Internal server error:")
        traceback.print_exc()
        return {"error": str(e)}