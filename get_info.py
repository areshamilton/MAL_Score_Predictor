from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://myanimelist.net/anime/47778/Kimetsu_no_Yaiba__Yuukaku-hen').text
soup = BeautifulSoup(html_text, 'lxml')
title = soup.find('h1', class_ = "title-name h1_bold_none").text
score = soup.find('span', itemprop = "ratingValue").text
studio = soup.find('span', text = "Studios:").find_next_sibling().text
source = soup.find('span', text = "Source:").next_sibling.strip()
genre = soup.find('span', text = "Genres:")
genres = genre.find_next_siblings('span', itemprop = "genre")
demographic = soup.find('span', text = "Demographic:").find_next_sibling().text
actors = soup.find_all(class_ ="va-t ar pl4 pr4")

print(title)
print(score)
print(studio)
print(source)
for each in genres:
    print(each.text)
for each in actors:
    print(each.text)
