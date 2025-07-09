import datetime
from collections import defaultdict
from ..domain.availability import Availability
import httpx
from bs4 import BeautifulSoup

class TennisCourtScraper:
    async def scrape(self, url, location_number):
        aest_now = datetime.datetime.now() + datetime.timedelta(hours=10)
        today_date = aest_now.strftime('%Y-%m-%d')

        if location_number == 6 and "jensenstennis" in url:
            full_url = f"{url}{location_number}&date={today_date}&court=283"
        else:
            full_url = f"{url}{location_number}&date={today_date}"

        async with httpx.AsyncClient(timeout=20) as client:
            selected_dates = [full_url]
            for j in range(1, 7):
                date = (datetime.date.today() + datetime.timedelta(days=j)).strftime('%Y-%m-%d')
                if location_number == 6:
                    date_url = f"{url}{location_number}&date={date}&court=283"
                else:
                    date_url = f"{url}{location_number}&date={date}"
                selected_dates.append(date_url)

            results = []

            for date_url in selected_dates:
                try:
                    response = await client.get(date_url)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, "html.parser")
                    time_slots = defaultdict(int)
                    book_cells = soup.select("td.book")

                    for cell in book_cells:
                        try:
                            link = cell.find("a")
                            if link:
                                href = link.get("href", "")
                                if "start=" in href:
                                    start_time = href.split("start=")[-1].split("&")[0]
                                    time_slots[start_time] += 1
                        except:
                            continue
                except Exception as e:
                    print(e)

                for time_str, count in sorted(time_slots.items()):
                    results.append(Availability(
                        date=date_url.split('date=')[-1][:10],
                        time=time_str,
                        courts_available=count,
                    ))

            return results
