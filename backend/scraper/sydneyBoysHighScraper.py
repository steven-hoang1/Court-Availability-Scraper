from .baseScraper import BaseScraper
import httpx
from ..domain.availability import Availability
import datetime
from bs4 import BeautifulSoup
from collections import defaultdict

class SydneyBoysHighScraper(BaseScraper):
    async def scrape(self, url, location_number):
        headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
            "Referer": "https://www.tennisvenues.com.au/booking/sydney-boys-high-school",
            "X-Requested-With": "XMLHttpRequest",
        }

        results = []

        async with httpx.AsyncClient(timeout=20) as client:
            for j in range(0, 7):  # today + next 6 days
                date = (datetime.date.today() + datetime.timedelta(days=j)).strftime(
                    "%Y%m%d"  # format required by API
                )

                full_url = f"{url}?client_id=sydney-boys-high-school&venue_id=2409&resource_id=&date={date}&_=1756078644462"
                

                try:
                    response = await client.get(full_url, headers=headers)
                    response.raise_for_status()
                except httpx.HTTPStatusError as e:
                    print(f"❌ HTTP error {e.response.status_code} on {date}")
                    continue

                soup = BeautifulSoup(response.text, "html.parser")


                book_cells = soup.select("td.TimeCell.Available")

                time_slots = defaultdict(int)

                for cell in book_cells:
                        try:
                            link = cell.find("a")
                            if link:
                                href = link.get("href", "")
                                if "t=" in href:
                                    start_time = href.split("t=")[-1].split("&")[0]
                                    formatted_start_time = start_time[:2] + ":" + start_time[2:]
                                    time_slots[formatted_start_time] += 1
                        except Exception as e:
                            continue

                formattedDate = f"{date[:4]}-{date[4:6]}-{date[6:]}"

                for time_str, count in sorted(time_slots.items()):
                    results.append(Availability(
                        date=formattedDate,
                        time=time_str,
                        courts_available=count,
                    ))

        return results        