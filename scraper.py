from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import re
from CourtNumberMapper import CourtMapper
from SuburbMapper import SuburbMapper

# Setup options
options = Options()
#options.add_argument("--headless")  # Remove this line if you want to see the browser

# Set path to your ChromeDriver
chrome_driver_path = "D:\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

wait = WebDriverWait(driver, 15)

try:
    # Step 1: Visit locations page
    driver.get("https://www.citycommunitytennis.com.au/locations")

    court_url = 'https://jensenstennis.intrac.com.au/tennis/book.cfm?facility='

    for i in range(1, 6):
        try:
            print(i)
            if(i <= 4):
                book_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, f"//a[text()='Book' and contains(@href, 'https://jensenstennis.intrac.com.au/tennis/book.cfm?facility={i}')]"
                )))
            else:
                book_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, f"//a[text()='Book' and contains(@href, 'https://jensenstennis.intrac.com.au/tennis/book.cfm?location=6&court=283')]"
                )))

            book_button.click()

            driver.switch_to.window(driver.window_handles[-1])

            # Step 3: Wait for new booking site to load
            wait.until(EC.url_contains("jensenstennis.intrac.com.au"))

            SuburbName = SuburbMapper.Map(i)
            print(f"➡️ Suburb: {SuburbName}")

            time.sleep(1)


            # Step 4: Get all .cal elements and extract date URLs
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.cal")))
            cal_cells = driver.find_elements(By.CSS_SELECTOR, "td.cal")

            today = datetime.date.today().day
            today_full = datetime.date.today().strftime('%Y-%m-%d')
            if i == 5:
                today_url = "https://jensenstennis.intrac.com.au/tennis/book.cfm?location=6&court=283"
            else:
                today_url = f"https://jensenstennis.intrac.com.au/tennis/book.cfm?location={i+1}&date={today_full}"
            selected_dates = [today_url]

            for cell in cal_cells:
                try:
                    link = cell.find_element(By.TAG_NAME, "a")
                    href = link.get_attribute("href")
                    date_str = href.split("-")[2][:2]
                    date_num = int(date_str.lstrip('0'))
                    if date_num >= today:
                        selected_dates.append(href)
                except Exception as e:
                    continue
                
            selected_dates = selected_dates[:7]
                
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.book")))
            book_cells = driver.find_elements(By.CSS_SELECTOR, "td.book")

            available_times = []
                
            for date_url in selected_dates:
                driver.get(date_url)
                date_str = date_url.split("date=")[-1]
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.book")))
                book_cells = driver.find_elements(By.CSS_SELECTOR, "td.book")
                for cell in book_cells:
                    try:
                        link = cell.find_element(By.TAG_NAME, "a")
                        href = link.get_attribute("href")
                        court = href.split("court=")[-1].split("%")[0]
                        courtMapper = CourtMapper()
                        court = courtMapper.Map(int(court))
                        time_text = link.text.strip().split(" ")[-1]
                    
                        if time_text:
                            available_times.append(time_text)
                            print("✅ Available:", date_str, "Court ", court, " at", time_text)
                            

                    except Exception as e:
                        continue
            driver.close()
            driver.switch_to.window(driver.window_handles[0])        
            time.sleep(1)
            selected_dates = []
        except Exception as e:
            print(e)
            continue

finally:
    driver.quit()