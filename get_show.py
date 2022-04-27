from attr import attr
from bs4 import BeautifulSoup, SoupStrainer
from get_info import *
import requests

# html_text = requests.get('https://myanimelist.net/anime/season/2021/winter').text
# soup = BeautifulSoup(html_text, 'lxml')

# this_season = soup.find_all('div', class_ = 'js-categories-seasonal')
# #shows = BeautifulSoup(this_season, 'lxml')
# print(this_season)

def main():
    get_info('https://myanimelist.net/anime/48736/Sono_Bisque_Doll_wa_Koi_wo_Suru')

if __name__=="__main__":
    main()

