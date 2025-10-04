from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from world

# Start the driver
driver = webdriver.Chrome()

# Go to your page
driver.get("https://www.nytimes.com/games/wordle/index.html")

# Optional: wait for the element (recommended)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Wait for the parent "Row 1" to be present
row = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@aria-label="Row 1"]'))
)

for _ in range(5):
