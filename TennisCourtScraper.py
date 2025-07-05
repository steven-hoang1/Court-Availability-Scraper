from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
from SuburbMapper import SuburbMapper
from collections import defaultdict

class TennisCourtScraper:
    def __init__(self):
        # Setup options
        options = Options()
        options.add_argument("--headless=new")  # Remove this line if you want to see the browser

        # Set path to your ChromeDriver
        chrome_driver_path = "D:\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
        self.service = Service(executable_path=chrome_driver_path)
        self.driver = webdriver.Chrome(service=self.service, options=options)
        self.wait = WebDriverWait(self.driver, 15)
    
    def scrape(self, url, locationNumber):
        try:
            today_date = datetime.date.today().strftime('%Y-%m-%d')
            full_url = f"{url}{locationNumber}&date={today_date}&court=283" if (locationNumber == 6 and "jensenstennis" in url) else f"{url}{locationNumber}&date={today_date}"
            
            try:
                self.driver.get(full_url)
                SuburbName = SuburbMapper.Map(locationNumber)
                print(f"➡️ Suburb: {SuburbName}")
                time.sleep(1)

                selected_dates = [self.driver.current_url]

                for j in range(1,7):
                    try:
                        date = (datetime.date.today() + datetime.timedelta(days=j)).strftime('%Y-%m-%d')
                        if locationNumber == 6:
                            date_url = f"{url}{locationNumber}&date={date}&court=283"
                        else:
                            date_url = f"{url}{locationNumber}&date={date}"
                        selected_dates.append(date_url)
                    except Exception as e:
                        print(e)
                        continue
                        
                    
                for date_url in selected_dates:
                    self.driver.get(date_url)
                    self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.book")))
                    book_cells = self.driver.find_elements(By.CSS_SELECTOR, "td.book")

                    time_slots = defaultdict(int)

                    for cell in book_cells:
                        try:
                            link = cell.find_element(By.TAG_NAME, "a")
                            href = link.get_attribute("href")

                            # Extract time from href, e.g. "start=07:00"
                            if "start=" in href:
                                start_time = href.split("start=")[-1].split("&")[0]  # → "07:00"
                                time_slots[start_time] += 1
                        except Exception as e:
                            continue
                # Print all time slots with court count
                    for time_str, count in sorted(time_slots.items()):
                        print(f"✅ {count} court(s) available at {time_str} on {date_url.split('date=')[-1][:10]}")
                
                time.sleep(1)
                selected_dates = []
            except Exception as e:
                print(e)

        finally:
            self.driver.quit()