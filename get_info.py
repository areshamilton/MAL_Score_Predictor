import re
from textwrap import indent
from bs4 import BeautifulSoup
from xml.dom import minidom
from xml.etree import ElementTree as ET
from lxml import etree
import os
import requests

def get_info(link):
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')
    title = soup.find('h1', class_ = "title-name h1_bold_none").text
    score = soup.find('span', itemprop = "ratingValue").text
    studio = soup.find('span', text = "Studios:").find_next_sibling().text
    source = soup.find('span', text = "Source:").next_sibling.strip()
    genre = soup.find('span', text = "Genres:")
    genres = genre.find_next_siblings('span', itemprop = "genre")
    demographic = soup.find('span', text = "Demographic:").find_next_sibling().text
    actors = soup.find_all(class_ ="va-t ar pl4 pr4")
    theme = soup.find('span', text = "Themes:")
    themes = theme.find_next_siblings('span', itemprop = 'genre')

    print(title)
    print(score)
    print(studio)
    print(source)
    print(demographic)
    for each in genres:
        print(each.text)
    for each in actors:
        print(each.text)
    for each in themes:
        print(each.text)



def main():
    get_info('https://myanimelist.net/anime/48736/Sono_Bisque_Doll_wa_Koi_wo_Suru')

if __name__=="__main__":
    main()
