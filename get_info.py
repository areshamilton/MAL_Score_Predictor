import re
from textwrap import indent
from bs4 import BeautifulSoup
from xml.dom import minidom
from xml.etree import ElementTree as ET
from lxml import etree
import os
import requests

def get_info(link):
    result = []

    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')

    title = soup.find('h1', class_ = "title-name h1_bold_none").text

    #score
    try:
        score = soup.find('span', itemprop = "ratingValue").text
    except AttributeError:
        score = '-1'

    #studio
    studios = soup.find('span', text = "Studios:")
    studio = studios.find_next_siblings('a')

    try:
        source = soup.find('span', text = "Source:").next_sibling.strip()
    except AttributeError:
        source = ''

    #This finds both genres and themes
    genres = soup.find_all('span', itemprop = 'genre')
    
    try:
        demographic = soup.find('span', text = "Demographic:").find_next_sibling().text
    except:
        demographic = ''
    
    actors = soup.find_all(class_ ="va-t ar pl4 pr4")

    #print(studio)

    #build the result
    result.append(title)
    result.append(score)
    if studio[0].text != 'add some':
        for each in studio:
            result.append(each.text)
    if source != '':
        result.append(source)
    if demographic != '':
        result.append(demographic)
    for each in genres:
        result.append(each.text)
    for each in actors:
        result.append(each.text.replace('Japanese','').strip('\n'))
    
    #print(result)
    return result


def main():
    output = get_info('https://myanimelist.net/anime/50380/Paripi_Koumei')

    output_filename = 'output.csv'
    with open(output_filename, 'a') as file_object:
        file_object.write(str(output).strip('[]')+'\n')


if __name__=="__main__":
    main()
