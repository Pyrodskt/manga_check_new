import requests
from bs4 import BeautifulSoup

class MangarockteamParser():
    def __init__(self, url, current):
        self.name = "MangaRockTeam Parser"
        self.url = url
        self.current = current
        self.last = 0
        self.results = []
        self.pages = []
        self.search(self.url)


    def search(self, url):
        req = requests.get(url)
        page = req.content
        soup = BeautifulSoup(page, features="html.parser")        
        for i in soup.find_all('li', {'class': 'wp-manga-chapter'}):
            self.results.append(i.find('a').text)


