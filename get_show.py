from attr import attr
from bs4 import BeautifulSoup, SoupStrainer
import requests

html_text = requests.get('https://myanimelist.net/anime/season/2021/winter').text
soup = BeautifulSoup(html_text, 'lxml')

this_season = soup.find_all('div', class_ = 'js-categories-seasonal')
#shows = BeautifulSoup(this_season, 'lxml')
print(this_season)



