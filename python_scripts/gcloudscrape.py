from datetime import datetime
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from google.cloud import storage
from io import StringIO
import pandas as pd
import chromedriver_binary  # Adds chromedriver binary to path

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

url = 'https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/traffic_information/traffic-cameras/woodlands.html#trafficCameras'

BUCKET_NAME = 'frickubucket'
datetimes = 'datetimes.csv'
pics = 'snapshots/'
towardsbke = 'towardsbkesnapshot/'
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
    newrow = [date, time, day]
    df.loc[len(df)] = newrow
    buffer = StringIO()
    df.to_csv(buffer, index=False)
    blob.upload_from_string(buffer.getvalue(), content_type='text/csv')
    print('returned to sender')


def scrapeaddpic(url, bucketname, pics, towardsbke):
    print('scraping')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(2)

    snippet = driver.find_element(By.CSS_SELECTOR, "img[alt='View from Woodlands Causeway (Towards Johor)']")
    snippet_bke = driver.find_element(By.CSS_SELECTOR, "img[alt='View from Woodlands Checkpoint (Towards BKE)']")
    print('snippet done')
    snippet_src = snippet.get_attribute('src')
    snippet_bke_src = snippet_bke.get_attribute('src')
    print('get attribute done')
    response = requests.get(snippet_src)
    response_bke = requests.get(snippet_bke_src)
    print('request done')
    # addtofolder portion from here onwards
    print('adding to folder')
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucketname)

    filename = f'{date}_{time}_{day}.jpg'
    print(filename)
    bke_filename = f'{date}_{time}_{day}_bke.jpg'
    print(bke_filename)

    blob = bucket.blob(f'{pics}{filename}')
    blob.upload_from_string(response.content, content_type='image/jpeg')
    print('first blob uploaded')
    blob_bke = bucket.blob(f'{towardsbke}{bke_filename}')
    blob_bke.upload_from_string(response_bke.content, content_type='image/jpeg')
    print('bke blob uploaded')
    driver.quit()
    print('yuh')


def execute(request):
    scrapeaddpic(url, BUCKET_NAME, pics, towardsbke)
    print('scrapesuccess')
    adddatetime(BUCKET_NAME, datetimes)
    print('adddatetime success')
    return "Success", 200  # Return a success message and HTTP 200 status
