# Import packages

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup

links = [] # Empty links bucket
maxPage = 250 # Number of pages to scrape before stopping

first_next_path = "/html[1]/body[1]/div[5]/div[2]/div[5]/div[1]/div[2]/span[1]/a[5]" # xpath for 'next' button the first page
next_next_paths = "/html[1]/body[1]/div[5]/div[2]/div[5]/div[1]/div[2]/span[1]/a[6]" # xpath for 'next' button on subsequent pages

# Initiate ChromeDriver

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(chrome_options = options)
driver.get('http://newssearch.chinadaily.com.cn/en/search?query=tariff')

# Scrape links on first page

elems = driver.find_elements_by_xpath("//div[@class='art_detail']//h4//a") # Find divs with class .art_detail, take the h4, take the a
for elem in elems:
    links.append(elem.get_attribute("href")) # Extract href attribute from each a
print(len(links))

# Find and click the next button

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, first_next_path)))
next_button = driver.find_element_by_xpath(first_next_path)
next_button.click()  # Clicking button

# Scrape links in each subsequent page

for _ in range(maxPage):
    sleep(1)
    try:
        elems = driver.find_elements_by_xpath("//div[@class='art_detail']//h4//a")
        for elem in elems:
            links.append(elem.get_attribute("href"))
        print(len(links))
    except Exception as elem:
        print(elem)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, next_next_paths)))
    next_button = driver.find_element_by_xpath(next_next_paths)
    next_button.click()  # Clicking button

# Scrape the content from each link

from requests import get
from bs4 import BeautifulSoup

import pandas as pd
import csv

titles = []
dates = []
texts = []

for link in links:
    response = get(link)
    htmlSoup = BeautifulSoup(response.text, 'html.parser')

    # Sometimes stored in h1, sometimes in h2
    # Sometimes search results aren't news articles, and we don't care about them
    title = htmlSoup.find('h1')
    if title is not None:
        titles.append(title.get_text(strip = True))
    elif htmlSoup.find('h2') is not None:
        titles.append(htmlSoup.find('h2').get_text(strip = True))
    else:
        titles.append("NA")

    dateObj = htmlSoup.find('div', {"class": "info"})
    if dateObj is not None:
        dates.append(dateObj.get_text(strip = True).split(':', 1)[1][1:12].strip())
        # The character positions shift: when we go from 1 to 12, we will either get
        # an extra leading space or a trailing space. strip() gets rid of this space
    else:
        dates.append('1970-01-01')
        # Sometimes a search result isn't a normal news article, and we don't care about them

    textObj = htmlSoup.find('div', {"id": "Content"})
    if textObj is not None:
        texts.append(textObj.get_text(strip = True, separator = ' '))
    else:
        texts.append('NotAnArticle')

    print("Progress: " + str(len(titles)))
    sleep(1) # Prevent server timeout

df = pd.DataFrame({'link': links, 'title': titles, 'date': dates, 'text': texts})
df['text'] = df['text'].str.replace('\n', ' ')

df.to_csv('chinaDailyOutput_tariff.csv')