# Import packages

from requests import get
from bs4 import BeautifulSoup
from time import sleep

import pandas as pd
import csv

# Setup

links = [] # empty bucket for links
term = 'tariff' # search term
maxPage = 100 # max number of pages to go through before stopping

# Scrape links

for j in range(maxPage):
    url = 'http://search.people.com.cn/language/search.do?pageNum=' + str(j + 1) + '&keyword=' + term + '&siteName=english&dateFlag=true&a=&b=&c=&d=&e=&f='

    response = get(url)
    htmlSoup = BeautifulSoup(response.text, 'html.parser')

    linkContainers = htmlSoup.find_all('ul', {'class': 'on1'}) # Links to articles are stored in unordered lists with class 'on1'
    for c in linkContainers:
        links.append(c.a.get('href')) # Get only the links in each ul

    print(len(links)) # Show progress
    sleep(1) # Prevent server timeout

print("Number of links scraped: " + str(len(links)))

# Scrape everything else

titles = []
dates = []
texts = []

for link in links:
    response = get(link)
    htmlSoup = BeautifulSoup(response.text, 'html.parser')

    # Sometimes the title is in h1, sometimes it's in h2
    title = htmlSoup.find('h1')
    if title is not None:
        titles.append(title.get_text(strip = True))
    else:
        title = htmlSoup.find('h2')
        titles.append(title.get_text(strip = True))

    # The text that has the date and time is two siblings after the title element
    # Extract that text, then find the ':' in the time, then move 4 characters to the right, which is where the date starts
    date = title.next_sibling.next_sibling.get_text(strip = True).split(':', 1)[1][4:]
    dates.append(date)

    soup = htmlSoup.find('div', class_ = 'wb_12')
    for aside in soup.find_all('center'):
        aside.decompose()
    
    text = soup.get_text(strip = True, separator = ' ') # Add spaces between p tags
    texts.append(text)

    print("Progress: " + str(len(titles)))
    sleep(2)

df = pd.DataFrame({'link': links, 'title': titles, 'date': dates, 'text': texts})
df['text'] = df['text'].str.replace('\n', ' ')

df.to_csv('peoplesDailyOutput_tariff.csv')
