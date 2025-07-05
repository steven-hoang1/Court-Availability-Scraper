import datetime
from collections import defaultdict
from SuburbMapper import SuburbMapper
from playwright.async_api import async_playwright


class TennisCourtScraper:
    async def scrape(self, url, location_number):
        today_date = datetime.date.today().strftime('%Y-%m-%d')

        if location_number == 6 and "jensenstennis" in url:
            full_url = f"{url}{location_number}&date={today_date}&court=283"
        else:
            full_url = f"{url}{location_number}&date={today_date}"

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(full_url)

            suburb_name = SuburbMapper.Map(location_number)
            print(f"➡️ Suburb: {suburb_name}")

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
                await page.goto(date_url)
                await page.wait_for_selector("td.book", timeout=10000)

                time_slots = defaultdict(int)
                book_cells = await page.query_selector_all("td.book")

                for cell in book_cells:
                    try:
                        link = await cell.query_selector("a")
                        if link:
                            href = await link.get_attribute("href")
                            if "start=" in href:
                                start_time = href.split("start=")[-1].split("&")[0]
                                time_slots[start_time] += 1
                    except:
                        continue

                for time_str, count in sorted(time_slots.items()):
                    print(f"✅ {count} court(s) available at {time_str} on {date_url.split('date=')[-1][:10]}")
                    results.append((time_str, count))

            await browser.close()
            return results
