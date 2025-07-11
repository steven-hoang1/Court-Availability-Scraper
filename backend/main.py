from fastapi import FastAPI
from .scraper.TennisCourtScraper import TennisCourtScraper
from .utils.urlMapper import urlMapper
import traceback
import time
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
import asyncio

app = FastAPI()

origins = [
    "https://lastminutetennis.netlify.app",
    "http://localhost:5173",  # for local dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cache = {}  # key: location_id, value: (timestamp, data)
CACHE_TTL = 300

@app.get("/")
def root():
    return {"message": "Court Availability API is running 🚀"}

@app.get("/location/all")
async def scrape_all():
    try:
        location_ids = [2, 3, 4, 5, 6, 55, 72, 43, 70]
        results = []
        for location_id in location_ids:
            result = await get_data(location_id)
            results.append(result)
        return results
    except Exception as e:
        print("❌ Internal server error:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/location/{location_id}")
async def scrape_parklands(location_id: int):
    try:
        return await get_data(location_id)
    except Exception as e:
        print("❌ Internal server error:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
async def get_data(location_id):
    now = time.time()
    if location_id in cache:
        cached_time, cached_data = cache[location_id]
        if now - cached_time < CACHE_TTL:
            return {"location_id": location_id, "data": cached_data}
    url = urlMapper.Map(location_id)
    scraper = TennisCourtScraper()
    data = await scraper.scrape(url, location_id)
    cache[location_id] = (now, data)
    return {"location_id": location_id, "data": data}