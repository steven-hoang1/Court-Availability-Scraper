from .baseScraper import BaseScraper
import httpx
from ..domain.availability import Availability
import datetime

class FullagarRoadScraper(BaseScraper):
    async def scrape(self, url, location_number):
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Origin": "https://play.tennis.com.au",
            "Referer": "https://play.tennis.com.au/court-hire/FullagarRoadTennisCourts",
        }

        results = []

        async with httpx.AsyncClient(timeout=20) as client:
            for j in range(0, 7):  # today + next 6 days
                date = (datetime.date.today() + datetime.timedelta(days=j)).strftime(
                    "%Y-%m-%d"
                )

                payload = {
                    "id": "Web_Ta_PublicVenueCourtHireAvailability",
                    "variables": {
                        "location": {"latitude": -37.8136, "longitude": 144.9631},
                        "earliestStart": 0,       # midnight
                        "latestStart": 1439,      # end of day
                        "duration": "60",
                        "date": date,
                        "pageSize": 20,
                        "pageNo": 1,
                        "ocsPageNo": 1,
                        "venueId": "8a670866-2fb4-4ad8-8f6a-91072c3cc00d",
                        "timeRange": True,
                        "slotTypes": ["RESOURCE"],
                    },
                }

                try:
                    response = await client.post(
                        url, headers=headers, json=payload
                    )
                    response.raise_for_status()
                except httpx.HTTPStatusError as e:
                    print(f"❌ HTTP error {e.response.status_code} on {date}")
                    continue

                data = response.json()


                slots = (
                    data.get("data", {})
                    .get("venueAvailability", {})
                    .get("allSlots", [])
                )

                for slot in slots:
                    start_minutes = slot.get("startTime")
                    if start_minutes is None:
                        continue

                    # Convert minutes since midnight to HH:MM
                    hours = start_minutes // 60
                    minutes = start_minutes % 60
                    time_str = f"{hours:02d}:{minutes:02d}"

                    courts_available = slot.get("totalResourceSlots", 0)

                    results.append(
                        Availability(
                            date=slot.get("date"),
                            time=time_str,
                            courts_available=courts_available,
                        )
                    )

        return results
    