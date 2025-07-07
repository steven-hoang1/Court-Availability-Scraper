from fastapi import FastAPI
from .scraper.TennisCourtScraper import TennisCourtScraper
from .utils.urlMapper import urlMapper
import traceback

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Court Availability API is running 🚀"}

@app.get("/scrape/{location_id}")
async def scrape_parklands(location_id: int):
    try:
        url = urlMapper.Map(location_id)
        scraper = TennisCourtScraper()
        results = await scraper.scrape(url, location_id)
        return results
    except Exception as e:
        print("❌ Internal server error:")
        traceback.print_exc()
        return {"error": str(e)}