from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
from .SuburbMapper import SuburbMapper
from .CourtNumberMapper import CourtMapper


class CityCommTennisScraper:
    def __init__(self):
        # Setup options
        options = Options()
        options.add_argument("--headless=new")  # Remove this line if you want to see the browser

        # Set path to your ChromeDriver
        chrome_driver_path = "D:\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
        self.service = Service(executable_path=chrome_driver_path)
        self.driver = webdriver.Chrome(service=self.service, options=options)
        self.wait = WebDriverWait(self.driver, 15)
        self.available_times = []
    
    def scrape(self):
        try:
            today_full = datetime.date.today().strftime('%Y-%m-%d')
            # Step 1: Visit locations page
            for i in range(2, 7):
                try:
                    if i == 6:
                        self.driver.get(f"https://jensenstennis.intrac.com.au/tennis/book.cfm?location=6&date={today_full}&court=283")
                    else:
                        self.driver.get(f"https://jensenstennis.intrac.com.au/tennis/book.cfm?location={i}&date={today_full}")

                    SuburbName = SuburbMapper.Map(i)
                    print(f"➡️ Suburb: {SuburbName}")
                    time.sleep(1)

                    selected_dates = [self.driver.current_url]

                    for j in range(1,7):
                        try:
                            date = (datetime.date.today() + datetime.timedelta(days=j)).strftime('%Y-%m-%d')
                            if i == 6:
                                date_url = f"https://jensenstennis.intrac.com.au/tennis/book.cfm?location=6&date={date}&court=283"
                            else:
                                date_url = f"https://jensenstennis.intrac.com.au/tennis/book.cfm?location={i}&date={date}"
                            selected_dates.append(date_url)
                        except Exception as e:
                            print(e)
                            continue
                            
                    available_times = []
                        
                    for date_url in selected_dates:
                        self.driver.get(date_url)
                        date_str = date_url.split("date=")[-1][:10]
                        self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.book")))
                        book_cells = self.driver.find_elements(By.CSS_SELECTOR, "td.book")
                        for cell in book_cells:
                            try:
                                link = cell.find_element(By.TAG_NAME, "a")
                                href = link.get_attribute("href")
                                court = href.split("court=")[-1].split("%")[0]
                                court = CourtMapper.Map(int(court))
                                time_text = link.text.strip().split(" ")[-1]
                            
                                if time_text:
                                    available_times.append(time_text)
                                    print("✅ Available:", date_str, "Court ", court, " at", time_text)
                                    
                            except Exception as e:
                                continue
                    time.sleep(1)
                    selected_dates = []
                except Exception as e:
                    print(e)
                    continue

        finally:
            self.driver.quit()