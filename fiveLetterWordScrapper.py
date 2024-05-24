import requests
from bs4 import BeautifulSoup
import cloudscraper
from pathlib import Path

#open(Path.cwd()/ 'fiveWordList.txt', 'w').close()

def fiveLetterWordScrapper():
  pageNum = 1
  while pageNum != 51:
    url = 'https://www.thewordfinder.com/wordlist/5-letter-words/?dir=ascending&field=word&pg=' + str(pageNum) + '&size=5'
    scraper = cloudscraper.CloudScraper()
    page = scraper.get(url)
    while True:
      try:
          scraper = cloudscraper.CloudScraper()
          page = scraper.get(url)
          page.raise_for_status()
          break  
      except requests.exceptions.HTTPError as error:
          print(f'HTTP error occurred: {error}')
          continue
        
    soup = BeautifulSoup(page.content, 'html.parser')
    findWords = soup.find('ul', class_ = 'clearfix')
    arrWordList = [x.text.strip()[0:5] for x in findWords if any(x.text.strip())]
    with open(Path.cwd()/ 'fiveWordList.txt', 'a') as wordList:
      for word in arrWordList:
        wordList.write(word.lower() + '\n')

    pageNum += 1


fiveLetterWordScrapper()





