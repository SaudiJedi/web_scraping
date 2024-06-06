# Packages to be imported
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import httpx
import asyncio
from bs4 import BeautifulSoup
import lxml
import pandas as pd
import re
import json
import boto3
from botocore.exceptions import NoCredentialsError
import os

#Adding headless Selenium
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')


# Headers to pypass website
# Modify headers depending on your website restrictions
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
}

# This list will then be holding all the data 
# and transformed to a csv file
dataset = []

# Async requests to urls 
async def async_requests(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout= 10)
        return response

# Using async calls to extract
async def main():
    # Handling first page where all products listed
    # This way it can handle dynamic web pages
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("<landing_page_URL>")
    time.sleep(1)
    
    # Extending Webpage
    extend_page_button = '<your_css_selector_of_the_load_more_button>'
    flag = True
    while flag == True:
        try:
            show_more_button = driver.find_element(
                By.CSS_SELECTOR, extend_page_button)
            show_more_button.click()
            time.sleep(1)
        except:
            flag = False

    # Identifying the ul by the CSS Selector in which URLs gets extracted
    parent_element = driver.find_element(
        By.CSS_SELECTOR, '<css_selector_of_the_products_list>')

    # Taking the URLs from each li by using the XPath for the URLs
    child_elements = parent_element.find_elements(By.XPATH, './/a')

    # Process the URLs
    urls = []
    for element in child_elements:
        url = element.get_attribute('href')
        urls.append(url)

    print('URLs extraction completed!')
    print(f'Number of URLs: {len(urls)}')
    
    # Fetch data from each URL asynchronously
    tasks = [async_requests(url) for url in urls]
    results = await asyncio.gather(*tasks)

    # Data Extraction
    for response in results:
        soup = BeautifulSoup(response.content, 'html.parser')
        dom = lxml.etree.HTML(str(soup))
        

        # Handle special cases of XPATHs before processing data
        # (Best Practice)


        # Data extraction
        # This dict is then to be stored as one row
        # When dataset gets transformed to a pandas DataFrame
        data = {
            # You can add all the data needed to be extracted
            # example
            'data_field_1': dom.xpath('<xpath_of_the_element>')
        }
        global dataset
        dataset.append(data)

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print(f'Extraction completed with time taken: {end-start}\nData extracted count: {len(dataset)}')

    # This now will transform the list to a DataFrame
    df = pd.DataFrame(dataset)
    

    # Your data cleaning happens here
    # You can use regex to clean unwanted text
    # visit https://regexr.com/ to make the pattern you want


    # Be careful with the encoding and test the output csv
    # before using the code to send the csv to s3 with boto3
    output_dir = '/app/output'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'dataset.csv')
    df.to_csv(output_path, encoding='latin-1', index=False)
    print(f'File: {output_path} has been created!') 


    # Now to the process of loading the csv file to the s3 bucket

    # Initialize a session using Amazon S3
    s3 = boto3.client('s3')

    # Your bucket name
    bucket_name = 'YOUR_BUCKET_NAME'

    # The path to the CSV file on your local machine
    local_file_path = '/app/dataset.csv'

    # The name you want the file to have in S3
    s3_file_name = 'YOUR_S3_FILE_NAME.csv'

    # Upload file to S3
    try:
        s3.upload_file(local_file_path, bucket_name, s3_file_name)
        print(f"File {local_file_path} uploaded to {bucket_name} as {s3_file_name}")
    except FileNotFoundError:
        print(f"The file {local_file_path} was not found.")
    except NoCredentialsError:
        print("Credentials not available for AWS S3.")
    except Exception as e:
        print(f"An error occurred: {e}")
    