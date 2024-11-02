import datetime

import requests
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

url = "https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/traffic_information/traffic-cameras/woodlands.html#trafficCameras"

driver_service = Service(executable_path=r"C:\Users\Yu Zen\Documents\Coding\chromedriver-win64\chromedriver.exe")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # Set user agent
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("window-size=1024,768")
chrome_options.add_argument("--no-sandbox")

def getjpg(url):
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(2)
    snippet = driver.find_element(By.CSS_SELECTOR,"img[alt='View from Woodlands Causeway (Towards Johor)']")
    snippet_src = snippet.get_attribute('src')
    # print(snippet_src)
    response = requests.get(snippet_src)
    now = datetime.now()
    day = now.strftime("%A")[:3]
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H-%M")
    filename = f'{day}_{date}_{time}.jpg'
    with open(filename, "wb") as file:
        file.write(response.content)
    driver.quit()
    print('yuh')
# print(getjpg(url))
now = datetime.datetime.now(datetime.UTC)
day = now.strftime("%A")[:3]
date = now.strftime("%m-%d")
time = now.strftime("%H:%M")
filename = f'{day}_{date}_{time}.jpg'
print(filename)

