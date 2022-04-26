import re
from textwrap import indent
from bs4 import BeautifulSoup
from xml.dom import minidom
from xml.etree import ElementTree as ET
from lxml import etree
import os
import requests

def get_show(link):
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


    tree = ET.parse('animelist.xml')
    root = tree.getroot()

    anime = ET.Element("ANIME")
    item1 = ET.SubElement(anime, 'title')
    item1.text = title

    item2 = ET.SubElement(anime, 'score')
    item2.text = score

    item3 = ET.SubElement(anime, 'studio')
    item3.text = studio

    x = etree.parse(root)
    pretty_xml= etree.tostring(x, pretty_print=True, encoding=str)
    print(pretty_xml)

    
    ugly = ET.tostring(anime, 'utf-8')
    pretty = minidom.parseString(ugly).toprettyxml(indent="\t")
    root.append(anime)
    ET.dump(tree)
    # # with open("animelist.xml", "w") as f:
    # #     f.write(pretty)

    # with open("animelist.xml", 'w') as output:
    #     output.write(pretty)


    #tree.write("animelist.xml", encoding="utf-8")
    # ugly = ET.tostring(tree, 'utf-8')
    # pretty = minidom.parseString(ugly)
    # print(pretty.toprettyxml(indent="\t"))

    # file1 = open("animelist.xml", 'a')
    # file1.writelines(title)
    # file1.close()


def main():
    get_show('https://myanimelist.net/anime/48736/Sono_Bisque_Doll_wa_Koi_wo_Suru')

if __name__=="__main__":
    main()
