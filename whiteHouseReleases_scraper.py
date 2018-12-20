# Import packages

from requests import get
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np
import csv

# Setup and get the number of pages of posts

links = [] # bucket for links

url = 'https://www.whitehouse.gov/news/' # starting page

response = get(url)
htmlSoup = BeautifulSoup(response.text, 'html.parser')

maxPage = int(htmlSoup.find_all('a', class_ = 'page-numbers')[-1].text) # Last page number in the nav part is the total number of pages

# Scrape all links

for i in range(maxPage):
    url = 'https://www.whitehouse.gov/news/page/' + str(i + 1) + '/'

    response = get(url)
    htmlSoup = BeautifulSoup(response.text, 'html.parser')

    linkContainers = htmlSoup.find_all('h2') # In each page of links, links are in the href within h2
    for c in linkContainers:
        links.append(c.a.get('href'))

    print(len(links))

print("Final length: " + str(len(links)))

# Scrape content of pages

titles = []
categories = []
types = []
dates = []
texts = []

for link in links:
    response = get(link)
    htmlSoup = BeautifulSoup(response.text, 'html.parser')

    titles.append(htmlSoup.find('h1', class_ = 'page-header__title').get_text(strip = True))

    # Some pages are different and don't have all types a type or category label, so for these, we ignore them
    if htmlSoup.find('p', class_ = 'page-header__section') is not None:
        types.append(htmlSoup.find('p', class_ = 'page-header__section').get_text(strip = True))
    else:
        types.append(np.nan)

    if htmlSoup.find('div', class_ = 'meta__issue') is not None:
        categories.append(htmlSoup.find('div', class_ = 'meta__issue').get_text(strip = True))
    else:
        categories.append(np.nan)

    # White House website stores data in HTML5 tags such as 'time'
    # Makes things like this super easy, beacuse it's the first (and only) one on the page!
    dates.append(htmlSoup.find('time').get_text(strip = True))

    # Social media sharing icons are located in 'asides', but we don't want them
    # Decompose gets rid of them in the soup
    soup = htmlSoup.find('div', class_ = 'page-content__content')
    for aside in soup.find_all('aside'):
        aside.decompose()
    
    # Remove extraneous characters
    text = soup.get_text(strip = True)
    text = text.replace('.', '. ')
    text = text.replace('\xa0', ' ')
    texts.append(text)

# Create a dataframe and export to csv
df = pd.DataFrame({'link': links, 'title': titles, 'date': dates, 'type': types, 'category': categories, 'text': texts})
df['text'] = df['text'].str.replace('\n', ' ')

df.to_csv('output.csv')

# Output just the links for convenience
dfLinks = df[['link', 'title', 'date']]
dfLinks.to_csv('links.csv')