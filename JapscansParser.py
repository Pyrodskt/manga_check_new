import requests
from bs4 import BeautifulSoup
import re


class JapscansParser():
    def __init__(self, url, current):
        self.name = "Japscans Parser"
        self.url = url
        self.current = current
        self.results = []
        self.pages = []
        self.search(self.url)

    def search(self, url):
        req = requests.get(url)
        page = req.content
        soup = BeautifulSoup(page, features="html.parser")
        result = soup.find_all("div", {"class": "chapters_list text-truncate"})
        for res in result:
            self.results.append(res.find("a").text.replace('\t', '').replace('\n', ''))

