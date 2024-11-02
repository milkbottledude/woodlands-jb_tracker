from google.cloud import storage
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from io import StringIO
import pandas as pd
from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path
import datetime
import requests

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # Sets user agent
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("window-size=1024,768")
chrome_options.add_argument("--no-sandbox")

url = 'https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/traffic_information/traffic-cameras/woodlands.html#trafficCameras'

BUCKET_NAME = 'frickubucket'
datetimes = 'datetimes.csv'
pics = 'snapshots/'
offset = datetime.timedelta(hours=8)

utc_now = datetime.datetime.now(datetime.UTC)
sg_time = utc_now + offset
day = sg_time.strftime("%A")[:3]
date = sg_time.strftime("%m-%d")
time = sg_time.strftime("%H-%M")

def adddatetime(bucketname, data):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucketname)
    blob = bucket.blob(data)
    with blob.open('r') as resume_file:
        df = pd.read_csv(StringIO(resume_file.read()))
    newrow = [day, date, time]
    df.loc[len(df)] = newrow
    buffer = StringIO()
    df.to_csv(buffer, index=False)
    blob.upload_from_string(buffer.getvalue(), content_type='text/csv')
    print('returned to sender')

def scrapeaddpic(url, bucketname, pics):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(2)
    snippet = driver.find_element(By.CSS_SELECTOR,"img[alt='View from Woodlands Causeway (Towards Johor)']")
    snippet_src = snippet.get_attribute('src')
    response = requests.get(snippet_src)
    #addtofolder portion from here onwards

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucketname)
    filename = f'{day}_{date}_{time}.jpg'
    print(filename)
    blob = bucket.blob(f'{pics}{filename}')
    blob.upload_from_string(response.content, content_type='image/jpeg')
    driver.quit()
    print('yuh')


adddatetime(BUCKET_NAME, datetimes)
scrapeaddpic(url, BUCKET_NAME, pics)