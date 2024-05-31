from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd

# Set up the webdriver
driver_path = 'chromedriver-mac-x64/chromedriver'
driver = webdriver.Chrome(driver_path)
driver.get('https://coinness.com/search?q=BTC&category=news')

# Wait for the page to load
wait = WebDriverWait(driver, 10)

def can_click_more():
    try:
        more_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "ButtonWrapper-sc-yv8mac-0 bZOMD")]')))
        more_button.click()
        return True
    except (TimeoutException, NoSuchElementException):
        return False

# Function to save news data to CSV file using Pandas
def save_to_csv(news_data, filename='news_data_coinness_btc_train.csv'):
    df = pd.DataFrame(news_data)
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"Data successfully saved to {filename}")

# Collect news information
news_data = []
try:
    while True:
        wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[contains(@class, "NewsWrap-sc")]')))
        news_items = driver.find_elements(By.XPATH, '//div[contains(@class, "NewsWrap-sc")]')
        for item in news_items:
            datetime = item.find_element(By.XPATH, './/div[contains(@class, "TimeDisplay-sc")]').text
            header = item.find_element(By.XPATH, './/h3[contains(@class, "Header-sc")]').text
            content = item.find_element(By.XPATH, './/div[contains(@class, "ContentsWrap-sc")]').text
            news_data.append({'datetime': datetime, 'header': header, 'content': content})
        if not can_click_more():
            break
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()
    save_to_csv(news_data)  # Save data to CSV upon finishing or in case of an exception

# Printing collected news data for debugging
for news in news_data:
    print(news)
