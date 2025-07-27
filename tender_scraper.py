from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException

import pandas as pd
import time


def selenium_web_driver() -> webdriver : 
    options = Options()  # Configure Selenium
    options.add_argument('--headless')  # Run browser in headless mode (no GUI)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    return driver


# Website from where the data should extract
WEBPATH: str = "https://etender.cpwd.gov.in"

# Total no of Record we Extract(Options:- 10,20,40,50,100)
no_of_Records: int = 20

# Sleep time between requests
sleep_time: int = 3

# Dictionary to rename the columns
csv_columns: dict = {
    "NIT/RFP NO": "ref_no",
    "Name of Work / Subwork / Packages": "title",
    "Estimated Cost": "tender_value",
    "Bid Submission Closing Date & Time": "bid_submission_end_date",
    "EMD Amount": "emd",
    "Bid Opening Date & Time": "bid_open_date"
}

try:
    # Create a Web driver for page rendering because the Website is JavaScript rendered
    driver: webdriver = selenium_web_driver() 

    # Step 1: Open website
    driver.get(WEBPATH)
    time.sleep(sleep_time)  # Let page load fully

    # Step 2: Waits for any alert if Pop-up
    try:
        WebDriverWait(driver, sleep_time).until(EC.alert_is_present())  # wait 3 seconds for alert Pop-up if any
        alert = driver.switch_to.alert
        alert.accept()  # Click OK on alert if Pop-up
    except NoAlertPresentException:
        pass # Pass if no Pop-up appear


    # Step 3: Click on "All" under New Tenders
    all_link = driver.find_element(By.ID, "a_TenderswithinOneday3")
    all_link.click()
    time.sleep(sleep_time) # wait for loading of table


    # Step 4: Find the dropdown that controls rows per page
    select_element = driver.find_element(By.NAME, "awardedDataTable_length")
    select = Select(select_element)
    select.select_by_value(f"{no_of_Records}")  # Select 20 rows per page
    time.sleep(sleep_time)  # wait for table to reload with 20 rows


    # Step 5: Wait until table rows are loaded
    WebDriverWait(driver, no_of_Records).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#awardedDataTable tbody tr"))
    )
    time.sleep(sleep_time-1)  # Additional wait for stable loading

    # Step 6: Scrape first 20 rows
    tenders = []
    rows = driver.find_elements(By.CSS_SELECTOR, "#awardedDataTable tbody tr")[:no_of_Records]

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) >= 6:
            tender_data = {
                "NIT/RFP NO": cells[1].text.strip(),
                "Name of Work / Subwork / Packages": cells[2].text.strip(),
                "Estimated Cost": cells[4].text.strip(),
                "Bid Submission Closing Date & Time": cells[6].text.strip(),
                "EMD Amount": cells[5].text.strip(),
                "Bid Opening Date & Time": cells[7].text.strip()
            }
            tenders.append(tender_data)

    # Step 7: Save to CSV
    df = pd.DataFrame(tenders)
    df.rename(columns=csv_columns, inplace=True)
    df.to_csv("new_tenders_data.csv", index=False)

    print("Data saved to new_tenders_data.csv")

except:
    print("Connection/Extraction Failed")

finally:
    # Step 8: Close browser regardless of success or failure to prevent memory leak
    driver.quit()
