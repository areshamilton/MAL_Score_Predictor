from attr import attr
from bs4 import BeautifulSoup, SoupStrainer
from get_info import *
import requests
import time

def get_show(link):
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')

    this_season = soup.find('div', class_ = 'seasonal-anime-list js-seasonal-anime-list js-seasonal-anime-list-key-1')
    shows = this_season.find_all('a', class_ = 'link-title')

    output_filename = 'show_links.csv'
    with open(output_filename, 'a', encoding='utf-8') as file_object:
        for each in shows:
            file_object.write(each.get('href') + '\n')
            #print(each.get('href'))

def main():

    seasons = ['winter', 'spring', 'summer', 'fall']
    for year in range(2012, 2020):
        for season in seasons:
            link = 'https://myanimelist.net/anime/season/' + str(year) + '/' + season
            get_show(link)
            print('Scrapping show links for season {0} year {1} -> success!'.format(season,year))
            time.sleep(2)

if __name__=="__main__":
    main()

