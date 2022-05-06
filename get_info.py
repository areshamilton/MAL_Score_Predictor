from textwrap import indent
from bs4 import BeautifulSoup
from lxml import etree
import requests
import time
from datetime import datetime


def get_info(link):
    result = []

    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'lxml')

    #title
    title = soup.find('h1', class_ = "title-name h1_bold_none").text.replace(',','')

    #score
    try:
        score = soup.find('span', itemprop = "ratingValue").text
    except AttributeError:
        score = '-1'

    #studio
    studios = soup.find('span', text = "Studios:")
    studio = studios.find_next_siblings('a')

    #source
    try:
        source = soup.find('span', text = "Source:").next_sibling.strip()
    except AttributeError:
        source = ''

    #This finds both genres and themes
    genres = soup.find_all('span', itemprop = 'genre')
    
    #demographic
    try:
        demographic = soup.find('span', text = "Demographic:").find_next_sibling().text
    except:
        demographic = ''
    
    # Actors
    actors = soup.find_all(class_ ="va-t ar pl4 pr4")

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
        result.append(each.text.replace('Japanese','').replace(',','').strip('\n'))
    
    # Remove stop words and punctuation before appending to show info
    stopWords = ['the', 'a', 'of', 'and', 'to', 'in', 'that', 
                'is', 'for', 'be', 'an', 'no', 'wo', 'ni', 'ga', ',']
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    titleWords = title.lower()
    for ele in titleWords:
        if ele in punc:
            titleWords = titleWords.replace(ele,'')
    titleWords = titleWords.split()
    for each in stopWords:
        if (each in titleWords):
            titleWords.remove(each)
    for each in titleWords:
        result.append(each)
    
    #print(result)
    return result


def main():
    startTime = datetime.now()
    links = []
    with open('anime_2012_2019.csv', 'r', encoding='utf-8') as reader:
        for line in reader.readlines():
            links.append((line.strip('\n')))

    with open('training.csv', 'a', encoding='utf-8') as writer:
        for link in links:
            output = get_info(link)
            writer.write(str(output).strip('[]')+'\n')
            print('Scrapping --> {0} success!!!'.format(link))
            time.sleep(4)
    endTime = datetime.now()

    print('Elapsed time: {hh:mm:ss.ms}',format(endTime - startTime))

if __name__=="__main__":
    main()
