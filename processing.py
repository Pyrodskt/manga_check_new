import requests
from bs4 import BeautifulSoup
import re
import json
from mangas import Mangas

class Processing:
    def __init__(self):
        self.urls = []
        self.config_path = './config.json'
        self.currentPage = 0
        self.pages = []
        self.visited = []
        self.nextPage = 0
        self.results = []
        
        self.search("https://mangarockteam.com/manga/the-rebirth-of-an-8th-circled-mage/")



    def search(self, url):
        req = requests.get(url)
        page = req.content
        soup = BeautifulSoup(page, features="html.parser")        
        for i in soup.find_all('li', {'class': 'wp-manga-chapter'}):
            self.results.append(i.find('a').text)

        for i in self.results:
            print(i)
    